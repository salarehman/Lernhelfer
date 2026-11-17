#!/usr/bin/env python3
"""chemie.py – erzeugt Figuren für die Chemie-Lernhelfer.

Läuft im öffentlichen Repo `Lernhelfer`. Braucht eine Python-Umgebung mit
`rdkit` und `matplotlib` (z. B. das scienv unter /opt/data/scienv).

Erzeugt je Aufgabe, die eine Abbildung braucht, ein `figures/`-Verzeichnis
im Aufgabenordner und legt dort hochauflösende PNGs ab, die über
`\\includegraphics` (graphicx, schon in tex/preamble) in theorie.tex /
loesung.tex eingebunden werden. Pfade relativ zur Repo-Wurzel angeben
(tectonic-Auflösung).

Subbefehle (komponierbar; jede Option kann mehrmals gesetzt werden):

  chemie.py mol      --smiles 'CCO'        Molekül aus SMILES (2D-Struktur)
  chemie.py analog   --smiles 'O=C=O'      besser lesbare 2D-Struktur (rdkit)
  chemie.py energie  --zustände g2 e1      Energie-Diagramm (Listen an Niveaus)
  chemie.py orbital  --typ p --achse x     p-/d-/f-Orbital schematisch (2D)
  chemie.py symmetrie --punkte C2 H       Molekül-Symmetrie / Orientierung
  chemie.py zeige  --ordnung 1,2,3,...     Energieniveau-/Besetzungsdiagramm

Allgemein:
  --out PFAD    Ziel-PNG (Absolut oder relativ zur Repo-Wurzel)
  --dpi N       Auflösung (Standard 200)

Beispiel:
  python3 werkzeuge/chemie.py mol --smiles 'CCO' \
      --out aufgaben/chemie/blatt01/01-bindung/figures/ethanol.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from rdkit import Chem
    from rdkit.Chem import Draw, AllChem
except ImportError:
    Chem = None
    Draw = None
    AllChem = None

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def _mol_png(smiles: str, out: Path, dpi: int, size=(500, 380)) -> None:
    if Chem is None:
        raise SystemExit("rdkit fehlt – nutze eine Umgebung mit rdkit (z. B. /opt/data/scienv).")
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        raise SystemExit(f"ungültige SMILES: {smiles!r}")
    AllChem.Compute2DCoords(m)
    img = Draw.MolToImage(m, size=size, dpi=(dpi, dpi))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"Figure: {out}")


def _energie_png(zustaende: list[str], out: Path, dpi: int) -> None:
    if plt is None:
        raise SystemExit("matplotlib fehlt.")
    fig, ax = plt.subplots(figsize=(7, 5))
    levels = [float(z) for z in zustaende]
    ymax = max(levels) * 1.3 + 0.5
    # Reaktionsdiagramm: Energieniveaus als Linien mit Labels
    for i, l in enumerate(levels):
        x = i / (len(levels) - 1) if len(levels) > 1 else 0.5
        ax.hlines(l, x - 0.12, x + 0.12, color="#1F4E79", lw=3)
        ax.annotate(f"{l:.1f}", (x, l), xytext=(x, l + 0.25),
                    ha="center", fontsize=11, color="#1F4E79")
    ax.set_ylim(-0.5, ymax)
    ax.set_ylabel("Energie (a.u.)", fontsize=12)
    ax.set_xlabel("Reaktionskoordinate", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print(f"Figure: {out}")


def _orbital_png(o_typ: str, achse: str, out: Path, dpi: int) -> None:
    if plt is None:
        raise SystemExit("matplotlib fehlt.")
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect("equal")
    t = __import__("numpy").linspace(0, 2 * 3.14159, 200)
    # Schematische Orbitallappen an der gewählten Achse
    amp = {"x": 1, "y": 1}.get(achse, 1)
    for sign in (1, -1):
        x = sign * 0.55 * __import__("numpy").cos(t)
        y = 0.35 * __import__("numpy").sin(t) * amp
        ax.fill(x, y, color=("#D94F4F" if sign == 1 else "#4A7BA6"),
                alpha=0.6, edgecolor="k", lw=1)
    ax.plot([0, 0], [-1.1, 1.1], "k-", lw=1.2)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis("off")
    ax.set_title(f"{o_typ}-Orbital ({achse}-Achse)", fontsize=12)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print(f"Figure: {out}")


def _symmetrie_png(punkte: list[str], out: Path, dpi: int) -> None:
    if plt is None:
        raise SystemExit("matplotlib fehlt.")
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect("equal")
    # Grobes Symmetrie-/Orientierungsschema: Punkte auf einem Kreis
    n = len(punkte)
    t = __import__("numpy").linspace(0, 2 * 3.14159, n + 1)[:-1]
    xs = __import__("numpy").cos(t)
    ys = __import__("numpy").sin(t)
    ax.scatter(xs, ys, s=260, color="#EAF1F8", edgecolor="#1F4E79", zorder=2)
    for (x, y, lab) in zip(xs, ys, punkte):
        ax.annotate(lab, (x, y), ha="center", va="center", fontsize=14, color="#1F4E79")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print(f"Figure: {out}")


def main() -> int:
    p = argparse.ArgumentParser(prog="chemie.py", description="Erzeugt Chemie-Figuren (rdkit + matplotlib).")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name in ("mol", "analog"):
        sp = sub.add_parser(name, help="Molekül-Struktur aus SMILES")
        sp.add_argument("--smiles", required=True)
        sp.add_argument("--out", required=True)
        sp.add_argument("--dpi", type=int, default=200)
        sp.set_defaults(func=lambda a: _mol_png(a.smiles, Path(a.out), a.dpi))

    sp = sub.add_parser("energie", help="Energie-Diagramm (Niveau-Liste)")
    sp.add_argument("--zustände", required=True, help="kommaseparierte Energie-Werte, z. B. 0,3,1.5")
    sp.add_argument("--out", required=True)
    sp.add_argument("--dpi", type=int, default=200)
    sp.set_defaults(func=lambda a: _energie_png([z for z in a.zustände.split(",")], Path(a.out), a.dpi))

    sp = sub.add_parser("orbital", help="Orbital-Schema (p/d/f)")
    sp.add_argument("--typ", default="p")
    sp.add_argument("--achse", default="x")
    sp.add_argument("--out", required=True)
    sp.add_argument("--dpi", type=int, default=200)
    sp.set_defaults(func=lambda a: _orbital_png(a.typ, a.achse, Path(a.out), a.dpi))

    sp = sub.add_parser("symmetrie", help="Symmetrie-/Orientierungsschema")
    sp.add_argument("--punkte", required=True, help="kommaseparierte Labels, z. B. C2,H,H")
    sp.add_argument("--out", required=True)
    sp.add_argument("--dpi", type=int, default=200)
    sp.set_defaults(func=lambda a: _symmetrie_png([x for x in a.punkte.split(",")], Path(a.out), a.dpi))

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
