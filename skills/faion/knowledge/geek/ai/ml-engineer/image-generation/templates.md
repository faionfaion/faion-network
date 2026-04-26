# Image Generation Prompt Templates

## Template Structure

All templates follow the formula:
```
[Subject] + [Style] + [Lighting] + [Composition] + [Details] + [Technical]
```

---

## Marketing & Advertising

### Hero Image

```
A [product/concept] in a [setting],
[style] photography style,
[lighting] lighting,
[composition] shot,
[brand colors/mood],
professional advertising quality, 8K resolution
```

**Example:**
```
A premium coffee cup on a rustic wooden table with morning light streaming through a window,
commercial photography style,
soft natural golden hour lighting,
centered composition with shallow depth of field,
warm earth tones with cream accents,
professional advertising quality, 8K resolution
```

### Product Shot

```
[Product] on a [surface/background],
product photography,
[lighting setup] lighting,
[angle] view,
[key details],
clean minimalist composition, studio quality
```

**Example:**
```
Sleek wireless headphones on a matte black surface,
product photography,
three-point studio lighting with soft highlights,
45-degree angle view,
showing premium materials and subtle logo,
clean minimalist composition, studio quality
```

### Social Media Post

```
[Subject/scene] for [platform],
[style] aesthetic,
[mood/vibe],
[aspect ratio appropriate for platform],
trendy, engaging, shareable
```

**Example (Instagram):**
```
Colorful smoothie bowl with tropical fruits for Instagram,
bright and airy food photography aesthetic,
healthy lifestyle summer vibes,
square format with negative space for text overlay,
trendy, engaging, shareable
```

---

## UI/UX Design

### App Screenshot Mockup

```
[Device type] mockup showing [app type] interface,
[design style] UI design,
[color scheme],
realistic device rendering,
[setting/context if applicable],
high fidelity mockup
```

**Example:**
```
iPhone 15 Pro mockup showing fitness tracking app interface,
modern minimal UI design with glassmorphism elements,
dark mode with vibrant accent colors,
realistic device rendering at slight angle,
gym setting with soft bokeh background,
high fidelity mockup
```

### Icon Design

```
[Icon concept] icon,
[style] design style,
[color palette],
[shape/container],
clean vector appearance,
suitable for [size/platform]
```

**Example:**
```
Cloud storage icon,
flat design style with subtle gradients,
blue to purple gradient on white background,
rounded square container,
clean vector appearance,
suitable for iOS app icon at 1024x1024
```

### Dashboard Visualization

```
[Dashboard type] dashboard interface,
[design style],
showing [data types/charts],
[color scheme],
[platform/device],
modern data visualization
```

---

## Illustration & Art

### Character Design

```
[Character description],
[art style],
[pose/action],
[setting/background],
[color palette],
[mood/expression],
detailed character design
```

**Example:**
```
A friendly robot assistant with rounded features and glowing blue eyes,
Pixar-style 3D render,
waving hello pose with slight tilt,
clean gradient background,
white and sky blue with orange accents,
cheerful and approachable expression,
detailed character design
```

### Scene Illustration

```
[Scene description],
[illustration style],
[time of day/lighting],
[perspective/composition],
[key elements],
[mood/atmosphere],
[technical specs]
```

**Example:**
```
A cozy bookshop interior with tall wooden shelves and reading nooks,
warm watercolor illustration style,
late afternoon golden light through bay windows,
wide angle perspective with depth,
stacks of books, antique lamps, comfortable armchairs,
peaceful nostalgic atmosphere,
high detail illustration
```

### Abstract Art

```
[Concept/theme] abstract composition,
[art movement/style],
[colors],
[shapes/forms],
[texture],
[mood],
contemporary art quality
```

---

## Photography Styles

### Portrait

```
[Subject description],
portrait photography,
[lighting style],
[background],
[lens/framing],
[mood/expression],
professional portrait quality
```

**Example:**
```
Professional business woman in her 30s with confident expression,
portrait photography,
Rembrandt lighting with soft fill,
neutral gradient background,
85mm lens medium close-up,
approachable and competent mood,
professional portrait quality
```

### Landscape

```
[Location/scene],
landscape photography,
[time of day/weather],
[composition technique],
[atmospheric elements],
[technical specs]
```

**Example:**
```
Icelandic waterfall with dramatic cliffs,
landscape photography,
blue hour with moody overcast sky,
rule of thirds with leading lines,
mist and spray creating atmosphere,
wide angle, long exposure effect, 16K resolution
```

### Architecture

```
[Building/structure],
architectural photography,
[perspective],
[lighting conditions],
[style emphasis],
[technical quality]
```

---

## Technical Specifications

### Resolution Keywords

| Keyword | Effect |
|---------|--------|
| 4K | Good detail |
| 8K | Very detailed |
| 16K | Maximum detail |
| ultra detailed | Enhanced fine details |
| hyper realistic | Photorealistic quality |

### Camera/Lens Keywords

| Keyword | Effect |
|---------|--------|
| wide angle | Expansive view, slight distortion |
| telephoto | Compressed perspective |
| macro | Extreme close-up detail |
| tilt-shift | Miniature effect |
| 35mm film | Analog film aesthetic |
| bokeh | Blurred background |
| shallow depth of field | Subject isolation |

### Lighting Keywords

| Keyword | Effect |
|---------|--------|
| golden hour | Warm, directional |
| blue hour | Cool, atmospheric |
| Rembrandt lighting | Dramatic portrait |
| soft box | Even, diffused |
| rim light | Edge highlighting |
| backlit | Silhouette effect |
| high key | Bright, low contrast |
| low key | Dark, high contrast |

### Art Style Keywords

| Keyword | Effect |
|---------|--------|
| photorealistic | Like a photograph |
| digital art | Clean digital illustration |
| oil painting | Traditional paint texture |
| watercolor | Soft, flowing colors |
| anime/manga | Japanese animation style |
| 3D render | CGI appearance |
| vector art | Clean, scalable graphics |
| concept art | Game/film design style |
| surrealist | Dream-like, unusual |

---

## Negative Prompt Templates (Stable Diffusion)

### General Quality

```
blurry, low quality, low resolution, jpeg artifacts,
pixelated, noisy, grainy, watermark, signature,
text, logo, banner, cropped, out of frame
```

### Portrait Quality

```
distorted face, extra limbs, mutated hands,
bad anatomy, deformed, ugly, duplicate,
morbid, disfigured, out of proportion
```

### Professional Photos

```
amateur, unprofessional, low lighting,
bad composition, cluttered background,
harsh shadows, overexposed, underexposed
```

---

## Prompt Builder Class

```python
class PromptTemplate:
    """Build prompts from templates."""

    TEMPLATES = {
        "hero_image": (
            "A {product} in a {setting}, "
            "{style} photography style, "
            "{lighting} lighting, "
            "{composition} shot, "
            "{mood}, "
            "professional advertising quality, 8K resolution"
        ),

        "product_shot": (
            "{product} on a {surface}, "
            "product photography, "
            "{lighting} lighting, "
            "{angle} view, "
            "{details}, "
            "clean minimalist composition, studio quality"
        ),

        "character": (
            "{character_description}, "
            "{art_style}, "
            "{pose}, "
            "{background}, "
            "{colors}, "
            "{mood}, "
            "detailed character design"
        ),

        "landscape": (
            "{location}, "
            "landscape photography, "
            "{time_of_day}, "
            "{composition}, "
            "{atmosphere}, "
            "{technical}"
        )
    }

    @classmethod
    def build(cls, template_name: str, **kwargs) -> str:
        """Build prompt from template."""
        if template_name not in cls.TEMPLATES:
            raise ValueError(f"Unknown template: {template_name}")

        template = cls.TEMPLATES[template_name]
        return template.format(**kwargs)


# Usage
prompt = PromptTemplate.build(
    "hero_image",
    product="artisan coffee cup",
    setting="cozy cafe with exposed brick",
    style="commercial",
    lighting="warm natural",
    composition="centered with depth",
    mood="inviting morning atmosphere"
)
```

---

## Platform-Specific Templates

### LinkedIn Banner (1584x396)

```
[Professional scene/concept],
modern corporate photography,
clean and professional,
wide panoramic composition,
[brand colors],
suitable for LinkedIn banner with text space on left
```

### Twitter/X Header (1500x500)

```
[Scene/concept],
[style],
wide cinematic composition,
[mood],
space for profile picture overlay on left,
engaging social media header
```

### YouTube Thumbnail (1280x720)

```
[Subject/scene] for YouTube thumbnail,
bold and eye-catching,
high contrast colors,
simple composition with clear focal point,
space for text overlay,
attention-grabbing
```

### Instagram Story (1080x1920)

```
[Content/scene] for Instagram story,
vertical mobile-first composition,
[aesthetic style],
space for text at top and bottom,
engaging and scrollable
```
