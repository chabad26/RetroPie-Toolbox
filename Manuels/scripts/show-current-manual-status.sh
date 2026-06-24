#!/usr/bin/env bash

export DISPLAY="${DISPLAY:-:1}"
export XAUTHORITY="${XAUTHORITY:-/home/retropie/.Xauthority}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=/run/user/$(id -u retropie)/bus}"

CURRENT="/tmp/retropie-current-manual.txt"
LOG="/tmp/retropie-manual-status.log"

sleep 2

MANUAL=""

if [ -f "$CURRENT" ]; then
  MANUAL="$(cat "$CURRENT" 2>/dev/null | head -n 1)"
fi

if command -v notify-send >/dev/null 2>&1; then
  if [ -n "$MANUAL" ] && [ -f "$MANUAL" ]; then
    BASENAME="$(basename "$MANUAL")"

    echo "$(date) | Manuel disponible : $MANUAL" >> "$LOG"

    notify-send \
      --app-name="RetroPie" \
      --icon=dialog-information \
      --expire-time=3500 \
      "📘 Manuel disponible" \
      "$BASENAME
L3 + R3 pour ouvrir"
  else
    echo "$(date) | Aucun manuel disponible" >> "$LOG"
  fi

  exit 0
fi

# Fallback YAD si notify-send n'est pas disponible.
if [ -n "$MANUAL" ] && [ -f "$MANUAL" ]; then
  BASENAME="$(basename "$MANUAL")"

  yad \
    --center \
    --on-top \
    --undecorated \
    --skip-taskbar \
    --no-buttons \
    --timeout=3 \
    --width=430 \
    --height=90 \
    --borders=8 \
    --text-align=center \
    --text="<span font='18' weight='bold'>📘 Manuel disponible</span>\n<span font='11'>$BASENAME</span>\n<span font='13' weight='bold'>L3 + R3 pour ouvrir</span>" \
    2>/dev/null || true
else
  yad \
    --center \
    --on-top \
    --undecorated \
    --skip-taskbar \
    --no-buttons \
    --timeout=2 \
    --width=340 \
    --height=70 \
    --borders=8 \
    --text-align=center \
    --text="<span font='16' weight='bold'>📕 Aucun manuel disponible</span>" \
    2>/dev/null || true
fi
