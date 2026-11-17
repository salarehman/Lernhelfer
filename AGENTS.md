# Arbeitsregeln für dieses Repository

Diese Regeln gelten für Menschen und Agenten. Ziel ist ein Lernwerkzeug für
universitäre Aufgaben aus mehreren Fächern (Physik, Mathematik, Chemie, …),
nicht das bloße Produzieren von Musterlösungen. Vor Änderungen README.md, diese
Datei und die relevanten Quellen lesen.

## Zwei Repos: öffentlich + privat

Dieses Repo (`Lernhelfer`) ist **öffentlich** und enthält NUR selbst
geschriebene Inhalte. Das urheberrechtlich geschützte Vorlesungsmaterial
(Skripte, eingescannte Übungsblätter) liegt im privaten Repo
`Lernhelfer-Material` und gehört NIEMALS hierher:

- **`Lernhelfer`** (dieses, öffentlich) — `aufgaben/`, `tex/`, `werkzeuge/`,
  `out/`, `docs/`.
- **`Lernhelfer-Material`** (privat) — `eingang/<fach>/` (neue Blätter+Skripte
  aus adam-sync) und `skript/<fach>/` (geschützte Skript-PDFs).

Die Git-Historie ist bereits sauber geschrieben (kein Material drin); dieser
Zustand bewahren. Niemals Skript- oder Blatt-PDFs einchecken.

## Ziel und Trennung

Jede Aufgabe liegt als LaTeX-Ordner unter `aufgaben/<fach>/<blattNN>/` und hat
zwei getrennte Teile, in zwei Dateien:

- **Teil I: Theorie** (`theorie.tex`). Erkläre verständlich und präzise nur die
  Begriffe, Sätze, Definitionen, allgemeinen Gleichungen, Voraussetzungen und
  typischen Fehler, die für die Aufgabe nützlich sind. Verweise auf die
  Fundstelle im Skript. Keine aufgabenspezifischen Zahlen, keine konkrete
  Reihenfolge der Rechenschritte, kein versteckter Lösungsweg und kein Ergebnis.
  Der Ansatz bleibt eigene Denkarbeit. **Knapp halten** — der Nutzer will selbst
  denken lernen; Über-erklären zerstört den Zweck.
- **Teil II: Lösung** (`loesung.tex`). Führe nachvollziehbar durch den
  Lösungsweg: Gegebenes und Gesuchtes, begründeter Ansatz, verständliche
  Rechnung, Ergebnis und passende Prüfung. Erkläre den entscheidenden
  Gedankenschritt und, wo sinnvoll, was auf ähnliche Aufgaben übertragbar ist.
  Nicht unnötig ausschweifen.

Prüfe die Trennung inhaltlich, nicht nur anhand der Dateinamen.

## Struktur

```text
aufgaben/<fach>/<blattNN>/NN-slug/   je Aufgabe: theorie.tex + loesung.tex
aufgaben/archiv/          aufbewahrte Beispiele, werden nicht mitgebaut
tex/                      geteiltes Layout + Hauptdatei
werkzeuge/                build.py, neue_aufgabe.py, chemie.py
skript/<fach>/aktuell.md  nur Metadaten (Fassung, Prüfsumme); die PDFs liegen privat
out/                      <fach>-<blattNN>-lernhelfer.pdf (Theorie + Lösung)
generated/                vom Build erzeugt, nicht bearbeiten/einchecken
```

Ein **Übungsblatt** = ein `blattNN`-Ordner in einem Fach. Ein **Lernhelfer** =
das gebaute PDF `out/<fach>/<blattNN>-lernhelfer.pdf`, das beide Teile (Theorie
+ Lösung) in einem Dokument vereint: erst die Theorie je Aufgabe, dann die
durchgerechneten Lösungen. Es gibt **keine** separate Theorie-PDF — pro Fach und
Blatt wird genau EIN Lernhelfer gebaut.

## Übungsblätter und Lernhelfer

- **Ein Blatt, ein eigener Lernhelfer.** Keine Aufgaben verschiedener Blätter
  oder Fächer in denselben Lernhelfer mischen, ausser der Nutzer verlangt
  ausdrücklich eine Sammlung.
- Bearbeite grundsätzlich alle Aufgaben und Teilaufgaben eines Blatts.
  Kennzeichne jede Aufgabe durch **Fach, Blatt und Aufgabennummer**, z. B.
  `Physik Blatt 7, A1` (Metadaten `% titel:` in `theorie.tex`).
- Verlinke Ergebnisse und Bearbeitungsstand in `out/` und im README.
- Bevor du baust, prüfe, dass nur Aufgaben des gewünschten Fach/Blatts
  aufgenommen werden; prüfe danach das PDF auf Vollständigkeit.

## Wöchentlicher Ablauf (das ist die Kernaufgabe)

Der Nutzer holt wöchentlich neue Unterlagen per `adam-sync` ins private
Material-Repo (`eingang/<fach>/`). Der Agent übernimmt die Einordnung und baut
die Lernhelfer:

1. **Eingang sichten.** Im privaten Material-Repo (`eingang/<fach>/`) den neuen
   Aufgabentext und ggf. das neue Skript lesen. Fach zuordnen (physik, mathe,
   chemie). `eingang.py einordnen --public ../Lernhelfer` zieht Skripte nach
   `skript/<fach>/` und legt Scaffold-Ordner hier unter `aufgaben/<fach>/blattNN/` an.
2. **Sortieren/Ausfüllen.** Je Aufgabe einen Ordner `NN-slug/` mit
   `theorie.tex` und `loesung.tex` anlegen (oder `neue_aufgabe.py <fach> <blatt>
   <nummer> "Titel"`). Für jede Aufgabe Theorie (Teil I, knapp, **lösungsfrei**)
   und Lösung (Teil II) schreiben. Konkrete Zahlen und die Aufgabenstellung nur
   aus der tatsächlichen PDF übernehmen — nichts erfinden.
3. **Bauen.** `python3 werkzeuge/build.py` im Repo-Wurzelverzeichnis (baut alle
   Fächer+Blätter) bzw. `--fach <fach>` für eines. Das Ergebnis liegt in
   `out/<fach>/<blattNN>-lernhelfer.pdf`.
4. **Prüfen.** Jede Datei beim Build automatisch prüfen; die Theorie lösungsfrei
   lassen; Inhalte aus dem Skript verifizieren.
5. **Commit + Push** im Git. Skripte/Blätter bleiben im privaten Repo.

**Ein Lernhelfer pro Fach und Woche:** der Nutzer erwartet pro Fach genau einen
Lernhelfer (physik, mathe, chemie), jeder mit zwei Teilen. Ein Fach ohne
Blatt diese Woche bleibt außen vor.

## Chemie

Das Fach `chemie` ist vollständig eingerichtet (`fach_titel` im Build,
`aufgaben/chemie/`, `skript/chemie/`). Die ersten Blätter kommen, sobald ein
Chemie-Blatt über adam-sync eintrifft. Für Chemie-Figuren (Molekülstrukturen,
Energie-/Orbital-/Symmetrie-Diagramme) nutze `werkzeuge/chemie.py`:

```bash
# braucht rdkit + matplotlib (z. B. /opt/data/scienv/bin/python)
python3 werkzeuge/chemie.py mol --smiles 'CCO' --out aufgaben/chemie/blatt01/01-x/figures/ethanol.png
python3 werkzeuge/chemie.py energie --zustände 0,3,1.5 --out .../figures/energie.png
python3 werkzeuge/chemie.py orbital --typ p --achse x --out .../figures/orb.png
python3 werkzeuge/chemie.py symmetrie --punkte C2,H,H --out .../figures/sym.png
```

PNGs einbinden mit `\includegraphics{...}` (graphicx ist geladen); Pfade
relativ zur Repo-Wurzel (tectonic-Auflösung) angeben. `--dpi N` zum Nachschärfen.

## Kommunikation mit dem Nutzer (wichtig)

- Nachrichten kommen per Chat (z. B. Telegram). **Kein laufender Kommentar.**
  Keine Extra-Nachrichten pro Teilschritt; arbeiten und erst melden, wenn etwas
  fertig ist oder ein echter Blocker auftritt.
- Nicht jeder Zwischenschritt wird bestätigt: Bauen im Hintergrund machen,
  kein Fortschritts-Ticker.
- Bei mehrdeutiger Aufgabe auf den vernünftigen Standard zurückgreifen (das
  Fach/Blatt, das wirklich vorhanden ist) und die Annahme einmal in der
  Abschlussmeldung nennen. Nur bei echten Blocker (fehlende Angaben,
  unlesbares PDF, fehlende Rechte) nachfragen.
- LMS-Links (z. B. ADAM/ILIAS) sind hinter Login: nicht versuchen zu scrapen —
  darauf verweisen, dass der Nutzer `adam-sync setup` (einmaliger Browser-Login)
  ausgeführt hat. Nie nach Passwort im Chat fragen und Inhalte nie erfinden.

## Quellen und fachliche Qualität

- Verwende das aktuelle Skript des Fachs (privat, `Lernhelfer-Material/
  skript/<fach>/`) und den vollständigen Aufgabentext als maßgebliche Quellen.
  Nenne Kapitel und Seiten, soweit sicher bekannt.
- Erfinde keine Aufgaben, Werte, Sätze, Abbildungen oder Fundstellen.
  Kennzeichne ergänzende Annahmen als solche. Bei fehlenden Daten oder
  mehrdeutiger Aufgabenstellung nachfragen oder die Unsicherheit festhalten;
  keine scheinbar vollständige Lösung ausgeben.
- Aus PDF-Text extrahierte Formeln, Abbildungen und Nummerierung anhand des
  Originals prüfen. Rechne sorgfältig, prüfe Vorzeichen, Einheiten,
  Gültigkeitsbedingungen und nach Möglichkeit Grenzfälle oder Gegenbeispiele.

## Werkzeuge

- `python3 werkzeuge/build.py [--fach <fach>] [--offen] [--kein-pdf]` baut alle
  (oder nur die eines Fachs) Lernhelfer nach `out/`. `--kein-pdf` schreibt nur
  `generated/`. Fehlt `pdflatex`, kompiliert der Build automatisch mit
  `tectonic`.
- Neue Aufgabe: `python3 werkzeuge/neue_aufgabe.py <fach> <blatt> <nummer> "Titel"`
  erzeugt Platzhalter, keine fertige Bearbeitung. Entwürfe vor einem fertigen
  PDF kontrollieren.
- Chemie-Figuren: `python3 werkzeuge/chemie.py …` (siehe Abschnitt Chemie).
- Einordnung (im privaten Repo): `python3 werkzeuge/eingang.py sichten/einordnen
  --public <PFAD>`. Flake-Automation: `lernhelfer-sync` in `flake-environments`.

## Sprache, Sicherheit und Abschluss

- Dokument und Lerninhalte auf Deutsch; verständlich, knapp, fachlich genau.
  Keine Emojis, keine KI- oder Werkzeug-Bylines im Dokument oder in Commits.
- Größen mit `siunitx` (`\qty{}{}`) ausweisen; dimensionslose Zahlen und rein
  symbolische Gleichungen brauchen keine erfundene Einheit.
- Vor dem Teilen von Vorlesungsunterlagen Nutzungsrechte und Privatsphäre
  beachten. Keine Zugangsdaten einchecken und nichts Geschütztes ins öffentliche
  Repo (auch nicht in die Git-Historie) geben.
- Vor Abschluss fachliche Aussagen und Aufgabenabdeckung prüfen, den passenden
  Build ausführen und betroffene PDF-Seiten ansehen. Ein erfolgreicher LaTeX-Build
  ersetzt keine inhaltliche Prüfung. Bestehende Änderungen respektieren; sachliche
  Commits ohne Co-Author-Signatur.
