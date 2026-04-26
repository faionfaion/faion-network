"""WebRTC-VAD-based recording — stops when silence detected."""
import webrtcvad
import sounddevice as sd
import collections


def record_until_silence(sample_rate: int = 16000, silence_ms: int = 1000,
                         aggressiveness: int = 2) -> bytes:
    """
    Record audio until silence_ms of silence is detected.
    aggressiveness: 0 (permissive) to 3 (aggressive)
    Returns raw PCM bytes (int16, mono, 16kHz).
    """
    vad = webrtcvad.Vad(aggressiveness)
    frame_ms = 30  # VAD frame must be 10, 20, or 30ms
    frame_bytes = sample_rate * frame_ms // 1000 * 2  # 2 bytes per int16 sample
    silence_frames = silence_ms // frame_ms
    ring = collections.deque(maxlen=silence_frames)
    frames = []
    speech_started = False

    with sd.RawInputStream(samplerate=sample_rate, channels=1, dtype='int16') as s:
        while True:
            data, _ = s.read(frame_bytes // 2)
            frame = bytes(data)
            is_speech = vad.is_speech(frame, sample_rate)
            ring.append(is_speech)
            if is_speech:
                speech_started = True
            if speech_started:
                frames.append(frame)
            # Stop when we have seen silence_frames of consecutive silence after speech
            if speech_started and len(ring) == silence_frames and not any(ring):
                break

    return b"".join(frames)
