#!/usr/bin/env python3
"""webseite_erzeugen.py — erzeugt index.html (Landing-Page) für die Lernhelfer-PDFs.

Die Seite listet jede Fach/Blatt-Kombination als grossen, antippbaren Eintrag,
der die fertige PDF direkt im Browser öffnet — bewusst ohne git, ohne Ordner,
ohne Fachsprache: Eine einzige URL, zum Teilen mit Kommilitonen.

Aufruf (Repo-Wurzelverzeichnis):
    python3 werkzeuge/webseite_erzeugen.py   # schreibt / überschreibt index.html

Danach baut eine GitHub-Action diesen Inhalt als Pages-Site (Quelle: main,
Ordner: /), sodass https://<user>.github.io/Lernhelfer/ die aktuelle Indexseite
plus alle out/<fach>/<blatt>-lernhelfer.pdf direkt ausliefert.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
OUT = WURZEL / "out"

FACH_NAME = {"mathe": "Mathematik", "physik": "Physik", "chemie": "Chemie"}
FACH_BESCHR = {
    "mathe": "Mathematische Methoden I",
    "physik": "Physik I",
    "chemie": "Chemie",
}


def blatt_sammlung() -> dict[str, dict[int, str]]:
    """fach -> {blattnummer: relativer PDF-Pfad}."""
    erg = {}
    if not OUT.is_dir():
        return erg
    for f in sorted(OUT.iterdir()):
        if not f.is_dir():
            continue
        subs = {}
        for p in sorted(f.glob("blatt*-lernhelfer.pdf")):
            m = re.match(r"blatt(\d+)-lernhelfer\.pdf", p.name)
            if m:
                subs[int(m.group(1))] = p.relative_to(WURZEL).as_posix()
        if subs:
            erg[f.name] = subs
    return erg


def baue(blätter: dict[str, dict[int, str]]) -> str:
    fach_html = []
    for fach, subs in blätter.items():
        name = FACH_NAME.get(fach, fach)
        beschr = FACH_BESCHR.get(fach, "")
        eintraege = ""
        for num in sorted(subs):
            href = html.escape(subs[num])
            eintraege += (
                f'<a class="blatt" href="{href}" target="_blank" rel="noopener">'
                f"Blatt {num}<small>als PDF öffnen</small></a>\n"
            )
        fach_html.append(
            f'<section class="fach">'
            f'<h2><span class="badge">{html.escape(name)}</span></h2>'
            f'{f"<p class=\u0022beschr\u0022>{html.escape(beschr)}</p>" if beschr else ""}'
            f'<div class="blatt-list">{eintraege}</div>'
            f"</section>"
        )
    faecher = "\n".join(fach_html)
    return f"""<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lernhelfer — Mathe, Physik, Chemie</title>
<style>
  :root {{ --akzent:#2a6df4; --bg:#f4f6fb; --karte:#fff; --text:#1a2333; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
          background:var(--bg); color:var(--text); line-height:1.5; -webkit-text-size-adjust:100%; }}
  header {{ background:linear-gradient(135deg,#1e3a8a,#2a6df4); color:#fff; padding:2.4rem 1.2rem; text-align:center; }}
  header h1 {{ margin:0 0 .4rem; font-size:1.75rem; }}
  header p {{ margin:0 auto; opacity:.94; font-size:1.05rem; max-width:540px; }}
  main {{ max-width:780px; margin:0 auto; padding:1.4rem 1.2rem; }}
  .fach {{ margin:1.8rem 0; }}
  .fach > h2 {{ font-size:1.3rem; margin:0 0 .1rem; color:#23304d; }}
  .beschr {{ color:#5b6b82; font-size:.94rem; margin:0 0 .9rem; }}
  .blatt-list {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(185px,1fr)); gap:.65rem; }}
  a.blatt {{ display:block; background:var(--karte); border:1px solid #e2e8f2; border-radius:.75rem;
             padding:.75rem .9rem; text-decoration:none; color:var(--text); font-weight:600;
             box-shadow:0 1px 2px rgb(0 0 0/4%); transition:transform .06s,box-shadow .15s,border-color .15s; }}
  a.blatt:hover, a.blatt:focus {{ transform:translateY(-2px); box-shadow:0 4px 12px rgb(18 52 120/12%); border-color:var(--akzent); }}
  a.blatt small {{ display:block; font-weight:400; color:#62708a; font-size:.82rem; margin-top:.15rem; }}
  footer {{ text-align:center; color:#71809a; font-size:.84rem; padding:1.8rem 1rem 2.6rem; }}
</style>
</head>
<body>
<header>
  <h1>Lernhelfer</h1>
  <p>Vollständig gerechnete Übungsblätter von Mathe, Physik und Chemie — einfach antippen, PDF öffnet direkt.</p>
</header>
<main>
{faecher}
</main>
<footer>Neu aufgetauchte Blätter landen automatisch hier.</footer>
</body>
</html>
"""


def main() -> int:
    blätter = blatt_sammlung()
    if not blätter:
        print("Warnung: keine PDFs gefunden in out/ — Seite wird leer.", file=__import__("sys").stderr)
    out = WURZEL / "index.html"
    out.write_text(baue(blätter), encoding="utf-8")
    print(f"index.html geschrieben: {len(blätter)} Fächer, "
          f"{sum(len(v) for v in blätter.values())} Blätter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
