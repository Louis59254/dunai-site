# Déploiement & notes techniques — dunai.fr

Site statique (HTML/CSS/JS, sans build) servi par nginx (Coolify → Hostinger).
Pas de pipeline de build : les fichiers du dépôt sont servis tels quels depuis la racine.

## Architecture

- `index.html` — SPA mono-fichier. 8 vues `.page` (home, agents, roi, tarifs, contact,
  calculateur, mentions, confidentialite) affichées/masquées par `showPage()` + `history.pushState`.
- `Blog/` — blog statique séparé, servi sur `/blog` (→ `Blog/index.html`).
- `sitemap.xml`, `robots.txt` — à la racine.
- `images/og-cover.png` — image de partage social (1200×630), référencée par les balises Open Graph.

## ⚠️ Deep-links SPA — config serveur requise

Les URL `/agents`, `/roi`, `/tarifs`, `/contact`, `/calculateur`, `/mentions-legales`,
`/confidentialite` sont gérées **côté client**. En accès direct (lien partagé, crawl Google),
le serveur doit renvoyer `index.html` sinon **404**.

`.htaccess` (Apache) est **ignoré par nginx**. Ajouter dans la config nginx du service Coolify :

```nginx
location / {
    try_files $uri $uri/ /index.html;
}

# Garder le blog servi directement
location /blog {
    return 301 /Blog/;
}
```

Une fois ce fallback en place :
1. les deep-links résolvent (plus de 404) ;
2. on peut convertir la nav `onclick="showPage('x')"` en `<a href="/x">` **crawlables**
   (progressive enhancement : `href` pour Google, `return false` pour la fluidité SPA) ;
3. ajouter les routes (`/agents`, `/roi`, `/tarifs`, `/contact`, `/calculateur`) au `sitemap.xml`.

**Alternative SEO optimale** : éclater la SPA en vraies pages statiques
(`/agents/index.html`, etc.), chacune avec `title`/`meta`/`canonical`/JSON-LD propres.
Meilleur référencement, mais maintenance d'un shell dupliqué (ou génération au build).

## Identité légale (renseignée)

Louis Slosse, entrepreneur individuel (« Dunai ») · SIREN 792 902 892 ·
SIRET 792 902 892 00019 · TVA FR95792902892 · 78 rue Marceau, 59240 Dunkerque.
Mentions légales + politique de confidentialité remplies ; JSON-LD avec NAP complet.

## À vérifier / compléter

- **Hébergeur** : mentions légales indiquent Hostinger (déduit de Coolify→Hostinger).
  À corriger si le VPS Coolify est chez un autre fournisseur (OVH, Hetzner…).
- **Code APE 9329Z** (« Autres activités récréatives et de loisirs ») au registre :
  ne correspond pas à l'activité IA/conseil — envisager une mise à jour auprès de l'INSEE/URSSAF
  (point administratif, sans impact sur le site).
- **`sameAs` JSON-LD** : ajouter l'URL LinkedIn de l'entreprise une fois connue.
- **n8n** (`WEBHOOK_URL`) : endpoint public sans auth — ajouter rate-limiting / honeypot côté n8n.
- **« Satisfait ou remboursé sans conditions »** : à encadrer par des CGV.

## Cohérence chiffres à surveiller

- Témoignage home « 28h = 14 000 €/an » implique ~41,6 €/h, alors que le site ancre 35 €/h.
- Le blog (`Blog/*.html`) cite « 28h = 18 000 €/an » pour un cas similaire → aligner sur un jeu canon.

## Revue complète 2026-06-12 — plan « premier sur Google » (local Nord → national)

**Fait (commit 2d67cbe)** : FAQPage home+traiteur, geo JSON-LD, BlogPosting+Breadcrumb sur 15 articles,
7 liens cassés blog corrigés, /blog→/Blog/ normalisé partout, canonical doublon ROI → pilier,
/traiteur/ ajouté au sitemap, title traiteur ≤60.

**Chantier n°1 : FAIT (2026-06-12, commits c07bb93 + d894562)** : SPA éclatée en vraies pages
(/agents/ /roi/ /tarifs/ /contact/ /calculateur/ /mentions-legales/ /confidentialite/ + /agence-ia-dunkerque/),
assets partagés (assets/site.css, assets/site.js), nav crawlable, titles/metas/JSON-LD par page,
sitemap 25 URLs, chiffre canon 28h=11 800 €/an, compteurs requalifiés.
Anciennes routes sans slash : 301 automatique nginx (redirect dossier).

**Google Business Profile (Louis, levier n°1 local)** :
- Créer la fiche : catégorie « Consultant en informatique », zone desservie Dunkerque + CUD + Nord.
- NAP strictement identique au site : Dunai · 101 rue du Meulhouck, 59254 Ghyvelde · +33 6 46 89 08 87.
- Photos (logo, captures CRM), description avec « agence IA Dunkerque », lien dunai.fr.
- Avis Google : demander après CHAQUE audit/mission (objectif 5-10 en 2 mois), répondre à tous.
- Citations NAP identiques : PagesJaunes, Bing Places, Apple Plans, Kompass, annuaire CCI Hauts-de-France.
- Backlinks locaux : CCI Grand Lille, French Tech Lille/Euratechnologies, Voix du Nord / Phare dunkerquois, France Num (activateur).

**Contenu à produire (peut être fait par Claude)** :
- Pages locales : /agence-ia-dunkerque (P1), /agence-ia-lille + /automatisation-ia-hauts-de-france (P2). Contenu unique par ville, pas de clone.
- 10 articles planifiés (3 supports CRM Traiteur : « logiciel pour traiteur », « comment faire un devis traiteur », « gestion événements traiteur »).

**Conversion (revue)** : ajouter réservation de créneau (Cal.com) sur /contact ; capture email au résultat du mini-calc ;
témoignage NOMMÉ avec photo (Louis) ; vraies CGV encadrant « satisfait ou remboursé » ; bloc « qui est derrière Dunai » avec photo.

**Décisions en attente (Louis)** :
- Chiffre canon témoignage : 28h/mois = 14 000 €/an (home) vs 18 000 €/an (blog ×12) vs 11 760 € (cohérent 35 €/h). Recommandation : ~11 800 €/an partout.
- Compteurs « 4800 emails / 340h / 1200 devis » : à requalifier ou retirer tant que pas de volume réel.
- WebP pour les 6 PNG traiteur (2,5 MB → ~300 KB).

## Recherche concurrence 2026-06-12 (résumé actionnable)

Marché fragmenté, aucun leader. À Dunkerque : QUE des pages SEO fantômes d'agences distantes
(Synapze/Var, NexFlow…) → /agence-ia-dunkerque/ créée pour prendre la place. Seul vrai concurrent
régional : Les Entrecodeurs (Lille) — forts (secteurs, certifs, tarifs partiels) mais 0 blog, 0 avis.

Standards du marché à matcher : calculateur ROI (on l'a), diagnostic en ligne multi-étapes (à faire),
Calendly (à faire, compte Louis), audit gratuit (on l'a).
Gaps que PERSONNE ne couvre (à prendre) : témoignages vidéo, tarifs transparents (on les a → marteler),
livre blanc téléchargeable, blog fourni (eux : 3-6 articles).
CRM Traiteur : créneau « IA » totalement vierge chez les logiciels traiteur (MobiChef, DigiFactory…),
tous opaques sur les prix sauf DigiFactory 10 €/mois/user. Angle gagnant : « CRM traiteur augmenté par
l'IA » + page comparatif transparent (« logiciel traiteur prix », « DigiFactory avis », « MobiChef tarif »).

Backlog contenu (ordre) : pages secteurs (BTP, logistique/port, commerce, services) ·
/agence-ia-lille/ + /automatisation-ia-hauts-de-france/ · 10 articles (3 supports traiteur :
« logiciel pour traiteur », « comment faire un devis traiteur », « gestion événements traiteur ») ·
comparatif « n8n vs Make vs Zapier » · « combien coûte l'automatisation » · livre blanc PDF.
Villes sans concurrent : Gravelines, Grande-Synthe, Bergues, Hazebrouck, Cassel (longue traîne).

## Vignettes de blog — contrôle qualité permanent (2026-08-05)

Chaque article a une vignette `Blog/images/dunai-thumb-<slug>.svg` (cards du site)
et son jumeau `.png` 1200×630 (og:image / twitter:image, les réseaux sociaux ne
rendent pas le SVG).

**Contrôle : `python3 tools/check-thumbs.py`** (toutes) ou avec un fichier en
argument. Vérifie : XML, viewBox 1200×630, marque `dunai.fr`, chiffres canon
(ROI ×3 jamais ×4, 11 800 €/an jamais 18 000), zéro tiret cadratin, accents
français obligatoires, pas de « garanti » ni de formulation anxiogène, pas de
« 2 jours » (l'audit réel dure 2h), débordements et collisions de texte.

**Automatisation en place** (hooks `~/.claude/settings.json`) :
1. Toute écriture d'un `dunai-thumb-*.svg` déclenche le check ; si défaut,
   l'agent reçoit la liste des erreurs et doit corriger avant publication.
   Si OK, le PNG og:image est régénéré automatiquement (Chrome headless).
2. Le hook de publication d'articles réécrit les og:image `.svg` → `.png`,
   et n'ajoute la vignette au commit que si le check passe.

Audit du 2026-08-05 : les 23 vignettes revues visuellement (planches lot par
lot) et corrigées : ×4→×3, 18 000→11 800 €/an, accents restaurés (appels
d'offres, recrutement, reporting, service client), tirets cadratins supprimés,
« 2 jours »→2h, « ROI garanti » supprimé, label collé décollé (Dunkerque),
label erroné facturation, pied dunai.fr ajouté sur IA Act. 23/23 vertes.

## Passe SEO Hauts-de-France (2026-08-05, commit 025aef9)

20 nouvelles pages, contenu différencié (pas des clones) :
- **9 villes** : /agence-ia-{lille,calais,boulogne-sur-mer,saint-omer,hazebrouck,arras,lens,valenciennes,amiens}/
  (tissu éco local réel, cas d'usage adaptés, FAQ locale, Service JSON-LD areaServed ville).
  Dunkerque conservée telle quelle (page historique).
- **8 secteurs** : /ia-{industrie,logistique-transport,btp-artisans,commerce,restauration-traiteurs,professions-liberales,sante,services-b2b}/
  (douleurs, chiffres canon mesurés uniquement, 3 articles blog liés chacun, FAQ métier).
- **3 offres** : /crm-sur-mesure/ (tarifs = catalogue traiteur en référence),
  /accompagnement-ia/ (audit → Pack Déclic → suivi mensuel ; Référent IA 3 900 € déductible),
  /automatisation-ia-hauts-de-france/ (pilier : liens villes+secteurs+solutions).
- **Maillage** : footer 3 colonnes (Zones/Secteurs/Solutions, 27 liens) sur toutes les pages
  standard + ligne SEO sur /traiteur/ ; section « Hauts-de-France » sur la home (18 pills liens) ;
  areaServed business élargi (10 villes + Nord/Pas-de-Calais/Somme) ; sitemap 53 URLs.
- Générateurs : /tmp/seo/*.py (jetables). Article prospection inexistant (vignette orpheline
  dunai-thumb-ia-prospection-*) : lien remplacé, article à écrire (candidat plan édito).

Louis (rappel toujours en attente) : GA4, Search Console + soumission sitemap (53 URLs
maintenant), Google Business Profile. Ces trois-là comptent plus que tout pour le local.

## Bloc nginx à coller dans Coolify (revue 2026-08-07, item 4)

Dans Coolify > service dunai.fr > configuration nginx personnalisée :

```nginx
# vraies 404 (fin du soft-404 hérité de la SPA)
try_files $uri $uri/ =404;
error_page 404 /404.html;
autoindex off;

# blog : casse unifiée
location = /blog { return 301 /Blog/; }
location ~ ^/blog/(.+)$ { return 301 /Blog/$1; }

# cache long sur les assets versionnés (?v=), no-cache sur le HTML
location ~* \.(css|js|svg|webp|png|jpg|woff2)$ {
  add_header Cache-Control "public, max-age=31536000, immutable";
}
location ~* \.html$ {
  add_header Cache-Control "no-cache";
}
```

Après application : tester `curl -I https://dunai.fr/page-inexistante/` (attendu 404),
`curl -I https://dunai.fr/blog/ai-act-pme-2026/` (attendu 301 → /Blog/...),
`curl -sI https://dunai.fr/assets/site.css | grep -i cache` (attendu max-age=31536000).
