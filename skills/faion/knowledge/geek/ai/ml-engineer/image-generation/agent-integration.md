# Agent Integration — Image Generation

## When to use
- Generating marketing visuals, social media graphics, or product mockups as part of an automated content pipeline
- Producing custom illustrations for articles, blog posts, or newsletters where stock photography is inadequate
- Rapid UI/UX prototyping: visualizing interface concepts before implementation
- Generating variation sets (A/B test creatives) at scale for advertising campaigns
- Brand asset generation with consistent style through fine-tuned models or style references
- AI news pipelines where each article requires a unique header image generated from the article summary

## When NOT to use
- Legal/medical/financial documents where image hallucinations create liability
- Photorealistic images of real named people — content policy violations + legal risk (likeness rights)
- Logo design requiring precise vector output — generative models produce raster; use a designer or vector tools
- High-volume generation where per-image cost matters at scale — self-host Flux schnell (Apache 2.0) instead of paying per API call
- Consistent character generation across many images without Flux Kontext or LoRA — models don't preserve identity by default
- Anything requiring exact pixel-level control (infographics with precise data, technical diagrams)

## Where it fails / limitations
- Text rendering in images is unreliable for strings longer than 25 characters even with GPT-4o/DALL-E 3 — never use image generation for text-heavy content
- Consistent character appearance across a series requires seeds (SD) or reference image support (Flux Kontext) — standard API calls produce visually different people each time
- DALL-E 3's `revised_prompt` silently modifies your prompt for safety — the generated image may not match the input prompt; log `revised_prompt` for debugging
- Content policy rejections are unpredictable on borderline prompts — implement retry with softened prompt and exponential backoff
- Aspect ratio must match intended use case at generation time — upscaling or cropping after the fact degrades quality significantly
- Midjourney has no official API — only Discord bot or unofficial wrappers; not suitable for automated pipelines

## Agentic workflow
Use a prompt-engineer subagent to transform a raw content brief into a structured image prompt using the formula [Subject] + [Style] + [Lighting] + [Composition] + [Details] + [Technical], then pass the structured prompt to an image-generator subagent that selects the model based on requirements (artistic → Midjourney-style prompts for Flux Dev; OCR text in image → DALL-E 3/GPT-4o; high-volume batch → Flux schnell self-hosted) and calls the API. A quality-checker subagent uses a vision model to verify the generated image matches key requirements before accepting it; on failure, the loop retries with a revised prompt up to 3 times.

### Recommended subagents
- `prompt-engineer` — transforms content brief into structured image prompt; applies style guidelines
- `image-generator` — selects model + API, executes generation, returns image URL/path + revised_prompt
- `quality-checker` — uses VLM (Claude/GPT-4o) to verify image matches requirements: subject present, style correct, no obvious artifacts
- `batch-scheduler` — manages concurrent generation requests within rate limits; queues and retries

### Prompt pattern
```
You are an image prompt engineer. Transform this content brief into an optimized generation prompt.

Brief: {brief}
Target model: {model}  # dall-e-3 | flux-dev | sdxl
Style guidelines: {style}
Aspect ratio: {ratio}  # 1:1 | 16:9 | 9:16

Output a single optimized prompt following this formula:
[Subject description], [Art style], [Lighting conditions], [Composition], [Specific details], [Technical specs]

Do not include: real people's names, copyrighted characters, explicit content.
```

```python
import openai, base64
from pathlib import Path

def generate_image(prompt: str, size: str = "1792x1024") -> dict:
    client = openai.OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    img = response.data[0]
    return {
        "url": img.url,
        "revised_prompt": img.revised_prompt,  # log this — DALL-E may have changed your prompt
        "model": "dall-e-3",
    }
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | DALL-E 3 and GPT-4o image generation | `pip install openai` / https://platform.openai.com/docs/guides/images |
| `replicate` | Flux, SDXL, and 100+ models via API | `pip install replicate` / https://replicate.com/docs |
| `diffusers` | Hugging Face local inference (SD, Flux) | `pip install diffusers transformers accelerate` / https://huggingface.co/docs/diffusers |
| `stability-sdk` | Stability AI API (SD 3.5) | `pip install stability-sdk` / https://stability.ai/stable-image |
| `fal-client` | Flux Pro via fal.ai API | `pip install fal-client` / https://fal.ai/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Images API | SaaS | Yes | DALL-E 3 + GPT-4o; best text rendering, structured JSON response |
| Replicate | SaaS | Yes | Flux, SDXL, ControlNet via simple API; pay-per-second; good for prototyping |
| Black Forest Labs (Flux) | SaaS | Yes | Flux Pro/Dev/Kontext API; best anatomy + photorealism |
| fal.ai | SaaS | Yes | Fast Flux inference; webhook support for async agent pipelines |
| AWS Bedrock | SaaS | Yes | Stability AI SD 3.5 Enterprise; HIPAA/SOC2 compliant for regulated industries |
| RunPod | SaaS | Partial | GPU rental for self-hosted Flux schnell / SDXL; cost-effective at volume |

## Templates & scripts
See `templates.md` for full prompt templates and batch generation patterns.

Minimal batch generation with retry:
```python
import time
from openai import OpenAI

def batch_generate(prompts: list[str], model: str = "dall-e-3") -> list[dict]:
    client = OpenAI()
    results = []
    for prompt in prompts:
        for attempt in range(3):
            try:
                resp = client.images.generate(model=model, prompt=prompt, size="1792x1024", n=1)
                results.append({"prompt": prompt, "url": resp.data[0].url, "revised": resp.data[0].revised_prompt})
                break
            except Exception as e:
                if "content_policy" in str(e).lower():
                    prompt = soften_prompt(prompt)  # remove specific proper nouns, explicit terms
                time.sleep(2 ** attempt)
        else:
            results.append({"prompt": prompt, "url": None, "error": "failed after 3 attempts"})
    return results
```

## Best practices
- Always cache generated images — identical prompts sent twice waste money; hash the prompt + parameters as cache key
- Log `revised_prompt` from DALL-E 3 alongside the output — it shows what the model actually generated vs. what you requested; essential for debugging drift
- Use negative prompts in Stable Diffusion (`blurry, deformed, ugly, watermark`) to filter common artifacts; negative prompts don't exist in DALL-E API
- For consistent brand style, use Flux Kontext with a reference image rather than trying to engineer style consistency through prompt keywords alone
- Pre-filter prompts through a content-policy checker before hitting the API — rejected requests still cost latency and may count against rate limits
- Match the generation model's strength to the task: `dall-e-3` for editorial/conceptual, `flux-1-schnell` for bulk social posts, `sdxl + LoRA` for brand-specific assets

## AI-agent gotchas
- Image URLs from OpenAI API expire after 1 hour — agents must download and store images immediately, not just log the URL for later retrieval
- Rate limits on image APIs are much lower than text APIs (DALL-E 3: 5 images/minute on Tier 1) — agent batch jobs must implement proper throttling or queue
- "Revised prompt" silent modification means the agent's quality-check assertion ("does the image show X?") must be based on what was actually generated, not the requested prompt
- Human-in-the-loop checkpoint: for marketing assets going to paid channels, require human approval of generated images before publishing — automated quality checks can miss brand guideline violations, off-brand color schemes, or subtle content issues

## References
- OpenAI Images API: https://platform.openai.com/docs/guides/images
- Flux models (Black Forest Labs): https://bfl.ai/
- Stable Diffusion 3.5 (Stability AI): https://stability.ai/stable-image
- Replicate Flux inference: https://replicate.com/black-forest-labs/flux-1.1-pro
- HuggingFace Diffusers: https://huggingface.co/docs/diffusers/index
- Prompt engineering guide (OpenAI): https://platform.openai.com/docs/guides/prompt-engineering
