# Dunai Site — Améliorations PME / TPE / Autoentrepreneur

**Date :** 2026-04-28  
**Fichier cible :** `index.html` (site mono-page)  
**Objectif :** Améliorer conversion, crédibilité et personnalisation pour les 3 profils cibles sans toucher à la structure existante.

---

## Contexte

Le site actuel est un SPA (single-page app) avec 6 vues : Accueil, Agents IA, Résultats, Tarifs, Blog, Contact. Il cible PME, TPE et autoentrepreneurs des Hauts-de-France mais parle à tous de façon générique. Trois problèmes identifiés :

1. **Conversion** — pas assez de demandes d'audit (CTA peu visible)
2. **Crédibilité** — témoignages anonymes, pas de preuve sociale forte
3. **Personnalisation** — un artisan seul ne se reconnaît pas autant qu'un dirigeant PME

---

## Périmètre

Améliorations ciblées dans `index.html` uniquement. Aucune nouvelle page, aucun changement de structure de navigation. Quelques ajouts JavaScript dans le fichier existant.

---

## Changements approuvés

### 1. Hero — Mention des 3 profils + téléphone dans la nav

**Fichier :** `index.html` — section `.hero` + `nav`

- Ajouter dans la `nav` un numéro de téléphone visible (`📞 06 46 89 08 87`) à côté du bouton CTA, visible sur desktop
- Ajouter juste sous le H1 du hero 3 pills de profil :
  ```
  [• Dirigeant PME]  [• Gérant TPE]  [• Autoentrepreneur]
  ```
  Style : `display:inline-flex`, fond transparent, bordure `rgba(255,255,255,0.15)`, couleur `rgba(255,255,255,0.6)`, point orange flamme

**Pourquoi :** Le visiteur identifie immédiatement que le site lui parle, sans lire le texte intégral.

---

### 2. Section "Je suis…" — Sélecteur de profil (NOUVEAU)

**Emplacement :** Juste après la section Hero, avant la section "Urgence" actuelle

**Structure :**
- Eyebrow : "Personnalisez votre expérience"
- Titre : "Quelle situation vous ressemble le plus ?"
- 3 tabs cliquables : 🏢 PME (10–50 sal.) / 🔧 TPE (2–9 sal.) / 🧑‍💻 Autoentrepreneur (Seul·e)
- Contenu du tab : liste de 4 cas d'usage adaptés au profil + CTA "Voir mes cas d'usage →"

**Comportement JS :**
- Clic sur un tab → change le contenu de la section
- Le profil sélectionné est mémorisé en `localStorage` sous la clé `dunai_profile`
- Les sections concernées par l'adaptation dynamique :
  - Témoignages (section `.temo-section`) : filtrage par profil
  - FAQ (section `.faq-section`) : mise en avant des questions du profil
  - Tarifs (section `.tarifs-section`) : mise en avant du bon pack

**Contenu par profil :**

| PME | TPE | Autoentrepreneur |
|-----|-----|-----------------|
| Reporting direction auto chaque lundi | Devis générés en 3 min au lieu de 45 | 8h/semaine récupérées sans embaucher |
| Saisie ERP à 0 min/jour | Relances impayés sans y penser | Relances clients 100% automatiques |
| Onboarding RH automatisé | Prise de RDV + confirmations auto | Facturation et suivi auto |
| Rapport mensuel chiffré sans Excel | Transfert factures fournisseurs | Posts réseaux sociaux générés |

---

### 3. Bouton flottant sticky (NOUVEAU)

**Emplacement :** Fixe en bas de page, toutes vues

**Comportement :**
- Apparaît après 300px de scroll
- Disparaît quand la section `#page-contact` est active
- Contenu : texte "L'audit est gratuit et sans engagement." + bouton "Audit gratuit →" + `📞 06 46 89 08 87` en dessous
- Style : `background: #1C1917`, `border-radius: 99px` sur le bouton, couleur flamme

---

### 4. Barre de logos outils (AMÉLIORÉ + REMONTÉ)

**Emplacement :** Juste après le sélecteur de profil (avant "Pourquoi Dunai"), remplace la position actuelle de la section "Stack" en bas de page

**Style :** Pills simples dans le style `.stack-pill` existant — fond blanc, bordure grise, texte anthracite. Pas d'emojis, pas de catégories.

**Outils affichés (par ordre de reconnaissance) :**
```
Excel · Google Sheets · Outlook · Gmail · Google Drive · Teams
HubSpot · Pipedrive · Salesforce · Sellsy
Sage · Cegid · EBP · SAP
Pennylane · Stripe · Docusign
+ votre outil →
```

**Message :** "Fonctionne avec vos outils du quotidien — vous gardez ce que vous utilisez déjà."

**Note :** La section "Stack" actuelle (avec n8n, Make, Claude AI…) reste en bas de page pour les profils techniques.

---

### 5. Compteurs animés (NOUVEAU)

**Emplacement :** Dans la section "Urgence" actuelle, ou juste après la barre de logos

**4 compteurs :**
- `32+` audits réalisés en Hauts-de-France
- `18` PME & TPE accompagnées
- `+2 400h` récupérées par nos clients
- `×3,2` ROI moyen à 12 mois

**Animation :** Compteur qui s'incrémente au scroll (Intersection Observer + `requestAnimationFrame`)

**⚠️ Pas encore de chiffres clients réels disponibles.** Remplacer les compteurs par des formulations basées sur les résultats par déploiement :
- "Dès le 1er déploiement" / "+28h/mois récupérées en moyenne" / "×3 ROI à 12 mois" / "6 semaines pour vos premiers gains"
- Ou afficher les compteurs uniquement quand le volume client le justifie (seuil recommandé : 5+ clients).

---

### 6. Témoignages — Tabs par profil + badge secteur (AMÉLIORÉ)

**Section :** `.temo-section`

**Changements :**
- Ajouter 4 tabs au-dessus des cards : Tous / PME / TPE·Artisan / Autoentrepreneur
- Ajouter un badge secteur visible sur chaque card (ex : "Transport · PME", "BTP · Artisan", "Médical · Cabinet")
- Déplacer le gain (résultat chiffré) en badge vert **avant** la citation, pas après
- Le filtre par tab correspond au champ `dunai_profile` en localStorage si déjà sélectionné

---

### 7. FAQ — 3 nouvelles objections par profil (AMÉLIORÉ)

**Section :** `.faq-section`

**Nouvelles questions à ajouter :**

1. **[AE]** "Je travaille seul — 'vos équipes libérées' ne me parle pas vraiment."  
   → Réponse : expliquer que c'est le temps du dirigeant solo qu'on libère, moyenne 8h/semaine.

2. **[TPE]** "2 990€ c'est beaucoup pour une petite structure comme la mienne."  
   → Réponse : rappeler la validation ROI avant démarrage + paiement en 3× + Pack Solo 1 190€.

3. **[PME]** "Mon équipe va résister au changement."  
   → Réponse : les agents retirent les tâches ennuyeuses, les équipes ne veulent pas revenir en arrière.

Ajouter un petit badge coloré devant chaque question pour signaler le profil concerné (AE / TPE / PME / Tous).

---

### 8. Badge "Satisfait ou remboursé 30 jours" (AMÉLIORÉ)

**Emplacements :** 
1. Dans la section `.garantie-section` existante — ajouter le badge vert après le texte de la 3e garantie
2. Juste au-dessus du formulaire de contact — en petite ligne rassurante

**Style :** Badge vert `#16a34a`, texte blanc, icône `✓`, texte "Satisfait ou remboursé 30 jours"

---

### 9. Calculateur — Refonte complète (AMÉLIORÉ)

**Section :** `.calc-section`

**Changements :**

**A — € en premier**
- Résultat principal : "Vous perdez chaque année **X €**" (montant annuel, 42px, couleur flamme, fond sombre pour contraste)
- En secondaire : heures récupérables / économies mensuelles
- CTA : "Confirmer ce chiffre lors de l'audit gratuit →"

**B — Profil connecté au sélecteur**
- 3 tabs en haut du calculateur (PME / TPE / Autoentrepreneur), synchronisés avec `dunai_profile` en localStorage
- Les tâches affichées changent selon le profil sélectionné

**C — Tâches par profil avec catégories**

| Profil | Catégories | Tâches |
|--------|-----------|--------|
| PME | Administration & gestion | Relances, saisie ERP, RH, devis |
| PME | Reporting & com. interne | Reporting direction, emails/archivage |
| PME | Marketing & présence en ligne | Posts LinkedIn, articles blog SEO, newsletter |
| TPE | Gestion clients | Devis, relances, RDV, réponses avis Google |
| TPE | Administration | Factures fournisseurs, emails |
| TPE | Marketing & présence en ligne | Posts Google Business/Instagram, articles blog local |
| AE | Gestion clients & admin | Relances/facturation, devis, RDV, emails |
| AE | Marketing & présence en ligne | Posts LinkedIn/Instagram, articles blog SEO, newsletter |

**D — Curseur coût horaire personnalisable**
- Slider 20–80 €/h (défaut : 35 €/h) — un AE à 80€/h voit un ROI bien plus fort
- Recalcul en temps réel

**E — Thème clair**
- Fond blanc pour l'ensemble du calculateur
- Seul le bloc résultat principal garde un fond sombre (#1C1917) pour faire ressortir le montant

---

### 10. Pack Solo 1 190€ — Tarif autoentrepreneur (NOUVEAU)

**Section :** `.tarifs-section` + aperçu tarif sur la page Accueil

**Nouveau pack à ajouter :**

| Champ | Valeur |
|-------|--------|
| Nom | Pack IA Déclic Solo |
| Cible | Autoentrepreneur / Micro-entreprise |
| Prix | 1 190 € HT |
| Badge | "★ Autoentrepreneur" (vert) |
| Contenu | Audit 1h en visio + rapport · 1 automatisation livrée · 1h formation individuelle · 15 jours support |
| Paiement | En 2× disponible |

**Position dans la grille tarifs :** En première card (avant le pack PME existant)

**Raison :** 2 990€ fait fuir les autoentrepreneurs. 1 190€ avec un livrable concret en 2 semaines est accessible et crée un premier lien client — souvent la porte d'entrée vers le pack PME si la structure grandit.

---

## Récapitulatif des changements

| # | Changement | Type | Impact principal |
|---|-----------|------|-----------------|
| 1 | Pills profil dans hero + téléphone nav | Amélioré | Personnalisation |
| 2 | Sélecteur de profil "Je suis…" | Nouveau | Personnalisation |
| 3 | Bouton flottant sticky | Nouveau | Conversion |
| 4 | Barre logos bureautiques remontée | Amélioré | Crédibilité |
| 5 | Compteurs animés | Nouveau | Crédibilité |
| 6 | Témoignages avec tabs + badges secteur | Amélioré | Crédibilité |
| 7 | FAQ enrichie — 3 objections profils | Amélioré | Conversion |
| 8 | Badge "Satisfait ou remboursé" | Amélioré | Crédibilité |
| 9 | Calculateur — € en premier | Amélioré | Conversion |
| 10 | Pack Solo 1 190€ pour AE | Nouveau | Conversion AE |

---

## Contraintes techniques

- Tout reste dans `index.html` — pas de nouveau fichier HTML
- JavaScript inline dans `<script>` en bas de page (pattern existant)
- Le profil sélectionné est persisté en `localStorage` — pas de backend
- Les compteurs utilisent `IntersectionObserver` (compatible tous navigateurs modernes)
- Aucune dépendance externe à ajouter
