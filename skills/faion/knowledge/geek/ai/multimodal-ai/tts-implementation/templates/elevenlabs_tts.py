"""
ElevenLabs TTS and voice cloning.
Requirements: pip install elevenlabs
Consent: voice cloning requires explicit consent from the person whose voice is cloned.
"""
from __future__ import annotations

import os

from elevenlabs import ElevenLabs, Voice, VoiceSettings


def elevenlabs_tts(
    text: str,
    output_path: str,
    voice_id: str,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    model: str = "eleven_multilingual_v2",
) -> str:
    """
    Generate speech using ElevenLabs.
    voice_id: use a built-in voice ID or one returned by clone_voice().
    stability: 0.0-1.0 (lower = more variable/expressive)
    similarity_boost: 0.0-1.0 (higher = closer to original voice)
    """
    client = ElevenLabs()
    audio = client.generate(
        text=text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                style=0.5,
                use_speaker_boost=True,
            ),
        ),
        model=model,
    )
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return output_path


def clone_voice(audio_sample_paths: list[str], name: str, description: str = "") -> str:
    """
    Clone a voice from audio samples. Returns voice_id for use in elevenlabs_tts().
    audio_sample_paths: list of ABSOLUTE paths to .mp3 or .wav files, each >= 30 seconds.
    Recommended: 3 samples of 30-60s each, minimal background noise, normalized levels.
    SLOW: 10-30 seconds per call. Call once and cache the returned voice_id.
    """
    for path in audio_sample_paths:
        if not os.path.isabs(path):
            raise ValueError(f"clone_voice requires absolute paths, got: {path}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sample file not found: {path}")
    client = ElevenLabs()
    voice = client.clone(name=name, description=description, files=audio_sample_paths)
    return voice.voice_id
