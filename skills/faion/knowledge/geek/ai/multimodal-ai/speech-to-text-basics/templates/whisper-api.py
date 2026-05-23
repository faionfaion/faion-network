"""
purpose: OpenAI Whisper API helpers — language-pinned transcribe + verbose_json with timestamps + translate.
consumes: audio path + language code + OpenAI client
produces: verbose_json with segments + start/end timestamps
depends-on: content/01-core-rules.xml r1, r2
token-budget-impact: per-minute API cost (no Whisper input-token cost; flat per-minute)
"""
from openai import OpenAI

client = OpenAI()


def transcribe_audio(audio_path: str, language: str = "en",
                     response_format: str = "text",
                     prompt: str = None) -> str:
    """
    Transcribe audio using Whisper API.
    language: ISO-639-1 code (e.g., "en", "uk", "es"). Always specify explicitly.
    response_format: "text" | "json" | "verbose_json" | "srt" | "vtt"
    prompt: domain terms, speaker names — keep under 100 tokens.
    """
    kwargs = {
        "model": "whisper-1",
        "language": language,
        "response_format": response_format,
    }
    if prompt:
        kwargs["prompt"] = prompt
    with open(audio_path, "rb") as audio_file:
        kwargs["file"] = audio_file
        response = client.audio.transcriptions.create(**kwargs)
    return response if response_format == "text" else response


def transcribe_with_timestamps(audio_path: str, language: str = "en") -> dict:
    """Get transcription with word and segment timestamps."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,
            response_format="verbose_json",       # required for timestamps
            timestamp_granularities=["word", "segment"]
        )
    return {
        "text": response.text,
        "segments": response.segments,
        # response.words is Word objects, not dicts — serialize manually if needed
        "words": [{"word": w.word, "start": w.start, "end": w.end}
                  for w in (response.words or [])],
        "duration": response.duration,
        "language": response.language
    }


def translate_audio(audio_path: str) -> str:
    """Translate non-English audio to English."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.translations.create(
            model="whisper-1", file=audio_file
        )
    return response.text
