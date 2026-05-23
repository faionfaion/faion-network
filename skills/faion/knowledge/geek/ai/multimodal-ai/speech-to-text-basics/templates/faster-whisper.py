"""
purpose: Local faster-whisper (CTranslate2) transcriber with VAD filter and streaming output.
consumes: audio path + model size + GPU/CPU device + language
produces: segments with timestamps (verbose_json-equivalent)
depends-on: content/01-core-rules.xml r1, r5
token-budget-impact: zero per call (sunk GPU cost)
"""
from faster_whisper import WhisperModel
from typing import Generator


class FasterWhisperTranscriber:
    """Optimized Whisper using CTranslate2 — 4x faster than original."""

    def __init__(self, model_size: str = "base",
                 device: str = "auto", compute_type: str = "auto"):
        """
        model_size: "tiny" | "base" | "small" | "medium" | "large-v3"
        device: "auto" | "cpu" | "cuda"
        Note: large-v3 on CPU requires ~10GB RAM — use base/small for CPU.
        """
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: str, language: str = None,
                   beam_size: int = 5, word_timestamps: bool = False,
                   vad_filter: bool = True) -> dict:
        """
        vad_filter=True removes silence (20-40% speed improvement on long files).
        Warning: vad_filter can silently drop segments under 0.5s.
        """
        segments, info = self.model.transcribe(
            audio_path,
            language=language,  # specify explicitly for accuracy + speed
            beam_size=beam_size,
            word_timestamps=word_timestamps,
            vad_filter=vad_filter
        )
        all_segments = []
        full_text = ""
        for segment in segments:
            seg = {"start": segment.start, "end": segment.end, "text": segment.text}
            if word_timestamps and segment.words:
                seg["words"] = [
                    {"word": w.word, "start": w.start, "end": w.end,
                     "probability": w.probability}
                    for w in segment.words
                ]
            all_segments.append(seg)
            full_text += segment.text
        return {
            "text": full_text.strip(),
            "segments": all_segments,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration
        }

    def transcribe_stream(self, audio_path: str,
                          language: str = None) -> Generator[dict, None, None]:
        """Stream segments as they complete (still processes full file)."""
        segments, _ = self.model.transcribe(audio_path, language=language)
        for segment in segments:
            yield {"start": segment.start, "end": segment.end, "text": segment.text}
