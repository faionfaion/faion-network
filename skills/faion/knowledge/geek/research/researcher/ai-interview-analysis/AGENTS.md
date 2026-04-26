# AI-Assisted Interview Analysis

## Summary

A two-stage pipeline for transcribing recorded user interviews and extracting themes, sentiment, and cross-interview patterns at scale. Haiku handles transcription; Sonnet extracts themes per interview; Opus synthesizes patterns across interviews. Human review is required between stages 2 and 3.

## Why

Manual transcription and thematic analysis of 10+ interviews takes days; AI reduces it to hours without removing researcher judgment from the critical step (cross-interview synthesis). Accuracy benchmarks: up to 99% transcription accuracy on good audio, ~80-85% sentiment accuracy — the latter always requires human review.

## When To Use

- Transcribing recorded user interviews or usability sessions (audio/video files).
- Extracting themes and sentiment across a batch of 5+ interviews in parallel.
- Building a research repository searchable by insight, theme, or participant.
- Pre-processing transcripts before human thematic analysis to remove mechanical work.

## When NOT To Use

- When audio quality is poor (heavy accent + background noise) — accuracy drops below 80%.
- When the research question requires nonverbal data (gaze, hesitation, body language).
- When participant confidentiality is high-risk and SaaS tools cannot be used — use local Whisper.
- As a replacement for the researcher's interpretive judgment — themes require human validation.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-landscape.xml` | Transcription and analysis tool comparison, accuracy benchmarks, limitations. |
| `content/02-agent-workflow.xml` | Three-stage pipeline rules, prompt patterns, gotchas, best practices. |

## Templates

| File | Purpose |
|------|---------|
| `templates/batch-transcribe.py` | Whisper batch transcription: folder of audio files → JSON transcripts. |
| `templates/analysis-prompt.txt` | Prompt for per-interview theme extraction + cross-interview synthesis. |
