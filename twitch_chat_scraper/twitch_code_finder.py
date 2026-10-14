# #!/usr/bin/env python3
# """
# Twitch Code Finder
# ==================
# Liest den Chat vieler Twitch-Kanäle live mit (anonym, ohne Login) und listet
# alle Codes im Format  XXXX-XXXX-XXXXX-XXXX-XXXX  untereinander auf –
# jeweils mit "Kopieren"-Button. Neueste Codes stehen oben.
#
# Die Kanäle kommen aus einer Textdatei (Standard: kanaele.txt neben diesem Skript):
#   - ein Kanal pro Zeile ODER mit Komma getrennt
#   - auch Links (https://twitch.tv/name), @name, #name und nummerierte Listen
#     ("1. name", "- name") funktionieren
#   - Kommentarzeilen beginnen mit "// " oder "# " (Raute + Leerzeichen)
#   - Änderungen an der Datei werden bei laufendem Programm automatisch übernommen
#
# Start:   python twitch_code_finder.py
# Benötigt nur Python 3 (tkinter ist meist dabei; unter Linux ggf. `sudo apt install python3-tk`).
# """

import json
import os
import queue
import random
import re
import socket
import ssl
import subprocess
import sys
import threading
import time
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
SETTINGS_FILE = os.path.join(BASE_DIR, "twitch_code_finder.json")
LOG_FILE = os.path.join(BASE_DIR, "twitch_chatlog.txt")
DEFAULT_CHANNEL_FILE = os.path.join(BASE_DIR, "kanaele.txt")

# 4-4-5-4-4 Zeichen (Buchstaben/Ziffern), Groß-/Kleinschreibung egal
CODE_RE = re.compile(
    r"(?<![A-Z0-9-])[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}-[A-Z0-9]{4}-[A-Z0-9]{4}(?![A-Z0-9-])",
    re.IGNORECASE,
)
PRIVMSG_RE = re.compile(r"^(?:@\S+ )?:(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #(\w+) :(.*)$")
JOIN_RE = re.compile(r"^:(\w+)!\w+@\w+\.tmi\.twitch\.tv JOIN #(\w+)\s*$")

TEMPLATE = """\
# Twitch-Kanäle für den Code Finder
# Ein Kanal pro Zeile (oder mit Komma getrennt). Auch Links wie https://twitch.tv/name gehen.
# Zeilen, die mit "// " oder "# " (Raute + Leerzeichen) beginnen, sind Kommentare.
# Änderungen werden bei laufendem Programm automatisch übernommen.
# Ersetze die Beispiele unten durch deine Liste (z. B. die Top-100 WoW-Streamer):

asmongold
https://www.twitch.tv/method
"""


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


# ============================ IRC-Worker ================================
class IrcWorker(threading.Thread):
    """Läuft im Hintergrund und schickt Ereignisse per Queue an die GUI."""

    def __init__(self, channels, out_q, log_enabled=False):
        super().__init__(daemon=True)
        self._wanted = list(channels)
        self._lock = threading.Lock()
        self.q = out_q
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
        for match in CODE_RE.finditer(text):
            self.q.put((self, "code", match.group(0).upper(), channel, user, f"{now:%H:%M:%S}"))


# ================================ GUI ===================================
class App:
    BG_NEW = "#fff3b0"   # frisch gefundener Code
    BG_OLD = "#f3f3f3"
    FG = "#111111"

    def __init__(self, root):
        self.root = root
        root.title("Twitch Code Finder")
        root.geometry("700x680")
        root.minsize(620, 420)

        self.q = queue.Queue()
        self.worker = None
        self.rows = {}    # code -> dict
        self.order = []   # Zeilen, neueste zuerst
        self._file_sig = None

        cfg = self._load_settings()
        self.file_var = tk.StringVar(value=cfg.get("channel_file", DEFAULT_CHANNEL_FILE))
        self.auto_copy_var = tk.BooleanVar(value=cfg.get("auto_copy", True))
        self.sound_var = tk.BooleanVar(value=cfg.get("sound", True))
        self.topmost_var = tk.BooleanVar(value=cfg.get("topmost", False))
        self.log_var = tk.BooleanVar(value=cfg.get("log", False))
        self.status_var = tk.StringVar(value="Nicht verbunden")
        self.list_var = tk.StringVar(value="")
        self.count_var = tk.StringVar(value="Gefundene Codes: 0")

        if self.file_var.get() == DEFAULT_CHANNEL_FILE:
            ensure_channel_file(DEFAULT_CHANNEL_FILE)

        self.code_font = tkfont.nametofont("TkFixedFont").copy()
        self.code_font.configure(size=15, weight="bold")
        self.bold_font = tkfont.nametofont("TkDefaultFont").copy()
        self.bold_font.configure(weight="bold")

        self._build()
        self._apply_topmost()
        root.protocol("WM_DELETE_WINDOW", self._close)
        root.after(100, self._poll)
        root.after(150, self._watch_file)

    # ---------------------------- Aufbau ------------------------------
    def _build(self):
        r = self.root

        top = ttk.Frame(r, padding=(10, 10, 10, 2))
        top.pack(fill="x")
        ttk.Label(top, text="Kanalliste (.txt):").pack(side="left")
        ttk.Entry(top, textvariable=self.file_var).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(top, text="Durchsuchen …", command=self._browse).pack(side="left")
        ttk.Button(top, text="Bearbeiten", command=self._edit_file).pack(side="left", padx=4)
        self.btn = ttk.Button(top, text="Start", width=8, command=self._toggle)
        self.btn.pack(side="left")

        ttk.Label(r, textvariable=self.list_var, padding=(10, 0, 10, 0)).pack(fill="x")

        opts = ttk.Frame(r, padding=(10, 4, 10, 2))
        opts.pack(fill="x")
        ttk.Checkbutton(opts, text="Neuesten automatisch kopieren", variable=self.auto_copy_var).pack(side="left")
        ttk.Checkbutton(opts, text="Ton", variable=self.sound_var).pack(side="left", padx=8)
        ttk.Checkbutton(opts, text="Immer im Vordergrund", variable=self.topmost_var,
                        command=self._apply_topmost).pack(side="left")
        ttk.Checkbutton(opts, text="Chat in Datei loggen", variable=self.log_var,
                        command=self._apply_log).pack(side="left", padx=8)

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

    # ------------------------- Kanalliste (.txt) ----------------------
    def _read_channels(self):
        """-> (Liste, None) oder (None, Fehlertext)"""
        path = self.file_var.get().strip()
        if not path:
            return None, "Keine Kanalliste ausgewählt."
        try:
            return parse_channels(read_text_file(path)), None
        except OSError as e:
            return None, f"Kanalliste nicht lesbar: {e.strerror or e}"

    def _browse(self):
        cur = self.file_var.get().strip()
        path = filedialog.askopenfilename(
            title="Kanalliste wählen",
            initialdir=os.path.dirname(cur) if cur else BASE_DIR,
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")])
        if path:
            self.file_var.set(path)
            self._save_settings()

    def _edit_file(self):
        path = self.file_var.get().strip()
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
        path = self.file_var.get().strip()
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
        channels, err = self._read_channels()
        if err:
            self.status_var.set(err)
            return
        if not channels:
            self.status_var.set("Die Kanalliste ist leer – bitte Kanäle in die Datei eintragen („Bearbeiten“).")
            return
        self._save_settings()
        self.list_var.set(f"{len(channels)} Kanäle in der Liste")
        self.worker = IrcWorker(channels, self.q, self.log_var.get())
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
        entry = tk.Entry(frame, textvariable=var, state="readonly", font=self.code_font, width=27,
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
            self.root.bell()
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

    # ---------------------------- Einstellungen -----------------------
    def _load_settings(self):
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_settings(self):
        data = {
            "channel_file": self.file_var.get().strip() or DEFAULT_CHANNEL_FILE,
            "auto_copy": bool(self.auto_copy_var.get()),
            "sound": bool(self.sound_var.get()),
            "topmost": bool(self.topmost_var.get()),
            "log": bool(self.log_var.get()),
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError:
            pass

    def _close(self):
        if self.worker:
            self.worker.stop()
        self._save_settings()
        self.root.destroy()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
