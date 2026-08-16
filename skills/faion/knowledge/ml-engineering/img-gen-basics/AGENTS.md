# Image Generation Basics: DALL-E, Flux, and SDXL

## Summary

**One-sentence:** Produces an image-generation integration — DALL-E 3 / Flux / SDXL via Replicate, ImagePromptBuilder + revised_prompt audit + immediate download + rate-limit handling.

**One-paragraph:** DALL-E 3 is the gold standard for photorealistic generation but rewrites prompts silently (`revised_prompt` in response), has a 5 imgs/min rate limit per org, and returns URLs expiring in ~1 hour. Production wires: log `revised_prompt` for audit, structure prompts via ImagePromptBuilder (subject + style + lighting + composition + technical), download images immediately to durable storage, respect rate limits with exponential backoff, manually verify the first 3 outputs before launching a 100-image batch. For cost-sensitive batches use Flux-schnell or SDXL via Replicate (~100x cheaper).

**Ефективно для:** content engineer, що генерує article headers / social cards / product mockups і потребує детермінованої pipeline з audit trail, rate-limit safety, і cost-aware provider routing.

## Applies If (ALL must hold)

- Generating article headers, social media visuals, or product mockups from text descriptions.
- Pipeline can tolerate prompt rewriting (DALL-E 3) or wants Flux/SDXL cost profile.
- Outputs will pass human review before publish for regulated content (medical / legal / financial).
- A durable artefact storage (S3 / GCS) is available for immediate download.

## Skip If (ANY kills it)

- Pixel-perfect brand consistency required — DALL-E 3 revised prompts silently alter inputs.
- Images used without human review in regulated contexts.
- Subject requires real-person likeness — OpenAI policy blocks this.
- Exact text rendering in image required — all current models struggle.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Provider API key (OpenAI or Replicate) | secret | secrets manager |
| ImagePromptBuilder template + style guide | doc | brand repo |
| Durable artefact storage | S3/GCS URI | infra |
| Rate-limit budget (5/min tier 1) | doc | finops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/multimodal-ai/img-gen-tools` | Sibling: production patterns + multi-provider fallback. |
| `geek/ai/llm-integration/openai-api-integration` | OpenAI SDK baseline for DALL-E. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: structured prompts, log revised_prompt, download immediately, respect rate limit, manual smoke before batch, route by cost. | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for img-gen-config: provider, prompt_builder fields, storage, rate_limit. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: lost revised_prompt, cached URL 404, RL shared key, real-person likeness, on-image text expectation. | ~700 |
| `content/04-procedure.xml` | medium | Steps: pick provider → build prompt → smoke 3 → batch with RL → download to storage → log audit. | ~700 |
| `content/06-decision-tree.xml` | essential | Routes by cost-tolerance + brand-precision needs to DALL-E vs Flux vs SDXL. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `build-prompt` | sonnet | Template fill from style guide. |
| `pick-provider` | opus | Cost vs quality reasoning. |
| `audit-revised-prompt` | haiku | Diff and log. |

## Templates

| File | Purpose |
|---|---|
| `templates/dalle3.py` | DALL-E 3 client with revised_prompt logging + immediate download. |
| `templates/prompt-builder.py` | ImagePromptBuilder (subject + style + lighting + composition + technical). |
| `templates/batch-generator.py` | Batch driver with rate-limit aware backoff. |
| `templates/prompt-generate.txt` | Prompt-template for LLM-assisted prompt construction. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-img-gen-basics.py` | Validate img-gen-config: provider, storage URI, RL budget, prompt_builder fields. | Pre-commit + CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[img-gen-tools]]
- [[openai-api-integration]]
- [[ai-cost-attribution-schema]]

## Decision tree

The tree at `content/06-decision-tree.xml` routes by cost-tolerance + brand-precision: tight brand + cost OK → DALL-E 3; high-volume social → Flux-schnell via Replicate; cost-only with editable seed → SDXL. Walk it before wiring a generator so provider and storage are picked deterministically.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/dalle3.py`

```python
"""
import base64
import requests
from openai import OpenAI

client = OpenAI()


def generate_image(prompt: str, size: str = "1024x1024",
                   quality: str = "standard", style: str = "vivid") -> dict:
    """
    Generate with DALL-E 3. Always log revised_prompt.
    size: "1024x1024" | "1792x1024" | "1024x1792"
    quality: "standard" | "hd"
    style: "vivid" (creative) | "natural" (photorealistic products)
    """
    response = client.images.generate(
        model="dall-e-3", prompt=prompt,
        size=size, quality=quality, style=style, n=1
    )
    return {
        "url": response.data[0].url,
        "revised_prompt": response.data[0].revised_prompt  # log — can diverge from input
    }


def generate_and_save(prompt: str, output_path: str, **kwargs) -> str:
    """Generate and download immediately. URLs expire in ~1 hour."""
    result = generate_image(prompt, **kwargs)
    response = requests.get(result["url"], timeout=30)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def generate_variations(image_path: str, n: int = 3) -> list[str]:
    """DALL-E 2 only. Requires PNG with alpha channel — JPEG causes 400 error."""
    with open(image_path, "rb") as f:
        response = client.images.create_variation(
            image=f, n=n, size="1024x1024", model="dall-e-2"
        )
    return [img.url for img in response.data]


def edit_image(image_path: str, mask_path: str, prompt: str) -> str:
    """DALL-E 2 only. Both image and mask must be PNG with alpha channel."""
    with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
        response = client.images.edit(
            image=img, mask=mask, prompt=prompt,
            n=1, size="1024x1024", model="dall-e-2"
        )
    return response.data[0].url


def describe_image(image_path: str) -> str:
    """Describe image using GPT-4o Vision for describe-then-generate cycle."""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "Describe this image in detail for image generation."},
            {"type": "image_url",
             "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
        ]}]
    )
    return response.choices[0].message.content
```

### `templates/prompt-builder.py`

```python
"""


class ImagePromptBuilder:
    """Build structured image generation prompts from typed components."""

    STYLES = {
        "photorealistic": "photorealistic, highly detailed photograph",
        "digital_art": "digital art, vibrant colors",
        "oil_painting": "oil painting, textured brushstrokes",
        "watercolor": "watercolor painting, soft edges, fluid",
        "anime": "anime style, cel shading",
        "3d_render": "3D render, octane render, highly detailed",
        "sketch": "pencil sketch, hand-drawn",
        "minimalist": "minimalist, clean lines, simple"
    }

    LIGHTING = {
        "golden_hour": "golden hour lighting, warm tones",
        "studio": "professional studio lighting",
        "dramatic": "dramatic lighting, high contrast",
        "soft": "soft diffused lighting",
        "neon": "neon lighting, cyberpunk atmosphere",
        "natural": "natural daylight"
    }

    TECHNICAL = {
        "4k": "4K resolution, ultra detailed",
        "8k": "8K resolution, extremely detailed",
        "depth_of_field": "shallow depth of field, bokeh",
        "wide_angle": "wide angle lens",
        "macro": "macro photography, extreme detail",
        "cinematic": "cinematic composition, film grain"
    }

    def __init__(self):
        self.components: dict[str, str | list] = {
            "subject": "", "style": "", "lighting": "",
            "composition": "", "mood": "", "details": [], "technical": []
        }

    def set_subject(self, subject: str) -> "ImagePromptBuilder":
        self.components["subject"] = subject
        return self

    def set_style(self, style: str) -> "ImagePromptBuilder":
        self.components["style"] = self.STYLES.get(style, style)
        return self

    def set_lighting(self, lighting: str) -> "ImagePromptBuilder":
        self.components["lighting"] = self.LIGHTING.get(lighting, lighting)
        return self

    def set_composition(self, composition: str) -> "ImagePromptBuilder":
        self.components["composition"] = composition
        return self

    def set_mood(self, mood: str) -> "ImagePromptBuilder":
        self.components["mood"] = mood
        return self

    def add_detail(self, detail: str) -> "ImagePromptBuilder":
        self.components["details"].append(detail)
        return self

    def add_technical(self, spec: str) -> "ImagePromptBuilder":
        self.components["technical"].append(self.TECHNICAL.get(spec, spec))
        return self

    def build(self) -> str:
        parts = []
        for key in ("subject", "style", "lighting", "composition"):
            if self.components[key]:
                parts.append(self.components[key])
        if self.components["mood"]:
            parts.append(f"{self.components['mood']} mood")
        parts.extend(self.components["details"])
        parts.extend(self.components["technical"])
        return ", ".join(parts)
```

### `templates/batch-generator.py`

```python
"""
import time
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI, RateLimitError


class BatchImageGenerator:
    """Generate multiple images. Use safe_batch_generate for DALL-E tier-1."""

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.client = OpenAI()

    def generate_batch(self, prompts: list[str], **kwargs) -> list[dict]:
        """Parallel generation. Risk: hits rate limits on tier-1 keys."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = [(p, executor.submit(self._generate_single, p, **kwargs))
                       for p in prompts]
        for prompt, future in futures:
            try:
                results.append({"prompt": prompt, "success": True, **future.result()})
            except Exception as e:
                results.append({"prompt": prompt, "success": False, "error": str(e)})
        return results

    def _generate_single(self, prompt: str, **kwargs) -> dict:
        response = self.client.images.generate(
            model="dall-e-3", prompt=prompt, **kwargs
        )
        return {"url": response.data[0].url,
                "revised_prompt": response.data[0].revised_prompt}


def safe_batch_generate(prompts: list[str], size: str = "1024x1024",
                        delay: float = 12.0) -> list[dict]:
    """
    Rate-limit-safe batch generation for DALL-E tier-1 (5 img/min = 12s/img).
    Retries up to 3 times on RateLimitError with exponential backoff.
    """
    client = OpenAI()
    results = []
    for i, prompt in enumerate(prompts):
        for attempt in range(3):
            try:
                resp = client.images.generate(
                    model="dall-e-3", prompt=prompt, size=size, n=1)
                results.append({
                    "prompt": prompt,
                    "url": resp.data[0].url,
                    "revised": resp.data[0].revised_prompt
                })
                break
            except RateLimitError:
                time.sleep(delay * (2 ** attempt))
        else:
            results.append({"prompt": prompt, "error": "rate_limit"})
        # Inter-image delay — respect 5 img/min limit
        if i < len(prompts) - 1:
            time.sleep(delay)
    return results
```

### `templates/prompt-generate.txt`

```text
-->
<task>
Generate an image for this brief:
<brief>{CONTENT_BRIEF}</brief>

Use ImagePromptBuilder. Specify:
- subject
- style (photorealistic|digital_art|oil_painting|watercolor|anime|3d_render|sketch|minimalist)
- lighting (golden_hour|studio|dramatic|soft|neon|natural)
- composition (rule of thirds, centered, etc.)
- technical specs (4k|8k|depth_of_field|cinematic|wide_angle)

Return the ImagePromptBuilder call and final prompt string, then execute:
Size: {SIZE}  Quality: {QUALITY}  Style: {STYLE}

On success return: {"url": "...", "revised_prompt": "..."}
On rate limit (429): wait 12s, retry up to 3 times.
On content violation: return {"error": "policy", "prompt": "{PROMPT}"}

After success: download image immediately (URL expires ~1 hour).
Log revised_prompt alongside original — it can diverge significantly.
</task>
```
