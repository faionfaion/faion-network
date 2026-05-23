# purpose: TTS call with content-hash cache layer (Redis / local)
# consumes: text + voice + model
# produces: code (drop-in cached TTS module)
# depends-on: openai or elevenlabs SDK; redis (optional)
# token-budget-impact: ~200 tokens if loaded into LLM context
"""TTS with content-hash caching to avoid redundant API calls."""
import hashlib
import os
from pathlib import Path

from elevenlabs.client import ElevenLabs
from elevenlabs import stream


CACHE_DIR = Path(os.environ.get("TTS_CACHE_DIR", "/tmp/tts-cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

DEFAULT_VOICE = "JBFqnCBsd6RMkjVDRZzb"   # Rachel
DEFAULT_MODEL = "eleven_flash_v2_5"
DEFAULT_FORMAT = "mp3_44100_128"


def _cache_key(text: str, voice_id: str, model_id: str, output_format: str) -> str:
    raw = f"{text}|{voice_id}|{model_id}|{output_format}"
    return hashlib.sha256(raw.encode()).hexdigest()


def synthesize(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    model_id: str = DEFAULT_MODEL,
    output_format: str = DEFAULT_FORMAT,
) -> bytes:
    """Generate TTS audio with cache. Returns audio bytes."""
    key = _cache_key(text, voice_id, model_id, output_format)
    cache_path = CACHE_DIR / f"{key}.mp3"

    if cache_path.exists():
        return cache_path.read_bytes()

    audio = b"".join(client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=model_id,
        output_format=output_format,
    ))
    cache_path.write_bytes(audio)
    return audio


def synthesize_streaming(
    text: str,
    voice_id: str = DEFAULT_VOICE,
    model_id: str = DEFAULT_MODEL,
) -> None:
    """Stream TTS audio to speakers with minimal latency. Does not cache."""
    audio_stream = client.text_to_speech.stream(
        voice_id=voice_id,
        text=text,
        model_id=model_id,
        output_format="mp3_44100_128",
    )
    stream(audio_stream)
