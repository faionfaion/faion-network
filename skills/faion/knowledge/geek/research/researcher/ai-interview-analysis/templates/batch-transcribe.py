# batch_transcribe.py — transcribe a folder of audio files using Whisper
# Requires: pip install openai-whisper ffmpeg-python
# Pre-process audio first: ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav

import whisper
import json
from pathlib import Path

model = whisper.load_model("base")  # use "medium" or "large" for better accuracy


def transcribe_folder(audio_dir: str, out_dir: str) -> None:
    """Transcribe all audio files in audio_dir and write JSON transcripts to out_dir."""
    audio_path = Path(audio_dir)
    out_path = Path(out_dir)
    out_path.mkdir(exist_ok=True)

    extensions = {".mp3", ".mp4", ".m4a", ".wav", ".ogg", ".flac"}
    audio_files = [f for f in audio_path.iterdir() if f.suffix.lower() in extensions]

    for audio_file in audio_files:
        print(f"Transcribing: {audio_file.name}")
        result = model.transcribe(
            str(audio_file),
            task="transcribe",
            language=None,  # auto-detect; set "en" to force English
        )
        out_file = out_path / f"{audio_file.stem}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump({
                "file": audio_file.name,
                "language": result.get("language"),
                "text": result["text"],
                "segments": [
                    {
                        "start": s["start"],
                        "end": s["end"],
                        "text": s["text"].strip(),
                    }
                    for s in result["segments"]
                ],
            }, f, indent=2, ensure_ascii=False)
        print(f"  → {out_file.name}")


# Usage:
# transcribe_folder("./recordings", "./transcripts")
