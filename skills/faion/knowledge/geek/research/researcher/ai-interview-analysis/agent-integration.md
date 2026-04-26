# Agent Integration — AI-Assisted Interview Analysis

## When to use
- Transcribing recorded user interviews or usability sessions (audio/video files)
- Extracting themes and sentiment across a batch of 5+ interviews in parallel
- Building a research repository searchable by insight, theme, or participant
- Generating cross-interview pattern reports from an existing transcript archive
- Pre-processing transcripts before human thematic analysis to remove mechanical work

## When NOT to use
- When the interview moderation itself needs to be automated — AI cannot facilitate nuanced probing
- When the research question requires nonverbal behavioral data (gaze, hesitation, body language)
- When audio quality is poor (heavy accent + background noise) — transcription accuracy drops below 80%, making analysis unreliable
- When participant confidentiality is high-risk and SaaS tools cannot be used — run local transcription (Whisper) instead
- As a replacement for the researcher's interpretive judgment — themes require human validation before becoming findings

## Where it fails / limitations
- Speaker diarization degrades with 3+ speakers or overlapping speech
- Sentiment analysis accuracy is approximately 80-85%; irony, sarcasm, and cultural nuance are consistently misclassified
- Topic modeling conflates distinct themes when transcripts are short (< 10 minutes per session)
- Insight extraction is text-only; behavioral observations from screen shares or physical usability tests are invisible to the model
- Research tools lock analysis inside proprietary repositories; exporting structured insights for downstream agents requires manual work or API access
- AI-generated summaries sometimes omit low-frequency but high-salience quotes — human review of the full transcript remains essential for key findings

## Agentic workflow
A two-stage pipeline: Haiku handles transcription and speaker tagging from audio or existing transcript files; Sonnet extracts themes, sentiment, and representative quotes per topic; Opus performs cross-interview pattern synthesis and generates the insight report. Human review is required between stages 2 and 3 to validate theme labels before Opus synthesizes patterns across them.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrates multi-stage research pipelines with quality gates between transcription, analysis, and synthesis steps
- General Claude subagent (Haiku) — transcript structuring, speaker segmentation, mechanical sentiment tagging
- General Claude subagent (Sonnet) — theme extraction, quote selection, per-interview summaries
- General Claude subagent (Opus) — cross-interview pattern recognition, insight ranking, report generation

### Prompt pattern
```
Analyze this interview transcript. Extract:
1. Top 5 themes (label + 2-sentence description + 2 representative quotes each)
2. Sentiment per theme: positive / negative / mixed
3. Unmet needs explicitly or implicitly stated
4. One "aha" quote that best represents the core insight

Transcript:
[paste transcript]

Format output as JSON with keys: themes, sentiment_map, unmet_needs, aha_quote.
```

```
You have theme extractions from N interviews: [paste N JSON objects].
Perform cross-interview synthesis:
1. Which themes appear in 3+ interviews? (high confidence)
2. Which appear in only 1 interview? (outlier — flag, do not generalize)
3. What is the single most surprising finding?
4. Draft 3 "How Might We" statements based on top themes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Whisper (OpenAI) | Local audio transcription, no data leaves machine | `pip install openai-whisper` / github.com/openai/whisper |
| whisper.cpp | C++ port of Whisper, faster on CPU, Mac/Linux | github.com/ggerganov/whisper.cpp |
| ffmpeg | Audio preprocessing (noise reduction, format conversion) | `apt install ffmpeg` / ffmpeg.org |
| yt-dlp | Download audio from remote recordings for transcription | `pip install yt-dlp` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Looppanel | SaaS | Partial (API beta) | Best UX research focus; 17 languages; 90%+ accuracy; insight tagging |
| Dovetail | SaaS | Yes (API) | Research repository + highlights API; best for structured knowledge base |
| Insight7 | SaaS | Yes (API) | Bulk upload + theme extraction API; strong for 20+ interview batches |
| UserBit | SaaS | Partial | 50+ languages; speaker ID; limited API exposure |
| Otter.ai | SaaS | Yes (API) | Real-time transcription API; best for live meeting capture |
| Fireflies.ai | SaaS | Yes (API) | Meeting transcription + CRM integration; strongest for sales/CS interviews |
| Descript | SaaS | No | Video editing + transcription; no programmatic access to transcript data |
| AssemblyAI | SaaS | Yes (API) | Transcription + sentiment + entity recognition API; most developer-friendly |

## Templates & scripts
Whisper batch transcription script (Python, inline):
```python
# batch_transcribe.py
import whisper
import json
from pathlib import Path

model = whisper.load_model("base")  # or "medium" for better accuracy

def transcribe_folder(audio_dir: str, out_dir: str) -> None:
    audio_path = Path(audio_dir)
    out_path = Path(out_dir)
    out_path.mkdir(exist_ok=True)

    for audio_file in audio_path.glob("*.{mp3,mp4,m4a,wav}"):
        result = model.transcribe(str(audio_file))
        out_file = out_path / f"{audio_file.stem}.json"
        with open(out_file, "w") as f:
            json.dump({
                "file": audio_file.name,
                "text": result["text"],
                "segments": result["segments"],
            }, f, indent=2)
        print(f"Transcribed: {audio_file.name}")

transcribe_folder("./recordings", "./transcripts")
```

## Best practices
- Pre-process audio with ffmpeg to normalize volume and reduce background noise before transcription — 5 dB improvement in SNR significantly increases accuracy
- Always send a speaker diarization prompt ("Identify each speaker as Speaker 1, Speaker 2...") before theme extraction — mixed-speaker text produces unreliable sentiment
- Use Dovetail or Looppanel as the canonical research repository; run agents against exported transcripts, not against the SaaS UI
- For cross-interview synthesis, analyze interviews independently first, then synthesize — do not feed all transcripts to one agent call; context window limits distort results
- Tag themes with participant count ("3/8 participants mentioned X") so stakeholders can assess confidence without reading raw transcripts
- Never omit minority views; low-frequency but emotionally intense quotes often contain the most actionable insights

## AI-agent gotchas
- Agents lose nuance when given dense 60+ minute transcripts in a single call; chunk by topic or time segment and merge summaries
- Sentiment on research interviews is systematically less useful than in consumer feedback — interview context is formal and positive bias is common; weight behavioral observations over stated sentiment
- LLMs will hallucinate themes that sound plausible but do not appear in the source transcript; require the agent to cite a verbatim quote for every theme it identifies
- Speaker attribution errors in transcription propagate into theme analysis; human spot-check of speaker labels is necessary before synthesis
- Human checkpoint required before finalizing findings: agents cannot distinguish between a genuinely surprising insight and a transcription artifact

## References
- https://looppanel.com/
- https://dovetail.com/
- https://www.assemblyai.com/docs
- https://github.com/openai/whisper
- https://www.nngroup.com/articles/thematic-analysis/
- Portigal, S. — Interviewing Users (2013) — foundational methodology
