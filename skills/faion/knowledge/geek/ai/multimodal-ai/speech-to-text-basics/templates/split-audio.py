"""Split audio into chunks under 24MB for Whisper API upload."""
from pydub import AudioSegment
import math
import os


def split_audio(path: str, chunk_min: int = 10,
                out_dir: str = "/tmp") -> list[str]:
    """
    Split audio file into chunks of ~chunk_min minutes.
    Exports as MP3 at 64kbps to stay well under 25MB Whisper API limit.
    Returns list of chunk file paths in order.
    """
    audio = AudioSegment.from_file(path)
    chunk_ms = chunk_min * 60 * 1000
    n = math.ceil(len(audio) / chunk_ms)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i in range(n):
        chunk = audio[i * chunk_ms:(i + 1) * chunk_ms]
        p = os.path.join(out_dir, f"chunk_{i:03d}.mp3")
        chunk.export(p, format="mp3", bitrate="64k")
        paths.append(p)
    return paths


def merge_transcripts(transcripts: list[dict],
                      chunk_duration_s: float) -> dict:
    """
    Merge transcript chunks with adjusted timestamps.
    transcripts: list of verbose_json transcript dicts (one per chunk).
    chunk_duration_s: duration of each chunk in seconds.
    """
    merged_segments = []
    full_text = ""
    for i, transcript in enumerate(transcripts):
        offset = i * chunk_duration_s
        for segment in transcript.get("segments", []):
            merged_segments.append({
                "start": segment["start"] + offset,
                "end": segment["end"] + offset,
                "text": segment["text"]
            })
        full_text += transcript.get("text", "")
    return {"text": full_text.strip(), "segments": merged_segments}
