# Arbeitsweise

Hinweis: Das Gerüst und diese Arbeitsweise sind noch in Entwicklung. Bei
Widersprüchen gelten `AGENTS.md` und die dort beschriebenen Grenzen der
Werkzeuge. Der Import entfernt keine alten Skriptdateien und archiviert keine
Aufgabenordner automatisch; der Abgleich erkennt keine inhaltlichen Änderungen.

Wie hier gearbeitet wird, damit das PDF beim Lernen wirklich hilft. Die Kurzform
steht in `AGENTS.md`, hier steht das Warum und die Details.

## Der Zweck

Aus dem Vorlesungsskript wird ein Dokument gebaut, das zwei verschiedene
Beduerfnisse bedient:

1. Nachschlagen, wenn eine Aufgabe ansteht: welche Werkzeuge braucht dieses
   Thema ueberhaupt, und in welcher Form stehen sie im Skript?
2. Nachvollziehen, wenn eine Aufgabe nicht aufgeht: wie kommt man auf den
   Ansatz, und wo war der eigene Denkfehler?

Teil I darf die Aufgabe nicht loesen. Wer nur Teil I liest, soll die Aufgabe
noch selbst anpacken muessen. Deshalb: keine Zahlen aus der Aufgabe, keine
Schrittfolge, kein Ergebnis, keine Formel, die schon die konkrete Aufgabe
einsetzt.

## Teil I: Theorie je Aufgabe

Aufbau, in dieser Reihenfolge, nur die Punkte, die die Aufgabe wirklich braucht:

1. **Worum es geht.** Ein oder zwei Saetze: welche Situation, welche Frage.
2. **Werkzeuge.** Die Gesetze und Gleichungen in allgemeiner Form, mit den
   Gueltigkeitsgrenzen ("nur fuer kleine Auslenkungen", "nur im Vakuum").
   Herkunft nennen, wenn sie im Skript hergeleitet werden (Kapitel/Abschnitt).
3. **Vorgehen in allgemeiner Form.** Welche Groessen sind gegeben, welche
   gesucht, welche Beziehung verbindet sie. Als Landkarte, nicht als Rezept.
4. **Einheiten und Plausibilitaet.** Erwartete Einheit des Ergebnisses,
   typische Groessenordnung, Grenzfaelle, an denen man die Formel testen kann.
5. **Typische Fallen.** Vorzeichen, Bezugssystem, Winkel vs. Bogenmass,
   Masse vs. Gewichtskraft, gerundete Zwischenergebnisse.

Laenge: eine gute halbe bis eine Seite pro Aufgabe. Wenn es deutlich mehr wird,
gehoert ein Teil davon in eine Grundlagen-Sektion oder ist zu weit vom Thema weg.

## Teil II: Loesung je Aufgabe

- **Gegeben / Gesucht** zuerst, mit Einheiten und mit dem benutzten Bezugssystem.
- **Ansatz** mit einem Satz Begruendung, warum dieser Weg: welches Gesetz, welche
  Symmetrie, welche Erhaltungsgroesse.
- **Rechnung** in Zeilen, die man nachvollziehen kann. Symbolisch bis zum
  Schluss, Zahlen erst im letzten Schritt.
- **Kontrolle**: Einheit, Grenzfall oder Plausibilitaet der Zahl. Wenn eine
  Kontrolle nicht moeglich ist, das sagen statt eine zu erfinden.
- **Merksatz**: was man aus dieser Aufgabe auf andere uebertragen kann.

Zahlen mit `siunitx`, signifikante Stellen so, wie es die gegebenen Werte
zulassen. Zwischenergebnisse nicht runden, erst das Endergebnis.

## Versionen des Skripts

Neue Skript-Versionen sollen alles aus der alten Version und zusaetzlichen
Stoff enthalten. Das wird anhand der Quellen geprueft:

- Eine neue Version wird manuell mit der vorherigen verglichen. Alte Dateien
  bleiben erhalten, bis ihr Verbleib bewusst geklärt ist. Der Import entfernt
  sie nicht automatisch.
- `skript/aktuell.md` nennt Version, Datum und eine gekürzte Prüfsumme der
  aktuellen Datei. Das Importwerkzeug schreibt diese Datei.
- Das Werkzeug meldet anhand erkannter Nummern, welche Aufgaben neu sind oder
  scheinbar fehlen. Erkennung, Änderungen und mögliche Umnummerierungen müssen
  mit dem Original geprüft werden. Ordner werden nicht automatisch verschoben.
- Erkannte Aufgaben ohne passenden Ordner erscheinen in `skript/offen.md`.
  Ein Ordner beweist jedoch nicht, dass Theorie oder Lösung fertig sind.

## Qualitaetskontrolle vor dem Commit

1. `python3 werkzeuge/build.py --offen` zeigt Luecken und offene Aufgaben.
2. `python3 werkzeuge/build.py` laeuft ohne Fehler und ohne neue Warnungen
   (Overfull-Boxen sind erlaubt, aber auffaellige Stellen nachsehen).
3. Die betroffenen Seiten im PDF wirklich ansehen: Formelbild, Einheiten,
   Verweise, Seitenumbruch.
4. Gegengelesen: wuerde Teil I die Aufgabe verraten? Fehlt in Teil II eine
   Begruendung? Ist jede Zahl mit Einheit?
