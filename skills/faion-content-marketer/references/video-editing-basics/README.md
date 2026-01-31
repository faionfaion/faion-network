# Video Editing Basics

**Workflows, Automation, FFmpeg, DaVinci Resolve**

---

## Text-to-Video Workflow

```
1. CONCEPT
   ├── Define scene objective
   ├── Write detailed description
   └── Choose platform based on needs

2. PROMPT ENGINEERING
   ├── Subject: Who/what is in the scene
   ├── Action: What happens
   ├── Setting: Where, when
   ├── Camera: Movement, angle
   ├── Style: Aesthetic, mood
   └── Technical: Duration, aspect ratio

3. GENERATION
   ├── Start with shorter duration (5s)
   ├── Iterate on prompt
   ├── Try variations
   └── Select best result

4. REFINEMENT
   ├── Extend if needed
   ├── Apply fixes (inpainting)
   ├── Color grade
   └── Add audio

5. POST-PRODUCTION
   ├── Upscale if needed
   ├── Add music/SFX
   ├── Export in required format
   └── Archive prompts and settings
```

---

## Image-to-Video Workflow

```
1. IMAGE PREPARATION
   ├── High resolution (min 1024px)
   ├── Clean composition
   ├── Consider what will move
   └── Remove artifacts

2. MOTION PLANNING
   ├── What moves: subject, background, camera
   ├── Direction of movement
   ├── Speed/intensity
   └── Duration needed

3. GENERATION
   ├── Upload image
   ├── Describe motion in prompt
   ├── Set camera controls if available
   └── Generate and review

4. ITERATION
   ├── Adjust motion strength
   ├── Try different angles
   ├── Combine multiple generations
   └── Use motion brush for precision
```

---

## Multi-Shot Production

```
1. SCRIPT BREAKDOWN
   ├── Write or obtain script
   ├── Break into scenes
   ├── Break scenes into shots
   └── Note required visuals per shot

2. SHOT LIST
   Shot #  | Description      | Duration | Camera      | Platform
   01      | Estab. wide     | 5s       | Static      | Runway
   02      | Subject enters  | 10s      | Track right | Sora
   03      | Close-up face   | 5s       | Push in     | Runway
   04      | POV shot        | 5s       | Handheld    | Pika

3. GENERATION ORDER
   ├── Generate establishing shots first
   ├── Then action sequences
   ├── Finally close-ups and details
   └── Keep consistent style prompts

4. EDITING
   ├── Import all clips to timeline (Premiere, DaVinci)
   ├── Arrange in sequence
   ├── Add transitions
   ├── Color match all clips
   └── Add audio track

5. EXPORT
   ├── Master in highest quality
   ├── Create platform-specific versions
   └── Archive project files
```

---

## Style Consistency

### Maintaining Visual Coherence

| Technique | Description |
|-----------|-------------|
| **Style Prompt Base** | Use consistent style descriptors across all shots |
| **Reference Image** | Use same source image for related shots |
| **Character Sheets** | Generate reference images first, use for all videos |
| **Color Palette** | Specify exact colors in prompts |
| **Lighting Consistency** | Same lighting description across shots |

### Style Prompt Template

```
Base Style Prompt (prepend to all shots):
"[Shot description], cinematic film grain, color graded in teal and orange,
professional lighting, 24fps motion blur, shallow depth of field,
shot on RED camera --style [consistent_style_id]"
```

### Character Consistency

1. **Generate Character Reference**
   - Create detailed character image first
   - Document exact appearance details
   - Save as reference for all shots

2. **Description Template**
   ```
   [Character: young woman, dark curly hair, brown eyes, wearing
   olive green jacket and white t-shirt] + [action/scene]
   ```

3. **Use Image-to-Video**
   - Keep character image as starting frame
   - Describe motion, not appearance
   - Maintain same source across shots

---

## Video Editing Automation

### Bulk Generation Scripts

```python
# Batch video generation with Runway
import runwayml
import json
import time

client = runwayml.RunwayML()

# Load shot list
with open("shot_list.json") as f:
    shots = json.load(f)

# Example shot_list.json:
# [
#   {"id": "01", "prompt": "...", "duration": 5, "image": "shot01.png"},
#   {"id": "02", "prompt": "...", "duration": 10, "image": null}
# ]

results = []

for shot in shots:
    if shot.get("image"):
        # Image-to-video
        with open(shot["image"], "rb") as f:
            task = client.image_to_video.create(
                model="gen4",
                prompt_image=f.read(),
                prompt_text=shot["prompt"],
                duration=shot["duration"]
            )
    else:
        # Text-to-video
        task = client.text_to_video.create(
            model="gen4",
            prompt=shot["prompt"],
            duration=shot["duration"]
        )

    results.append({
        "shot_id": shot["id"],
        "task_id": task.id
    })

    print(f"Started shot {shot['id']}: {task.id}")
    time.sleep(2)  # Rate limiting

# Poll all tasks
completed = []
while len(completed) < len(results):
    for result in results:
        if result["shot_id"] in [c["shot_id"] for c in completed]:
            continue

        task = client.tasks.retrieve(result["task_id"])
        if task.status == "SUCCEEDED":
            completed.append({
                "shot_id": result["shot_id"],
                "url": task.output[0]
            })
            print(f"Completed shot {result['shot_id']}")
        elif task.status == "FAILED":
            print(f"Failed shot {result['shot_id']}: {task.error}")
            completed.append({"shot_id": result["shot_id"], "url": None})

    time.sleep(10)

# Save results
with open("generated_videos.json", "w") as f:
    json.dump(completed, f, indent=2)
```

---

## FFmpeg Post-Processing

```bash
# Concatenate multiple clips
ffmpeg -f concat -safe 0 -i clips.txt -c copy output.mp4

# clips.txt format:
# file 'shot01.mp4'
# file 'shot02.mp4'
# file 'shot03.mp4'

# Upscale to 4K
ffmpeg -i input.mp4 -vf "scale=3840:2160:flags=lanczos" -c:v libx264 -crf 18 output_4k.mp4

# Add audio track
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest output.mp4

# Create loop
ffmpeg -stream_loop 3 -i input.mp4 -c copy output_looped.mp4

# Adjust speed (2x faster)
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output_fast.mp4

# Add fade in/out (1 second each)
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=4:d=1" output.mp4

# Convert to GIF (for previews)
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos" -c:v gif output.gif
```

---

## DaVinci Resolve Automation

```python
# DaVinci Resolve script (run inside Resolve)
import DaVinciResolveScript as dvr

resolve = dvr.scriptapp("Resolve")
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()

# Create timeline
media_pool = project.GetMediaPool()
timeline = media_pool.CreateTimelineFromClips(
    "AI Generated Sequence",
    clips_list  # List of imported clips
)

# Add transitions
for i, clip in enumerate(timeline.GetItemListInTrack("video", 1)):
    if i > 0:
        timeline.AddTransition(
            clip,
            "Cross Dissolve",
            duration=24  # frames
        )

# Color match
project.SetCurrentTimeline(timeline)
timeline.ApplyGradeFromDRX(0, "color_grade.drx")

# Render
project.SetCurrentRenderFormatAndCodec("mp4", "H265_NVIDIA")
project.SetRenderSettings({
    "TargetDir": "/output/",
    "CustomName": "final_output"
})
project.AddRenderJob()
project.StartRendering()
```

---

## Storyboarding

### Pre-Production Planning

```markdown
# Storyboard Template

## Project: [Title]
## Total Duration: [X seconds/minutes]
## Platform: [Sora/Runway/Pika]

---

### Shot 01
- **Duration:** 5s
- **Visual:** Wide establishing shot of city at dawn
- **Camera:** Slow push forward
- **Motion:** Cars moving on streets below
- **Audio:** Ambient city sounds
- **Prompt:** "Aerial view of Manhattan at dawn, golden hour lighting,
  camera slowly pushes forward toward the skyline, cars visible on
  streets below, cinematic, 4K quality"
- **Reference:** [image link]

---

### Shot 02
- **Duration:** 3s
- **Visual:** Close-up of protagonist's eyes opening
- **Camera:** Static, then slight push in
- **Motion:** Eyes open, blink
- **Audio:** Alarm clock sound
- **Prompt:** "Extreme close-up of human eyes opening, morning light
  falling across face, eyes blink twice, photorealistic, shallow DOF"
- **Reference:** [image link]
```

### Sora Storyboard Mode

1. **Access Storyboard**
   - Open Sora interface
   - Select "Storyboard" mode
   - Define timeline length

2. **Add Shots**
   - Click to add shot markers
   - Write prompt for each shot
   - Upload reference images

3. **Connect Shots**
   - Define transitions between shots
   - Set camera continuity
   - Preview full sequence

4. **Generate**
   - Generate all shots in sequence
   - Review and regenerate as needed
   - Export final video

---

## Resolution and Export

### Supported Resolutions

| Platform | Max Resolution | Aspect Ratios |
|----------|---------------|---------------|
| Sora 2 | 1920x1080 | 16:9, 9:16, 1:1 |
| Runway Gen-4 | 4096x2160 | 16:9, 9:16, 1:1, 4:5, 21:9 |
| Pika 2.5 | 1920x1080 | 16:9, 9:16, 1:1 |
| Kling 2.0 | 1920x1080 | 16:9, 9:16 |

### Platform-Specific Exports

| Platform | Resolution | Aspect | Duration | Notes |
|----------|------------|--------|----------|-------|
| YouTube | 1920x1080+ | 16:9 | Any | Include 2s intro/outro |
| TikTok | 1080x1920 | 9:16 | 15-60s | Vertical, fast-paced |
| Instagram Reels | 1080x1920 | 9:16 | 15-90s | Vertical |
| Instagram Post | 1080x1350 | 4:5 | 3-60s | Square or tall |
| Twitter/X | 1280x720 | 16:9 | 2:20 max | Keep under 512MB |
| LinkedIn | 1920x1080 | 16:9 | 3-10min | Professional content |

### Upscaling

For higher resolution output:

```python
# Using Topaz Video AI (via CLI)
import subprocess

subprocess.run([
    "tvai",
    "--input", "generated_1080p.mp4",
    "--output", "upscaled_4k.mp4",
    "--model", "proteus-3",
    "--scale", "2",
    "--format", "mp4"
])

# Using Real-ESRGAN for frames
# 1. Extract frames
subprocess.run([
    "ffmpeg", "-i", "input.mp4",
    "-vf", "fps=24",
    "frames/frame_%04d.png"
])

# 2. Upscale frames
subprocess.run([
    "realesrgan-ncnn-vulkan",
    "-i", "frames/",
    "-o", "upscaled_frames/",
    "-n", "realesrgan-x4plus"
])

# 3. Reassemble video
subprocess.run([
    "ffmpeg", "-framerate", "24",
    "-i", "upscaled_frames/frame_%04d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "upscaled_video.mp4"
])
```

---

## Tools and Resources

| Tool | Purpose | Link |
|------|---------|------|
| FFmpeg | Video processing CLI | ffmpeg.org |
| DaVinci Resolve | Professional editing | blackmagicdesign.com |
| Topaz Video AI | Upscaling | topazlabs.com |
| Runway API | Programmatic access | docs.runwayml.com |
| Pika API | Programmatic access | pika.art/api |

---

*Part of faion-marketing-manager skill*
*Reference: video-editing-basics.md*


## Sources

- [DaVinci Resolve Tutorials](https://www.blackmagicdesign.com/products/davinciresolve/training)
- [Adobe Premiere Pro Guide](https://helpx.adobe.com/premiere-pro/tutorials.html)
- [CapCut Video Editing](https://www.capcut.com/resource/)
- [Frame.io Collaboration](https://blog.frame.io/)
- [Video Editing Best Practices](https://www.videomaker.com/)
