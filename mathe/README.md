# Mathe-Lernhelfer (Modul im selben Repo)

Der Mathe-Teil lebt unter `mathe/`, getrennt vom Physik-Teil auf der obersten
Ebene, damit beides in einem privat teilbaren Repo bleibt und trotzdem
übersichtlich ist. Ein Übungsblatt → ein Lernhelfer-PDF.

## Aufbau

```text
mathe/
  aufgaben/           ein Ordner je Aufgabe (NN-titel/ mit theorie.tex + loesung.tex)
  tex/                LaTeX-Hauptdatei und Layout
  werkzeuge/          Build-Skript, Gerüst-Generator und Vorlagen
  out/                gebaute Lernhelfer-PDFs
  skript/             Vorlesungsmaterial und aktuelle Fassung
  docs/               Arbeitsweise und Regeln
```

## Bauen

Im Ordner `mathe/` ausführen:

```bash
python3 werkzeuge/build.py                 # out/mathe-uebungen.pdf (Theorie + Lösungen)
python3 werkzeuge/build.py --nur-theorie   # out/mathe-theorie.pdf
./bau.sh
```

Neue Aufgabe anlegen:

```bash
python3 werkzeuge/neue_aufgabe.py 1 "Folgen und Reihen" --skript "Kap. 2, S. 10"
```

Regeln: Theorie verrät nie den Lösungsweg, Teil I und II sind getrennt,
Fundstellen kommen aus dem aktuellen Skript. Siehe `mathe/docs/arbeitsweise.md`.
