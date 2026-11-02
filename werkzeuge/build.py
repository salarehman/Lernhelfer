#!/usr/bin/env python3
"""Baut das Lern-PDF aus den Aufgaben-Ordnern unter aufgaben/.

Teil I sammelt alle theorie.tex, Teil II alle loesung.tex. Der Build erzeugt
generated/*.tex, kompiliert tex/main.tex zweimal mit pdflatex und legt das PDF
in out/ ab.

Aufrufe (immer aus dem Repo-Wurzelverzeichnis bzw. egal, das Skript findet es):

    python3 werkzeuge/build.py                  # out/physik-uebungen.pdf
    python3 werkzeuge/build.py --nur-theorie    # out/physik-theorie.pdf
    python3 werkzeuge/build.py --nur-loesungen  # out/physik-loesungen.pdf
    python3 werkzeuge/build.py --offen          # nur Abdeckung, nichts bauen
    python3 werkzeuge/build.py --kein-pdf       # nur generated/ schreiben
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
AUFGABEN = WURZEL / "aufgaben"
GENERIERT = WURZEL / "generated"
OUT = WURZEL / "out"
SKRIPT = WURZEL / "skript"
ARCHIVNAME = "archiv"

META_RE = re.compile(r"^\s*%\s*(titel|skript|stand|schlagworte)\s*:\s*(.+?)\s*$", re.I)
ORDNER_RE = re.compile(r"^(\d+)-(.+)$")


# --------------------------------------------------------------- Einlesen


def metadaten(datei: Path) -> dict[str, str]:
    """Liest die Kommentarzeilen ``% titel: ...`` am Dateianfang."""
    daten: dict[str, str] = {}
    if not datei.exists():
        return daten
    for zeile in datei.read_text(encoding="utf-8").splitlines():
        treffer = META_RE.match(zeile)
        if treffer:
            daten.setdefault(treffer.group(1).lower(), treffer.group(2))
    return daten


def titel_aus_slug(slug: str) -> str:
    return slug.replace("-", " ").strip().capitalize()


def sammle_aufgaben() -> list[dict]:
    """Alle Aufgaben-Ordner mit Nummernpräfix, nach Nummer sortiert."""
    if not AUFGABEN.is_dir():
        return []
    gefunden: list[dict] = []
    for pfad in sorted(AUFGABEN.iterdir()):
        if not pfad.is_dir() or pfad.name == ARCHIVNAME:
            continue
        treffer = ORDNER_RE.match(pfad.name)
        if not treffer:
            print(f"  Hinweis: Ordner ohne Nummernpräfix wird übersprungen: {pfad.name}")
            continue
        meta = metadaten(pfad / "theorie.tex")
        gefunden.append(
            {
                "nr": int(treffer.group(1)),
                "key": pfad.name,
                "pfad": pfad,
                "titel": meta.get("titel") or titel_aus_slug(treffer.group(2)),
                "skript": meta.get("skript", ""),
                "hat_theorie": (pfad / "theorie.tex").is_file(),
                "hat_loesung": (pfad / "loesung.tex").is_file(),
            }
        )
    gefunden.sort(key=lambda a: (a["nr"], a["key"]))
    return gefunden


def skript_index() -> list[dict]:
    """Liest die Aufgaben-Tabelle aus skript/aufgaben.md."""
    datei = SKRIPT / "aufgaben.md"
    if not datei.is_file():
        return []
    eintraege: list[dict] = []
    for zeile in datei.read_text(encoding="utf-8").splitlines():
        zeile = zeile.strip()
        if not zeile.startswith("|"):
            continue
        zellen = [z.strip() for z in zeile.strip("|").split("|")]
        if len(zellen) < 2 or not zellen[0].isdigit():
            continue
        eintraege.append(
            {
                "nr": int(zellen[0]),
                "titel": zellen[1],
                "fundstelle": zellen[2] if len(zellen) > 2 else "",
            }
        )
    return eintraege


def skript_stand() -> dict[str, str]:
    """Liest skript/aktuell.md (Version, Datum, Prüfsumme)."""
    datei = SKRIPT / "aktuell.md"
    stand: dict[str, str] = {}
    if not datei.is_file():
        return stand
    for zeile in datei.read_text(encoding="utf-8").splitlines():
        if ":" in zeile:
            schluessel, _, wert = zeile.partition(":")
            stand[schluessel.strip().lower()] = wert.strip()
    return stand


# ------------------------------------------------------------- Schreiben


def tex_sicher(text: str) -> str:
    """Sonderzeichen, die in Überschriften Ärger machen, maskieren."""
    ersatz = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(ersatz.get(z, z) for z in text)


def schreibe_generated(aufgaben: list[dict], nur_theorie: bool, nur_loesungen: bool) -> None:
    GENERIERT.mkdir(exist_ok=True)

    stand = skript_stand()
    beschriftung = stand.get("titel") or "Skript der Vorlesung"
    teile = [beschriftung]
    if stand.get("version"):
        teile.append(f"vom {stand['version']}")
    if stand.get("pruefsumme"):
        teile.append(f"({stand['pruefsumme']})")
    stand_text = " ".join(teile) if stand else "Skript noch nicht hinterlegt"

    (GENERIERT / "meta.tex").write_text(
        "% Automatisch erzeugt von werkzeuge/build.py. Nicht bearbeiten.\n"
        f"\\renewcommand{{\\SkriptStand}}{{{tex_sicher(stand_text)}}}\n"
        f"\\renewcommand{{\\SkriptQuelle}}{{{tex_sicher(stand.get('datei', ''))}}}\n"
        f"\\renewcommand{{\\StandDatum}}{{{date.today().strftime('%d.%m.%Y')}}}\n",
        encoding="utf-8",
    )

    zeigetheorie = "false" if nur_loesungen else "true"
    zeigeloesungen = "false" if nur_theorie else "true"
    (GENERIERT / "modus.tex").write_text(
        "% Automatisch erzeugt von werkzeuge/build.py. Nicht bearbeiten.\n"
        f"\\zeigetheorie{zeigetheorie}\n"
        f"\\zeigeloesungen{zeigeloesungen}\n",
        encoding="utf-8",
    )

    kopf = "% Automatisch erzeugt von werkzeuge/build.py. Nicht bearbeiten.\n\n"

    theorie_zeilen = [kopf]
    loesung_zeilen = [kopf]
    for aufgabe in aufgaben:
        kopfzeile = (
            f"\\aufgabenkopf{{{tex_sicher(aufgabe['skript'])}}}\n"
            if aufgabe["skript"]
            else ""
        )
        if aufgabe["hat_theorie"]:
            theorie_zeilen.append(
                f"\\section{{{tex_sicher(aufgabe['titel'])}}}\n"
                f"\\label{{aufg:{aufgabe['key']}}}\n"
                f"{kopfzeile}"
                f"\\input{{aufgaben/{aufgabe['key']}/theorie.tex}}\n"
                f"\\loesungsverweis{{{aufgabe['key']}}}\n\n"
            )
        if aufgabe["hat_loesung"]:
            loesung_zeilen.append(
                f"\\section{{Lösung: {tex_sicher(aufgabe['titel'])}}}\n"
                f"\\label{{loes:{aufgabe['key']}}}\n"
                f"\\input{{aufgaben/{aufgabe['key']}/loesung.tex}}\n"
                f"\\theorieverweis{{{aufgabe['key']}}}\n\n"
            )

    if len(theorie_zeilen) == 1:
        theorie_zeilen.append("\\section*{Keine Aufgaben hinterlegt}\n")
    if len(loesung_zeilen) == 1:
        loesung_zeilen.append("\\section*{Keine Lösungen hinterlegt}\n")

    (GENERIERT / "teil-theorie.tex").write_text("".join(theorie_zeilen), encoding="utf-8")
    (GENERIERT / "teil-loesungen.tex").write_text("".join(loesung_zeilen), encoding="utf-8")


# ------------------------------------------------------------- Berichte


def abdeckung(aufgaben: list[dict], schreiben: bool = True) -> tuple[list[dict], list[dict]]:
    """Vergleicht Skript-Index mit den vorhandenen Ordnern."""
    index = skript_index()
    vorhanden = {a["nr"] for a in aufgaben}
    fehlend = [e for e in index if e["nr"] not in vorhanden]
    ueberzaehlig = [a for a in aufgaben if index and a["nr"] not in {e["nr"] for e in index}]

    if schreiben and index:
        zeilen = [
            "# Offene Aufgaben",
            "",
            "Aufgaben aus dem Skript, für die es unter `aufgaben/` noch nichts gibt.",
            "Erzeugt von `werkzeuge/build.py`, wird bei jedem Build neu geschrieben.",
            "",
            "| Nr | Titel | Fundstelle |",
            "|----|-------|------------|",
        ]
        for eintrag in fehlend:
            zeilen.append(f"| {eintrag['nr']} | {eintrag['titel']} | {eintrag['fundstelle']} |")
        if not fehlend:
            zeilen.append("| - | alles bearbeitet | - |")
        zeilen.append("")
        (SKRIPT / "offen.md").write_text("\n".join(zeilen), encoding="utf-8")

    return fehlend, ueberzaehlig


def bericht(aufgaben: list[dict], fehlend: list[dict], ueberzaehlig: list[dict]) -> None:
    index = skript_index()
    print(f"Aufgaben im Skript-Index: {len(index)}" if index else "Kein Skript-Index vorhanden")
    print(f"Aufgaben-Ordner: {len(aufgaben)}")
    for aufgabe in aufgaben:
        luecken = []
        if not aufgabe["hat_theorie"]:
            luecken.append("theorie.tex fehlt")
        if not aufgabe["hat_loesung"]:
            luecken.append("loesung.tex fehlt")
        marke = "ok" if not luecken else "UNVOLLSTÄNDIG: " + ", ".join(luecken)
        print(f"  {aufgabe['nr']:02d} {aufgabe['titel']} [{marke}]")
    if fehlend:
        print("Noch offen (im Skript, hier ohne Ordner):")
        for eintrag in fehlend:
            print(f"  {eintrag['nr']:02d} {eintrag['titel']} ({eintrag['fundstelle']})")
    if ueberzaehlig:
        print("Ohne Skript-Eintrag (Nummer im Index prüfen):")
        for aufgabe in ueberzaehlig:
            print(f"  {aufgabe['nr']:02d} {aufgabe['titel']}")


# ------------------------------------------------------------- Kompilieren


def pdflatex_ausschnitt(protokoll: str) -> str:
    zeilen = protokoll.splitlines()
    wichtig = [z for z in zeilen if z.startswith("!") or re.match(r"^\./|^tex/|^aufgaben/|^generated/", z)]
    if not wichtig:
        wichtig = zeilen[-15:]
    return "\n".join(wichtig[-25:])


def kompilieren(ziel: Path) -> bool:
    OUT.mkdir(exist_ok=True)
    for lauf in (1, 2):
        ergebnis = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-halt-on-error",
                f"-output-directory={OUT}",
                "tex/main.tex",
            ],
            cwd=WURZEL,
            capture_output=True,
            text=True,
        )
        if ergebnis.returncode != 0:
            print(f"pdflatex ist im Durchlauf {lauf} abgebrochen:")
            print(pdflatex_ausschnitt(ergebnis.stdout))
            return False

    gebaut = OUT / "main.pdf"
    if not gebaut.is_file():
        print("pdflatex hat kein PDF erzeugt.")
        return False
    shutil.move(str(gebaut), str(ziel))
    for rest in OUT.glob("main.*"):
        rest.unlink()
    return True


# ----------------------------------------------------------------- Haupt


def main() -> int:
    parser = argparse.ArgumentParser(description="Baut das Lern-PDF aus aufgaben/.")
    modus = parser.add_mutually_exclusive_group()
    modus.add_argument("--nur-theorie", action="store_true", help="nur Teil I bauen")
    modus.add_argument("--nur-loesungen", action="store_true", help="nur Teil II bauen")
    parser.add_argument("--offen", action="store_true", help="nur Abdeckung prüfen, nichts bauen")
    parser.add_argument("--kein-pdf", action="store_true", help="generated/ schreiben, nicht kompilieren")
    args = parser.parse_args()

    aufgaben = sammle_aufgaben()
    fehlend, ueberzaehlig = abdeckung(aufgaben, schreiben=not args.offen)
    bericht(aufgaben, fehlend, ueberzaehlig)

    if args.offen:
        return 0

    schreibe_generated(aufgaben, args.nur_theorie, args.nur_loesungen)
    print("generated/ neu geschrieben")

    if args.kein_pdf:
        return 0

    if args.nur_theorie:
        ziel = OUT / "physik-theorie.pdf"
    elif args.nur_loesungen:
        ziel = OUT / "physik-loesungen.pdf"
    else:
        ziel = OUT / "physik-uebungen.pdf"

    if not kompilieren(ziel):
        return 1
    groesse = ziel.stat().st_size / 1024
    print(f"gebaut: {ziel.relative_to(WURZEL)}  ({groesse:.0f} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
