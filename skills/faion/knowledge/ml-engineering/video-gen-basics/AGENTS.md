# Video Generation Basics

## Summary

**One-sentence:** Generates a short (≤10s) AI video clip via Runway Gen-3, Luma Dream Machine, Pika, or Replicate, with a structured prompt builder and async polling.

**One-paragraph:** Wraps text-to-video and image-to-video generation with a VideoPromptBuilder that enforces explicit subject, action, setting, camera-movement, style, and lighting fields. Submits to provider, polls status (30-300s typical), downloads the pre-signed URL within the expiry window (30-60min), and runs ffprobe validation before returning. Caches generated clips by prompt hash with seed; defaults to image-to-video when subject consistency matters across shots.

**Ефективно для:** агента контент-конвеєра, що збирає короткі промо / b-roll / соцмережеві кліпи з єдиним брифом — закриває петлю між текстовим брифом і відеофайлом, готовим до монтажу.

## Applies If (ALL must hold)

- Generating short (≤10s) marketing, social, or b-roll video clips from text or image input.
- Pipeline tolerates 30-300s async latency per clip (not user-interactive).
- A structured brief (subject + action + setting) is available before the call.
- Output is consumed by ffmpeg for trim / concat / resize, not by a realtime player.
- At least one provider API key (Runway / Luma / Replicate / Pika) is configured.

## Skip If (ANY kills it)

- Precise temporal control needed (specific action at specific timestamp) — no current model enforces this.
- Character consistency across multiple shots is mandatory — models drift between generations.
- Videos longer than 10-15s without chaining — concat via ffmpeg or use `video-gen-tools` for extension.
- Real-time generation required — generation is async, 30-300s per clip.
- Faces or brand logos in the brief — providers silently FAIL on policy violations.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Brief | dict: `{subject, action, setting, camera, style, lighting, duration_s}` | content planner |
| Provider credentials | env: `RUNWAY_API_KEY`, `LUMA_API_KEY`, `REPLICATE_API_TOKEN` | secrets manager |
| Image source (optional) | URL or local path (for image-to-video) | content store |
| Output dir | filesystem path with rw | pipeline orchestrator |
| ffmpeg + ffprobe installed | apt / brew | host setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/multimodal-ai/video-gen-tools` | downstream production layer with VideoGenerationService + multi-provider fallback |
| `geek/ai/llm-integration/structured-output-basics` | upstream brief shaping (subject/action/camera as typed fields) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: explicit camera, image-to-video default, ffprobe validate, seed cache, 5s cap, no inline video read | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema of generate() result + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing camera, fixed temp paths, no ffprobe, expired URL, inline video read | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: build prompt → submit → poll → download → ffprobe → cache | ~700 |
| `content/05-examples.xml` | medium | Worked Runway Gen-3 5s clip with VideoPromptBuilder + polling + ffprobe | ~500 |
| `content/06-decision-tree.xml` | essential | Provider routing: photorealistic / cinematic / animated / prototype + text vs image input | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `build-prompt` | sonnet | Brief → VideoPromptBuilder call with camera/style choices. |
| `poll-status` | haiku | Mechanical loop, sleep+check. |
| `validate-output` | haiku | ffprobe + size check; deterministic. |
| `route-provider` | sonnet | Decision-tree walk on style_tag + input mode. |

## Templates

| File | Purpose |
|------|---------|
| `templates/video-prompt-builder.py` | VideoPromptBuilder with subject / action / setting / camera / style / lighting fields. |
| `templates/video-processor.py` | VideoProcessor: ffprobe validate, ffmpeg concat / resize / audio-merge. |
| `templates/concat-clips.sh` | Bash helper for ffmpeg concat from `clips.txt`. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-gen-basics.py` | Validate generate() output JSON against 02-output-contract. | Post-generation, before downstream consumes path. |

## Related

- [[video-gen-tools]] — production service with multi-provider fallback + retry.
- [[img-gen-basics]] — image generator providing image-to-video source frames.
- [[vision-applications]] — verify generated frames against the brief.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes provider by style_tag (photorealistic → Luma; cinematic → Runway; animated → Replicate AnimateDiff; prototype → Replicate SVD), and decides text-to-video vs image-to-video based on whether subject consistency across shots is required. Use it at the generate() entry point before the first provider call.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/video-prompt-builder.py`

```python
"""VideoPromptBuilder fluent API enforcing closed camera vocabulary."""


class VideoPromptBuilder:
    """Build structured prompts for video generation."""

    CAMERA_MOVEMENTS = {
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

    STYLES = {
        "cinematic": "cinematic, film quality, 35mm",
        "documentary": "documentary style, natural",
        "commercial": "commercial quality, polished",
        "artistic": "artistic, stylized",
        "anime": "anime style, animation",
        "realistic": "photorealistic, lifelike"
    }

    def __init__(self):
        self.components: dict[str, str | list] = {
            "subject": "", "action": "", "setting": "",
            "camera": "", "style": "", "lighting": "", "details": []
        }

    def set_subject(self, subject: str) -> "VideoPromptBuilder":
        self.components["subject"] = subject
        return self

    def set_action(self, action: str) -> "VideoPromptBuilder":
        self.components["action"] = action
        return self

    def set_setting(self, setting: str) -> "VideoPromptBuilder":
        self.components["setting"] = setting
        return self

    def set_camera(self, camera: str) -> "VideoPromptBuilder":
        self.components["camera"] = self.CAMERA_MOVEMENTS.get(camera, camera)
        return self

    def set_style(self, style: str) -> "VideoPromptBuilder":
        self.components["style"] = self.STYLES.get(style, style)
        return self

    def set_lighting(self, lighting: str) -> "VideoPromptBuilder":
        self.components["lighting"] = lighting
        return self

    def add_detail(self, detail: str) -> "VideoPromptBuilder":
        self.components["details"].append(detail)
        return self

    def build(self) -> str:
        parts = []
        for key in ("subject", "action"):
            if self.components[key]:
                parts.append(self.components[key])
        if self.components["setting"]:
            parts.append(f"in {self.components['setting']}")
        for key in ("camera", "style", "lighting"):
            if self.components[key]:
                parts.append(self.components[key])
        parts.extend(self.components["details"])
        return ", ".join(parts)
```

### `templates/video-processor.py`

```python
"""VideoProcessor: ffmpeg utilities + ffprobe validation per rule r3."""
import subprocess
import json
from pathlib import Path


class VideoProcessor:
    """ffmpeg/ffprobe utilities for video post-processing."""

    @staticmethod
    def get_video_info(video_path: str) -> dict:
        """Get video metadata. Always call on output before downstream use."""
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
               "-show_format", "-show_streams", video_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)

    @staticmethod
    def validate_output(video_path: str) -> bool:
        """Return True if file exists, size > 0, and has valid video stream."""
        p = Path(video_path)
        if not p.exists() or p.stat().st_size == 0:
            return False
        try:
            info = VideoProcessor.get_video_info(video_path)
            streams = info.get("streams", [])
            return any(s.get("codec_type") == "video" for s in streams)
        except Exception:
            return False

    @staticmethod
    def extract_frames(video_path: str, output_dir: str, fps: int = 1) -> list[str]:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-i", video_path, "-vf", f"fps={fps}",
               f"{output_dir}/frame_%04d.png"]
        subprocess.run(cmd, check=True)
        return sorted(str(p) for p in Path(output_dir).glob("frame_*.png"))

    @staticmethod
    def concatenate_videos(video_paths: list[str], output_path: str) -> None:
        list_path = "/tmp/video_list.txt"
        with open(list_path, "w") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")
        cmd = ["ffmpeg", "-f", "concat", "-safe", "0",
               "-i", list_path, "-c", "copy", output_path]
        subprocess.run(cmd, check=True)
        Path(list_path).unlink()

    @staticmethod
    def add_audio(video_path: str, audio_path: str, output_path: str) -> None:
        cmd = ["ffmpeg", "-i", video_path, "-i", audio_path,
               "-c:v", "copy", "-c:a", "aac", "-shortest", output_path]
        subprocess.run(cmd, check=True)

    @staticmethod
    def resize_video(video_path: str, output_path: str,
                     width: int, height: int) -> None:
        cmd = ["ffmpeg", "-i", video_path, "-vf", f"scale={width}:{height}",
               "-c:a", "copy", output_path]
        subprocess.run(cmd, check=True)
```

### `templates/concat-clips.sh`

```bash
# Usage: bash concat-clips.sh output.mp4 [clips.txt]
set -euo pipefail

INPUT_LIST="${2:-clips.txt}"
OUTPUT="${1:-output.mp4}"

if [ ! -f "$INPUT_LIST" ]; then
    echo "Error: $INPUT_LIST not found" >&2
    exit 1
fi

# Build ffmpeg concat list
while IFS= read -r f; do
    echo "file '$f'"
done < "$INPUT_LIST" > /tmp/concat_list.txt

ffmpeg -f concat -safe 0 -i /tmp/concat_list.txt -c copy "$OUTPUT"
rm -f /tmp/concat_list.txt
echo "Written: $OUTPUT"
```
