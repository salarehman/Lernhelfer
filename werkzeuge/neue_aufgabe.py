#!/usr/bin/env python3
"""Legt für eine neue Aufgabe den Ordner mit den beiden Gerüstdateien an.

    python3 werkzeuge/neue_aufgabe.py physik 7 "Maxwell-Rad" --skript "Kap. 6, S. 96"

Erzeugt aufgaben/<fach>/blatt<N>/NN-<slug>/theorie.tex und loesung.tex aus den
Vorlagen in werkzeuge/vorlagen/. Die Nummer bestimmt die Sortierung und muss
zur Nummer im Skript-Index passen. Fächer und Blätter folgen den Ordnern unter
aufgaben/, z. B. physik und 7 → aufgaben/physik/blatt07/.
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


def blatt_ordner(fach: str, blatt: int) -> Path:
    return AUFGABEN / fach / f"blatt{blatt:02d}"


def freie_nummer(fach: str, blatt: int) -> int:
    hoechste = 0
    for pfad in sorted(blatt_ordner(fach, blatt).iterdir()) if blatt_ordner(fach, blatt).is_dir() else []:
        treffer = re.match(r"^(\d+)-", pfad.name)
        if pfad.is_dir() and treffer:
            hoechste = max(hoechste, int(treffer.group(1)))
    return hoechste + 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Neue Aufgabe anlegen.")
    parser.add_argument("fach", nargs="?", help="Fach, z. B. physik, mathe")
    parser.add_argument("blatt", nargs="?", type=int, help="Blattnummer der Woche")
    parser.add_argument("nummer", nargs="?", type=int, help="Aufgabennummer aus dem Skript")
    parser.add_argument("titel", nargs="?", help="Titel der Aufgabe")
    parser.add_argument("--skript", default="", help="Fundstelle, z. B. 'Kap. 3, S. 14'")
    parser.add_argument("--fach-liste", action="store_true", help="verfügbare Fächer anzeigen")
    args = parser.parse_args()

    if args.fach_liste:
        print("Verfügbare Fächer unter aufgaben/:")
        for pfad in sorted(AUFGABEN.iterdir()) if AUFGABEN.is_dir() else []:
            if pfad.is_dir() and pfad.name != "archiv":
                print(f"  {pfad.name}")
        return 0

    if None in (args.fach, args.blatt, args.nummer, args.titel):
        print(
            'Aufruf: python3 werkzeuge/neue_aufgabe.py <fach> <blatt> <nummer> "<Titel>" '
            '--skript "Kap. 3, S. 14"'
        )
        if args.fach and args.blatt is not None:
            print(f"Nächste freie Nummer wäre {freie_nummer(args.fach, args.blatt)}.")
        return 1

    ziel = blatt_ordner(args.fach, args.blatt) / f"{args.nummer:02d}-{slug_bauen(args.titel)}"
    if ziel.exists():
        print(f"Gibt es schon: {ziel.relative_to(WURZEL)}")
        return 1

    ziel.mkdir(parents=True)
    for name in ("theorie.tex", "loesung.tex"):
        vorlage = (VORLAGEN / name).read_text(encoding="utf-8")
        vorlage = vorlage.replace("@TITEL@", args.titel).replace("@SKRIPT@", args.skript)
        (ziel / name).write_text(vorlage, encoding="utf-8")

    print(f"angelegt: {ziel.relative_to(WURZEL)}")
    print("  theorie.tex  Werkzeuge und typische Fallen, kein Lösungsweg")
    print("  loesung.tex  Gegeben/Gesucht, Ansatz, Rechnung, Kontrolle, Merksatz")
    print("Danach: python3 werkzeuge/build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
