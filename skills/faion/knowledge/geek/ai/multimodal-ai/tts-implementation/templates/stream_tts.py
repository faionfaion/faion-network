"""
Async TTS streaming: stream_tts generator and stream_to_speaker for pyaudio.
Note: pyaudio requires portaudio system library. Verify at import, not at runtime.
"""
from __future__ import annotations

from typing import AsyncGenerator

from openai import AsyncOpenAI


async def stream_tts(text: str, voice: str = "alloy") -> AsyncGenerator[bytes, None]:
    """
    Stream TTS audio as PCM bytes.
    Must be called from async context. In sync context:
        audio = asyncio.run(collect_stream(text))
    """
    client = AsyncOpenAI()
    async with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="pcm",
    ) as response:
        async for chunk in response.iter_bytes():
            yield chunk


async def collect_stream(text: str, voice: str = "alloy") -> bytes:
    """Collect all stream chunks into a single bytes object (sync-friendly wrapper)."""
    return b"".join([chunk async for chunk in stream_tts(text, voice=voice)])


async def stream_to_speaker(text: str, voice: str = "alloy") -> None:
    """
    Stream TTS directly to speakers via pyaudio.
    Requires: pip install pyaudio && apt install portaudio19-dev
    PCM format: paInt16, 1 channel, 24000 Hz (matches OpenAI PCM output).
    """
    try:
        import pyaudio
    except ImportError as e:
        raise ImportError("pyaudio not installed. Run: pip install pyaudio (requires portaudio)") from e

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=24_000, output=True)
    try:
        async for chunk in stream_tts(text, voice=voice):
            stream.write(chunk)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


async def ws_tts_handler(websocket: object, text: str, voice: str = "alloy") -> None:
    """Forward TTS stream to a WebSocket client."""
    async for chunk in stream_tts(text, voice=voice):
        await websocket.send_bytes(chunk)  # type: ignore[attr-defined]
