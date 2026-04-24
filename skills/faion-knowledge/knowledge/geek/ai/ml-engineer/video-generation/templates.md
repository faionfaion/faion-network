# Video Generation Templates

Production-ready service templates for AI video generation.

## Multi-Provider Service

```python
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Callable
from pathlib import Path
from enum import Enum
import logging
import asyncio
import httpx
import os

class VideoProvider(Enum):
    RUNWAY = "runway"
    LUMA = "luma"
    REPLICATE = "replicate"

@dataclass
class VideoConfig:
    """Video generation configuration."""
    provider: VideoProvider = VideoProvider.LUMA
    default_duration: int = 5
    default_aspect_ratio: str = "16:9"
    max_retries: int = 3
    timeout: int = 600  # 10 minutes
    output_dir: str = "./generated_videos"

    # Provider-specific
    runway_model: str = "gen3a_turbo"
    luma_loop: bool = False

@dataclass
class VideoResult:
    """Video generation result."""
    status: str  # success, failed, timeout
    video_url: Optional[str] = None
    local_path: Optional[str] = None
    task_id: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class VideoGenerationService:
    """Production video generation service with multi-provider support."""

    def __init__(self, config: Optional[VideoConfig] = None):
        self.config = config or VideoConfig()
        self.logger = logging.getLogger(__name__)
        Path(self.config.output_dir).mkdir(exist_ok=True)

        # Initialize provider clients lazily
        self._runway_client = None
        self._luma_api_key = os.environ.get("LUMA_API_KEY")

    async def generate(
        self,
        prompt: str,
        provider: Optional[VideoProvider] = None,
        duration: Optional[int] = None,
        aspect_ratio: Optional[str] = None,
        image_url: Optional[str] = None,
        callback: Optional[Callable] = None,
        **kwargs
    ) -> VideoResult:
        """Generate video with automatic retries and fallback."""
        provider = provider or self.config.provider
        duration = duration or self.config.default_duration
        aspect_ratio = aspect_ratio or self.config.default_aspect_ratio

        for attempt in range(self.config.max_retries):
            try:
                self.logger.info(
                    f"Attempt {attempt + 1}: Generating video with {provider.value}"
                )

                if provider == VideoProvider.RUNWAY:
                    result = await self._generate_runway(
                        prompt, duration, aspect_ratio, image_url, **kwargs
                    )
                elif provider == VideoProvider.LUMA:
                    result = await self._generate_luma(
                        prompt, aspect_ratio, image_url, **kwargs
                    )
                else:
                    result = await self._generate_replicate(
                        prompt, **kwargs
                    )

                if result.status == "success":
                    # Download video locally
                    result.local_path = await self._download_video(
                        result.video_url,
                        self._sanitize_filename(prompt)
                    )

                    if callback:
                        await callback(result)

                    return result

            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.config.max_retries - 1:
                    return VideoResult(
                        status="failed",
                        error=str(e)
                    )

        return VideoResult(status="failed", error="Max retries exceeded")

    async def generate_from_image(
        self,
        image_path: str,
        prompt: str,
        **kwargs
    ) -> VideoResult:
        """Generate video from local image."""
        # Upload image to get URL (implement based on your storage)
        image_url = await self._upload_image(image_path)
        return await self.generate(prompt, image_url=image_url, **kwargs)

    async def _generate_runway(
        self,
        prompt: str,
        duration: int,
        aspect_ratio: str,
        image_url: Optional[str],
        **kwargs
    ) -> VideoResult:
        """Generate using Runway Gen-3."""
        import runwayml

        if not self._runway_client:
            self._runway_client = runwayml.RunwayML()

        task_params = {
            "model": self.config.runway_model,
            "prompt_text": prompt,
            "duration": duration,
            "ratio": aspect_ratio
        }

        if image_url:
            task_params["prompt_image"] = image_url

        task = self._runway_client.image_to_video.create(**task_params)

        return await self._poll_runway(task.id)

    async def _poll_runway(self, task_id: str) -> VideoResult:
        """Poll Runway task status."""
        import runwayml

        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < self.config.timeout:
            task = self._runway_client.tasks.retrieve(task_id)

            if task.status == "SUCCEEDED":
                return VideoResult(
                    status="success",
                    video_url=task.output[0],
                    task_id=task_id
                )
            elif task.status == "FAILED":
                return VideoResult(
                    status="failed",
                    error=task.failure,
                    task_id=task_id
                )

            await asyncio.sleep(5)

        return VideoResult(status="timeout", task_id=task_id)

    async def _generate_luma(
        self,
        prompt: str,
        aspect_ratio: str,
        image_url: Optional[str],
        **kwargs
    ) -> VideoResult:
        """Generate using Luma Dream Machine."""
        async with httpx.AsyncClient() as client:
            payload = {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "loop": self.config.luma_loop
            }

            if image_url:
                payload["keyframes"] = {
                    "frame0": {"type": "image", "url": image_url}
                }

            response = await client.post(
                "https://api.lumalabs.ai/dream-machine/v1/generations",
                headers={"Authorization": f"Bearer {self._luma_api_key}"},
                json=payload
            )
            response.raise_for_status()

            generation_id = response.json()["id"]
            return await self._poll_luma(client, generation_id)

    async def _poll_luma(
        self,
        client: httpx.AsyncClient,
        generation_id: str
    ) -> VideoResult:
        """Poll Luma generation status."""
        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < self.config.timeout:
            response = await client.get(
                f"https://api.lumalabs.ai/dream-machine/v1/generations/{generation_id}",
                headers={"Authorization": f"Bearer {self._luma_api_key}"}
            )
            data = response.json()

            if data["state"] == "completed":
                return VideoResult(
                    status="success",
                    video_url=data["assets"]["video"],
                    task_id=generation_id
                )
            elif data["state"] == "failed":
                return VideoResult(
                    status="failed",
                    error=data.get("failure_reason"),
                    task_id=generation_id
                )

            await asyncio.sleep(5)

        return VideoResult(status="timeout", task_id=generation_id)

    async def _generate_replicate(
        self,
        prompt: str,
        model: str = "zeroscope",
        **kwargs
    ) -> VideoResult:
        """Generate using Replicate models."""
        import replicate

        if model == "zeroscope":
            output = replicate.run(
                "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
                input={
                    "prompt": prompt,
                    "num_frames": kwargs.get("num_frames", 24),
                    "fps": kwargs.get("fps", 8)
                }
            )
        elif model == "animatediff":
            output = replicate.run(
                "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48c9f",
                input={
                    "prompt": prompt,
                    "num_frames": kwargs.get("num_frames", 16)
                }
            )

        return VideoResult(status="success", video_url=output)

    async def _download_video(self, url: str, name: str) -> str:
        """Download video from URL."""
        output_path = Path(self.config.output_dir) / f"{name}.mp4"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

        return str(output_path)

    async def _upload_image(self, image_path: str) -> str:
        """Upload image and return URL.

        Override this method with your storage implementation:
        - S3
        - Cloudinary
        - Google Cloud Storage
        """
        raise NotImplementedError("Implement image upload for your storage provider")

    def _sanitize_filename(self, text: str) -> str:
        """Sanitize text for use as filename."""
        import re
        clean = re.sub(r'[^\w\s-]', '', text).strip()[:50]
        return clean.replace(' ', '_')
```

## FastAPI Integration

```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

# In-memory job storage (use Redis in production)
jobs: Dict[str, VideoResult] = {}

class VideoRequest(BaseModel):
    prompt: str
    provider: Optional[str] = "luma"
    duration: Optional[int] = 5
    aspect_ratio: Optional[str] = "16:9"
    image_url: Optional[str] = None

class VideoResponse(BaseModel):
    job_id: str
    status: str
    video_url: Optional[str] = None
    error: Optional[str] = None

service = VideoGenerationService()

@app.post("/api/videos/generate", response_model=VideoResponse)
async def create_video(
    request: VideoRequest,
    background_tasks: BackgroundTasks
):
    """Start video generation job."""
    job_id = str(uuid.uuid4())
    jobs[job_id] = VideoResult(status="processing")

    background_tasks.add_task(
        generate_video_task,
        job_id,
        request
    )

    return VideoResponse(job_id=job_id, status="processing")

async def generate_video_task(job_id: str, request: VideoRequest):
    """Background task for video generation."""
    try:
        provider = VideoProvider(request.provider)
        result = await service.generate(
            prompt=request.prompt,
            provider=provider,
            duration=request.duration,
            aspect_ratio=request.aspect_ratio,
            image_url=request.image_url
        )
        jobs[job_id] = result
    except Exception as e:
        jobs[job_id] = VideoResult(status="failed", error=str(e))

@app.get("/api/videos/{job_id}", response_model=VideoResponse)
async def get_video_status(job_id: str):
    """Get video generation status."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    result = jobs[job_id]
    return VideoResponse(
        job_id=job_id,
        status=result.status,
        video_url=result.video_url,
        error=result.error
    )
```

## Queue-Based Processing

```python
from dataclasses import dataclass
from typing import Optional
import asyncio
from collections import deque

@dataclass
class VideoJob:
    id: str
    prompt: str
    provider: VideoProvider
    priority: int = 0
    created_at: float = 0

class VideoQueue:
    """Priority queue for video generation jobs."""

    def __init__(self, service: VideoGenerationService, max_concurrent: int = 3):
        self.service = service
        self.max_concurrent = max_concurrent
        self.queue: deque[VideoJob] = deque()
        self.processing: Dict[str, VideoJob] = {}
        self.results: Dict[str, VideoResult] = {}
        self._lock = asyncio.Lock()

    async def submit(self, job: VideoJob) -> str:
        """Submit job to queue."""
        async with self._lock:
            # Insert by priority
            inserted = False
            for i, existing in enumerate(self.queue):
                if job.priority > existing.priority:
                    self.queue.insert(i, job)
                    inserted = True
                    break

            if not inserted:
                self.queue.append(job)

        return job.id

    async def process(self):
        """Process jobs from queue."""
        while True:
            if len(self.processing) < self.max_concurrent and self.queue:
                async with self._lock:
                    job = self.queue.popleft()
                    self.processing[job.id] = job

                asyncio.create_task(self._process_job(job))

            await asyncio.sleep(1)

    async def _process_job(self, job: VideoJob):
        """Process single job."""
        try:
            result = await self.service.generate(
                prompt=job.prompt,
                provider=job.provider
            )
            self.results[job.id] = result
        finally:
            async with self._lock:
                del self.processing[job.id]

    def get_result(self, job_id: str) -> Optional[VideoResult]:
        """Get job result."""
        return self.results.get(job_id)

    def get_status(self, job_id: str) -> str:
        """Get job status."""
        if job_id in self.results:
            return self.results[job_id].status
        if job_id in self.processing:
            return "processing"
        if any(j.id == job_id for j in self.queue):
            return "queued"
        return "not_found"
```

## Video Processing Utils

```python
import subprocess
from pathlib import Path
from typing import List, Optional

class VideoProcessor:
    """Video processing utilities using ffmpeg."""

    def extract_frames(
        self,
        video_path: str,
        output_dir: str,
        fps: int = 1
    ) -> List[Path]:
        """Extract frames from video."""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        cmd = [
            "ffmpeg", "-i", video_path,
            "-vf", f"fps={fps}",
            "-y", str(output_dir / "frame_%04d.png")
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        return sorted(output_dir.glob("frame_*.png"))

    def concatenate_videos(
        self,
        video_paths: List[str],
        output_path: str
    ) -> str:
        """Concatenate multiple videos."""
        # Create file list
        list_path = "/tmp/videos.txt"
        with open(list_path, "w") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            "-y", output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        return output_path

    def add_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> str:
        """Add audio track to video."""
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            "-y", output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        return output_path

    def resize_video(
        self,
        video_path: str,
        output_path: str,
        width: int,
        height: int
    ) -> str:
        """Resize video to specific dimensions."""
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vf", f"scale={width}:{height}",
            "-c:a", "copy",
            "-y", output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        return output_path

    def get_duration(self, video_path: str) -> float:
        """Get video duration in seconds."""
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())
```

## Usage Example

```python
import asyncio
from video_service import VideoGenerationService, VideoConfig, VideoProvider

async def main():
    # Configure service
    config = VideoConfig(
        provider=VideoProvider.LUMA,
        output_dir="./videos",
        max_retries=3,
        timeout=600
    )

    service = VideoGenerationService(config)

    # Generate video
    result = await service.generate(
        prompt="A serene lake at sunset with mountains in background, cinematic drone shot",
        duration=5,
        aspect_ratio="16:9"
    )

    if result.status == "success":
        print(f"Video saved to: {result.local_path}")
        print(f"Video URL: {result.video_url}")
    else:
        print(f"Generation failed: {result.error}")

asyncio.run(main())
```

## See Also

- [examples.md](examples.md) - Provider-specific examples
- [llm-prompts.md](llm-prompts.md) - Prompt engineering
- [checklist.md](checklist.md) - Implementation checklist
