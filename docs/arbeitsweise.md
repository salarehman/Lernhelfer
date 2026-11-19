# Arbeitsweise

Kurzform der Regeln steht in `AGENTS.md`; hier steht das Warum und die Details.
Hinweis: Das Gerüst und diese Arbeitsweise sind noch in Entwicklung. Bei
Widersprüchen gelten `AGENTS.md` und der Build-Aufruf
`python3 werkzeuge/build.py [--fach <fach>] [--offen] [--kein-pdf]`, der je
Fach+Blatt genau **eine** Datei erzeugt:
`out/<fach>/<blattNN>-lernhelfer.pdf` (keine separate Theorie-Variante).

## Der Zweck

Aus dem Vorlesungsskript wird ein Dokument gebaut, das zwei verschiedene
Bedürfnisse bedient:

1. Nachschlagen, wenn eine Aufgabe ansteht: welche Werkzeuge braucht dieses
   Thema überhaupt, und in welcher Form stehen sie im Skript?
2. Nachvollziehen, wenn eine Aufgabe nicht aufgeht: wie kommt man auf den
   Ansatz, und wo war der eigene Denkfehler?

Teil I darf die Aufgabe nicht lösen. Wer nur Teil I liest, soll die Aufgabe
noch selbst anpacken müssen. Deshalb: keine Zahlen aus der Aufgabe, keine
Schrittfolge, kein Ergebnis, keine Formel, die schon die konkrete Aufgabe
einsetzt.

## Teil I: Theorie je Aufgabe

Aufbau, in dieser Reihenfolge, nur die Punkte, die die Aufgabe wirklich braucht:

1. **Worum es geht.** Ein oder zwei Sätze: welche Situation, welche Frage.
2. **Werkzeuge.** Die Gesetze und Gleichungen in allgemeiner Form, mit den
   Gültigkeitsgrenzen („nur für kleine Auslenkungen“, „nur im Vakuum“).
   Herkunft nennen, wenn sie im Skript hergeleitet werden (Kapitel/Abschnitt).
3. **Vorgehen in allgemeiner Form.** Welche Größen sind gegeben, welche
   gesucht, welche Beziehung verbindet sie. Als Landkarte, nicht als Rezept.
4. **Einheiten und Plausibilität.** Erwartete Einheit des Ergebnisses,
   typische Größenordnung, Grenzfälle, an denen man die Formel testen kann.
5. **Typische Fallen.** Vorzeichen, Bezugssystem, Winkel vs. Bogenmaß,
   Masse vs. Gewichtskraft, gerundete Zwischenergebnisse.

Länge: eine gute halbe bis eine Seite pro Aufgabe. Wird es deutlich mehr,
gehört ein Teil davon in eine Grundlagen-Sektion oder ist zu weit vom Thema weg.

## Teil II: Lösung je Aufgabe

- **Gegeben / Gesucht** zuerst, mit Einheiten und mit dem benutzten Bezugssystem.
- **Ansatz** mit einem Satz Begründung, warum dieser Weg: welches Gesetz,
  welche Symmetrie, welche Erhaltungsgröße.
- **Rechnung** in Zeilen, die man nachvollziehen kann. Symbolisch bis zum
  Schluss, Zahlen erst im letzten Schritt.
- **Kontrolle**: Einheit, Grenzfall oder Plausibilität der Zahl. Wenn eine
  Kontrolle nicht möglich ist, das sagen statt eine zu erfinden.
- **Merksatz**: was man aus dieser Aufgabe auf andere übertragen kann.

Zahlen mit `siunitx`, signifikante Stellen so, wie es die gegebenen Werte
zulassen. Zwischenergebnisse nicht runden, erst das Endergebnis.

## Woher das Material kommt (adam-sync)

Neue Übungsblätter und Skripte kommen automatisiert über **adam-sync** aus
Uni Basel ADAM in das private Repo `Lernhelfer-Material` (`eingang/<fach>/`)
und werden von dort über `eingang.py einordnen` einsortiert. Die genaue
Beschreibung des Ingest, der Cookie-Ablage und des täglichen 02:00-Timers
(inkl. `SESSION_EXPIRED`-Meldung) steht in
[docs/adam-sync.md](adam-sync.md). Wichtig: Blätter und Skripte sind
geschütztes Material und bleiben im privaten Repo — nie ins öffentliche
`Lernhelfer` kopieren.

## Versionen des Skripts

Neue Skript-Versionen sollen alles aus der alten Version und zusätzlichen
Stoff enthalten. Das wird anhand der Quellen geprüft:

- Eine neue Version wird manuell mit der vorherigen verglichen. Alte Dateien
  bleiben erhalten, bis ihr Verbleib bewusst geklärt ist. Der Import entfernt
  sie nicht automatisch.
- `skript/<fach>/aktuell.md` nennt Version, Datum und eine gekürzte Prüfsumme
  der aktuellen Datei je Fach. Das Importwerkzeug schreibt diese Datei.
- Das Werkzeug meldet anhand erkannter Nummern, welche Aufgaben neu sind oder
  scheinbar fehlen. Erkennung, Änderungen und mögliche Umnummerierungen müssen
  mit dem Original geprüft werden. Ordner werden nicht automatisch verschoben.
- Erkannte Aufgaben ohne passenden Ordner erscheinen in
  `skript/<fach>/offen.md`. Ein Ordner beweist jedoch nicht, dass Theorie oder
  Lösung fertig sind.

## Qualitätskontrolle vor dem Commit

1. `python3 werkzeuge/build.py --offen` zeigt Lücken und offene Aufgaben.
2. `python3 werkzeuge/build.py` läuft ohne Fehler und ohne neue Warnungen
   (Overfull-Boxen sind erlaubt, aber auffällige Stellen nachsehen).
3. Die betroffenen Seiten im PDF wirklich ansehen: Formelbild, Einheiten,
   Verweise, Seitenumbruch.
4. Gegengelesen: würde Teil I die Aufgabe verraten? Fehlt in Teil II eine
   Begründung? Ist jede Zahl mit Einheit?
