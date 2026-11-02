#!/usr/bin/env python3
"""Legt für eine neue Aufgabe den Ordner mit den beiden Gerüstdateien an.

    python3 werkzeuge/neue_aufgabe.py 3 "Schiefer Wurf" --skript "Kap. 3, S. 14"

Erzeugt aufgaben/03-schiefer-wurf/theorie.tex und loesung.tex aus den Vorlagen
in werkzeuge/vorlagen/. Die Nummer bestimmt die Sortierung und muss zur Nummer
im Skript-Index passen.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
AUFGABEN = WURZEL / "aufgaben"
VORLAGEN = WURZEL / "werkzeuge" / "vorlagen"


def slug_bauen(titel: str) -> str:
    text = titel.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "aufgabe"


def freie_nummer() -> int:
    hoechste = 0
    for pfad in AUFGABEN.iterdir() if AUFGABEN.is_dir() else []:
        treffer = re.match(r"^(\d+)-", pfad.name)
        if pfad.is_dir() and treffer:
            hoechste = max(hoechste, int(treffer.group(1)))
    return hoechste + 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Neue Aufgabe anlegen.")
    parser.add_argument("nummer", nargs="?", type=int, help="Aufgabennummer aus dem Skript")
    parser.add_argument("titel", nargs="?", help="Titel der Aufgabe")
    parser.add_argument("--skript", default="", help="Fundstelle, z. B. 'Kap. 3, S. 14'")
    args = parser.parse_args()

    if args.nummer is None or not args.titel:
        print(f"Nächste freie Nummer wäre {freie_nummer()}.")
        print('Aufruf: python3 werkzeuge/neue_aufgabe.py 3 "Schiefer Wurf" --skript "Kap. 3, S. 14"')
        return 1

    ordner = AUFGABEN / f"{args.nummer:02d}-{slug_bauen(args.titel)}"
    if ordner.exists():
        print(f"Gibt es schon: {ordner.relative_to(WURZEL)}")
        return 1

    ordner.mkdir(parents=True)
    for name in ("theorie.tex", "loesung.tex"):
        vorlage = (VORLAGEN / name).read_text(encoding="utf-8")
        vorlage = vorlage.replace("@TITEL@", args.titel).replace("@SKRIPT@", args.skript)
        (ordner / name).write_text(vorlage, encoding="utf-8")

    print(f"angelegt: {ordner.relative_to(WURZEL)}")
    print("  theorie.tex  Werkzeuge und typische Fallen, kein Lösungsweg")
    print("  loesung.tex  Gegeben/Gesucht, Ansatz, Rechnung, Kontrolle, Merksatz")
    print("Danach: python3 werkzeuge/build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
