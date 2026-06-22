#!/usr/bin/env python3

from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

HOME = Path.home()
GAMELISTS_ROOT = HOME / ".emulationstation" / "gamelists"
MANUALS_ROOT = HOME / "RetroPie" / "manuals"

def clean_name(name: str) -> str:
    name = re.sub(r"\[[^\]]*\]", "", name)
    name = re.sub(r"\([^)]*\)", "", name)
    name = re.sub(r"\s+", " ", name)
    name = name.strip(" -_")
    return name.strip()

def norm(name: str) -> str:
    name = clean_name(name).lower()
    name = re.sub(r"[^a-z0-9]+", "", name)
    return name

def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

def main():
    total_added = 0

    for gamelist in sorted(GAMELISTS_ROOT.glob("*/gamelist.xml")):
        system = gamelist.parent.name
        manual_dir = MANUALS_ROOT / system

        if not manual_dir.is_dir():
            continue

        pdfs = {}
        for pdf in manual_dir.glob("*.pdf"):
            pdfs[norm(pdf.stem)] = pdf

        if not pdfs:
            continue

        tree = ET.parse(gamelist)
        root = tree.getroot()
        changed = False
        added = 0

        for game in root.findall("game"):
            name_node = game.find("name")
            path_node = game.find("path")

            if name_node is None or not name_node.text:
                continue

            manual_node = game.find("manual")
            if manual_node is not None and manual_node.text and manual_node.text.strip():
                continue

            candidates = [
                name_node.text,
            ]

            if path_node is not None and path_node.text:
                candidates.append(Path(path_node.text).stem)

            found_pdf = None

            for candidate in candidates:
                key = norm(candidate)
                if key in pdfs:
                    found_pdf = pdfs[key]
                    break

            if not found_pdf:
                continue

            if manual_node is None:
                manual_node = ET.SubElement(game, "manual")

            manual_node.text = str(found_pdf)
            changed = True
            added += 1
            total_added += 1

        if changed:
            backup = gamelist.with_suffix(".xml.bak-manuals-from-pdfs")
            shutil.copy2(gamelist, backup)
            indent(root)
            tree.write(gamelist, encoding="utf-8", xml_declaration=True)
            print(f"✅ {system}: {added} manuel(s) ajouté(s)")

    print(f"\n🎉 Total : {total_added} balise(s) <manual> ajoutée(s)")

if __name__ == "__main__":
    main()
