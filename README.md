# Übungsaufgaben-Lernhelfer

Werkzeug fürs Uni-Studium (Physik, Mathematik, Chemie): Es baut aus den
wöchentlichen Übungsblättern sog. **Lernhelfer-PDFs** — eine pro Fach und
Blatt, in zwei Teilen.

Der Clou: Die **Theorie verrät die Lösung nicht vorweg**. Sie steht vorher
knapp und verständlich da (Formeln, Bedingungen, typische Fehler), damit du
selbst auf den Rechenweg kommst. Erst der zweite Teil zeigt die
durchgerechnete Lösung. So lernt man beim Nachschlagen, ohne dass einem die
Lösung die Arbeit abnimmt.

> **Urheberrecht-Linie:** Dieses Repo enthält **nur selbst geschriebene**
> Inhalte. Die Vorlesungsskripte und die eingescannten Übungsblätter sind
> geschütztes Material und liegen **nicht** hier, sondern im privaten Repo
> `Lernhelfer-Material`. Aus demselben Grund ist die Git-Historie frei von
> diesen Dateien.

## Zweck & Projekt-Überblick

Zwei Repos arbeiten zusammen; der Build selbst braucht kein Material.

| Repo | Sichtbarkeit | Inhalt |
|------|--------------|--------|
| `Lernhelfer` (dieses) | öffentlich | selbst geschriebene Lernhelfer: `aufgaben/`, `tex/`, `werkzeuge/`, `out/`, `docs/` |
| `Lernhelfer-Material` | privat | `eingang/<fach>/` (neue Blätter+Skripte aus adam-sync), `skript/<fach>/` (geschützte Skripte) |

Fehlt `skript/<fach>/aktuell.md`, steht auf dem Titel nur „Skript noch nicht
hinterlegt“. Für die volle Skript-Angabe liegt das Material-Repo lokal neben
diesem (z. B. als Schwester-Ordner `../Lernhelfer-Material`).

## Struktur

```text
aufgaben/<fach>/<blattNN>/NN-slug/   je Aufgabe: theorie.tex + loesung.tex
aufgaben/chemie/                     Chemie (eingerichtet, Blätter sobald vorhanden)
werkzeuge/                           build.py, neue_aufgabe.py, chemie.py
out/<fach>/<blattNN>-lernhelfer.pdf  gebaute Lernhelfer (eine Datei je Blatt)
docs/adam-sync.md                    Woher die Blätter kommen (Referenz)
AGENTS.md                            Regeln für Menschen & Agenten
docs/arbeitsweise.md                 Das Warum hinter Theorie/Lösung
```

Ein **Lernhelfer** vereint beide Teile in **einem** Dokument: erst die Theorie
je Aufgabe, dann die durchgerechneten Lösungen. Es gibt keine separate
Theorie-PDF (eine Datei reicht). Beispiel: `out/physik/blatt07-lernhelfer.pdf`.

## Fächer

- **Physik** — Mechanik/Fluide (blatt07–09).
- **Mathematik** — Differenzial-/Integralrechnung (blatt07, 09).
- **Chemie** — Scaffold ist eingebaut (`fach_titel` + `aufgaben/chemie/` +
  Figuren-Werkzeug); die ersten Blätter kommen, sobald ein Chemie-Blatt über
  adam-sync eintrifft. Chemie-Figuren erzeugt `werkzeuge/chemie.py`
  (braucht `rdkit` + `matplotlib`, z. B. unter `/opt/data/scienv`).

## Wöchentliche Routine

1. **Ingest (automatisch):** adam-sync zieht neue Dateien aus ADAM ins private
   Material-Repo (`eingang/<fach>/`); ein täglicher 02:00-Timer/probe stößt
   Sync + Einordnung an. Details: [docs/adam-sync.md](docs/adam-sync.md).
2. **Einordnen:** `eingang.py einordnen --public ../Lernhelfer` sortiert
   Skripte → `skript/<fach>/`, Blätter → Scaffold-Ordner hier in
   `aufgaben/<fach>/blattNN/`.
3. **Bearbeiten:** für jede Aufgabe eine knappe lösungsfreie Theorie und
   durchgerechnete Lösung schreiben.
4. **Bauen:** `python3 werkzeuge/build.py` erzeugt die Lernhelfer in `out/`.
5. **Prüfen & Commit:** PDFs sichten; Quellen liegen sauber im Git (Material
   bleibt privat).

Das Ganze lässt sich als Nix-Flake automatisieren (`lernhelfer-sync` und
`adam-sync` in `flake-environments`).

## Bauen (für Fortgeschrittene)

Im Repo-Wurzelverzeichnis:

```bash
python3 werkzeuge/build.py               # alle Fächer + Blätter bauen
python3 werkzeuge/build.py --fach physik # nur ein Fach
python3 werkzeuge/build.py --offen       # Überblick, ohne zu bauen
python3 werkzeuge/build.py --kein-pdf    # nur generated/ schreiben
```

Voraussetzungen: Python 3 und `pdflatex`; fehlt `pdflatex`, kompiliert der
Build automatisch mit `tectonic`.

## Regeln für Agenten / neue Mithelfende

Die ausführliche Anleitung steht in [AGENTS.md](AGENTS.md) — **lies sie vor der
Arbeit**. Sie beschreibt Ordnerstruktur, die wöchentliche Routine (ein
Lernhelfer pro Fach und Blatt, Theorie + Lösung), die lösungsfreie Theorie und
die Kommunikation mit dem Nutzer. [docs/arbeitsweise.md](docs/arbeitsweise.md)
enthält das Warum und die Details.

> Hinweis: Skripte und Übungsblätter gehören ins private Repo
> `Lernhelfer-Material` und dürfen nicht ins öffentliche Repo oder in dessen
> Git-Historie gelangen. Siehe [docs/adam-sync.md](docs/adam-sync.md).
