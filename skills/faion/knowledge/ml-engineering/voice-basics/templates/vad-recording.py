# purpose: WebRTC VAD recorder — stop on consecutive silence per rule r2-vad-recording.
# consumes: silence_ms (default 1000), max_duration_s (default 30), sample_rate (16000).
# produces: WAV bytes (16kHz, mono, int16) ready for Whisper STT.
# depends-on: webrtcvad; sounddevice; portaudio system lib.
# token-budget-impact: zero (audio path, no LLM call).
"""record_until_silence(): WebRTC-VAD-based recorder."""

from __future__ import annotations
import collections, io, time, wave
import sounddevice as sd
import webrtcvad

SAMPLE_RATE = 16000
FRAME_MS = 30


def record_until_silence(silence_ms: int = 1000, max_s: int = 30,
                         aggressiveness: int = 2) -> bytes:
    vad = webrtcvad.Vad(aggressiveness)
    frame_samples = SAMPLE_RATE * FRAME_MS // 1000
    silence_frames = silence_ms // FRAME_MS
    ring = collections.deque(maxlen=silence_frames)
    frames: list[bytes] = []
    t0 = time.monotonic()
    with sd.RawInputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as stream:
        while time.monotonic() - t0 < max_s:
            data, _ = stream.read(frame_samples)
            frame = bytes(data)
            ring.append(vad.is_speech(frame, SAMPLE_RATE))
            frames.append(frame)
            if len(frames) > silence_frames and not any(ring):
                break
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SAMPLE_RATE)
        w.writeframes(b"".join(frames))
    return buf.getvalue()
