# AGENTS.md — Regeln für dieses Repository

Gelten für Menschen und Agenten. Vor Änderungen erst README.md, diese Datei,
die relevanten Quellen und ggf. [docs/adam-sync.md](docs/adam-sync.md) lesen.

## Zweck

Ein Lernwerkzeug für universitäre Aufgaben (Physik, Mathematik, Chemie …),
nicht das blosse Produzieren von Musterlösungen. Jede Aufgabe erscheint als
**Lernhelfer-PDF** mit zwei getrennten Teilen (Theorie, dann Lösung), die dem
Nutzer helfen, selbst auf den Rechenweg zu kommen.

## Zwei Repos: öffentlich + privat

Dieses Repo (`Lernhelfer`) ist **öffentlich** und enthält NUR selbst
geschriebene Inhalte. Das urheberrechtlich geschützte Vorlesungsmaterial
(Skripte, eingescannte Übungsblätter) liegt im privaten Repo
`Lernhelfer-Material` und gehört NIEMALS hierher:

- **`Lernhelfer`** (dieses, öffentlich) — `aufgaben/`, `tex/`, `werkzeuge/`,
  `out/`, `docs/`.
- **`Lernhelfer-Material`** (privat) — `eingang/<fach>/` (neue Blätter+Skripte
  aus adam-sync) und `skript/<fach>/` (geschützte Skript-PDFs).

Die Git-Historie ist bereits sauber geschrieben (kein Material drin); diesen
Zustand bewahren. Niemals Skript- oder Blatt-PDFs einchecken. Details zum
Material-Fluss: [docs/adam-sync.md](docs/adam-sync.md).

## Struktur

```text
aufgaben/<fach>/<blattNN>/NN-slug/   je Aufgabe: theorie.tex + loesung.tex
aufgaben/archiv/          aufbewahrte Beispiele, werden nicht mitgebaut
tex/                      geteiltes Layout + Hauptdatei
werkzeuge/                build.py, neue_aufgabe.py, chemie.py, skript_uebernehmen.py
out/<fach>/<blattNN>-lernhelfer.pdf  gebaute Lernhelfer (Theorie + Lösung)
generated/                vom Build erzeugt, nicht bearbeiten/einchecken
```

Ein **Übungsblatt** = ein `blattNN`-Ordner in einem Fach. Ein **Lernhelfer** =
das gebaute PDF `out/<fach>/<blattNN>-lernhelfer.pdf`, das beide Teile in einem
Dokument vereint: erst die Theorie je Aufgabe, dann die durchgerechneten
Lösungen. Es gibt **keine** separate Theorie-PDF — pro Fach und Blatt wird
genau EIN Lernhelfer gebaut.

## Aufbau je Aufgabe

Jede Aufgabe liegt als LaTeX-Ordner `aufgaben/<fach>/<blattNN>/NN-slug/` mit
zwei getrennten Dateien:

- **Teil I — Theorie** (`theorie.tex`). Erkläre verständlich und präzise nur
  die Begriffe, Sätze, Definitionen, allgemeinen Gleichungen,
  Gültigkeitsbedingungen und typischen Fehler, die die Aufgabe braucht. Verweis
  auf die Fundstelle im Skript. **Keine aufgabenspezifischen Zahlen, keine
  rechenbare Schrittfolge, kein Ergebnis** — der Ansatz bleibt eigene
  Denkarbeit. **Knapp halten**; Über-erklären zerstört den Zweck.
- **Teil II — Lösung** (`loesung.tex`). Gegeben/Gesucht, begründeter Ansatz,
  nachvollziehbare Rechnung, Ergebnis und passende Prüfung. Erkläre den
  entscheidenden Gedankenschritt und, wo sinnvoll, was auf ähnliche Aufgaben
  übertragbar ist. Nicht unnötig ausschweifen.

Prüfe die Trennung inhaltlich, nicht nur anhand der Dateinamen
(Details: [docs/arbeitsweise.md](docs/arbeitsweise.md)).

## Übungsblätter → Lernhelfer

- **Ein Blatt, ein eigener Lernhelfer.** Keine Aufgaben verschiedener Blätter
  oder Fächer mischen, ausser der Nutzer verlangt ausdrücklich eine Sammlung.
- Bearbeite grundsätzlich alle Aufgaben und Teilaufgaben eines Blatts.
- Kennzeichne jede Aufgabe durch **Fach, Blatt und Aufgabennummer**, z. B.
  `Physik Blatt 7, A1` (Metadaten `% titel:` in `theorie.tex`).
- Verlinke Ergebnisse und Bearbeitungsstand in `out/` und im README.
- Vor dem Bauen prüfen, dass nur Aufgaben des gewünschten Fach/Blatts
  aufgenommen werden; danach das PDF auf Vollständigkeit prüfen.

## Wöchentlicher Ablauf (Kernaufgabe)

Der Nutzer holt wöchentlich neue Unterlagen per adam-sync ins private
Material-Repo; der Agent übernimmt Einordnung und Build:

1. **Eingang sichten.** Im privaten Material-Repo (`eingang/<fach>/`) den
   neuen Aufgabentext und ggf. das Skript lesen. Fach zuordnen (physik, mathe,
   chemie). `eingang.py einordnen --public ../Lernhelfer` zieht Skripte nach
   `skript/<fach>/` und legt Scaffold-Ordner unter
   `aufgaben/<fach>/blattNN/` an.
2. **Ausfüllen.** Je Aufgabe einen Ordner `NN-slug/` mit `theorie.tex` und
   `loesung.tex` anlegen (oder `neue_aufgabe.py <fach> <blatt> <nummer>
   "Titel"`). Für jede Aufgabe Theorie (Teil I, knapp, lösungsfrei) und Lösung
   (Teil II) schreiben. Konkrete Zahlen und die Aufgabenstellung nur aus der
   tatsächlichen PDF übernehmen — nichts erfinden.
3. **Bauen.** `python3 werkzeuge/build.py` im Repo-Wurzelverzeichnis (baut
   alle Fächer+Blätter) bzw. `--fach <fach>`. Ergebnis:
   `out/<fach>/<blattNN>-lernhelfer.pdf`.
4. **Prüfen.** Jede Datei beim Build automatisch prüfen; Theorie lösungsfrei
   lassen; Inhalte aus dem Skript verifizieren (siehe Qualität).
5. **Commit + Push.** Skripte/Blätter bleiben im privaten Repo.

**Ein Lernhelfer pro Fach und Woche:** pro Fach genau einer (physik, mathe,
chemie), jeder mit zwei Teilen. Ein Fach ohne Blatt diese Woche bleibt aussen
vor.

## Chemie

Vollständig eingerichtet (`fach_titel` im Build, `aufgaben/chemie/`,
`skript/chemie/`). Die ersten Blätter kommen, sobald ein Chemie-Blatt über
adam-sync eintrifft. Für Chemie-Figuren (Molekülstrukturen,
Energie-/Orbital-/Symmetrie-Diagramme) `werkzeuge/chemie.py`:

```bash
# braucht rdkit + matplotlib (z. B. /opt/data/scienv/bin/python)
python3 werkzeuge/chemie.py mol --smiles 'CCO' --out aufgaben/chemie/blatt01/01-x/figures/ethanol.png
python3 werkzeuge/chemie.py energie --zustände 0,3,1.5 --out .../figures/energie.png
python3 werkzeuge/chemie.py orbital --typ p --achse x --out .../figures/orb.png
python3 werkzeuge/chemie.py symmetrie --punkte C2,H,H --out .../figures/sym.png
```

PNGs einbinden mit `\includegraphics{...}` (graphicx ist geladen); Pfade
relativ zur Repo-Wurzel (tectonic-Auflösung) angeben. `--dpi N` zum Nachschärfen.

## Kommunikation mit dem Nutzer

- Nachrichten kommen per Chat (z. B. Telegram). **Kein laufender Kommentar** —
  arbeiten, erst melden, wenn etwas fertig ist oder ein echter Blocker auftritt.
- Kein Fortschritts-Ticker und keine Bestätigung jedes Zwischenschritts.
- Bei mehrdeutiger Aufgabe auf den vernünftigen Standard zurückgreifen (das
  Fach/Blatt, das wirklich vorhanden ist) und die Annahme einmal in der
  Abschlussmeldung nennen. Nur bei echten Blockern (fehlende Angaben,
  unlesbares PDF, fehlende Rechte) nachfragen.
- **ADAM/ILIAS-Links** stehen hinter Login: nicht zu scrapen versuchen, nicht
  nach Passwort im Chat fragen, Inhalte nie erfinden. Bei
  `SESSION_EXPIRED` (siehe docs/adam-sync.md) den Nutzer zum einmaligen
  Cookie-Export auffordern.

## Paralleles Arbeiten (Standard: Issue + Worktree + Merge)

Für parallele (Agenten-)Aufträge gilt ein fester Ablauf, damit kein zweiter
Lauf auf die vom ersten veränderten Dateien stösst (geteilte `generated/`,
`_bm.tex`): **ein Auftrag → eine Issue → ein Worktree → ein Merge (+ ein
Commit).**

- **Issue anlegen** pro Auftrag in GitHub (Titel, Fach/Blatt, Akzeptanz),
  guter Name z. B. `physik/blatt10`, `docs/upgrade` — eindeutig und
  nachvollziehbar.
- **Separates Worktree** für jede Issue: `git worktree add ../<name> -b
  issue/<name>`. Dort arbeitet der Agent ausschliesslich — nie im Haupt-Checkout
  und nie parallel in mehreren Worktrees, die dieselben Dateien berühren.
- **Merge** zurück zu `main` (PR oder `git merge issue/<name> --no-ff`),
  danach Worktree entfernen (`git worktree remove`) und Branch löschen.
- **Commit + Push je Auftrag getrennt**: ein fertiger Auftrag wird sofort
  committet und gepusht (eigener, klar benannter Commit), nicht angesammelt.
- **Rechenprotokoll**: jeder Worktree-Agent verifiziert seine Zahlen selbst
  (python) und nennt die geprüften Ergebnisse in seiner Abschlussmeldung; der
  Orchestrator prüft stichprobenartig nach.

Hintergrund (Warum): mehrere Subagents, die `build.py` auf demselben Checkout
laufen lassen, überschreiben sich gegenseitig `generated/` und `_bm.tex` —
isolierte Worktrees verhindern das (siehe docs/adam-sync.md, Abschnitt
„Warum getrennte Arbeit“).


## Quellen und fachliche Qualität

- Aktuelles Skript des Fachs (privat, `Lernhelfer-Material/skript/<fach>/`)
  und den vollständigen Aufgabentext als massgebliche Quellen nutzen. Kapitel
  und Seiten nennen, soweit sicher bekannt.
- Nichts erfinden: keine Aufgaben, Werte, Sätze, Abbildungen oder Fundstellen.
  Ergänzende Annahmen als solche kennzeichnen. Bei fehlenden Daten oder
  mehrdeutiger Aufgabenstellung nachfragen oder die Unsicherheit festhalten —
  keine scheinbar vollständige Lösung ausgeben.
- Aus PDF extrahierte Formeln, Abbildungen und Nummerierung am Original
  prüfen. Sorgfältig rechnen: Vorzeichen, Einheiten, Gültigkeitsbedingungen,
  möglichst Grenzfälle oder Gegenbeispiele.

## Werkzeuge

- **Build:** `python3 werkzeuge/build.py [--fach <fach>] [--offen] [--kein-pdf]`
  — baut alle (oder je Fach) Lernhelfer nach `out/` (`--kein-pdf` schreibt nur
  `generated/`). Fehlt `pdflatex`, nutzt der Build `tectonic`.
- **Neue Aufgabe:** `neue_aufgabe.py <fach> <blatt> <nummer> "Titel"` erzeugt
  Platzhalter, keine fertige Bearbeitung. Entwürfe vor dem PDF kontrollieren.
- **Chemie-Figuren:** `chemie.py …` (siehe Abschnitt Chemie).
- **Einordnung (im privaten Repo):** `eingang.py sichten/einordnen
  --public <PFAD>`. Flake-Automation: `lernhelfer-sync` in `flake-environments`.

## Sprache, Sicherheit und Abschluss

- Deutsch, verständlich, knapp, fachlich genau. Keine Emojis, keine KI- oder
  Werkzeug-Bylines im Dokument oder in Commits.
- Grössen mit `siunitx` (`\qty{}{}`); dimensionslose Zahlen und rein
  symbolische Gleichungen brauchen keine erfundene Einheit.
- **Vor dem Teilen** von Vorlesungsunterlagen Nutzungsrechte und Privatsphäre
  beachten. Keine Zugangsdaten einchecken, nichts Geschütztes ins öffentliche
  Repo (auch nicht in die Git-Historie).
- **Abschluss:** fachliche Aussagen und Aufgabenabdeckung prüfen, den passenden
  Build ausführen und betroffene PDF-Seiten ansehen. Ein erfolgreicher
  LaTeX-Build ersetzt keine inhaltliche Prüfung. Bestehende Änderungen
  respektieren; sachliche Commits ohne Co-Author-Signatur.
