# Übungsaufgaben-Lernhelfer

Werkzeug fürs Uni-Studium (Physik, Mathematik, Chemie): Es baut aus den
wöchentlichen Übungsblättern sog. **Lernhelfer-PDFs** — eine pro Fach, pro
Blatt, mit zwei Teilen.

Der Clou: Die **Theorie sagt dir nicht die Lösung vorweg**. Sie steht vorher
knapp und verständlich da (Formeln, Bedingungen, typische Fehler), damit du
selbst auf den Rechenweg kommst. Erst der zweite Teil zeigt die durchgerechnete
Lösung. So lernt man beim Nachschlagen, ohne dass einem die Lösung die Arbeit
abnimmt. Die Theorie ist bewusst „lösungsfrei“ gehalten.

> **Urheberrecht-Linie:** Dieses Repo enthält **nur selbst geschriebene**
> Inhalte (die Lernhelfer). Die Vorlesungsskripte und die eingescannten
> Übungsblätter sind geschütztes Material und liegen **nicht** hier, sondern im
> privaten Repo `Lernhelfer-Material` (siehe unten). Aus demselben Grund ist
> die Git-Historie frei von diesen Dateien.

## Die beiden Repos

| Repo | Sichtbarkeit | Inhalt |
|------|--------------|--------|
| `Lernhelfer` (dieses) | öffentlich | `aufgaben/`, `tex/`, `werkzeuge/`, `out/` |
| `Lernhelfer-Material` | privat | `eingang/<fach>/` (neue Blätter+Skripte aus adam-sync), `skript/<fach>/` (geschützte Skripte) |

Der Build braucht kein Material: fehlt `skript/<fach>/aktuell.md`, steht auf
dem Titel nur „Skript noch nicht hinterlegt“. Für die volle Skript-Angabe wird
das Material-Repo lokal neben dieses gelegt (z. B. als Schwester-Ordner).

## So sieht es aus

```text
aufgaben/<fach>/<blattNN>/NN-slug/
                                je Aufgabe ein Ordner mit theorie.tex + loesung.tex
                                z. B. aufgaben/physik/blatt07/01-maxwell-rad/
aufgaben/chemie/                Chemie (eingerichtet, Blätter sobald vorhanden)
werkzeuge/                      build.py, neue_aufgabe.py, chemie.py (Figuren)
skript/<fach>/aktuell.md        nur Metadaten (Version/Prüfsumme); PDFs privat
out/                            gebaute Lernhelfer (nur -lernhelfer.pdf)
```

Gebaute PDFs liegen unter `out/`, z. B.:

- `out/physik/blatt07-lernhelfer.pdf` — Physik Blatt 7, **Theorie + Lösung**

Jeder Lernhelfer enthält beide Teile in einem Dokument: zuerst die Theorie je
Aufgabe, dann die durchgerechneten Lösungen. Es gibt keine separate
Theorie-PDF mehr (eine Datei reicht).

## Fächer

- **Physik** — Mechanik/Fluide (what heute da ist; blatt07–09)
- **Mathematik** — Differenzial-/Integralrechnung (blatt07, 09)
- **Chemie** — Scaffold ist eingebaut (fach_titel + `aufgaben/chemie/` +
  Figuren-Werkzeug), die ersten Blätter kommen sobald ein Chemie-Blatt über
  adam-sync eintrifft. Chemie-Figuren (Molekülstrukturen, Energie-/Orbital-/
  Symmetrie-Diagramme) erzeugt `werkzeuge/chemie.py` (braucht `rdkit` +
  `matplotlib`).

## Die wöchentliche Routine

1. `adam-sync sync` zieht neue Dateien aus ADAM in das private
   Material-Repo (`eingang/<fach>/`). Einmalig anmelden (Cookie-Login).
2. `eingang.py einordnen --public ../Lernhelfer` sortiert: Skripte →
   `skript/<fach>/`, Blätter → Scaffold-Ordner hier in `aufgaben/<fach>/blattNN/`.
3. Ein (Agent-)Helfer schreibt für jede Aufgabe eine knappe lösungsfreie
   Theorie und eine durchgerechnete Lösung.
4. `python3 werkzeuge/build.py` baut die Lernhelfer nach `out/`.
5. Fertig: die PDFs sind da, die Quellen liegen sauber im Git.

Das Ganze lässt sich als Nix-Flake automatisieren: siehe
`lernhelfer-sync` im Repo `flake-environments` (adam-sync → einordnen → build,
mit NixOS-Timer-Option).

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
Arbeit. Sie beschreibt Ordnerstruktur, die wöchentliche Routine (ein Lernhelfer
pro Fach und Blatt, Theorie + Lösung), die lösungsfreie Theorie und wie man mit
dem Nutzer kommuniziert ([docs/arbeitsweise.md](docs/arbeitsweise.md) enthält
die Details).

> Hinweis: Skripte und Übungsblätter gehören ins private Repo
> `Lernhelfer-Material` und dürfen nicht hierher oder in öffentliche
> Git-Historie gelangen.
