# Audio Editing & Analysis

**Tools and techniques for audio manipulation, analysis, and processing**

---

## pydub (Audio Manipulation)

### Installation

```bash
pip install pydub
```

### Basic Operations

```python
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from pydub.silence import split_on_silence

# Load audio
audio = AudioSegment.from_file("input.mp3")

# Basic operations
audio = audio + 10  # Increase volume by 10dB
audio = audio - 5   # Decrease volume by 5dB
audio = audio.fade_in(1000).fade_out(1000)  # Fade in/out
audio = audio.set_frame_rate(44100)  # Resample
audio = audio.set_channels(1)  # Convert to mono

# Concatenation
combined = audio1 + audio2

# Slicing
first_10_seconds = audio[:10000]  # milliseconds

# Split on silence
chunks = split_on_silence(
    audio,
    min_silence_len=500,
    silence_thresh=-40,
    keep_silence=200,
)

# Effects
audio = normalize(audio)
audio = compress_dynamic_range(audio, threshold=-20, ratio=4.0)

# Export
audio.export("output.mp3", format="mp3", bitrate="192k")
audio.export("output.wav", format="wav")
```

---

## librosa (Audio Analysis)

### Installation

```bash
pip install librosa
```

### Feature Extraction

```python
import librosa
import numpy as np

# Load audio
y, sr = librosa.load("audio.mp3", sr=None)

# Get duration
duration = librosa.get_duration(y=y, sr=sr)

# Extract features
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Pitch detection
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Speech/music detection
# (Use onset detection for speech segmentation)
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
```

---

## soundfile (Read/Write Audio)

### Installation

```bash
pip install soundfile
```

### Usage

```python
import soundfile as sf

# Read audio
data, samplerate = sf.read("audio.wav")

# Write audio
sf.write("output.wav", data, samplerate)

# Get info without loading
info = sf.info("audio.wav")
print(f"Duration: {info.duration}s, Channels: {info.channels}")
```

---

## Common Audio Workflows

### Convert Audio Format

```python
from pydub import AudioSegment

# Convert any format to any format
audio = AudioSegment.from_file("input.m4a", format="m4a")
audio.export("output.mp3", format="mp3", bitrate="192k")
```

### Normalize Audio Levels

```python
from pydub import AudioSegment
from pydub.effects import normalize

audio = AudioSegment.from_file("input.mp3")
normalized = normalize(audio)
normalized.export("output.mp3", format="mp3")
```

### Remove Silence

```python
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

audio = AudioSegment.from_file("input.mp3")

# Detect non-silent chunks
nonsilent_ranges = detect_nonsilent(
    audio,
    min_silence_len=1000,  # ms
    silence_thresh=-40,     # dBFS
)

# Keep only non-silent parts
result = AudioSegment.empty()
for start, end in nonsilent_ranges:
    result += audio[start:end]

result.export("output.mp3", format="mp3")
```

### Extract Audio from Video

```python
from pydub import AudioSegment

# Extract audio from video file
audio = AudioSegment.from_file("video.mp4", format="mp4")
audio.export("audio.mp3", format="mp3")
```

### Batch Process Audio Files

```python
from pydub import AudioSegment
from pathlib import Path

input_dir = Path("./input")
output_dir = Path("./output")
output_dir.mkdir(exist_ok=True)

for audio_file in input_dir.glob("*.wav"):
    audio = AudioSegment.from_file(audio_file)

    # Process audio
    audio = audio.set_frame_rate(44100)
    audio = audio.set_channels(1)
    audio = normalize(audio)

    # Export
    output_path = output_dir / f"{audio_file.stem}.mp3"
    audio.export(output_path, format="mp3", bitrate="192k")
```

---

## Audio Quality Optimization

### Podcast Audio Processing

```python
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

def process_podcast(input_file: str, output_file: str):
    """Process podcast audio for optimal quality"""

    # Load audio
    audio = AudioSegment.from_file(input_file)

    # Convert to mono (podcasts don't need stereo)
    audio = audio.set_channels(1)

    # Resample to 44.1kHz
    audio = audio.set_frame_rate(44100)

    # Normalize volume
    audio = normalize(audio)

    # Apply compression
    audio = compress_dynamic_range(
        audio,
        threshold=-20,  # dBFS
        ratio=4.0,
        attack=5.0,
        release=50.0
    )

    # Apply high-pass filter to remove rumble
    # (pydub doesn't have built-in filters, use scipy for advanced filtering)

    # Export
    audio.export(
        output_file,
        format="mp3",
        bitrate="128k",  # Good quality for speech
        parameters=["-ac", "1"]  # Force mono
    )

# Usage
process_podcast("raw_podcast.wav", "final_podcast.mp3")
```

### Voice Recording Cleanup

```python
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.effects import normalize

def cleanup_voice_recording(input_file: str, output_file: str):
    """Clean up voice recording by removing silence and normalizing"""

    audio = AudioSegment.from_file(input_file)

    # Split on silence and keep only speech
    chunks = split_on_silence(
        audio,
        min_silence_len=500,   # 500ms of silence
        silence_thresh=-40,     # Consider anything quieter than -40 dBFS as silence
        keep_silence=200,       # Keep 200ms of silence at boundaries
    )

    # Concatenate chunks with consistent padding
    result = AudioSegment.empty()
    for chunk in chunks:
        result += chunk + AudioSegment.silent(duration=300)  # 300ms pause

    # Normalize
    result = normalize(result)

    # Export
    result.export(output_file, format="mp3", bitrate="192k")

# Usage
cleanup_voice_recording("raw_recording.wav", "clean_recording.mp3")
```

---

## References

- [pydub Documentation](https://github.com/jiaaro/pydub)
- [librosa Documentation](https://librosa.org/doc/latest/)
- [soundfile Documentation](https://python-soundfile.readthedocs.io/)


## Sources

- [Audacity Audio Editing Guide](https://manual.audacityteam.org/)
- [Adobe Audition Tutorials](https://helpx.adobe.com/audition/tutorials.html)
- [iZotope Audio Production](https://www.izotope.com/en/learn.html)
- [Waves Audio Mixing Guide](https://www.waves.com/mixing-mastering-tips)
- [Sound on Sound Recording Techniques](https://www.soundonsound.com/)
