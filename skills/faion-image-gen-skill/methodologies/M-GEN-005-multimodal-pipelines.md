# M-GEN-005: Multimodal Pipelines

## Overview

Multimodal pipelines chain multiple AI generation steps: text to image, image to video, video to audio, and back. Complex workflows enable rich content creation from simple inputs. Key patterns include storyboarding, asset generation, and automated production.

**When to use:** Creating complete multimedia content (videos with voiceover, animated presentations, product showcases) from text or simple inputs.

## Core Concepts

### 1. Pipeline Types

| Pipeline | Input | Output | Use Case |
|----------|-------|--------|----------|
| **Text → Image → Video** | Script | Animated video | Marketing videos |
| **Text → Audio + Images** | Article | Narrated slideshow | Educational content |
| **Image → Video + Audio** | Product shot | Product demo | E-commerce |
| **Audio → Text → Summary** | Recording | Notes | Meeting summaries |
| **Text → Full Production** | Brief | Complete video | Automated content |

### 2. Pipeline Architecture

```
Input (Text/Brief)
        │
        ▼
┌───────────────────┐
│   Orchestrator    │ ◄── Manages workflow
└───────────────────┘
        │
        ├──────────────────────────────────────┐
        ▼                                      ▼
┌───────────────┐                      ┌───────────────┐
│ Text Generator│                      │ Script Parser │
│   (LLM)       │                      │   (LLM)       │
└───────────────┘                      └───────────────┘
        │                                      │
        ▼                                      ▼
┌───────────────┐                      ┌───────────────┐
│Image Generator│                      │ Voice Synth   │
│ (DALL-E/FLUX) │                      │ (ElevenLabs)  │
└───────────────┘                      └───────────────┘
        │                                      │
        ▼                                      ▼
┌───────────────┐                      ┌───────────────┐
│Video Generator│                      │ Music/SFX     │
│ (Runway/Pika) │                      │ (Suno/Udio)   │
└───────────────┘                      └───────────────┘
        │                                      │
        └──────────────────────────────────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  Compositor   │
                   │ (FFmpeg/AIAE) │
                   └───────────────┘
                           │
                           ▼
                    Final Output
```

### 3. State Management

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class PipelineState:
    """Track multimodal pipeline state."""
    id: str
    input: dict
    steps: Dict[str, StepStatus] = field(default_factory=dict)
    artifacts: Dict[str, str] = field(default_factory=dict)  # step_name -> file_path
    errors: List[dict] = field(default_factory=list)
    created_at: str = None
    completed_at: str = None
```

## Best Practices

### 1. Design Modular Steps

```python
from abc import ABC, abstractmethod

class PipelineStep(ABC):
    """Base class for pipeline steps."""

    @abstractmethod
    async def execute(self, inputs: dict, state: PipelineState) -> dict:
        """Execute step and return outputs."""
        pass

    @abstractmethod
    def validate_inputs(self, inputs: dict) -> bool:
        """Validate required inputs are present."""
        pass

class ImageGenerationStep(PipelineStep):
    def __init__(self, model: str = "dall-e-3"):
        self.model = model
        self.client = OpenAI()

    async def execute(self, inputs: dict, state: PipelineState) -> dict:
        prompt = inputs["prompt"]

        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size="1792x1024",
            quality="hd"
        )

        image_url = response.data[0].url
        local_path = download_image(image_url, state.id)

        return {"image_path": local_path}

    def validate_inputs(self, inputs: dict) -> bool:
        return "prompt" in inputs
```

### 2. Handle Dependencies

```python
from collections import defaultdict

class PipelineOrchestrator:
    """Orchestrate multimodal pipeline with dependencies."""

    def __init__(self):
        self.steps: Dict[str, PipelineStep] = {}
        self.dependencies: Dict[str, List[str]] = defaultdict(list)

    def add_step(self, name: str, step: PipelineStep, depends_on: List[str] = None):
        """Register a pipeline step."""
        self.steps[name] = step
        if depends_on:
            self.dependencies[name] = depends_on

    def get_execution_order(self) -> List[str]:
        """Topological sort of steps."""
        visited = set()
        order = []

        def visit(name):
            if name in visited:
                return
            visited.add(name)
            for dep in self.dependencies[name]:
                visit(dep)
            order.append(name)

        for name in self.steps:
            visit(name)

        return order

    async def execute(self, initial_inputs: dict) -> PipelineState:
        """Execute pipeline in dependency order."""
        state = PipelineState(
            id=generate_id(),
            input=initial_inputs,
            created_at=datetime.utcnow().isoformat()
        )

        execution_order = self.get_execution_order()
        current_outputs = initial_inputs.copy()

        for step_name in execution_order:
            step = self.steps[step_name]
            state.steps[step_name] = StepStatus.RUNNING

            try:
                outputs = await step.execute(current_outputs, state)
                current_outputs.update(outputs)
                state.artifacts.update(outputs)
                state.steps[step_name] = StepStatus.COMPLETED
            except Exception as e:
                state.steps[step_name] = StepStatus.FAILED
                state.errors.append({"step": step_name, "error": str(e)})
                raise

        state.completed_at = datetime.utcnow().isoformat()
        return state
```

### 3. Enable Parallelization

```python
import asyncio

async def execute_parallel_steps(
    steps: Dict[str, PipelineStep],
    inputs: dict,
    state: PipelineState
) -> dict:
    """Execute independent steps in parallel."""

    tasks = {}
    for name, step in steps.items():
        if step.validate_inputs(inputs):
            tasks[name] = asyncio.create_task(step.execute(inputs, state))

    results = {}
    for name, task in tasks.items():
        try:
            result = await task
            results[name] = result
            state.steps[name] = StepStatus.COMPLETED
        except Exception as e:
            state.steps[name] = StepStatus.FAILED
            state.errors.append({"step": name, "error": str(e)})

    return results
```

## Common Patterns

### Pattern 1: Text-to-Video Pipeline

```python
class TextToVideoPipeline:
    """Complete text-to-video pipeline."""

    def __init__(self):
        self.llm = OpenAI()
        self.image_gen = ImageGenerator()
        self.video_gen = VideoGenerator()
        self.voice_gen = VoiceGenerator()

    async def generate(self, brief: str) -> str:
        """Generate video from text brief."""

        # Step 1: Generate script and storyboard
        script = await self._generate_script(brief)

        # Step 2: Generate assets in parallel
        images_task = asyncio.create_task(self._generate_images(script))
        voice_task = asyncio.create_task(self._generate_voice(script))

        images, voice_path = await asyncio.gather(images_task, voice_task)

        # Step 3: Generate video clips from images
        video_clips = await self._animate_images(images)

        # Step 4: Composite final video
        final_video = await self._composite(video_clips, voice_path, script)

        return final_video

    async def _generate_script(self, brief: str) -> dict:
        """Generate video script with scenes."""
        prompt = f"""
        Create a video script from this brief: {brief}

        Return JSON with:
        {{
            "title": "Video title",
            "duration_seconds": 30,
            "scenes": [
                {{
                    "scene_number": 1,
                    "duration": 5,
                    "visual_prompt": "Detailed image generation prompt",
                    "voiceover": "Narration text for this scene",
                    "camera_motion": "pan_left/zoom_in/static"
                }}
            ]
        }}
        """

        response = await self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    async def _generate_images(self, script: dict) -> List[str]:
        """Generate images for each scene."""
        images = []
        for scene in script["scenes"]:
            image = await self.image_gen.generate(
                scene["visual_prompt"],
                size="1792x1024"
            )
            images.append(image)
        return images

    async def _generate_voice(self, script: dict) -> str:
        """Generate voiceover for script."""
        full_narration = " ".join(
            scene["voiceover"] for scene in script["scenes"]
        )
        return await self.voice_gen.generate(full_narration)

    async def _animate_images(self, images: List[str]) -> List[str]:
        """Convert images to video clips."""
        clips = []
        for image in images:
            clip = await self.video_gen.image_to_video(
                image,
                duration=4,
                motion="subtle"
            )
            clips.append(clip)
        return clips

    async def _composite(
        self,
        clips: List[str],
        audio: str,
        script: dict
    ) -> str:
        """Combine clips and audio into final video."""
        return composite_video(
            clips=clips,
            audio=audio,
            transitions="crossfade",
            output_path=f"output_{script['title']}.mp4"
        )
```

### Pattern 2: Narrated Slideshow

```python
class NarratedSlideshowPipeline:
    """Generate narrated slideshow from article."""

    async def generate(self, article: str) -> str:
        # Parse article into slides
        slides = await self._parse_to_slides(article)

        # Generate visuals and audio in parallel
        results = await asyncio.gather(
            self._generate_slide_images(slides),
            self._generate_narration(slides)
        )

        images, audio_segments = results

        # Create slideshow video
        return self._create_slideshow(slides, images, audio_segments)

    async def _parse_to_slides(self, article: str) -> List[dict]:
        """Parse article into presentation slides."""
        response = await llm.generate(f"""
        Convert this article into presentation slides:

        {article}

        Return JSON array with:
        [{{
            "title": "Slide title",
            "bullet_points": ["point 1", "point 2"],
            "image_prompt": "Visual description for this slide",
            "narration": "What to say for this slide",
            "duration_seconds": 10
        }}]
        """)

        return json.loads(response)

    async def _generate_slide_images(self, slides: List[dict]) -> List[str]:
        """Generate image for each slide."""
        tasks = [
            image_gen.generate(slide["image_prompt"])
            for slide in slides
        ]
        return await asyncio.gather(*tasks)

    async def _generate_narration(self, slides: List[dict]) -> List[str]:
        """Generate audio for each slide."""
        tasks = [
            voice_gen.generate(slide["narration"])
            for slide in slides
        ]
        return await asyncio.gather(*tasks)

    def _create_slideshow(
        self,
        slides: List[dict],
        images: List[str],
        audio_segments: List[str]
    ) -> str:
        """Compose final slideshow video."""
        import moviepy.editor as mp

        clips = []
        for slide, image, audio in zip(slides, images, audio_segments):
            # Create image clip with duration matching audio
            audio_clip = mp.AudioFileClip(audio)
            img_clip = mp.ImageClip(image).set_duration(audio_clip.duration)

            # Add text overlay
            txt_clip = mp.TextClip(
                slide["title"],
                fontsize=48,
                color='white',
                font='Arial-Bold'
            ).set_position(('center', 'bottom')).set_duration(audio_clip.duration)

            # Combine
            composite = mp.CompositeVideoClip([img_clip, txt_clip])
            composite = composite.set_audio(audio_clip)
            clips.append(composite)

        final = mp.concatenate_videoclips(clips, method="compose")
        output_path = "slideshow.mp4"
        final.write_videofile(output_path, fps=24)

        return output_path
```

### Pattern 3: Product Demo Generator

```python
class ProductDemoPipeline:
    """Generate product demo from product info."""

    async def generate(self, product: dict) -> str:
        # Generate demo script
        script = await self._create_demo_script(product)

        # Generate product shots
        product_shots = await self._generate_product_visuals(product, script)

        # Animate shots
        animated_clips = await self._animate_product_shots(product_shots)

        # Generate voiceover
        voiceover = await self._generate_voiceover(script)

        # Add background music
        music = await self._select_music(product["mood"])

        # Composite
        return await self._composite_demo(animated_clips, voiceover, music)

    async def _create_demo_script(self, product: dict) -> dict:
        return await llm.generate(f"""
        Create a 30-second product demo script for:
        Product: {product['name']}
        Features: {product['features']}
        Target audience: {product['audience']}

        Include:
        - Hook (3 seconds)
        - Problem statement (5 seconds)
        - Solution introduction (5 seconds)
        - Feature highlights (12 seconds)
        - Call to action (5 seconds)
        """)

    async def _generate_product_visuals(
        self,
        product: dict,
        script: dict
    ) -> List[str]:
        """Generate product images for each section."""
        prompts = [
            f"Hero shot of {product['name']}, premium product photography",
            f"Person frustrated with {product['problem']}, lifestyle photo",
            f"{product['name']} being used, showing key feature, clean background",
            f"Close-up of {product['name']} details, studio lighting",
            f"{product['name']} with satisfied customer, lifestyle setting"
        ]

        return await asyncio.gather(*[
            image_gen.generate(p, style="product photography")
            for p in prompts
        ])
```

### Pattern 4: Audio-Visual Synchronization

```python
class AVSyncPipeline:
    """Synchronize generated visuals with audio."""

    def sync_to_audio(
        self,
        audio_path: str,
        visual_prompts: List[str]
    ) -> str:
        """Generate visuals synchronized to audio."""

        # Analyze audio for timing
        audio_analysis = self._analyze_audio(audio_path)

        # Generate visuals for each segment
        visuals = []
        for segment in audio_analysis["segments"]:
            prompt = self._select_prompt(segment, visual_prompts)
            visual = self._generate_visual_for_segment(prompt, segment)
            visuals.append(visual)

        # Composite with precise timing
        return self._composite_synchronized(visuals, audio_path, audio_analysis)

    def _analyze_audio(self, audio_path: str) -> dict:
        """Analyze audio for beats, segments, mood."""
        import librosa

        y, sr = librosa.load(audio_path)

        # Detect beats
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)

        # Segment by energy
        segments = librosa.effects.split(y, top_db=20)
        segment_times = [
            {
                "start": librosa.frames_to_time(s[0], sr=sr),
                "end": librosa.frames_to_time(s[1], sr=sr)
            }
            for s in segments
        ]

        return {
            "tempo": tempo,
            "beat_times": beat_times.tolist(),
            "segments": segment_times,
            "duration": librosa.get_duration(y=y, sr=sr)
        }
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Sequential execution | Slow pipeline | Parallelize independent steps |
| No state tracking | Can't resume failures | Persist pipeline state |
| Hard-coded steps | Inflexible | Modular step design |
| No validation | Garbage propagates | Validate between steps |
| Ignoring timing | A/V desync | Explicit synchronization |

## Tools & References

### Related Skills
- faion-image-gen-skill
- faion-video-gen-skill
- faion-audio-skill
- faion-langchain-skill

### Related Agents
- faion-multimodal-agent

### External Resources
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Workflow orchestration
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [FFmpeg](https://ffmpeg.org/) - Media processing

## Checklist

- [ ] Designed pipeline architecture
- [ ] Defined step dependencies
- [ ] Implemented modular steps
- [ ] Added parallel execution
- [ ] Set up state management
- [ ] Added error handling
- [ ] Implemented retry logic
- [ ] Tested end-to-end
- [ ] Optimized for speed
- [ ] Documented pipeline

---

*Methodology: M-GEN-005 | Category: Multimodal/Generation*
*Related: faion-multimodal-agent*
