# Übungsaufgaben-Lernhelfer

Kleines Werkzeug fürs Physik- und Mathe-Studium: Es sammelt die wöchentlichen
Übungsblätter und baut daraus sog. **Lernhelfer-PDFs** — eine pro Fach, pro
Woche, jeweils mit zwei Teilen.

Der Clou: Die **Theorie sagt dir nicht die Lösung vorweg**. Sie steht vorher
knapp und verständlich da (Formeln, Bedingungen, typische Fehler), damit du
selbst auf den Rechenweg kommst. Erst der zweite Teil zeigt die durchgerechnete
Lösung. So lernt man beim Nachschlagen, ohne dass einem die Lösung die Arbeit
abnimmt. Die Theorie ist bewusst „lösungsfrei“ gehalten.

Alles liegt in **einem** Repo, nach Fach und Blatt sortiert — man findet jede
Aufgabe und jede gebaute PDF schnell wieder.

## So sieht es aus

```text
eingang/                       "Dropschublade": neue Blätter + Skripte hier rein
aufgaben/<fach>/<blattNN>/NN-slug/
                                je Aufgabe ein Ordner mit theorie.tex + loesung.tex
                                z. B. aufgaben/physik/blatt07/01-maxwell-rad/
skript/<fach>/                 Vorlesungsskript + aktuell.md (Fassung, Prüfsumme)
out/                           gebaute Lernhelfer
docs/, tex/, werkzeuge/        Regeln, Layout, Build-Werkzeuge
```

Gebaute PDFs liegen unter `out/` und heißen z. B.:

- `out/physik/blatt07-lernhelfer.pdf` — Physik Blatt 7, **Theorie + Lösung**
- `out/physik/blatt07-theorie.pdf` — Physik Blatt 7, nur **Theorie**

## Die wöchentliche Routine

1. Neues Übungsblatt (und ggf. neues Skript) in `eingang/` legen.
2. Ein (Agent-)Helfer sortiert es nach Fach und Blatt, schreibt für jede
   Aufgabe eine knappe lösungsfreie Theorie und eine durchgerechnete Lösung.
3. Er baut daraus die zwei Lernhelfer je Fach und legt sie in `out/`.
4. Fertig: die PDFs sind da, die Quellen liegen sauber im Git.

## Bauen (für Fortgeschrittene)

Im Repo-Wurzelverzeichnis:

```bash
python3 werkzeuge/build.py               # alle Fächer + Blätter bauen
python3 werkzeuge/build.py --fach physik # nur ein Fach
python3 werkzeuge/build.py --offen       # Überblick, ohne zu bauen
```

Voraussetzungen: Python 3 und `pdflatex`; fehlt `pdflatex`, kompiliert der
Build automatisch mit `tectonic` (Standalone-LaTeX-Engine).

## Regeln für Agenten / neue Mithelfende

Die ausführliche Anleitung steht in [AGENTS.md](AGENTS.md) — lese sie vor der
Arbeit. Sie beschreibt Ordnerstruktur, die wöchentliche Routine (zwei
Lernhelfer pro Woche: Physik + Mathe, je Theorie + Lösung), die lösungsfreie
Theorie und wie man mit dem Nutzer kommuniziert ([docs/arbeitsweise.md](docs/arbeitsweise.md)
enthält die Details).

> Hinweis: Vorlesungsunterlagen nicht weitergeben, wenn die Rechte dazu fehlen.
> Das Repo ist privat — aber Privatheit ist keine Garantie gegen Weitergabe.
