#!/usr/bin/env bash

STATE="/tmp/retropie-current-manual.txt"
LOG="/tmp/retropie-open-manual.log"
PDF_LOG="/tmp/retropie-pdf-viewer.log"
LOCK="/tmp/retropie-open-manual.lock"

echo "==============================" >> "$LOG"
echo "Date: $(date)" >> "$LOG"

show_no_manual_message() {
  export DISPLAY="${DISPLAY:-:1}"
  export XAUTHORITY="${XAUTHORITY:-/home/retropie/.Xauthority}"

  if command -v yad >/dev/null 2>&1; then
    nohup yad \
      --center \
      --on-top \
      --no-buttons \
      --timeout=2 \
      --width=720 \
      --height=180 \
      --text="<span font='32' weight='bold'>Aucun manuel disponible</span>" \
      >/tmp/retropie-no-manual.log 2>&1 &
  elif command -v xmessage >/dev/null 2>&1; then
    nohup xmessage \
      -center \
      -timeout 2 \
      -geometry 720x180 \
      -fn "-*-helvetica-bold-r-*-*-34-*-*-*-*-*-*-*" \
      "Aucun manuel disponible" \
      >/tmp/retropie-no-manual.log 2>&1 &
  else
    echo "Aucun manuel disponible, mais aucun afficheur trouvé." >> "$LOG"
  fi
}



now="$(date +%s)"
last="0"

if [ -f "$LOCK" ]; then
  last="$(cat "$LOCK" 2>/dev/null || echo 0)"
fi

if [ "$((now - last))" -lt 3 ]; then
  echo "Ignoré : cooldown actif" >> "$LOG"
  exit 0
fi

echo "$now" > "$LOCK"

if [ ! -s "$STATE" ]; then
  echo "Aucun manuel courant." >> "$LOG"
  show_no_manual_message
  exit 0
fi

MANUAL="$(cat "$STATE")"

if [ ! -f "$MANUAL" ]; then
  echo "Manuel introuvable : $MANUAL" >> "$LOG"
  show_no_manual_message
  exit 0
fi

echo "Ouverture manuel : $MANUAL" >> "$LOG"

export DISPLAY="${DISPLAY:-:1}"
export XAUTHORITY="${XAUTHORITY:-/home/retropie/.Xauthority}"

echo "DISPLAY=$DISPLAY" >> "$LOG"
echo "XAUTHORITY=$XAUTHORITY" >> "$LOG"

# Ferme les anciens lecteurs PDF
pkill -u retropie -f "xpdf.*\.pdf" 2>/dev/null || true
pkill -u retropie -f "zathura.*\.pdf" 2>/dev/null || true
pkill -u retropie -f "mupdf.*\.pdf" 2>/dev/null || true

if command -v xpdf >/dev/null 2>&1; then
  nohup xpdf -fullscreen "$MANUAL" > "$PDF_LOG" 2>&1 &
elif command -v zathura >/dev/null 2>&1; then
  nohup zathura --fork "$MANUAL" > "$PDF_LOG" 2>&1 &
elif command -v evince >/dev/null 2>&1; then
  nohup evince --fullscreen "$MANUAL" > "$PDF_LOG" 2>&1 &
else
  echo "Aucun lecteur PDF compatible trouvé." >> "$LOG"
  exit 1
fi

exit 0
