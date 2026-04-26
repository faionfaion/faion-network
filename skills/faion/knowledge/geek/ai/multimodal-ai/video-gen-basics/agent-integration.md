# Agent Integration — Video Generation Basics

## When to use
- Generating short marketing or social media videos from text descriptions
- Animating static product images into demo clips
- Prototyping visual content before committing to full video production
- Creating background loops or b-roll for video pipelines
- Automating video content for content pipelines (news, social, educational)

## When NOT to use
- Precise temporal control is required (specific actions at specific timestamps)
- Character consistency across multiple shots is mandatory — current models drift
- Videos longer than 10–15 seconds are needed without chaining/extending
- Lip-sync accuracy matters for spokesperson content
- Real-time generation is required — generation takes 30–300s per clip

## Where it fails / limitations
- No semantic consistency across separate generations (different clips, different lighting/faces)
- Motion physics fails for fluid dynamics, complex cloth, crowds
- Text rendering in video is unreliable across all current models
- Hands/fingers deform during motion
- Generation costs are high ($0.05–$0.50/clip); iteration loops burn budget quickly
- Long-form continuity: concatenated clips have visible seam artifacts
- API availability is gated (Sora is invite-only as of Q2 2026; Runway/Luma have rate limits)

## Agentic workflow
A Claude subagent receives a content brief and uses `VideoPromptBuilder` to construct a structured prompt with explicit motion, camera, style, and lighting fields. The subagent calls the video generation API, polls for completion, downloads the clip, then passes it to a post-processing step (ffmpeg) for trimming or concatenation. For multi-clip sequences, an orchestrator agent breaks the brief into shots, dispatches parallel generation calls, then assembles via ffmpeg concat.

### Recommended subagents
- `haiku` — API dispatch: submit generation job, poll status, download result
- `sonnet` — Prompt engineering: translate brief → structured VideoPromptBuilder call with camera/motion/style choices
- `sonnet` — Pipeline design: multi-shot breakdown, clip sequencing, quality review loop

### Prompt pattern
```
You are a video prompt engineer. Given this brief:
<brief>{{CONTENT_BRIEF}}</brief>

Build a VideoPromptBuilder call specifying:
- subject (what/who)
- action (motion verbs)
- camera (from: static, pan_left, pan_right, dolly_in, dolly_out, tracking, crane, drone, orbit)
- style (cinematic/documentary/commercial/realistic)
- lighting (golden_hour/studio/dramatic/natural)
- duration: {{SECONDS}}s
Return Python code only.
```

```
Poll task {{TASK_ID}} every 5s. On SUCCEEDED: download video_url to ./output/{{SLUG}}.mp4 and return {"status":"ok","path":"..."}. On FAILED: return {"status":"error","reason":"..."}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| ffmpeg | Frame extraction, concat, resize, audio merge | `apt install ffmpeg` / ffmpeg.org |
| ffprobe | Video metadata inspection | Bundled with ffmpeg |
| yt-dlp | Download reference videos for img2video input | `pip install yt-dlp` |
| imageio | Frame-level video I/O in Python | `pip install imageio[ffmpeg]` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Runway Gen-3 Alpha Turbo | SaaS | Yes — REST API + Python SDK | Best cost/quality; 5–10s clips; `pip install runwayml` |
| Luma Dream Machine | SaaS | Yes — REST API | Video extend feature useful for chaining; 5s clips |
| Replicate (Stable Video Diffusion, AnimateDiff, Zeroscope) | SaaS | Yes — Python SDK | Open models, cheaper, lower quality; good for testing |
| Pika 2.0 | SaaS | Partial — web UI + unofficial API | 4s clips; strong for img2video |
| Kling | SaaS | Yes — REST API | Strong motion quality; Chinese service, latency varies |
| OpenAI Sora | SaaS | Limited — invite-only | Highest quality; no public API as of Q2 2026 |
| ComfyUI + SVD | OSS | Yes — local REST server | Self-hosted; GPU required (12GB+ VRAM); high latency |

## Templates & scripts
See `templates.md` for VideoPromptBuilder and VideoProcessor full implementations.

Inline: ffmpeg concat helper (10 lines):
```bash
#!/bin/bash
# concat_clips.sh — concatenate clips listed in clips.txt
# clips.txt format: one file path per line
while IFS= read -r f; do echo "file '$f'"; done < clips.txt > /tmp/concat_list.txt
ffmpeg -f concat -safe 0 -i /tmp/concat_list.txt -c copy "${1:-output.mp4}"
```

## Best practices
- Always specify camera movement explicitly — omitting it produces random/shaky camera
- Use image-to-video instead of text-to-video when subject consistency matters
- Generate 3+ variations per shot; selection is cheaper than re-prompting after review
- Keep individual clips under 5s for maximum quality; chain via ffmpeg for longer sequences
- Cache generated clips by prompt hash; video generation is expensive and deterministic at fixed seed
- For social: generate at native 9:16 by setting aspect_ratio parameter, not by cropping 16:9
- Run ffprobe on outputs before downstream processing to catch silent failures (0-byte files)
- Store seed values with each clip; they enable near-identical regeneration with minor prompt tweaks

## AI-agent gotchas
- Generation is async — never block on a synchronous call; always poll with timeout and expose status
- API timeout ≠ failure: Runway tasks can take 3–5 minutes; 30s HTTP timeout will false-fail
- Video URL expiry: Runway/Luma pre-signed URLs expire in ~1 hour; download immediately after SUCCEEDED
- Content policy: abstract violence, brand logos, and real faces trigger refusals silently (returns FAILED with no useful error)
- Seed reproducibility is provider-specific — same seed on Luma vs Runway yields completely different outputs
- The `revised_prompt` analog doesn't exist for video APIs; what-you-prompt-is-what-runs, so validate prompts before submitting
- Agent must not attempt to read/stream video content inline — download to disk first, then pass path to ffprobe/ffmpeg
- Rate limits are per-minute not per-day on most providers; batch submissions need exponential backoff

## References
- https://runwayml.com/api
- https://lumalabs.ai/dream-machine/api
- https://replicate.com/collections/video-generation
- https://stability.ai/stable-video
- https://ffmpeg.org/documentation.html
- https://pika.art/home
