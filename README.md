# Physik-Übungen

Dieses private Repository unterstützt beim Bearbeiten von Physikaufgaben aus der
Universität. Aus dem Vorlesungsskript und den Aufgaben entsteht ein LaTeX-PDF
mit zwei getrennten Teilen:

1. **Theorie:** Für jede Aufgabe die relevanten Begriffe, Gesetze, Gleichungen,
   Voraussetzungen, Einheiten und typischen Fehler verständlich und knapp
   erklären. Die Theorie soll das Suchen im Skript ersetzen, aber weder den
   konkreten Lösungsweg noch das Ergebnis verraten. Der Ansatz bleibt eigene
   Denkarbeit.
2. **Lösungen:** Für jede Aufgabe einen nachvollziehbaren Lösungsweg mit
   Begründung, Rechnung und Prüfung zeigen. Erklären, warum der Ansatz passt und
   was sich auf andere Aufgaben übertragen lässt, statt nur ein Ergebnis zu
   präsentieren.

Ziel ist, möglichst viel zu lernen, ohne die kreative Arbeit beim Lösen
abzunehmen. Die Theorie ist auf die jeweilige Aufgabe zugeschnitten, aber die
Formeln und Erklärungen bleiben allgemein.

## Stand

Das Repository ist ein **Gerüst**, noch keine fertige Aufgabensammlung. Ein
künstliches Federpendel-Beispiel demonstriert den Aufbau; es stammt nicht aus
dem Vorlesungsskript und ist kein Qualitätsmaßstab für echte Aufgaben. Es liegt
noch kein Vorlesungsskript vor. Die Werkzeuge sind ein erster Prototyp: Ihre
Ausgaben und das PDF müssen insbesondere bei echten Unterlagen geprüft werden.

## Welche Unterlagen werden benötigt?

- Das aktuelle vollständige Vorlesungsskript, vorzugsweise als durchsuchbares
  PDF. Bei gescannten Seiten zusätzlich eine lesbare OCR-Fassung, falls
  vorhanden; Formeln und Abbildungen müssen am Original geprüft werden.
- Die Übungsaufgaben oder Übungsblätter, falls sie nicht vollständig im Skript
  enthalten sind. Nummern, Aufgabentexte, Abbildungen und alle gegebenen Werte
  müssen lesbar sein.
- Den aktuellen Vorlesungs- oder Bearbeitungsstand und welche Aufgaben als
  Nächstes bearbeitet werden sollen. Falls es Vorgaben zu Notation, zulässigen
  Hilfsmitteln oder Musterlösungen gibt, diese ebenfalls mitteilen.

Die Dateien können in das private GitHub-Repository hochgeladen werden, zum
Beispiel das Skript unter `skript/` und Aufgabenblätter unter einem neu
angelegten Ordner `eingang/`. Danach den Dateipfad und den gewünschten Auftrag
im Chat nennen. Alternativ kann ein absoluter Pfad zu einer Datei genannt werden,
auf die die Arbeitsumgebung tatsächlich Zugriff hat. Ein Pfad auf dem eigenen
Rechner ist nicht automatisch in der Arbeitsumgebung sichtbar.

Nur Unterlagen hochladen, deren Speicherung dort zulässig ist. Das Repository
ist privat, aber keine Garantie gegen Weitergabe oder Zugriffe durch Berechtigte.
Keine Zugangsdaten oder personenbezogenen Daten unnötig einchecken.

## Arbeitsablauf

1. Skript und Aufgaben entgegennehmen, Lesbarkeit, Version und Fundstellen
   prüfen. Fehlende oder unklare Angaben nicht erfinden.
2. Neue Skriptversionen sollen alles bisherige Material und zusätzlichen Stoff
   enthalten. Mit der vorherigen Version vergleichen, auch Änderungen an
   bestehenden Aufgaben prüfen. Eine scheinbar fehlende Aufgabe erst manuell
   überprüfen. Nichts aufgrund einer unsicheren Erkennung löschen.
3. Für jede zu bearbeitende Aufgabe die notwendige Theorie mit Fundstellen
   zusammenstellen und eine getrennte, begründete Lösung erstellen.
4. Den Inhalt fachlich prüfen, das PDF bauen und die betroffenen Seiten auf
   Lesbarkeit, Formeln, Umbrüche und Trennung zwischen Theorie und Lösung prüfen.

Die ausführlichen Regeln für die Arbeit im Repository stehen in [AGENTS.md](AGENTS.md),
weitere Hinweise in [docs/arbeitsweise.md](docs/arbeitsweise.md).

## Dateien

```text
skript/             Vorlesungsskript und gegebenenfalls erzeugter Index/Text
aufgaben/           ein Ordner je Aufgabe mit theorie.tex und loesung.tex
  00-beispiel/      künstliches Beispiel, keine echte Vorlesungsaufgabe
tex/                LaTeX-Hauptdatei und Layout
werkzeuge/          Prototypen für Build, Aufgabengerüst und Skriptübernahme
werkzeuge/vorlagen/  Vorlagen für neue Aufgaben
out/                gebaute PDFs
generated/          vom Build erzeugte Dateien, nicht bearbeiten oder einchecken
```

## Bauen und Aufgaben anlegen

Voraussetzungen sind Python 3, `pdflatex` mit den verwendeten LaTeX-Paketen und
für die Textextraktion `pdftotext` aus `poppler-utils`. Zum Beispiel auf Ubuntu:

```bash
sudo apt-get install texlive-latex-base texlive-latex-recommended \
  texlive-latex-extra texlive-lang-german texlive-science texlive-pictures \
  texlive-fonts-recommended lmodern poppler-utils
```

Im Repository ausführen:

```bash
python3 werkzeuge/build.py                 # out/physik-uebungen.pdf
python3 werkzeuge/build.py --nur-theorie    # out/physik-theorie.pdf
python3 werkzeuge/build.py --nur-loesungen  # out/physik-loesungen.pdf
python3 werkzeuge/build.py --offen          # Index und Ordner vergleichen
./bau.sh                                    # Abkürzung für den Gesamt-Build
```

Der Build kompiliert `tex/main.tex` zweimal. Neue Aufgaben können mit folgendem
Befehl vorbereitet werden:

```bash
python3 werkzeuge/neue_aufgabe.py 3 "Schiefer Wurf" --skript "Kap. 3, S. 14"
```

Die erzeugten Dateien sind Platzhalter und müssen inhaltlich ausgefüllt werden.
Der Build berücksichtigt vorhandene Dateien auch dann, wenn sie noch
Platzhalter enthalten. Deshalb Entwürfe vor einem fertigen PDF kontrollieren.

## Skriptübernahme: Grenzen des Prototyps

```bash
python3 werkzeuge/skript_uebernehmen.py /pfad/zum/skript.pdf --datum 2026-11-09
```

Das Werkzeug kopiert die Eingabe nach `skript/`, extrahiert bei PDFs Text mit
`pdftotext` und schreibt `skript/aktuell.md`, `skript/aufgaben.md` und
`skript/offen.md`. Es erkennt nur bestimmte Zeilenformen wie `Aufgabe 3` und
errät Titel und Fundstellen. Unterschiedliche Nummerierung, schlechte
Texterkennung, Abbildungen und Formeln können zu falschen oder fehlenden
Einträgen führen; der Vergleich ist kein Nachweis, dass eine Version vollständig
ist oder dass Aufgaben unverändert sind. Den Index mit dem Original abgleichen.

Der Import überschreibt bei gleichem Datum vorhandene Dateien und ersetzt den
Index. Ältere Skriptdateien und Textauszüge werden nicht automatisch entfernt;
fehlende Aufgabenordner werden nicht automatisch archiviert. Vor einem Import
bestehende Daten sichern und Änderungen prüfen. `--offen` vergleicht nur
Nummern im Index mit Ordnernamen; es prüft weder die Erkennung noch, ob Theorie
und Lösung fachlich fertig sind. Ein grüner Build beweist keine fachliche
Richtigkeit.
