#!/usr/bin/env node
/**
 * Anonymisation optionnelle + Caviardage cryptographique irreversible (SHA-256 + flou CSS + cadenas)
 * d'une presentation HTML pour publication publique dans `github/index.html`.
 *
 * Dissociation stricte:
 *   - `./index.html` (racine) reste 100% NON anonymise et 100% lisible en clair.
 *   - `./github/index.html` (sortie de ce script) est:
 *       1) Integralement anonymise de la slide 1 a 15 (via `--anonymize-map <json>`) et controle
 *          contre toute fuite nominative (`--forbid-terms <json>`).
 *       2) Irreversiblement verrouille a partir de `--start-slide` (defaut: 5):
 *          - Paragraphes (<p>), listes (<li>), bannières (.banner-note), KPIs (.kpi-val, .kpi-label),
 *            badges (.pill) et cellules de tableaux (colonnes > --keep-cols, defaut: 1) remplaces
 *            dans le DOM par un flux hexadecimal SHA-256 (texte source detruit du code HTML).
 *          - Suppression physique du bouton `[U] Mode seance`, du raccourci clavier `U` et de la
 *            lightbox plein ecran `#archLightbox`.
 *          - Floutage verrouille des schemas `.arch-plate` sur les slides verrouillees et blocage de
 *            l'extraction par impression PDF (`@media print`) sur les slides >= start-slide.
 *   - Zero dependance externe (Node.js standard uniquement).
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

function parseArgs(argv) {
  const opts = {
    input: 'index.html',
    output: path.join('github', 'index.html'),
    startSlide: 5,
    keepCols: 1,
    seed: path.basename(process.cwd()) || 'public-locked',
    keepSubtitle: false,
    anonymizeMapPath: null,
    forbidTermsPath: null,
  };

  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--input' && argv[i + 1]) opts.input = argv[++i];
    else if (arg === '--output' && argv[i + 1]) opts.output = argv[++i];
    else if (arg === '--start-slide' && argv[i + 1]) opts.startSlide = Math.max(1, parseInt(argv[++i], 10));
    else if (arg === '--keep-cols' && argv[i + 1]) opts.keepCols = Math.max(0, parseInt(argv[++i], 10));
    else if (arg === '--seed' && argv[i + 1]) opts.seed = argv[++i];
    else if (arg === '--keep-subtitle') opts.keepSubtitle = true;
    else if (arg === '--anonymize-map' && argv[i + 1]) opts.anonymizeMapPath = argv[++i];
    else if (arg === '--forbid-terms' && argv[i + 1]) opts.forbidTermsPath = argv[++i];
  }
  return opts;
}

function decodeEntities(str) {
  return str
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&middot;/g, '·')
    .replace(/&nbsp;/g, ' ')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&rsquo;/g, "'")
    .replace(/&lsquo;/g, "'")
    .replace(/&laquo;/g, '"')
    .replace(/&raquo;/g, '"')
    .replace(/&ge;/g, '>=')
    .replace(/&le;/g, '<=')
    .replace(/&rarr;/g, '->');
}

function hexStream(seedBase, seed, needed) {
  let out = '';
  let counter = 0;
  while (out.length < needed) {
    out += crypto.createHash('sha256').update(`${seedBase}::${seed}::${counter++}`).digest('hex');
  }
  return out.slice(0, needed);
}

function stripTagsToDecoded(htmlFrag) {
  return decodeEntities(htmlFrag.replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
}

function escapeRegExp(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Applique un dictionnaire de remplacements d'anonymisation uniquement hors balises `<script>` et `<style>`,
 * sur les noeuds texte et les attributs textuels (`title`, `alt`, `aria-label`).
 */
function applyAnonymizeMap(html, replacements) {
  if (!Array.isArray(replacements) || replacements.length === 0) return html;

  // Trier du motif le plus long au plus court pour eviter les remplacements partiels
  const sorted = [...replacements]
    .filter((item) => item && typeof item.from === 'string' && item.from.length > 0)
    .sort((a, b) => b.from.length - a.from.length)
    .map((item) => ({
      regex: new RegExp(item.regex ? item.from : escapeRegExp(item.from), item.flags || 'g'),
      to: String(item.to ?? ''),
    }));

  const replaceInText = (txt) => {
    let out = txt;
    for (const rule of sorted) {
      out = out.replace(rule.regex, rule.to);
    }
    return out;
  };

  // Isoler <style>...</style> et <script>...</script>
  const blocks = html.split(/(<style[\s\S]*?<\/style>|<script[\s\S]*?<\/script>)/gi);
  return blocks
    .map((chunk) => {
      if (/^<(style|script)\b/i.test(chunk)) return chunk;
      // Dans le HTML normal, traiter separement les balises et le texte entre balises
      return chunk
        .split(/(<[^>]+>)/g)
        .map((token) => {
          if (!token.startsWith('<')) return replaceInText(token);
          // Remplacer aussi dans alt="...", title="...", aria-label="..."
          return token.replace(/\b(alt|title|aria-label)="([^"]*)"/gi, (_, attr, val) => {
            return `${attr}="${replaceInText(val)}"`;
          });
        })
        .join('');
    })
    .join('');
}

const LOCK_BADGE = `<span class="redacted-lock" title="Contenu verrouillé (version publique)"><svg aria-hidden="true"><use href="#ico-lock"></use></svg><span>Verrouillé</span></span>`;

const ARCH_LOCK_BADGE = `<span class="redacted-lock redacted-lock-lg" title="Architecture verrouillée (version publique)"><svg aria-hidden="true"><use href="#ico-lock"></use></svg><span>Schéma verrouillé (présenté en entretien)</span></span>`;

const LOCK_SYMBOL_SVG = `<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true"><symbol id="ico-lock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"></rect><path d="M8 11V7a4 4 0 0 1 8 0v4"></path></symbol></svg>`;

const TEASER_CSS = `
    /* ===========================================
       PUBLIC LOCKED MODE (SHA-256 + BLUR + NO UNLOCK)
       =========================================== */
    .slide-locked-public {
      user-select: none !important;
      -webkit-user-select: none !important;
    }
    .redacted-p {
      position: relative;
      display: block;
      min-height: 1.85em;
    }
    .redacted-li {
      position: relative;
    }
    .redacted-cell {
      position: relative;
      display: block;
      min-height: 1.55em;
    }
    .redacted-banner {
      position: relative;
    }
    .redacted-hash {
      font-family: var(--font-body, system-ui, sans-serif);
      font-size: 0.92em;
      line-height: inherit;
      color: var(--text-secondary, var(--ink-secondary, #6b7280));
      filter: blur(5px);
      opacity: 0.72;
      user-select: none !important;
      pointer-events: none !important;
    }
    .pill > .redacted-hash,
    .kpi-val > .redacted-hash {
      filter: blur(4.2px);
    }
    .redacted-p > .redacted-hash,
    .redacted-cell > .redacted-hash {
      display: block;
    }
    .redacted-banner > .redacted-hash,
    .redacted-li > .redacted-hash {
      display: inline;
    }
    .redacted-lock {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.28rem;
      font-family: var(--font-mono, monospace);
      font-size: var(--small-size, 0.7rem);
      font-weight: 600;
      color: var(--text-primary, var(--ink-primary, #111315));
      background: var(--bg-surface-elevated, rgba(246, 245, 240, 0.95));
      border: 1px solid var(--border-subtle, rgba(17, 19, 21, 0.18));
      border-left: 2px solid var(--accent-primary, var(--accent-signal, #9A6B16));
      padding: 0.14rem 0.48rem;
      border-radius: 4px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.14);
      white-space: nowrap;
      z-index: 4;
      pointer-events: none !important;
    }
    .redacted-lock-lg {
      padding: 0.38rem 0.85rem;
      font-size: clamp(0.7rem, 0.9vw, 0.84rem);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.24);
    }
    .redacted-banner > .redacted-lock {
      left: 62%;
    }
    .redacted-lock svg {
      width: 0.85em;
      height: 0.85em;
      color: var(--accent-primary, var(--accent-signal, #9A6B16));
      flex-shrink: 0;
    }
    .arch-plate-locked {
      position: relative !important;
      pointer-events: none !important;
      user-select: none !important;
    }
    .arch-plate-locked img,
    .arch-plate-locked .arch-fallback {
      filter: blur(11px) grayscale(0.25) !important;
      opacity: 0.45 !important;
      pointer-events: none !important;
    }
    .teaser-badge,
    #teaserToggleBtn,
    #archLightbox {
      display: none !important;
    }
    .blur-target {
      filter: none !important;
      opacity: 1 !important;
    }
    @media (max-width: 620px) {
      .redacted-p, .redacted-cell { min-height: 1.45em; }
      .redacted-lock { font-size: 0.52rem; padding: 0.06rem 0.24rem; gap: 0.15rem; }
      .redacted-banner > .redacted-lock { left: 50%; top: 64%; }
      .td-redacted .redacted-lock svg { display: none; }
    }
    @media print {
      .slide-locked-public .slide-content > *:not(.eyebrow):not(.slide-title):not(.slide-footer) {
        display: none !important;
      }
      .slide-locked-public .slide-content::after {
        content: "Contenu stratégique verrouillé dans la version publique GitHub.";
        display: block;
        margin-top: 2rem;
        padding: 1.25rem;
        border: 1px solid #64748b;
        font-family: monospace;
        font-size: 1rem;
      }
    }`;

function redactHtml(fullHtml, opts, replacements) {
  const parityChecks = [];

  function redactInnerHtml(htmlFragment, seedPrefix) {
    const cleanText = stripTagsToDecoded(htmlFragment);
    if (!cleanText) return htmlFragment;

    const parts = htmlFragment.split(/(<[^>]+>)/g);
    let blockIdx = 0;
    const out = parts
      .map((part) => {
        if (part.startsWith('<')) return part;
        if (!part) return '';
        const decoded = decodeEntities(part);
        const normalized = decoded.replace(/\s+/g, ' ');
        const hex = hexStream(opts.seed, `${seedPrefix}::${blockIdx++}::${normalized}`, normalized.length);
        let pos = 0;
        let res = '';
        for (const ch of normalized) {
          if (ch === ' ') res += ' ';
          else res += hex[pos++];
        }
        return res;
      })
      .join('');

    const redClean = stripTagsToDecoded(out);
    parityChecks.push({
      id: seedPrefix,
      origLen: cleanText.length,
      redLen: redClean.length,
      origWords: cleanText.split(' ').map((w) => w.length).join(','),
      redWords: redClean.split(' ').map((w) => w.length).join(','),
    });
    return out;
  }

  // 0. Appliquer d'abord l'anonymisation globale sur tout le document
  let html = applyAnonymizeMap(fullHtml, replacements);

  // 1. Supprimer physiquement le bouton [U] Mode seance, les mentions [U] d'aide et la Lightbox HD
  html = html.replace(/<button\b[^>]*\bid="teaserToggleBtn"[^>]*>[\s\S]*?<\/button>/gi, '');
  html = html.replace(/\s*\|\s*\[U\]\s*mode\s+s[ée]ance/gi, '');
  html = html.replace(/<!--\s*Full-Screen Lightbox[\s\S]*?<\/div>\s*<\/div>/i, '');
  html = html.replace(/<div\b[^>]*\bid="archLightbox"[\s\S]*?<\/div>\s*<\/div>/i, '');

  // Neutraliser les gestionnaires JS de deverrouillage clavier `U` et clic lightbox
  html = html.replace(/this\.initTeasers\(\);/g, '/* public-locked: teasers disabled */');
  html = html.replace(/this\.initLightbox\(\);/g, '/* public-locked: lightbox disabled */');
  html = html.replace(/else\s+if\s*\(\s*e\.key\.toLowerCase\(\)\s*===\s*['"]u['"]\s*\)\s*\{[\s\S]*?\}/g, '');

  // 2. Injecter le CSS public verrouille avant la derniere balise </style>
  const lastStyleIdx = html.lastIndexOf('</style>');
  if (lastStyleIdx !== -1) {
    html = html.slice(0, lastStyleIdx) + TEASER_CSS + '\n  ' + html.slice(lastStyleIdx);
  }

  // 3. Injecter le symbole SVG cadenas juste apres <body...> (et retirer unlock-all-teasers si present)
  html = html.replace(/<body([^>]*)>/, (_, attrs = '') => {
    const cleanAttrs = attrs.replace(/\bunlock-all-teasers\b/g, '').replace(/\s+/g, ' ');
    return `<body${cleanAttrs}>\n  ${LOCK_SYMBOL_SVG}`;
  });

  // 4. Decouper par <section class="slide
  const splitToken = '<section class="slide';
  const chunks = html.split(splitToken);
  if (chunks.length <= 1) {
    throw new Error('Aucune slide detectee (<section class="slide...) dans le fichier source.');
  }

  // Sur les slides publiques (1 a startSlide - 1), retirer tout reliquat de flou .teaser-blur / .teaser-badge
  for (let s = 1; s < Math.min(opts.startSlide, chunks.length); s++) {
    let pubSlide = chunks[s];
    pubSlide = pubSlide.replace(/\bteaser-blur\b/g, '');
    pubSlide = pubSlide.replace(/\bblur-target\b/g, '');
    pubSlide = pubSlide.replace(/<span class="teaser-badge">[\s\S]*?<\/span>/g, '');
    pubSlide = pubSlide.replace(/\s*title="Cliquer pour dévoiler[^"]*"/g, '');
    chunks[s] = pubSlide;
  }

  // Sur les slides verrouillees (startSlide a N), detruire le texte exploitable dans le DOM
  for (let s = opts.startSlide; s < chunks.length; s++) {
    let slide = chunks[s];

    // Marquer la section comme verrouillee publiquement
    slide = slide.replace(/^([^"]*)"/, '$1 slide-locked-public"');
    slide = slide.replace(/\bteaser-blur\b/g, '');
    slide = slide.replace(/\bblur-target\b/g, '');
    slide = slide.replace(/<span class="teaser-badge">[\s\S]*?<\/span>/g, '');
    slide = slide.replace(/\s*title="Cliquer pour dévoiler[^"]*"/g, '');
    slide = slide.replace(/\s*id="archZoomTrigger"/g, '');
    slide = slide.replace(/cursor:\s*zoom-in;?/g, 'cursor: default;');

    // Verrouiller visuellement tout conteneur .arch-plate sur les slides >= startSlide (independant de l'imbrication)
    slide = slide.replace(/<span class="pill[^"]*">[\s\S]*?Plein [ée]cran[\s\S]*?<\/span>/gi, '');
    slide = slide.replace(
      /<div([^>]*\bclass="[^"]*\barch-plate\b[^"]*"[^>]*)>/g,
      (_, attrs) => {
        const updated = attrs.replace(/class="([^"]*)"/, 'class="$1 arch-plate-locked"');
        return `<div${updated}>${ARCH_LOCK_BADGE}`;
      }
    );

    // Caviarder tous les paragraphes <p>
    let pIdx = 0;
    slide = slide.replace(/<p(\s+[^>]*)?>([\s\S]*?)<\/p>/g, (match, attrs = '', inner) => {
      if (opts.keepSubtitle && /slide-subtitle/.test(attrs)) return match;
      if (!stripTagsToDecoded(inner)) return match;
      const red = redactInnerHtml(inner.trim(), `s${s}-p${pIdx++}`);
      let newAttrs = attrs;
      if (/class="/.test(newAttrs)) {
        newAttrs = newAttrs.replace(/class="([^"]*)"/, 'class="$1 redacted-p"');
      } else {
        newAttrs += ' class="redacted-p"';
      }
      return `<p${newAttrs}><span class="redacted-hash">${red}</span>${LOCK_BADGE}</p>`;
    });

    // Caviarder tous les elements de listes <li>
    let liIdx = 0;
    slide = slide.replace(/<li(\s+[^>]*)?>([\s\S]*?)<\/li>/g, (match, attrs = '', inner) => {
      if (!stripTagsToDecoded(inner)) return match;
      const red = redactInnerHtml(inner.trim(), `s${s}-li${liIdx++}`);
      return `<li${attrs} class="redacted-li"><span class="redacted-hash">${red}</span></li>`;
    });

    // Caviarder toutes les .banner-note (meme avec d'autres classes comme "banner-note reveal reveal-d3"),
    // sauf si marquees explicitement data-public-contact="true"
    let bIdx = 0;
    slide = slide.replace(
      /<div(\s+[^>]*\bclass="[^"]*\bbanner-note\b[^"]*"[^>]*)>([\s\S]*?)<\/div>/g,
      (match, attrs = '', inner) => {
        if (/data-public-contact="true"/.test(attrs)) return match;
        if (!stripTagsToDecoded(inner)) return match;
        const red = redactInnerHtml(inner.trim(), `s${s}-b${bIdx++}`);
        const updatedAttrs = attrs.replace(/class="([^"]*)"/, 'class="$1 redacted-banner"');
        return `<div${updatedAttrs}><span class="redacted-hash">${red}</span>${LOCK_BADGE}</div>`;
      }
    );

    // Caviarder les KPI boxes (.kpi-val et .kpi-label)
    let kIdx = 0;
    slide = slide.replace(
      /<div class="kpi-val">([\s\S]*?)<\/div>/g,
      (match, inner) => {
        if (!stripTagsToDecoded(inner)) return match;
        const red = redactInnerHtml(inner.trim(), `s${s}-kv${kIdx++}`);
        return `<div class="kpi-val"><span class="redacted-hash">${red}</span></div>`;
      }
    );
    slide = slide.replace(
      /<div class="kpi-label">([\s\S]*?)<\/div>/g,
      (match, inner) => {
        if (!stripTagsToDecoded(inner)) return match;
        const red = redactInnerHtml(inner.trim(), `s${s}-kl${kIdx++}`);
        return `<div class="kpi-label redacted-cell"><span class="redacted-hash">${red}</span>${LOCK_BADGE}</div>`;
      }
    );

    // Caviarder les cellules <td> au-dela de keepCols (defaut: 1 seule colonne d'identifiant conservee)
    let rIdx = 0;
    slide = slide.replace(/<tbody>([\s\S]*?)<\/tbody>/g, (_, tbodyInner) => {
      const newTbody = tbodyInner.replace(/<tr([^>]*)>([\s\S]*?)<\/tr>/g, (__, trAttrs = '', trInner) => {
        let cIdx = 0;
        const newTr = trInner.replace(/<td(\s+[^>]*)?>([\s\S]*?)<\/td>/g, (___, tdAttrs = '', tdInner) => {
          cIdx++;
          if (cIdx <= opts.keepCols) return `<td${tdAttrs}>${tdInner}</td>`;
          if (!stripTagsToDecoded(tdInner)) return `<td${tdAttrs}>${tdInner}</td>`;
          // Retirer les barres de score visuelles eventuelles avant hachage pour ne pas trahir les poids
          const cleanedTd = tdInner.replace(/<div class="score-bar-track">[\s\S]*?<\/div>\s*<\/div>/g, '');
          const red = redactInnerHtml(cleanedTd.trim(), `s${s}-r${rIdx}-c${cIdx}`);
          return `<td class="td-redacted"><div class="redacted-cell"><span class="redacted-hash">${red}</span>${LOCK_BADGE}</div></td>`;
        });
        rIdx++;
        return `<tr${trAttrs}>${newTr}</tr>`;
      });
      return `<tbody>${newTbody}</tbody>`;
    });

    // Caviarder les badges .pill restants dans les cartes (.tag-row) sur les slides verrouillees
    let pillIdx = 0;
    slide = slide.replace(
      /<div class="tag-row">([\s\S]*?)<\/div>/g,
      (_, tagInner) => {
        const newPills = tagInner.replace(
          /<span class="(pill[^"]*)">([\s\S]*?)<\/span>/g,
          (pm, pClass, pContent) => {
            if (!stripTagsToDecoded(pContent)) return pm;
            const red = redactInnerHtml(pContent.trim(), `s${s}-pill${pillIdx++}`);
            return `<span class="${pClass}"><span class="redacted-hash">${red}</span></span>`;
          }
        );
        return `<div class="tag-row">${newPills}</div>`;
      }
    );

    chunks[s] = slide;
  }

  html = chunks.join(splitToken);

  return { html, parityChecks, totalSlides: chunks.length - 1 };
}

function main() {
  const opts = parseArgs(process.argv);
  const inputPath = path.resolve(opts.input);
  const outputPath = path.resolve(opts.output);

  if (!fs.existsSync(inputPath)) {
    console.error(`Fichier source introuvable: ${inputPath}`);
    process.exit(1);
  }

  let replacements = [];
  if (opts.anonymizeMapPath && fs.existsSync(path.resolve(opts.anonymizeMapPath))) {
    const mapRaw = fs.readFileSync(path.resolve(opts.anonymizeMapPath), 'utf8');
    const parsed = JSON.parse(mapRaw);
    replacements = Array.isArray(parsed) ? parsed : (parsed.replacements || []);
  }

  let forbidTerms = [];
  if (opts.forbidTermsPath && fs.existsSync(path.resolve(opts.forbidTermsPath))) {
    const forbidRaw = fs.readFileSync(path.resolve(opts.forbidTermsPath), 'utf8');
    const parsed = JSON.parse(forbidRaw);
    forbidTerms = Array.isArray(parsed) ? parsed : (parsed.forbidden_terms || []);
  } else if (opts.anonymizeMapPath && fs.existsSync(path.resolve(opts.anonymizeMapPath))) {
    const mapRaw = JSON.parse(fs.readFileSync(path.resolve(opts.anonymizeMapPath), 'utf8'));
    if (Array.isArray(mapRaw.forbidden_terms)) {
      forbidTerms = mapRaw.forbidden_terms;
    }
  }

  const fullHtml = fs.readFileSync(inputPath, 'utf8');
  const { html, parityChecks, totalSlides } = redactHtml(fullHtml, opts, replacements);

  // Controle 1: Parite 100% des longueurs de caracteres et de mots sur tous les blocs caviardes
  const mismatches = parityChecks.filter((c) => c.origLen !== c.redLen || c.origWords !== c.redWords);
  if (mismatches.length > 0) {
    console.error(`Echec parite sur ${mismatches.length} bloc(s):`, mismatches.slice(0, 3));
    process.exit(1);
  }

  // Controle 2: Zero caractere non-hexadecimal dans les blocs .redacted-hash
  const hashContents = [...html.matchAll(/<span class="redacted-hash">([\s\S]*?)<\/span>/g)].map((m) =>
    m[1].replace(/<[^>]+>/g, '')
  );
  const nonHex = hashContents.filter((txt) => /[^0-9a-f ]/.test(txt));
  if (nonHex.length > 0) {
    console.error('Fuite de caracteres non-hexadecimaux detectee:', nonHex[0]);
    process.exit(1);
  }

  // Controle 3: Zero bouton de deverrouillage #teaserToggleBtn ou #archLightbox residuel
  if (html.includes('id="teaserToggleBtn"') || html.includes('id="archLightbox"')) {
    console.error('Echec verrouillage: #teaserToggleBtn ou #archLightbox encore present dans la sortie.');
    process.exit(1);
  }

  // Controle 4: Zero fuite des termes interdits (entreprise cible, partenaire, dirigeants, marques)
  const visibleHtml = html
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<script[\s\S]*?<\/script>/gi, '');
  const leakedTerms = [];
  for (const term of forbidTerms) {
    if (!term || typeof term !== 'string') continue;
    const re = new RegExp(`\\b${escapeRegExp(term)}\\b`, 'i');
    if (re.test(visibleHtml)) {
      leakedTerms.push(term);
    }
  }
  if (leakedTerms.length > 0) {
    console.error(`Fuite d'anonymisation detectee dans github/index.html sur les termes:`, leakedTerms);
    process.exit(1);
  }

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  if (fs.existsSync(outputPath)) {
    try {
      fs.unlinkSync(outputPath);
    } catch {
      // ignore if unlink not permitted; writeFileSync will attempt overwrite
    }
  }
  fs.writeFileSync(outputPath, html, 'utf8');

  console.log(
    JSON.stringify({
      status: 'OK',
      input: inputPath,
      output: outputPath,
      totalSlides,
      publicAnonymizedSlides: `1-${Math.min(opts.startSlide - 1, totalSlides)}`,
      lockedRedactedSlides: `${opts.startSlide}-${totalSlides}`,
      keepCols: opts.keepCols,
      redactedBlocks: parityChecks.length,
      anonymizationRulesApplied: replacements.length,
      forbiddenTermsChecked: forbidTerms.length,
      leakedTerms: 0,
      parityMismatches: 0,
      nonHexLeaks: 0,
    })
  );
}

main();
