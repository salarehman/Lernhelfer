#!/usr/bin/env python3
"""Baut die Lernhelfer-PDFs aus den Aufgaben-Ordnern.

Aufbau: aufgaben/<fach>/<blattNN>/<NN-slug>/  mit theorie.tex und loesung.tex.
Für jede gefundene Kombination aus Fach und Blatt wird erzeugt:

    out/<fach>/<blattNN>-lernhelfer.pdf   (Teil I Theorie + Teil II Lösung)
    out/<fach>/<blattNN>-theorie.pdf      (nur Teil I Theorie)

Der Build erzeugt generated/*.tex und kompiliert tex/main.tex mit pdflatex;
fehlt pdflatex, wird Tectonic verwendet (GLEICHES VERHALTEN wie pdflatex,
Temperatur-Kopie _bm.tex im Repo-Wurzelverzeichnis).

Aufrufe (immer aus dem Repo-Wurzelverzeichnis):

    python3 werkzeuge/build.py                  # alle Fächer/Blätter bauen
    python3 werkzeuge/build.py --fach physik    # nur ein Fach
    python3 werkzeuge/build.py --offen          # nur Überblick, nichts bauen
    python3 werkzeuge/build.py --kein-pdf       # nur generated/ schreiben
"""

from __future__ import annotations

import argparse
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
FACH_RE = re.compile(r"^([a-záéöü]+)$")
BLATT_RE = re.compile(r"^blatt(\d+)$")
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


def sammle_faecher() -> list[str]:
    """Fach-Ordnernamen unter aufgaben/, sortiert (physik, mathe, ...)."""
    if not AUFGABEN.is_dir():
        return []
    return sorted(
        d.name for d in AUFGABEN.iterdir()
        if d.is_dir() and d.name != ARCHIVNAME and FACH_RE.match(d.name)
    )


def sammle_blaetter(fach: str) -> list[dict]:
    """Blätter eines Fachs: aufgaben/<fach>/blattNN/."""
    fach_pfad = AUFGABEN / fach
    if not fach_pfad.is_dir():
        return []
    blaetter: list[dict] = []
    for pfad in sorted(fach_pfad.iterdir()):
        if not pfad.is_dir():
            continue
        treffer = BLATT_RE.match(pfad.name)
        if not treffer:
            print(f"  Hinweis: wird übersprungen (kein blattNN): {pfad.name}")
            continue
        aufgaben = sammle_aufgaben(fach, pfad.name)
        if not aufgaben:
            continue
        blaetter.append(
            {
                "nr": int(treffer.group(1)),
                "name": pfad.name,
                "pfad": pfad,
                "aufgaben": aufgaben,
            }
        )
    blaetter.sort(key=lambda b: b["nr"])
    return blaetter


def sammle_aufgaben(fach: str, blatt: str) -> list[dict]:
    """Aufgaben in aufgaben/<fach>/<blatt>/ mit Nummernpräfix."""
    blatt_pfad = AUFGABEN / fach / blatt
    gefunden: list[dict] = []
    if not blatt_pfad.is_dir():
        return gefunden
    for pfad in sorted(blatt_pfad.iterdir()):
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
                "rel": f"{fach}/{blatt}/{pfad.name}",
                "pfad": pfad,
                "titel": meta.get("titel") or titel_aus_slug(treffer.group(2)),
                "skript": meta.get("skript", ""),
                "hat_theorie": (pfad / "theorie.tex").is_file(),
                "hat_loesung": (pfad / "loesung.tex").is_file(),
            }
        )
    gefunden.sort(key=lambda a: (a["nr"], a["key"]))
    return gefunden


def skript_stand(fach: str) -> dict[str, str]:
    """Liest skript/<fach>/aktuell.md (Version, Datum, Prüfsumme)."""
    datei = SKRIPT / fach / "aktuell.md"
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


def schreibe_generated(fach: str, blatt: dict, nur_theorie: bool) -> None:
    """Schreibt generated/ für ein Fach+Blatt in die gewünschte Variante."""
    GENERIERT.mkdir(exist_ok=True)
    aufgaben = blatt["aufgaben"]

    stand = skript_stand(fach)
    beschriftung = stand.get("titel") or "Skript der Vorlesung"
    teile = [beschriftung]
    if stand.get("version"):
        teile.append(f"vom {stand['version']}")
    if stand.get("pruefsumme"):
        teile.append(f"({stand['pruefsumme']})")
    stand_text = " ".join(teile) if stand else "Skript noch nicht hinterlegt"

    fach_titel = {
        "physik": "Physik",
        "mathe": "Mathematik",
    }.get(fach, fach.capitalize())

    (GENERIERT / "meta.tex").write_text(
        "% Automatisch erzeugt von werkzeuge/build.py. Nicht bearbeiten.\n"
        f"\\renewcommand{{\\SkriptStand}}{{{tex_sicher(stand_text)}}}\n"
        f"\\renewcommand{{\\SkriptQuelle}}{{{tex_sicher(stand.get('datei', ''))}}}\n"
        f"\\renewcommand{{\\StandDatum}}{{{date.today().strftime('%d.%m.%Y')}}}\n"
        f"\\renewcommand{{\\Fachtitel}}{{{fach_titel}, Blatt {blatt['nr']}}}\n",
        encoding="utf-8",
    )

    zeigetheorie = "true"
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
                f"\\label{{aufg:{fach}/{aufgabe['key']}}}\n"
                f"{kopfzeile}"
                f"\\input{{aufgaben/{aufgabe['rel']}/theorie.tex}}\n"
                f"\\loesungsverweis{{{aufgabe['key']}}}\n\n"
            )
        if aufgabe["hat_loesung"]:
            loesung_zeilen.append(
                f"\\section{{Lösung: {tex_sicher(aufgabe['titel'])}}}\n"
                f"\\label{{loes:{fach}/{aufgabe['key']}}}\n"
                f"\\input{{aufgaben/{aufgabe['rel']}/loesung.tex}}\n"
                f"\\theorieverweis{{{aufgabe['key']}}}\n\n"
            )

    if len(theorie_zeilen) == 1:
        theorie_zeilen.append("\\section*{Keine Aufgaben hinterlegt}\n")
    if len(loesung_zeilen) == 1:
        loesung_zeilen.append("\\section*{Keine Lösungen hinterlegt}\n")

    (GENERIERT / "teil-theorie.tex").write_text("".join(theorie_zeilen), encoding="utf-8")
    (GENERIERT / "teil-loesungen.tex").write_text("".join(loesung_zeilen), encoding="utf-8")


# ------------------------------------------------------------- Kompilieren


def habe_prog(name: str) -> bool:
    return shutil.which(name) is not None


def pdflatex_ausschnitt(protokoll: str) -> str:
    zeilen = protokoll.splitlines()
    wichtig = [z for z in zeilen if z.startswith("!") or re.match(r"^\./|^tex/|^aufgaben/|^generated/", z)]
    if not wichtig:
        wichtig = zeilen[-15:]
    return "\n".join(wichtig[-25:])


def kompilieren_tectonic(ziel: Path) -> bool:
    """pdflatex fehlt: Tectonic kompiliert tex/main.tex über eine Kopie an der
    Repo-Wurzel (path resolution und --outdir-Konflikt umgehen)."""
    t = shutil.which("tectonic") or str(WURZEL.parent / "bin" / "tectonic")
    kopie = WURZEL / "_bm.tex"
    shutil.copyfile(WURZEL / "tex" / "main.tex", kopie)
    OUT.mkdir(exist_ok=True)
    ergebnis = subprocess.run(
        [t, "--outdir", str(OUT), str(kopie)],
        cwd=WURZEL,
        capture_output=True,
        text=True,
    )
    kopie.unlink(missing_ok=True)
    if ergebnis.returncode != 0:
        print("tectonic abgebrochen:")
        print(pdflatex_ausschnitt(ergebnis.stderr or ergebnis.stdout))
        return False
    gebaut = OUT / "_bm.pdf"
    if not gebaut.is_file():
        print("Tectonic hat kein PDF erzeugt.")
        return False
    shutil.move(str(gebaut), str(ziel))
    return True


def kompilieren_pdflatex(ziel: Path) -> bool:
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


def kompilieren(ziel: Path) -> bool:
    OUT.mkdir(exist_ok=True)
    if habe_prog("pdflatex"):
        return kompilieren_pdflatex(ziel)
    return kompilieren_tectonic(ziel)


# ---------------------------------------------------------------- Berichte


def bericht(baetterpro_fach: dict[str, list[dict]]) -> None:
    for fach, blaetter in baetterpro_fach.items():
        print(f"\nFach: {fach}")
        if not blaetter:
            print("  (keine Blätter hinterlegt)")
            continue
        for blatt in blaetter:
            luecken = []
            for a in blatt["aufgaben"]:
                if not a["hat_theorie"]:
                    luecken.append(f"{a['nr']:02d} theorie fehlt")
                if not a["hat_loesung"]:
                    luecken.append(f"{a['nr']:02d} loesung fehlt")
            marke = "ok" if not luecken else "UNVOLLSTÄNDIG: " + ", ".join(luecken)
            print(f"  {blatt['name']}: {len(blatt['aufgaben'])} Aufgaben [{marke}]")


# ----------------------------------------------------------------- Haupt


def main() -> int:
    parser = argparse.ArgumentParser(description="Baut Lernhelfer-PDFs aus aufgaben/<fach>/<blatt>/.")
    parser.add_argument("--fach", default=None, help="nur dieses Fach bauen (z. B. physik, mathe)")
    parser.add_argument("--offen", action="store_true", help="nur Überblick, nichts bauen")
    parser.add_argument("--kein-pdf", action="store_true", help="generated/ schreiben, nicht kompilieren")
    args = parser.parse_args()

    faecher = sammle_faecher()
    if args.fach:
        if args.fach not in faecher:
            print(f"Unbekanntes Fach: {args.fach}. Verfügbar: {faecher}")
            return 1
        faecher = [args.fach]

    baetterpro_fach: dict[str, list[dict]] = {}
    for fach in faecher:
        baetterpro_fach[fach] = sammle_blaetter(fach)

    bericht(baetterpro_fach)

    if args.offen:
        return 0

    ziele: list[Path] = []
    for fach, blaetter in baetterpro_fach.items():
        for blatt in blaetter:
            fach_dir = OUT / fach
            fach_dir.mkdir(exist_ok=True)
            stamm = fach_dir / blatt["name"]

            schreibe_generated(fach, blatt, nur_theorie=False)
            if not args.kein_pdf:
                ziel = Path(str(stamm) + "-lernhelfer.pdf")
                if not kompilieren(ziel):
                    return 1
                ziele.append(ziel)

            schreibe_generated(fach, blatt, nur_theorie=True)
            if not args.kein_pdf:
                ziel = Path(str(stamm) + "-theorie.pdf")
                if not kompilieren(ziel):
                    return 1
                ziele.append(ziel)

    if args.kein_pdf:
        print("generated/ neu geschrieben (zuletzt: Theorie-Variante).")
        return 0

    for ziel in ziele:
        print(f"gebaut: {ziel.relative_to(WURZEL)}  ({ziel.stat().st_size / 1024:.0f} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
