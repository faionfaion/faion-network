# Agent Integration — Adobe Firefly Integration

## When to use
- Generating commercial-safe imagery for marketing, product pages, or editorial content without stock photo licensing risk
- Creating on-brand variations of existing images at scale (background removal, generative fill for product shots)
- Producing vector assets from text descriptions for icon sets or illustration libraries
- Text effects and typography treatments for campaign assets where custom lettering is needed
- Batch asset generation within an established Creative Cloud workflow where Photoshop/Illustrator are already in use

## When NOT to use
- UI/UX prototyping — use Figma; Firefly does not produce interactive components or design system artifacts
- Developer handoff assets — Firefly generates raster/vector art, not production-ready SVG component assets
- When generative credits are exhausted and content deadline is imminent — Firefly is credit-gated; have a fallback (stock, human designer)
- Brand-critical assets requiring exact color accuracy — AI generation introduces color variation; always validate against brand palette
- When the style guide strictly requires human-created imagery (some editorial, legal, or medical contexts)

## Where it fails / limitations
- Firefly cannot be driven by a Claude agent directly — there is no public Firefly API as of 2026 for third-party automation; automation requires Adobe's Firefly Services (enterprise, beta access required)
- Generative Fill in Photoshop is interactive-only; batch processing requires Photoshop Actions or the Firefly Services Batch API
- Text-to-vector (Illustrator) produces decorative vectors, not production SVG icons suitable for UI; paths are complex and non-editable
- Prompt sensitivity is high: small wording changes produce radically different outputs — determinism is not guaranteed
- Firefly is trained on Adobe Stock; outputs may trend toward stock photo aesthetic, which may not match brand personality
- Generative credits expire and are not always predictable in consumption; enterprise batch jobs can exhaust monthly allowance

## Agentic workflow
A Claude subagent can operate in the design-brief and post-processing layers of Firefly integration: generate structured image briefs (prompt + style parameters + negative prompt) from brand guidelines, and analyze Firefly output images for brand consistency (color, composition, subject matter). Direct API automation requires Adobe Firefly Services enterprise access. For teams with that access, an agent can submit batch generation jobs via the Firefly Services REST API and poll for completion.

### Recommended subagents
- Custom brand-brief-generator agent — takes a content brief and brand guide, outputs structured Firefly prompt + style parameters + negative prompt for each asset needed
- Custom asset-review agent — takes generated image paths, evaluates against brand checklist (color palette, composition, subject), flags non-compliant assets

### Prompt pattern
```
You are a creative director generating image prompts for Adobe Firefly.
Given this content brief: {{content_brief}}
And this brand guide extract: {{brand_guide}}

For each image needed, output:
{
  "positive_prompt": "...",  // max 200 chars, specific style and subject
  "negative_prompt": "...",  // elements to exclude
  "style_preset": "...",     // photo / art / graphic
  "aspect_ratio": "...",     // 16:9 / 1:1 / 4:5
  "content_type": "..."      // photo / illustration / vector
}

Rules:
- Reference brand colors by name, not hex (Firefly understands color names)
- Avoid trademarked elements, real people, brand logos
- Keep prompts specific: "minimalist flat illustration, teal and white, single coffee cup, white background" not "coffee image"
```

```
Audit these generated image assets against brand standards:
<brand_standards>{{brand_standards}}</brand_standards>
<image_descriptions>{{image_descriptions}}</image_descriptions>

For each image, rate:
- Color alignment: pass / partial / fail
- Style consistency: pass / partial / fail
- Subject appropriateness: pass / partial / fail

Flag any that require regeneration or manual editing before publishing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Adobe Firefly Services CLI | Batch generation via enterprise API | developer.adobe.com/firefly-services |
| `adobe-io-cli` | Adobe I/O API gateway management | `npm install -g @adobe/aio-cli` / developer.adobe.com |
| `imagemagick` | Post-processing: resize, format convert, color analysis | imagemagick.org |
| `exiftool` | Read/write image metadata including AI generation provenance | exiftool.org |
| `sharp` (Node.js) | Fast image processing for batch pipeline | `npm install sharp` / sharp.pixelplumbing.com |
| `colormath` (Python) | Validate generated image color palette against brand colors | `pip install colormath` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Adobe Firefly Services | SaaS (enterprise) | Yes — REST API | Batch generation API; requires enterprise agreement + beta access |
| Adobe Creative Cloud API | SaaS | Partial — REST API | Photoshop API actions; can trigger Generative Fill programmatically |
| Midjourney | SaaS | No public API | High quality; Discord-only; not agent-drivable without unofficial workarounds |
| DALL-E 3 (OpenAI) | SaaS | Yes — REST API | Alternative; strong API; no commercial-safe training guarantee at Firefly level |
| Stability AI | SaaS/OSS | Yes — REST API | Open weights available; self-hostable; less commercial-safe than Firefly |
| Cloudinary | SaaS | Yes — REST API | Asset storage + transformation pipeline; integrates with Firefly output |
| Brandfolder | SaaS | Yes — REST API | Digital asset management; stores and distributes Firefly-generated assets |

## Templates & scripts
See templates.md for brand-compliant prompt template and batch generation schema.

Inline: batch image prompt generator:
```python
import json

def generate_firefly_prompts(brief: dict, brand: dict) -> list:
    """Generate structured prompts for Firefly Services batch API."""
    prompts = []
    for asset in brief["assets"]:
        prompt = {
            "prompt": f"{asset['subject']}, {brand['style']}, {brand['color_palette_description']}, {asset['context']}",
            "negativePrompt": f"text, watermark, logo, realistic photo, {brand.get('exclude', '')}",
            "size": {"width": asset["width"], "height": asset["height"]},
            "numVariations": asset.get("variants", 3),
            "contentClass": asset.get("content_class", "photo"),
        }
        prompts.append({"asset_id": asset["id"], "firefly_params": prompt})
    return prompts

# Example usage:
brief = json.load(open("content_brief.json"))
brand = json.load(open("brand_guide.json"))
batch = generate_firefly_prompts(brief, brand)
print(json.dumps(batch, indent=2))
```

## Best practices
- Always include a negative prompt — Firefly default outputs trend toward stock photo aesthetics without exclusion constraints
- Use Firefly for iteration speed in early creative stages; involve a human art director before any asset goes to production
- Store generation prompts alongside assets in metadata (exiftool) for reproducibility and content provenance documentation
- Validate generative credits before scheduling a batch job — depleted credits during a campaign launch are a real risk
- For typography/text effects, proof in Illustrator at intended print or screen size before approval — Firefly vectors are decorative quality, not production-ready
- Document AI-generated content with C2PA content credentials for transparency compliance

## AI-agent gotchas
- There is no public Firefly API for individuals — agent automation requires Adobe Firefly Services enterprise contract; agents cannot autonomously generate via standard Creative Cloud accounts
- Prompt outputs are non-deterministic; an agent running the same prompt twice will get different results — always generate variants and human-select
- Adobe generative credits are consumed per variation, not per prompt; an agent that requests 10 variants per asset will exhaust credits rapidly
- Firefly's content moderation rejects certain subjects silently (returns error, not explanation); agents must handle rejection with a rephrased prompt retry
- Color descriptions in prompts are interpreted loosely; "navy blue" in Firefly may not match brand navy — post-processing color correction is often needed

## References
- Adobe Firefly Services documentation — developer.adobe.com/firefly-services
- Adobe Creative Cloud API (Photoshop) — developer.adobe.com/photoshop
- C2PA Content Credentials standard — c2pa.org
- "Prompt Engineering for Image Generation" — Stability AI guide — stability.ai/learn
- Adobe "Commercial Safety" framework — adobe.com/firefly/commercial-safety
