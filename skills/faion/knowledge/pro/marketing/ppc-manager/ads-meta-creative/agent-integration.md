# Agent Integration — Meta Creative Best Practices

## When to use
- Brainstorming and producing the first wave of 5-10 creatives for a new product launch.
- Bi-weekly creative refresh — refilling the rotation when winners show fatigue (CTR decay > 20%).
- Scaling a winning concept into systematic variations (hook A × visual B × proof C).
- Generating native-style UGC scripts for paid creators or AI video tools.
- Producing localized variants (1:1 + 9:16 + reel-cuts, EN + native-language).

## When NOT to use
- Regulated verticals (health claims, finance, gambling) — auto-generated copy/images can violate policy or law; route through compliance.
- Account that hasn't yet found a winning angle — generating 50 variants of a non-working concept just multiplies the loss.
- Extremely brand-controlled industries (luxury, fashion editorial) — agent-generated visuals look generic; book a real shoot.

## Where it fails / limitations
- Meta's Standard Enhancements automatically rewrites copy and adds music to videos in 2024+ accounts; the variant your agent produced may not be the one served.
- Meta image policy (text-overlay rule was removed but readability still affects delivery) — agents that pile on text get throttled silently.
- AI-generated images are increasingly detected and de-prioritized; Meta's Advantage+ creative downranks "synthetic" assets when it can identify them.
- Video creative needs captions burned in for Stories/Reels — agents rendering "audio-on by default" videos lose the 85% of users who watch on mute.
- Frequency cap signals are at the ad-set level, not creative; an agent rotating creatives within a fatigued ad set won't reset frequency.

## Agentic workflow
Three-stage pipeline: (1) **strategy agent** picks angles per audience from a prior winning-asset library + product brief; (2) **production agent** generates copy + image (Midjourney / DALL-E / nano-banana) or video script (Runway / Veo / Sora); (3) **QA agent** lints copy for banned words, validates image specs (1:1, 9:16), checks captions on video, runs synthetic LP click. Always upload as PAUSED, eyeball-review, then enable. Post-launch loop: an analyzer agent reads ad-level CTR + thumb-stop rate after 5-7 days and 1k+ impressions, kills < 0.5% CTR creatives, requests variations of winners.

### Recommended subagents
- `faion-ads-agent` — uploads creative via Marketing API, manages ad-level structure.
- `faion-content-marketer` (knowledge tier) — writes hook-first primary text and headlines.
- `faion-improver` — closes loop: read performance → kill losers → request variations.
- `faion-brainstorm` — diverge/converge for new angle generation when stuck.

### Prompt pattern
```
Generate 5 ad concepts for {product} targeting {audience}. Each concept:
hook (one line, stop-the-scroll), primary text (~125 chars before "See more"
+ 100 more), headline (≤40 chars, benefit-focused), CTA button choice.
Mix formulas: question, bold claim, curiosity, social proof, direct benefit.
No emojis. No banned claims (best, #1, guaranteed). Output JSON.
```

```
Audit ads in ad set {id}. For each: report CTR, thumb-stop rate, frequency,
CPA. Flag fatigue (CTR decline >20% week-over-week, freq >3). For winners
(top 20% CTR), propose 3 variations preserving the hook but rotating the
visual or proof. For losers, recommend kill.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook-business` Python SDK | Upload creatives, get ad-level insights | `pip install facebook-business` |
| Canva API | Programmatic image generation from templates | https://www.canva.dev/docs/connect/ |
| Figma + plugins | Design system → ad batches | https://www.figma.com/developers |
| FFmpeg | Resize/recut video to 1:1 + 9:16, burn captions | `apt install ffmpeg` |
| Whisper (OpenAI) | Auto-caption generation for video | `pip install openai-whisper` |
| Replicate / Fal.ai | Hosted image/video model APIs | https://replicate.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Midjourney | SaaS | Limited (Discord) | Best brand-look images; weak API; use Replicate proxies |
| DALL-E 3 / `gpt-image-1` | SaaS API | Yes | OpenAI Image API; good for product mockups |
| Runway Gen-3 / Veo / Sora | SaaS API | Yes | Short-form video, expensive per second |
| ElevenLabs | SaaS API | Yes | Voiceover for VSLs |
| CapCut / Adobe Express | SaaS | Limited | UI-first; templates work but agent-driven editing weak |
| Billo / Insense | SaaS | Yes | Real UGC creators on demand; agents can brief + receive |
| Smartly.io | SaaS | Partial | Enterprise creative automation; good for catalog ads |
| Pencil (Brandtech) | SaaS | Partial | AI ad generation; predicts performance |
| Meta Ad Library | Free | Yes | Scrape competitor ads for inspiration |

## Templates & scripts
See `templates.md` for image/video spec sheets. Inline asset-validator — agents skip this and ship ads that get rejected:

```python
from PIL import Image

BANNED_WORDS = {"best", "#1", "guaranteed", "amazing", "free"}  # adjust per offer

def lint_copy(primary, headline, description):
    """Reject ad copy that violates common Meta + good-practice rules."""
    issues = []
    if len(headline) > 40: issues.append(f"headline {len(headline)}>40")
    if len(description) > 30: issues.append(f"desc {len(description)}>30")
    text = f"{primary} {headline} {description}".lower()
    hits = [w for w in BANNED_WORDS if w in text]
    if hits: issues.append(f"banned words: {hits}")
    if primary.count("\n\n") < 1: issues.append("no paragraph break — add whitespace")
    return issues

def validate_image(path, target="square"):
    img = Image.open(path)
    w, h = img.size
    ratio = w / h
    expected = {"square": (1.0, 0.05), "vertical": (0.5625, 0.02)}[target]
    if abs(ratio - expected[0]) > expected[1]:
        return [f"ratio {ratio:.3f} expected {expected[0]}"]
    if min(w, h) < 1080:
        return [f"too small: {w}x{h}"]
    return []
```

## Best practices
- Always produce 1:1 AND 9:16 of every concept; Stories/Reels inventory is the cheapest CPM and you waste it without vertical assets.
- Burn captions into video — 85% watch on mute; uncaptioned video is wasted spend.
- Hook in the first 3 seconds (video) or first 7 words (image overlay). After that the user is gone.
- Refresh creative every 14 days even if metrics are still good — proactively avoids the cliff. CTR decay is exponential, not linear.
- Keep a "winner library" of past top performers tagged by angle/visual/format. Agents iterate on these, never start from scratch.
- For systematic A/B testing: change ONE variable per ad (hook OR visual OR copy) — multivariate inside a single ad set is uninterpretable.

## AI-agent gotchas
- LLM-generated copy has tells: em-dashes, "in today's fast-paced world", "leverage", "robust", "seamless", "elevate" — lint for these.
- Agents generating 10 variants tend to repeat hooks with minor word changes; embedding-similarity check before upload, drop dupes.
- Image models hallucinate text on images that gets read as gibberish — render text overlays in code (PIL/CSS), not in the image generation prompt.
- Video models often fail captions or render them in wrong aspect; always re-caption with Whisper post-render and overlay programmatically.
- Standard Enhancements is on by default; agents producing brand-controlled copy must explicitly disable it per ad creative.
- Human-in-loop checkpoint: first creative on a new product, any imagery showing people (model release / likeness rights), any claim mentioning numbers or competitors.
- Don't let an agent kill creatives at < 1000 impressions or < $20 spend — that's noise, not signal.

## References
- https://www.facebook.com/business/ads-guide/update/image (specs)
- https://www.facebook.com/business/help/120391115283200 (video specs)
- https://www.facebook.com/business/help/531428077950670 (Advantage+ creative)
- https://www.facebook.com/business/inspiration (Ad Library)
- https://developers.facebook.com/docs/marketing-api/reference/ad-creative/
