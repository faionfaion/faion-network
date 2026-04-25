# Agent Integration — Image Generation Basics

## When to use
- Generating article header images, social media visuals, or product mockups from text descriptions
- Creating image variations for A/B testing content at scale
- Automating visual asset production in content pipelines
- Reimagining/restyling an existing image (vision → describe → generate cycle)
- Batch generating illustration sets for structured prompts (e.g., FAQ cards, product categories)

## When NOT to use
- Pixel-perfect brand consistency is required — DALL-E 3 revised prompts silently alter inputs
- Images will be used without human review in regulated contexts (medical, legal, financial)
- Subject requires real-person likeness — OpenAI policy blocks this
- High-volume generation where cost is primary constraint — DALL-E 3 at $0.04–$0.12/image adds up fast; use Replicate/Flux for cost
- Exact text rendering in image is required — all current models struggle with on-image text

## Where it fails / limitations
- DALL-E 3 rewrites prompts silently; `revised_prompt` in the response often diverges substantially from input
- `n=1` is the only option for DALL-E 3 — generating 10 variations requires 10 API calls
- DALL-E 2 edit/variation endpoints are being deprecated; do not build new workflows on them
- Batch generator uses `ThreadPoolExecutor` — DALL-E 3 rate limit is 5 images/minute on tier 1; threads will hit 429 errors
- `describe_image` uses GPT-4o vision then re-generates; quality depends on how accurately vision describes the original
- Content policy enforcement is inconsistent — edge-case prompts may succeed today and fail next week
- `generate_and_save` downloads image synchronously; DALL-E URLs expire in ~1 hour so stale pipelines will 404

## Agentic workflow
A Claude subagent receives a content brief and uses `ImagePromptBuilder` to construct a structured prompt with style, lighting, composition, and technical spec fields. The subagent calls `generate_image`, captures `revised_prompt` for audit logging, downloads the image, and returns a structured result. For batch operations, an orchestrator agent dispatches up to 3 concurrent generation calls (respecting rate limits), collects results, and surfaces failures for re-prompt retry.

### Recommended subagents
- `haiku` — Execute single or batch image generation API calls with retry
- `sonnet` — Translate content brief into `ImagePromptBuilder` structured prompt with style/lighting decisions
- `sonnet` — Quality review: use vision to assess generated image against brief criteria, decide pass/retry

### Prompt pattern
```xml
<task>
Generate an image for this brief:
<brief>{{CONTENT_BRIEF}}</brief>

Use ImagePromptBuilder. Specify:
- subject
- style (photorealistic/digital_art/oil_painting/watercolor/anime/3d_render/sketch/minimalist)
- lighting (golden_hour/studio/dramatic/soft/neon/natural)
- composition (rule of thirds, centered, etc.)
- technical specs (4k/depth_of_field/cinematic/wide_angle)

Return the Python ImagePromptBuilder call and final prompt string.
</task>
```

```
Attempt image generation with this prompt: "{{PROMPT}}"
Size: {{SIZE}}  Quality: {{QUALITY}}  Style: {{STYLE}}
On success return: {"url": "...", "revised_prompt": "..."}
On rate limit (429): wait 12s, retry up to 3 times.
On content violation: return {"error": "policy", "prompt": "{{PROMPT}}"}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| openai (Python SDK) | DALL-E 3/2 API client | `pip install openai` / platform.openai.com/docs |
| replicate | Access SDXL, Flux via Replicate API | `pip install replicate` |
| Pillow | Local image validation, resize, format convert | `pip install Pillow` |
| httpx / requests | Download generated images | `pip install httpx` |
| imagehash | Perceptual hash for dedup/cache key | `pip install imagehash` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI DALL-E 3 | SaaS | Yes — Python SDK | Best quality for photorealistic; rate limited; revised_prompt can diverge |
| Replicate (SDXL, Flux-schnell) | SaaS | Yes — Python SDK | Cheapest; Flux-schnell best speed/quality balance |
| Midjourney | SaaS | Partial — unofficial API only | Highest artistic quality; no official API; automation is against ToS |
| Stability AI API | SaaS | Yes — REST API | SDXL + SD3 access; good for fine-tuned model access |
| Cloudinary | SaaS | Yes | Image storage, transform, CDN; complements generation |
| AWS S3 | SaaS | Yes | Standard storage for generated images at scale |
| Imgix | SaaS | Yes | Real-time image transform/CDN on top of S3 |

## Templates & scripts
See `templates.md` for `ImagePromptBuilder`, `BatchImageGenerator`, `generate_and_save`.

Inline: rate-limit-safe batch generator (25 lines):
```python
import time
from openai import OpenAI, RateLimitError

def safe_batch_generate(prompts: list[str], size="1024x1024", delay=12.0) -> list[dict]:
    """Generate images with rate-limit backoff (5 img/min tier-1 limit)."""
    client = OpenAI()
    results = []
    for i, prompt in enumerate(prompts):
        for attempt in range(3):
            try:
                resp = client.images.generate(
                    model="dall-e-3", prompt=prompt, size=size, n=1
                )
                results.append({"prompt": prompt, "url": resp.data[0].url,
                                 "revised": resp.data[0].revised_prompt})
                break
            except RateLimitError:
                time.sleep(delay * (2 ** attempt))
        else:
            results.append({"prompt": prompt, "error": "rate_limit"})
        if i < len(prompts) - 1:
            time.sleep(delay)  # 5 img/min = 12s/img
    return results
```

## Best practices
- Always log `revised_prompt` alongside the original prompt — divergence reveals what the model actually generated
- Use content-based cache keys (hash of prompt+size+quality+style) to avoid regenerating identical images
- Download images immediately after generation; DALL-E URLs are pre-signed and expire in ~60 minutes
- For A/B testing, generate variants with the same base prompt + style modifier, not completely different prompts
- Validate generated images with Pillow before downstream use: check dimensions, file size > 0, format integrity
- Use `style="natural"` for product photography; `style="vivid"` for artistic/marketing content
- For SDXL/Flux on Replicate: output_format="webp" reduces storage ~40% vs PNG with negligible quality loss
- Test prompts manually on the first 3 before launching a 100-image batch

## AI-agent gotchas
- `revised_prompt` is often significantly different from input — agent downstream logic must not assume the generated image matches the original prompt word-for-word
- DALL-E 3 rate limit is per-organization not per-API-key — concurrent agents sharing an org key will hit shared limits
- Content policy decisions are not deterministic — a prompt that passed yesterday may be rejected today; agent must handle refusal gracefully without infinite retry
- `ThreadPoolExecutor` in `BatchImageGenerator` does not respect API rate limits; running 10 threads on a tier-1 key will fail immediately — serialize with delay instead
- DALL-E 2 variation/edit endpoints require PNG with alpha channel; passing JPEG causes a cryptic 400 error
- Replicate `run()` is synchronous and blocking — wrap in `asyncio.to_thread()` if using in async context
- The `reimagine_image` pattern (vision describe → regenerate) produces a loosely-related image, not a precise variation; manage human expectations

## References
- https://platform.openai.com/docs/guides/images
- https://platform.openai.com/docs/api-reference/images
- https://replicate.com/black-forest-labs/flux-schnell
- https://replicate.com/stability-ai/sdxl
- https://help.openai.com/en/articles/6654000-best-practices-for-dall-e
- https://openai.com/api/pricing/
