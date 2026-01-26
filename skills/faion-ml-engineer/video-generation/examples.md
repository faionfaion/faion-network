# Video Generation Examples

Production-ready code examples for AI video generation APIs.

## Runway Gen-3 Alpha

### Installation

```bash
pip install runwayml
```

### Text-to-Video

```python
import runwayml
from typing import Optional
import time

class RunwayVideoGenerator:
    """Generate videos using Runway Gen-3 Alpha."""

    def __init__(self):
        self.client = runwayml.RunwayML()

    def generate_from_text(
        self,
        prompt: str,
        duration: int = 5,  # 5 or 10 seconds
        aspect_ratio: str = "16:9",  # 16:9, 9:16, 1:1
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
        duration: int = 5
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

        return {"status": "timeout", "task_id": task_id}


# Usage
runway = RunwayVideoGenerator()

result = runway.generate_from_text(
    prompt="A golden retriever running through sunflowers, cinematic lighting",
    duration=5,
    aspect_ratio="16:9"
)

print(result["video_url"])
```

## Luma Dream Machine

### Text-to-Video

```python
import requests
import time
from typing import Optional

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
        response.raise_for_status()

        generation = response.json()
        return self._wait_for_completion(generation["id"])

    def generate_from_image(
        self,
        prompt: str,
        image_url: str,
        end_image_url: Optional[str] = None
    ) -> dict:
        """Generate video from image(s)."""
        keyframes = {
            "frame0": {
                "type": "image",
                "url": image_url
            }
        }

        if end_image_url:
            keyframes["frame1"] = {
                "type": "image",
                "url": end_image_url
            }

        response = requests.post(
            f"{self.base_url}/generations",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "prompt": prompt,
                "keyframes": keyframes
            }
        )
        response.raise_for_status()

        return self._wait_for_completion(response.json()["id"])

    def extend_video(
        self,
        video_id: str,
        prompt: str
    ) -> dict:
        """Extend existing video with continuation."""
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
        response.raise_for_status()

        return self._wait_for_completion(response.json()["id"])

    def _wait_for_completion(self, generation_id: str) -> dict:
        """Wait for video generation to complete."""
        while True:
            response = requests.get(
                f"{self.base_url}/generations/{generation_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()

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


# Usage
import os

luma = LumaVideoGenerator(api_key=os.environ["LUMA_API_KEY"])

result = luma.generate(
    prompt="Cinematic drone shot of a mountain landscape at golden hour",
    aspect_ratio="16:9",
    loop=False
)

print(result["video_url"])
```

## Replicate Models

### Stable Video Diffusion

```python
import replicate
from typing import Optional

class ReplicateVideoGenerator:
    """Generate videos using Replicate models."""

    def generate_stable_video(
        self,
        image_path: str,
        motion_bucket_id: int = 127,  # 1-255, higher = more motion
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
        negative_prompt: str = "blurry, low quality",
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
        """Generate video using Zeroscope v2."""
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


# Usage
generator = ReplicateVideoGenerator()

# From image
video_url = generator.generate_stable_video(
    image_path="./input.jpg",
    motion_bucket_id=127,
    fps=7
)

# From text
video_url = generator.generate_with_animatediff(
    prompt="A cat walking on a beach, cinematic",
    num_frames=16
)
```

## Async Example with httpx

```python
import httpx
import asyncio
from typing import Optional

class AsyncLumaGenerator:
    """Async Luma Dream Machine client."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"

    async def generate(
        self,
        prompt: str,
        aspect_ratio: str = "16:9"
    ) -> dict:
        """Generate video asynchronously."""
        async with httpx.AsyncClient() as client:
            # Start generation
            response = await client.post(
                f"{self.base_url}/generations",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio
                }
            )
            response.raise_for_status()
            generation_id = response.json()["id"]

            # Poll for completion
            while True:
                response = await client.get(
                    f"{self.base_url}/generations/{generation_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                data = response.json()

                if data["state"] == "completed":
                    return {
                        "status": "success",
                        "video_url": data["assets"]["video"]
                    }
                elif data["state"] == "failed":
                    return {
                        "status": "failed",
                        "error": data.get("failure_reason")
                    }

                await asyncio.sleep(5)


# Usage
async def main():
    generator = AsyncLumaGenerator(api_key="your-api-key")

    # Generate multiple videos concurrently
    prompts = [
        "A sunset over the ocean",
        "A city street at night",
        "A forest with morning mist"
    ]

    tasks = [generator.generate(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)

    for prompt, result in zip(prompts, results):
        print(f"{prompt}: {result['video_url']}")

asyncio.run(main())
```

## Webhook Integration

```python
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.post("/webhook/runway")
async def runway_webhook(request: Request):
    """Handle Runway completion webhook."""
    data = await request.json()

    if data["status"] == "SUCCEEDED":
        video_url = data["output"][0]
        task_id = data["id"]

        # Process completed video
        await process_video(task_id, video_url)

    elif data["status"] == "FAILED":
        # Handle failure
        await handle_failure(data["id"], data.get("failure"))

    return {"status": "ok"}

@app.post("/webhook/luma")
async def luma_webhook(request: Request):
    """Handle Luma completion webhook."""
    data = await request.json()

    if data["state"] == "completed":
        video_url = data["assets"]["video"]
        await process_video(data["id"], video_url)

    return {"status": "ok"}
```

## Download and Process Video

```python
import httpx
from pathlib import Path
import subprocess

async def download_video(url: str, output_path: str) -> str:
    """Download video from URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

    return output_path

def transcode_video(
    input_path: str,
    output_path: str,
    codec: str = "libx264",
    crf: int = 23
) -> str:
    """Transcode video using ffmpeg."""
    cmd = [
        "ffmpeg", "-i", input_path,
        "-c:v", codec,
        "-crf", str(crf),
        "-preset", "medium",
        "-y", output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path

def extract_thumbnail(
    video_path: str,
    output_path: str,
    time: str = "00:00:01"
) -> str:
    """Extract thumbnail from video."""
    cmd = [
        "ffmpeg", "-i", video_path,
        "-ss", time,
        "-vframes", "1",
        "-y", output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path
```

## See Also

- [templates.md](templates.md) - Production service templates
- [llm-prompts.md](llm-prompts.md) - Prompt engineering guide
- [checklist.md](checklist.md) - Implementation checklist
