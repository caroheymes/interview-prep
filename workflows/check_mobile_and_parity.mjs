import fs from 'node:fs';
import crypto from 'node:crypto';
import { chromium } from 'file:///C:/Users/Admin/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';

const fullPath = 'C:/Users/Admin/Documents/MALT/chateauform/presentation-chateauform-head-of-data.html';
const idxPath = 'C:/Users/Admin/Documents/MALT/chateauform/index.html';
const outDir = 'C:/Users/Admin/.gemini/antigravity-cli/brain/9fb953a3-eee2-4c64-97d4-5ba3ebd53cb0/scratch';

const fullHtml = fs.readFileSync(fullPath, 'utf8');
const oldIdxHtml = fs.readFileSync(idxPath, 'utf8');

const svgMatch = oldIdxHtml.match(/<svg id="archDiagramSvg"[\s\S]*?<\/svg>/);
if (!svgMatch) throw new Error('Could not find archDiagramSvg in index.html');
const inlineRedactedSvg = svgMatch[0];

function decodeEntities(str) {
  return str
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&middot;/g, '·')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

function hexStream(seed, needed) {
  let out = '';
  let counter = 0;
  while (out.length < needed) {
    out += crypto.createHash('sha256').update(`chateauform-teaser-v2::${seed}::${counter++}`).digest('hex');
  }
  return out.slice(0, needed);
}

const parityChecks = [];

function stripTagsToDecoded(htmlFrag) {
  return decodeEntities(htmlFrag.replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
}

function redactInnerHtml(htmlFragment, seedPrefix) {
  const parts = htmlFragment.split(/(<[^>]+>)/g);
  let blockIdx = 0;
  const out = parts
    .map((part) => {
      if (part.startsWith('<')) return part;
      if (!part) return '';
      const decoded = decodeEntities(part);
      const normalized = decoded.replace(/\s+/g, ' ');
      const hex = hexStream(`${seedPrefix}::${blockIdx++}::${normalized}`, normalized.length);
      let pos = 0;
      let res = '';
      for (const ch of normalized) {
        if (ch === ' ') res += ' ';
        else res += hex[pos++];
      }
      return res;
    })
    .join('');

  const origClean = stripTagsToDecoded(htmlFragment);
  const redClean = stripTagsToDecoded(out);
  parityChecks.push({
    id: seedPrefix,
    origLen: origClean.length,
    redLen: redClean.length,
    origWords: origClean.split(' ').map(w => w.length).join(','),
    redWords: redClean.split(' ').map(w => w.length).join(','),
  });
  return out;
}

const LOCK_BADGE = `<span class="redacted-lock" title="Contenu dévoilé en séance"><svg aria-hidden="true"><use href="#ico-lock"></use></svg><span>Dévoilé en séance</span></span>`;

function generateFinalIndexHtml() {
  let html = fullHtml;

  const teaserCss = `
    /* ===========================================
       PUBLIC TEASER MODE (SHA-256 + BLUR + LOCK)
       =========================================== */
    .arch-frame {
      position: relative;
    }
    .arch-frame svg {
      width: 100%;
      height: auto;
      max-height: min(52vh, 490px);
      display: block;
    }
    .zoom-modal svg {
      width: 94vw;
      height: auto;
      max-height: 86vh;
      display: block;
    }
    .redacted-p {
      position: relative;
      display: block;
      min-height: 1.85em;
    }
    .redacted-cell {
      position: relative;
      display: block;
      min-height: 1.65em;
    }
    .redacted-banner {
      position: relative;
    }
    .redacted-hash {
      font-family: var(--font-body);
      font-size: 0.92em;
      line-height: inherit;
      color: var(--ink-secondary);
      filter: blur(4.4px);
      opacity: 0.76;
      user-select: none;
      pointer-events: none;
    }
    .redacted-p > .redacted-hash,
    .redacted-cell > .redacted-hash {
      display: block;
    }
    .redacted-banner > .redacted-hash {
      display: inline;
    }
    .swiss-card.dark .redacted-hash {
      color: #d1d5db;
      opacity: 0.72;
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
      font-family: var(--font-mono);
      font-size: var(--small-size);
      font-weight: 600;
      color: var(--ink-primary);
      background: rgba(246, 245, 240, 0.94);
      border: 1px solid var(--line-soft);
      border-left: 2px solid var(--accent-signal);
      padding: 0.12rem 0.46rem;
      box-shadow: 0 2px 6px rgba(17, 24, 39, 0.08);
      white-space: nowrap;
      z-index: 2;
      pointer-events: none;
    }
    .redacted-banner > .redacted-lock {
      left: 62%;
    }
    .redacted-lock svg {
      width: 0.82em;
      height: 0.82em;
      color: var(--accent-signal);
      flex-shrink: 0;
    }
    .swiss-card.dark .redacted-lock {
      background: rgba(17, 24, 39, 0.92);
      color: #f9fafb;
      border-color: rgba(255, 255, 255, 0.24);
      border-left-color: #fca5a5;
    }
    .swiss-card.dark .redacted-lock svg {
      color: #fca5a5;
    }
    .arch-lock .redacted-lock {
      font-size: clamp(0.72rem, 1.05vw, 0.92rem);
      padding: 0.28rem 0.75rem;
      border-left-width: 3px;
      box-shadow: 0 4px 14px rgba(17, 24, 39, 0.14);
    }
    @media (max-height: 720px) {
      .arch-frame svg { max-height: 44vh; }
    }
    @media (max-height: 600px) {
      .arch-frame svg { max-height: 48vh; }
      .redacted-p { min-height: 1.5em; }
      .redacted-cell { min-height: 1.4em; }
    }
    @media (max-height: 440px) {
      .arch-frame svg { max-height: 52vh; }
      .redacted-p { min-height: 1.2em; }
      .redacted-cell { min-height: 1.15em; }
      .redacted-lock { font-size: 0.46rem; padding: 0.04rem 0.22rem; gap: 0.15rem; }
    }
    @media (max-width: 620px) {
      .redacted-p { min-height: 1.45em; }
      .redacted-cell { min-height: 1.45em; }
      .redacted-lock { font-size: 0.48rem; padding: 0.05rem 0.22rem; gap: 0.15rem; }
      .redacted-banner > .redacted-lock { left: 50%; top: 64%; }
      .td-redacted .redacted-lock {
        white-space: normal;
        text-align: center;
        line-height: 1.04;
        max-width: 96%;
        padding: 0.05rem 0.12rem;
        font-size: 0.42rem;
      }
      .td-redacted .redacted-lock svg { display: none; }
    }`;

  html = html.replace('  </style>', teaserCss + '\n  </style>');

  html = html.replace(
    '<body>',
    '<body>\n  <svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true"><symbol id="ico-lock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"></rect><path d="M8 11V7a4 4 0 0 1 8 0v4"></path></symbol></svg>'
  );
  html = html.replace(
    /<div class="zoom-modal" id="zoomModal"[\s\S]*?<\/div>\s*<\/div>/,
    `<div class="zoom-modal" id="zoomModal" role="dialog" aria-label="Schéma d'architecture agrandi">
    <div id="zoomSvgHost" style="position: relative; display: flex; align-items: center; justify-content: center;"></div>
    <div class="zoom-caption">Schéma détaillé dévoilé en séance &middot; Cliquer ou appuyer sur Échap pour fermer</div>
  </div>`
  );

  const chunks = html.split('<section class="slide');
  for (let s = 4; s <= 29; s++) {
    let slide = chunks[s];

    if (s === 6) {
      slide = slide.replace(
        /<img id="archDiagramImg"[^>]*\/>/,
        `${inlineRedactedSvg}\n            <div class="arch-lock">${LOCK_BADGE}</div>`
      );
      let bIdx = 0;
      slide = slide.replace(/<div class="banner-note">([\s\S]*?)<\/div>/g, (_, inner) => {
        const red = redactInnerHtml(inner.trim(), `s06-b${bIdx++}`);
        return `<div class="banner-note"><div class="redacted-cell"><span class="redacted-hash">${red}</span>${LOCK_BADGE}</div></div>`;
      });
    } else {
      let pIdx = 0;
      slide = slide.replace(/<p(\s+[^>]*)?>([\s\S]*?)<\/p>/g, (_, attrs = '', inner) => {
        const red = redactInnerHtml(inner.trim(), `s${s}-p${pIdx++}`);
        let newAttrs = attrs;
        if (/class="/.test(newAttrs)) {
          newAttrs = newAttrs.replace(/class="([^"]*)"/, 'class="$1 redacted-p"');
        } else {
          newAttrs += ' class="redacted-p"';
        }
        return `<p${newAttrs}><span class="redacted-hash">${red}</span>${LOCK_BADGE}</p>`;
      });

      let bIdx = 0;
      slide = slide.replace(
        /<div class="banner-note"([^>]*)>\s*(<strong>[\s\S]*?<\/strong>)\s*([\s\S]*?)\s*<\/div>/g,
        (_, attrs = '', strongLead, rest) => {
          const red = redactInnerHtml(rest.trim(), `s${s}-b${bIdx++}`);
          return `<div class="banner-note redacted-banner"${attrs}>${strongLead} <span class="redacted-hash">${red}</span>${LOCK_BADGE}</div>`;
        }
      );

      const keepClearCols = s === 27 ? 1 : 2;
      let rIdx = 0;
      slide = slide.replace(/<tbody>([\s\S]*?)<\/tbody>/g, (_, tbodyInner) => {
        const newTbody = tbodyInner.replace(/<tr>([\s\S]*?)<\/tr>/g, (__, trInner) => {
          let cIdx = 0;
          const newTr = trInner.replace(/<td(\s+[^>]*)?>([\s\S]*?)<\/td>/g, (___, tdAttrs = '', tdInner) => {
            cIdx++;
            if (cIdx <= keepClearCols) return `<td${tdAttrs}>${tdInner}</td>`;
            const red = redactInnerHtml(tdInner.trim(), `s${s}-r${rIdx}-c${cIdx}`);
            return `<td class="td-redacted"><div class="redacted-cell"><span class="redacted-hash">${red}</span>${LOCK_BADGE}</div></td>`;
          });
          rIdx++;
          return `<tr>${newTr}</tr>`;
        });
        return `<tbody>${newTbody}</tbody>`;
      });
    }

    chunks[s] = slide;
  }
  html = chunks.join('<section class="slide');

  html = html.replace('this.zoomImg = document.getElementById("zoomImg");', 'this.zoomHost = document.getElementById("zoomSvgHost");');
  html = html.replace('this.archImg = document.getElementById("archDiagramImg");', 'this.archSvg = document.getElementById("archDiagramSvg");');
  html = html.replace(
    /toggleZoom\(forceClose = false\) \{[\s\S]*?\n      \}/,
    `toggleZoom(forceClose = false) {
        if (!this.archSvg || !this.zoomHost) return;
        if (forceClose || this.zoomModal.classList.contains("open")) {
          this.zoomModal.classList.remove("open");
        } else {
          this.zoomHost.innerHTML = this.archTrigger.innerHTML;
          this.zoomModal.classList.add("open");
        }
      }`
  );

  return html;
}

const finalOutPath = `${outDir}/final-index.html`;
const finalHtml = generateFinalIndexHtml();
fs.writeFileSync(finalOutPath, finalHtml, 'utf8');

// 1. Assert 100% parity of character counts and word lengths
const mismatches = parityChecks.filter(c => c.origLen !== c.redLen || c.origWords !== c.redWords);
console.log(`Total redacted blocks checked: ${parityChecks.length}, mismatches: ${mismatches.length}`);
if (mismatches.length) {
  console.error(mismatches.slice(0, 5));
  process.exit(1);
}

// 2. Assert zero non-hex/space chars inside .redacted-hash text nodes
const hashContents = [...finalHtml.matchAll(/<span class="redacted-hash">([\s\S]*?)<\/span>/g)].map(m => m[1].replace(/<[^>]+>/g, ''));
const nonHex = hashContents.filter(txt => /[^0-9a-f ]/.test(txt));
console.log(`Redacted blocks with non-hex characters: ${nonHex.length}`);
if (nonHex.length) {
  console.error(nonHex[0]);
  process.exit(1);
}

// 3. Browser verification across 7 viewports + mobile screenshots
const browser = await chromium.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true,
});
const page = await browser.newPage();
await page.goto(`file:///${finalOutPath}`, { waitUntil: 'domcontentloaded' });
await page.addStyleTag({ content: '.reveal { opacity: 1 !important; transform: none !important; transition: none !important; }' });

const viewports = [
  [1920, 1080],
  [1440, 900],
  [1366, 768],
  [1280, 720],
  [1024, 600],
  [800, 430],
  [390, 844],
];

for (const [w, h] of viewports) {
  await page.setViewportSize({ width: w, height: h });
  const bad = await page.evaluate(() => {
    const res = [];
    document.querySelectorAll('.slide').forEach((sl, idx) => {
      const sc = sl.querySelector('.slide-content');
      const sb = sl.querySelector('.slide-body');
      if (sc.scrollHeight > sc.clientHeight + 2 || sc.scrollWidth > sc.clientWidth + 2 || (sb && sb.scrollHeight > sb.clientHeight + 2)) {
        res.push(`S${idx + 1}(sc:${sc.scrollHeight}/${sc.clientHeight})`);
      }
    });
    return res;
  });
  console.log(`Viewport ${w}x${h} overflows: ${bad.length ? bad.join(', ') : '0'}`);
}

await page.setViewportSize({ width: 390, height: 844 });
for (const s of [3, 4, 28]) {
  await page.evaluate((i) => document.querySelectorAll('.slide')[i].scrollIntoView({ behavior: 'instant' }), s);
  await page.waitForTimeout(50);
  await page.screenshot({ path: `${outDir}/mobile-s${String(s + 1).padStart(2, '0')}.png` });
}

await browser.close();
