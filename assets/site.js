
function toggleMenu() {
  const menu = document.getElementById('mobileMenu'); const btn = document.getElementById('hamburger');
  const open = menu.classList.toggle('open'); btn.classList.toggle('open', open); btn.setAttribute('aria-expanded', String(open)); document.body.style.overflow = open ? 'hidden' : '';
}
function closeMenu() {
  document.getElementById('mobileMenu').classList.remove('open'); const btn = document.getElementById('hamburger'); btn.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = '';
}

const auditData = [
  { title:'Exemple : PME Logistique 18 salariés', findings:[{label:'Opportunité n°1',text:'Relances clients : 3h/sem passées à envoyer des emails de relance manuelle depuis Outlook',gain:'↑ Gain estimé : 3h/sem · ROI en 3 semaines'},{label:'Opportunité n°2',text:'Bons de livraison : saisie manuelle dans le TMS depuis des PDF reçus chaque matin',gain:'↑ Gain estimé : 1h30/jour · ROI en 5 semaines'},{label:'Opportunité n°3',text:'Reporting hebdo : 4h chaque vendredi à compiler des tableaux Excel depuis 3 sources',gain:'↑ Gain estimé : 4h/sem · ROI en 4 semaines'}], total:'+28h / mois'},
  { title:'Cartographie : PME Commerce 12 salariés', findings:[{label:'Flux A',text:'Commandes reçues par email → saisie manuelle dans le logiciel de gestion',gain:'↑ Volume : 40 commandes/sem · 20 min chacune = 13h/sem'},{label:'Flux B',text:'Confirmations de livraison saisies 2× (email + ERP), doublon chronophage',gain:'↑ Gain estimé : 3h/sem en automatisant la synchro'},{label:'Flux C',text:'Inventaire mensuel : comptage + Excel + mise à jour ERP = 2 jours',gain:'↑ Gain estimé : 1,5 jour/mois par automatisation'}], total:'+18h / mois'},
  { title:'Priorisation : Cabinet services 8 salariés', findings:[{label:'🔥 Impact fort · Faisabilité haute',text:'Automatisation devis (45 min → 3 min) · Intégration Make + GPT + envoi auto',gain:'↑ ROI estimé : 6 semaines · Gain : 12h/sem'},{label:'🟠 Impact moyen · Faisabilité haute',text:'Relances impayés : séquence auto J+30/60/90 · Stripe + Gmail',gain:'↑ ROI estimé : 3 semaines · Gain : 2h/sem'},{label:'🟡 Impact fort · Faisabilité moyenne',text:'Reporting mensuel : consolidation multi-sources + envoi dirigeants',gain:'↑ ROI estimé : 8 semaines · Gain : 4h/mois'}], total:'+14h / semaine'},
  { title:'Rapport final : Recommandations prioritaires', findings:[{label:'Action immédiate (sem. 1–2)',text:'Agent commercial : relances + devis. Intégration en 5 jours sur votre CRM.',gain:'↑ Gain immédiat : 12h/sem dès la 3e semaine'},{label:'Action court terme (mois 2)',text:'Agent administratif : factures + saisie ERP. Compatible Sage/Cegid.',gain:'↑ +8h/sem · 9 600€/an économisés'},{label:'Action moyen terme (mois 3–4)',text:'Agent reporting + dashboard dirigeants. Connexion à vos 3 sources.',gain:'↑ 4h libérées/sem · décisions plus rapides'}], total:'ROI estimé ×3 à ×4 sur 12 mois'}
];
function selectStep(el,idx) {
  document.querySelectorAll('.audit-step').forEach(s=>s.classList.remove('active')); el.classList.add('active');
  const d=auditData[idx]; document.getElementById('auditTitle').textContent=d.title;
  document.getElementById('auditFindings').innerHTML=d.findings.map(f=>`<div class="audit-finding"><div class="finding-lbl">${f.label}</div><div class="finding-txt">${f.text}</div><div class="finding-gain">${f.gain}</div></div>`).join('');
  document.getElementById('auditTotal').textContent=d.total;
}


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

// Accès localStorage sûr (navigation privée / stockage bloqué)
const store = {
  get(k){ try { return localStorage.getItem(k); } catch { return null; } },
  set(k,v){ try { localStorage.setItem(k,v); } catch {} }
};

function syncCalcProfile(p) {
  _calcProfile = p;
  _calcChecked = {};
  _calcSliders = {};
  _calcTaskIndex = [];
  document.querySelectorAll('#calcProfileTabs .calc-ptab').forEach(t => {
    t.classList.toggle('active', t.dataset.calcProfile === p);
  });
  store.set('dunai_profile', p);
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
      row.innerHTML = `<div class="calc-task-hdr">
        <input type="checkbox" class="calc-cb" id="ccb-${idx}" onchange="calcToggleTask(${idx},this.checked)">
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
  if (!document.getElementById('calcResultEmpty')) return;
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
  const saved = store.get('dunai_profile') || 'pme';
  syncCalcProfile(saved);
})();

// ── MINI CALCULATEUR (homepage) ──
// hpw = heures/semaine par défaut · max = borne haute du slider
const MC_DATA = {
  pme: [
    { label: 'Prospection commerciale & cold email', hpw: 6, max: 20 },
    { label: 'Qualification de leads & suivi CRM', hpw: 5, max: 15 },
    { label: 'Relances clients & impayés', hpw: 5, max: 15 },
    { label: 'Génération de devis', hpw: 8, max: 20 },
    { label: 'Accueil téléphonique & prise de messages', hpw: 8, max: 25 },
    { label: 'Service client & réponses aux demandes', hpw: 6, max: 20 },
    { label: 'Saisie ERP / logiciels métier', hpw: 6, max: 20 },
    { label: 'Emails, archivage, classement', hpw: 4, max: 15 },
    { label: 'Reporting & tableaux de bord direction', hpw: 5, max: 15 },
    { label: 'Veille concurrentielle & analyse marché', hpw: 3, max: 12 },
    { label: 'Onboarding & gestion RH', hpw: 3, max: 10 },
  ],
  tpe: [
    { label: 'Prospection & recherche de clients', hpw: 3, max: 12 },
    { label: 'Génération et envoi de devis', hpw: 4, max: 12 },
    { label: 'Relances clients & impayés', hpw: 3, max: 10 },
    { label: 'Répondre au téléphone & rappels clients', hpw: 5, max: 15 },
    { label: 'Prise de RDV & confirmations', hpw: 2, max: 8 },
    { label: 'Suivi commercial & relances devis', hpw: 3, max: 10 },
    { label: 'Transfert factures fournisseurs', hpw: 4, max: 12 },
    { label: 'Emails & archivage', hpw: 2, max: 10 },
    { label: 'Réponses avis Google / Trustpilot', hpw: 2, max: 6 },
    { label: 'Veille concurrence & prix du marché', hpw: 2, max: 8 },
  ],
  ae: [
    { label: 'Prospection & cold email / DM LinkedIn', hpw: 4, max: 12 },
    { label: 'Qualification de prospects & suivi', hpw: 2, max: 8 },
    { label: 'Relances clients & facturation', hpw: 2, max: 8 },
    { label: 'Génération de devis & propositions', hpw: 2, max: 8 },
    { label: 'Réponses messages & téléphone', hpw: 2, max: 8 },
    { label: 'Prise de RDV & confirmations', hpw: 2, max: 6 },
    { label: 'Emails, admin, classement', hpw: 2, max: 8 },
    { label: 'Posts LinkedIn / réseaux sociaux', hpw: 2, max: 8 },
    { label: 'Contenus & newsletter', hpw: 2, max: 6 },
    { label: 'Veille concurrentielle & marché', hpw: 2, max: 8 },
  ],
};
const MC_RATE = 35;     // €/h chargé
const MC_AUTO = 0.8;    // part automatisable
const MC_WPM = 4.33;    // semaines/mois
let _mcProfile = 'pme';
let _mcTask = null;

function mcSetProfile(p) {
  _mcProfile = p;
  document.querySelectorAll('.minicalc-ptab').forEach(t => t.classList.toggle('active', t.dataset.mcProfile === p));
  const sel = document.getElementById('mcTaskSelect');
  if (!sel) return;
  sel.innerHTML = '<option value="">Choisir une tâche...</option>';
  MC_DATA[p].forEach((t, i) => { const o = document.createElement('option'); o.value = i; o.textContent = t.label; sel.appendChild(o); });
  sel.value = '';
  _mcTask = null;
  mcReset();
}

function mcReset() {
  const slider = document.getElementById('mcSliderRow');
  const r = document.getElementById('mcResult');
  const e = document.getElementById('mcEmpty');
  if (slider) slider.style.display = 'none';
  if (r) r.style.display = 'none';
  if (e) e.style.display = 'block';
}

function mcOnSelect() {
  const sel = document.getElementById('mcTaskSelect');
  if (!sel || sel.value === '') { _mcTask = null; mcReset(); return; }
  _mcTask = MC_DATA[_mcProfile][parseInt(sel.value)];
  // configurer le slider sur la tâche choisie
  const slider = document.getElementById('mcSlider');
  slider.min = 1;
  slider.max = _mcTask.max;
  slider.value = _mcTask.hpw;
  document.getElementById('mcScaleMax').textContent = _mcTask.max + 'h';
  document.getElementById('mcSliderRow').style.display = 'flex';
  mcRender(_mcTask.hpw);
}

function mcOnSlider(val) { mcRender(parseFloat(val)); }

function mcRender(hpw) {
  // math explicite et cohérente
  const monthlyTotal = hpw * MC_WPM;                       // h/mois passées
  const monthlyRec = Math.round(monthlyTotal * MC_AUTO);   // h/mois récupérables
  const monthlyCost = Math.round(monthlyRec * MC_RATE);    // €/mois
  const annual = monthlyCost * 12;                         // €/an
  const annualHours = monthlyRec * 12;                     // h/an récupérables
  const days = Math.round(annualHours / 7);                // jours de travail (7h)

  // header
  document.getElementById('mcHpw').textContent = hpw;
  document.getElementById('mcAmount').textContent = annual.toLocaleString('fr-FR') + ' €';
  document.getElementById('mcHours').innerHTML = 'soit <strong>' + monthlyRec + 'h</strong> récupérables par mois';

  // détail
  document.getElementById('mcBdTime').textContent = hpw + ' h/sem · ~' + Math.round(monthlyTotal) + ' h/mois';
  document.getElementById('mcBdAuto').textContent = monthlyRec + ' h/mois récupérables';
  document.getElementById('mcBdMonthly').textContent = monthlyCost.toLocaleString('fr-FR') + ' €/mois';
  document.getElementById('mcBdAnnual').textContent = annual.toLocaleString('fr-FR') + ' €/an';

  // impact
  document.getElementById('mcImpact').innerHTML = '⏱️ <span>≈ <strong>' + days + ' jours</strong> de travail récupérés par an sur cette seule tâche.</span>';

  document.getElementById('mcEmpty').style.display = 'none';
  document.getElementById('mcResult').style.display = 'flex';
}

(function initMiniCalc() { mcSetProfile('pme'); })();

function toggleFaq(el) {
  const item=el.closest('.faq-item'); const isOpen=item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(i=>i.classList.remove('open'));
  if(!isOpen) item.classList.add('open');
}

const WEBHOOK_URL='https://n8n.dunai.fr/webhook/dunai-contact';
async function handleSubmit(arg) {
  // accepte un Event (onsubmit) ou le bouton (rétrocompat)
  const form = arg && arg.target && arg.target.closest ? arg.target.closest('.contact-form')
    : (arg && arg.closest ? arg.closest('.contact-form') : document.getElementById('auditForm'));
  if (arg && arg.preventDefault) arg.preventDefault();
  if (!form) return;
  const btn = form.querySelector('.field-submit');
  const val = id => { const el = form.querySelector('#'+id); return el ? el.value.trim() : ''; };
  const consent = form.querySelector('#rgpdConsent');
  const payload = {
    prenom: val('f-prenom'), nom: val('f-nom'), entreprise: val('f-entreprise'),
    email: val('f-email'), telephone: val('f-telephone'),
    secteur: form.querySelector('#f-secteur')?.value || '',
    taille: form.querySelector('#f-taille')?.value || '',
    message: val('f-message'),
    consentement: !!(consent && consent.checked),
    source: 'Site dunai.fr', date: new Date().toLocaleString('fr-FR')
  };
  const showErr = msg => { const e = form.querySelector('.form-error') || (()=>{const d=document.createElement('p');d.className='form-error';d.style.cssText='color:#DC2626;font-size:13px;margin-top:8px;';btn.parentNode.insertBefore(d,btn.nextSibling);return d;})(); e.innerHTML = msg; };
  if (!payload.email.includes('@') || !payload.entreprise) { showErr('⚠ Merci de renseigner votre email et le nom de votre entreprise.'); return; }
  if (!payload.consentement) { showErr('⚠ Merci d’accepter la politique de confidentialité pour être recontacté(e).'); return; }
  const prevErr = form.querySelector('.form-error'); if (prevErr) prevErr.remove();
  const original = btn.textContent;
  btn.textContent = 'Envoi en cours…'; btn.disabled = true;
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 12000);
  try {
    const response = await fetch(WEBHOOK_URL, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload), signal:ctrl.signal });
    if (!response.ok) throw new Error('HTTP '+response.status);
    btn.textContent = '✓ Demande reçue, on revient vers vous sous 24h !'; btn.style.background = '#16A34A';
    setTimeout(() => {
      form.querySelectorAll('.field-input,.field-textarea').forEach(el => el.value = '');
      form.querySelectorAll('.field-select').forEach(el => el.value = '');
      if (consent) consent.checked = false;
      btn.textContent = original; btn.style.background = ''; btn.disabled = false;
    }, 3000);
  } catch (err) {
    showErr('Erreur réseau, réessayez ou écrivez-nous à <a href="mailto:contact@dunai.fr" style="color:#DC2626;text-decoration:underline">contact@dunai.fr</a>.');
    btn.textContent = original; btn.disabled = false;
  } finally {
    clearTimeout(timer);
  }
}

(function initSticky() {
  const btn = document.getElementById('stickyCta');
  if (!btn) return;
  function updateSticky() {
    const onContact = document.getElementById('page-contact') &&
      document.getElementById('page-contact').classList.contains('active');
    const scrolled = window.scrollY > 300;
    btn.classList.toggle('visible', scrolled && !onContact);
    btn.setAttribute('aria-hidden', String(!(scrolled && !onContact)));
  }
  window.addEventListener('scroll', updateSticky, { passive: true });
  updateSticky();
})();

