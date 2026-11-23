import subprocess
from pathlib import Path
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

UTILS_DIR = Path(__file__).resolve().parent
WORKSPACE = UTILS_DIR.parent
CARTOON_HTML = UTILS_DIR / "cartoon_explainer.html"
VIDEO_TMP_DIR = UTILS_DIR / "_tmp_cartoon"
VIDEO_TMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_MP4 = WORKSPACE / "demarche_ecg_cartoon.mp4"
OUT_THUMB = WORKSPACE / "demarche_ecg_cartoon_thumb.png"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_EXE, headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(VIDEO_TMP_DIR),
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        page.goto(CARTOON_HTML.resolve().as_uri(), wait_until="networkidle")

        # Scene 1
        page.wait_for_timeout(1600)
        page.screenshot(path=str(OUT_THUMB))
        page.wait_for_timeout(4400)

        # Scenes 2 to 5
        for num, wait_ms in [(2, 6200), (3, 6200), (4, 6800), (5, 6400)]:
            page.evaluate(f"window.goScene({num})")
            page.wait_for_timeout(wait_ms)

        video_path = Path(page.video.path())
        context.close()
        browser.close()

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe, "-y", "-i", str(video_path),
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(OUT_MP4),
    ]
    subprocess.run(cmd, check=True)
    print(f"CARTOON_READY: {OUT_MP4} ({OUT_MP4.stat().st_size} bytes)", flush=True)
    print(f"THUMB_READY: {OUT_THUMB} ({OUT_THUMB.stat().st_size} bytes)", flush=True)


if __name__ == "__main__":
    main()
