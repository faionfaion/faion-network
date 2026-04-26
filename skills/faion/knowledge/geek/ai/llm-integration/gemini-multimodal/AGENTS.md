# Gemini Multimodal

## Summary

Patterns for Gemini's native multimodal capabilities: images (JPG/PNG/WEBP/HEIC, 20MB), video (MP4/MOV/AVI up to 2GB with async polling), audio (MP3/WAV/FLAC, 100MB), PDFs (100MB), and Python code execution sandbox. Includes context caching for documents queried repeatedly and Vertex AI enterprise integration. The core rule: use GCS URIs instead of SDK uploads for large or persistent files; always guard the video-processing polling loop with a max-iteration timeout.

## Why

Gemini is the only frontier model with native video understanding (no frame extraction), native audio processing (no separate Whisper call), and a 2M-token context window. For multi-document pipelines, context caching cuts costs 75% vs. full-price per call. Without the polling guard and file-expiry handler, agents loop indefinitely or silently re-upload duplicate files.

## When To Use

- Processing video natively — no frame extraction or separate transcription pipeline needed
- Audio transcription and analysis without a separate Whisper call
- Long document pipelines — 2M token context handles books, large codebases, multi-document sets
- Combined modality tasks: video + PDF slides, image + audio explanation, multiple images compared
- Code execution tasks where the model must compute and return results
- Enterprise Google Cloud deployments requiring CMEK, VPC Service Controls, IAM (Vertex AI)

## When NOT To Use

- Simple text-only tasks — adds SDK complexity if already on OpenAI/Anthropic
- When maximum reasoning depth matters — Claude Opus and o1 outperform Gemini on complex multi-step reasoning
- Privacy-sensitive content that cannot leave on-premises — Gemini requires upload to Google servers
- Low-latency real-time voice — Gemini Live API is more complex than OpenAI Realtime API
- Teams with deep OpenAI or Anthropic expertise — switching SDK adds friction for marginal gains on text tasks

## Content

| File | What's inside |
|------|---------------|
| `content/01-modalities.xml` | Image, video, audio, PDF upload patterns; supported formats and size limits; combined modality examples |
| `content/02-video-async.xml` | Video upload state machine (upload → poll → analyze), timeout guard, ACTIVE/FAILED state handling |
| `content/03-context-caching.xml` | Cache creation (32K minimum), TTL management, cost comparison (75% cheaper), listing and deleting caches |
| `content/04-code-execution.xml` | Python sandbox setup, accessing executable_code and code_execution_result parts, data analysis pattern |
| `content/05-vertex-ai.xml` | Vertex AI setup, GCS URI multimodal, enterprise features table, tuned model access |

## Templates

| File | Purpose |
|------|---------|
| `templates/analyze-video.py` | Async-safe video upload + polling + analysis function with max-iteration guard |
| `templates/context-cache.py` | Context cache create/use/manage pattern for repeated document queries |
