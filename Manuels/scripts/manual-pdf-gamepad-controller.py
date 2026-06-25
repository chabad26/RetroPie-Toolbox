#!/usr/bin/env python3

from evdev import InputDevice, ecodes
from pathlib import Path
import subprocess
import sys
import time
import os

DEVICE_PATH = sys.argv[1] if len(sys.argv) > 1 else "/dev/input/by-id/usb-PowerA_NSW_wired_controller-event-joystick"
LOG = Path("/tmp/retropie-manual-pdf-gamepad.log")

COOLDOWN = 0.18
last_action = 0.0


def log(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} | {msg}\n")


def xkey(key):
    env = os.environ.copy()
    env["DISPLAY"] = ":1"
    env["XAUTHORITY"] = "/home/retropie/.Xauthority"

    subprocess.Popen(
        ["xdotool", "key", key],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )


def do_action(action):
    global last_action

    now = time.time()
    if now - last_action < COOLDOWN:
        return

    last_action = now
    log(action)

    if action == "down":
        xkey("Down")
    elif action == "up":
        xkey("Up")
    elif action == "page_down":
        xkey("Next")
    elif action == "page_up":
        xkey("Prior")
    elif action == "zoom_in":
        xkey("plus")
    elif action == "zoom_out":
        xkey("minus")
    elif action == "fit":
        xkey("w")
    elif action == "quit":
        xkey("q")


try:
    dev = InputDevice(DEVICE_PATH)
except Exception as exc:
    log(f"Impossible d'ouvrir {DEVICE_PATH}: {exc}")
    sys.exit(1)

log(f"Contrôleur PDF démarré sur {DEVICE_PATH}")

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value != 1:
            continue

        code = event.code

        # D-Pad sur beaucoup de manettes
        if code == ecodes.BTN_DPAD_DOWN:
            do_action("down")
        elif code == ecodes.BTN_DPAD_UP:
            do_action("up")
        elif code == ecodes.BTN_DPAD_RIGHT:
            do_action("page_down")
        elif code == ecodes.BTN_DPAD_LEFT:
            do_action("page_up")

        # Boutons génériques possibles
        elif code in (ecodes.BTN_SOUTH, ecodes.BTN_EAST):
            do_action("quit")
        elif code == ecodes.BTN_TR:
            do_action("zoom_in")
        elif code == ecodes.BTN_TL:
            do_action("zoom_out")
        elif code in (ecodes.BTN_SELECT, ecodes.BTN_START):
            do_action("fit")

    elif event.type == ecodes.EV_ABS:
        code = event.code
        value = event.value

        # Croix directionnelle en ABS_HAT
        if code == ecodes.ABS_HAT0Y:
            if value == 1:
                do_action("down")
            elif value == -1:
                do_action("up")

        elif code == ecodes.ABS_HAT0X:
            if value == 1:
                do_action("page_down")
            elif value == -1:
                do_action("page_up")

        # Stick gauche vertical, fallback
        elif code == ecodes.ABS_Y:
            if value > 45000:
                do_action("down")
            elif value < 20000:
                do_action("up")
