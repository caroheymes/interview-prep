import json
import os
import sys
import time
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent
SCRATCH_DIR = Path(r"C:\Users\Admin\.gemini\antigravity-cli\brain\a4a71dbe-21d4-4830-886a-122062d75a34\scratch")

AUDIO_PATH = sys.argv[1] if len(sys.argv) > 1 else str(WORKSPACE_DIR / "entretien.mp4")
MODEL_MEDIUM = r"C:\Users\Admin\.cache\huggingface\hub\models--Systran--faster-whisper-medium\snapshots\08e178d48790749d25932bbc082711ddcfdfbc4f"

OUT_WORKSPACE_JSON = WORKSPACE_DIR / "whisper_raw_segments.json"
OUT_WORKSPACE_TXT = WORKSPACE_DIR / "whisper_raw.txt"
OUT_SCRATCH_JSON = SCRATCH_DIR / "whisper_raw_segments.json"
OUT_SCRATCH_TXT = SCRATCH_DIR / "whisper_raw.txt"

INITIAL_PROMPT = (
    "Entretien de recrutement Data Scientist Senior Pricing et Revenue Management chez "
    "European Camping Group (ECG) avec Hugo Rannou, Noélie et Caroline Heymes. "
    "Termes techniques: Resalys, BigQuery, architecture médaillon, ORTEC, Homair, Eurocamp, "
    "yield management, ancillaries, F&B, Omnibus, TVA, A/B test, clustering, XGBoost, "
    "Random Forest, Prophet, time series, booking pace, pick-up, data drift, concept drift, "
    "voicebot, call center, Interflora, Centrale Lyon, EM Lyon."
)


def register_cuda_dlls() -> list[str]:
    added = []
    nvidia_site = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
    if nvidia_site.exists():
        for bin_dir in nvidia_site.glob("*/bin"):
            if bin_dir.is_dir():
                dll_dir = str(bin_dir)
                if dll_dir not in added:
                    os.add_dll_directory(dll_dir)
                    os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")
                    added.append(dll_dir)

    candidates = [
        Path(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"),
        Path(r"C:\Program Files\NVIDIA"),
    ]
    for root in candidates:
        if not root.exists():
            continue
        try:
            for dll in root.rglob("cublas64_*.dll"):
                dll_dir = str(dll.parent)
                if dll_dir not in added:
                    os.add_dll_directory(dll_dir)
                    os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")
                    added.append(dll_dir)
            for dll in root.rglob("cudnn_ops*.dll"):
                dll_dir = str(dll.parent)
                if dll_dir not in added:
                    os.add_dll_directory(dll_dir)
                    os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")
                    added.append(dll_dir)
        except Exception:
            pass
    return added


def fmt_ts(seconds: float) -> str:
    s = int(round(seconds))
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"


def load_pipeline():
    import av
    from faster_whisper import BatchedInferencePipeline, WhisperModel

    _orig_av_open = av.open

    def _compat_av_open(*args, **kwargs):
        try:
            return _orig_av_open(*args, **kwargs)
        except TypeError:
            kwargs.pop("metadata_errors", None)
            return _orig_av_open(*args, **kwargs)

    av.open = _compat_av_open

    dll_dirs = register_cuda_dlls()
    has_cublas = any((Path(d) / "cublas64_12.dll").exists() for d in dll_dirs)
    if has_cublas:
        print(f"DLL CUDA 12 détectées ({dll_dirs}) -> exécution sur GPU NVIDIA T600 (int8_float16, batch_size=4)", flush=True)
        model = WhisperModel(MODEL_MEDIUM, device="cuda", compute_type="int8_float16")
        return BatchedInferencePipeline(model=model), "cuda", 4

    print("Aucune DLL cublas64_12.dll détectée -> exécution sur CPU (int8, 14 threads)...", flush=True)
    model = WhisperModel(MODEL_MEDIUM, device="cpu", compute_type="int8", cpu_threads=14)
    return BatchedInferencePipeline(model=model), "cpu", 8


def save_outputs(segments_out: list[dict], lines_out: list[str]) -> str:
    json_payload = json.dumps(segments_out, ensure_ascii=False, indent=2)
    txt_payload = "\n".join(lines_out) + ("\n" if lines_out else "")
    written_target = str(OUT_SCRATCH_TXT)
    if SCRATCH_DIR.exists():
        OUT_SCRATCH_JSON.write_text(json_payload, encoding="utf-8")
        OUT_SCRATCH_TXT.write_text(txt_payload, encoding="utf-8")
    try:
        OUT_WORKSPACE_JSON.write_text(json_payload, encoding="utf-8")
        OUT_WORKSPACE_TXT.write_text(txt_payload, encoding="utf-8")
        written_target = str(OUT_WORKSPACE_TXT)
    except PermissionError:
        pass
    return written_target


def main():
    t0 = time.time()
    pipeline, device, batch_size = load_pipeline()
    t_load = time.time()
    print(f"Modèle chargé en {t_load - t0:.1f}s sur {device}. Démarrage de la transcription...", flush=True)

    segments_gen, info = pipeline.transcribe(
        AUDIO_PATH,
        language="fr",
        batch_size=batch_size,
        beam_size=5,
        without_timestamps=False,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=False,
        initial_prompt=INITIAL_PROMPT,
    )
    print(f"Durée audio: {info.duration:.1f}s (après VAD: {info.duration_after_vad:.1f}s)", flush=True)

    segments_out = []
    lines_out = []
    for idx, seg in enumerate(segments_gen, start=1):
        text = seg.text.strip()
        if not text:
            continue
        item = {
            "id": idx,
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "start_ts": fmt_ts(seg.start),
            "end_ts": fmt_ts(seg.end),
            "text": text,
        }
        segments_out.append(item)
        lines_out.append(f"[{item['start_ts']} -> {item['end_ts']}] {text}")
        if idx % 50 == 0:
            save_outputs(segments_out, lines_out)
            elapsed = time.time() - t_load
            speed = seg.end / max(elapsed, 0.1)
            print(
                f"Segment {idx} | Position audio: {fmt_ts(seg.end)} / {fmt_ts(info.duration)} "
                f"| Temps écoulé: {elapsed:.1f}s | Vitesse: {speed:.1f}x temps réel",
                flush=True,
            )

    final_target = save_outputs(segments_out, lines_out)
    total_elapsed = time.time() - t0
    print(
        f"TERMINÉ: {len(segments_out)} segments écrits en {total_elapsed:.1f}s -> {final_target}",
        flush=True,
    )


if __name__ == "__main__":
    main()
