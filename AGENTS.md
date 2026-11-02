# Arbeitsregeln für dieses Repository

Diese Regeln gelten für Menschen und Agenten. Ziel ist ein Lernwerkzeug für
universitäre Aufgaben aus mehreren Fächern (Physik, Mathematik, …), nicht das
bloße Produzieren von Musterlösungen. Vor Änderungen README.md, diese Datei und
die relevanten Quellen lesen.

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
eingang/                  Ablage für neue Skripte + Aufgabenblätter (Eingang)
aufgaben/<fach>/<blattNN>/NN-slug/   je Aufgabe: theorie.tex + loesung.tex
aufgaben/archiv/          aufbewahrte Beispiele, werden nicht mitgebaut
skript/<fach>/            Vorlesungsskript + aktuell.md (Fassung, Prüfsumme)
tex/                      geteiltes Layout + Hauptdatei
werkzeuge/                Build, Gerüst-Generator, Skriptübernahme
out/                      <fach>-<blattNN>-lernhelfer.pdf und -theorie.pdf
generated/                vom Build erzeugt, nicht bearbeiten/einchecken
```

Ein **Übungsblatt** = ein `blattNN`-Ordner in einem Fach. Ein **Lernhelfer** =
das gebaute PDF `out/<fach>/<blattNN>-lernhelfer.pdf` (Theorie + Lösung); die
Fassung nur mit Theorie heisst `out/<fach>/<blattNN>-theorie.pdf` und ist eine
ergänzende Ansicht, kein Ersatz. Pro Fach und Blatt werden beide gebaut.

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

Der Nutzer legt jede Woche neue Unterlagen in `eingang/` ab (Skript und/oder
Übungsblatt als PDF, pro Fach). Der Agent übernimmt die Sortierung und baut die
Lernhelfer:

1. **Eingang sichten.** In `eingang/` den neuen Aufgabentext und ggf. das neue
   Skript lesen. Fach zuordnen (physik, mathe, …).
2. **Sortieren.** Das Blatt nach `aufgaben/<fach>/blattNN/` legen; je Aufgabe
   einen Ordner `NN-slug/` mit `theorie.tex` und `loesung.tex` anlegen (oder
   `neue_aufgabe.py <fach> <blatt> <nummer> "Titel" --skript "Fundstelle"`).
   Das Skript unter `skript/<fach>/` ablegen und `aktuell.md` mit Fassung,
   Datum und sha256-Prüfsumme versehen.
3. **Ausfüllen.** Für jede Aufgabe Theorie (Teil I, knapp, **lösungsfrei**) und
   Lösung (Teil II) schreiben. Konkrete Zahlen und die Aufgabenstellung nur aus
   der tatsächlichen PDF übernehmen — nichts erfinden.
4. **Bauen.** `python3 werkzeuge/build.py` im Repo-Wurzelverzeichnis (baut
   alle Fächer+Blätter) bzw. `--fach <fach>` für eines. Das Ergebnis liegt in
   `out/<fach>/<blattNN>-lernhelfer.pdf` (Theorie+Lösung) und
   `out/<fach>/<blattNN>-theorie.pdf` (nur Theorie).
5. **Prüfen.** Jede Datei beim Build automatisch prüfen; die Theorie lösungsfrei
   lassen; Inhalte aus dem Skript verifizieren.
6. **Commit + Push** im Git (private Dateien nicht in öffentliche Repos).

**Zwei Lernhelfer pro Woche:** der Nutzer erwartet pro Fach genau einen
Lernhelfer (physik + mathe), jeder mit zwei Teilen. Es sei denn, ein Fach hat
diese Woche kein Blatt — dann bleibt es bei dem Fach mit Blatt.

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
- LMS-Links (z. B. ADAM/ILIAS) sind hinter Login: nicht versuchen zu scrapen.
  Auf Anlage in `eingang/` verweisen; nie nach Passwort im Chat fragen und
  Inhalte nie erfinden.

## Quellen und fachliche Qualität

- Verwende das aktuelle Skript des Fachs (`skript/<fach>/`) und den
  vollständigen Aufgabentext als maßgebliche Quellen. Nenne Kapitel und Seiten,
  soweit sicher bekannt.
- Erfinde keine Aufgaben, Werte, Sätze, Abbildungen oder Fundstellen.
  Kennzeichne ergänzende Annahmen als solche. Bei fehlenden Daten oder
  mehrdeutiger Aufgabenstellung nachfragen oder die Unsicherheit festhalten;
  keine scheinbar vollständige Lösung ausgeben.
- Aus PDF-Text extrahierte Formeln, Abbildungen und Nummerierung anhand des
  Originals prüfen. Rechne sorgfältig, prüfe Vorzeichen, Einheiten,
  Gültigkeitsbedingungen und nach Möglichkeit Grenzfälle oder Gegenbeispiele.

## Werkzeuge

- `python3 werkzeuge/build.py [--fach <fach>] [--offen] [--kein-pdf]` baut alle
  (oder nur die eines Fachs) Lernhelfer nach `out/`. `--offen` zeigt nur den
  Überblick. Fehlt `pdflatex`, kompiliert der Build automatisch mit `tectonic`.
- Neue Aufgabe: `python3 werkzeuge/neue_aufgabe.py <fach> <blatt> <nummer> "Titel"
  --skript "Kap. 3, S. 14"` erzeugt Platzhalter, keine fertige Bearbeitung.
  Entwürfe vor einem fertigen PDF kontrollieren.
- Skriptübernahme: `werkzeuge/skript_uebernehmen.py` (Prototyp) kopiert einen
  Import nach `skript/<fach>/` und schreibt `aktuell.md`. Die Erkennung ist grob
  — Index und Fundstellen manuell gegen das Original prüfen.

## Sprache, Sicherheit und Abschluss

- Dokument und Lerninhalte auf Deutsch; verständlich, knapp, fachlich genau.
  Keine Emojis, keine KI- oder Werkzeug-Bylines im Dokument oder in Commits.
- Größen mit `siunitx` (`\qty{}{}`) ausweisen; dimensionslose Zahlen und rein
  symbolische Gleichungen brauchen keine erfundene Einheit.
- Vor dem Teilen von Vorlesungsunterlagen Nutzungsrechte und Privatsphäre
  beachten. Keine Zugangsdaten einchecken.
- Vor Abschluss fachliche Aussagen und Aufgabenabdeckung prüfen, den passenden
  Build ausführen und betroffene PDF-Seiten ansehen. Ein erfolgreicher LaTeX-Build
  ersetzt keine inhaltliche Prüfung. Bestehende Änderungen respektieren, keine
  Historie umschreiben, sachliche Commits ohne Co-Author-Signatur.
