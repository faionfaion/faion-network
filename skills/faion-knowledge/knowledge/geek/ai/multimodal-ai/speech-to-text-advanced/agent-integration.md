# Agent Integration — Speech-to-Text Advanced

## When to use
- Transcribing audio files larger than 25MB (Whisper API limit) via chunked processing
- Meeting transcription where speaker attribution (who said what) is required
- Podcast or interview processing with multi-speaker diarization
- Long-form transcription (1+ hour files) with time-stamped segments
- Building a production STT service with provider fallback (cloud vs local)

## When NOT to use
- Audio is under 25MB and single-speaker — use `speech-to-text-basics` direct API call; `LongAudioTranscriber` adds overhead
- Speaker diarization is needed but GPU is unavailable — `pyannote` on CPU is extremely slow (10× real-time)
- Real-time transcription is needed — Whisper is batch-only; use Deepgram or AssemblyAI streaming for live audio
- Language is non-standard or heavily accented — validate transcription quality first before building automated pipelines around it

## Where it fails / limitations
- `LongAudioTranscriber._transcribe_chunk` returns the full response object, not `response.text` — `_merge_results` then calls `full_text += " " + results[i]["text"]` which concatenates the response object, not the string; this is a bug in the template
- `SpeakerDiarizer` requires HuggingFace token with explicit pyannote model access — requires agreeing to model license at hf.co; access is not automatic
- Overlap strategy in `_split_audio` can duplicate words across chunk boundaries — `_merge_results` does not deduplicate overlapping content
- `TranscriptionService._transcribe_local` delegates to `FasterWhisperTranscriber` and `LocalWhisper` which are referenced but not defined in the template — requires separate implementation
- `word_timestamps` via `timestamp_granularities=["word", "segment"]` requires `response_format="verbose_json"` — the code sets this correctly, but `response.words` uses `getattr` with None default, so missing word timestamps fail silently
- pyannote `speaker-diarization-3.1` model is ~1.5GB download on first run — production deployments must pre-cache the model, not download on first request

## Agentic workflow
An orchestrator agent receives an audio file path and determines processing strategy: if file < 25MB and single-speaker, call OpenAI Whisper directly; if large, route to `LongAudioTranscriber`; if multi-speaker, add `SpeakerDiarizer` after transcription. Results are assembled into a structured transcript with timestamps and optional speaker labels. A review agent validates transcript completeness (non-empty, duration matches) before passing downstream.

### Recommended subagents
- `haiku` — Execute transcription: load file, select strategy, call `TranscriptionService.transcribe()`, return structured result
- `sonnet` — Diarization + alignment: call `SpeakerDiarizer.align_with_transcript()`, format speaker-labeled output
- `sonnet` — Transcript quality check: scan for repeated segments (chunking artifact), flag unusually short transcripts relative to audio duration

### Prompt pattern
```xml
<task>
Transcribe audio file.
Path: {{AUDIO_PATH}}
File size: {{SIZE_MB}}MB
Speakers: {{NUM_SPEAKERS}}  (1 = single, 2+ = diarization needed)
Language: {{LANGUAGE_CODE}}  (null = auto-detect)
Word timestamps: {{BOOL}}

Strategy:
- If size > 25MB: use LongAudioTranscriber
- If speakers > 1: add SpeakerDiarizer after transcription
- Provider: openai (fallback: faster_whisper if local GPU available)

Return: {"text": "...", "segments": [...], "speakers": [...] or null}
</task>
```

```python
# File size routing pattern
def route_transcription(path: str) -> str:
    size_mb = Path(path).stat().st_size / (1024 * 1024)
    if size_mb > 25:
        return "chunked"
    elif size_mb > 5:
        return "standard"
    else:
        return "direct"
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| openai (Python SDK) | Whisper API (whisper-1) | `pip install openai` |
| faster-whisper | Local Whisper with CTranslate2 (faster) | `pip install faster-whisper` |
| pyannote-audio | Speaker diarization | `pip install pyannote.audio` |
| pydub | Audio chunking and format conversion | `pip install pydub` |
| torch | GPU inference for pyannote | `pip install torch` |
| ffmpeg | Audio preprocessing (mono, resample to 16kHz) | `apt install ffmpeg` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Whisper API | SaaS | Yes — Python SDK | 25MB limit; word timestamps; $0.006/min; no real-time |
| Deepgram | SaaS | Yes — REST API | Real-time streaming; speaker diarization; best for live audio |
| AssemblyAI | SaaS | Yes — Python SDK | Speaker diarization; async long audio; PII redaction |
| Groq Whisper | SaaS | Yes — OpenAI-compatible API | 10× faster than OpenAI Whisper; same model; cheap |
| faster-whisper | OSS | Yes — local Python | CTranslate2 backend; 4× faster than openai-whisper on GPU |
| openai-whisper | OSS | Yes — local Python | Reference implementation; slowest; most portable |
| pyannote-audio 3.1 | OSS | Yes — local Python | Best open diarization; requires GPU for reasonable speed |
| WhisperX | OSS | Yes — local Python | Whisper + diarization combined; word-level timestamps |

## Templates & scripts
See `templates.md` for `LongAudioTranscriber`, `SpeakerDiarizer`, `TranscriptionService`.

Bug fix for `_transcribe_chunk` (returns text not response object):
```python
def _transcribe_chunk(self, audio_path: str) -> str:
    with open(audio_path, "rb") as f:
        response = self.client.audio.transcriptions.create(
            model="whisper-1", file=f
        )
    return response.text  # was: return response (object, not string)
```

Audio preprocessing before chunking (normalize to 16kHz mono):
```bash
ffmpeg -i input.mp4 -ar 16000 -ac 1 -c:a pcm_s16le output.wav
```

## Best practices
- Preprocess audio to 16kHz mono WAV before transcription — reduces file size and matches Whisper's training format
- For diarization: run pyannote separately from transcription, then align by timestamp midpoint; do not interleave diarization into transcription loop
- Use `faster-whisper` locally for development and high-volume batch; use OpenAI API for production when GPU is unavailable
- Store word-level timestamps if downstream use requires searchable transcripts or subtitle generation
- For meetings: cap `num_speakers` at actual participant count in pyannote for better separation
- Validate chunk overlap logic: overlapping chunks will produce duplicate content; implement text deduplication on merge
- Cache transcription results by audio file hash (not filename) — re-transcribing identical audio costs real money
- Use `language` parameter when language is known — auto-detect adds ~1s latency and occasionally misidentifies short clips

## AI-agent gotchas
- Whisper API 25MB limit applies to the compressed audio file, not the duration — a 1-hour 64kbps mp3 is ~28MB and will fail; convert to lower bitrate or chunk before calling
- `pyannote` model download on first use (~1.5GB) can fail mid-request in production — pre-cache during container build, not at request time
- `SpeakerDiarizer.align_with_transcript` uses `segment_mid = (start + end) / 2` — if a speaker segment is very short (< 100ms), the midpoint may fall outside the speaker segment due to float rounding; add boundary check
- Whisper output is not punctuated on some audio types — downstream agents processing raw transcript text must not assume sentence structure
- `TranscriptionService` raises `ValueError` on unsupported format, but `supported_formats` defaults to `[".mp3", ".wav", ".m4a", ".flac", ".webm", ".mp4"]` — `.ogg` is a common format not in the list; agents must convert before calling
- Large audio files loaded via pydub hold full PCM in memory — a 2-hour WAV at 16kHz 16-bit is ~230MB in RAM; chunk on disk, not in memory
- Groq Whisper uses the same API format as OpenAI but has stricter file size limits (check current limits); test before routing production traffic

## References
- https://platform.openai.com/docs/guides/speech-to-text
- https://platform.openai.com/docs/api-reference/audio/createTranscription
- https://github.com/pyannote/pyannote-audio
- https://github.com/SYSTRAN/faster-whisper
- https://github.com/m-bain/whisperX
- https://developers.deepgram.com/docs
- https://www.assemblyai.com/docs
- https://groq.com/docs/speech
