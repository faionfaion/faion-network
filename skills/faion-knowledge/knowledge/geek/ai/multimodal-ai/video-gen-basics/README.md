---
id: video-gen-basics
name: "Video Generation Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Video Generation Basics

## Overview

AI video generation creates video content from text prompts, images, or other videos. Modern models like Sora, Runway Gen-3, and Pika can generate realistic videos with complex motion, physics, and scene understanding.

## When to Use

- Marketing and advertising content
- Social media content creation
- Product demonstrations
- Educational content
- Film and animation prototyping
- Video editing and enhancement
- Creative exploration

## Key Concepts

### Video Generation Services

| Service | Quality | Duration | Resolution | Access |
|---------|---------|----------|------------|--------|
| OpenAI Sora | Highest | 60s | 1080p | Limited |
| Runway Gen-3 | Very High | 10s | 1080p | API |
| Pika | High | 4s | 1080p | API |
| Stable Video | Good | 4s | 1024x576 | Open |
| Luma Dream Machine | High | 5s | 720p | API |
| Kling | Very High | 5s | 1080p | API |

### Generation Types

| Type | Input | Output |
|------|-------|--------|
| Text-to-Video | Text prompt | Video |
| Image-to-Video | Image + prompt | Video animating image |
| Video-to-Video | Video + prompt | Modified video |
| Interpolation | Frames | Smooth video |

## Video Prompt Engineering

### Prompt Builder

```python
class VideoPromptBuilder:
    """Build effective prompts for video generation."""

    def __init__(self):
        self.components = {
            "subject": "",
            "action": "",
            "setting": "",
            "camera": "",
            "style": "",
            "lighting": "",
            "details": []
        }

    def set_subject(self, subject: str):
        """Set main subject."""
        self.components["subject"] = subject
        return self

    def set_action(self, action: str):
        """Set the action/motion."""
        self.components["action"] = action
        return self

    def set_setting(self, setting: str):
        """Set the environment/background."""
        self.components["setting"] = setting
        return self

    def set_camera(self, camera: str):
        """Set camera movement/angle."""
        camera_movements = {
            "static": "static camera, locked shot",
            "pan_left": "smooth pan left",
            "pan_right": "smooth pan right",
            "dolly_in": "dolly in, moving closer",
            "dolly_out": "dolly out, pulling back",
            "tracking": "tracking shot, following subject",
            "crane": "crane shot, rising up",
            "handheld": "handheld camera, slight shake",
            "drone": "aerial drone shot",
            "orbit": "orbiting around subject"
        }
        self.components["camera"] = camera_movements.get(camera, camera)
        return self

    def set_style(self, style: str):
        """Set visual style."""
        styles = {
            "cinematic": "cinematic, film quality, 35mm",
            "documentary": "documentary style, natural",
            "commercial": "commercial quality, polished",
            "artistic": "artistic, stylized",
            "anime": "anime style, animation",
            "realistic": "photorealistic, lifelike"
        }
        self.components["style"] = styles.get(style, style)
        return self

    def set_lighting(self, lighting: str):
        """Set lighting conditions."""
        self.components["lighting"] = lighting
        return self

    def add_detail(self, detail: str):
        """Add specific detail."""
        self.components["details"].append(detail)
        return self

    def build(self) -> str:
        """Build final prompt."""
        parts = []

        if self.components["subject"]:
            parts.append(self.components["subject"])

        if self.components["action"]:
            parts.append(self.components["action"])

        if self.components["setting"]:
            parts.append(f"in {self.components['setting']}")

        if self.components["camera"]:
            parts.append(self.components["camera"])

        if self.components["style"]:
            parts.append(self.components["style"])

        if self.components["lighting"]:
            parts.append(self.components["lighting"])

        parts.extend(self.components["details"])

        return ", ".join(parts)

# Usage
prompt = (
    VideoPromptBuilder()
    .set_subject("a golden retriever")
    .set_action("running through a field of sunflowers")
    .set_setting("sunny countryside")
    .set_camera("tracking")
    .set_style("cinematic")
    .set_lighting("golden hour lighting")
    .add_detail("slow motion")
    .add_detail("4K quality")
    .build()
)
```

## Video Processing Utilities

```python
import subprocess
from pathlib import Path
from typing import List

class VideoProcessor:
    """Utilities for video processing."""

    @staticmethod
    def get_video_info(video_path: str) -> dict:
        """Get video metadata using ffprobe."""
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        import json
        return json.loads(result.stdout)

    @staticmethod
    def extract_frames(
        video_path: str,
        output_dir: str,
        fps: int = 1
    ) -> List[str]:
        """Extract frames from video."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"fps={fps}",
            f"{output_dir}/frame_%04d.png"
        ]

        subprocess.run(cmd, check=True)

        return sorted(Path(output_dir).glob("frame_*.png"))

    @staticmethod
    def create_video_from_frames(
        frame_pattern: str,
        output_path: str,
        fps: int = 24
    ):
        """Create video from image sequence."""
        cmd = [
            "ffmpeg",
            "-framerate", str(fps),
            "-i", frame_pattern,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_path
        ]

        subprocess.run(cmd, check=True)

    @staticmethod
    def concatenate_videos(
        video_paths: List[str],
        output_path: str
    ):
        """Concatenate multiple videos."""
        list_path = "/tmp/video_list.txt"
        with open(list_path, "w") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_path
        ]

        subprocess.run(cmd, check=True)
        Path(list_path).unlink()

    @staticmethod
    def add_audio(
        video_path: str,
        audio_path: str,
        output_path: str
    ):
        """Add audio track to video."""
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]

        subprocess.run(cmd, check=True)

    @staticmethod
    def resize_video(
        video_path: str,
        output_path: str,
        width: int,
        height: int
    ):
        """Resize video to specific dimensions."""
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"scale={width}:{height}",
            "-c:a", "copy",
            output_path
        ]

        subprocess.run(cmd, check=True)

    @staticmethod
    def loop_video(
        video_path: str,
        output_path: str,
        loop_count: int = 3
    ):
        """Loop video multiple times."""
        cmd = [
            "ffmpeg",
            "-stream_loop", str(loop_count - 1),
            "-i", video_path,
            "-c", "copy",
            output_path
        ]

        subprocess.run(cmd, check=True)
```

## Best Practices

1. **Prompt Quality**
   - Describe motion explicitly
   - Specify camera movements
   - Include style and lighting
   - Keep prompts focused

2. **Generation Settings**
   - Start with short durations
   - Use appropriate aspect ratios
   - Test different seeds

3. **Iteration**
   - Generate multiple versions
   - Refine prompts based on results
   - Use image-to-video for control

4. **Post-Processing**
   - Add music/sound effects
   - Color grade if needed
   - Trim/edit generated content

5. **Cost Management**
   - Start with cheaper models
   - Cache successful generations
   - Use appropriate quality levels

## Common Pitfalls

1. **Vague Motion** - Not specifying how things move
2. **Wrong Duration** - Videos too short/long
3. **No Camera Specified** - Random camera movements
4. **Conflicting Elements** - Too many things happening
5. **Ignoring Physics** - Unrealistic expectations
6. **No Style Guidance** - Inconsistent aesthetics

## See Also

- [video-gen-tools.md](video-gen-tools.md) - Service integrations and API implementations

## References

- [Runway ML](https://runwayml.com/)
- [Luma AI](https://lumalabs.ai/)
- [Stable Video Diffusion](https://stability.ai/stable-video)
- [Pika](https://pika.art/)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate video from text prompts | haiku | API execution and monitoring |
| Create video generation workflow | sonnet | Pipeline design and integration |
| Optimize video generation quality | opus | Complex trade-offs and strategy |

