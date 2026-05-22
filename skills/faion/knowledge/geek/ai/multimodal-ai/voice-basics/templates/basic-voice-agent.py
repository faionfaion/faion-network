# purpose: BasicVoiceAgent — VAD listen → Whisper STT → GPT-4o reason → strip Markdown → streaming TTS.
# consumes: voice id, language tag, system prompt; OPENAI_API_KEY env.
# produces: per-turn dict per 02-output-contract; in-memory conversation_history (cap 10 pairs).
# depends-on: openai SDK; sounddevice; webrtcvad; rules r1-r6 in 01-core-rules.
# token-budget-impact: ~50 system prompt tokens + per-turn ~150 reply tokens.
"""BasicVoiceAgent: turn-based STT→LLM→TTS loop with VAD + history cap."""

from __future__ import annotations
import collections, io, re, time, wave
from typing import Optional
import sounddevice as sd
import webrtcvad
from openai import OpenAI

SAMPLE_RATE = 16000


class BasicVoiceAgent:
    def __init__(self, system_prompt: str, voice: str = "nova", language: str = "en",
                 max_pairs: int = 10) -> None:
        self.system_prompt = system_prompt
        self.voice = voice
        self.language = language
        self.max_pairs = max_pairs
        self.history = [{"role": "system", "content": system_prompt}]
        self.client = OpenAI()

    def listen(self, silence_ms: int = 1000, max_s: int = 30) -> bytes:
        vad = webrtcvad.Vad(2)
        frame_samples = SAMPLE_RATE * 30 // 1000
        silence_frames = silence_ms // 30
        ring = collections.deque(maxlen=silence_frames)
        frames: list[bytes] = []
        t0 = time.monotonic()
        with sd.RawInputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as s:
            while time.monotonic() - t0 < max_s:
                data, _ = s.read(frame_samples)
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

    def transcribe(self, wav: bytes) -> str:
        return self.client.audio.transcriptions.create(
            model="whisper-1", file=("audio.wav", io.BytesIO(wav)),
            language=self.language).text

    def reason(self, user_text: str) -> str:
        self.history.append({"role": "user", "content": user_text})
        self.history = self.history[:1] + self.history[1:][-(self.max_pairs * 2):]
        resp = self.client.chat.completions.create(
            model="gpt-4o", messages=self.history, max_tokens=200)
        text = self._strip_markdown(resp.choices[0].message.content or "")
        self.history.append({"role": "assistant", "content": text})
        return text

    def speak(self, text: str, out_path: str) -> str:
        with self.client.audio.speech.with_streaming_response.create(
                model="tts-1", voice=self.voice, input=text,
                response_format="mp3") as r:
            with open(out_path, "wb") as f:
                for chunk in r.iter_bytes(1024):
                    f.write(chunk)
        return out_path

    @staticmethod
    def _strip_markdown(t: str) -> str:
        return re.sub(r"[*_`#>]", "", t).strip()
