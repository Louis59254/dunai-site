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
