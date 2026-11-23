import shutil
import subprocess
from pathlib import Path
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

UTILS_DIR = Path(__file__).resolve().parent
WORKSPACE = UTILS_DIR.parent
EXPLAINER_HTML = UTILS_DIR / "demarche_explainer.html"
DECK_HTML = WORKSPACE / "index.html"
VIDEO_TMP_DIR = UTILS_DIR / "_tmp_video"
VIDEO_TMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_MP4 = WORKSPACE / "demarche_demo.mp4"
OUT_THUMB = WORKSPACE / "demarche_demo_thumb.png"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def inject_overlays(page):
    page.evaluate("""() => {
      if (!document.getElementById('demo-cursor')) {
        const cursor = document.createElement('div');
        cursor.id = 'demo-cursor';
        cursor.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 3L19 12L12 13L9 20L5 3Z" fill="white" stroke="black" stroke-width="1.5" stroke-linejoin="round"/>
        </svg>`;
        cursor.style.cssText = 'position:fixed;z-index:999999;pointer-events:none;width:24px;height:24px;transition:left 0.08s,top 0.08s;filter:drop-shadow(1px 1px 2px rgba(0,0,0,0.35));left:640px;top:360px;';
        document.body.appendChild(cursor);
        document.addEventListener('mousemove', e => {
          cursor.style.left = e.clientX + 'px';
          cursor.style.top = e.clientY + 'px';
        });
      }
      if (!document.getElementById('demo-subtitle')) {
        const bar = document.createElement('div');
        bar.id = 'demo-subtitle';
        bar.style.cssText = 'position:fixed;bottom:0;left:0;right:0;z-index:999998;text-align:center;padding:11px 24px;background:rgba(20,23,28,0.86);color:#F6F3EC;font-family:"Segoe UI",sans-serif;font-size:15px;font-weight:500;letter-spacing:0.2px;transition:opacity 0.25s;pointer-events:none;opacity:0;';
        document.body.appendChild(bar);
      }
    }""")


def set_subtitle(page, text: str):
    page.evaluate("""(t) => {
      const bar = document.getElementById('demo-subtitle');
      if (!bar) return;
      if (t) { bar.textContent = t; bar.style.opacity = '1'; }
      else { bar.style.opacity = '0'; }
    }""", text)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_EXE, headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(VIDEO_TMP_DIR),
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()

        # --- SCÈNES 1 à 5 : Explainer animé de la démarche ---
        page.goto(EXPLAINER_HTML.resolve().as_uri(), wait_until="networkidle")
        inject_overlays(page)

        # Scène 1
        set_subtitle(page, "Étape 1 - De 80 lignes d'offre à une feuille de route vérifiée")
        page.wait_for_timeout(1600)
        page.screenshot(path=str(OUT_THUMB))
        page.wait_for_timeout(3200)

        # Scène 2
        page.evaluate("window.showScene(2)")
        set_subtitle(page, "Étape 2 - Temps 1: 5 pistes Deep Recon sourcées en parallèle")
        page.wait_for_timeout(5200)

        # Scène 3
        page.evaluate("window.showScene(3)")
        set_subtitle(page, "Étape 3 - Temps 2: arbitrages BMad et PRD contrôlé ASD-STE100")
        page.wait_for_timeout(5200)

        # Scène 4
        page.evaluate("window.showScene(4)")
        set_subtitle(page, "Étape 4 - Temps 3: architecture AD-01..07 et 5 ateliers stress-test")
        page.wait_for_timeout(5200)

        # Scène 5
        page.evaluate("window.showScene(5)")
        set_subtitle(page, "Étape 5 - Boucle terrain: transcription Whisper de l'entretien réel")
        page.wait_for_timeout(5800)

        # --- SCÈNE 6 : Démo live du livrable final index.html ---
        page.goto(DECK_HTML.resolve().as_uri(), wait_until="networkidle")
        inject_overlays(page)
        page.evaluate("""() => {
          document.querySelectorAll('.reveal, .reveal-d1, .reveal-d2, .reveal-d3').forEach(el => {
            el.style.opacity = '1'; el.style.transform = 'none';
          });
        }""")
        set_subtitle(page, "Étape 6 - Livrable final: deck autonome 15 slides + export PowerPoint")
        page.wait_for_timeout(3000)

        # Navigation fluide vers Slide 5 (3 chantiers recalés)
        page.evaluate("document.querySelector('section[data-slide=\"5\"]').scrollIntoView({behavior:'smooth'})")
        set_subtitle(page, "Livrable recalé: logs ORTEC, Prophet/exogènes et campings jumeaux")
        page.wait_for_timeout(3600)

        # Navigation vers Slide 7 (Architecture simplifiée ASD-STE100)
        page.evaluate("document.querySelector('section[data-slide=\"7\"]').scrollIntoView({behavior:'smooth'})")
        set_subtitle(page, "Architecture simplifiée ASD-STE100: zéro jargon opaque à l'oral")
        page.wait_for_timeout(3200)

        # Bascule thème Dark Botanical puis retour Swiss Strategy
        dark_btn = page.locator("button[data-set-theme='luxury']").first
        box = dark_btn.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=12)
            page.wait_for_timeout(350)
            dark_btn.click()
            set_subtitle(page, "3 thèmes visuels intégrés + export PowerPoint 16:9 HD")
            page.wait_for_timeout(2000)

        swiss_btn = page.locator("button[data-set-theme='swiss']").first
        box2 = swiss_btn.bounding_box()
        if box2:
            page.mouse.move(box2["x"] + box2["width"] / 2, box2["y"] + box2["height"] / 2, steps=10)
            page.wait_for_timeout(250)
            swiss_btn.click()

        # Fin sur Slide 15 (Profil Caroline Heymes)
        page.evaluate("document.querySelector('section[data-slide=\"15\"]').scrollIntoView({behavior:'smooth'})")
        set_subtitle(page, "Prêt pour le débriefing équipe technique — Caroline Heymes")
        page.wait_for_timeout(3200)
        set_subtitle(page, "")
        page.wait_for_timeout(800)

        video_path = Path(page.video.path())
        context.close()
        browser.close()

    # Conversion WebM -> MP4 H.264 universel via imageio-ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe, "-y", "-i", str(video_path),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(OUT_MP4),
    ]
    subprocess.run(cmd, check=True)
    print(f"VIDEO_READY: {OUT_MP4} ({OUT_MP4.stat().st_size} bytes)", flush=True)
    print(f"THUMB_READY: {OUT_THUMB} ({OUT_THUMB.stat().st_size} bytes)", flush=True)


if __name__ == "__main__":
    main()
