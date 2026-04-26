"""RealtimeVoiceAgent with threaded capture and VAD processing."""
import queue
import threading
from dataclasses import dataclass
from pathlib import Path
import tempfile
import wave

import numpy as np
from openai import OpenAI


@dataclass
class VADConfig:
    threshold: float = 0.02           # energy RMS threshold — prototype only
    min_speech_duration: float = 0.5  # seconds
    silence_duration: float = 0.8     # seconds before utterance ends


class RealtimeVoiceAgent:
    """Voice agent with threaded mic capture and energy-based VAD."""

    def __init__(self, system_prompt: str, voice: str = "nova",
                 vad_config: VADConfig | None = None):
        self.system_prompt = system_prompt
        self.voice = voice
        self.vad_config = vad_config or VADConfig()
        self.client = OpenAI()
        self.conversation_history = [{"role": "system", "content": system_prompt}]
        self.audio_queue: queue.Queue = queue.Queue()
        self.is_listening = False
        self.is_speaking = False

    def start(self) -> tuple[threading.Thread, threading.Thread]:
        self.is_listening = True
        capture_thread = threading.Thread(target=self._capture_audio, daemon=True)
        process_thread = threading.Thread(target=self._process_audio, daemon=True)
        capture_thread.start()
        process_thread.start()
        return capture_thread, process_thread

    def stop(self) -> None:
        self.is_listening = False

    def _capture_audio(self) -> None:
        import sounddevice as sd

        def callback(indata, frames, time, status):
            if self.is_listening and not self.is_speaking:
                self.audio_queue.put(indata.copy())

        with sd.InputStream(samplerate=16000, channels=1, dtype="float32",
                            callback=callback, blocksize=1600):
            while self.is_listening:
                sd.sleep(100)

    def _process_audio(self) -> None:
        """Energy-based VAD. Replace with Silero VAD for production."""
        audio_buffer, speech_detected, silence_frames = [], False, 0

        while self.is_listening:
            try:
                audio_chunk = self.audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            energy = np.sqrt(np.mean(audio_chunk ** 2))
            if energy > self.vad_config.threshold:
                speech_detected = True
                silence_frames = 0
                audio_buffer.append(audio_chunk)
            elif speech_detected:
                silence_frames += 1
                audio_buffer.append(audio_chunk)
                if silence_frames > self.vad_config.silence_duration * 10:
                    if len(audio_buffer) > self.vad_config.min_speech_duration * 10:
                        self._handle_utterance(np.concatenate(audio_buffer))
                    audio_buffer, speech_detected, silence_frames = [], False, 0

    def _handle_utterance(self, audio_data: np.ndarray) -> None:
        self.is_speaking = True
        try:
            transcript = self._transcribe(audio_data)
            if transcript.strip():
                response = self._generate_response(transcript)
                self._speak(response)
        finally:
            self.is_speaking = False

    def _transcribe(self, audio_data: np.ndarray) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            with wave.open(f.name, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
            with open(f.name, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, language="en")
            Path(f.name).unlink()
        return result.text

    def _generate_response(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model="gpt-4o", messages=self.conversation_history, max_tokens=150)
        msg = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": msg})
        return msg

    def _speak(self, text: str) -> None:
        """Stream TTS audio to pyaudio output."""
        import pyaudio
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1", voice=self.voice, input=text, response_format="pcm"
        ) as response:
            for chunk in response.iter_bytes(chunk_size=1024):
                stream.write(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
