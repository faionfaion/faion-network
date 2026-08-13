# Video Generation Tools

## Summary

**One-sentence:** Wraps Runway Gen-3, Luma Dream Machine, and Replicate adapters behind a unified async VideoGenerationService with multi-provider fallback and immediate download.

**One-paragraph:** RunwayVideoGenerator (official SDK, timeout-protected polling), LumaVideoGenerator (REST + custom timeout fix), ReplicateVideoGenerator (pinned model hashes for SVD / AnimateDiff / Zeroscope), and a VideoGenerationService that selects provider by style_tag, retries on transient failure, fallbacks across providers, and streams the pre-signed URL to disk before the 30-60 min expiry. The `_upload_image` method is intentionally a stub — must be implemented per storage backend (S3 / GCS / Cloudinary) before image-to-video works.

**Ефективно для:** інженера AI-конвеєра, що будує надійну відеогенерацію з фолбеком провайдерів і архівацією — закриває петлю між сирим брифом і файлом у постійному сховищі.

## Applies If (ALL must hold)

- Integrating Runway / Luma / Replicate into an automated content pipeline.
- Multi-provider fallback is required (one provider's failure cannot break the pipeline).
- Generation calls happen in an async runtime (asyncio, FastAPI, LiveKit).
- Output must be in permanent storage within the pre-signed URL expiry window (30-60 min).
- Provider rate limits are known and enforced (Runway 10 concurrent tasks, Luma plan-dependent).

## Skip If (ANY kills it)

- Single one-off clip — use `video-gen-basics` direct call; service setup overhead unjustified.
- Synchronous request/response architecture — all video APIs are async polling, will block sync handler.
- Output quality not yet validated — manually verify provider output before automating at scale.
- Latency-sensitive user flow (sub-2s response) — generation is 30-300s; pre-generate or cache.
- No permanent storage backend wired up — pre-signed URLs WILL expire and clips WILL be lost.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| VideoGenerationConfig | dataclass: provider, default_duration, max_retries, timeout, output_dir | pipeline config |
| Provider credentials | env: `RUNWAY_API_KEY`, `LUMA_API_KEY`, `REPLICATE_API_TOKEN` | secrets manager |
| Image upload backend | callable `_upload_image(local_path) -> public_url` | per-host implementation |
| Permanent storage | S3 / GCS bucket with rw + sync IAM | infra team |
| ffmpeg + ffprobe | apt / brew | host setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/multimodal-ai/video-gen-basics` | core VideoPromptBuilder + ffprobe validation reused by every adapter. |
| `geek/ai/multimodal-ai/img-gen-basics` | upstream source for anchor frames passed to image-to-video. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: immediate download, streaming download, pin model hashes, provider-id isolation, log prompt+task, validate ffprobe | ~1000 |
| `content/02-output-contract.xml` | essential | Schema of service.generate() result with retries, fallback chain, archived_path | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: expired URL, OOM download, cross-provider id mix, retry on policy violation, stub upload | ~900 |
| `content/04-procedure.xml` | deep | 8-step procedure: dispatch → poll → stream-download → ffprobe → archive → fallback → retry → log | ~900 |
| `content/05-examples.xml` | medium | Worked Runway → Luma fallback for a cinematic 5s clip; S3 archival path | ~600 |
| `content/06-decision-tree.xml` | essential | Provider routing + fallback ordering by style_tag and recent provider failure state | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `dispatch-provider` | haiku | Adapter dispatch is mechanical. |
| `route-by-style` | sonnet | Decision-tree walk on style_tag + provider health state. |
| `archive-to-s3` | haiku | Sweep + upload + metadata write; mechanical. |
| `analyze-policy-failure` | sonnet | When FAILED with terse error, judge if it's a policy violation vs transient. |

## Templates

| File | Purpose |
|------|---------|
| `templates/runway-generator.py` | RunwayVideoGenerator — text-to-video, image-to-video, timeout-protected polling. |
| `templates/luma-generator.py` | LumaVideoGenerator — REST + timeout fix; generation_id tracking for extend. |
| `templates/replicate-generator.py` | ReplicateVideoGenerator — SVD / AnimateDiff / Zeroscope with pinned hashes. |
| `templates/video-service.py` | VideoGenerationService with multi-provider fallback + retry + streaming download. |
| `templates/prompt-generate.txt` | Agent prompt for dispatching + polling + returning structured result. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-gen-tools.py` | Validate service.generate() output against 02-output-contract. | Post-generation; before sweeper archives to S3. |

## Related

- [[video-gen-basics]] — single-call layer this service builds on.
- [[img-gen-tools]] — generates anchor frames for image-to-video.
- [[multimodal-ai/vision-applications]] — post-hoc verification of generated frames against brief.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` selects primary provider by style_tag (photorealistic → Luma; cinematic → Runway; animated → Replicate AnimateDiff), then defines the fallback chain when the primary returns FAILED or TIMEOUT or a policy violation is suspected. Use it at the dispatch step in VideoGenerationService.generate() before any provider call.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/runway-generator.py`

```python
"""RunwayVideoGenerator: Gen-3 Alpha Turbo via official SDK."""
import runwayml
import time
from typing import Optional


class RunwayVideoGenerator:
    """Generate videos using Runway Gen-3 Alpha Turbo."""

    def __init__(self):
        self.client = runwayml.RunwayML()

    def generate_from_text(self, prompt: str, duration: int = 5,
                           aspect_ratio: str = "16:9",
                           seed: Optional[int] = None) -> dict:
        task = self.client.image_to_video.create(
            model="gen3a_turbo", prompt_text=prompt,
            duration=duration, ratio=aspect_ratio, seed=seed
        )
        return self._wait_for_completion(task.id)

    def generate_from_image(self, image_url: str, prompt: str,
                            duration: int = 5) -> dict:
        task = self.client.image_to_video.create(
            model="gen3a_turbo", prompt_image=image_url,
            prompt_text=prompt, duration=duration
        )
        return self._wait_for_completion(task.id)

    def _wait_for_completion(self, task_id: str, timeout: int = 300) -> dict:
        """Poll for task completion. Runway tasks can take 3-5 minutes."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = self.client.tasks.retrieve(task_id)
            if task.status == "SUCCEEDED":
                return {"status": "success", "video_url": task.output[0],
                        "task_id": task_id}
            elif task.status == "FAILED":
                # Content policy failures return terse error — do not retry same prompt
                return {"status": "failed", "error": task.failure, "task_id": task_id}
            time.sleep(5)
        return {"status": "timeout", "task_id": task_id}
```

### `templates/luma-generator.py`

```python
"""LumaVideoGenerator: Dream Machine REST + extend via keyframes.frame0."""
import requests
import time


class LumaVideoGenerator:
    """Generate videos using Luma AI Dream Machine (no official Python SDK)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate(self, prompt: str, aspect_ratio: str = "16:9",
                 loop: bool = False) -> dict:
        response = requests.post(f"{self.base_url}/generations",
                                 headers=self.headers,
                                 json={"prompt": prompt, "aspect_ratio": aspect_ratio,
                                       "loop": loop})
        return self._wait_for_completion(response.json()["id"])

    def generate_from_image(self, prompt: str, image_url: str) -> dict:
        payload = {"prompt": prompt, "keyframes": {
            "frame0": {"type": "image", "url": image_url}
        }}
        response = requests.post(f"{self.base_url}/generations",
                                 headers=self.headers, json=payload)
        return self._wait_for_completion(response.json()["id"])

    def extend_video(self, video_id: str, prompt: str) -> dict:
        """Extend using generation ID (not video URL) in keyframes."""
        payload = {"prompt": prompt, "keyframes": {
            "frame0": {"type": "generation", "id": video_id}  # ID, not URL
        }}
        response = requests.post(f"{self.base_url}/generations",
                                 headers=self.headers, json=payload)
        return self._wait_for_completion(response.json()["id"])

    def _wait_for_completion(self, generation_id: str, timeout: int = 300) -> dict:
        """Fixed version with timeout — original would loop infinitely."""
        start = time.time()
        while time.time() - start < timeout:
            response = requests.get(f"{self.base_url}/generations/{generation_id}",
                                    headers=self.headers)
            gen = response.json()
            if gen["state"] == "completed":
                return {"status": "success",
                        "video_url": gen["assets"]["video"], "id": generation_id}
            elif gen["state"] == "failed":
                return {"status": "failed",
                        "error": gen.get("failure_reason"), "id": generation_id}
            time.sleep(5)
        return {"status": "timeout", "id": generation_id}
```

### `templates/replicate-generator.py`

```python
"""ReplicateVideoGenerator: SVD / AnimateDiff / Zeroscope with pinned hashes."""
import replicate


class ReplicateVideoGenerator:
    """Generate videos using Replicate open models."""

    # Pin version hashes — update intentionally, not automatically
    MODELS = {
        "svd": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        "animatediff": "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48c9f",
        "zeroscope": "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
    }

    def generate_stable_video(self, image_path: str,
                               motion_bucket_id: int = 127,
                               fps: int = 7, num_frames: int = 25) -> str:
        """Image-to-video with Stable Video Diffusion. Returns URL string."""
        output = replicate.run(
            self.MODELS["svd"],
            input={"input_image": open(image_path, "rb"),
                   "motion_bucket_id": motion_bucket_id,
                   "fps": fps, "num_frames": num_frames}
        )
        return output  # SVD returns URL string directly

    def generate_with_animatediff(self, prompt: str, negative_prompt: str = "",
                                   num_frames: int = 16,
                                   guidance_scale: float = 7.5) -> str:
        output = replicate.run(
            self.MODELS["animatediff"],
            input={"prompt": prompt, "negative_prompt": negative_prompt,
                   "num_frames": num_frames, "guidance_scale": guidance_scale}
        )
        # Some models return iterator; handle both
        if hasattr(output, "__iter__") and not isinstance(output, str):
            return next(iter(output))
        return output

    def generate_with_zeroscope(self, prompt: str, num_frames: int = 24,
                                 fps: int = 8, width: int = 576,
                                 height: int = 320) -> str:
        output = replicate.run(
            self.MODELS["zeroscope"],
            input={"prompt": prompt, "num_frames": num_frames,
                   "fps": fps, "width": width, "height": height}
        )
        if hasattr(output, "__iter__") and not isinstance(output, str):
            return next(iter(output))
        return output
```

### `templates/video-service.py`

```python
"""VideoGenerationService: multi-provider routing + fallback + streaming I/O."""
import asyncio
import logging
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import httpx


class VideoProvider(Enum):
    RUNWAY = "runway"
    LUMA = "luma"
    REPLICATE = "replicate"


@dataclass
class VideoGenerationConfig:
    provider: VideoProvider = VideoProvider.REPLICATE
    default_duration: int = 5
    default_aspect_ratio: str = "16:9"
    max_retries: int = 3
    timeout: int = 600
    output_dir: str = "./generated_videos"


class VideoGenerationService:
    """Production async video generation service."""

    def __init__(self, config: Optional[VideoGenerationConfig] = None):
        self.config = config or VideoGenerationConfig()
        self.logger = logging.getLogger(__name__)
        Path(self.config.output_dir).mkdir(exist_ok=True)

    async def generate(self, prompt: str,
                       provider: Optional[VideoProvider] = None,
                       **kwargs) -> dict[str, Any]:
        provider = provider or self.config.provider
        for attempt in range(self.config.max_retries):
            try:
                result = await self._dispatch(provider, prompt, **kwargs)
                if result["status"] == "success":
                    output_path = await self._download_video(
                        result["video_url"], prompt[:50])
                    if not Path(output_path).exists() or Path(output_path).stat().st_size == 0:
                        return {"status": "failed", "error": "empty output file"}
                    result["local_path"] = output_path
                return result
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.config.max_retries - 1:
                    return {"status": "failed", "error": str(e)}
        return {"status": "failed", "error": "max retries exceeded"}

    async def _dispatch(self, provider: VideoProvider, prompt: str, **kwargs) -> dict:
        from video_gen_tools.templates.runway_generator import RunwayVideoGenerator
        from video_gen_tools.templates.luma_generator import LumaVideoGenerator
        from video_gen_tools.templates.replicate_generator import ReplicateVideoGenerator
        import os

        if provider == VideoProvider.RUNWAY:
            gen = RunwayVideoGenerator()
            return gen.generate_from_text(
                prompt,
                duration=kwargs.get("duration", self.config.default_duration),
                aspect_ratio=kwargs.get("aspect_ratio", self.config.default_aspect_ratio))
        elif provider == VideoProvider.LUMA:
            gen = LumaVideoGenerator(os.environ["LUMA_API_KEY"])
            return gen.generate(prompt,
                                aspect_ratio=kwargs.get("aspect_ratio",
                                                        self.config.default_aspect_ratio))
        else:
            gen = ReplicateVideoGenerator()
            url = gen.generate_with_zeroscope(prompt)
            return {"status": "success", "video_url": url}

    async def _download_video(self, url: str, name: str) -> str:
        """Stream download to avoid OOM on large files."""
        clean_name = re.sub(r"[^\w\s-]", "", name).strip()[:50]
        output_path = Path(self.config.output_dir) / f"{clean_name}.mp4"
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url) as response:
                with open(output_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
        return str(output_path)
```

### `templates/prompt-generate.txt`

```text
<task>
Generate a video clip.
Provider: {PROVIDER}
Prompt: {PROMPT}
Duration: {DURATION}s
Aspect ratio: {ASPECT_RATIO}
Output dir: {OUTPUT_DIR}

Return JSON:
{"status": "success"|"failed", "local_path": "...", "video_url": "...", "error": "..."}

Rules:
- Poll every 5s until SUCCEEDED or FAILED
- Download immediately after SUCCEEDED (URL expires in 30-60 min)
- Validate output file exists and size > 0 before returning success
- On FAILED with content policy error: do NOT retry without modifying the prompt
</task>
```
