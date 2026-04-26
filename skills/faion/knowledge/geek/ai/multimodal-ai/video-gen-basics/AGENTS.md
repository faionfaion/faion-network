# Video Generation Basics

## Summary

Generating short video clips from text or image input using Runway, Luma, Replicate, or Pika. Covers service comparison, VideoPromptBuilder for structured prompt construction, ffmpeg utilities for post-processing, and the async generation polling pattern.

## Why

AI video generation is inherently async (30–300s per clip) and requires structured prompt construction to control motion, camera movement, style, and lighting. Vague prompts produce random camera movements; explicit fields are the primary quality lever.

## When To Use

- Generating short marketing or social media videos from text descriptions
- Animating static product images into demo clips
- Prototyping visual content before committing to full production
- Creating background loops or b-roll for video pipelines
- Automating video content in content pipelines

## When NOT To Use

- Precise temporal control needed (specific actions at specific timestamps) — current models cannot enforce this
- Character consistency across multiple shots is mandatory — models drift between generations
- Videos longer than 10–15 seconds without chaining — extend or concatenate via ffmpeg
- Real-time generation required — generation takes 30–300s per clip; not user-interactive

## Content

| File | What's inside |
|------|---------------|
| `content/01-services.xml` | Service comparison table (Runway, Luma, Pika, Replicate, Sora), generation type matrix |
| `content/02-prompt-and-process.xml` | VideoPromptBuilder fluent API; VideoProcessor ffmpeg utilities; rules for prompt structure |

## Templates

| File | Purpose |
|------|---------|
| `templates/video-prompt-builder.py` | VideoPromptBuilder with subject/action/camera/style/lighting fields |
| `templates/video-processor.py` | VideoProcessor: extract frames, concat, resize, add audio |
| `templates/concat-clips.sh` | ffmpeg concat bash helper |
