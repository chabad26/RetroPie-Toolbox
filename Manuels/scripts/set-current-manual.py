#!/usr/bin/env python3

from pathlib import Path
import sys
import xml.etree.ElementTree as ET

HOME = Path.home()
ROMS_ROOT = HOME / "RetroPie" / "roms"
GAMELISTS_ROOT = HOME / ".emulationstation" / "gamelists"
STATE_PATH = Path("/tmp/retropie-current-manual.txt")
LOG_PATH = Path("/tmp/retropie-current-manual.log")


def log(message: str) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(message + "\n")


def normalize(path: Path) -> str:
    try:
        return str(path.expanduser().resolve())
    except Exception:
        return str(path.expanduser())



def clean_game_name(name: str) -> str:
    import re
    name = re.sub(r"\[[^\]]*\]", "", name)
    name = re.sub(r"\([^)]*\)", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip(" -_")


def norm_name(name: str) -> str:
    import re
    name = clean_game_name(name).lower()
    return re.sub(r"[^a-z0-9]+", "", name)


def find_manual_pdf(system: str, names: list[str]) -> Path | None:
    manual_dir = Path.home() / "RetroPie" / "manuals" / system

    if not manual_dir.is_dir():
        return None

    pdfs = {norm_name(pdf.stem): pdf for pdf in manual_dir.glob("*.pdf")}

    for name in names:
        key = norm_name(name)
        if key in pdfs:
            return pdfs[key]

    return None

def main():
    if len(sys.argv) < 3:
        log(f"ARGS insuffisants : {sys.argv}")
        STATE_PATH.unlink(missing_ok=True)
        return

    system = sys.argv[1]
    rom_arg = sys.argv[2]

    rom_path = Path(rom_arg)
    rom_abs = normalize(rom_path)

    gamelist = GAMELISTS_ROOT / system / "gamelist.xml"

    if not gamelist.is_file():
        log(f"Gamelist introuvable : {gamelist}")
        STATE_PATH.unlink(missing_ok=True)
        return

    try:
        tree = ET.parse(gamelist)
        root = tree.getroot()
    except Exception as exc:
        log(f"Erreur XML {gamelist} : {exc}")
        STATE_PATH.unlink(missing_ok=True)
        return

    for game in root.findall("game"):
        path_node = game.find("path")
        manual_node = game.find("manual")

        if path_node is None or not path_node.text:
            continue

        game_path_text = path_node.text.strip()

        if game_path_text.startswith("./"):
            game_path = ROMS_ROOT / system / game_path_text[2:]
        else:
            game_path = Path(game_path_text)

        game_abs = normalize(game_path)

        if game_abs != rom_abs:
            continue

        if manual_node is None or not manual_node.text:
            fallback = find_manual_pdf(system, [
                game.findtext("name", ""),
                Path(game_path_text).stem,
                Path(rom_arg).stem,
            ])

            if fallback:
                STATE_PATH.write_text(str(fallback), encoding="utf-8")
                log(f"Manuel courant via fallback PDF : {fallback}")
                return

            log(f"Aucun manuel pour : {rom_arg}")
            STATE_PATH.unlink(missing_ok=True)
            return

        manual_path = Path(manual_node.text.strip())

        if not manual_path.is_file():
            log(f"Manuel absent sur disque : {manual_path}")
            STATE_PATH.unlink(missing_ok=True)
            return

        STATE_PATH.write_text(str(manual_path), encoding="utf-8")
        log(f"Manuel courant : {manual_path}")
        return

    log(f"Jeu non trouvé dans gamelist : {rom_arg}")
    STATE_PATH.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
