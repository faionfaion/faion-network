# M-GEN-002: Video Generation Workflow

## Overview

Video generation transforms text, images, or short clips into full video content. The workflow involves storyboarding, asset preparation, generation, and post-processing. Modern tools include Sora, Runway, Pika Labs, and Kling.

**When to use:** Creating video content for marketing, social media, product demos, or creative projects without traditional filming.

## Core Concepts

### 1. Video Generation Models (2025)

| Model | Input Types | Max Length | Best For |
|-------|-------------|------------|----------|
| **Sora** | Text, Image | 60s | Cinematic, complex |
| **Runway Gen-3** | Text, Image, Video | 10s | Motion, style |
| **Pika Labs** | Text, Image | 4s | Quick iterations |
| **Kling** | Text, Image | 5s | Realistic motion |
| **Stable Video** | Image | 4s | Image animation |
| **Luma Dream Machine** | Text, Image | 5s | Creative, surreal |

### 2. Video Generation Workflow

```
Concept → Storyboard → Asset Prep → Generation → Post-Production → Export
   ↓          ↓            ↓           ↓              ↓            ↓
Script    Shot list    Images     API calls      Editing      Formats
          Timing      Prompts    Iterations     Music/VO     Compression
```

### 3. Key Parameters

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| **Duration** | Video length | 2-10 seconds |
| **Aspect Ratio** | Frame shape | 16:9, 9:16, 1:1 |
| **FPS** | Frame rate | 24, 30, 60 |
| **Resolution** | Output size | 720p, 1080p |
| **Motion Amount** | Movement intensity | Low, Medium, High |
| **Camera Motion** | Virtual camera | Static, Pan, Zoom |

## Best Practices

### 1. Create Detailed Storyboards

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Shot:
    shot_number: int
    duration: float  # seconds
    description: str
    camera_motion: str
    prompt: str
    reference_image: str = None
    audio_notes: str = None

@dataclass
class Storyboard:
    title: str
    total_duration: float
    shots: List[Shot]
    style_guide: str
    music_notes: str

# Example storyboard
storyboard = Storyboard(
    title="Product Launch Video",
    total_duration=30,
    style_guide="Cinematic, premium feel, warm color grade",
    music_notes="Upbeat, inspiring, builds to climax",
    shots=[
        Shot(
            shot_number=1,
            duration=3,
            description="Sunrise over city skyline",
            camera_motion="slow push in",
            prompt="Aerial view of modern city skyline at golden hour, drone footage, cinematic"
        ),
        Shot(
            shot_number=2,
            duration=4,
            description="Product reveal on desk",
            camera_motion="orbit around",
            prompt="Sleek laptop on minimalist desk, morning light through window, premium product shot"
        ),
        # ... more shots
    ]
)
```

### 2. Prepare Consistent Assets

```python
def prepare_video_assets(storyboard: Storyboard) -> dict:
    """Prepare all assets needed for video generation."""

    assets = {
        "reference_images": [],
        "generated_frames": [],
        "prompts": [],
        "style_reference": None
    }

    # Generate or collect reference images for consistency
    for shot in storyboard.shots:
        if shot.reference_image:
            assets["reference_images"].append(shot.reference_image)
        else:
            # Generate a reference frame
            frame = generate_image(shot.prompt, style=storyboard.style_guide)
            assets["generated_frames"].append(frame)

        # Prepare detailed prompt
        full_prompt = f"""
        {shot.prompt}
        Style: {storyboard.style_guide}
        Camera: {shot.camera_motion}
        Duration: {shot.duration}s
        """
        assets["prompts"].append(full_prompt)

    return assets
```

### 3. Iterate and Refine

```python
def generate_with_iterations(
    prompt: str,
    reference_image: str = None,
    max_attempts: int = 3
) -> dict:
    """Generate video with quality iterations."""

    best_result = None
    best_score = 0

    for attempt in range(max_attempts):
        # Generate video
        result = video_api.generate(
            prompt=prompt,
            image=reference_image,
            duration=4,
            aspect_ratio="16:9"
        )

        # Score result
        score = evaluate_video_quality(result)

        if score > best_score:
            best_score = score
            best_result = result

        # Stop if good enough
        if score > 0.9:
            break

        # Refine prompt based on issues
        prompt = refine_prompt(prompt, result.feedback)

    return {
        "video": best_result,
        "score": best_score,
        "attempts": attempt + 1
    }
```

## Common Patterns

### Pattern 1: Text-to-Video with Runway

```python
import runway

def generate_runway_video(
    prompt: str,
    duration: int = 5,
    aspect_ratio: str = "16:9"
) -> str:
    """Generate video using Runway Gen-3."""

    # Initialize client
    client = runway.Client(api_key="your-api-key")

    # Generate video
    task = client.text_to_video(
        prompt=prompt,
        duration=duration,
        aspect_ratio=aspect_ratio,
        motion_score=50,  # 0-100, controls motion amount
        seed=None  # Random for variation
    )

    # Wait for completion
    result = task.wait()

    return result.video_url

# Example
prompt = """
A serene mountain lake at dawn, mist rising from water,
camera slowly pushes forward, cinematic, 4K quality,
peaceful atmosphere, soft morning light
"""

video_url = generate_runway_video(prompt, duration=10)
```

### Pattern 2: Image-to-Video

```python
def image_to_video(
    image_path: str,
    motion_prompt: str,
    camera_motion: str = "static"
) -> str:
    """Animate a static image into video."""

    camera_motions = {
        "static": "camera remains still",
        "push_in": "camera slowly pushes forward",
        "pull_out": "camera slowly pulls back",
        "pan_left": "camera pans left to right",
        "pan_right": "camera pans right to left",
        "orbit": "camera orbits around subject"
    }

    full_prompt = f"""
    {motion_prompt}
    Camera movement: {camera_motions.get(camera_motion, camera_motion)}
    Smooth, natural motion, maintain image quality
    """

    result = video_api.image_to_video(
        image=image_path,
        prompt=full_prompt,
        duration=4,
        motion_strength=0.6
    )

    return result.video_url

# Example: Animate a product image
video = image_to_video(
    image_path="product_hero.png",
    motion_prompt="Product rotates slowly, highlighting features",
    camera_motion="orbit"
)
```

### Pattern 3: Video Extension

```python
def extend_video(
    video_path: str,
    direction: str = "forward",
    seconds: int = 4
) -> str:
    """Extend video duration with consistent motion."""

    result = video_api.extend(
        video=video_path,
        direction=direction,  # "forward" or "backward"
        duration=seconds,
        maintain_style=True
    )

    return result.video_url

def create_long_video(shots: list, target_duration: int) -> str:
    """Create longer video by extending and joining shots."""

    generated_clips = []

    for shot in shots:
        # Generate initial clip
        clip = generate_runway_video(shot.prompt, duration=5)

        # Extend if needed
        while get_video_duration(clip) < shot.duration:
            clip = extend_video(clip, "forward", 4)

        generated_clips.append({
            "path": clip,
            "duration": shot.duration
        })

    # Join clips in video editor
    return join_video_clips(generated_clips)
```

### Pattern 4: Style-Consistent Series

```python
class VideoSeriesGenerator:
    """Generate consistent video series with same style."""

    def __init__(self, style_reference: str):
        self.style = style_reference
        self.generated_videos = []

    def generate_episode(
        self,
        script: str,
        episode_number: int
    ) -> str:
        """Generate one episode maintaining series style."""

        # Parse script into shots
        shots = self._parse_script(script)

        # Generate each shot with style consistency
        clips = []
        for shot in shots:
            prompt = f"""
            {shot.description}
            Style reference: {self.style}
            Consistent with series aesthetic
            Episode {episode_number} of series
            """

            clip = generate_runway_video(prompt, duration=shot.duration)
            clips.append(clip)

        # Combine clips
        episode = join_video_clips(clips)
        self.generated_videos.append(episode)

        return episode

    def _parse_script(self, script: str) -> list:
        """Parse script into individual shots."""
        # Use LLM to break down script
        return llm.parse_script_to_shots(script)
```

### Pattern 5: Post-Production Pipeline

```python
import moviepy.editor as mp

def post_process_video(
    video_path: str,
    music_path: str = None,
    voiceover_path: str = None,
    color_grade: str = "cinematic",
    add_titles: bool = False
) -> str:
    """Post-process generated video."""

    video = mp.VideoFileClip(video_path)

    # Apply color grading
    if color_grade:
        video = apply_color_grade(video, color_grade)

    # Add music
    if music_path:
        music = mp.AudioFileClip(music_path)
        music = music.subclip(0, video.duration)
        music = music.volumex(0.3)  # Background level

        if voiceover_path:
            voiceover = mp.AudioFileClip(voiceover_path)
            final_audio = mp.CompositeAudioClip([music, voiceover])
        else:
            final_audio = music

        video = video.set_audio(final_audio)

    # Add title cards
    if add_titles:
        title = create_title_card("Product Launch", duration=2)
        video = mp.concatenate_videoclips([title, video])

    # Export
    output_path = video_path.replace(".mp4", "_final.mp4")
    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        bitrate="8000k"
    )

    return output_path
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| No storyboard | Inconsistent results | Plan before generating |
| Ignoring motion limits | Jarring movements | Use appropriate motion scores |
| Single generation | Suboptimal quality | Iterate and select best |
| Mixing styles | Visual inconsistency | Maintain style guide |
| Skipping post-production | Raw look | Add color, audio, transitions |

## Tools & References

### Related Skills
- faion-video-gen-skill
- faion-image-gen-skill
- faion-audio-skill

### Related Agents
- faion-video-generator-agent
- faion-multimodal-agent

### External Resources
- [Runway ML](https://runwayml.com/)
- [Pika Labs](https://pika.art/)
- [Kling AI](https://klingai.com/)
- [Sora](https://openai.com/sora) (when available)

## Checklist

- [ ] Created detailed storyboard
- [ ] Defined visual style guide
- [ ] Prepared reference images
- [ ] Wrote prompts for each shot
- [ ] Selected appropriate model
- [ ] Generated initial clips
- [ ] Iterated for quality
- [ ] Applied post-production
- [ ] Added audio (music/VO)
- [ ] Exported in target formats

---

*Methodology: M-GEN-002 | Category: Multimodal/Generation*
*Related: faion-video-generator-agent, faion-video-gen-skill*
