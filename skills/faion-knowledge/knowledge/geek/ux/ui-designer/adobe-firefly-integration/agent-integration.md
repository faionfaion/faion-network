# Agent Integration — Adobe Firefly Integration

## When to use
- Generating commercial-safe image assets for UI mockups, marketing banners, or product visuals
- Creating vector assets in Illustrator via text-to-vector prompts for icon sets or illustrations
- Removing or replacing image backgrounds in Photoshop for product shots or UI hero images
- Applying AI-generated text effects and typography variations at scale
- Producing asset variations (color, style, format) from a single source for A/B testing

## When NOT to use
- When the design requires a coherent custom illustration style — Firefly outputs generic aesthetics
- When iterating on UI layout or component design — Figma is the correct tool
- When the team has no Adobe CC licenses — generative credits are consumed per generation
- When output needs to strictly match an established illustration system — Firefly cannot learn custom styles without training
- When speed is critical and assets must integrate directly into a Figma file without round-trips

## Where it fails / limitations
- Generated images often need manual refinement to match brand-specific visual language
- Text rendering inside generated images is unreliable — Firefly still produces garbled text in images
- Generative Fill quality degrades on complex UI screenshots (pixel art, dense interfaces)
- Credit consumption is opaque for automated pipelines; large batches exhaust allotments quickly
- Firefly API (Firefly Services) requires Adobe enterprise agreement and is not available on standard CC plans
- API rate limits and latency (2–8s per generation) make synchronous loops impractical

## Agentic workflow
An agent can drive Adobe Firefly through the Firefly Services REST API to batch-generate image variations, apply Generative Fill to placeholder regions, or produce vector assets from text prompts. The agent constructs a prompt from a design brief, calls the API, downloads results, and stores them in a shared asset folder for human review. Because Firefly output requires brand alignment review, the pipeline must include a human-in-loop checkpoint before any asset proceeds to production. Agents work best when the prompt template is pre-approved by a designer and the agent only fills in variable parameters (subject, color, format).

### Recommended subagents
- `faion-sdd-executor-agent` — executes an asset-generation task defined in an SDD task file, calling Firefly API and logging results
- Custom batch-generation script agent — loops over a CSV of asset specs, calls Firefly Services, downloads outputs

### Prompt pattern
```
Generate a commercial-safe hero image for a SaaS landing page:
Subject: {subject}
Style: clean, minimal, soft gradient
Dimensions: 1200x630px
Output: JPEG, sRGB

Return: asset URL + generation ID for tracking.
```

```
# Firefly Services API — minimal call
curl -X POST https://firefly-api.adobe.io/v2/images/generate \
  -H "Authorization: Bearer $FIREFLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"{prompt}","size":{"width":1200,"height":630},"numVariations":3}'
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| adobe-firefly-cli (unofficial) | Thin shell wrapper around Firefly Services REST | github.com/nicholasgasior/firefly-cli |
| curl / httpx | Direct REST calls to Firefly Services | stdlib |
| imagemagick | Post-process downloaded assets (resize, crop, convert) | apt install imagemagick |
| rclone | Sync generated assets to S3/GCS/Cloudflare R2 | rclone.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Adobe Firefly Services | SaaS (enterprise) | Yes — REST API | Requires Adobe enterprise plan; OAuth2 machine-to-machine auth |
| Adobe Creative Cloud API | SaaS | Partial | CC Apps (PS/AI) automatable via UXP plugins, not purely headless |
| Photoshop API | SaaS (enterprise) | Yes — REST | Headless PS operations: remove-bg, smart-crop, generative fill |
| Illustrator API | SaaS (beta) | Limited | Still gated behind enterprise agreement as of 2026 |
| Cloudinary | SaaS | Yes | Can receive and transform Firefly outputs; acts as CDN for generated assets |
| Bynder / Brandfolder | SaaS (DAM) | Yes — REST | Destination for approved Firefly assets; enforces brand consistency |

## Templates & scripts
See templates.md for prompt templates.

Minimal batch generation script (Python, <50 lines):

```python
import os, requests, csv, pathlib

TOKEN = os.environ["FIREFLY_TOKEN"]
API = "https://firefly-api.adobe.io/v2/images/generate"
OUT = pathlib.Path("firefly-output")
OUT.mkdir(exist_ok=True)

def generate(prompt: str, name: str) -> None:
    resp = requests.post(
        API,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
        json={"prompt": prompt, "size": {"width": 1200, "height": 630}, "numVariations": 1},
        timeout=30,
    )
    resp.raise_for_status()
    for i, item in enumerate(resp.json()["outputs"]):
        url = item["image"]["presignedUrl"]
        img = requests.get(url, timeout=30).content
        (OUT / f"{name}_{i}.jpg").write_bytes(img)
        print(f"Saved {name}_{i}.jpg")

with open("assets.csv") as f:
    for row in csv.DictReader(f):
        generate(row["prompt"], row["name"])
```

## Best practices
- Pre-define a prompt template approved by the brand team; agents fill variables, never freeform prompts
- Store generation IDs alongside downloaded assets for audit trails and regeneration
- Use `numVariations: 3` and have a human select; never auto-select generated images for production
- Set up a staging folder separate from production assets; require explicit human promotion step
- Cache approved Firefly assets in a DAM (Bynder, Brandfolder) to avoid re-generating the same assets
- Monitor credit consumption per project with a dashboard; alert before budget exhaustion
- For Photoshop Generative Fill via API, always supply a mask rather than relying on auto-detection
- Test prompts manually in Firefly web UI before encoding them into agent pipelines

## AI-agent gotchas
- Firefly Services token expires every 24h; agents must implement OAuth2 client-credentials refresh
- Rate limits (varies by plan, typically 10 req/s) require exponential backoff in batch loops
- Generated image presigned URLs expire in 1 hour — download immediately, do not store the URL
- "Content moderation" blocks can silently return 200 with empty outputs array; always validate length > 0
- Firefly cannot be driven from inside Figma headlessly; any Figma plugin usage requires a human at the keyboard
- Brand-specific style prompts are not reproducible across model updates — Firefly model versions change without notice
- Never pass user-provided freeform text directly to Firefly — sanitize to prevent prompt injection into commercial asset pipeline

## References
- https://www.adobe.com/products/firefly.html
- https://developer.adobe.com/firefly-services/docs/
- https://helpx.adobe.com/firefly/using/generative-credits-faq.html
- https://www.adobe.com/legal/licenses-terms/adobe-firefly.html
- https://developer.adobe.com/photoshop/photoshop-api-docs/
