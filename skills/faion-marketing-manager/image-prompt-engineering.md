# Image Prompt Engineering

**Complete guide to crafting effective image generation prompts (2025-2026)**

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

**DALL-E 3:**
- Natural language works best
- System adds detail automatically
- Check `revised_prompt` to understand changes
- Use "natural" style for realism

**Midjourney:**
- Use `--style raw` for less stylization
- Stack style references with `--sref`
- Lower `--stylize` for more prompt adherence
- Separate concepts with `::`

**FLUX:**
- More literal prompt following
- Good with technical photography terms
- Supports longer prompts well
- Use `prompt_upsampling` for enhancement

**Stable Diffusion:**
- Use LoRAs for consistent styles
- CFG scale 4-7 for SD 3.5
- Negative prompts are important
- ComfyUI for complex workflows
