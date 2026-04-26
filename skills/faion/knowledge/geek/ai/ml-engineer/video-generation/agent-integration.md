# Agent Integration — Video Generation

## When to use
- Automated content pipelines that need short video clips from text scripts (news, social media)
- Talking-head video generation with lip-sync for explainer or marketing content
- Image animation: converting static product images to motion assets
- B-roll generation for long-form video without stock footage licensing
- Prototype video ads or storyboards before committing to human production

## When NOT to use
- Precise character consistency across multiple shots required — current models drift
- Video longer than 60 seconds from a single call — all current APIs cap at 5-60s per generation
- Budget is constrained: video generation is expensive ($0.05-$0.50 per second of output)
- Real-time generation needed (<30s turnaround) — all providers are async, typically 60-300s
- Licensed character or brand content: generated video may violate IP rights

## Where it fails / limitations
- Physics simulation is poor: liquid, smoke, hands, and complex multi-object interactions degrade quickly
- Character consistency across cuts requires careful prompt repetition and image seeding — still unreliable
- Native audio (Sora 2, Veo 3) cannot be controlled: voices, accents, and content are non-deterministic
- 4K from Veo 3 requires Vertex AI access — not available as a self-service API to most developers (2026)
- Runway Gen-3 lip-sync works only with a frontal face image + clear audio track; off-angle faces fail
- All providers are async: generation takes 60-300s; agent must poll, not block

## Agentic workflow
A subagent receives a script or text prompt, selects the appropriate provider based on task requirements (lip-sync → Runway; long-form → Sora; budget → Luma), submits the generation job, polls for completion with exponential backoff, downloads the video file, and passes it to a downstream agent for assembly or publishing. For multi-clip projects, the agent generates clips in parallel and assembles with ffmpeg. Human review is required before publishing any generated video.

### Recommended subagents
- `faion-sdd-executor-agent` — drives multi-step video pipeline as sequential tasks

### Prompt pattern
```
# Task: Generate a 5-second B-roll clip
Provider: Runway Gen-3 Alpha
Style: Cinematic, shallow depth of field
Motion: Slow pan left
Subject: {subject_description}
Lighting: Golden hour, warm tones
Avoid: Text, faces, logos
```

```python
# Runway Gen-3 API — async job with polling
import httpx, time, os

RUNWAY_KEY = os.environ["RUNWAY_API_KEY"]

def generate_video(prompt: str, image_url: str | None = None) -> str:
    """Submit generation job, poll until done, return video URL."""
    payload = {"prompt": prompt, "model": "gen3a_turbo", "duration": 5}
    if image_url:
        payload["image_as_end_frame"] = False
        payload["init_image"] = image_url

    r = httpx.post(
        "https://api.dev.runwayml.com/v1/image_to_video",
        headers={"Authorization": f"Bearer {RUNWAY_KEY}"},
        json=payload, timeout=30
    )
    job_id = r.json()["id"]

    for _ in range(60):  # max 10 minutes
        time.sleep(10)
        status = httpx.get(
            f"https://api.dev.runwayml.com/v1/tasks/{job_id}",
            headers={"Authorization": f"Bearer {RUNWAY_KEY}"}
        ).json()
        if status["status"] == "SUCCEEDED":
            return status["output"][0]
        if status["status"] == "FAILED":
            raise RuntimeError(f"Video generation failed: {status.get('failure')}")
    raise TimeoutError("Video generation timed out after 10 minutes")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `runwayml` Python SDK | Runway Gen-3 API | `pip install runwayml` / runwayml.com/api |
| `lumaai` Python SDK | Luma Dream Machine API | `pip install lumaai` / lumalabs.ai/api |
| `replicate` Python SDK | Open-source video models (CogVideoX, AnimateDiff) | `pip install replicate` / replicate.com |
| `ffmpeg` | Video assembly, format conversion, concat | system package / ffmpeg.org |
| `moviepy` | Python video editing (trim, overlay, concat) | `pip install moviepy` / zulko.github.io/moviepy |
| `httpx` | Async HTTP for provider polling loops | `pip install httpx` / python-httpx.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Runway ML | SaaS | Yes | Public REST API; Gen-3 Alpha; lip-sync; video-to-video |
| Luma AI | SaaS | Yes | Public API; Dream Machine; image animation; video extension |
| Replicate | SaaS | Yes | API for 50+ open video models; pay per generation |
| Kling | SaaS | Yes | Credits-based API; 10s @ 1080p; competitive quality |
| Stability AI (Stable Video) | SaaS | Yes | Image-to-video; lower cost than Runway |
| OpenAI Sora | SaaS | Partial | API limited to ChatGPT Pro subscribers as of 2026 |
| Google Veo 3 | SaaS | Partial | Via Vertex AI; enterprise access required for 4K |

## Templates & scripts
See `templates.md` for full Runway + Luma production service templates.

Multi-clip parallel assembly:

```python
import asyncio, httpx, subprocess
from pathlib import Path

async def fetch_clip(url: str, out_path: str) -> None:
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        Path(out_path).write_bytes(r.content)

def concat_clips(paths: list[str], output: str) -> None:
    list_file = "concat_list.txt"
    with open(list_file, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")
    subprocess.run(
        ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file,
         "-c", "copy", output, "-y"],
        check=True
    )
```

## Best practices
- Write prompts in the style native to the provider: Runway prefers cinematic camera directions; Luma prefers descriptive scene prose
- Always specify "no text, no logos" explicitly in prompts to avoid content policy triggers and visual noise
- Seed with a reference image (image-to-video) for character consistency — text-only produces higher variance
- Generate at provider-native duration (5-10s); assemble longer videos with ffmpeg concat
- Cache video files by prompt hash — regeneration costs the same; avoid unnecessary regeneration
- Monitor per-generation cost: add a cost estimate log before every job submission
- Never publish AI-generated video without a review step for accuracy, brand fit, and policy compliance

## AI-agent gotchas
- All providers are async with 60-300s latency; agent must never block synchronously — use polling with timeout
- Runway returns a task ID on submission; status polling endpoint is separate from submission endpoint
- Generation failures can be silent (status: FAILED with empty failure message) — always log raw response
- Parallel generation of many clips may hit provider rate limits; implement per-provider rate limiting
- Video URLs from Runway/Luma expire (typically 24-72h) — download immediately after completion, do not store URLs
- Human review checkpoint before any public video publication — AI video can contain unexpected content

## References
- https://runwayml.com/api
- https://lumalabs.ai/api
- https://replicate.com/collections/video-generation
- https://deepmind.google/technologies/veo/
- https://openai.com/index/sora/
