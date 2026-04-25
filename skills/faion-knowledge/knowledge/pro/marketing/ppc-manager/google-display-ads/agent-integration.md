# Agent Integration — Google Display Ads

## When to use
- Programmatic Display campaigns at scale: bulk responsive-display-ad asset uploads, placement-list management, audience refresh.
- Remarketing pipelines where customer-segment shifts (cart-abandoner, churn-risk) trigger fresh audience uploads via Customer Match.
- Cleaning up "wasted" placements — agents pull placement reports nightly and exclude apps/sites with zero conversions and high spend.
- Launching upper-funnel awareness campaigns alongside Search where the structure is templated (same ad-group themes, swapped imagery).

## When NOT to use
- Direct-response performance with no brand recognition — Display CTRs are typically 0.05–0.5%; Search converts far better.
- B2B niche where audience size is too small for Display reach to matter.
- Brand-safety-sensitive campaigns without curated placement lists — Display can land you on long-tail content you don't want.
- Replacing Performance Max — if you want AI-driven cross-channel, use `google-pmax` instead of stitching Display by hand.

## Where it fails / limitations
- Responsive Display Ads (RDA) auto-generate combinations — you cannot fully control which headline / image combo serves; brand teams hate this.
- Image asset requirements are strict: marketing images 1.91:1 (1200x628 min), square 1:1 (1200x1200 min), logo 1:1 + 4:1. Wrong ratios silently rejected.
- `placement.url` targeting accepts both domains and YouTube channel URLs; mixing them creates ambiguous criteria that don't fire as expected.
- Display reach numbers in Keyword Planner are inflated; treat them as upper-bound only.
- Audience-only targeting (no contextual signal) often delivers very low CTR; combining audience + topic + placement narrows fast.
- View-through conversions inflate Display ROAS — agents that optimize on view-through often shift budget to vanity placements.

## Agentic workflow
A Display agent should manage three loops: (1) creative refresh — periodically upload new image assets and rotate them into RDAs, (2) placement hygiene — daily query of `detail_placement_view`, exclude underperformers, (3) audience refresh — push updated remarketing lists. All three should produce a diff preview before committing. Pair with a "policy gate" check: validate image ratios + file size locally before calling `AssetService` to avoid noisy upload failures.

### Recommended subagents
- `faion-ads-agent` — Google Ads execution (shares credentials with Search/Shopping flows).
- `faion-sdd-executor-agent` — gates code changes that wire creative pipelines into product.
- A creative-generation agent (vision-capable model) for sourcing/cropping image variants — Display is asset-hungry.

### Prompt pattern
```
System: You are the Display agent. Validate image ratios and file size
        BEFORE upload. For placement exclusions, only act when impressions
        > 5000 AND conversions == 0 AND cost > $20 over 14 days. Diff first.
User:   Refresh RDA assets in campaign 4567 with these 6 new images,
        retire any image with <0.1% CTR and >2k impressions.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | Display campaign + asset operations | `pip install google-ads` |
| Google Ads Editor | Bulk offline edits, fast diff | https://ads.google.com/intl/en/home/tools/ads-editor/ |
| `Pillow` (PIL) | Pre-flight image validation (size, ratio) | `pip install Pillow` |
| `ffmpeg` | Crop/resize source assets to required ratios | https://ffmpeg.org |
| Google Ad Manager → Display & Video 360 | Programmatic display beyond GDN | https://marketingplatform.google.com/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Display Network (GDN) | SaaS | Yes (Ads API) | Default reach surface, 2M+ websites. |
| YouTube (via Display in Search/Display) | SaaS | Partial | Use Video campaigns for YouTube-first; Display reaches it incidentally. |
| Display & Video 360 (DV360) | SaaS | Yes (separate API) | For programmatic / private marketplaces, not the same API as Google Ads. |
| Customer Match | SaaS | Yes (Ads API) | Hashed-email upload for retargeting; agents handle hashing + chunked upload. |
| Pinterest / Reddit Display | SaaS | Yes (own APIs) | Worth pairing for niche audience reach when GDN underdelivers. |
| Brand-safety vendors (DoubleVerify, IAS) | SaaS | Yes (API) | Programmatic exclusion lists agents can sync into Google Ads. |

## Templates & scripts
See `templates.md` and the inline RDA / placement helpers in `README.md`. Inline image pre-flight (run before `upload_image_asset`) — saves wasted API calls and developer-token quota:

```python
# image_preflight.py — validate Display image asset locally
from PIL import Image
import math, os

ALLOWED = {"marketing": (1.91, (1200, 628)),
           "square":    (1.00, (1200, 1200)),
           "logo":      (1.00, (1200, 1200))}
MAX_BYTES = 5 * 1024 * 1024  # 5 MB

def preflight(path: str, kind: str) -> dict:
    if kind not in ALLOWED:
        return {"ok": False, "reason": f"unknown kind {kind}"}
    target_ratio, (min_w, min_h) = ALLOWED[kind]
    size = os.path.getsize(path)
    with Image.open(path) as im:
        w, h = im.size
    ratio = w / h
    ok = (size <= MAX_BYTES and w >= min_w and h >= min_h
          and math.isclose(ratio, target_ratio, abs_tol=0.05))
    return {"ok": ok, "ratio": round(ratio, 3), "w": w, "h": h, "bytes": size}
```

## Best practices
- Combine targeting layers: audience AND topic, OR audience AND placement — pure broad audience burns budget.
- Always upload at least 5 marketing images, 5 square images, 1 logo — fewer assets = less rotation = creative fatigue.
- Set `target_content_network = True` and disable Search/Search Partner explicitly on Display campaigns; default settings can leak.
- Build placement-exclusion lists at the account level (shared library) so every Display campaign inherits them automatically.
- Use Customer Match + similar audiences for retargeting; raw cookie remarketing is degrading post-cookie deprecation.
- Frequency cap (3–7 impressions per user per week) — Display without caps creates ad fatigue and brand annoyance fast.
- Monitor `placement_type` in reports separately for `WEBSITE`, `MOBILE_APPLICATION`, `YOUTUBE_VIDEO`; mobile-app inventory often dominates spend with poor conversions.

## AI-agent gotchas
- Agents auto-generating ad copy often exceed the 30-char headline / 90-char description limit and the request fails server-side.
- Image asset uploads send raw bytes; agents that pass URLs without fetching them first hit `AssetError.INVALID_IMAGE`.
- Models confuse `placement` (specific URL) with `topic` (Google's content category) — these are different criterion types.
- Customer Match list upload requires SHA-256 of normalized lowercase email; LLMs frequently skip the lowercase / strip step → 0% match rate.
- View-through conversions: agents reading `metrics.conversions` may miss `metrics.view_through_conversions`; double-counting risk if both summed.
- Human-in-loop checkpoint: enabling a Display campaign, raising budget >25%, removing an exclusion list, switching to "Optimized targeting" (which expands audience automatically).
- "Optimized targeting" auto-expansion: Google can ignore your audience config and target whoever it wants. Agents must explicitly disable it for tight-targeted campaigns.

## References
- Display Network overview — https://support.google.com/google-ads/answer/2404190
- Responsive Display Ads — https://support.google.com/google-ads/answer/7005917
- Image asset specs — https://support.google.com/google-ads/answer/9120872
- Customer Match — https://support.google.com/google-ads/answer/6379332
- Optimized targeting — https://support.google.com/google-ads/answer/11458007
