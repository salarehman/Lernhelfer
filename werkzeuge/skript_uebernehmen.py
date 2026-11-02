#!/usr/bin/env python3
"""Nimmt eine neue Skript-Version der Vorlesung auf.

    python3 werkzeuge/skript_uebernehmen.py /pfad/skript.pdf --datum 2026-11-09
    python3 werkzeuge/skript_uebernehmen.py /pfad/skript.txt --titel "Physik I"

Was passiert:

1. Die Datei wandert nach skript/skript-<datum>.<endung>.
2. Aus einer PDF wird der Text nach skript/text/<datum>.txt gezogen (pdftotext).
3. Aufgabennummern und Titel werden aus dem Text gelesen und mit dem bisherigen
   Index verglichen: was ist neu, was fehlt (verletzt die Superset-Erwartung).
4. skript/aufgaben.md (Titel von Hand bleiben erhalten), skript/aktuell.md
   (Version, Datum, Prüfsumme, Anzahl) und skript/offen.md werden geschrieben.

Der Aufgabentitel im Skript wird geraten (erste Zeile nach der Nummer). Nach dem
Lauf kurz über die Tabelle sehen und Titel bei Bedarf von Hand kürzen: der
Abgleich überschreibt vorhandene Titel nicht.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
SKRIPT = WURZEL / "skript"
TEXT = SKRIPT / "text"
AUFGABEN = WURZEL / "aufgaben"
INDEX = SKRIPT / "aufgaben.md"
STAND = SKRIPT / "aktuell.md"
OFFEN = SKRIPT / "offen.md"

AUFGABE_RE = re.compile(r"^\s*(?:Aufgabe|Aufg\.?)\s*(\d{1,3})\b[:.\-–]?\s*(.*)$", re.I)
ORDNER_RE = re.compile(r"^(\d+)-")
TITEL_MAX = 70


def index_lesen() -> dict[int, dict[str, str]]:
    """Bisheriger Index als {Nummer: {titel, fundstelle}}."""
    eintraege: dict[int, dict[str, str]] = {}
    if not INDEX.is_file():
        return eintraege
    for zeile in INDEX.read_text(encoding="utf-8").splitlines():
        zeile = zeile.strip()
        if not zeile.startswith("|"):
            continue
        zellen = [z.strip() for z in zeile.strip("|").split("|")]
        if len(zellen) < 2 or not zellen[0].isdigit():
            continue
        eintraege[int(zellen[0])] = {
            "titel": zellen[1],
            "fundstelle": zellen[2] if len(zellen) > 2 else "",
        }
    return eintraege


def text_ziehen(pdf: Path, ziel: Path) -> str:
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ergebnis = subprocess.run(
        ["pdftotext", "-layout", str(pdf), str(ziel)],
        capture_output=True,
        text=True,
    )
    if ergebnis.returncode != 0:
        print(f"pdftotext ist fehlgeschlagen: {ergebnis.stderr.strip()}")
        sys.exit(1)
    return ziel.read_text(encoding="utf-8", errors="replace")


def aufgaben_finden(text: str) -> list[dict]:
    """Aufgabennummern samt geratenem Titel und Seitenzahl."""
    seiten = text.split("\f")
    gefunden: list[dict] = []
    for seitennummer, seiteninhalt in enumerate(seiten, start=1):
        zeilen = seiteninhalt.splitlines()
        for i, zeile in enumerate(zeilen):
            treffer = AUFGABE_RE.match(zeile)
            if not treffer:
                continue
            nummer = int(treffer.group(1))
            if any(e["nr"] == nummer for e in gefunden):
                continue
            titel = treffer.group(2).strip(" :.-")
            if not titel:
                for folge in zeilen[i + 1 : i + 4]:
                    if folge.strip():
                        titel = folge.strip()
                        break
            gefunden.append(
                {
                    "nr": nummer,
                    "titel": titel[:TITEL_MAX] or f"Aufgabe {nummer}",
                    "fundstelle": f"S. {seitennummer}",
                    "seite": seitennummer,
                }
            )
    gefunden.sort(key=lambda e: e["nr"])
    return gefunden


def ordner_nummern() -> set[int]:
    if not AUFGABEN.is_dir():
        return set()
    nummern = set()
    for pfad in AUFGABEN.iterdir():
        treffer = ORDNER_RE.match(pfad.name)
        if pfad.is_dir() and treffer:
            nummern.add(int(treffer.group(1)))
    return nummern


def index_schreiben(gefunden: list[dict], alt: dict[int, dict[str, str]]) -> None:
    zeilen = [
        "# Aufgaben-Index",
        "",
        "Aus dem Skript gelesen von `werkzeuge/skript_uebernehmen.py`. Titel und",
        "Fundstellen dürfen von Hand verbessert werden: vorhandene Titel bleiben beim",
        "nächsten Lauf erhalten, nur neue Nummern werden ergänzt.",
        "",
        "| Nr | Titel | Fundstelle |",
        "|----|-------|------------|",
    ]
    for eintrag in gefunden:
        vorher = alt.get(eintrag["nr"])
        titel = vorher["titel"] if vorher and vorher["titel"] else eintrag["titel"]
        fundstelle = eintrag["fundstelle"]
        zeilen.append(f"| {eintrag['nr']} | {titel} | {fundstelle} |")
    zeilen.append("")
    INDEX.write_text("\n".join(zeilen), encoding="utf-8")


def offen_schreiben(gefunden: list[dict]) -> None:
    vorhanden = ordner_nummern()
    fehlend = [e for e in gefunden if e["nr"] not in vorhanden]
    zeilen = [
        "# Offene Aufgaben",
        "",
        "Aufgaben aus dem Skript, für die es unter `aufgaben/` noch nichts gibt.",
        "",
        "| Nr | Titel | Fundstelle |",
        "|----|-------|------------|",
    ]
    for eintrag in fehlend:
        zeilen.append(f"| {eintrag['nr']} | {eintrag['titel']} | {eintrag['fundstelle']} |")
    if not fehlend:
        zeilen.append("| - | alles bearbeitet | - |")
    zeilen.append("")
    OFFEN.write_text("\n".join(zeilen), encoding="utf-8")
    return


def stand_schreiben(datei: Path, datum: str, titel: str, anzahl: int, pruefsumme: str) -> None:
    STAND.write_text(
        "\n".join(
            [
                "# Aktuelles Skript",
                "",
                "Von `werkzeuge/skript_uebernehmen.py` gepflegt, nicht von Hand ändern.",
                "",
                f"version: {datum}",
                f"datum: {datum}",
                f"datei: {datei.name}",
                f"titel: {titel}",
                f"pruefsumme: sha256:{pruefsumme[:12]}",
                f"aufgaben: {anzahl}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Neue Skript-Version aufnehmen.")
    parser.add_argument("quelle", type=Path, help="Skript-Datei (PDF, TXT, TEX)")
    parser.add_argument("--datum", default=date.today().isoformat(), help="Version, Standard: heute")
    parser.add_argument("--titel", default="Physik", help="Name der Vorlesung")
    args = parser.parse_args()

    if not args.quelle.is_file():
        print(f"Datei nicht gefunden: {args.quelle}")
        return 1

    SKRIPT.mkdir(exist_ok=True)
    endung = args.quelle.suffix.lower() or ".pdf"
    ziel = SKRIPT / f"skript-{args.datum}{endung}"
    if ziel.exists():
        print(f"{ziel.name} gibt es schon, wird ersetzt.")
    shutil.copy2(args.quelle, ziel)
    rohdaten = ziel.read_bytes()
    pruefsumme = hashlib.sha256(rohdaten).hexdigest()

    if endung == ".pdf":
        text = text_ziehen(ziel, TEXT / f"skript-{args.datum}.txt")
    else:
        TEXT.mkdir(parents=True, exist_ok=True)
        (TEXT / f"skript-{args.datum}.txt").write_bytes(rohdaten)
        text = rohdaten.decode("utf-8", errors="replace")

    altein = index_lesen()
    gefunden = aufgaben_finden(text)
    neue = [e for e in gefunden if e["nr"] not in altein]
    verschwunden = [nr for nr in sorted(altein) if nr not in {e["nr"] for e in gefunden}]

    index_schreiben(gefunden, altein)
    offen_schreiben(gefunden)
    stand_schreiben(ziel, args.datum, args.titel, len(gefunden), pruefsumme)

    print(f"aufgenommen: {ziel.name}  (sha256:{pruefsumme[:12]})")
    print(f"Text:        {(TEXT / f'skript-{args.datum}.txt').relative_to(WURZEL)}")
    print(f"Aufgaben:    {len(gefunden)} im Skript gelesen")
    if neue:
        print("Neu gegenüber der Vorversion:")
        for eintrag in neue:
            print(f"  {eintrag['nr']:02d} {eintrag['titel']} ({eintrag['fundstelle']})")
    else:
        print("Keine neuen Aufgabennummern gegenüber dem bisherigen Index.")
    if verschwunden:
        print("Achtung, die Superset-Erwartung ist verletzt, diese Nummern fehlen jetzt:")
        for nr in verschwunden:
            print(f"  {nr:02d} {altein[nr]['titel']}")
        print("Prüfen, ob die richtige Datei übergeben wurde. Ordner nie löschen,")
        print("sondern nach aufgaben/archiv/ verschieben (siehe docs/arbeitsweise.md).")

    fehlend = [e for e in gefunden if e["nr"] not in ordner_nummern()]
    if fehlend:
        print(f"Noch zu bearbeiten ({len(fehlend)}), siehe skript/offen.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
