# AI Image Generation Prompting

**Prompt engineering best practices for text-to-image AI models**

---

## Prompt Structure

```
[Subject] + [Setting/Environment] + [Style] + [Lighting] + [Composition] + [Technical]
```

**Example:**
```
A professional businesswoman | in a modern glass office | corporate photography style |
soft natural window light | medium shot, shallow depth of field | 8K, sharp focus
```

---

## Subject Keywords

| Category | Keywords |
|----------|----------|
| **People** | portrait, headshot, full body, group, candid |
| **Objects** | product shot, floating, isolated, arrangement |
| **Animals** | wildlife, pet portrait, action shot |
| **Landscapes** | panoramic, aerial view, close-up detail |
| **Abstract** | patterns, textures, geometric shapes |

---

## Style Keywords

| Style | Keywords |
|-------|----------|
| **Photorealistic** | photorealistic, hyperrealistic, RAW photo, 8K UHD |
| **Artistic** | oil painting, watercolor, digital art, illustration |
| **Commercial** | product photography, advertising, editorial |
| **Cinematic** | cinematic, movie still, film grain, anamorphic |
| **Minimalist** | minimalist, clean, simple, white space |
| **Vintage** | retro, vintage, film photography, polaroid |
| **3D** | 3D render, CGI, octane render, unreal engine |

---

## Lighting Keywords

| Lighting | Effect |
|----------|--------|
| **Natural** | golden hour, blue hour, overcast, harsh sunlight |
| **Studio** | softbox, rim light, key light, fill light |
| **Dramatic** | chiaroscuro, low-key, high contrast, silhouette |
| **Ambient** | neon glow, bioluminescent, candlelight, moonlight |
| **Technical** | backlit, side-lit, front-lit, diffused |

---

## Composition Keywords

| Composition | Description |
|-------------|-------------|
| **Framing** | close-up, medium shot, wide shot, extreme close-up |
| **Angle** | eye level, bird's eye, worm's eye, Dutch angle |
| **Rule of thirds** | subject positioned at intersection points |
| **Symmetry** | balanced, mirrored, centered |
| **Depth** | shallow DOF, bokeh, layered, foreground interest |

---

## Technical Quality Keywords

```
High quality: 8K, UHD, high resolution, sharp focus, detailed
Camera: shot on Sony A7R IV, Canon EOS R5, Hasselblad
Lens: 85mm f/1.4, 35mm wide angle, macro lens
Post-processing: color graded, professionally retouched
```

---

## Negative Prompts

Common elements to exclude:

```
blurry, low quality, distorted, deformed, ugly, duplicate,
watermark, text, signature, cropped, out of frame,
extra limbs, bad anatomy, bad proportions, gross proportions,
mutation, disfigured, poorly drawn, jpeg artifacts
```

---

## Model-Specific Tips

### DALL-E 3

- Natural language works best
- System adds detail automatically
- Check `revised_prompt` to understand changes
- Use "natural" style for realism

**Examples:**

```
Good: "A modern minimalist living room with a grey sofa, wooden coffee table, and large windows showing city skyline at sunset, Scandinavian interior design style"

Bad: "living room, sofa, window"
```

### Midjourney

- Use `--style raw` for less stylization
- Stack style references with `--sref`
- Lower `--stylize` for more prompt adherence
- Separate concepts with `::`

**Examples:**

```
Good: "portrait of a scientist in a laboratory, dramatic lighting, photorealistic --ar 3:4 --style raw --v 6.1"

Advanced: "dreamy forest::2 magical atmosphere::1 --ar 16:9 --stylize 500"
```

### FLUX

- More literal prompt following
- Good with technical photography terms
- Supports longer prompts well
- Use `prompt_upsampling` for enhancement

**Examples:**

```
Good: "Professional product photograph of wireless earbuds on white marble surface, studio lighting with soft shadows, shot on Canon EOS R5 with 100mm macro lens, f/2.8, commercial photography style"

Technical: "Architectural photography of modern glass building, blue hour, long exposure, symmetrical composition, ultra-sharp details, 16K resolution"
```

### Stable Diffusion

- Use LoRAs for consistent styles
- CFG scale 4-7 for SD 3.5
- Negative prompts are important
- ComfyUI for complex workflows

**Examples:**

```
Prompt: "a beautiful landscape with mountains and lake, golden hour, dramatic clouds, vibrant colors, highly detailed, 8K"

Negative: "blurry, low quality, distorted, oversaturated, watermark, text, signature"

CFG: 5.0
Steps: 28
```

---

## Prompt Templates by Use Case

### Product Photography

```
Professional product shot of [PRODUCT], placed on [SURFACE], [LIGHTING TYPE],
[BACKGROUND], shot on [CAMERA], [LENS], commercial photography style,
high resolution, sharp focus
```

**Example:**
```
Professional product shot of wireless headphones, placed on black reflective surface,
soft studio lighting with rim light, white gradient background, shot on Sony A7R IV,
85mm f/1.4 lens, commercial photography style, high resolution, sharp focus
```

### Portrait Photography

```
[TYPE] portrait of [SUBJECT], [CLOTHING/STYLE], [LOCATION/SETTING],
[LIGHTING], [MOOD/EXPRESSION], shot on [CAMERA], [LENS], [STYLE]
```

**Example:**
```
Professional headshot portrait of a business executive, wearing navy suit,
in modern office with glass walls, soft natural window light, confident expression,
shot on Canon EOS R5, 85mm f/1.2 lens, corporate photography style
```

### Landscape Photography

```
[VIEW TYPE] landscape photograph of [LOCATION], [TIME OF DAY], [WEATHER],
[FOREGROUND ELEMENTS], [COMPOSITION], shot on [CAMERA], [LENS],
[PHOTOGRAPHY STYLE]
```

**Example:**
```
Panoramic landscape photograph of mountain valley with river, golden hour,
dramatic clouds, wildflowers in foreground, rule of thirds composition,
shot on Sony A7R IV, 24-70mm wide angle lens, landscape photography style
```

### Logo Design

```
[STYLE] logo design for "[COMPANY NAME]", [INDUSTRY], featuring [ELEMENTS],
[COLOR SCHEME], [BACKGROUND], vector style, modern, professional
```

**Example:**
```
Minimalist logo design for "TechFlow AI", tech startup, featuring abstract
neural network pattern, deep blue and silver gradient, white background,
vector style, modern, professional, clean lines
```

### Social Media Graphics

```
[STYLE] social media graphic for [PLATFORM], [TOPIC/MESSAGE],
[VISUAL ELEMENTS], [COLOR SCHEME], [TYPOGRAPHY NOTES], engaging,
eye-catching, [MOOD]
```

**Example:**
```
Bold modern social media graphic for Instagram, announcing product launch,
featuring smartphone mockup with glowing screen, vibrant gradient background
blue to purple, large bold text "LAUNCH DAY", engaging, eye-catching, exciting
```

### Illustration/Art

```
[ART STYLE] illustration of [SUBJECT], [SETTING], [COLOR PALETTE],
[MOOD/ATMOSPHERE], [TECHNICAL DETAILS], [ARTIST REFERENCE if needed]
```

**Example:**
```
Digital art illustration of futuristic cyberpunk city at night, neon lights,
rain-soaked streets, vibrant color palette with pink and blue tones,
atmospheric mood, highly detailed, trending on ArtStation
```

---

## Advanced Techniques

### Weighted Prompts (Midjourney)

Use `::` to separate concepts and numbers to weight them:

```
dreamy forest::2 magical atmosphere::1 sunset colors::1.5
```

### Prompt Emphasis (Stable Diffusion)

Use parentheses for emphasis:

```
(beautiful landscape:1.3), mountains, lake, (sunset:1.2)
```

### Multi-Stage Prompts

For complex scenes, build prompts in layers:

```
Stage 1: Main subject and composition
Stage 2: Lighting and atmosphere
Stage 3: Technical details and quality
Stage 4: Style and artistic direction
```

### Iterative Refinement

1. Start with basic prompt
2. Generate initial image
3. Identify what's missing or wrong
4. Add specific keywords to address issues
5. Repeat until satisfied

---

## Quality Control

### Checklist Before Generation

- [ ] Subject clearly defined
- [ ] Setting/environment specified
- [ ] Lighting direction mentioned
- [ ] Style/mood established
- [ ] Technical quality keywords added
- [ ] Negative prompts included (if applicable)
- [ ] Aspect ratio appropriate for use case

### Post-Generation Review

- [ ] Subject matches prompt
- [ ] Composition is balanced
- [ ] Lighting looks natural
- [ ] No unwanted artifacts
- [ ] Text renders correctly (if applicable)
- [ ] Style matches requirements
- [ ] Resolution sufficient for use case

---

## Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Too vague | "a person" | Be specific: "professional businesswoman in her 40s" |
| Conflicting styles | "photorealistic cartoon" | Choose one style approach |
| Too many concepts | 20+ elements in one prompt | Focus on 3-5 key elements |
| Missing context | "red car" | Add setting: "red sports car in modern showroom" |
| Ignoring aspect ratio | Portrait subject in 16:9 | Match ratio to subject type |
| No quality keywords | Just subject description | Add "8K, sharp focus, high quality" |
| Generic lighting | No lighting specified | Specify "golden hour" or "studio lighting" |

---

## Prompt Optimization by Platform

### For DALL-E 3

```
✅ Natural descriptive language
✅ Detailed specifications
✅ Check revised_prompt
❌ Don't over-optimize keywords
❌ Avoid technical jargon
```

### For Midjourney

```
✅ Concise artistic descriptions
✅ Use parameters (--ar, --style, --v)
✅ Reference styles and artists
✅ Use emphasis with ::
❌ Avoid overly long prompts
```

### For FLUX

```
✅ Technical photography terms
✅ Longer detailed prompts work well
✅ Specific camera/lens details
✅ Enable prompt_upsampling
❌ Don't rely on automatic enhancement
```

### For Stable Diffusion

```
✅ Structured prompt format
✅ Strong negative prompts
✅ Use emphasis with ()
✅ CFG scale 4-7 for SD 3.5
❌ Avoid conflicting keywords
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **faion-video-gen-skill** | Generate source images for image-to-video |
| **faion-marketing-manager** | Social media and ad visuals |
| **faion-ux-ui-designer** | UI mockups and design assets |
| **faion-content-agent** | Blog post images and graphics |

---

*Part of Faion Network Marketing Manager Skill*
*Last Updated: 2026-01-23*


## Sources

- [Prompt Engineering Guide](https://www.promptingguide.ai/applications/image_prompting)
- [Learn Prompting Image Module](https://learnprompting.org/docs/images/intro)
- [Midjourney Prompt Craft](https://docs.midjourney.com/docs/prompts)
- [DALL-E Prompt Book](https://dallery.gallery/the-dalle-2-prompt-book/)
- [Stable Diffusion Prompt Guide](https://stable-diffusion-art.com/prompt-guide/)
