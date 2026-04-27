"""Minimal ASR → LLM → TTS pipeline. Swap Whisper/Polly for preferred services."""
import anthropic
import boto3
import io

import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

PERSONA = (
    "You are a helpful assistant. Keep responses under 2 sentences. "
    "Ask one clarifying question when the request is ambiguous."
)


def transcribe(audio_data: bytes) -> str:
    """Transcribe audio via Whisper (swap for Deepgram/AssemblyAI as needed)."""
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(io.BytesIO(audio_data))
    return result["text"]


def generate_response(history: list[dict], user_text: str) -> str:
    """Generate a conversational reply, maintaining a 10-turn history window."""
    client = anthropic.Anthropic()
    history.append({"role": "user", "content": user_text})
    if len(history) > 20:  # 10 turns = 20 messages
        history = history[-20:]
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        system=PERSONA,
        messages=history,
    )
    reply = msg.content[0].text
    history.append({"role": "assistant", "content": reply})
    return reply


def speak(text: str) -> None:
    """Convert text to speech via Amazon Polly and play locally."""
    polly = boto3.client("polly", region_name="us-east-1")
    response = polly.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna"
    )
    audio = AudioSegment.from_mp3(io.BytesIO(response["AudioStream"].read()))
    play(audio)
