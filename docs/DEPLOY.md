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

**Chantier n°1 (à exécuter)** : éclater la SPA en vraies pages statiques
(/agents/ /roi/ /tarifs/ /contact/ /calculateur/ + légales), nav en <a href>, titles/metas dédiés
(carte mots-clés dans la revue), sitemap complet, 301 nginx des routes sans slash.

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
