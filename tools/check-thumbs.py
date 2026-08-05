#!/usr/bin/env python3
"""Contrôle qualité des vignettes de blog (Blog/images/dunai-thumb-*.svg).

Usage :
  python3 tools/check-thumbs.py                 # vérifie toutes les vignettes
  python3 tools/check-thumbs.py FICHIER.svg ... # vérifie des fichiers précis
  python3 tools/check-thumbs.py --hook          # mode hook Claude Code (JSON sur stdin)

Sort avec le code 1 (ou 2 en mode --hook) si un problème est détecté.
Vérifie : XML valide, viewBox 1200x630, marque présente, chiffres canon
(ROI x3, 11 800 EUR/an), zéro tiret cadratin, français accentué, pas de
formulation anxiogène, débordements et collisions de texte (anchor-aware).
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VIEWBOX = (1200.0, 630.0)
MARGIN = 20.0          # marge minimale au bord
GAP_MIN = 12.0         # espace minimal entre deux textes sur une même ligne
CHAR_W_BOLD = 0.60     # largeur estimée d'un caractère (ratio de font-size)
CHAR_W_NORM = 0.55

# Chaînes interdites (comparées après décodage des entités, insensible à la casse)
FORBIDDEN = [
    ("—", "tiret cadratin (interdit sur tout le site)"),
    ("×4", "ROI ×4 : le chiffre canon est ×3"),
    ("x4", "ROI x4 : le chiffre canon est ×3"),
    ("18 000", "18 000 : le chiffre canon est 11 800 €/an"),
    ("18k", "18k : le chiffre canon est 11,8k€"),
    ("14 000", "14 000 : chiffre hors canon"),
    ("garanti", "« garanti » : promesse interdite (risque juridique)"),
    ("2 jours", "audit « 2 jours » : l'offre réelle est 2h sur site ou en visio"),
    ("ratez", "formulation anxiogène (ligne éditoriale : jamais de peur)"),
    ("en retard", "formulation anxiogène (ligne éditoriale : jamais de peur)"),
    ("trop tard", "formulation anxiogène (ligne éditoriale : jamais de peur)"),
]

# Mots français qui DOIVENT porter un accent : leur forme désaccentuée = faute
UNACCENTED = [
    "repondre", "reponse", "reponses", "repond ",
    "detecter", "rediger", "redaction",
    "salarie/", "/salarie", "salaries ",
    "taches", "repetitives", "repetitive",
    "automatise par", "automatise.", "se met a jour",
    "traites 24", "traitees", "demandes traites",
    "gagnee", "economise", "economisee", "qualifie ", "qualifies ",
    "marches publics", "aux marches",
    "premiere", "derniere", "cout ", "couts ",
    "a votre place", "deja", "grace a",
]

BRAND_REQUIRED = ["dunai.fr"]


def decode(s: str) -> str:
    import html
    return html.unescape(s)


def _floats(v, default=None):
    try:
        return float(re.sub(r"[a-z%]+$", "", v.strip()))
    except (TypeError, ValueError, AttributeError):
        return default


def _font_size(el, inherited):
    fs = el.get("font-size")
    style = el.get("style", "")
    m = re.search(r"font-size\s*:\s*([\d.]+)", style)
    if m:
        return float(m.group(1))
    if fs:
        return _floats(fs, inherited)
    return inherited


def _anchor(el, inherited):
    style = el.get("style", "")
    m = re.search(r"text-anchor\s*:\s*(\w+)", style)
    if m:
        return m.group(1)
    return el.get("text-anchor", inherited)


def collect_texts(root):
    """Retourne [(texte, x, y, font_size, anchor)] pour chaque run de texte."""
    out = []
    ns = {"svg": "http://www.w3.org/2000/svg"}
    for tag in ("text", "svg:text"):
        for t in root.iter(tag.split(":")[-1] if ":" not in tag else f"{{{ns['svg']}}}text"):
            tx = _floats(t.get("x"), 0.0)
            ty = _floats(t.get("y"), 0.0)
            tfs = _font_size(t, 16.0)
            tan = _anchor(t, "start")
            spans = list(t) or [None]
            if t.text and t.text.strip():
                out.append((t.text.strip(), tx, ty, tfs, tan))
            for sp in spans:
                if sp is None or not (sp.text and sp.text.strip()):
                    continue
                sx = _floats(sp.get("x"), tx)
                sy = _floats(sp.get("y"), ty)
                sfs = _font_size(sp, tfs)
                san = _anchor(sp, tan)
                out.append((sp.text.strip(), sx, sy, sfs, san))
        break
    return out


def check_file(path: Path):
    errors = []
    raw = path.read_text(encoding="utf-8")
    plain = decode(raw).lower()

    # 1. Contenu interdit (sur le fichier entier, entités décodées)
    for needle, why in FORBIDDEN:
        if needle.lower() in plain:
            errors.append(f"contenu interdit « {needle} » : {why}")

    # 2. Français désaccentué
    for w in UNACCENTED:
        if w in plain:
            errors.append(f"accent manquant : « {w.strip()} » trouvé sans accent")

    # 3. Marque
    for b in BRAND_REQUIRED:
        if b not in plain:
            errors.append(f"élément de marque absent : « {b} »")

    # 4. XML + géométrie
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        errors.append(f"XML invalide : {e}")
        return errors

    vb = (root.get("viewBox") or "").split()
    if len(vb) == 4:
        w, h = float(vb[2]), float(vb[3])
        if (w, h) != VIEWBOX:
            errors.append(f"viewBox {w:g}x{h:g} : attendu {VIEWBOX[0]:g}x{VIEWBOX[1]:g}")
    else:
        errors.append("viewBox absent ou malformé")

    texts = collect_texts(root)

    # 5. Débordements (anchor-aware)
    lines = {}
    for s, x, y, fs, anchor in texts:
        est = len(decode(s)) * fs * (CHAR_W_BOLD if fs >= 40 else CHAR_W_NORM)
        if anchor == "middle":
            x0, x1 = x - est / 2, x + est / 2
        elif anchor == "end":
            x0, x1 = x - est, x
        else:
            x0, x1 = x, x + est
        if x1 > VIEWBOX[0] - MARGIN + 14 or x0 < MARGIN - 14:
            errors.append(
                f"débordement probable : « {s[:40]} » "
                f"(x {x0:.0f}→{x1:.0f}, taille {fs:g}, anchor {anchor})")
        lines.setdefault(round(y / 8), []).append((x0, x1, s))

    # 6. Collisions entre textes d'une même ligne
    for _, runs in lines.items():
        runs.sort()
        for (a0, a1, sa), (b0, b1, sb) in zip(runs, runs[1:]):
            if b0 - a1 < GAP_MIN and sa != sb:
                errors.append(
                    f"textes trop proches sur une ligne : « {sa[:25]} » "
                    f"finit à {a1:.0f}, « {sb[:25]} » commence à {b0:.0f}")
    return errors


def run(paths):
    total_err = 0
    for p in paths:
        errs = check_file(p)
        if errs:
            total_err += len(errs)
            print(f"✗ {p.name}")
            for e in errs:
                print(f"    - {e}")
        else:
            print(f"✓ {p.name}")
    return total_err


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def render_png(svg_path: Path):
    """Génère le PNG 1200x630 jumeau du SVG (pour og:image). Best effort."""
    png = svg_path.with_suffix(".png")
    try:
        import subprocess
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             f"--screenshot={png}", "--window-size=1200,630",
             f"file://{svg_path.resolve()}"],
            capture_output=True, timeout=60, check=True)
        try:
            from PIL import Image
            im = Image.open(png).convert("RGB")
            im.save(png, optimize=True)
        except Exception:
            pass
        return png.exists()
    except Exception:
        return False


def main():
    args = sys.argv[1:]
    if args and args[0] == "--hook":
        # Hook Claude Code : JSON sur stdin, ne vérifie que le fichier écrit
        try:
            payload = json.load(sys.stdin)
        except Exception:
            sys.exit(0)
        fp = (payload.get("tool_input") or {}).get("file_path", "")
        if not re.search(r"dunai-thumb-.*\.svg$", fp):
            sys.exit(0)
        path = Path(fp)
        if not path.exists():
            sys.exit(0)
        errs = check_file(path)
        if errs:
            print(f"Vignette {path.name} refusée par tools/check-thumbs.py :",
                  file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
            print("Corrige le SVG puis réécris-le : le visuel doit être parfait "
                  "avant publication.", file=sys.stderr)
            sys.exit(2)  # exit 2 = feedback bloquant renvoyé à l'agent
        # Vignette valide : génère le PNG jumeau pour l'og:image des réseaux sociaux
        render_png(path)
        sys.exit(0)

    if args:
        paths = [Path(a) for a in args]
    else:
        paths = sorted((REPO / "Blog" / "images").glob("dunai-thumb-*.svg"))
    if not paths:
        print("aucune vignette trouvée")
        sys.exit(1)
    n = run(paths)
    print(f"\n{len(paths)} vignettes, {n} problème(s)")
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
