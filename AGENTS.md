# Arbeitsregeln für dieses Repository

Diese Regeln gelten für Menschen und Agenten. Ziel ist ein Lernwerkzeug für
universitäre Physikaufgaben, nicht das bloße Produzieren von Musterlösungen.
Vor Änderungen README.md, diese Datei und die relevanten Quellen lesen.

## Ziel und Trennung

Das Lern-PDF hat zwei getrennte Teile, jeweils nach Aufgaben gegliedert:

- **Teil I: Theorie.** Erkläre verständlich und präzise nur die Konzepte,
  Gesetze, allgemeinen Gleichungen, Voraussetzungen, Einheiten und typischen
  Fehler, die für die Aufgabe nützlich sind. Verweise auf die Fundstelle im
  Skript. Die Theorie soll das Suchen erleichtern und Verständnis aufbauen.
  Keine aufgabenspezifischen Zahlen, keine konkrete Reihenfolge der
  Rechenschritte, kein versteckter Lösungsweg und kein Ergebnis. Allgemeine
  Beziehungen dürfen erklärt werden, ohne die konkrete Aufgabe zu lösen.
- **Teil II: Lösung.** Führe nachvollziehbar durch den Lösungsweg: Gegebenes
  und Gesuchtes, begründeter Ansatz, verständliche Rechnung, Ergebnis und
  passende Prüfung. Erläutere den entscheidenden Gedankenschritt und, wo es
  sinnvoll ist, was auf ähnliche Aufgaben übertragbar ist. Nicht unnötig
  ausschweifen und keine entscheidenden Zwischenschritte überspringen.

Prüfe die Trennung inhaltlich, nicht nur anhand der Dateinamen. Besonders bei
ähnlichen Standardaufgaben kann eine allgemeine Formel oder ein Beispiel den
konkreten Ansatz bereits verraten. Ein vorhandenes Beispiel ist kein Beweis,
dass es diese Regeln erfüllt.

## Quellen und fachliche Qualität

- Verwende das aktuelle Vorlesungsskript und den vollständigen Aufgabentext als
  maßgebliche Quellen. Beachte den vom Nutzer genannten Vorlesungsstand und
  dessen Notation und Vorgaben. Nenne Kapitel und Seiten, soweit sicher bekannt.
- Erfinde keine Aufgaben, Werte, Abbildungen, Fundstellen oder Aussagen über
  das Skript. Kennzeichne ergänzende Standardkenntnisse und Annahmen als solche.
  Bei fehlenden Daten, unlesbaren Formeln oder mehrdeutiger Aufgabenstellung
  nachfragen oder die Unsicherheit ausdrücklich festhalten; keine scheinbar
  vollständige Lösung ausgeben.
- Aus PDF-Text extrahierte Formeln, Abbildungen und die Nummerierung anhand des
  Originals prüfen. Eine leere oder fehlerhafte Textextraktion ist kein Beweis,
  dass der Inhalt nicht existiert.
- Rechne sorgfältig, prüfe Vorzeichen, Maßeinheiten, Gültigkeitsbedingungen und
  nach Möglichkeit Grenzfälle oder Größenordnungen. Runde erst am Ende und
  erläutere, wenn eine unabhängige Kontrolle nicht möglich ist.

## Neue Skriptversionen

Der Nutzer erwartet, dass jede neue Version die alte vollständig enthält und
neuen Stoff ergänzt. Das ist eine Erwartung, keine bereits verifizierte
Eigenschaft. Neue und alte Version anhand der Quellen vergleichen, einschließlich
geänderter Aufgaben und möglicher Umnummerierung. Unklare Abweichungen melden,
nicht stillschweigend löschen oder als erledigt markieren. Frühere Materialien
und Bearbeitungen erhalten, bis ihre Herkunft und Wiederherstellbarkeit geklärt
sind. Archivierung erfolgt nur bewusst nach Prüfung, nicht automatisch.

`werkzeuge/skript_uebernehmen.py` ist ein Prototyp: Es kopiert die Datei,
extrahiert Text und erkennt nur bestimmte Nummernmuster. Es ersetzt den Index,
kann Dateien bei gleichem Datum überschreiben und entfernt keine alten
Skriptdateien. Vor der Ausführung Eingabe und vorhandene Dateien prüfen und
bei Bedarf sichern. Den erzeugten Index und die Fundstellen manuell gegen das
Original abgleichen. `--offen` prüft Ordnernummern, nicht fachliche Vollständigkeit.
Eine gleichbleibende Nummer beweist nicht, dass eine Aufgabe unverändert ist.

## Aufbau und Werkzeuge

- Je Aufgabe ein Ordner `aufgaben/NN-titel/` mit `theorie.tex` und
  `loesung.tex`. Metadaten `% titel: ...` und `% skript: ...` stehen in
  `theorie.tex`. Eine Fundstelle nur angeben, wenn sie verifiziert ist.
- `python3 werkzeuge/neue_aufgabe.py NUMMER "Titel" --skript "Fundstelle"`
  erzeugt Platzhalter, keine fertig bearbeitete Aufgabe. Der Build nimmt auch
  Platzhalter auf; vor Veröffentlichung sicherstellen, dass keine enthalten sind.
- `python3 werkzeuge/build.py` baut das vollständige PDF, `--nur-theorie` und
  `--nur-loesungen` bauen getrennte Fassungen. Der Build erzeugt `generated/`
  neu und kompiliert zweimal mit `pdflatex`.
- `python3 werkzeuge/build.py --offen` zeigt den nummernbasierten Abgleich,
  sofern ein Index existiert. Existenz eines Ordners oder zweier Dateien bedeutet
  nicht, dass Inhalt geprüft oder abgeschlossen ist.
- Das Federpendel unter `aufgaben/archiv/00-beispiel/` ist ein künstliches
  Beispiel ohne Skriptbezug und wird nicht mitgebaut. Es nicht als
  Vorlesungsinhalt ausgeben.

## Sprache, Sicherheit und Abschluss

- Dokument und Lerninhalte auf Deutsch; verständlich, knapp und fachlich genau.
  Keine Gedankenstriche als Satztrenner, keine Emojis, keine Signaturen oder
  KI- und Werkzeug-Bylines im Dokument oder in Commits.
- Größen mit Einheiten korrekt ausweisen, LaTeX-Einheiten mit `siunitx`
  setzen, z. B. `\qty{9.81}{\metre\per\second\squared}`. Dimensionslose
  Zahlen und rein symbolische Gleichungen benötigen keine erfundene Einheit.
- Vor dem Teilen von Vorlesungsunterlagen Nutzungsrechte und Privatsphäre
  beachten. Keine Zugangsdaten einchecken. Git-Historie bewahrt auch gelöschte
  Dateien; private Repository-Sichtbarkeit nicht als Geheimhaltung garantieren.
- Vor Abschluss fachliche Aussagen und Aufgabenabdeckung prüfen, den passenden
  Build ausführen und betroffene PDF-Seiten ansehen. Fehler, Warnungen,
  ungeprüfte Inhalte und fehlende Quellen offen melden. Ein erfolgreicher
  LaTeX-Build ersetzt keine inhaltliche oder visuelle Prüfung.
- Bestehende Änderungen respektieren. Keine fremden Dateien überschreiben,
  keine Historie umschreiben und keine unnötigen Änderungen außerhalb des
  Auftrags vornehmen. Sachliche Commits ohne Co-Author-Signatur.
