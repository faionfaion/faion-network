# Agent Integration — Speech-to-Text Basics

## When to use
- Transcribing recorded audio files (interviews, meetings, podcasts, call recordings) as part of a content pipeline
- Building voice input for agents where microphone audio is the primary input channel
- Generating searchable transcripts with timestamps for media libraries
- Multilingual transcription or audio-to-English translation
- Pre-processing audio before LLM analysis (summarization, Q&A extraction, sentiment)

## When NOT to use
- Real-time streaming requirements below 300ms — Whisper API is batch-only (full file upload); use Deepgram or AssemblyAI streaming instead
- Audio longer than 25MB per file — Whisper API rejects; must split first
- Extremely noisy audio (SNR < 5dB) — accuracy degrades to unusable; pre-filter or reject
- High-volume production (>10k hours/month) — API costs exceed local deployment cost; switch to faster-whisper on GPU

## Where it fails / limitations
- Whisper API has a 25MB file size limit — a typical 90-minute meeting WAV exceeds this; must chunk by duration
- `timestamp_granularities=["word"]` requires `response_format="verbose_json"` — using other formats silently drops word timestamps
- Language auto-detection adds ~200ms latency and occasionally misidentifies similar languages (Ukrainian ↔ Russian, Serbian ↔ Croatian)
- Local Whisper large-v3 on CPU takes 5-10x real-time for 1h audio — viable only with GPU (CUDA) for production
- faster-whisper's `vad_filter=True` can silently drop short speech segments under 0.5s (single words, interjections)
- `transcribe_stream()` in the README yields segments as they complete, but the model still processes the full file — it is not true streaming

## Agentic workflow
STT fits into agent pipelines as a preprocessing node: agent receives an audio file path or URL, calls the transcription function, and passes the text to downstream LLM processing (summarization, extraction, classification). Claude subagents can orchestrate the full pipeline: split long audio → transcribe chunks → merge transcripts → analyze. The STT step itself is a single tool call with no LLM reasoning required — use it as a primitive in tool definitions.

### Recommended subagents
- Custom audio pipeline agent — given a media file, split by silence, transcribe each chunk, merge with timestamps, return full transcript
- `faion-sdd-execution` — scaffold a transcript processing pipeline (meeting → action items, podcast → summary)

### Prompt pattern
```
Transcription complete. Full transcript:
---
{transcript}
---
Task: {task_description}
Extract the following structured information: {output_schema}
Return JSON only.
```

```
You have a transcript in segments with timestamps. Language: {language}.
Clean the transcript: fix obvious STT errors, normalize punctuation, remove filler words (um, uh, like).
Keep timestamps. Return corrected transcript in the same segment format.
Input: {segments_json}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | Whisper API: transcription + translation | `pip install openai` · platform.openai.com/docs/guides/speech-to-text |
| `openai-whisper` | Local Whisper model (original) | `pip install openai-whisper` · github.com/openai/whisper |
| `faster-whisper` | CTranslate2-optimized local Whisper; 4x faster | `pip install faster-whisper` · github.com/guillaumekln/faster-whisper |
| `whisperx` | faster-whisper + forced alignment + diarization | `pip install whisperx` · github.com/m-bain/whisperX |
| `pydub` | Audio splitting, format conversion, silence detection | `pip install pydub` · github.com/jiaaro/pydub |
| `ffmpeg` | Audio decoding, resampling, format conversion | System install: `apt install ffmpeg` · ffmpeg.org |
| `deepgram-sdk` | Real-time streaming STT + diarization | `pip install deepgram-sdk` · developers.deepgram.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Whisper API | SaaS | Yes — SDK | $0.006/min; 25MB limit; no streaming; 99 languages |
| Deepgram Nova-2 | SaaS | Yes — WebSocket/REST | Real-time + batch; speaker diarization; $0.0043/min |
| AssemblyAI | SaaS | Yes — SDK | Async batch + streaming; LeMUR for LLM-on-transcript |
| AWS Transcribe | SaaS | Yes — Boto3 | Batch + streaming; custom vocabulary; PII redaction |
| Google Speech-to-Text | SaaS | Yes — Python client | Real-time streaming; 125 languages; telephony model |
| Azure Speech | SaaS | Yes — SDK | Real-time + batch; speaker diarization; custom models |
| faster-whisper | OSS | Yes — Python | Self-hosted; best cost/quality for high volume |

## Templates & scripts
See `templates.md` for `LocalWhisper` and `FasterWhisperTranscriber` classes.

Inline: split audio file into chunks under 24MB before API upload:
```python
from pydub import AudioSegment
import math, os

def split_audio(path: str, chunk_min: int = 10, out_dir: str = "/tmp") -> list[str]:
    """Split audio into chunks of ~chunk_min minutes."""
    audio = AudioSegment.from_file(path)
    chunk_ms = chunk_min * 60 * 1000
    n = math.ceil(len(audio) / chunk_ms)
    paths = []
    for i in range(n):
        chunk = audio[i * chunk_ms:(i + 1) * chunk_ms]
        p = os.path.join(out_dir, f"chunk_{i:03d}.mp3")
        chunk.export(p, format="mp3", bitrate="64k")
        paths.append(p)
    return paths
```

## Best practices
- Always specify `language` parameter explicitly — auto-detection adds latency and can hallucinate in multilingual audio
- Use `verbose_json` format with `timestamp_granularities=["segment"]` for all production work — segment timestamps enable downstream chunking
- For meeting transcription, use WhisperX (local) or AssemblyAI (API) for speaker diarization — standard Whisper cannot distinguish speakers
- Pre-process audio: convert to 16kHz mono WAV, normalize amplitude, apply noise reduction — improves accuracy 5-15%
- Cache transcriptions by audio content hash (SHA-256 of file bytes) — re-transcribing the same file wastes cost and time
- Use `vad_filter=True` in faster-whisper for long files with silence — reduces processing time by 20-40%
- For the Whisper `prompt` parameter: include domain-specific terms, speaker names, and expected vocabulary to reduce substitution errors

## AI-agent gotchas
- Whisper API accepts MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM — not FLAC or OGG; convert before upload
- The `prompt` parameter is prepended to the model context, not searched against the audio — keep it under 100 tokens
- `response.words` from `timestamp_granularities=["word"]` is a list of `Word` objects, not dicts — agents using `json.dumps()` on raw response objects will get `TypeError`
- Local Whisper on CPU with `large-v3` model requires ~10GB RAM; agents running on memory-constrained hosts should use `base` or `small`
- Transcription of code-switching audio (mixed languages per sentence) requires `language=None` + post-processing — explicit language setting forces a single language
- Long transcription jobs via AssemblyAI/AWS are async — agent must poll status URL, not await synchronously

## References
- https://platform.openai.com/docs/guides/speech-to-text
- https://github.com/openai/whisper
- https://github.com/guillaumekln/faster-whisper
- https://github.com/m-bain/whisperX
- https://developers.deepgram.com/docs/getting-started
- https://www.assemblyai.com/docs
