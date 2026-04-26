"""BasicVoiceAgent with listen/think/speak loop."""
from openai import OpenAI
import sounddevice as sd
import numpy as np
import tempfile
import wave
from pathlib import Path

client = OpenAI()


class BasicVoiceAgent:
    """Simple voice agent: STT (Whisper) + LLM (GPT-4o) + TTS."""

    def __init__(self, system_prompt: str = "You are a helpful assistant.",
                 voice: str = "nova", sample_rate: int = 16000):
        self.system_prompt = system_prompt
        self.voice = voice
        self.sample_rate = sample_rate
        self.conversation_history = [{"role": "system", "content": system_prompt}]

    def listen(self, duration: float = 5.0) -> str:
        """Record fixed-duration audio and transcribe. Use VAD in production."""
        audio = sd.rec(int(duration * self.sample_rate),
                       samplerate=self.sample_rate, channels=1, dtype='int16')
        sd.wait()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            with wave.open(f.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio.tobytes())
            with open(f.name, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file,
                    language="en"  # specify language — avoid auto-detection latency
                )
            Path(f.name).unlink()
        return transcript.text

    def think(self, user_input: str) -> str:
        """Limit history to last 10 turns to prevent context overflow."""
        self.conversation_history.append({"role": "user", "content": user_input})
        # Sliding window: system prompt + last 20 messages (10 turns)
        system = [m for m in self.conversation_history if m["role"] == "system"]
        turns = [m for m in self.conversation_history if m["role"] != "system"]
        messages = system + turns[-20:]
        response = client.chat.completions.create(model="gpt-4o", messages=messages)
        msg = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": msg})
        return msg

    def speak(self, text: str) -> None:
        """Stream TTS audio to speaker. Requires pygame."""
        import pygame
        response = client.audio.speech.create(
            model="tts-1", voice=self.voice, input=text  # tts-1 for low-latency
        )
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            response.stream_to_file(f.name)
            pygame.mixer.init()
            pygame.mixer.music.load(f.name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            Path(f.name).unlink()

    def chat(self, duration: float = 5.0) -> str:
        user_input = self.listen(duration)
        print(f"You: {user_input}")
        response = self.think(user_input)
        print(f"Agent: {response}")
        self.speak(response)
        return response
