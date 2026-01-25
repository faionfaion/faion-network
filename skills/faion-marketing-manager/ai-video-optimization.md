# AI Video Optimization

**Cost optimization, troubleshooting, and quality improvement strategies for AI video platforms**

---

## Cost Comparison

### Monthly Subscription Comparison

| Platform | Free Tier | Basic | Pro | Unlimited |
|----------|-----------|-------|-----|-----------|
| Sora 2 | - | $20/mo (Plus) | $200/mo (Pro) | - |
| Runway | 125 credits | $15/mo | $35/mo | $96/mo |
| Pika | 250 credits | $8/mo | $28/mo | $58/mo |
| Kling | Yes | $5/mo | $10/mo | - |

### Per-Video Cost Estimate

| Video Type | Duration | Sora | Runway | Pika |
|------------|----------|------|--------|------|
| Social clip | 5s | ~$1 | $0.25 | $0.20 |
| Product demo | 30s | ~$5 | $1.50 | $1.00 |
| Short film | 2min | ~$20 | $6.00 | $4.00 |

### Cost Optimization Tips

1. **Prototype cheap, produce premium**
   - Use Pika/Kling for concept testing
   - Generate final in Sora/Runway

2. **Optimize duration**
   - Shorter clips = lower cost
   - Combine clips in post-production

3. **Batch processing**
   - Generate during off-peak hours
   - Use API for bulk discounts

4. **Cache and reuse**
   - Save successful prompts
   - Extend existing clips vs. generating new

---

## Common Issues and Solutions

### Quality Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Blurry output | Low motion, poor prompt | Increase motion strength, add detail |
| Morphing faces | Complex motion, profile views | Use front-facing shots, shorter duration |
| Flickering | Frame inconsistency | Reduce motion, use image-to-video |
| Artifacts | Complex scene, hands/text | Simplify scene, avoid text generation |
| Wrong style | Vague prompt | Add explicit style references |

### Motion Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No movement | Motion strength too low | Increase motion parameter |
| Chaotic motion | Too many moving elements | Focus on one subject |
| Unnatural motion | Over-prompting | Simplify motion description |
| Camera drift | Default behavior | Specify "static camera" |

### Consistency Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Character changes | No reference | Use same source image |
| Color mismatch | Different generations | Add color palette to prompt |
| Style drift | Inconsistent prompts | Create base style prompt |

---

## Prompt Engineering Best Practices

### Universal Prompt Structure

```
[Subject] + [Action] + [Environment] + [Camera] + [Lighting] + [Style]
```

**Examples:**

```
# E-commerce Product
A minimalist white coffee mug slowly rotates on black marble.
Camera orbits smoothly. Soft studio lighting from left.
Commercial product photography style.

# Social Media Clip
A golden retriever jumps through falling autumn leaves in slow motion.
Camera follows at eye level. Warm golden hour lighting.
Inspirational lifestyle aesthetic.

# Tutorial/Explainer
A hand draws a flowchart on a whiteboard with colorful markers.
Static overhead camera. Bright even lighting.
Clean educational video style.
```

### Platform-Specific Tips

**Sora 2:**
- Emphasize cinematic language ("tracking shot", "dolly zoom")
- Reference film genres for style
- Describe temporal progression for longer clips

**Runway Gen-4:**
- Use camera motion parameters for precise control
- Leverage motion brush for selective animation
- Structure reference for character consistency

**Pika Labs:**
- Keep prompts concise for faster generation
- Use Pikaffects for stylized effects
- Motion strength 2-3 for natural movement

**Kling:**
- Use motion templates as starting point
- Simpler prompts work better
- Test in free tier before upgrading

---

## Quality Optimization Workflow

### 1. Initial Generation

```
Low-cost platform (Pika/Kling) → Test concept → Iterate prompt
```

### 2. Refinement

```
Mid-tier (Runway) → Add camera controls → Fine-tune motion
```

### 3. Final Production

```
High-quality (Sora/Runway 4K) → Extended duration → Post-processing
```

### 4. Post-Production

- Color grading
- Audio sync
- Transitions
- Text overlays (avoid generating text in-platform)

---

## Multi-Platform Strategy

### Use Case Matrix

| Goal | Prototyping | Production | Scale |
|------|-------------|------------|-------|
| **Social content** | Pika | Pika/Runway | Runway API |
| **Product demos** | Kling | Runway | Runway API |
| **Ads** | Pika | Sora 2 | Runway API |
| **Cinematic** | Runway | Sora 2 Pro | Sora 2 Pro |
| **Documentation** | Pika | Runway | Runway API |

### Cost-Efficiency Strategy

1. **Start cheap**: Validate concept with Pika/Kling
2. **Refine mid-tier**: Polish with Runway Standard
3. **Produce premium**: Final output with Sora 2 or Runway 4K
4. **Scale with API**: Automate with Runway/Pika API

---

## Automation and Workflows

### Batch Video Generation Script

```python
import runwayml
import time

client = runwayml.RunwayML()

prompts = [
    "Product shot: smartphone on marble",
    "Lifestyle: person using app in cafe",
    "Tutorial: hand swiping through interface"
]

def generate_batch(prompts, platform="runway"):
    tasks = []

    for prompt in prompts:
        if platform == "runway":
            task = client.text_to_video.create(
                model="gen4",
                prompt=prompt,
                duration=5,
                aspect_ratio="16:9"
            )
            tasks.append(task)
            time.sleep(2)  # Rate limiting

    # Poll all tasks
    completed = []
    while len(completed) < len(tasks):
        for i, task in enumerate(tasks):
            if i in completed:
                continue

            status = client.tasks.retrieve(task.id)
            if status.status == "SUCCEEDED":
                completed.append(i)
                print(f"Video {i+1} ready: {status.output[0]}")

    return completed

# Run batch
generate_batch(prompts)
```

### Quality Control Checklist

Before accepting generated video:

- [ ] Motion is smooth and natural
- [ ] Subject remains consistent
- [ ] No morphing or artifacts
- [ ] Lighting matches prompt
- [ ] Duration meets requirements
- [ ] Resolution is acceptable
- [ ] Audio (if any) syncs properly
- [ ] Brand guidelines followed

---

## Platform Selection Decision Tree

```
What's your priority?

QUALITY → Sora 2 Pro
├─ Budget unlimited? → Sora 2 Pro
└─ Budget limited? → Runway Gen-4

SPEED → Pika Labs
├─ Need effects? → Pika (Pikaffects)
└─ Simple clips? → Luma Dream Machine

COST → Kling 2.0
├─ Testing phase? → Kling Free
└─ Production? → Pika Pro

API INTEGRATION → Runway
├─ High volume? → Runway Unlimited
└─ Low volume? → Runway Standard

EXPERIMENTATION → Start Pika → Refine Runway → Produce Sora
```

---

## Advanced Optimization Techniques

### 1. Prompt Chaining

Generate video in stages, use output as input for next stage:

```
Stage 1: Generate base scene (Pika)
Stage 2: Add camera motion (Runway)
Stage 3: Enhance quality (Sora re-cut)
```

### 2. Hybrid Workflows

Combine AI with traditional tools:

```
AI Generation → After Effects compositing → Color grading → Final export
```

### 3. Style Transfer

Create consistent brand style:

```
1. Generate style reference (Sora)
2. Use as structure reference (Runway)
3. Apply to all videos for consistency
```

### 4. Asset Reuse

Build library of reusable elements:

- Background scenes
- Product shots
- Motion templates
- Lighting setups

---

## Performance Metrics

Track these metrics for optimization:

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| First-time success rate | >60% | Improve prompt templates |
| Cost per video | <$2 | Switch to cheaper platform |
| Generation time | <5min | Use turbo mode or batch |
| User engagement | >30s watch | Improve motion/pacing |
| Brand consistency | >90% | Create style guide |

---

## Troubleshooting Guide

### Platform-Specific Issues

**Sora:**
- Export limit reached → Upgrade to Pro or wait for reset
- Queue time too long → Generate during off-peak hours
- Video quality degraded → Check subscription tier

**Runway:**
- API rate limit → Implement exponential backoff
- Credits depleted → Switch to subscription plan
- Generation failed → Check prompt length and complexity

**Pika:**
- Motion too subtle → Increase motion_strength parameter
- Special effects not working → Check Pikaffects compatibility
- API errors → Verify authentication token

**Kling:**
- Geo-restriction → Use VPN (check ToS)
- Slow processing → Upgrade to paid tier
- Documentation unclear → Use Google Translate

---

*Part of faion-marketing-manager skill*
*Reference: ai-video-optimization.md*
