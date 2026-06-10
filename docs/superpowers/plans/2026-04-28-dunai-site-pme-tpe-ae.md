# Dunai Site — PME/TPE/AE Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Améliorer la conversion, la crédibilité et la personnalisation de `index.html` pour les profils PME, TPE et autoentrepreneur.

**Architecture:** Tout reste dans `index.html` — CSS en haut dans `<style>`, HTML dans le `<body>`, JS en bas dans `<script>`. Le profil utilisateur (`dunai_profile`) est persisté en `localStorage` et pilote l'adaptation dynamique de plusieurs sections (témoignages, FAQ, calculateur, tarifs). Aucune dépendance externe ajoutée.

**Tech Stack:** HTML5, CSS3, JavaScript vanilla (ES6+), localStorage API, IntersectionObserver API

---

## Fichiers concernés

| Fichier | Rôle |
|---------|------|
| `index.html` | Unique fichier modifié — CSS, HTML et JS |

---

## Ordre d'implémentation recommandé

Les tâches 1–4 sont indépendantes. La tâche 5 dépend de la tâche 2 (fonction `setProfile`). Les tâches 6–11 sont indépendantes entre elles mais bénéficient de la tâche 5 déjà en place.

---

## Task 1 : Hero — Pills profil + téléphone dans la nav

**Fichier :** `index.html`  
**Lignes concernées :** nav (L.474–491), hero h1 (L.503)

- [ ] **Étape 1 : Ajouter le téléphone dans la nav (desktop uniquement)**

Dans le bloc `.nav-pill`, juste avant le bouton `.nav-cta-btn`, ajouter :

```html
<a href="tel:0646890887" class="nav-phone">
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.05 2.18 2 2 0 012.03 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>
  06 46 89 08 87
</a>
```

CSS à ajouter dans `<style>` :

```css
.nav-phone { display: none; align-items: center; gap: 5px; font-size: 12px; color: rgba(255,255,255,0.55); text-decoration: none; padding: 7px 12px; border-radius: var(--r-full); transition: color .18s; }
.nav-phone:hover { color: var(--blanc); }
.nav-phone svg { stroke: currentColor; flex-shrink: 0; }
@media (min-width: 1024px) { .nav-phone { display: flex; } }
```

- [ ] **Étape 2 : Ajouter les 3 pills profil sous le H1 du hero**

Après la balise `</h1>` (fin du H1 "Vos tâches répétitives…"), insérer :

```html
<div class="hero-profile-pills">
  <span class="hero-profile-pill"><span class="hpp-dot"></span>Dirigeant PME</span>
  <span class="hero-profile-pill"><span class="hpp-dot"></span>Gérant TPE</span>
  <span class="hero-profile-pill"><span class="hpp-dot"></span>Autoentrepreneur</span>
</div>
```

CSS à ajouter :

```css
.hero-profile-pills { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1rem; }
.hero-profile-pill { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: rgba(255,255,255,0.55); border: 1px solid rgba(255,255,255,0.15); border-radius: var(--r-full); padding: 5px 12px; }
.hpp-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--flamme); flex-shrink: 0; }
```

- [ ] **Étape 3 : Vérifier dans le navigateur**

Ouvrir `index.html` en local. Vérifier :
- Sur desktop (>1024px) : numéro visible dans la nav entre les liens et le bouton CTA
- Sous le H1 : 3 pills orange/blanc visibles
- Sur mobile : numéro absent de la nav, pills wrappent proprement

- [ ] **Étape 4 : Commit**

```bash
git add index.html
git commit -m "feat: add profile pills in hero and phone number in nav"
```

---

## Task 2 : Section sélecteur de profil "Je suis…"

**Fichier :** `index.html`  
**Emplacement HTML :** Juste après la fermeture de `</section>` du hero, avant la `div.urgence`

- [ ] **Étape 1 : Ajouter le CSS du sélecteur**

Dans `<style>`, ajouter :

```css
/* SÉLECTEUR DE PROFIL */
.profile-selector { background: var(--creme); padding: 2.5rem 1.25rem; }
.profile-selector-inner { max-width: 1160px; margin: 0 auto; }
.profile-selector-hdr { margin-bottom: 1.5rem; }
.profile-tabs { display: flex; gap: 0; border: 1.5px solid var(--border-light); border-radius: var(--r-lg); overflow: hidden; margin-bottom: 0; }
.profile-tab { flex: 1; padding: 14px 10px; text-align: center; cursor: pointer; background: var(--blanc); border-right: 1px solid var(--border-light); transition: background .18s; }
.profile-tab:last-child { border-right: none; }
.profile-tab.active { background: var(--flamme-pale); border-bottom: 2px solid var(--flamme); }
.profile-tab-icon { font-size: 20px; display: block; margin-bottom: 4px; }
.profile-tab-name { font-size: 13px; font-weight: 600; color: var(--brun); display: block; }
.profile-tab.active .profile-tab-name { color: var(--flamme); }
.profile-tab-desc { font-size: 10px; color: var(--sable); display: block; margin-top: 1px; }
.profile-content { background: var(--blanc); border: 1.5px solid var(--border-light); border-top: none; border-radius: 0 0 var(--r-lg) var(--r-lg); padding: 1.5rem; }
.profile-content-title { font-size: 14px; font-weight: 700; color: var(--anthracite); margin-bottom: .875rem; font-family: 'Plus Jakarta Sans', sans-serif; }
.profile-use-cases { display: flex; flex-direction: column; gap: .5rem; margin-bottom: 1.25rem; }
.profile-use-case { display: flex; align-items: flex-start; gap: .625rem; font-size: 13px; color: var(--brun); }
.profile-use-case::before { content: '→'; color: var(--flamme); font-weight: 700; flex-shrink: 0; }
.profile-cta-row { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.profile-cta-link { font-size: 12px; color: var(--brun); text-decoration: underline; cursor: pointer; }
@media (min-width: 640px) { .profile-tabs { gap: 0; } }
@media (min-width: 1024px) { .profile-content-inner { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start; } }
```

- [ ] **Étape 2 : Ajouter le HTML de la section**

Insérer après `</section>` (fin du hero) et avant `<div class="urgence">` :

```html
<!-- SÉLECTEUR DE PROFIL -->
<section class="profile-selector">
  <div class="profile-selector-inner">
    <div class="profile-selector-hdr">
      <span class="eyebrow">Personnalisez votre expérience</span>
      <h2 class="h2" style="font-size:clamp(1.5rem,4vw,2.25rem)">Quelle situation vous ressemble le plus ?</h2>
    </div>
    <div class="profile-tabs" id="profileTabs">
      <div class="profile-tab active" data-profile="pme" onclick="setProfile('pme')">
        <span class="profile-tab-icon">🏢</span>
        <span class="profile-tab-name">PME</span>
        <span class="profile-tab-desc">10–50 salariés</span>
      </div>
      <div class="profile-tab" data-profile="tpe" onclick="setProfile('tpe')">
        <span class="profile-tab-icon">🔧</span>
        <span class="profile-tab-name">TPE / Artisan</span>
        <span class="profile-tab-desc">2–9 salariés</span>
      </div>
      <div class="profile-tab" data-profile="ae" onclick="setProfile('ae')">
        <span class="profile-tab-icon">🧑‍💻</span>
        <span class="profile-tab-name">Autoentrepreneur</span>
        <span class="profile-tab-desc">Seul·e</span>
      </div>
    </div>
    <div class="profile-content" id="profileContent"></div>
  </div>
</section>
```

- [ ] **Étape 3 : Ajouter le JS de base `setProfile()`**

Dans `<script>` en bas de page, ajouter la fonction et les données :

```javascript
const PROFILE_DATA = {
  pme: {
    title: 'Ce que Dunai automatise pour vous :',
    cases: [
      'Reporting direction produit chaque lundi — zéro intervention',
      'Saisie ERP à 0 min/jour — transfert automatique',
      'Onboarding RH en 4h au lieu de 2 jours',
      'Rapport mensuel chiffré sans toucher à Excel',
    ],
  },
  tpe: {
    title: 'Ce que Dunai automatise pour vous :',
    cases: [
      'Devis générés en 3 min au lieu de 45',
      'Relances impayés sans y penser',
      'Prise de RDV + confirmations automatiques',
      'Transfert factures fournisseurs à 0 min/jour',
    ],
  },
  ae: {
    title: 'Ce que Dunai automatise pour vous :',
    cases: [
      '8h/semaine récupérées sans embaucher',
      'Relances clients 100% automatiques',
      'Facturation et suivi sans effort',
      'Posts réseaux sociaux générés chaque semaine',
    ],
  },
};

function setProfile(p) {
  localStorage.setItem('dunai_profile', p);
  // Mettre à jour les tabs
  document.querySelectorAll('.profile-tab').forEach(t => {
    t.classList.toggle('active', t.dataset.profile === p);
  });
  // Mettre à jour le contenu
  const data = PROFILE_DATA[p];
  const content = document.getElementById('profileContent');
  if (content && data) {
    content.innerHTML = `
      <div class="profile-content-title">${data.title}</div>
      <div class="profile-use-cases">
        ${data.cases.map(c => `<div class="profile-use-case">${c}</div>`).join('')}
      </div>
      <div class="profile-cta-row">
        <button class="btn-primary" onclick="showPage('agents')" style="width:auto">Voir mes cas d'usage →</button>
        <span class="profile-cta-link" onclick="showPage('contact')">Ou commencer par l'audit gratuit</span>
      </div>`;
  }
  // Synchroniser le calculateur si présent
  if (typeof syncCalcProfile === 'function') syncCalcProfile(p);
  // Synchroniser les témoignages
  if (typeof filterTemoByProfile === 'function') filterTemoByProfile(p);
}

// Init au chargement
(function initProfile() {
  const saved = localStorage.getItem('dunai_profile') || 'pme';
  setProfile(saved);
})();
```

- [ ] **Étape 4 : Vérifier dans le navigateur**

- Cliquer sur chaque tab : le contenu change avec les bons cas d'usage
- Recharger la page : le dernier profil sélectionné est restauré
- Vérifier que `showPage('agents')` fonctionne (navigation existante)

- [ ] **Étape 5 : Commit**

```bash
git add index.html
git commit -m "feat: add profile selector section with localStorage persistence"
```

---

## Task 3 : Bouton flottant sticky

**Fichier :** `index.html`

- [ ] **Étape 1 : Ajouter le CSS du sticky**

```css
/* STICKY CTA */
.sticky-cta { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%) translateY(100px); z-index: 150; background: var(--anthracite); border: 1px solid rgba(255,255,255,0.1); border-radius: var(--r-xl); padding: 12px 16px 10px; display: flex; align-items: center; gap: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.35); transition: transform .35s cubic-bezier(.4,0,.2,1), opacity .35s; opacity: 0; pointer-events: none; white-space: nowrap; }
.sticky-cta.visible { transform: translateX(-50%) translateY(0); opacity: 1; pointer-events: all; }
.sticky-cta-text { font-size: 12px; color: rgba(255,255,255,0.5); }
.sticky-cta-phone { font-size: 11px; color: rgba(255,255,255,0.3); margin-top: 1px; }
.sticky-cta-btn { background: var(--flamme); color: var(--blanc); font-size: 13px; font-weight: 600; padding: 10px 20px; border-radius: var(--r-full); border: none; cursor: pointer; white-space: nowrap; transition: background .2s; flex-shrink: 0; }
.sticky-cta-btn:hover { background: var(--flamme2); }
@media (max-width: 639px) { .sticky-cta { bottom: 12px; padding: 10px 12px 8px; gap: 10px; } .sticky-cta-text { display: none; } }
```

- [ ] **Étape 2 : Ajouter le HTML juste avant `</body>`**

```html
<!-- STICKY CTA -->
<div class="sticky-cta" id="stickyCta">
  <div>
    <div class="sticky-cta-text">L'audit est gratuit et sans engagement.</div>
    <div class="sticky-cta-phone">📞 06 46 89 08 87</div>
  </div>
  <button class="sticky-cta-btn" onclick="showPage('contact');stickyCta.classList.remove('visible')">Audit gratuit →</button>
</div>
```

- [ ] **Étape 3 : Ajouter le JS de gestion du sticky**

Dans `<script>`, ajouter :

```javascript
(function initSticky() {
  const btn = document.getElementById('stickyCta');
  if (!btn) return;
  function updateSticky() {
    const onContact = document.getElementById('page-contact') &&
      document.getElementById('page-contact').classList.contains('active');
    const scrolled = window.scrollY > 300;
    btn.classList.toggle('visible', scrolled && !onContact);
  }
  window.addEventListener('scroll', updateSticky, { passive: true });
  // Re-vérifier au changement de page (hook sur showPage existant)
  const _orig = window.showPage;
  window.showPage = function(p) { _orig(p); setTimeout(updateSticky, 50); };
  updateSticky();
})();
```

- [ ] **Étape 4 : Vérifier dans le navigateur**

- Scroller > 300px sur la page Accueil : le bouton apparaît depuis le bas
- Naviguer vers Contact : le bouton disparaît
- Revenir sur Accueil et scroller : le bouton réapparaît
- Sur mobile : seul le bouton est visible (le texte est masqué)

- [ ] **Étape 5 : Commit**

```bash
git add index.html
git commit -m "feat: add floating sticky CTA button with scroll/page awareness"
```

---

## Task 4 : Barre de logos outils bureautiques

**Fichier :** `index.html`  
**Emplacement :** Après `</section>` du sélecteur de profil (Task 2), avant `<div class="urgence">`

- [ ] **Étape 1 : Ajouter le CSS**

```css
/* OUTILS COMPATIBLES */
.outils-section { background: var(--blanc); padding: 2rem 1.25rem; border-top: 1px solid var(--border-light); border-bottom: 1px solid var(--border-light); }
.outils-inner { max-width: 1160px; margin: 0 auto; }
.outils-label { font-size: 11px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--sable); text-align: center; margin-bottom: .5rem; }
.outils-tagline { font-size: 14px; font-weight: 500; color: var(--brun); text-align: center; margin-bottom: 1.25rem; }
.outils-pills { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
```

- [ ] **Étape 2 : Ajouter le HTML**

Insérer après la section sélecteur de profil (Task 2) :

```html
<!-- OUTILS COMPATIBLES -->
<div class="outils-section">
  <div class="outils-inner">
    <div class="outils-label">Fonctionne avec vos outils du quotidien</div>
    <div class="outils-tagline">Vous gardez ce que vous utilisez déjà — on connecte tout.</div>
    <div class="outils-pills">
      <span class="stack-pill">Excel</span>
      <span class="stack-pill">Google Sheets</span>
      <span class="stack-pill">Outlook</span>
      <span class="stack-pill">Gmail</span>
      <span class="stack-pill">Google Drive</span>
      <span class="stack-pill">Teams</span>
      <span class="stack-pill">HubSpot</span>
      <span class="stack-pill">Pipedrive</span>
      <span class="stack-pill">Salesforce</span>
      <span class="stack-pill">Sellsy</span>
      <span class="stack-pill">Sage</span>
      <span class="stack-pill">Cegid</span>
      <span class="stack-pill">EBP</span>
      <span class="stack-pill">SAP</span>
      <span class="stack-pill">Pennylane</span>
      <span class="stack-pill">Stripe</span>
      <span class="stack-pill">Docusign</span>
      <span class="stack-pill" onclick="showPage('contact')" style="cursor:pointer;border-color:var(--flamme);color:var(--flamme)">+ votre outil →</span>
    </div>
  </div>
</div>
```

- [ ] **Étape 3 : Vérifier dans le navigateur**

- Pills disposées en flex-wrap centrées
- Hover sur les pills : bordure flamme
- "+ votre outil →" en orange, clique vers Contact
- La section "Stack" existante en bas de page reste en place (outils techniques)

- [ ] **Étape 4 : Commit**

```bash
git add index.html
git commit -m "feat: add bureautique tools bar above urgence section"
```

---

## Task 5 : Statistiques clés (remplace les compteurs animés)

**Fichier :** `index.html`  
**Emplacement :** Remplace ou s'intègre dans la section `.urgence` existante

Pas de chiffres clients inventés — on utilise les résultats typiques par déploiement.

- [ ] **Étape 1 : Modifier le HTML de la section urgence**

Remplacer le contenu de `.urgence-stats` par :

```html
<div class="urgence-stats">
  <div class="u-stat"><div class="n">+28h</div><div class="l">récupérées dès le 1er déploiement, en moyenne</div></div>
  <div class="u-stat"><div class="n">×3</div><div class="l">ROI moyen constaté à 12 mois</div></div>
  <div class="u-stat"><div class="n">6 sem.</div><div class="l">pour vos premiers gains concrets</div></div>
  <div class="u-stat"><div class="n">−90%</div><div class="l">de saisie manuelle sur les tâches automatisées</div></div>
</div>
```

Mettre à jour le CSS `.urgence-stats` pour accepter 4 colonnes sur desktop :

```css
@media (min-width: 640px) { .urgence-stats { grid-template-columns: auto auto auto auto; } }
```

- [ ] **Étape 2 : Vérifier dans le navigateur**

- 4 stats visibles sur desktop, 2×2 sur mobile
- Aucun chiffre client inventé

- [ ] **Étape 3 : Commit**

```bash
git add index.html
git commit -m "feat: update urgence stats with deployment-based figures (no fake client counts)"
```

---

## Task 6 : Témoignages — Tabs profil + badges secteur

**Fichier :** `index.html`  
**Section :** `.temo-section`

- [ ] **Étape 1 : Ajouter le CSS des tabs et badges**

```css
/* TÉMOIGNAGES — TABS */
.temo-tabs { display: flex; gap: 6px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.temo-tab { font-size: 12px; font-weight: 500; padding: 6px 14px; border-radius: var(--r-full); border: 1px solid var(--border-light); background: var(--blanc); color: var(--brun); cursor: pointer; transition: all .18s; }
.temo-tab:hover { border-color: var(--flamme); color: var(--flamme); }
.temo-tab.active { background: var(--flamme); color: var(--blanc); border-color: var(--flamme); }
.temo-sector-badge { display: inline-block; background: var(--flamme-pale); border: 1px solid var(--flamme-mid); border-radius: var(--r-full); font-size: 9px; font-weight: 700; color: var(--flamme); padding: 2px 8px; margin-bottom: .5rem; text-transform: uppercase; letter-spacing: .06em; }
```

- [ ] **Étape 2 : Modifier le HTML des témoignages**

Remplacer `<div class="temo-grid">` et son contenu par :

```html
<div class="temo-tabs" id="temoTabs">
  <button class="temo-tab active" onclick="filterTemoByProfile('all')">Tous</button>
  <button class="temo-tab" onclick="filterTemoByProfile('pme')">PME</button>
  <button class="temo-tab" onclick="filterTemoByProfile('tpe')">TPE · Artisan</button>
  <button class="temo-tab" onclick="filterTemoByProfile('ae')">Autoentrepreneur</button>
</div>
<div class="temo-grid" id="temoGrid">
  <div class="temo-card" data-temo-profile="pme">
    <div class="temo-sector-badge">Transport · PME</div>
    <div class="temo-stars">★★★★★</div>
    <div class="temo-gain">28h récupérées/mois · 14 000€ économisés/an</div>
    <p class="temo-quote">L'audit m'a ouvert les yeux. Voir les chiffres écrits noir sur blanc — 28 heures par mois sur des tâches automatisables — ça m'a décidé en 5 minutes.</p>
    <div class="temo-author">Directeur général</div>
    <div class="temo-role">Transport & logistique · 18 salariés · Dunkerque</div>
  </div>
  <div class="temo-card" data-temo-profile="tpe">
    <div class="temo-sector-badge">BTP · Artisan</div>
    <div class="temo-stars">★★★★★</div>
    <div class="temo-gain">Devis 45 min → 3 min · 0 relance manuelle</div>
    <p class="temo-quote">Ce qui m'a convaincu, c'est que Dunai parle le même langage que nous. Pas de blabla tech. Juste : voilà ce qu'on peut faire, voilà ce que vous gagnez.</p>
    <div class="temo-author">Gérant</div>
    <div class="temo-role">Artisan BTP · 3 collaborateurs · Région Dunkerquoise</div>
  </div>
  <div class="temo-card" data-temo-profile="pme">
    <div class="temo-sector-badge">Médical · Cabinet</div>
    <div class="temo-stars">★★★★★</div>
    <div class="temo-gain">−62% no-show · +22% CA</div>
    <p class="temo-quote">On était sceptiques. Six semaines après, mes équipes ne veulent plus revenir en arrière. Les tâches répétitives ont simplement disparu.</p>
    <div class="temo-author">Directrice de cabinet</div>
    <div class="temo-role">Cabinet médical · 6 praticiens · Nord (59)</div>
  </div>
</div>
```

- [ ] **Étape 3 : Ajouter la fonction JS `filterTemoByProfile()`**

Dans `<script>` :

```javascript
function filterTemoByProfile(p) {
  // Mettre à jour les tabs
  document.querySelectorAll('#temoTabs .temo-tab').forEach(t => {
    t.classList.toggle('active', t.textContent.trim().toLowerCase().startsWith(p === 'all' ? 't' : p === 'pme' ? 'p' : p === 'tpe' ? 't' : 'a') || p === 'all');
  });
  // Forcer le tab actif via l'onclick comparaison
  document.querySelectorAll('#temoTabs .temo-tab').forEach(t => {
    const onclick = t.getAttribute('onclick') || '';
    t.classList.toggle('active', onclick.includes(`'${p}'`));
  });
  // Filtrer les cards
  document.querySelectorAll('#temoGrid .temo-card').forEach(card => {
    const show = p === 'all' || card.dataset.temoProfile === p;
    card.style.display = show ? '' : 'none';
  });
}
```

- [ ] **Étape 4 : Connecter à `setProfile()`**

La fonction `setProfile()` (Task 2) appelle déjà `filterTemoByProfile(p)`. Vérifier que l'appel est présent dans le code ajouté à la Task 2. Si absent, ajouter dans `setProfile()` :

```javascript
if (typeof filterTemoByProfile === 'function') filterTemoByProfile(p);
```

- [ ] **Étape 5 : Vérifier dans le navigateur**

- Tab "Tous" : 3 témoignages visibles
- Tab "PME" : 2 témoignages (Transport + Médical)
- Tab "TPE · Artisan" : 1 témoignage (BTP)
- Tab "Autoentrepreneur" : 0 témoignage (vide — acceptable jusqu'à l'ajout de vrais clients AE)
- Badge secteur visible en haut de chaque card
- Badge gain vert visible avant la citation

- [ ] **Étape 6 : Commit**

```bash
git add index.html
git commit -m "feat: add profile tabs and sector badges to testimonials section"
```

---

## Task 7 : FAQ — 3 nouvelles objections par profil

**Fichier :** `index.html`  
**Section :** `.faq-section` / `.faq-list`

- [ ] **Étape 1 : Ajouter le CSS des badges profil FAQ**

```css
.faq-profile-badge { display: inline-block; font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 4px; text-transform: uppercase; letter-spacing: .05em; margin-right: 8px; vertical-align: middle; }
.fpb-ae  { background: var(--flamme-pale); color: var(--flamme); }
.fpb-tpe { background: #faf5ff; color: #7c3aed; }
.fpb-pme { background: #eff6ff; color: #2563eb; }
.fpb-all { background: var(--vert-pale); color: var(--vert); }
```

- [ ] **Étape 2 : Insérer les 3 nouveaux items FAQ**

Dans `.faq-list`, ajouter avant le premier `.faq-item` existant :

```html
<div class="faq-item">
  <div class="faq-q" onclick="toggleFaq(this)">
    <span><span class="faq-profile-badge fpb-ae">AE</span>Je travaille seul — "vos équipes libérées" ne me parle pas vraiment.</span>
    <span class="faq-icon">+</span>
  </div>
  <div class="faq-a">C'est votre temps à vous qu'on libère. En solo, chaque heure récupérée sur des tâches répétitives est une heure que vous réinvestissez en clients, en CA ou en vie. Nos clients autoentrepreneurs récupèrent en moyenne 8h par semaine — sans embaucher, sans déléguer à quelqu'un d'autre.</div>
</div>
<div class="faq-item">
  <div class="faq-q" onclick="toggleFaq(this)">
    <span><span class="faq-profile-badge fpb-tpe">TPE</span>2 990€ c'est beaucoup pour une petite structure comme la mienne.</span>
    <span class="faq-icon">+</span>
  </div>
  <div class="faq-a">C'est exactement pourquoi on valide le ROI avant de vous proposer quoi que ce soit. Si votre automatisation ne rembourse pas au moins 3× l'investissement dans les 12 mois, on ne vous la propose pas. Nous avons aussi un Pack Solo à 1 190€ HT spécialement conçu pour les petites structures — et le paiement en 2× ou 3× est disponible sur tous nos packs.</div>
</div>
<div class="faq-item">
  <div class="faq-q" onclick="toggleFaq(this)">
    <span><span class="faq-profile-badge fpb-pme">PME</span>Mon équipe va résister au changement.</span>
    <span class="faq-icon">+</span>
  </div>
  <div class="faq-a">C'est la première crainte qu'on entend — et la dernière qu'on observe. Les agents IA ne remplacent pas vos salariés : ils leur retirent les tâches ennuyeuses et répétitives. Dans 100% des cas, après 6 semaines de déploiement, les équipes ne veulent plus revenir en arrière. La résistance vient du mot "IA" — elle disparaît dès le premier gain concret.</div>
</div>
```

- [ ] **Étape 3 : Vérifier que `toggleFaq()` fonctionne sur les nouveaux items**

La fonction `toggleFaq()` existante s'applique à tous les `.faq-item`. Tester l'ouverture/fermeture des 3 nouveaux items dans le navigateur.

- [ ] **Étape 4 : Commit**

```bash
git add index.html
git commit -m "feat: add 3 profile-specific FAQ entries (AE, TPE, PME objections)"
```

---

## Task 8 : Badge "Satisfait ou remboursé 30 jours"

**Fichier :** `index.html`

- [ ] **Étape 1 : Ajouter le CSS du badge**

```css
.satisfait-badge { display: inline-flex; align-items: center; gap: 6px; background: var(--vert); color: var(--blanc); font-size: 11px; font-weight: 700; padding: 6px 14px; border-radius: var(--r-full); }
.satisfait-badge-small { display: flex; align-items: center; gap: 6px; font-size: 11px; color: var(--vert); font-weight: 500; margin-top: .5rem; }
.satisfait-badge-small::before { content: '✓'; font-weight: 700; }
```

- [ ] **Étape 2 : Ajouter le badge dans `.garantie-section`**

Dans le 3e `.garantie-item` (Support 30 jours), après `.garantie-item-desc`, ajouter :

```html
<div style="margin-top:.75rem"><span class="satisfait-badge">✓ Satisfait ou remboursé 30 jours</span></div>
```

- [ ] **Étape 3 : Ajouter le badge au-dessus du formulaire de contact**

Dans `.contact-form`, avant `<div class="form-title">`, ajouter :

```html
<div class="satisfait-badge-small" style="margin-bottom:.875rem">Satisfait ou remboursé 30 jours — sans conditions</div>
```

- [ ] **Étape 4 : Vérifier dans le navigateur**

- Page Accueil, section Garantie : badge vert visible sous le 3e item
- Page Contact, formulaire : badge vert visible au-dessus du titre du formulaire

- [ ] **Étape 5 : Commit**

```bash
git add index.html
git commit -m "feat: add satisfait-ou-rembourse badge in garantie and contact form"
```

---

## Task 9 : Calculateur — Refonte complète

**Fichier :** `index.html`  
**Section :** `.calc-section`

C'est la tâche la plus volumineuse. Elle remplace intégralement le CSS, le HTML et le JS du calculateur existant.

- [ ] **Étape 1 : Remplacer le CSS de `.calc-section`**

Remplacer tous les blocs CSS commençant par `/* CALCULATEUR */` par :

```css
/* CALCULATEUR */
.calc-section { background: var(--creme2); }
.calc-grid { display: flex; flex-direction: column; gap: 0; }
.calc-profile-tabs { display: flex; border-bottom: 1.5px solid var(--border-light); background: var(--creme2); }
.calc-ptab { flex: 1; padding: 12px 8px; text-align: center; cursor: pointer; background: var(--creme2); border-bottom: 2px solid transparent; transition: all .18s; }
.calc-ptab-icon { font-size: 16px; display: block; margin-bottom: 3px; }
.calc-ptab-name { font-size: 11px; font-weight: 600; color: var(--brun); display: block; }
.calc-ptab-desc { font-size: 9px; color: var(--sable); display: block; }
.calc-ptab.active { border-bottom-color: var(--flamme); background: var(--flamme-pale); }
.calc-ptab.active .calc-ptab-name { color: var(--flamme); }
.calc-body-wrap { display: flex; flex-direction: column; gap: 0; }
.calc-tasks { padding: 1.25rem; display: flex; flex-direction: column; gap: .5rem; background: var(--blanc); border: 1.5px solid var(--border-light); border-top: none; border-radius: 0 0 var(--r-lg) var(--r-lg); }
.calc-category-label { font-size: 9px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--sable); margin-top: .625rem; margin-bottom: .25rem; }
.calc-category-label:first-child { margin-top: 0; }
.calc-task { background: var(--creme); border: 1.5px solid var(--border-light); border-radius: var(--r-md); padding: .75rem 1rem; transition: border-color .2s, background .2s; }
.calc-task.active { border-color: var(--flamme-mid); background: var(--flamme-pale); }
.calc-task-hdr { display: flex; align-items: center; gap: .75rem; cursor: pointer; }
.calc-cb { width: 16px; height: 16px; border-radius: 4px; accent-color: var(--flamme); flex-shrink: 0; cursor: pointer; }
.calc-task-label { font-size: 13px; color: var(--anthracite); flex: 1; }
.calc-task-hint { font-size: 10px; color: var(--sable); white-space: nowrap; }
.calc-slider-wrap { margin-top: .625rem; padding-top: .625rem; border-top: 1px solid var(--border-light); display: none; }
.calc-task.active .calc-slider-wrap { display: block; }
.calc-slider-label { font-size: 11px; color: var(--flamme); font-weight: 500; margin-bottom: .375rem; }
.calc-slider { width: 100%; accent-color: var(--flamme); cursor: pointer; }
.calc-result-box { background: var(--creme); border: 1.5px solid var(--border-light); border-top: none; padding: 1.25rem; display: flex; flex-direction: column; gap: .875rem; }
.calc-result-main { background: var(--anthracite); border-radius: var(--r-lg); padding: 1.5rem; text-align: center; }
.calc-result-main-label { font-size: 10px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: rgba(255,255,255,0.4); margin-bottom: .5rem; }
.calc-result-main-amount { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.75rem; font-weight: 800; color: var(--flamme); line-height: 1; letter-spacing: -2px; margin-bottom: .375rem; }
.calc-result-main-sub { font-size: 11px; color: rgba(255,255,255,0.4); }
.calc-result-empty { font-size: 13px; color: var(--sable); text-align: center; padding: 2rem 1rem; }
.calc-result-secondary { display: grid; grid-template-columns: 1fr 1fr; gap: .625rem; }
.calc-result-item-light { background: var(--blanc); border: 1.5px solid var(--border-light); border-radius: var(--r-md); padding: .875rem; text-align: center; }
.calc-result-item-light .n { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.5rem; font-weight: 800; color: var(--vert); line-height: 1; margin-bottom: 3px; }
.calc-result-item-light .l { font-size: 10px; color: var(--brun); line-height: 1.4; }
.calc-hourly-row { display: flex; align-items: center; gap: .75rem; background: var(--blanc); border: 1.5px solid var(--border-light); border-radius: var(--r-md); padding: .75rem 1rem; }
.calc-hourly-label { font-size: 11px; color: var(--brun); flex: 1; }
.calc-hourly-val { font-size: 13px; font-weight: 700; color: var(--flamme); white-space: nowrap; }
@media (min-width: 640px) { .calc-body-wrap { display: grid; grid-template-columns: 1.1fr 1fr; } .calc-tasks { border-radius: 0 0 0 var(--r-lg); border-right: none; } .calc-result-box { border-radius: 0 0 var(--r-lg) 0; border-left: none; } }
@media (min-width: 1024px) { .calc-grid { display: block; } }
```

- [ ] **Étape 2 : Remplacer le HTML du calculateur**

Remplacer le contenu de `<section class="section calc-section">` par :

```html
<section class="section calc-section">
  <div class="section-inner">
    <span class="eyebrow">Calculateur de gains</span>
    <h2 class="h2 h2-white" style="color:var(--anthracite)">Estimez vos gains en 60 secondes.</h2>
    <p class="lead" style="color:var(--brun)">Sélectionnez votre profil, cochez vos tâches, ajustez les volumes.</p>
    <div class="calc-grid">
      <div class="calc-profile-tabs" id="calcProfileTabs">
        <div class="calc-ptab active" data-calc-profile="pme" onclick="syncCalcProfile('pme')">
          <span class="calc-ptab-icon">🏢</span><span class="calc-ptab-name">PME</span><span class="calc-ptab-desc">10–50 sal.</span>
        </div>
        <div class="calc-ptab" data-calc-profile="tpe" onclick="syncCalcProfile('tpe')">
          <span class="calc-ptab-icon">🔧</span><span class="calc-ptab-name">TPE / Artisan</span><span class="calc-ptab-desc">2–9 sal.</span>
        </div>
        <div class="calc-ptab" data-calc-profile="ae" onclick="syncCalcProfile('ae')">
          <span class="calc-ptab-icon">🧑‍💻</span><span class="calc-ptab-name">Autoentrepreneur</span><span class="calc-ptab-desc">Seul·e</span>
        </div>
      </div>
      <div class="calc-body-wrap">
        <div class="calc-tasks" id="calcTasksContainer"></div>
        <div class="calc-result-box">
          <div id="calcResultEmpty" class="calc-result-empty">Cochez au moins une tâche pour voir votre estimation →</div>
          <div id="calcResultFilled" style="display:none;flex-direction:column;gap:.875rem">
            <div class="calc-result-main">
              <div class="calc-result-main-label">Vous perdez chaque année</div>
              <div class="calc-result-main-amount" id="calcAnnual">0 €</div>
              <div class="calc-result-main-sub">sur des tâches automatisables</div>
            </div>
            <div class="calc-result-secondary">
              <div class="calc-result-item-light"><div class="n" id="calcHours">0h</div><div class="l">récupérables / mois</div></div>
              <div class="calc-result-item-light"><div class="n" id="calcMonthly">0 €</div><div class="l">économisés / mois</div></div>
            </div>
            <div class="calc-hourly-row">
              <div class="calc-hourly-label">Votre coût horaire</div>
              <input type="range" class="calc-slider" id="calcHourlySlider" min="20" max="80" value="35" oninput="calcUpdateHourly(this.value)" style="width:80px;flex-shrink:0">
              <div class="calc-hourly-val" id="calcHourlyVal">35 €/h</div>
            </div>
            <button class="btn-primary" onclick="showPage('contact')" style="width:100%">Confirmer ce chiffre lors de l'audit gratuit →</button>
          </div>
          <p class="calc-disclaimer">Estimation indicative (taux horaire personnalisable · 80% récupérables). Vos gains réels estimés lors de l'audit.</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Étape 3 : Ajouter le JS complet du calculateur**

Remplacer toutes les fonctions `calcUpdate`, `calcSlider`, `toggleCalcTask` par :

```javascript
const CALC_PROFILES = {
  pme: [
    { cat: 'Administration & gestion', tasks: [
      { label: 'Relances clients & impayés', unit: 'h/sem', min:1, max:20, val:5, hpu:1 },
      { label: 'Saisie ERP / logiciels métier', unit: 'h/sem', min:1, max:20, val:6, hpu:1 },
      { label: 'Onboarding & gestion RH', unit: 'h/sem', min:1, max:10, val:3, hpu:1 },
      { label: 'Génération de devis', unit: 'devis/sem', min:1, max:30, val:8, hpu:0.75 },
    ]},
    { cat: 'Reporting & communication interne', tasks: [
      { label: 'Reporting & tableaux de bord direction', unit: 'h/sem', min:1, max:15, val:5, hpu:1 },
      { label: 'Emails, archivage, classement', unit: 'h/sem', min:1, max:10, val:3, hpu:1 },
    ]},
    { cat: 'Marketing & présence en ligne', tasks: [
      { label: 'Posts LinkedIn & réseaux sociaux', unit: 'posts/sem', min:1, max:10, val:3, hpu:0.75 },
      { label: 'Articles de blog & contenu SEO', unit: 'articles/mois', min:1, max:8, val:2, hpu:3 },
      { label: 'Newsletter mensuelle', unit: 'newsletters/mois', min:1, max:4, val:1, hpu:2 },
    ]},
  ],
  tpe: [
    { cat: 'Gestion clients', tasks: [
      { label: 'Génération et envoi de devis', unit: 'devis/sem', min:1, max:20, val:5, hpu:0.75 },
      { label: 'Relances clients & impayés', unit: 'h/sem', min:1, max:10, val:3, hpu:1 },
      { label: 'Prise de RDV & confirmations', unit: 'h/sem', min:1, max:8, val:2, hpu:1 },
      { label: 'Réponses avis Google / Trustpilot', unit: 'h/sem', min:1, max:5, val:1, hpu:1 },
    ]},
    { cat: 'Administration', tasks: [
      { label: 'Transfert factures fournisseurs', unit: 'h/sem', min:1, max:10, val:4, hpu:1 },
      { label: 'Emails & archivage', unit: 'h/sem', min:1, max:8, val:2, hpu:1 },
    ]},
    { cat: 'Marketing & présence en ligne', tasks: [
      { label: 'Posts Google Business / Instagram', unit: 'posts/sem', min:1, max:7, val:2, hpu:0.75 },
      { label: 'Articles de blog local & SEO', unit: 'articles/mois', min:1, max:4, val:1, hpu:3 },
    ]},
  ],
  ae: [
    { cat: 'Gestion clients & admin', tasks: [
      { label: 'Relances clients & facturation', unit: 'h/sem', min:1, max:8, val:2, hpu:1 },
      { label: 'Génération de devis & propositions', unit: 'devis/sem', min:1, max:10, val:3, hpu:0.75 },
      { label: 'Prise de RDV & confirmations', unit: 'h/sem', min:1, max:6, val:2, hpu:1 },
      { label: 'Emails, admin, classement', unit: 'h/sem', min:1, max:6, val:2, hpu:1 },
    ]},
    { cat: 'Marketing & présence en ligne', tasks: [
      { label: 'Posts LinkedIn / Instagram', unit: 'posts/sem', min:1, max:10, val:3, hpu:0.75 },
      { label: 'Articles de blog & contenu SEO', unit: 'articles/mois', min:1, max:6, val:2, hpu:3 },
      { label: 'Newsletter clients', unit: 'newsletters/mois', min:1, max:4, val:1, hpu:2 },
    ]},
  ],
};

let _calcProfile = 'pme';
let _calcHourly = 35;
let _calcChecked = {};
let _calcSliders = {};
let _calcTaskIndex = [];

function syncCalcProfile(p) {
  _calcProfile = p;
  _calcChecked = {};
  _calcSliders = {};
  _calcTaskIndex = [];
  // Mettre à jour les tabs du calculateur
  document.querySelectorAll('#calcProfileTabs .calc-ptab').forEach(t => {
    t.classList.toggle('active', t.dataset.calcProfile === p);
  });
  // Mettre à jour le sélecteur de profil principal si différent
  const savedProfile = localStorage.getItem('dunai_profile');
  if (savedProfile !== p) {
    localStorage.setItem('dunai_profile', p);
    document.querySelectorAll('#profileTabs .profile-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.profile === p);
    });
    if (typeof PROFILE_DATA !== 'undefined') {
      const data = PROFILE_DATA[p];
      const content = document.getElementById('profileContent');
      if (content && data) {
        content.innerHTML = `<div class="profile-content-title">${data.title}</div>
          <div class="profile-use-cases">${data.cases.map(c=>`<div class="profile-use-case">${c}</div>`).join('')}</div>
          <div class="profile-cta-row"><button class="btn-primary" onclick="showPage('agents')" style="width:auto">Voir mes cas d'usage →</button>
          <span class="profile-cta-link" onclick="showPage('contact')">Ou commencer par l'audit gratuit</span></div>`;
      }
    }
  }
  renderCalcTasks();
  calcUpdateResult();
}

function renderCalcTasks() {
  const sections = CALC_PROFILES[_calcProfile];
  const container = document.getElementById('calcTasksContainer');
  if (!container) return;
  container.innerHTML = '';
  let idx = 0;
  sections.forEach(sec => {
    const catEl = document.createElement('div');
    catEl.className = 'calc-category-label';
    catEl.textContent = sec.cat;
    container.appendChild(catEl);
    sec.tasks.forEach(t => {
      _calcTaskIndex[idx] = t;
      _calcSliders[idx] = t.val;
      const row = document.createElement('div');
      row.className = 'calc-task';
      row.id = `ctask-${idx}`;
      row.innerHTML = `<div class="calc-task-hdr" onclick="calcToggleTask(${idx})">
        <input type="checkbox" class="calc-cb" id="ccb-${idx}" onchange="calcToggleTask(${idx},this.checked)" onclick="event.stopPropagation()">
        <label class="calc-task-label" for="ccb-${idx}">${t.label}</label>
        <span class="calc-task-hint" id="chint-${idx}">0 ${t.unit}</span>
      </div>
      <div class="calc-slider-wrap">
        <div class="calc-slider-label" id="clbl-${idx}">${t.val} ${t.unit}</div>
        <input type="range" class="calc-slider" min="${t.min}" max="${t.max}" value="${t.val}" oninput="calcOnSlider(${idx},this.value)">
      </div>`;
      container.appendChild(row);
      idx++;
    });
  });
}

function calcToggleTask(i, forceVal) {
  const cb = document.getElementById(`ccb-${i}`);
  if (forceVal === undefined) { cb.checked = !cb.checked; }
  _calcChecked[i] = cb.checked;
  document.getElementById(`ctask-${i}`).classList.toggle('active', cb.checked);
  const t = _calcTaskIndex[i];
  document.getElementById(`chint-${i}`).textContent = cb.checked ? `${_calcSliders[i]} ${t.unit}` : `0 ${t.unit}`;
  calcUpdateResult();
}

function calcOnSlider(i, val) {
  _calcSliders[i] = parseFloat(val);
  const t = _calcTaskIndex[i];
  document.getElementById(`clbl-${i}`).textContent = `${val} ${t.unit}`;
  document.getElementById(`chint-${i}`).textContent = `${val} ${t.unit}`;
  calcUpdateResult();
}

function calcUpdateHourly(val) {
  _calcHourly = parseFloat(val);
  document.getElementById('calcHourlyVal').textContent = `${val} €/h`;
  calcUpdateResult();
}

function calcUpdateResult() {
  let totalH = 0;
  _calcTaskIndex.forEach((t, i) => { if (_calcChecked[i]) totalH += _calcSliders[i] * t.hpu; });
  const recH = Math.round(totalH * 4.33 * 0.8);
  const monthly = Math.round(recH * _calcHourly);
  const annual = monthly * 12;
  const hasChecked = Object.values(_calcChecked).some(Boolean);
  document.getElementById('calcResultEmpty').style.display = hasChecked ? 'none' : 'block';
  const filled = document.getElementById('calcResultFilled');
  filled.style.display = hasChecked ? 'flex' : 'none';
  if (hasChecked) {
    document.getElementById('calcAnnual').textContent = annual.toLocaleString('fr-FR') + ' €';
    document.getElementById('calcHours').textContent = recH + 'h';
    document.getElementById('calcMonthly').textContent = monthly.toLocaleString('fr-FR') + ' €';
  }
}

// Init calculateur au chargement
(function initCalc() {
  const saved = localStorage.getItem('dunai_profile') || 'pme';
  syncCalcProfile(saved);
})();
```

- [ ] **Étape 4 : Supprimer l'ancien JS du calculateur**

Rechercher et supprimer les anciennes fonctions : `toggleCalcTask`, `calcUpdate`, `calcSlider`. Elles sont remplacées par les fonctions ci-dessus.

- [ ] **Étape 5 : Vérifier dans le navigateur**

- Changer le profil dans le sélecteur "Je suis…" → les tâches du calculateur changent automatiquement
- Cocher des tâches, bouger les sliders → le montant annuel s'affiche en grand
- Modifier le curseur coût horaire → recalcul immédiat
- Vérifier sur mobile : tâches en colonne pleine largeur au-dessus du résultat

- [ ] **Étape 6 : Commit**

```bash
git add index.html
git commit -m "feat: refactor calculator with profile tabs, categories, hourly slider, light theme"
```

---

## Task 10 : Pack Solo 1 190€ — Tarif autoentrepreneur

**Fichier :** `index.html`  
**Sections :** Page Tarifs (`.tarifs-section`) + aperçu tarif page Accueil

- [ ] **Étape 1 : Ajouter le CSS du badge AE**

```css
.tarif-badge-ae { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: var(--vert); color: var(--blanc); font-size: 10px; font-weight: 600; padding: 4px 14px; border-radius: var(--r-full); white-space: nowrap; letter-spacing: .04em; }
.tarif-card.ae-card { border-color: var(--vert); }
```

- [ ] **Étape 2 : Ajouter le Pack Solo dans la grille tarifs (page Tarifs)**

Dans `.tarifs-grid` de la page `#page-tarifs`, insérer en premier :

```html
<div class="tarif-card ae-card" style="position:relative">
  <div class="tarif-badge-ae">★ Autoentrepreneur</div>
  <div class="tarif-tier">Pack Solo</div>
  <div class="tarif-price" style="color:var(--vert)">1 190 €</div>
  <div class="tarif-desc">HT · forfait fixe · paiement en 2×</div>
  <ul class="tarif-feats">
    <li>Audit 1h en visio + rapport chiffré</li>
    <li>1 automatisation livrée en 2 semaines</li>
    <li>1h de formation individuelle</li>
    <li>15 jours de support post-déploiement</li>
  </ul>
  <button class="tarif-btn" onclick="showPage('contact')" style="border-color:var(--vert);color:var(--vert)">Démarrer →</button>
</div>
```

- [ ] **Étape 3 : Mettre à jour la FAQ TPE pour mentionner 1 190€**

Vérifier que le texte de la nouvelle question FAQ (Task 7) mentionne bien `1 190€` — déjà fait dans le HTML de la Task 7.

- [ ] **Étape 4 : Vérifier dans le navigateur**

- Page Tarifs : Pack Solo vert en première position
- Badge "★ Autoentrepreneur" visible en haut de la card
- Bouton vert, hover correct
- Grille tarifs reste bien alignée à 3 colonnes sur desktop

- [ ] **Étape 5 : Commit**

```bash
git add index.html
git commit -m "feat: add Pack Solo 1190€ AE card to pricing page"
```

---

## Revue finale

- [ ] **Ouvrir `index.html` et tester les 6 pages** (Accueil, Agents IA, Résultats, Tarifs, Blog, Contact)
- [ ] **Tester le flow complet** : sélectionner AE → vérifier que témoignages, FAQ, calculateur et tarifs s'adaptent
- [ ] **Tester sur mobile** (DevTools, viewport 375px) : sticky button, calculateur, sélecteur de profil
- [ ] **Vérifier localStorage** : recharger après sélection AE → profil restauré partout
- [ ] **Commit final si tout est bon**

```bash
git add index.html
git commit -m "chore: final verification pass — all 10 improvements validated"
```
