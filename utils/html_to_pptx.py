import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from pptx import Presentation
from pptx.util import Inches

UTILS_DIR = Path(__file__).resolve().parent
WORKSPACE = UTILS_DIR.parent
HTML_PATH = WORKSPACE / "index.html"
PPTX_PATH = WORKSPACE / "presentation_pricing_v2.pptx"
SCRATCH_DIR = UTILS_DIR / "_tmp_slides_png"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def main():
    url = HTML_PATH.resolve().as_uri()
    slides_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_EXE, headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1.5)
        page.goto(url, wait_until="networkidle")

        # Hide web-only navigation controls and disable reveal animations
        page.add_style_tag(content="""
            .deck-controls, .nav-dots, .progress-bar { display: none !important; }
            .reveal, .reveal-d1, .reveal-d2, .reveal-d3 {
                opacity: 1 !important;
                transform: none !important;
                transition: none !important;
            }
            html, body { scroll-behavior: auto !important; }
        """)
        page.wait_for_timeout(400)

        slide_count = page.locator("section.slide").count()
        print(f"Detected {slide_count} slides in {HTML_PATH.name}", flush=True)

        for i in range(slide_count):
            slide = page.locator("section.slide").nth(i)
            # Scroll the slide cleanly into the 1920x1080 viewport
            page.evaluate(
                """(idx) => {
                    const el = document.querySelectorAll('section.slide')[idx];
                    el.classList.add('is-visible');
                    el.scrollIntoView({ behavior: 'instant', block: 'start' });
                }""",
                i,
            )
            page.wait_for_timeout(150)

            png_path = SCRATCH_DIR / f"slide_{i+1:02d}.png"
            page.screenshot(path=str(png_path), full_page=False)

            notes_text = slide.inner_text().strip()
            slides_data.append((png_path, notes_text))
            print(f"Captured slide {i+1:02d}/{slide_count:02d}", flush=True)

        browser.close()

    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for idx, (png_path, notes_text) in enumerate(slides_data, start=1):
        s = prs.slides.add_slide(blank_layout)
        s.shapes.add_picture(str(png_path), Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)
        notes_slide = s.notes_slide
        notes_slide.notes_text_frame.text = notes_text

    prs.save(str(PPTX_PATH))
    print(f"SAVED_PPTX: {PPTX_PATH} ({PPTX_PATH.stat().st_size} bytes)", flush=True)


if __name__ == "__main__":
    main()
