from pathlib import Path
import subprocess
import json
import tempfile
import re
import shlex

ROOT = Path(".")
OUT_DIR = ROOT / "demos"
OUT_DIR.mkdir(exist_ok=True)

EMOJI_DIR = ROOT / "emoji"

ORDER = [
    "alpha_pos0.0.wav",
    "alpha_pos10.0.wav",
    "alpha_neg10.0.wav",
]

MOODS = {
    "alpha_pos0.0.wav": {
        "label": "neutral",
        "emoji_path": EMOJI_DIR / "neutral.png",
    },
    "alpha_pos10.0.wav": {
        "label": "positive steering",
        "emoji_path": EMOJI_DIR / "euphoric.png",
    },
    "alpha_neg10.0.wav": {
        "label": "negative steering",
        "emoji_path": EMOJI_DIR / "melancholic.png",
    },
}

VIDEO_W = 1920
VIDEO_H = 1080
WAVE_W = 1920
WAVE_H = 620
WAVE_Y_OFFSET = 230
FPS = 60

BACKGROUND_COLOR = "000000"
WAVE_COLOR = "00E5FF"

# Transparent text overlay area, centered
LABEL_W = 1600
LABEL_H = 220
LABEL_X = (VIDEO_W - LABEL_W) // 2
LABEL_Y = 350

TEXT_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
TEXT_FONT_SIZE = 90

# Emoji on its own centered line
EMOJI_SIZE = 135
EMOJI_X = (VIDEO_W - EMOJI_SIZE) // 2
EMOJI_Y = LABEL_Y + 170


def run(cmd):
    print(" ".join(shlex.quote(str(c)) for c in cmd))
    subprocess.run(cmd, check=True)


def ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def clean_folder_name(folder_name: str) -> str:
    name = re.sub(r"^\d+_", "", folder_name)
    name = name.replace("_", " ")
    return name


def make_concat_audio(files: list[Path], output_path: Path):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        concat_list = Path(f.name)

        for wav in files:
            f.write(f"file '{wav.resolve()}'\n")

    try:
        run([
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-c:a", "pcm_s16le",
            str(output_path),
        ])
    finally:
        concat_list.unlink(missing_ok=True)


def make_label_text_png(label_text: str, output_path: Path):
    """
    Creates a transparent PNG with only text.
    Emoji is overlaid separately by ffmpeg to preserve color.
    """
    run([
        "magick",
        "-size", f"{LABEL_W}x{LABEL_H}",
        "xc:none",
        "-font", TEXT_FONT,
        "-pointsize", str(TEXT_FONT_SIZE),
        "-fill", "white",
        "-gravity", "center",
        "-annotate", "+0+0", label_text,
        str(output_path),
    ])


def make_timeline_and_labels(folder_name: str, files: list[Path]):
    display_name = clean_folder_name(folder_name)
    timeline = []

    t = 0.0

    for i, wav in enumerate(files, start=1):
        dur = ffprobe_duration(wav)
        start = t
        end = t + dur

        mood = MOODS[wav.name]
        label_text = f"{display_name} {mood['label']}"
        label_png = OUT_DIR / f"{folder_name}_label_text_{i}.png"
        emoji_path = mood["emoji_path"]

        if not emoji_path.exists():
            raise FileNotFoundError(
                f"Missing emoji file: {emoji_path}\n"
                f"Run the curl commands below to download the emoji PNGs."
            )

        make_label_text_png(label_text, label_png)

        timeline.append({
            "label_png": label_png,
            "emoji_path": emoji_path,
            "start": start,
            "end": end,
        })

        t = end

    return timeline


def make_video(concat_audio: Path, timeline: list[dict], video_path: Path):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(concat_audio),
    ]

    # For each segment, add:
    # 1. transparent text PNG
    # 2. original color emoji PNG
    for item in timeline:
        cmd += [
            "-loop", "1",
            "-i", str(item["label_png"]),
            "-loop", "1",
            "-i", str(item["emoji_path"]),
        ]

    filter_parts = [
        f"[0:a]"
        f"showwaves=s={WAVE_W}x{WAVE_H}:mode=line:rate={FPS}:colors={WAVE_COLOR},"
        f"format=rgba"
        f"[wave]",

        f"[wave]"
        f"pad={VIDEO_W}:{VIDEO_H}:0:{WAVE_Y_OFFSET}:color={BACKGROUND_COLOR}"
        f"[base]",
    ]

    current = "base"

    for idx, item in enumerate(timeline, start=1):
        start = item["start"]
        end = item["end"]

        label_input = 1 + (idx - 1) * 2
        emoji_input = label_input + 1

        label_out = f"label{idx}"
        emoji_scaled = f"emoji{idx}"
        final_out = f"v{idx}"

        enable = f"between(t,{start:.3f},{end:.3f})"

        # Overlay transparent text
        filter_parts.append(
            f"[{current}][{label_input}:v]"
            f"overlay="
            f"x={LABEL_X}:"
            f"y={LABEL_Y}:"
            f"enable='{enable}'"
            f"[{label_out}]"
        )

        # Scale original emoji PNG directly in ffmpeg
        filter_parts.append(
            f"[{emoji_input}:v]"
            f"scale={EMOJI_SIZE}:{EMOJI_SIZE},"
            f"format=rgba"
            f"[{emoji_scaled}]"
        )

        # Overlay emoji on its own centered line
        filter_parts.append(
            f"[{label_out}][{emoji_scaled}]"
            f"overlay="
            f"x={EMOJI_X}:"
            f"y={EMOJI_Y}:"
            f"enable='{enable}'"
            f"[{final_out}]"
        )

        current = final_out

    filter_parts.append(f"[{current}]format=yuv420p[v]")

    filter_complex = ";".join(filter_parts)

    cmd += [
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(video_path),
    ]

    run(cmd)


def make_demo(folder: Path):
    folder_name = folder.name
    wavs = [folder / name for name in ORDER]

    missing = [p for p in wavs if not p.exists()]
    if missing:
        print(f"Skipping {folder_name}, missing files:")
        for p in missing:
            print(f"  - {p}")
        return

    concat_audio = OUT_DIR / f"{folder_name}_concat.wav"
    video_path = OUT_DIR / f"{folder_name}_demo.mp4"

    make_concat_audio(wavs, concat_audio)
    timeline = make_timeline_and_labels(folder_name, wavs)
    make_video(concat_audio, timeline, video_path)

    print(f"Created {video_path}")


def main():
    folders = sorted(
        p for p in ROOT.iterdir()
        if p.is_dir() and p.name[:2].isdigit()
    )

    if not folders:
        print("No numbered folders found.")
        return

    for folder in folders:
        make_demo(folder)


if __name__ == "__main__":
    main()
