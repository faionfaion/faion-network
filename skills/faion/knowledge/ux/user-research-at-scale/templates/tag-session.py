# tag-session.py — Whisper transcription + Anthropic taxonomy tagging at scale
# Input: sessions/*.mp4, taxonomy.json
# Output: tagged.json with {file, tagged: [{segment, tags, untagged: bool}]}
# Usage: python tag-session.py
# Requires: pip install whisperx anthropic

import json
import os
from pathlib import Path

import anthropic
import whisperx

TAX = json.loads(Path("taxonomy.json").read_text())
client = anthropic.Anthropic()


def transcribe(path: Path) -> list[dict]:
    device = "cuda" if os.getenv("USE_GPU") else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    model = whisperx.load_model("large-v3", device, compute_type=compute_type)
    audio = whisperx.load_audio(str(path))
    result = model.transcribe(audio, batch_size=16)
    return result["segments"]


def tag(segments: list[dict]) -> list[dict]:
    prompt = json.dumps({
        "taxonomy": TAX,
        "segments": segments,
        "instructions": (
            "Tag every segment using ONLY tags from the provided taxonomy. "
            "If no tag fits, set untagged=true. "
            "Never invent new tags. "
            "Return a JSON array of {segment_id, text, tags: [], untagged: bool}."
        ),
    })
    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4000,
        system="You tag user-research segments using ONLY the provided taxonomy. Never invent tags.",
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(msg.content[0].text)


if __name__ == "__main__":
    out = []
    for f in sorted(Path("sessions").glob("*.mp4")):
        print(f"Transcribing {f.name}...")
        segs = transcribe(f)
        print(f"Tagging {len(segs)} segments...")
        tagged = tag(segs)
        out.append({"file": f.name, "tagged": tagged})
    Path("tagged.json").write_text(json.dumps(out, indent=2))
    print(f"Done. {len(out)} sessions written to tagged.json")
