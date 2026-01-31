# Text-to-Speech (TTS) Services

**Comprehensive guide for text-to-speech synthesis using ElevenLabs, OpenAI, and Azure**

---

## Quick Reference

**When to use this guide:**
- Text-to-speech synthesis (TTS)
- Voice selection and customization
- Voice cloning and voice design
- Emotion control and SSML
- Real-time speech synthesis

---

## TTS Service Comparison

| Service | Latency | Quality | Voices | Price/1k chars | Best For |
|---------|---------|---------|--------|----------------|----------|
| **ElevenLabs** | ~200ms | Excellent | 1000+ | $0.30 | Quality, voice cloning |
| **OpenAI TTS** | ~300ms | Very Good | 6 | $0.015 | Simple, cheap |
| **Azure Speech** | ~150ms | Very Good | 400+ | $0.016 | Enterprise, SSML |
| **Cartesia Sonic** | ~75ms | Good | 100+ | $0.04 | Ultra-low latency |
| **Google Cloud TTS** | ~200ms | Very Good | 220+ | $0.016 | Multilingual |
| **Amazon Polly** | ~150ms | Good | 60+ | $0.016 | AWS integration |

---

## ElevenLabs TTS

### Overview

ElevenLabs offers the highest quality AI voices with voice cloning capabilities.

**Models:**
| Model | Latency | Quality | Use Case |
|-------|---------|---------|----------|
| `eleven_multilingual_v2` | ~300ms | Highest | Production, 29 languages |
| `eleven_turbo_v2_5` | ~200ms | Very High | General use |
| `eleven_flash_v2_5` | ~100ms | High | Real-time streaming |

### Installation

```bash
pip install elevenlabs
```

### Basic TTS

```python
from elevenlabs import ElevenLabs, play, save
import os

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Generate audio
audio = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
    text="Hello, welcome to Faion Network!",
    model_id="eleven_turbo_v2_5",
    output_format="mp3_44100_128",
)

# Play directly
play(audio)

# Or save to file
save(audio, "output.mp3")
```

### Streaming (Low Latency)

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

# Streaming for real-time playback
audio_stream = client.text_to_speech.convert_as_stream(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text="This is streaming audio generation for low latency applications.",
    model_id="eleven_flash_v2_5",
    output_format="mp3_44100_32",  # Lower bitrate for faster streaming
)

# Process chunks as they arrive
for chunk in audio_stream:
    # Send to audio player or WebSocket
    process_audio_chunk(chunk)
```

### Voice Selection

```python
# List available voices
voices = client.voices.get_all()
for voice in voices.voices:
    print(f"{voice.name}: {voice.voice_id}")

# Popular voice IDs
VOICES = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",      # Female, American
    "Domi": "AZnzlk1XvdvUeBnXmlld",         # Female, American
    "Bella": "EXAVITQu4vr4xnSDxMaL",        # Female, American
    "Antoni": "ErXwobaYiN019PkySvjV",       # Male, American
    "Josh": "TxGEqnHWrfWFTfGW9XjX",         # Male, American
    "Arnold": "VR6AewLTigWG4xSOukaG",       # Male, American
    "Adam": "pNInz6obpgDQGcFmaJgB",         # Male, American
    "Sam": "yoZ06aMxZJJ28mfd3POQ",          # Male, American
}
```

### Voice Cloning (Instant)

```python
from elevenlabs import VoiceSettings

# Clone voice from audio sample
voice = client.clone(
    name="My Custom Voice",
    description="Voice cloned from sample audio",
    files=["sample1.mp3", "sample2.mp3"],  # 1-30 minutes of audio
)

# Use cloned voice
audio = client.text_to_speech.convert(
    voice_id=voice.voice_id,
    text="Hello, this is my cloned voice!",
    model_id="eleven_multilingual_v2",
)
```

### Voice Settings (Emotion Control)

```python
from elevenlabs import VoiceSettings

audio = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text="I am so excited about this!",
    model_id="eleven_turbo_v2_5",
    voice_settings=VoiceSettings(
        stability=0.5,          # 0-1: Lower = more expressive
        similarity_boost=0.75,  # 0-1: Higher = closer to original
        style=0.3,              # 0-1: Style exaggeration
        use_speaker_boost=True,
    ),
)
```

### Voice Design (Create from Description)

```python
# Create voice from text description
voice = client.voices.design(
    name="Custom Voice",
    description="A warm, friendly female voice with a British accent",
    text="Hello! This is a sample of the generated voice.",
)
```

### Pronunciation Dictionary

```python
# Custom pronunciation
audio = client.text_to_speech.convert_with_pronunciation_dictionaries(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text="Welcome to Faion Network!",
    model_id="eleven_turbo_v2_5",
    pronunciation_dictionary_locators=[
        {
            "pronunciation_dictionary_id": "dict_id",
            "version_id": "version_id"
        }
    ],
)
```

---

## OpenAI TTS

### Overview

OpenAI TTS offers simple integration with good quality at low cost.

**Models:**
| Model | Quality | Latency | Price/1M chars |
|-------|---------|---------|----------------|
| `tts-1` | Good | Low | $15 |
| `tts-1-hd` | High | Higher | $30 |

**Voices:** alloy, echo, fable, onyx, nova, shimmer

### Basic Usage

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

# Generate speech
response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input="Hello, this is OpenAI text to speech!",
    response_format="mp3",  # mp3, opus, aac, flac, wav, pcm
    speed=1.0,  # 0.25 to 4.0
)

# Save to file
response.stream_to_file(Path("output.mp3"))
```

### Streaming

```python
# Real-time streaming
response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input="This is streaming audio from OpenAI.",
)

# Stream to file
with open("output.mp3", "wb") as f:
    for chunk in response.iter_bytes():
        f.write(chunk)
```

### Voice Characteristics

| Voice | Gender | Style |
|-------|--------|-------|
| alloy | Neutral | Balanced |
| echo | Male | Warm |
| fable | Female | British |
| onyx | Male | Deep |
| nova | Female | Friendly |
| shimmer | Female | Soft |

---

## Azure Speech Services

### Overview

Azure offers enterprise-grade TTS with SSML support and neural voices.

### Installation

```bash
pip install azure-cognitiveservices-speech
```

### Basic TTS

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="your_key",
    region="eastus"
)
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Synthesize to speaker
result = synthesizer.speak_text_async("Hello from Azure!").get()

# Synthesize to file
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)
result = synthesizer.speak_text_async("Hello from Azure!").get()
```

### SSML (Speech Synthesis Markup Language)

```python
ssml = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <mstts:express-as style="cheerful" styledegree="2">
            Hello! I am so happy to meet you!
        </mstts:express-as>
        <break time="500ms"/>
        <prosody rate="-10%" pitch="+5%">
            This is spoken more slowly with higher pitch.
        </prosody>
    </voice>
</speak>
"""

result = synthesizer.speak_ssml_async(ssml).get()
```

### Custom Neural Voice

```python
# Azure custom voice endpoint
speech_config.endpoint_id = "your_custom_voice_endpoint_id"
speech_config.speech_synthesis_voice_name = "YourCustomVoiceName"
```

---

## API Credentials

### Environment Variables

```bash
# ElevenLabs
export ELEVENLABS_API_KEY="your_key"

# OpenAI
export OPENAI_API_KEY="your_key"

# Azure Speech
export AZURE_SPEECH_KEY="your_key"
export AZURE_SPEECH_REGION="eastus"
```

### Loading Credentials

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Or use secrets file
# source ~/.secrets/elevenlabs
# source ~/.secrets/openai
```

---

## Related Files

- [audio-stt-services.md](audio-stt-services.md) - Speech-to-text services
- [audio-voice-agents.md](audio-voice-agents.md) - Voice cloning, real-time streaming, voice agents

---

## References

- [ElevenLabs Docs](https://elevenlabs.io/docs)
- [OpenAI Audio API](https://platform.openai.com/docs/guides/audio)
- [Azure Speech Services](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)


## Sources

- [Murf AI Voice Generation](https://murf.ai/resources/)
- [Resemble AI Voice Cloning](https://www.resemble.ai/blog/)
- [WellSaid Labs TTS](https://wellsaidlabs.com/resources/)
- [Speechify Text-to-Speech](https://speechify.com/blog/)
- [Natural Reader TTS](https://www.naturalreaders.com/blog/)
