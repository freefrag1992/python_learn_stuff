import tkinter as tk
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# ================= GPIO =================
GPIO.setmode(GPIO.BCM)

LED_UP = 17
LED_DOWN = 27
LED_RUN = 22
LED_AUTO = 23

LED_TOP = 13
LED_MID = 19
LED_BOTTOM = 26

GPIO.setup(
    [LED_UP, LED_DOWN, LED_RUN, LED_AUTO,
     LED_TOP, LED_MID, LED_BOTTOM],
    GPIO.OUT
)

# ================= ADS1115 =================
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x48)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)

# ================= STATUS =================
MODE = "MANUAL"
POSITION = "OBEN"
AUTO_TARGET = "OBEN"

# LED-Status für Tkinter
LED_STATE_UP = False
LED_STATE_DOWN = False
LED_STATE_RUN = False
LED_STATE_AUTO = False

# ================= HELPER =================
def motor_off():
    global LED_STATE_UP, LED_STATE_DOWN, LED_STATE_RUN
    GPIO.output([LED_UP, LED_DOWN, LED_RUN], False)
    LED_STATE_UP = LED_STATE_DOWN = LED_STATE_RUN = False
    update_ui()

def set_position_leds():
    GPIO.output([LED_TOP, LED_MID, LED_BOTTOM], False)
    if POSITION == "OBEN":
        GPIO.output(LED_TOP, True)
    elif POSITION == "MITTE":
        GPIO.output(LED_MID, True)
    elif POSITION == "UNTEN":
        GPIO.output(LED_BOTTOM, True)

# ================= HYSTERESE =================
def determine_target(ldr, current):
    if current == "UNTEN" and ldr < 20000:
        return "MITTE"
    if current == "MITTE":
        if ldr > 26000:
            return "UNTEN"
        if ldr < 8000:
            return "OBEN"
    if current == "OBEN" and ldr > 12000:
        return "MITTE"
    return current

# ================= MOTOR =================
def move_to(target):
    global LED_STATE_UP, LED_STATE_DOWN, LED_STATE_RUN

    if POSITION == target:
        return

    motor_off()

    GPIO.output(LED_RUN, True)
    LED_STATE_RUN = True

    if target in ["MITTE", "UNTEN"]:
        GPIO.output(LED_DOWN, True)
        LED_STATE_DOWN = True
    else:
        GPIO.output(LED_UP, True)
        LED_STATE_UP = True

    update_ui()
    root.after(1000, lambda: finish_move(target))

def finish_move(target):
    global POSITION
    POSITION = target
    motor_off()
    set_position_leds()
    update_ui()

# ================= UI CALLBACKS =================
def set_auto():
    global MODE, LED_STATE_AUTO
    MODE = "AUTO"
    GPIO.output(LED_AUTO, True)
    LED_STATE_AUTO = True
    update_ui()

def set_manual():
    global MODE, LED_STATE_AUTO
    MODE = "MANUAL"
    GPIO.output(LED_AUTO, False)
    LED_STATE_AUTO = False
    motor_off()
    update_ui()

def manual_up():
    if MODE == "MANUAL" and POSITION != "OBEN":
        move_to("OBEN")

def manual_down():
    if MODE == "MANUAL" and POSITION != "UNTEN":
        move_to("UNTEN")

# ================= AUTOMATIK =================
def automation_loop():
    global AUTO_TARGET

    if MODE == "AUTO":
        ldr_value = chan.value
        AUTO_TARGET = determine_target(ldr_value, AUTO_TARGET)
        move_to(AUTO_TARGET)
        lbl_ldr.config(text=f"LDR: {ldr_value}")

    root.after(1000, automation_loop)

# ================= TKINTER =================
root = tk.Tk()
root.title("Jalousiensteuerung – ADS1115")

def led_label(parent, text):
    lbl = tk.Label(parent, text=text, width=12, bg="grey")
    lbl.pack(side=tk.LEFT, padx=3)
    return lbl

def update_led(lbl, state):
    lbl.config(bg="green" if state else "grey")

frame_mode = tk.Frame(root)
frame_mode.pack(pady=5)
tk.Button(frame_mode, text="AUTOMATIK", width=12, command=set_auto).pack(side=tk.LEFT, padx=5)
tk.Button(frame_mode, text="HAND", width=12, command=set_manual).pack(side=tk.LEFT, padx=5)

frame_manual = tk.Frame(root)
frame_manual.pack(pady=5)
tk.Button(frame_manual, text="AUF", width=12, command=manual_up).pack(side=tk.LEFT, padx=5)
tk.Button(frame_manual, text="AB", width=12, command=manual_down).pack(side=tk.LEFT, padx=5)

lbl_mode = tk.Label(root, text="")
lbl_mode.pack()
lbl_pos = tk.Label(root, text="")
lbl_pos.pack()
lbl_ldr = tk.Label(root, text="LDR: ---")
lbl_ldr.pack()

frame_leds = tk.Frame(root)
frame_leds.pack(pady=5)

led_up = led_label(frame_leds, "AUF")
led_down = led_label(frame_leds, "AB")
led_run = led_label(frame_leds, "RUN")
led_auto = led_label(frame_leds, "AUTO")

def update_ui():
    lbl_mode.config(text=f"Modus: {MODE}")
    lbl_pos.config(text=f"Position: {POSITION}")

    update_led(led_up, LED_STATE_UP)
    update_led(led_down, LED_STATE_DOWN)
    update_led(led_run, LED_STATE_RUN)
    update_led(led_auto, LED_STATE_AUTO)

# ================= START =================
set_position_leds()
update_ui()
automation_loop()

try:
    root.mainloop()
finally:
    motor_off()
    GPIO.cleanup()
