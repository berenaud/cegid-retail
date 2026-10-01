/*
 * Cegid Retail tools · code commun à toutes les pages outils.
 * Chargé AVANT le script propre à chaque page :
 * (balise script avec src="../../shared/common.js" dans chaque page).
 * Contient : langue, échappement HTML, connexion Aha!, lecture du lien,
 * versions de la page et du skill (footer).
 */

// ---------- Langue et utilitaires ----------
const FR = navigator.language?.startsWith('fr');

function escHtml(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

// ---------- Aha! ----------
// Même clé pour tous les outils : le token n'est saisi qu'une fois.
const LS_TOKEN = 'cegid_aha_token';
const AHA_BASE = 'https://cegid.aha.io/api/v1';

async function ahaFetch(path, opts = {}) {
  const tok = localStorage.getItem(LS_TOKEN);
  const res = await fetch(`${AHA_BASE}${path}`, {
    ...opts,
    headers: { 'Authorization': `Bearer ${tok}`, 'Content-Type': 'application/json', 'Accept': 'application/json', ...(opts.headers || {}) },
  });
  if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.error || `HTTP ${res.status}`); }
  return res.json();
}

// ---------- Lecture du lien ----------
// #z=...    : JSON compressé (deflate brut) puis base64url
// #data=... : JSON en base64url, non compressé
// &c=...    : optionnel, CRC32 (hexadécimal) des données, pour détecter un lien abîmé
// Renvoie { data, key } (key = empreinte courte, pour détecter une double publication),
// { error: 'corrupt' } si le lien contient des données illisibles, ou null s'il n'en contient pas.
function crc32(str) {
  let c, crc = 0xFFFFFFFF;
  for (let i = 0; i < str.length; i++) {
    c = (crc ^ str.charCodeAt(i)) & 0xFF;
    for (let k = 0; k < 8; k++) c = c & 1 ? (c >>> 1) ^ 0xEDB88320 : c >>> 1;
    crc = (crc >>> 8) ^ c;
  }
  return ((crc ^ 0xFFFFFFFF) >>> 0).toString(16).padStart(8, '0');
}

async function shortKey(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].slice(0, 12).map(b => b.toString(16).padStart(2, '0')).join('');
}

// Données lues depuis un fichier JSON (repli quand le lien est abîmé)
async function payloadFromText(text) {
  try { return { data: JSON.parse(text), key: await shortKey(text) }; }
  catch { return { error: 'corrupt' }; }
}
function b64urlToBytes(s) {
  const b64 = decodeURIComponent(s).replace(/-/g,'+').replace(/_/g,'/').replace(/[^A-Za-z0-9+/]/g,'');
  const padded = b64 + '='.repeat((4 - b64.length % 4) % 4);
  return Uint8Array.from(atob(padded), c => c.charCodeAt(0));
}

async function decodeHashPayload() {
  try {
    const m = location.hash.match(/[#&](z|data)=([^&]+)/);
    if (!m) return null;
    const check = location.hash.match(/[#&]c=([0-9a-f]{8})/)?.[1];
    if (check && crc32(m[2]) !== check) return { error: 'corrupt' };
    const bytes = b64urlToBytes(m[2]);
    let text;
    if (m[1] === 'z') {
      const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
      text = await new Response(stream).text();
    } else {
      text = new TextDecoder('utf-8').decode(bytes);
    }
    return { data: JSON.parse(text), key: await shortKey(m[2]) };
  } catch (e) { console.error('Hash parse error:', e); return { error: 'corrupt' }; }
}

// ---------- Versions (footer) ----------
// Ex. berenaud.github.io/cegid-retail/aha/feature/
//   -> dépôt "berenaud/cegid-retail", dossier de l'outil "aha/feature"
const GH = (() => {
  const owner = location.hostname.match(/^([^.]+)\.github\.io$/)?.[1];
  const parts = location.pathname.split('/').filter(Boolean);
  if (!owner || parts.length < 2) return null;
  const repo = parts.shift();
  if (/\.html?$/.test(parts[parts.length - 1])) parts.pop();
  return { repo: `${owner}/${repo}`, dir: parts.join('/') };
})();
const REPO_BLOB = GH ? `https://github.com/${GH.repo}/blob/main` : 'https://github.com/berenaud/cegid-retail/blob/main';

const fmtDate = d => new Date(/^\d{4}-\d{2}-\d{2}$/.test(d) ? `${d}T00:00:00` : d).toLocaleDateString('fr-FR');
const lsVersionKey = () => `cegid_page_version_${GH ? GH.dir.replace(/\W/g, '_') : 'local'}`;

function renderPageVersion(v) {
  const el = document.getElementById('footer-page-version');
  el.textContent = '';
  if (!v) { el.textContent = FR ? 'hors GitHub' : 'outside GitHub'; return; }
  const a = document.createElement('a');
  a.href = v.url; a.target = '_blank'; a.rel = 'noopener';
  a.style.color = 'inherit';
  a.textContent = fmtDate(v.date);
  a.title = `Commit ${v.sha}`;
  el.appendChild(a);
}

// Version de la page = dernier commit ayant modifié sa page OU le code commun
async function loadPageVersion() {
  if (!GH) { renderPageVersion(null); return; }
  try {
    const cached = JSON.parse(localStorage.getItem(lsVersionKey()) || 'null');
    if (cached && Date.now() - cached.t < 10 * 60 * 1000) { renderPageVersion(cached); return; }
  } catch {}
  try {
    const paths = [`${GH.dir}/index.html`, 'shared'];
    const lists = await Promise.all(paths.map(p =>
      fetch(`https://api.github.com/repos/${GH.repo}/commits?path=${encodeURIComponent(p)}&per_page=1`)
        .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })));
    const c = lists.map(l => l[0]).filter(Boolean)
      .sort((a, b) => b.commit.committer.date.localeCompare(a.commit.committer.date))[0];
    if (!c) throw new Error('no commit');
    const v = { t: Date.now(), sha: c.sha.slice(0, 7), date: c.commit.committer.date, url: c.html_url };
    try { localStorage.setItem(lsVersionKey(), JSON.stringify(v)); } catch {}
    renderPageVersion(v);
  } catch { document.getElementById('footer-page-version').textContent = FR ? 'version indisponible' : 'version unavailable'; }
}

function refreshPageVersion() {
  try { localStorage.removeItem(lsVersionKey()); } catch {}
  document.getElementById('footer-page-version').textContent = '…';
  loadPageVersion();
}

// Version du skill : date "skill_updated" du lien, comparée au SKILL.md publié
// dans le dossier de l'outil (même site, pas d'appel externe).
async function renderSkillVersion(data, skillName) {
  const el    = document.getElementById('footer-skill-version');
  const d     = data?.skill_updated;
  const valid = typeof d === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(d);
  el.textContent = valid
    ? ` · Skill version ${fmtDate(d)}`
    : (FR ? ' · Skill version ancienne (non datée)' : ' · Skill version: old (undated)');
  try {
    const res = await fetch(new URL(`skill/${skillName}/SKILL.md`, location.href), { cache: 'no-cache' });
    if (!res.ok) return;
    const latest = (await res.text()).match(/^\s*updated:\s*["']?(\d{4}-\d{2}-\d{2})/m)?.[1];
    if (!latest || (valid && latest <= d)) return;
    const guide = `${REPO_BLOB}/${GH ? GH.dir : ''}/README.md#${FR ? 'installer-le-skill-dans-claude' : 'installing-the-skill-in-claude'}`;
    el.append(' · ');
    const a = document.createElement('a');
    a.href = guide; a.target = '_blank'; a.rel = 'noopener';
    a.style.color = 'var(--link)'; a.style.fontWeight = '600';
    a.textContent = FR ? `⚠ Nouvelle version du skill (${fmtDate(latest)}), mets-le à jour`
                       : `⚠ New skill version (${fmtDate(latest)}), please update`;
    el.appendChild(a);
  } catch {}
}
