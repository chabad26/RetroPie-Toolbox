#!/usr/bin/env python3

from evdev import InputDevice, ecodes
from pathlib import Path
import subprocess
import sys
import time

DEVICE_PATH = sys.argv[1] if len(sys.argv) > 1 else ""
OPEN_SCRIPT = "/home/retropie/Documents/save_retropie/Manuels/scripts/open-current-manual.sh"
LOG = Path("/tmp/retropie-manual-hotkey.log")

# Sur ta PowerA :
# L3 = BTN_SELECT
HOTKEY = ecodes.BTN_SELECT

HOLD_SECONDS = 1.2
COOLDOWN_SECONDS = 3.0

pressed_at = None
last_trigger = 0.0

if not DEVICE_PATH:
    print("Usage: manual-hotkey-watcher.py /dev/input/by-id/xxx-event-joystick")
    sys.exit(1)

device = InputDevice(DEVICE_PATH)
LOG.open("a").write(f"Watcher lancé : {time.ctime()} sur {DEVICE_PATH}\n")

for event in device.read_loop():
    if event.type != ecodes.EV_KEY:
        continue

    if event.code != HOTKEY:
        continue

    # bouton pressé
    if event.value == 1:
        pressed_at = time.time()
        LOG.open("a").write(f"L3 pressé : {time.ctime()}\n")

    # bouton relâché
    elif event.value == 0:
        if pressed_at is None:
            continue

        held = time.time() - pressed_at
        pressed_at = None

        LOG.open("a").write(f"L3 relâché après {held:.2f}s\n")

        if held < HOLD_SECONDS:
            continue

        now = time.time()
        if now - last_trigger < COOLDOWN_SECONDS:
            LOG.open("a").write("Déclenchement ignoré : cooldown\n")
            continue

        last_trigger = now
        LOG.open("a").write(f"Ouverture demandée : {time.ctime()}\n")

        subprocess.Popen(
            [OPEN_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
