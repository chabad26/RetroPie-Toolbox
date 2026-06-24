#!/usr/bin/env python3

from evdev import InputDevice, ecodes
from pathlib import Path
import subprocess
import sys
import time
import os

DEVICE_PATH = sys.argv[1] if len(sys.argv) > 1 else "/dev/input/by-id/usb-PowerA_NSW_wired_controller-event-joystick"

OPEN_SCRIPT = "/home/retropie/Documents/save_retropie/Manuels/scripts/open-current-manual.sh"
LOG = Path("/tmp/retropie-manual-hotkey.log")

# Manette PowerA testée :
# L3 = code 314 = BTN_SELECT
# R3 = code 315 = BTN_START
LEFT_STICK_CODES = {
    ecodes.BTN_SELECT,
    ecodes.BTN_THUMBL,
}

RIGHT_STICK_CODES = {
    ecodes.BTN_START,
    ecodes.BTN_THUMBR,
}

COOLDOWN_SECONDS = 2.5


def log(message: str) -> None:
    with LOG.open("a", encoding="utf-8") as file:
        file.write(f"{time.ctime()} | {message}\n")


def open_manual() -> None:
    log("Ouverture manuel demandée par combo L3+R3")

    env = os.environ.copy()
    env["DISPLAY"] = ":1"
    env["XAUTHORITY"] = "/home/retropie/.Xauthority"

    subprocess.Popen(
        [OPEN_SCRIPT],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )


try:
    device = InputDevice(DEVICE_PATH)
except Exception as exc:
    log(f"Impossible d'ouvrir {DEVICE_PATH}: {exc}")
    sys.exit(1)

log(f"Watcher démarré sur {DEVICE_PATH}")
log("Combo actif : L3 + R3")

pressed_left = False
pressed_right = False
last_trigger = 0.0
combo_armed = True

for event in device.read_loop():
    if event.type != ecodes.EV_KEY:
        continue

    code = event.code
    value = event.value

    if code in LEFT_STICK_CODES:
        pressed_left = value != 0
        log(f"L3 état: {pressed_left} code={code}")

    elif code in RIGHT_STICK_CODES:
        pressed_right = value != 0
        log(f"R3 état: {pressed_right} code={code}")

    else:
        continue

    now = time.time()

    if pressed_left and pressed_right and combo_armed:
        if now - last_trigger >= COOLDOWN_SECONDS:
            log("Combo L3+R3 détecté")
            open_manual()
            last_trigger = now
            combo_armed = False

    if not pressed_left or not pressed_right:
        if not combo_armed:
            log("Combo L3+R3 réarmé")
        combo_armed = True
