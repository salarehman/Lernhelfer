# adam-sync — Referenz: Woher die Übungsblätter & Skripte kommen

Kurzreferenz für alle, die das Lernhelfer-Repo lesen oder daran arbeiten. Sie
beantwortet drei Fragen: Was tut adam-sync, wie ist der automatisierte Ingest
aufgebaut, und warum bleibt das Quell-Material im privaten Repo.

## Zweck

adam-sync lädt **neue** und **geänderte** Dateien aus deinen ADAM-Kursen
(Uni Basel, ILIAS) automatisch herunter. Es braucht keinen API-Zugriff und
keine Passwort-POSTs (ADAM authentifiziert über SWITCH edu-ID SSO, das ist
nicht verlässlich automatisierbar): Es nutzt die normale ADAM-Websession über
**Session-Cookies**.

Der Datenfluss für den Lernhelfer-Ingest:

```
ADAM (Uni Basel)
  │  adam-sync sync   (liest Session-Cookies, crawlt nur datei-Objekte)
  ▼
dest/<fach>/                             (fach-Zuordnung über roots-Mapping)
  │  eingang.py sortieren --quelle dest/<fach> --fach <fach>
  ▼
Lernhelfer-Material/eingang/<fach>/      (neue Blätter + Skripte, privat)
  │  eingang.py einordnen --public ../Lernhelfer
  ▼
skript/<fach>/  (Skripte)   ·   aufgaben/<fach>/<blattNN>/  (Scaffold, öffentlich)
```

## Wo es lebt

- **`flake-environments/adam-sync`** — das eigentliche Pull-Tool
  (`adam_sync.py`, Nix-Flake, NixOS-Modul mit `systemd`-Timer). GitHub:
  `github:salarehman/flake-environments?dir=adam-sync`.
  Die gegen den aktuellen ADAM dokumentierten Anpassungen stehen in
  **`adam-sync/GELOESTE-PROBLEME.md`**.
- **`flake-environments/lernhelfer-sync`** — koppelt adam-sync + `eingang.py` +
  Build in einen deklarativen Sync für die beiden Lernhelfer-Repos.
  GitHub: `github:salarehman/flake-environments?dir=lernhelfer-sync`.
- **Lokaler Wächter** `/opt/data/scripts/lernhelfer-probe.sh` — der tägliche
  Cron-Probe, der Sync + Einordnung anstößt und eine deterministische Signatur
  ausgibt (siehe unten).

## Cookies (einmaliger Login)

- **Einmalig:** `adam-sync setup` öffnet einen Browser-Login und speichert die
  Session-Cookies.
- **Ablageort NUR unter `~/.config/adam-sync/cookies.json`.**
- Cookies gehören **nie in ein Git-Repo** — auch nicht in ein privates. Im
  Material-Repo wird `eingang/*.txt` per `.gitignore` ausgeschlossen, damit ein
  versehentlich abgelegter Cookie-Export nicht eingecheckt wird.
- Die ADAM-Session (`PHPSESSID`, `_shibsession_…`) verfällt nach Stunden bis
  Tagen. Dann einfach einmal neu exportieren (siehe `SESSION_EXPIRED` unten).

## Tägliche Automatisierung (Cron / systemd-Timer)

Der Timer läuft **täglich um 02:00** (`Persistent = true`, ein versäumter Lauf
wird beim nächsten Start nachgeholt). Es gibt zwei gleichwertige Wege:

1. **NixOS-Modul `lernhelfer-sync`** (`services.lernhelfer-sync`): deklariert
   `materialDir` (privates Repo), `publicDir` (öffentliches Repo) und
   `interval = "02:00"`; erzeugt `systemd.services`/`.timers`.
2. **Wächter-skript** `lernhelfer-probe.sh` (Cron, lokaler Pfad
   `/opt/data/scripts/`): pullt das Material-Repo, ruft adam-sync auf, sortiert
   je Fach nach `eingang/<fach>/`, ordnet ein und gibt eine **deterministische
   Signatur** aus, damit der Cron den Agenten nur bei Neuerungen weckt.

## Meldungen des Wächters (Signatur)

- **`NEW_MATERIAL`** — es gab Änderungen; die Aufzählung folgt und der
  Ingest-Prozess startet.
- **`NOTHING_NEW`** — kein neues Material; nichts zu tun.
- **`SESSION_EXPIRED`** — Cookies fehlen/leer, oder adam-sync meldet
  Login-Pflicht (`doStandardAuthentication`, `cmd=showLogin`, `Anmelden`).
  Dann den Nutzer bitten, die Cookies einmal neu zu exportieren. **Nie im Chat
  nach Zugangsdaten fragen** — nur zum einmaligen Cookie-Export auffordern.

## Das Wichtigste: Urheberrechtliche Trennung

Die heruntergeladenen Übungsblätter und Vorlesungsskripte sind
**urheberrechtlich geschütztes Vorlesungsmaterial** und dürfen laut
Nutzungsbedingungen nicht weitergegeben werden — auch nicht über eine
öffentliche Git-Historie. Deshalb:

- Sie liegen **nur im privaten Repo `Lernhelfer-Material`**
  (`eingang/<fach>/` für Blätter, `skript/<fach>/` für Skripte).
- Das öffentliche Repo `Lernhelfer` enthält ausschließlich selbst geschriebene
  Inhalte (die Lernhelfer-PDFs und ihre LaTeX-Quellen) und ist frei von diesen
  Dateien — faktisch und in der Git-Historie.

## Links

- `flake-environments/adam-sync` → `github:salarehman/flake-environments?dir=adam-sync`
- `adam-sync/GELOESTE-PROBLEME.md` → dokumentiert jede Anpassung gegen den
  aktuellen ADAM (Navigation `/go/<typ>/<ref>`, `ilrepositorygui`-Download,
  `roots`-Fach-Mapping, `SESSION_EXPIRED`-Erkennung, …)
- `flake-environments/lernhelfer-sync` → kombinierter Sync-Flake
- `werkzeuge/eingang.py` (im Material-Repo) → subcommands `sichten` /
  `sortieren` / `einordnen` / `status`
- `AGENTS.md` → wöchentliche Routine ab dem Eingang
