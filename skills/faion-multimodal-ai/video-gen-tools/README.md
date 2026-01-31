---
id: video-gen-tools
name: "Video Generation Tools"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Video Generation Tools

API integrations and service implementations for AI video generation.

## Runway Gen-3 Integration

```python
import runwayml
from typing import Optional
import time

class RunwayVideoGenerator:
    """Generate videos using Runway Gen-3."""

    def __init__(self):
        self.client = runwayml.RunwayML()

    def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,  # seconds
        aspect_ratio: str = "16:9",
        seed: Optional[int] = None
    ) -> dict:
        """Generate video from text prompt."""
        task = self.client.image_to_video.create(
            model="gen3a_turbo",
            prompt_text=prompt,
            duration=duration,
            ratio=aspect_ratio,
            seed=seed
        )

        return self._wait_for_completion(task.id)

    def generate_from_image(
        self,
        image_url: str,
        prompt: str,
        duration: int = 5,
        motion_intensity: float = 0.5
    ) -> dict:
        """Generate video from image + prompt."""
        task = self.client.image_to_video.create(
            model="gen3a_turbo",
            prompt_image=image_url,
            prompt_text=prompt,
            duration=duration
        )

        return self._wait_for_completion(task.id)

    def _wait_for_completion(
        self,
        task_id: str,
        timeout: int = 300
    ) -> dict:
        """Poll for task completion."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            task = self.client.tasks.retrieve(task_id)

            if task.status == "SUCCEEDED":
                return {
                    "status": "success",
                    "video_url": task.output[0],
                    "task_id": task_id
                }
            elif task.status == "FAILED":
                return {
                    "status": "failed",
                    "error": task.failure,
                    "task_id": task_id
                }

            time.sleep(5)

        return {
            "status": "timeout",
            "task_id": task_id
        }
```

## Replicate Video Models

```python
import replicate
from typing import List, Optional

class ReplicateVideoGenerator:
    """Generate videos using Replicate models."""

    def generate_stable_video(
        self,
        image_path: str,
        motion_bucket_id: int = 127,
        fps: int = 7,
        num_frames: int = 25
    ) -> str:
        """Generate video from image using Stable Video Diffusion."""
        output = replicate.run(
            "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
            input={
                "input_image": open(image_path, "rb"),
                "motion_bucket_id": motion_bucket_id,
                "fps": fps,
                "num_frames": num_frames
            }
        )
        return output

    def generate_with_animatediff(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_frames: int = 16,
        guidance_scale: float = 7.5
    ) -> str:
        """Generate video using AnimateDiff."""
        output = replicate.run(
            "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48c9f",
            input={
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_frames": num_frames,
                "guidance_scale": guidance_scale
            }
        )
        return output

    def generate_with_zeroscope(
        self,
        prompt: str,
        num_frames: int = 24,
        fps: int = 8,
        width: int = 576,
        height: int = 320
    ) -> str:
        """Generate video using Zeroscope."""
        output = replicate.run(
            "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
            input={
                "prompt": prompt,
                "num_frames": num_frames,
                "fps": fps,
                "width": width,
                "height": height
            }
        )
        return output
```

## Luma Dream Machine

```python
import requests
from typing import Optional
import time

class LumaVideoGenerator:
    """Generate videos using Luma AI Dream Machine."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        loop: bool = False
    ) -> dict:
        """Generate video from text prompt."""
        response = requests.post(
            f"{self.base_url}/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "loop": loop
            }
        )

        generation = response.json()
        return self._wait_for_completion(generation["id"])

    def generate_from_image(
        self,
        prompt: str,
        image_url: str,
        keyframes: dict = None
    ) -> dict:
        """Generate video from image."""
        payload = {
            "prompt": prompt,
            "keyframes": {
                "frame0": {
                    "type": "image",
                    "url": image_url
                }
            }
        }

        if keyframes:
            payload["keyframes"].update(keyframes)

        response = requests.post(
            f"{self.base_url}/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload
        )

        return self._wait_for_completion(response.json()["id"])

    def extend_video(
        self,
        video_id: str,
        prompt: str
    ) -> dict:
        """Extend existing video."""
        response = requests.post(
            f"{self.base_url}/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "prompt": prompt,
                "keyframes": {
                    "frame0": {
                        "type": "generation",
                        "id": video_id
                    }
                }
            }
        )

        return self._wait_for_completion(response.json()["id"])

    def _wait_for_completion(self, generation_id: str) -> dict:
        """Wait for video generation to complete."""
        while True:
            response = requests.get(
                f"{self.base_url}/generations/{generation_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )

            generation = response.json()

            if generation["state"] == "completed":
                return {
                    "status": "success",
                    "video_url": generation["assets"]["video"],
                    "id": generation_id
                }
            elif generation["state"] == "failed":
                return {
                    "status": "failed",
                    "error": generation.get("failure_reason"),
                    "id": generation_id
                }

            time.sleep(5)
```

## Production Video Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from enum import Enum
import logging
import asyncio

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
    """Production video generation service."""

    def __init__(self, config: Optional[VideoGenerationConfig] = None):
        self.config = config or VideoGenerationConfig()
        self.logger = logging.getLogger(__name__)
        Path(self.config.output_dir).mkdir(exist_ok=True)

    async def generate(
        self,
        prompt: str,
        provider: Optional[VideoProvider] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate video from prompt."""
        provider = provider or self.config.provider

        for attempt in range(self.config.max_retries):
            try:
                if provider == VideoProvider.RUNWAY:
                    result = await self._generate_runway(prompt, **kwargs)
                elif provider == VideoProvider.LUMA:
                    result = await self._generate_luma(prompt, **kwargs)
                else:
                    result = await self._generate_replicate(prompt, **kwargs)

                if result["status"] == "success":
                    # Download video
                    output_path = await self._download_video(
                        result["video_url"],
                        prompt[:50]
                    )
                    result["local_path"] = output_path

                return result

            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.config.max_retries - 1:
                    return {"status": "failed", "error": str(e)}

        return {"status": "failed", "error": "Max retries exceeded"}

    async def generate_from_image(
        self,
        image_path: str,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate video from image."""
        image_url = await self._upload_image(image_path)

        return await self.generate(
            prompt,
            image_url=image_url,
            **kwargs
        )

    async def _generate_runway(self, prompt: str, **kwargs) -> Dict:
        """Generate using Runway."""
        generator = RunwayVideoGenerator()
        return generator.generate_from_text(
            prompt,
            duration=kwargs.get("duration", self.config.default_duration),
            aspect_ratio=kwargs.get("aspect_ratio", self.config.default_aspect_ratio)
        )

    async def _generate_luma(self, prompt: str, **kwargs) -> Dict:
        """Generate using Luma."""
        import os
        generator = LumaVideoGenerator(os.environ.get("LUMA_API_KEY"))
        return generator.generate(
            prompt,
            aspect_ratio=kwargs.get("aspect_ratio", self.config.default_aspect_ratio)
        )

    async def _generate_replicate(self, prompt: str, **kwargs) -> Dict:
        """Generate using Replicate."""
        generator = ReplicateVideoGenerator()
        video_url = generator.generate_with_zeroscope(prompt)
        return {"status": "success", "video_url": video_url}

    async def _download_video(self, url: str, name: str) -> str:
        """Download video from URL."""
        import httpx
        import re

        clean_name = re.sub(r'[^\w\s-]', '', name).strip()[:50]
        output_path = Path(self.config.output_dir) / f"{clean_name}.mp4"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            with open(output_path, "wb") as f:
                f.write(response.content)

        return str(output_path)

    async def _upload_image(self, image_path: str) -> str:
        """Upload image and get URL."""
        # Implementation depends on storage service
        # Could use S3, Cloudinary, etc.
        pass

    async def extend_video(
        self,
        video_path: str,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Extend existing video."""
        from video_gen_basics import VideoProcessor

        processor = VideoProcessor()
        frames_dir = "/tmp/extend_frames"
        frames = processor.extract_frames(video_path, frames_dir, fps=1)

        if not frames:
            return {"status": "failed", "error": "Could not extract frames"}

        last_frame = str(frames[-1])

        result = await self.generate_from_image(last_frame, prompt, **kwargs)

        if result["status"] == "success":
            output_path = str(Path(video_path).with_suffix(".extended.mp4"))
            processor.concatenate_videos(
                [video_path, result["local_path"]],
                output_path
            )
            result["extended_path"] = output_path

        return result
```

## Usage Examples

### Runway Gen-3

```python
runway = RunwayVideoGenerator()

result = runway.generate_from_text(
    prompt="A golden retriever running through sunflowers",
    duration=5,
    aspect_ratio="16:9"
)

print(result["video_url"])
```

### Luma Dream Machine

```python
luma = LumaVideoGenerator(api_key="your-api-key")

result = luma.generate(
    prompt="Cinematic drone shot of a mountain landscape",
    aspect_ratio="16:9",
    loop=False
)

print(result["video_url"])
```

### Production Service

```python
import asyncio

config = VideoGenerationConfig(
    provider=VideoProvider.LUMA,
    output_dir="./videos"
)

service = VideoGenerationService(config)

async def main():
    result = await service.generate(
        "A serene lake at sunset with mountains in background"
    )
    print(f"Video saved to: {result['local_path']}")

asyncio.run(main())
```

## See Also

- [video-gen-basics.md](video-gen-basics.md) - Concepts and prompt engineering

## References

- [Runway ML API](https://runwayml.com/api)
- [Luma AI API](https://lumalabs.ai/api)
- [Replicate Models](https://replicate.com/collections/video-generation)
