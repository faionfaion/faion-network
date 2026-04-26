# Agent Integration — Image Generation Tools & Production

## When to use
- Running a multi-provider image generation service where one provider may be unavailable
- Batch-generating style/size variant sets (e.g., 3 styles × 4 sizes = 12 images per concept)
- Building A/B test image sets automatically from a concept description
- Caching production image generation to avoid duplicate API costs
- Automating image generation inside a content pipeline (article images, social cards, etc.)

## When NOT to use
- Single image generation — `ImageGenerationService` adds overhead not justified for one call
- When provider selection logic needs human approval — automated fallback can silently produce lower-quality output
- High-frequency real-time requests (sub-second) — all providers have multi-second latency
- When DALL-E content policy is frequently triggered — automated pipelines will silently skip images

## Where it fails / limitations
- `_upload_image` is not implemented in the base templates — any img2img workflow stub-fails without S3/Cloudinary integration
- `MultiProviderImageService.generate` passes `**kwargs` directly to each provider; DALL-E 3 and SDXL have incompatible parameter sets (e.g., `quality` is DALL-E-specific)
- SHA-256 cache key does not account for prompt normalization (trailing spaces, case) — near-identical prompts miss cache
- `ImagePipeline.generate_variant_set` iterates styles × sizes without rate-limit delay — will 429 on DALL-E at scale
- `_generate_flux` uses `output[0]` — Flux output format varies by model version; some return a URL string, not a list
- Caching stores URLs, not image bytes — cached entries go stale when provider URLs expire (~1 hour for DALL-E)

## Agentic workflow
An agent receives a content brief with target style and size requirements. It calls `ImageGenerationService.generate()` with cache enabled — on cache miss, the service calls the configured provider with retry logic and caches the result. For multi-variant campaigns, an orchestrator agent calls `ImagePipeline.generate_variant_set()`, receives the style × size matrix, then routes each variant to a review subagent that checks dimensions and content before marking it ready. Failed variants are logged with prompt + error for human inspection.

### Recommended subagents
- `haiku` — Execute single image generation with caching and retry; return structured result
- `haiku` — Run batch variant generation for a set of prompts with rate-limit spacing
- `sonnet` — Interpret content brief → select provider, style preset, size; call `PromptTemplates` static methods
- `sonnet` — Quality review: load each generated image path, use vision to check against brief criteria

### Prompt pattern
```xml
<task>
Generate production image for:
<brief>{{BRIEF}}</brief>

Provider: {{PROVIDER}}  (dalle3|sdxl|flux)
Template: {{TEMPLATE}}  (product_photo|logo|social_media|ui_mockup)
Size: {{SIZE}}
Cache: enabled

Return: {"url": "...", "provider": "...", "cached": true|false}
On error: {"error": "...", "provider": "..."}
</task>
```

```python
# Provider selection heuristic for agents
def select_provider(use_case: str) -> str:
    return {
        "product_photo": "dalle3",    # best photorealism
        "logo": "dalle3",             # clean vector-like output
        "social_media": "flux",       # fast + cheap for volume
        "mockup": "sdxl",             # controllable composition
    }.get(use_case, "dalle3")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| openai (Python SDK) | DALL-E 3/2 generation | `pip install openai` |
| replicate | SDXL, Flux, other open models | `pip install replicate` |
| Pillow | Local image validation, format check | `pip install Pillow` |
| boto3 | S3 upload for persistent image storage | `pip install boto3` |
| redis-py | Distributed cache for multi-process pipelines | `pip install redis` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI DALL-E 3 | SaaS | Yes — Python SDK | Best quality; $0.04–$0.12/image; revised_prompt may diverge |
| Replicate SDXL | SaaS | Yes — Python SDK | Good quality; ~$0.002/image; slower than DALL-E |
| Replicate Flux-schnell | SaaS | Yes — Python SDK | Fastest open model; ~$0.001/image; best for high volume |
| Stability AI API | SaaS | Yes — REST API | Access to SD3, SDXL; fine-tuned model support |
| Cloudinary | SaaS | Yes | Upload, transform, CDN; resolves URL expiry problem |
| AWS S3 + CloudFront | SaaS | Yes | Standard production storage; combine with image transform Lambda |
| Redis | OSS/SaaS | Yes | Replace file-based cache with distributed cache for multi-worker pipelines |

## Templates & scripts
See `templates.md` for `ImageGenerationService`, `MultiProviderImageService`, `ImagePipeline`, `PromptTemplates`.

Inline: cache-to-S3 helper (20 lines — resolves URL expiry):
```python
import boto3, hashlib, requests
from pathlib import Path

def cache_to_s3(url: str, prompt: str, bucket: str, prefix: str = "img-gen") -> str:
    """Download generated image and upload to S3; return permanent S3 URL."""
    key = hashlib.sha256(prompt.encode()).hexdigest()[:16]
    ext = "webp" if "webp" in url else "png"
    s3_key = f"{prefix}/{key}.{ext}"
    s3 = boto3.client("s3")
    # check if already uploaded
    try:
        s3.head_object(Bucket=bucket, Key=s3_key)
        return f"https://{bucket}.s3.amazonaws.com/{s3_key}"
    except s3.exceptions.ClientError:
        pass
    data = requests.get(url, timeout=30).content
    s3.put_object(Bucket=bucket, Key=s3_key, Body=data, ContentType=f"image/{ext}")
    return f"https://{bucket}.s3.amazonaws.com/{s3_key}"
```

## Best practices
- Replace file-based URL caching with byte-based caching (download image, store bytes) to avoid expiry; use S3 or Redis as backend
- Normalize prompts before hashing (strip, lowercase) to improve cache hit rate
- Add rate-limit delays in `generate_variant_set`: DALL-E tier-1 = 5 img/min → 12s/call minimum
- Validate kwargs compatibility per provider before passing `**kwargs`; use provider-specific wrapper functions, not unified kwargs passthrough
- Log every generation with: provider, prompt, revised_prompt (DALL-E), cost estimate, cache hit/miss, output path
- For A/B test sets: generate all variants before surfacing any to avoid partial-set delivery
- Pin Replicate model version hashes in config; update intentionally, not automatically
- Use `PromptTemplates` static methods as the single source of truth for prompt construction; avoid ad-hoc prompt strings in pipeline code

## AI-agent gotchas
- `MultiProviderImageService` silently falls back to lower-quality providers on error — agent output metadata must include `provider` field so callers know what they got
- DALL-E 3 `revised_prompt` can produce substantially different images than intended; downstream agents using vision to validate generated images should compare against the revised prompt, not the original
- Replicate `flux-schnell` returns an iterator object, not a list — `output[0]` raises `TypeError`; use `next(iter(output))` instead
- File-based cache stores provider URLs which expire — agents resuming after 1+ hour will get 404 on cached entries; always revalidate before returning cached result
- `a_b_test_images` returns images labeled A/B/C but does not track which variant was shown to which user — agent must integrate with experiment tracking externally
- Concurrent agents sharing one API key hit shared rate limits; use a rate-limiter service (Redis + token bucket) not per-process sleep
- `ImageGenerationService._generate_sdxl` passes `size` as `{width}x{height}` split — Replicate SDXL expects separate `width` and `height` integers, correct

## References
- https://platform.openai.com/docs/guides/images
- https://replicate.com/docs
- https://replicate.com/black-forest-labs/flux-schnell
- https://replicate.com/stability-ai/sdxl
- https://stability.ai/api
- https://cloudinary.com/documentation
