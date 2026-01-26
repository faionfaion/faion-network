# Video Generation Prompts

Prompt engineering guide for AI video generation.

## Prompt Structure

### Basic Formula

```
[Subject] + [Action] + [Setting] + [Style] + [Camera] + [Lighting]
```

### Example

```
A golden retriever running through a field of sunflowers,
natural outdoor setting, cinematic film style,
tracking shot following the dog, warm golden hour lighting
```

## Prompt Components

### 1. Subject

Start with clear subject description:

```
# People
A young woman with red hair
An elderly man with a beard
A group of children

# Animals
A majestic white horse
A curious orange cat
A flock of birds

# Objects
A vintage red car
A steaming cup of coffee
A floating glass sphere
```

### 2. Action

Describe movement and behavior:

```
# Movement
walking slowly, running fast, dancing gracefully
flying through the air, swimming underwater
spinning, jumping, falling

# Behavior
laughing joyfully, looking contemplatively
reaching toward the camera
transforming into particles
```

### 3. Setting/Environment

Define the scene:

```
# Natural
in a dense forest, on a sandy beach
in a mountain meadow, underwater in the ocean
floating in clouds, in a wheat field

# Urban
on a busy city street, in an empty subway station
on a rooftop at night, in a neon-lit alley

# Abstract
in a void of light, surrounded by floating shapes
in a surreal dreamscape
```

### 4. Style

Specify visual style:

```
# Cinematic
cinematic film style, movie quality
blockbuster visual style, Hollywood production

# Photography
documentary style, raw footage
photorealistic, hyperrealistic

# Artistic
anime style, Studio Ghibli inspired
oil painting come to life
watercolor animation

# Vintage
8mm film grain, VHS aesthetic
black and white film noir
1970s Kodak film look
```

### 5. Camera Movement

Direct the camera:

```
# Movement Types
tracking shot, dolly shot, crane shot
handheld camera, steadicam
orbiting around subject
push in slowly, pull back dramatically

# Angles
low angle looking up, high angle looking down
eye level, bird's eye view
dutch angle, extreme close-up
```

### 6. Lighting

Set the mood:

```
# Natural
golden hour sunlight, soft morning light
harsh midday sun, overcast diffused light

# Artificial
neon lights, candlelight
spotlight, rim lighting
dramatic chiaroscuro

# Atmospheric
foggy atmosphere, dust particles in light
volumetric god rays, underwater caustics
```

## Prompt Templates by Use Case

### Product Videos

```
[Product] elegantly rotating on a [surface],
[lighting type] lighting highlighting [features],
smooth 360-degree rotation, [background description],
commercial photography style, 4K quality
```

**Example:**
```
A luxury watch elegantly rotating on a black marble surface,
soft studio lighting highlighting the gold accents,
smooth 360-degree rotation, dark gradient background,
commercial photography style, 4K quality
```

### Landscape/Nature

```
[Location description] at [time of day],
[weather/atmosphere], [camera movement],
[style reference], cinematic quality
```

**Example:**
```
Mountain peaks emerging from sea of clouds at sunrise,
misty atmosphere with golden light, slow drone pullback,
National Geographic documentary style, cinematic quality
```

### Character/Person

```
[Person description] [action] in [setting],
[emotion/expression], [camera angle and movement],
[lighting], [style]
```

**Example:**
```
Young woman with flowing dark hair walking through a rain-soaked city street,
contemplative expression looking up at the sky, tracking shot at eye level,
neon reflections on wet pavement, Blade Runner aesthetic
```

### Abstract/Artistic

```
[Abstract concept] visualized as [visual metaphor],
[colors and textures], [movement description],
[artistic style], dreamlike quality
```

**Example:**
```
Time visualized as flowing golden sand particles,
warm amber and deep blue gradients, particles swirling in slow motion,
abstract expressionist style, dreamlike quality
```

### Social Media (Vertical)

```
[Subject] [action], vertical 9:16 format,
[trending style], engaging motion,
[platform-appropriate style], high energy
```

**Example:**
```
Colorful smoothie being poured in slow motion, vertical 9:16 format,
satisfying ASMR style, engaging swirling motion,
Instagram Reels aesthetic, vibrant colors
```

## Provider-Specific Tips

### Runway Gen-3

- Excels at: Motion control, style transfer, lip-sync
- Prompt tips:
  - Be specific about camera movements
  - Include motion descriptors (slow, fast, smooth)
  - Works well with image input for style reference

```
# Good for Runway
A person speaking to camera, natural head movements,
soft interview lighting, slight camera drift,
professional corporate video style
```

### Luma Dream Machine

- Excels at: Natural motion, landscape, character consistency
- Prompt tips:
  - Focus on subject and environment
  - Less emphasis on technical camera terms
  - Good with emotional descriptions

```
# Good for Luma
A child discovering a butterfly in a sunlit garden,
wonder and curiosity, soft natural lighting,
warm nostalgic feeling, gentle movement
```

### Sora 2

- Excels at: Long-form, complex scenes, physics accuracy
- Prompt tips:
  - Can handle multiple subjects
  - Understands complex interactions
  - Good with temporal descriptions

```
# Good for Sora
A busy coffee shop scene, multiple patrons reading and chatting,
barista preparing drinks in background, natural ambient movement,
realistic physics, documentary observation style, 30 seconds
```

### Veo 3

- Excels at: 4K quality, native audio, photorealism
- Prompt tips:
  - Include audio/sound descriptions
  - Request specific resolutions
  - Good with dialogue scenes

```
# Good for Veo
Two people having a conversation at outdoor cafe,
ambient street sounds, natural dialogue,
4K photorealistic quality, shallow depth of field
```

## Negative Prompts

Use to exclude unwanted elements:

```
# Common exclusions
blurry, low quality, distorted faces
unnatural movement, glitchy artifacts
oversaturated, underexposed
watermark, text overlay

# Style exclusions
cartoon style, anime style (when wanting realism)
CGI look (when wanting photorealistic)
```

## Advanced Techniques

### Temporal Descriptions

```
Starting with [initial state], gradually transitioning to [end state]

Example:
Starting with a closed flower bud at dawn,
gradually transitioning to full bloom as sunlight increases
```

### Multi-Stage Prompts (for extensions)

```
Part 1: Establishing shot of [location]
Part 2: [Subject] enters frame and [action]
Part 3: Close-up of [detail], emotional beat
```

### Style Mixing

```
Combine [Style A] with [Style B] elements

Example:
Combine cyberpunk neon aesthetics with traditional Japanese garden elements,
cherry blossoms glowing with holographic shimmer
```

## Prompt Optimization Checklist

- [ ] Clear subject identification
- [ ] Specific action/movement
- [ ] Defined setting/environment
- [ ] Visual style specified
- [ ] Camera movement described
- [ ] Lighting conditions set
- [ ] Aspect ratio appropriate for platform
- [ ] Duration considered in complexity
- [ ] Provider strengths leveraged

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too vague | "A nice video of nature" | Specify subject, location, time, style |
| Conflicting styles | "Realistic anime" | Choose one dominant style |
| Too complex | Multiple unrelated elements | Focus on one clear concept |
| No motion | Static description | Add action verbs and camera movement |
| Wrong format | Landscape for TikTok | Match aspect ratio to platform |

## See Also

- [examples.md](examples.md) - Code examples
- [templates.md](templates.md) - Service templates
- [README.md](README.md) - Provider comparison
