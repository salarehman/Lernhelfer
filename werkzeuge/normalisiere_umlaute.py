#!/usr/bin/env python3
"""normalisiere_umlaute.py — Schweizer-Deutsch-Orthografie im Lernhelfer-Repo.

1) ß -> ss  überall (Schweizer Konvention; unterdrückt zugleich die „SS“-Artefakte,
   die LaTeX/Uppercase-Kopfzeilen aus ß erzeugen).
2) Transliterierte Umlaute (ae/oe/ue -> ä/ö/ü) NUR in vetteten deutschen Wörtern
   (Wortgrenzen-exakt). NICHT blind: legitime Wörter wie „Frequenz“, „Koeffizient“,
   „Quelle“, „Sauerstoff“, „quer“, „genauer“, „Dauer“, „neue“, „zuerst“ bleiben
   unangetastet (stehen schlicht NICHT in der Liste).

SICHERHEIT: Dateinamen, Pfade, \\input/\\ref/\\label/\\includegraphics/\\SI-Ziele,
URLs, backtick-Code-Spans und Diagramm-Pfade werden VOR der Umlaut-Übersetzung
durch einzigartige Platzhalter ersetzt und danach exakt zurückgesetzt, damit
Build & Werkzeuge intakt bleiben. ß->ss wird auf der gesamten Zeile angewandt
(ße kommt in Bezeichnern praktisch nie vor) — dafür werden die Platzhalter vorher
wieder eingesetzt, damit „ß“ in Bezeichnern (falls vorhanden) erhalten bleibt.

Aufruf (Repo-Wurzelverzeichnis, z. B. im Worktree):
    python3 werkzeuge/normalisiere_umlaute.py --check   # nur anzeigen (Dateiliste)
    python3 werkzeuge/normalisiere_umlaute.py           # anwenden
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
FAECHER = ["mathe", "physik", "chemie"]
MEHR_DOKS = ["README.md", "AGENTS.md", "docs/arbeitsweise.md", "docs/adam-sync.md"]

# ---------------------------------------------------------------- Wörterbuch
UMLAUT = {
    # ue -> ü
    "fuer": "für", "Fuer": "Für", "dafuer": "dafür",
    "zurueck": "zurück", "zurueckrechnen": "zurückrechnen", "zurueckfuehren": "zurückführen",
    "Rueckweg": "Rückweg", "Rueckfahrt": "Rückfahrt", "Ruecktreibende": "Rücktreibende",
    "ruecktreibender": "rücktreibender",
    "ueber": "über", "uebernimmt": "übernimmt", "uebernehmen": "übernehmen",
    "uebersteigen": "übersteigen", "ueberlagern": "überlagern", "ueberein": "überein",
    "uebt": "übt", "ausuebt": "ausübt",
    "wuerde": "würde", "bezueglich": "bezüglich", "abhaengig": "abhängig",
    "unabhaengige": "unabhängige", "wegunabhaengig": "wegunabhängig", "vertraeglich": "verträglich",
    "stueck": "Stück", "Stueck": "Stück", "Stuecks": "Stücks",
    "stueckweise": "stückweise", "Stueckweise": "Stückweise", "Reststueck": "Reststück",
    "verknuepft": "verknüpft", "kuerzen": "kürzen", "kuerzt": "kürzt",
    "gekruemmten": "gekrümmten", "gedrueckt": "gedrückt", "Eindruecken": "Eindrücken",
    "ausdruecken": "ausdrücken", "Molekuelen": "Molekülen", "Spruenge": "Sprünge",
    "pruefen": "prüfen", "prueft": "prüft", "geprueft": "geprüft",
    "pruefbar": "prüfbar", "Dimensionsprauefung": "Dimensionsprüfung",
    "behaelt": "behält", "erhaelt": "erhält", "enthaelt": "enthält",
    "haelt": "hält", "Behaelters": "Behälters", "zueinander": "zueinander",
    "uebrigens": "übrigens", "Verfuegung": "Verfügung", "begruendet": "begründet",
    "aufwaendig": "aufwändig", "Eiskunstlaeufer": "Eiskunstläufer",
    # ae -> ä
    "Laenge": "Länge", "laengs": "längs", "laengere": "längere",
    "Fadenlaenge": "Fadenlänge", "Armlaenge": "Armlänge", "Laengsspannung": "Längsspannung",
    "Laengeneinheit": "Längeneinheit",
    "faellt": "fällt", "abfaellt": "abfällt", "entfaellt": "entfällt",
    "haengt": "hängt", "laesst": "lässt", "waechst": "wächst",
    "haengende": "hängende", "haengenden": "hängenden",
    "zusammenhaengenden": "zusammenhängenden", "betraegt": "beträgt",
    "Betraege": "Beträge", "Elementbeitraege": "Elementbeiträge",
    "waehlen": "wählen", "waehlt": "wählt", "waehlbare": "wählbare",
    "waehlbaren": "wählbaren", "waehlbar": "wählbar", "gewaehlt": "gewählt",
    "gewaehlten": "gewählten", "zaehlt": "zählt", "Zaehle": "Zähle",
    "Zaehlen": "Zählen", "durchzaehlen": "durchzählen", "abzaehlen": "abzählen",
    "zunaechst": "zunächst", "zusaetzlich": "zusätzlich", "zusaetzliche": "zusätzliche",
    "Zusaetzlich": "Zusätzlich",
    "Verstaendnisfrage": "Verständnisfrage", "Verstaendnisfragen": "Verständnisfragen",
    "vollstaendig": "vollständig", "unvollstaendig": "unvollständig",
    "vollstaendigen": "vollständigen", "vernachlaessig": "vernachlässig",
    "vernachlaessigen": "vernachlässigen",
    "tatsaechlich": "tatsächlich", "tatsaechliche": "tatsächliche",
    "gleichfoermig": "gleichförmig", "gleichfoermige": "gleichförmige",
    "gleichfoermiges": "gleichförmiges", "gleichfoermigen": "gleichförmigen",
    "Regelmaessig": "Regelmäßig", "regelmaessig": "regelmäßig",
    "gleichmaessig": "gleichmäßig", "gleichmaessiger": "gleichmäßiger",
    "naeherungsweise": "näherungsweise", "naehert": "nähert", "naechsten": "nächsten",
    "Beschraenktheit": "Beschränktheit", "aendert": "ändert", "veraendert": "verändert",
    "unveraendert": "unverändert", "Radiusaenderung": "Radiusänderung",
    "Energieaenderung": "Energieänderung", "Geschwindigkeitsaenderung": "Geschwindigkeitsänderung",
    "aeusser": "äußere", "AEusser": "Äußere", "aeussere": "äußere",
    "aeusseres": "äußeres", "ausser": "außer", "aussen": "außen",
    "staendig": "ständig", "bestaendig": "beständig", "Staende": "Stände",
    "ausgeraeumt": "ausgeräumt", "verstaerktes": "verstärktes",
    "zusammenfuehren": "zusammenführen", "Geschwindigkeitsaenderung": "Geschwindigkeitsänderung",
    "Flaeche": "Fläche", "Auflageflaeche": "Auflagefläche", "Brettflaeche": "Brettfläche",
    "Parallelogrammflaeche": "Parallelogrammfläche", "Rechteckflaeche": "Rechteckfläche",
    "Flaecheninhalt": "Flächeninhalt", "Hoehstwert": "Höchstwert", "erhoeht": "erhöht",
    "hoechster": "höchster", "hoechsten": "höchsten", "koennte": "könnte",
    "Moebelruecken": "Möbelrücken", "gewoehnliche": "gewöhnliche",
    # oe -> ö
    "Koerper": "Körper", "koerper": "körper", "Koerpers": "Körpers",
    "Freikoerperbild": "Freikörperbild", "stoesst": "stößt", "Stoessen": "Stößen",
    # ae -> ä (Grössen, Trägheit, Verhältnis, Kräfte, …)
    "Groesse": "Größe", "Groessen": "Größen", "groesser": "größer",
    "groesseren": "größeren", "Traegheit": "Trägheit", "Traegheitsmoment": "Trägheitsmoment",
    "Traegheitskraefte": "Trägheitskräfte", "Verhaeltnis": "Verhältnis",
    "Verhaeltnisse": "Verhältnisse", "Stoffmengenverhaeltnis": "Stoffmengenverhältnis",
    "Stoffmengenverhaeltnisse": "Stoffmengenverhältnisse", "Zahlenverhaeltnis": "Zahlenverhältnis",
    "Mengenverhaeltnisse": "Mengenverhältnisse", "Frequenzverhaeltnisse": "Frequenzverhältnisse",
    "Normalkraefte": "Normalkräfte", "Gegenkraefte": "Gegenkräfte", "Kraefte": "Kräfte",
    "Kraeften": "Kräften", "Kraeftegleichgewicht": "Kräftegleichgewicht",
    "Kraeftegleichung": "Kräftegleichung", "Loesung": "Lösung", "losung": "Lösung",
    "loesungen": "Lösungen", "Loesungsweg": "Lösungsweg",
    "Loesungskonstanten": "Lösungskonstanten", "aufloesen": "Auflösen", "Aufloesen": "Auflösen",
    "Pruefung": "Prüfung", "Dimensionspruefung": "Dimensionsprüfung",
    "Zaehler": "Zähler", "zaehlbar": "zählbar",
    "Vohaeltnis": "Verhältnis",
}

_P = [(re.compile(rf"(?<![A-Za-zÄÖÜäöüß]){re.escape(k)}(?![A-Za-zÄÖÜäöüß])"), v)
      for k, v in UMLAUT.items()]

# Namenspanne, die NIEMALS übersetzt werden dürfen (Dateien, Pfade, LaTeX-Ziele,
# Befehle, backtick-Code). Eine kombinierte Alternative, längste zuerst, in einem
# einzigen Pass — so werden ineinanderliegende Spannen nicht doppelt verarbeitet.
# WICHTIG: nur Befehle mit einem einzelnen Literal-Argument (Pfad/Label/Zahl/URL)
# maskieren, NIEMALS Textbefehle wie \\textbf{…} oder \\kasten{…}, deren Inhalt
# deutsche Wörter trägt und übersetzt werden soll.
_CMD = (r"\\(?:input|includegraphics|include|label|ref|pageref|SI|qty|num|url|href)"
        r"\{[^{}]*\}")
_MASKE = re.compile(rf"{_CMD}|`[^`]*`|[\w./-]+\.[A-Za-z]{{1,4}}(?![A-Za-z])")


def anwenden(text: str) -> str:
    out = []
    for zeile in text.split("\n"):
        ph_map = {}
        idx = [0]
        def _keep(m):
            ph = f"\x00N{idx[0]}\x00"
            ph_map[ph] = m.group(0)
            idx[0] += 1
            return ph
        zeile_m = _MASKE.sub(_keep, zeile)
        for pat, repl in _P:
            zeile_m = pat.sub(repl, zeile_m)
        zeile_m = zeile_m.replace("ß", "ss")
        for ph, orig in ph_map.items():
            zeile_m = zeile_m.replace(ph, orig)
        out.append(zeile_m)
    return "\n".join(out)


def ziele() -> list[Path]:
    out = []
    for fach in FAECHER:
        out += list((WURZEL / "aufgaben" / fach).rglob("*.tex"))
    for d in MEHR_DOKS:
        out.append(WURZEL / d)
    return sorted({z for z in out if z.exists()})


def main() -> int:
    check = "--check" in sys.argv
    anz = 0
    for pfad in ziele():
        t = pfad.read_text(encoding="utf-8")
        neu = anwenden(t)
        if neu == t:
            continue
        anz += 1
        if check:
            print(f"CHECK: {pfad.relative_to(WURZEL)}")
        else:
            pfad.write_text(neu, encoding="utf-8")
            print(f"  geändert: {pfad.relative_to(WURZEL)}")
    print(f"{'CHECK' if check else 'OK'}: {anz} Datei(en).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
