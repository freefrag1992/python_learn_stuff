#!/usr/bin/env python3
"""
Twitch Code Finder
==================
Liest den Chat vieler Twitch-Kanäle live mit (anonym, ohne Login) und listet
alle Codes, die zum eingestellten Suchmuster passen, untereinander auf –
jeweils mit "Kopieren"-Button. Neueste Codes stehen oben.

Dateien (alle im Ordner dieses Skripts):
  kanaele.txt        Kanalliste (ein Kanal pro Zeile, Links/@name/#name gehen auch)
  alarm.mp3          Alarmton bei jedem neuen Code (mp3/wav; fehlt sie -> Systemton)
  einstellungen.txt  wird automatisch gespeichert und beim Start wieder geladen

Suchmuster (im Fenster, gilt sofort – auch während der Suche):
  Einfach einen Beispielcode eintragen, z. B.  XXXX-XXXX-XXXXX-XXXX-XXXX
  - jeder Buchstabe/jede Ziffer  = beliebiges Zeichen (A-Z, 0-9)
  - #  = nur eine Ziffer          - ?  = nur ein Buchstabe
  - alles andere (z. B. "-")     = muss genau so vorkommen
  Optional: Haken "Regex" für einen regulären Ausdruck.

Start:   python twitch_code_finder.py
Benötigt nur Python 3 (tkinter ist meist dabei; unter Linux ggf. `sudo apt install python3-tk`).
"""

import json
import os
import queue
import random
import re
import shutil
import socket
import ssl
import subprocess
import sys
import threading
import time
import warnings
import tkinter as tk
import tkinter.font as tkfont
from collections import deque
from datetime import datetime
from tkinter import filedialog, ttk

IRC_HOST = "irc.chat.twitch.tv"
IRC_PORT = 6697  # TLS

# Twitch erlaubt 20 JOINs pro 10 Sekunden -> wir bleiben mit Puffer darunter
JOIN_LIMIT = 18
JOIN_WINDOW = 10.5

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "einstellungen.txt")
OLD_SETTINGS_JSON = os.path.join(BASE_DIR, "twitch_code_finder.json")   # nur für die Übernahme alter Einstellungen
LOG_FILE = os.path.join(BASE_DIR, "twitch_chatlog.txt")
DEFAULT_CHANNEL_NAME = "kanaele.txt"

PRIVMSG_RE = re.compile(r"^(?:@\S+ )?:(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #(\w+) :(.*)$")
JOIN_RE = re.compile(r"^:(\w+)!\w+@\w+\.tmi\.twitch\.tv JOIN #(\w+)\s*$")

TEMPLATE = """\
# Twitch-Kanäle für den Code Finder
# Ein Kanal pro Zeile (oder mit Komma getrennt). Auch Links wie https://twitch.tv/name gehen.
# Zeilen, die mit "// " oder "# " (Raute + Leerzeichen) beginnen, sind Kommentare.
# Änderungen werden bei laufendem Programm automatisch übernommen.
# Ersetze die Beispiele unten durch deine Liste (z. B. die Top-100 WoW-Streamer):

xaryu
https://www.twitch.tv/method
"""


# ============================ Pfade =====================================
def resolve_path(p):
    """Relative Pfade gelten ab dem Ordner des Programms."""
    p = os.path.expanduser((p or "").strip())
    if not p:
        return ""
    return p if os.path.isabs(p) else os.path.join(BASE_DIR, p)


def to_stored_path(p):
    """Liegt die Datei im Programmordner, wird nur der Dateiname gespeichert."""
    p = (p or "").strip()
    if p and os.path.isabs(p) and os.path.normcase(os.path.dirname(p)) == os.path.normcase(BASE_DIR):
        return os.path.basename(p)
    return p


# ====================== Kanalliste einlesen =============================
URL_RE = re.compile(r"(?:https?://)?(?:www\.|m\.)?twitch\.tv/([A-Za-z0-9_]{1,25})", re.IGNORECASE)
NAME_RE = re.compile(r"[A-Za-z0-9_]{4,25}")  # Twitch-Namen: 4–25 Zeichen


def _first_channel(piece):
    """Erster brauchbarer Kanalname in einem Textstück (oder None)."""
    m = URL_RE.search(piece)
    if m:
        return m.group(1).lower()
    for tok in re.split(r"[\s|;]+", piece):
        tok = tok.strip("\"'()[]{}<>*•·-–—.:").lstrip("#@")
        if NAME_RE.fullmatch(tok) and not tok.isdigit():
            return tok.lower()
    return None


def parse_channels(text):
    """Wandelt beliebigen Listentext in eine eindeutige Liste von Kanalnamen (Reihenfolge bleibt)."""
    seen, out = set(), []
    for raw in text.splitlines():
        line = raw.strip().lstrip("\ufeff")
        if not line or line.startswith("//") or re.match(r"#(\s|#|$)", line):
            continue
        line = re.sub(r"(?<!:)//.*$", "", line)   # Kommentar am Zeilenende
        line = re.sub(r"\s#\s.*$", "", line)
        pieces = line.split(",") if "," in line else [line]
        for piece in pieces:
            name = _first_channel(piece)
            if name and name not in seen:
                seen.add(name)
                out.append(name)
    return out


def read_text_file(path):
    with open(path, "rb") as f:
        raw = f.read()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):   # z. B. von PowerShell erzeugt
        return raw.decode("utf-16", errors="replace")
    return raw.decode("utf-8-sig", errors="replace")


def ensure_channel_file(path):
    """Legt die Kanalliste mit Vorlage an, falls sie fehlt. Gibt True zurück, wenn sie existiert."""
    if os.path.exists(path):
        return True
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE)
        return True
    except OSError:
        return False


def open_in_editor(path):
    if sys.platform.startswith("win"):
        os.startfile(path)  # noqa
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


# ========================== Suchmuster ==================================
class CodeMatcher:
    """Kapselt das kompilierte Suchmuster; wird live im laufenden Worker ausgetauscht."""

    def __init__(self, rx, upper):
        self.rx = rx
        self.upper = upper

    def find(self, text):
        out = []
        for m in self.rx.finditer(text):
            s = m.group(0)
            if s:
                out.append(s.upper() if self.upper else s)
        return out


def mask_to_regex(mask):
    """Beispielcode-Maske -> Regex. Buchstabe/Ziffer = beliebig, # = Ziffer, ? = Buchstabe, Rest wörtlich."""
    body = []
    for ch in mask:
        if ch == "#":
            body.append("[0-9]")
        elif ch == "?":
            body.append("[A-Za-z]")
        elif ch.isascii() and ch.isalnum():
            body.append("[A-Za-z0-9]")
        else:
            body.append(re.escape(ch))
    # nicht mitten in einem längeren Zeichen-/Bindestrich-Gebilde treffen
    return r"(?<![A-Za-z0-9-])" + "".join(body) + r"(?![A-Za-z0-9-])"


def build_matcher(text, regex_mode):
    """-> (CodeMatcher, None) oder (None, Fehlertext)"""
    text = (text or "").strip()
    if not text:
        return None, "Das Suchmuster ist leer."
    try:
        if regex_mode:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")   # z. B. "possible nested set" beim Tippen
                rx = re.compile(text, re.IGNORECASE)
            upper = False
        else:
            if not any(c == "#" or c == "?" or (c.isascii() and c.isalnum()) for c in text):
                return None, "Das Muster braucht mindestens einen Platzhalter (Buchstabe, Ziffer, # oder ?)."
            rx = re.compile(mask_to_regex(text))
            upper = True
    except re.error as e:
        return None, f"Ungültiger regulärer Ausdruck: {e}"
    if rx.search(""):
        return None, "Das Muster darf nicht auf leeren Text passen."
    return CodeMatcher(rx, upper), None


# ========================= Einstellungen (.txt) =========================
DEFAULTS = {
    "kanalliste": DEFAULT_CHANNEL_NAME,
    "muster": "XXXX-XXXX-XXXXX-XXXX-XXXX",
    "regex_modus": "nein",
    "regex_muster": r"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}-[A-Z0-9]{4}-[A-Z0-9]{4}",
    "automatisch_kopieren": "ja",
    "ton": "ja",
    "tondatei": "alarm.mp3",
    "immer_im_vordergrund": "nein",
    "chat_loggen": "nein",
    "fenstergroesse": "700x760",
}

SETTINGS_HEADER = """\
# Einstellungen für den Twitch Code Finder
# Diese Datei wird vom Programm automatisch gespeichert und beim Start gelesen.
# Du kannst sie auch von Hand ändern – aber nur, solange das Programm geschlossen ist,
# sonst wird deine Änderung beim nächsten automatischen Speichern überschrieben.
# Format:  schlüssel = wert      (Ja/Nein-Werte: ja oder nein)
#
# kanalliste            Textdatei mit den Twitch-Kanälen (im Programmordner oder voller Pfad)
# muster                Suchmuster als Beispielcode: Buchstabe/Ziffer = beliebiges Zeichen (A-Z, 0-9),
#                       # = nur Ziffer, ? = nur Buchstabe, alles andere (z. B. -) muss genau so vorkommen
# regex_modus           ja = stattdessen 'regex_muster' (regulärer Ausdruck) verwenden
# tondatei              Audiodatei für den Alarm (mp3/wav; im Programmordner oder voller Pfad)
# ton                   Alarm bei neuem Code abspielen
# automatisch_kopieren  neuesten Code sofort in die Zwischenablage legen
# chat_loggen           kompletten Chat in twitch_chatlog.txt mitschreiben

"""

SETTING_ORDER = ["kanalliste", "muster", "regex_modus", "regex_muster", "automatisch_kopieren", "ton",
                 "tondatei", "immer_im_vordergrund", "chat_loggen", "fenstergroesse"]


def parse_bool(value, default):
    v = str(value).strip().lower()
    if v in ("ja", "j", "true", "1", "an", "ein", "yes", "y", "on"):
        return True
    if v in ("nein", "n", "false", "0", "aus", "no", "off"):
        return False
    return default


def fmt_bool(b):
    return "ja" if b else "nein"


def load_settings():
    """Liest einstellungen.txt (schlüssel = wert). Übernimmt beim ersten Start ggf. die alte JSON-Datei."""
    cfg = {}
    try:
        text = read_text_file(SETTINGS_FILE)
    except OSError:
        text = None
    if text is not None:
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith(("#", ";", "//")) or "=" not in line:
                continue
            key, value = line.split("=", 1)
            cfg[key.strip().lower()] = value.strip()
        return cfg
    try:  # Übernahme der Einstellungen früherer Versionen
        with open(OLD_SETTINGS_JSON, encoding="utf-8") as f:
            old = json.load(f)
        mapping = {"channel_file": "kanalliste", "auto_copy": "automatisch_kopieren", "sound": "ton",
                   "topmost": "immer_im_vordergrund", "log": "chat_loggen"}
        for k, new in mapping.items():
            if k in old:
                cfg[new] = fmt_bool(old[k]) if isinstance(old[k], bool) else str(old[k])
        if "kanalliste" in cfg:
            cfg["kanalliste"] = to_stored_path(cfg["kanalliste"])
    except Exception:
        pass
    return cfg


def save_settings(cfg):
    lines = [SETTINGS_HEADER.rstrip("\n"), ""]
    for key in SETTING_ORDER:
        value = str(cfg.get(key, DEFAULTS[key])).replace("\r", "").replace("\n", "")
        lines.append(f"{key} = {value}")
    tmp = SETTINGS_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        os.replace(tmp, SETTINGS_FILE)
        return True
    except OSError:
        return False


# ============================ Alarmton ==================================
def play_sound(path):
    """Spielt eine Audiodatei asynchron ab. True = Player wurde gestartet, False = nicht möglich."""
    if not path or not os.path.isfile(path):
        return False
    try:
        if sys.platform.startswith("win"):
            ext = os.path.splitext(path)[1].lower()
            if ext == ".wav":
                import winsound
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                return True
            import ctypes
            mci = ctypes.windll.winmm.mciSendStringW   # Windows-eigener Player, kann mp3 ohne Zusatzpakete
            mci("close code_alarm", None, 0, None)
            kind = "type mpegvideo " if ext == ".mp3" else ""
            if mci(f'open "{path}" {kind}alias code_alarm', None, 0, None) != 0:
                return False
            return mci("play code_alarm from 0", None, 0, None) == 0
        if sys.platform == "darwin":
            subprocess.Popen(["afplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        players = (["mpg123", "-q"], ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"],
                   ["mpv", "--no-video", "--really-quiet"], ["cvlc", "--play-and-exit", "--quiet"],
                   ["paplay"], ["aplay", "-q"])
        for cmd in players:
            if shutil.which(cmd[0]):
                subprocess.Popen(cmd + [path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
    except Exception:
        return False
    return False


# ============================ IRC-Worker ================================
class IrcWorker(threading.Thread):
    """Läuft im Hintergrund und schickt Ereignisse per Queue an die GUI."""

    def __init__(self, channels, out_q, matcher, log_enabled=False):
        super().__init__(daemon=True)
        self._wanted = list(channels)
        self._lock = threading.Lock()
        self.q = out_q
        self.matcher = matcher
        self.log_enabled = log_enabled
        self.stop_event = threading.Event()
        self.delay = 2
        self.logf = None
        self._last_flush = 0.0
        self._last_status = None
        self._reset_session()

    # ---- Steuerung von außen ----
    def stop(self):
        self.stop_event.set()

    def update_channels(self, channels):
        """Neue Kanalliste übernehmen (wird live per JOIN/PART umgesetzt)."""
        with self._lock:
            self._wanted = list(channels)

    def set_matcher(self, matcher):
        """Neues Suchmuster übernehmen (gilt ab der nächsten Chatnachricht)."""
        self.matcher = matcher

    # ---- intern ----
    def _reset_session(self):
        self.nick = f"justinfan{random.randint(10000, 99999)}"
        self.sent = set()        # Kanäle, für die ein JOIN geschickt wurde
        self.confirmed = set()   # Kanäle, deren Beitritt Twitch bestätigt hat
        self.join_times = deque()

    def _status(self, text):
        if text != self._last_status:
            self._last_status = text
            self.q.put((self, "status", text))

    @staticmethod
    def _send(sock, msg):
        sock.sendall((msg + "\r\n").encode("utf-8"))

    def run(self):
        try:
            self.logf = open(LOG_FILE, "a", encoding="utf-8")
        except OSError:
            self.logf = None
        try:
            while not self.stop_event.is_set():
                try:
                    self._session()
                except OSError:
                    if self.stop_event.is_set():
                        break
                    self._status(f"Verbindung weg – neuer Versuch in {self.delay}s …")
                    if self.stop_event.wait(self.delay):
                        break
                    self.delay = min(self.delay * 2, 60)
        finally:
            if self.logf:
                self.logf.close()

    def _session(self):
        self._status("Verbinde …")
        self._reset_session()
        raw = socket.create_connection((IRC_HOST, IRC_PORT), timeout=15)
        sock = ssl.create_default_context().wrap_socket(raw, server_hostname=IRC_HOST)
        sock.settimeout(0.5)  # kurzer Timeout: Joins nachschieben + "Stopp" greift schnell
        try:
            self._send(sock, "PASS SCHMOOZE")  # bei anonymem Login egal
            self._send(sock, f"NICK {self.nick}")

            buf, last = "", time.time()
            while not self.stop_event.is_set():
                self._sync_channels(sock)   # fällige JOINs/PARTs, ohne den Chat zu blockieren
                try:
                    data = sock.recv(4096)
                except (socket.timeout, TimeoutError):
                    if time.time() - last > 420:  # Twitch pingt ca. alle 5 Min.
                        raise ConnectionError("keine Daten mehr")
                    continue
                if not data:
                    raise ConnectionError("Verbindung geschlossen")
                last = time.time()
                self.delay = 2
                buf += data.decode("utf-8", errors="replace")
                while "\r\n" in buf:
                    line, buf = buf.split("\r\n", 1)
                    self._handle_line(sock, line)
        finally:
            try:
                sock.close()
            except OSError:
                pass

    def _sync_channels(self, sock):
        with self._lock:
            wanted = list(self._wanted)
        wanted_set = set(wanted)

        # entfernte Kanäle verlassen
        for ch in [c for c in self.sent if c not in wanted_set]:
            self._send(sock, f"PART #{ch}")
            self.sent.discard(ch)
            self.confirmed.discard(ch)

        # neue Kanäle betreten – ratenbegrenzt, Rest folgt in den nächsten Durchläufen
        now = time.time()
        while self.join_times and now - self.join_times[0] > JOIN_WINDOW:
            self.join_times.popleft()
        for ch in wanted:
            if ch in self.sent:
                continue
            if len(self.join_times) >= JOIN_LIMIT:
                break
            self._send(sock, f"JOIN #{ch}")
            self.sent.add(ch)
            self.join_times.append(now)

        total = len(wanted)
        open_joins = sum(1 for c in wanted if c not in self.sent)
        if open_joins:
            self._status(f"Verbunden – trete Kanälen bei … ({total - open_joins}/{total})")
        else:
            self._status(f"Verbunden – {len(self.confirmed & wanted_set)}/{total} Kanäle bestätigt")

    def _handle_line(self, sock, line):
        if line.startswith("PING"):
            self._send(sock, "PONG " + line[5:])
            return

        jm = JOIN_RE.match(line)
        if jm:
            if jm.group(1) == self.nick:
                self.confirmed.add(jm.group(2).lower())
            return

        m = PRIVMSG_RE.match(line)
        if not m:
            return
        user, channel, text = m.groups()
        now = datetime.now()
        if self.log_enabled and self.logf:
            self.logf.write(f"[{now:%Y-%m-%d %H:%M:%S}] #{channel} <{user}>: {text}\n")
            if time.time() - self._last_flush > 1.0:
                self.logf.flush()
                self._last_flush = time.time()
        matcher = self.matcher   # kann live durch die GUI ausgetauscht werden
        if matcher is None:
            return
        for code in matcher.find(text):
            self.q.put((self, "code", code, channel, user, f"{now:%H:%M:%S}"))


# ================================ GUI ===================================
MASK_HELP = ("Beispielcode eintragen: jeder Buchstabe und jede Ziffer steht für ein beliebiges Zeichen (A–Z, 0–9). "
             "# = nur Ziffer, ? = nur Buchstabe. Alles andere (z. B. Bindestriche) muss genau so vorkommen. "
             "Änderungen gelten sofort – auch während der Suche.")
REGEX_HELP = ("Regulärer Ausdruck (Python-Syntax), Groß-/Kleinschreibung egal. "
              "Beispiel: [A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}-[A-Z0-9]{4}-[A-Z0-9]{4}")
OK_COLOR = "#1e8449"
ERR_COLOR = "#c0392b"


class App:
    BG_NEW = "#fff3b0"   # frisch gefundener Code
    BG_OLD = "#f3f3f3"
    FG = "#111111"

    def __init__(self, root):
        self.root = root
        root.title("Twitch Code Finder")

        cfg = dict(DEFAULTS)
        cfg.update(load_settings())

        m = re.fullmatch(r"(\d{3,4})x(\d{3,4})", cfg["fenstergroesse"].strip())
        self._size = m.group(0) if m else DEFAULTS["fenstergroesse"]
        root.geometry(self._size)
        root.minsize(640, 460)

        self.q = queue.Queue()
        self.worker = None
        self.matcher = None
        self.rows = {}    # code -> dict
        self.order = []   # Zeilen, neueste zuerst
        self._file_sig = None
        self._save_job = None
        self._apply_job = None

        self.file_var = tk.StringVar(value=cfg["kanalliste"])
        self.mask_text = cfg["muster"]
        self.regex_text = cfg["regex_muster"]
        self.regex_mode_var = tk.BooleanVar(value=parse_bool(cfg["regex_modus"], False))
        self.pattern_var = tk.StringVar(value=self.regex_text if self.regex_mode_var.get() else self.mask_text)
        self.auto_copy_var = tk.BooleanVar(value=parse_bool(cfg["automatisch_kopieren"], True))
        self.sound_var = tk.BooleanVar(value=parse_bool(cfg["ton"], True))
        self.sound_file_var = tk.StringVar(value=cfg["tondatei"])
        self.topmost_var = tk.BooleanVar(value=parse_bool(cfg["immer_im_vordergrund"], False))
        self.log_var = tk.BooleanVar(value=parse_bool(cfg["chat_loggen"], False))
        self.status_var = tk.StringVar(value="Nicht verbunden")
        self.list_var = tk.StringVar(value="")
        self.count_var = tk.StringVar(value="Gefundene Codes: 0")
        self.pattern_status_var = tk.StringVar(value="")
        self.pattern_help_var = tk.StringVar(value="")

        if os.path.normcase(resolve_path(self.file_var.get())) == \
                os.path.normcase(os.path.join(BASE_DIR, DEFAULT_CHANNEL_NAME)):
            ensure_channel_file(resolve_path(self.file_var.get()))

        self.code_font = tkfont.nametofont("TkFixedFont").copy()
        self.code_font.configure(size=15, weight="bold")
        self.bold_font = tkfont.nametofont("TkDefaultFont").copy()
        self.bold_font.configure(weight="bold")

        self._build()
        self._apply_topmost()
        self._update_help()
        self._apply_pattern()

        # Änderungen sofort übernehmen bzw. automatisch speichern
        for var in (self.file_var, self.auto_copy_var, self.sound_var, self.sound_file_var,
                    self.topmost_var, self.log_var):
            var.trace_add("write", lambda *a: self._schedule_save())
        self.pattern_var.trace_add("write", self._on_pattern_write)
        self.regex_mode_var.trace_add("write", self._on_mode_change)

        root.protocol("WM_DELETE_WINDOW", self._close)
        root.after(100, self._poll)
        root.after(150, self._watch_file)
        self._save_settings()   # legt einstellungen.txt beim ersten Start gleich an

    # ---------------------------- Aufbau ------------------------------
    def _build(self):
        r = self.root

        # Kanalliste
        top = ttk.Frame(r, padding=(10, 10, 10, 2))
        top.pack(fill="x")
        ttk.Label(top, text="Kanalliste (.txt):").pack(side="left")
        ttk.Entry(top, textvariable=self.file_var).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(top, text="Durchsuchen …", command=self._browse).pack(side="left")
        ttk.Button(top, text="Bearbeiten", command=self._edit_file).pack(side="left", padx=4)
        self.btn = ttk.Button(top, text="Start", width=8, command=self._toggle)
        self.btn.pack(side="left")

        ttk.Label(r, textvariable=self.list_var, padding=(10, 0, 10, 0)).pack(fill="x")

        # Suchmuster
        pat = ttk.Frame(r, padding=(10, 8, 10, 0))
        pat.pack(fill="x")
        ttk.Label(pat, text="Suchmuster:").pack(side="left")
        self.pattern_entry = ttk.Entry(pat, textvariable=self.pattern_var, font=self.code_font)
        self.pattern_entry.pack(side="left", fill="x", expand=True, padx=6)
        ttk.Checkbutton(pat, text="Regex", variable=self.regex_mode_var).pack(side="left")

        self.pattern_status_lbl = ttk.Label(r, textvariable=self.pattern_status_var, padding=(10, 2, 10, 0))
        self.pattern_status_lbl.pack(fill="x")
        self.help_lbl = ttk.Label(r, textvariable=self.pattern_help_var, foreground="#888", justify="left",
                                  wraplength=640, padding=(10, 0, 10, 4))
        self.help_lbl.pack(fill="x")
        self.help_lbl.bind("<Configure>", lambda e: self.help_lbl.config(wraplength=max(200, e.width - 20)))

        # Alarmton
        snd = ttk.Frame(r, padding=(10, 2, 10, 2))
        snd.pack(fill="x")
        ttk.Checkbutton(snd, text="Alarmton:", variable=self.sound_var).pack(side="left")
        ttk.Entry(snd, textvariable=self.sound_file_var).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(snd, text="Durchsuchen …", command=self._browse_sound).pack(side="left")
        ttk.Button(snd, text="▶ Test", width=7, command=lambda: self._play_alarm(test=True)).pack(side="left", padx=4)

        # weitere Optionen
        opts = ttk.Frame(r, padding=(10, 2, 10, 2))
        opts.pack(fill="x")
        ttk.Checkbutton(opts, text="Neuesten automatisch kopieren", variable=self.auto_copy_var).pack(side="left")
        ttk.Checkbutton(opts, text="Immer im Vordergrund", variable=self.topmost_var,
                        command=self._apply_topmost).pack(side="left", padx=8)
        ttk.Checkbutton(opts, text="Chat in Datei loggen", variable=self.log_var,
                        command=self._apply_log).pack(side="left")

        ttk.Label(r, textvariable=self.status_var, foreground="#666", padding=(10, 0, 10, 4)).pack(fill="x")
        ttk.Separator(r).pack(fill="x")

        head = ttk.Frame(r, padding=(10, 6, 10, 4))
        head.pack(fill="x")
        ttk.Label(head, textvariable=self.count_var, font=self.bold_font).pack(side="left")
        ttk.Button(head, text="Liste leeren", command=self._clear).pack(side="right")
        self.btn_all = ttk.Button(head, text="Alle kopieren", command=self._copy_all)
        self.btn_all.pack(side="right", padx=6)

        wrap = ttk.Frame(r)
        wrap.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(wrap, highlightthickness=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = ttk.Frame(self.canvas)
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width))
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.root.bind_all(seq, self._on_wheel)

        self.empty = ttk.Label(
            self.inner, justify="center", foreground="#888",
            text="Noch keine Codes gefunden.\n\nTrage deine Kanäle in die Textdatei ein\n"
                 "(„Bearbeiten“) und klicke auf „Start“.")
        self.empty.pack(pady=50, fill="x")

    def _on_wheel(self, e):
        if getattr(e, "num", None) == 4:
            d = -1
        elif getattr(e, "num", None) == 5:
            d = 1
        else:
            d = -1 if e.delta > 0 else 1
        self.canvas.yview_scroll(d, "units")

    # ------------------- Suchmuster (live änderbar) -------------------
    def _update_help(self):
        self.pattern_help_var.set(REGEX_HELP if self.regex_mode_var.get() else MASK_HELP)

    def _on_pattern_write(self, *_):
        if self.regex_mode_var.get():
            self.regex_text = self.pattern_var.get()
        else:
            self.mask_text = self.pattern_var.get()
        self._schedule_apply()
        self._schedule_save()

    def _on_mode_change(self, *_):
        # jeder Modus merkt sich sein eigenes Muster
        self.pattern_var.set(self.regex_text if self.regex_mode_var.get() else self.mask_text)
        self._update_help()
        self._schedule_apply()
        self._schedule_save()

    def _schedule_apply(self):
        if self._apply_job is not None:
            self.root.after_cancel(self._apply_job)
        self._apply_job = self.root.after(300, self._apply_pattern)

    def _apply_pattern(self):
        self._apply_job = None
        matcher, err = build_matcher(self.pattern_var.get(), bool(self.regex_mode_var.get()))
        if err:
            note = " – bisheriges Muster bleibt aktiv." if self.matcher else ""
            self.pattern_status_var.set("✗ " + err + note)
            self.pattern_status_lbl.config(foreground=ERR_COLOR)
            return
        self.matcher = matcher
        self.pattern_status_var.set("✓ Muster aktiv")
        self.pattern_status_lbl.config(foreground=OK_COLOR)
        if self._running():
            self.worker.set_matcher(matcher)

    # ------------------------ Einstellungen speichern -----------------
    def _schedule_save(self):
        if self._save_job is not None:
            self.root.after_cancel(self._save_job)
        self._save_job = self.root.after(600, self._save_settings)

    def _save_settings(self):
        self._save_job = None
        try:
            w, h = int(self.root.winfo_width()), int(self.root.winfo_height())
            if w > 300 and h > 300:
                self._size = f"{w}x{h}"
        except (TypeError, ValueError, tk.TclError):
            pass
        save_settings({
            "kanalliste": to_stored_path(self.file_var.get()),
            "muster": self.mask_text,
            "regex_modus": fmt_bool(self.regex_mode_var.get()),
            "regex_muster": self.regex_text,
            "automatisch_kopieren": fmt_bool(self.auto_copy_var.get()),
            "ton": fmt_bool(self.sound_var.get()),
            "tondatei": self.sound_file_var.get().strip(),
            "immer_im_vordergrund": fmt_bool(self.topmost_var.get()),
            "chat_loggen": fmt_bool(self.log_var.get()),
            "fenstergroesse": self._size,
        })

    # ------------------------- Kanalliste (.txt) ----------------------
    def _read_channels(self):
        """-> (Liste, None) oder (None, Fehlertext)"""
        path = resolve_path(self.file_var.get())
        if not path:
            return None, "Keine Kanalliste ausgewählt."
        try:
            return parse_channels(read_text_file(path)), None
        except OSError as e:
            return None, f"Kanalliste nicht lesbar: {e.strerror or e}"

    def _browse(self):
        cur = resolve_path(self.file_var.get())
        path = filedialog.askopenfilename(
            title="Kanalliste wählen",
            initialdir=os.path.dirname(cur) if cur else BASE_DIR,
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")])
        if path:
            self.file_var.set(to_stored_path(os.path.abspath(path)))

    def _edit_file(self):
        path = resolve_path(self.file_var.get())
        if not path:
            self.status_var.set("Bitte zuerst eine Datei wählen.")
            return
        if not ensure_channel_file(path):
            self.status_var.set("Datei konnte nicht angelegt werden.")
            return
        try:
            open_in_editor(path)
        except Exception as e:  # noqa
            self.status_var.set(f"Editor konnte nicht geöffnet werden: {e}")

    def _watch_file(self):
        """Prüft alle 2 s, ob die Liste geändert wurde, und wendet Änderungen live an."""
        path = resolve_path(self.file_var.get())
        try:
            st = os.stat(path)
            sig = (path, st.st_mtime, st.st_size)
        except OSError:
            sig = (path, None, None)
        if sig != self._file_sig:
            self._file_sig = sig
            channels, err = self._read_channels()
            if err:
                self.list_var.set(err)
            else:
                self.list_var.set(f"{len(channels)} Kanäle in der Liste")
                if channels and self._running():
                    self.worker.update_channels(channels)
        self.root.after(2000, self._watch_file)

    # --------------------------- Start / Stop -------------------------
    def _running(self):
        return self.worker is not None and self.worker.is_alive()

    def _toggle(self):
        if self._running():
            self.worker.stop()
            self.worker = None          # späte Meldungen des alten Workers werden ignoriert
            self.btn.config(text="Start")
            self.status_var.set("Gestoppt")
            return
        if self.matcher is None:
            self.status_var.set("Bitte zuerst ein gültiges Suchmuster eingeben.")
            return
        channels, err = self._read_channels()
        if err:
            self.status_var.set(err)
            return
        if not channels:
            self.status_var.set("Die Kanalliste ist leer – bitte Kanäle in die Datei eintragen („Bearbeiten“).")
            return
        self.list_var.set(f"{len(channels)} Kanäle in der Liste")
        self.worker = IrcWorker(channels, self.q, self.matcher, self.log_var.get())
        self.worker.start()
        self.btn.config(text="Stopp")
        self.status_var.set("Verbinde …")

    def _apply_topmost(self):
        self.root.attributes("-topmost", bool(self.topmost_var.get()))

    def _apply_log(self):
        if self.worker:
            self.worker.log_enabled = bool(self.log_var.get())

    # ------------------------- Ereignisse holen -----------------------
    def _poll(self):
        try:
            while True:
                worker, kind, *data = self.q.get_nowait()
                if worker is not self.worker:
                    continue
                if kind == "status":
                    self.status_var.set(data[0])
                elif kind == "code":
                    self._add_code(*data)
        except queue.Empty:
            pass
        self.root.after(100, self._poll)

    # ----------------------------- Alarmton ---------------------------
    def _browse_sound(self):
        cur = resolve_path(self.sound_file_var.get())
        path = filedialog.askopenfilename(
            title="Alarmton wählen",
            initialdir=os.path.dirname(cur) if cur else BASE_DIR,
            filetypes=[("Audiodateien", "*.mp3 *.wav *.ogg *.m4a"), ("Alle Dateien", "*.*")])
        if path:
            self.sound_file_var.set(to_stored_path(os.path.abspath(path)))

    def _play_alarm(self, test=False):
        raw = self.sound_file_var.get().strip()
        path = resolve_path(raw)
        if play_sound(path):
            if test:
                self.status_var.set(f"Alarmton wird abgespielt: {os.path.basename(path)}")
            return
        self.root.bell()   # Ersatz: Systemton
        if not raw:
            msg = "Keine Tondatei angegeben"
        elif not os.path.isfile(path):
            msg = f"Tondatei „{raw}“ nicht gefunden"
        else:
            msg = f"„{raw}“ konnte nicht abgespielt werden"
        self.status_var.set(msg + " – Systemton wird verwendet.")

    # ----------------------------- Codes ------------------------------
    def _add_code(self, code, channel, user, ts):
        if code in self.rows:  # Duplikat: nur Zähler erhöhen
            r = self.rows[code]
            r["n"] += 1
            r["cnt"].config(text=f"{r['n']}× gesehen")
            return

        if self.empty is not None:
            self.empty.destroy()
            self.empty = None

        for old in self.order[:1]:
            self._paint(old, self.BG_OLD)

        frame = tk.Frame(self.inner, bd=1, relief="solid", padx=10, pady=8, bg=self.BG_NEW)
        if self.order:
            frame.pack(fill="x", padx=8, pady=4, before=self.order[0]["frame"])
        else:
            frame.pack(fill="x", padx=8, pady=4)
        frame.columnconfigure(0, weight=1)

        var = tk.StringVar(value=code)
        entry = tk.Entry(frame, textvariable=var, state="readonly", font=self.code_font,
                         width=max(27, min(len(code) + 2, 60)),
                         relief="flat", bd=0, highlightthickness=0, fg=self.FG,
                         readonlybackground=self.BG_NEW)
        entry.grid(row=0, column=0, sticky="w")
        entry.bind("<FocusIn>", lambda e, en=entry: en.select_range(0, "end"))

        info = tk.Label(frame, text=f"#{channel} · {user} · {ts}", anchor="w", fg="#555", bg=self.BG_NEW)
        info.grid(row=1, column=0, sticky="w")
        cnt = tk.Label(frame, text="", anchor="e", fg="#888", bg=self.BG_NEW)
        cnt.grid(row=1, column=1, sticky="e", padx=(0, 8))

        btn = ttk.Button(frame, text="Kopieren", width=10)
        btn.config(command=lambda c=code, b=btn: self._copy(c, b))
        btn.grid(row=0, column=1, sticky="e", padx=(8, 0))

        row = {"code": code, "frame": frame, "entry": entry, "info": info, "cnt": cnt, "n": 1}
        self.rows[code] = row
        self.order.insert(0, row)
        self.count_var.set(f"Gefundene Codes: {len(self.order)}")

        if self.auto_copy_var.get():
            self._copy(code, btn)
        if self.sound_var.get():
            self._play_alarm()
        self.root.after_idle(lambda: self.canvas.yview_moveto(0))

    def _paint(self, row, color):
        row["frame"].config(bg=color)
        row["entry"].config(readonlybackground=color)
        row["info"].config(bg=color)
        row["cnt"].config(bg=color)

    # ---------------------------- Zwischenablage ----------------------
    def _copy(self, text, btn=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        if btn is not None:
            old = btn.cget("text")
            if old != "✓ Kopiert":
                btn.config(text="✓ Kopiert")
                self.root.after(1300, lambda: btn.winfo_exists() and btn.config(text=old))

    def _copy_all(self):
        if self.order:
            self._copy("\n".join(r["code"] for r in self.order), self.btn_all)

    def _clear(self):
        for r in self.order:
            r["frame"].destroy()
        self.order.clear()
        self.rows.clear()
        self.count_var.set("Gefundene Codes: 0")
        if self.empty is None:
            self.empty = ttk.Label(self.inner, justify="center", foreground="#888",
                                   text="Liste geleert.\nNeue Codes erscheinen hier automatisch.")
            self.empty.pack(pady=50, fill="x")

    def _close(self):
        if self.worker:
            self.worker.stop()
        for job in (self._save_job, self._apply_job):
            if job is not None:
                try:
                    self.root.after_cancel(job)
                except Exception:  # noqa
                    pass
        self._save_settings()
        self.root.destroy()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()