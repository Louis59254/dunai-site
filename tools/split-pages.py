#!/usr/bin/env python3
"""Migration one-shot : éclate la SPA index.html en vraies pages statiques.

- Extrait <style> -> assets/site.css et le JS -> assets/site.js (routing retiré, guards ajoutés)
- Génère /agents/ /roi/ /tarifs/ /contact/ /calculateur/ /mentions-legales/ /confidentialite/
- index.html devient la home seule
- Tous les onclick="showPage('x')" deviennent de vrais liens
"""
import re, os, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / "index.html").read_text(encoding="utf-8")

URL = {
    "home": "/", "agents": "/agents/", "roi": "/roi/", "tarifs": "/tarifs/",
    "contact": "/contact/", "calculateur": "/calculateur/",
    "mentions": "/mentions-legales/", "confidentialite": "/confidentialite/",
    "blog": "/Blog/",
}
NAV_LABEL = {  # libellé du lien nav correspondant à chaque page (pour aria-current)
    "home": "Accueil", "agents": "Agents IA", "roi": "Résultats", "tarifs": "Tarifs",
}
HEADS = {
    "home": ("Agence IA & automatisation à Dunkerque | Dunai",
             "Dunai, agence IA à Dunkerque : automatisation des tâches répétitives des PME des Hauts-de-France. Audit gratuit, agents IA, ROI en 6 semaines."),
    "agents": ("Agents IA pour PME : 7 cas d'usage concrets | Dunai",
               "7 agents IA qui automatisent relances, devis, factures, accueil téléphonique et reporting pour les PME. Exemples concrets et gains mesurés."),
    "roi": ("ROI de l'automatisation IA : résultats en PME | Dunai",
            "Chiffres réels d'automatisation IA en PME : heures gagnées, ROI en semaines, études de cas avant/après. Des résultats, pas des promesses."),
    "tarifs": ("Tarifs automatisation IA pour PME et TPE | Dunai",
               "Tarifs clairs : Pack IA Déclic 2 990 € HT, offres PME/ETI sur devis. ROI validé avant tout déploiement. Audit gratuit inclus."),
    "contact": ("Audit IA gratuit pour votre PME | Dunai Dunkerque",
                "Réservez votre audit IA gratuit : 2h sur site ou en visio, rapport chiffré sous 48h. PME, TPE et artisans, Hauts-de-France et toute la France."),
    "calculateur": ("Calculateur ROI : coût de vos tâches répétitives | Dunai",
                    "Estimez en 60 secondes le coût annuel de vos tâches répétitives et votre gain potentiel avec l'automatisation IA. Gratuit, sans inscription."),
    "mentions": ("Mentions légales | Dunai",
                 "Mentions légales du site dunai.fr, édité par Dunai (Louis Slosse), Ghyvelde, Hauts-de-France."),
    "confidentialite": ("Politique de confidentialité | Dunai",
                        "Politique de confidentialité et protection des données personnelles du site dunai.fr (RGPD)."),
}
PAGE_NAMES = {  # nom lisible pour le breadcrumb
    "agents": "Agents IA", "roi": "Résultats", "tarifs": "Tarifs", "contact": "Audit gratuit",
    "calculateur": "Calculateur ROI", "mentions": "Mentions légales", "confidentialite": "Confidentialité",
}

# ── découpage du source ──────────────────────────────────────────────
style_m = re.search(r"<style>([\s\S]*?)</style>", SRC)
css = style_m.group(1).strip()

script_blocks = re.findall(r"<script>([\s\S]*?)</script>", SRC)
js = script_blocks[-1]  # le gros bloc applicatif en fin de body

head_full = SRC[: SRC.index("<style>")]          # doctype -> juste avant <style> (inclut metas + ld+json home + fonts)
after_style_to_body = SRC[style_m.end(): SRC.index("<body>")]  # "</head>" résiduel
shell_top = SRC[SRC.index("<body>"): SRC.index('<div id="page-home"')]  # body, skip, noscript, menu, nav
sticky = SRC[SRC.index("<!-- STICKY CTA -->"): SRC.index("<script>", SRC.index("<!-- STICKY CTA -->"))]

# pages : positions de chaque <div id="page-X"
ids = ["home", "agents", "roi", "tarifs", "contact", "calculateur", "mentions", "confidentialite"]
pos = {i: SRC.index(f'<div id="page-{i}"') for i in ids}
end_pages = SRC.index("<!-- STICKY CTA -->")
page_html = {}
for k, i in enumerate(ids):
    start = pos[i]
    end = pos[ids[k + 1]] if k + 1 < len(ids) else end_pages
    page_html[i] = SRC[start:end].rstrip() + "\n"

# ── transformations de liens (s'appliquent partout) ──────────────────
def fix_links(h: str) -> str:
    # <a ... onclick="showPage('x')[;closeMenu()]" ...> -> <a ... href="/x/" ...>
    h = re.sub(r"""<a([^>]*?) onclick="showPage\('(\w+)'\)(?:;closeMenu\(\))?"([^>]*)>""",
               lambda m: f'<a{m.group(1)} href="{URL[m.group(2)]}"{m.group(3)}>', h)
    # <a onclick="showPage('x')"> variante sans espace avant onclick
    h = re.sub(r"""<a onclick="showPage\('(\w+)'\)(?:;closeMenu\(\))?">""",
               lambda m: f'<a href="{URL[m.group(1)]}">', h)
    # <button ... onclick="showPage('x')" ...> -> navigation JS (les CTA n'ont pas besoin d'être crawlables)
    h = re.sub(r'onclick="showPage\(\'(\w+)\'\)"',
               lambda m: f"onclick=\"location.href='{URL[m.group(1)]}'\"", h)
    return h

shell_top = fix_links(shell_top)
sticky = fix_links(sticky)
for i in ids:
    page_html[i] = fix_links(page_html[i])

# aria-current : retirer l'état actif par défaut du template nav
shell_top = shell_top.replace(' class="active">Accueil</a>', '>Accueil</a>')

def nav_for(page: str) -> str:
    nav = shell_top
    label = NAV_LABEL.get(page)
    if label:
        nav = nav.replace(f'href="{URL[page]}">{label}</a>',
                          f'href="{URL[page]}" class="active" aria-current="page">{label}</a>')
    # skip-link vers la bonne ancre
    nav = nav.replace('href="#page-home"', f'href="#page-{page}"')
    return nav

# ── JS partagé : retirer le routing, ajouter les guards ──────────────
def cut(js, start_marker, end_marker):
    a = js.index(start_marker)
    b = js.index(end_marker, a)
    return js[:a] + js[b:]

# routing complet (pageMap ... popstate listener)
js = cut(js, "const pageMap", "function toggleMenu")
# init DOMContentLoaded du routeur
js = cut(js, "let countersStarted=false;", "function startCounters")
js = "let countersStarted=false;\n" + js
# le hook showPage du sticky
js = js.replace("""  // Re-vérifier au changement de page (hook sur showPage existant)
  const _orig = window.showPage;
  window.showPage = function(...args) { _orig(...args); setTimeout(updateSticky, 50); };
  updateSticky();""", "  updateSticky();")
# guard calcUpdateResult (page sans calculateur)
js = js.replace("function calcUpdateResult() {\n  let totalH = 0;",
                "function calcUpdateResult() {\n  if (!document.getElementById('calcResultEmpty')) return;\n  let totalH = 0;")
# auto-init des compteurs sur la page agents
js += "\nif (document.getElementById('c1')) startCounters();\n"

assert "showPage" not in js, "showPage encore référencé dans le JS"

# ── heads ─────────────────────────────────────────────────────────────
ICON_FONTS = """<link rel="icon" href="/images/logo-favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/images/logo-favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">"""

def subpage_head(page: str) -> str:
    title, desc = HEADS[page]
    url = f"https://dunai.fr{URL[page]}"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": url, "url": url, "name": title,
             "inLanguage": "fr-FR", "isPartOf": {"@id": "https://dunai.fr/#website"},
             "about": {"@id": "https://dunai.fr/#business"}, "description": desc},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://dunai.fr/"},
                {"@type": "ListItem", "position": 2, "name": PAGE_NAMES[page]}]},
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Dunai">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://dunai.fr/images/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://dunai.fr/images/og-cover.png">
{ICON_FONTS}
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
"""

JS_TAG = '<script src="/assets/site.js"></script>'

def build_page(page: str) -> str:
    body = page_html[page].replace('class="page"', 'class="page active"', 1)
    return subpage_head(page) + nav_for(page) + "\n" + body + "\n" + sticky + JS_TAG + "\n</body>\n</html>\n"

# ── écriture ──────────────────────────────────────────────────────────
(ROOT / "assets").mkdir(exist_ok=True)
(ROOT / "assets/site.css").write_text(css + "\n", encoding="utf-8")
(ROOT / "assets/site.js").write_text(js.strip() + "\n", encoding="utf-8")

OUT = {"agents": "agents", "roi": "roi", "tarifs": "tarifs", "contact": "contact",
       "calculateur": "calculateur", "mentions": "mentions-legales", "confidentialite": "confidentialite"}
for page, folder in OUT.items():
    d = ROOT / folder
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(build_page(page), encoding="utf-8")

# ── home : head existant retravaillé + page-home seule ───────────────
home_head = head_full
home_title, home_desc = HEADS["home"]
home_head = re.sub(r"<title>[^<]+</title>", f"<title>{home_title}</title>", home_head)
home_head = re.sub(r'<meta name="description" content="[^"]+">',
                   f'<meta name="description" content="{home_desc}">', home_head)
home_head = re.sub(r'<meta property="og:title" content="[^"]+">',
                   f'<meta property="og:title" content="{home_title}">', home_head)
home_head = re.sub(r'<meta name="twitter:title" content="[^"]+">',
                   f'<meta name="twitter:title" content="{home_title}">', home_head)
home = (home_head + ICON_FONTS.replace('<link rel="icon" href="/images/logo-favicon.svg" type="image/svg+xml">\n<link rel="apple-touch-icon" href="/images/logo-favicon.svg">\n', '')  # icônes déjà dans le head home
        + "\n</head>\n" + nav_for("home") + "\n" + page_html["home"] + "\n" + sticky + JS_TAG + "\n</body>\n</html>\n")
# le head home contenait déjà preconnect+fonts -> retirer le doublon ajouté
home = home.replace("""<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://fonts.googleapis.com">""", """<link rel="preconnect" href="https://fonts.googleapis.com">""", 1)
(ROOT / "index.html").write_text(home, encoding="utf-8")

print("OK · pages générées :", ", ".join(OUT.values()))
print("CSS :", len(css), "chars · JS :", len(js), "chars")
