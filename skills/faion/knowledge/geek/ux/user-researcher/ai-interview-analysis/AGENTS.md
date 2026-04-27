# AI-Assisted Interview Analysis

## Summary

Use AI to automate transcript processing and cross-interview theme extraction. A local or cloud transcription model (Whisper, AssemblyAI) converts recordings to text, then a Claude agent segments speakers, extracts themes supported by verbatim quotes, scores sentiment, and produces a cross-interview pattern report. The human researcher reviews and interprets; the agent handles volume.

## Why

Manual transcription and analysis of 5+ interview sessions takes days. AI transcription runs in minutes with 90%+ accuracy on clear audio, and theme extraction with forced quote-grounding eliminates unsupported assertions. The result: researchers spend time on interpretation, not mechanical coding.

## When To Use

- Processing 5+ interview recordings where manual transcription/analysis would take days
- Extracting cross-interview themes for affinity diagramming or synthesis reporting
- Generating first-pass summaries of individual sessions before researcher review
- Running sentiment scoring on large transcript corpora to prioritize review order
- Producing pattern reports as input for product team debriefs

## When NOT To Use

- Single sessions where a researcher can take notes live — no meaningful speed gain
- Moderated usability studies where in-session facilitator judgment is the core deliverable
- Studies involving sensitive disclosures (health, legal) without explicit AI-processing consent
- High-stakes research where hesitation, emotional cues, or nonverbal behavior are critical — AI is text-only
- Any pipeline where AI output goes to stakeholders without researcher review

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-stack.xml` | Transcription services, tool comparison, accuracy benchmarks, data residency notes |
| `content/02-analysis-workflow.xml` | Step-by-step pipeline: transcribe → segment → extract themes → validate; rules for quote grounding and confidence annotation |
| `content/03-anti-patterns.xml` | Agent gotchas: hallucinated themes, long-transcript chunking, demographic inference, GDPR compliance |

## Templates

| File | Purpose |
|------|---------|
| `templates/transcribe-and-extract.py` | Full pipeline: audio → Whisper transcription → Claude theme extraction |
| `templates/prompt-theme-extraction.txt` | Claude system+user prompt for cross-interview theme analysis |
| `templates/prompt-single-interview.txt` | Prompt for structured single-session summary |
