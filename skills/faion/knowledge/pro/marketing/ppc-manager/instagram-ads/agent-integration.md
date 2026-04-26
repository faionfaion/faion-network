# Agent Integration — Instagram Ads

## When to use
- B2C/DTC brands with a strong visual story (fashion, beauty, food, lifestyle, fitness).
- Reels-driven discovery campaigns leveraging short-form vertical video.
- Stories-based promotional moments (limited-time offer, new launch, event).
- Retargeting Instagram engagers (profile visits, story views, reel saves) without leaving the platform.
- Influencer-style native creative campaigns where polished/over-produced ads underperform.
- Shopping ads with product tags via Meta Commerce Manager catalog.

## When NOT to use
- B2B or enterprise sales with long sales cycles — LinkedIn outperforms.
- Audience demographics skewing >55, low-income, or non-mobile — Instagram penetration drops sharply.
- Static, text-heavy creative — Instagram penalizes via reduced delivery; Facebook Feed is more forgiving.
- Markets with strict influencer-disclosure or pharma rules where native-look ads risk compliance.
- Anything requiring desktop conversion paths — Instagram is overwhelmingly mobile.

## Where it fails / limitations
- Reels and Stories require vertical 9:16 video; using square 1:1 reduces delivery quality and cost-per-result.
- iOS 14.5+ App Tracking Transparency cut signal — Conversions API (CAPI) is now mandatory, not optional.
- Instagram-positions data inside the Meta API is bundled with Facebook; agents must explicitly filter `publisher_platform=instagram` AND `instagram_positions`.
- Story top/bottom safe zones (250px each) eat into creative real estate — assets that look fine in design tools are clipped.
- Reels ad autoplay differences: muted vs unmuted varies by user and device, captions are non-negotiable.
- Music licensing in user-generated Reels does NOT transfer to ads; agents reusing organic Reels in ad-format must re-license audio.
- Frequency caps are softer than Facebook Feed — burnout faster.

## Agentic workflow
A subagent owns the Instagram-only ad pipeline: creative brief → asset spec validation (resolution, aspect, duration, safe-zones) → upload → ad-set creation with `publisher_platforms: ["instagram"]` → daily creative-fatigue scan (frequency, CTR decay) → swap creative → CAPI conversion validation. Heavy human-in-loop on creative concept, music licensing, influencer-collab approvals. Run separate ad sets per placement (Feed / Stories / Reels) for clean attribution, then collapse winners.

### Recommended subagents
- A `meta-creative-validator` subagent — runs ffprobe on uploaded videos, asserts resolution/duration/aspect-ratio per placement, flags safe-zone violations.
- A `reels-ad-builder` — generates 3-5 vertical-video ad variants from a product brief, optimizes hook in first 1-2s.
- `faion-ads-agent` — owns campaign/ad-set/ad mutations via Meta Marketing API.
- A `frequency-fatigue-monitor` — daily scan: flag ad sets with frequency >3.0 or CTR drop >25% week-over-week.
- `faion-sdd-executor-agent` (existing) — runs setup as SDD feature with acceptance gates.

### Prompt pattern
```
You are an Instagram Reels ad scriptwriter.
Input: product description, target audience, key benefit.
Output 3 scripts:
- duration: 15-30 seconds
- hook: ≤2 seconds, visual + 1 line of caption text
- body: visual cuts every 1-2 seconds
- CTA: visible on screen for last 3 seconds
- format: JSON with [{shot_n, visual, voiceover, on_screen_text, duration_sec}]
```

```
Validate Instagram ad creative spec.
Input: file path, intended placement (feed|story|reels|explore).
Output: {valid: bool, resolution, aspect_ratio, duration_sec, file_size_mb, issues: [...]}
Reject if: aspect ratio mismatch, duration outside placement bounds, file >4GB, no captions burned-in for sound-off.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook_business` Python SDK | Marketing API client | `pip install facebook_business` |
| `curl` + Graph API | Direct REST for ad-set / creative ops | preinstalled |
| `ffmpeg` / `ffprobe` | Video transcoding + spec validation | apt/brew |
| Meta Ads Library | Search competitor ads, public archive | facebook.com/ads/library |
| Meta Pixel Helper / Events Manager | Validate pixel + CAPI events | chrome.google.com/webstore |
| Meta Marketing API CLI (community) | Bulk operations | github.com/facebook/facebook-python-business-sdk |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Ads Manager | SaaS native | Yes — full API | Standard platform |
| Meta Commerce Manager | SaaS native | Yes — Catalog API | Required for Shopping ads |
| AdEspresso | SaaS | Yes | Bulk ad creation, A/B testing |
| Madgicx | SaaS | Yes | AI-driven Meta ad ops |
| Smartly.io | SaaS | Yes | Enterprise creative automation |
| Triple Whale / Northbeam | SaaS | Yes | E-comm attribution incl. Meta |
| CapCut / Canva | SaaS | Limited (no agent API) | Creative production |
| Remotion | OSS | Yes — programmatic video | React-based video as code |
| Meta CAPI Gateway | SaaS native | Yes | Server-side conversion forwarding |

## Templates & scripts
See `templates.md` for ad-set + creative templates. The README has full curl examples for Stories/Reels ad-set creation, Shopping ad creative, and audience targeting.

Inline ffprobe-based validator:

```bash
#!/usr/bin/env bash
# validate_ig_creative.sh <file> <placement>
FILE="$1"; PLACE="$2"
P=$(ffprobe -v quiet -print_format json -show_streams -show_format "$FILE")
W=$(echo "$P" | jq -r '.streams[] | select(.codec_type=="video") | .width')
H=$(echo "$P" | jq -r '.streams[] | select(.codec_type=="video") | .height')
DUR=$(echo "$P" | jq -r '.format.duration')
case "$PLACE" in
  feed)   [[ "$W" == "1080" && ("$H" == "1080" || "$H" == "1350") ]] || { echo "FAIL feed needs 1:1 or 4:5"; exit 1; };;
  story|reels)
    [[ "$W" == "1080" && "$H" == "1920" ]] || { echo "FAIL needs 9:16 1080x1920"; exit 1; }
    [[ $(echo "$DUR <= 90" | bc) == 1 ]] || { echo "FAIL reels >90s"; exit 1; };;
esac
echo "PASS $W x $H, ${DUR}s"
```

## Best practices
- Always burn captions into video files — 85%+ watch sound-off; native auto-captions are unreliable across regions.
- Test placements as separate ad sets for first 7-14 days, then consolidate winners. Mixing placements in one ad set hides which is profitable.
- For Reels, design native: phone-shot aesthetic, jump cuts, on-screen text, trending-style audio (re-licensed). Studio-polished ads underperform.
- Use Advantage+ Creative cautiously — auto-crop can ruin carefully composed images.
- Implement Conversions API server-side BEFORE iOS 14 traffic exceeds 30% of audience — pixel-only attribution will lose 30-50%.
- Match Instagram-account `instagram_actor_id` to brand's actual Business Account; mismatches cause "page link errors" at creative submission.
- Frequency cap: 2-3/week for conversion campaigns, 5-7/week for awareness. Default uncapped is too high for IG.
- Use Catalog ads (DPA) for retargeting product viewers — outperforms generic creative 3-5x.

## AI-agent gotchas
- Meta API versions deprecate every 2 years (each version supported ~2 yrs); agents pinned to old versions break silently. Pin and monitor.
- Token expiry: long-lived user tokens last 60 days; system-user tokens are non-expiring but require BM admin to issue.
- `actions` field in Insights returns array of action types — agents must filter by `action_type` (e.g., `offsite_conversion.fb_pixel_purchase`); reading `actions[0]` is wrong.
- Currency in `spend` is account-local, not always USD; agents reporting cross-account must convert via FX.
- iOS Aggregated Event Measurement: only top 8 prioritized events per domain count; agents adding 10+ pixel events lose visibility on lower-priority ones.
- `daily_budget` is in cents, not micros (`5000` = $50.00); easy off-by-100x bug compared to Google Ads.
- Promoted-object pixel events for IG conversions need both `pixel_id` and `custom_event_type`; missing custom_event_type silently optimizes for any conversion.
- Some `instagram_positions` (notably `ig_search`) are not auto-included with broad placements; agents must explicitly enumerate.
- Lead Gen ads on IG can use Instant Experience or in-app forms; agents must pick one and stick — switching mid-campaign resets learning.
- Special Ad Categories (housing, employment, credit) auto-disable interest+demographic targeting; agents creating campaigns in these verticals must set `special_ad_categories` field.

## References
- Meta Marketing API: https://developers.facebook.com/docs/marketing-apis/
- Instagram positions reference: https://developers.facebook.com/docs/marketing-api/reference/ad-set/targeting-specs/
- Conversions API: https://developers.facebook.com/docs/marketing-api/conversions-api/
- Aggregated Event Measurement: https://www.facebook.com/business/help/721422165168355
- Reels ad specs: https://www.facebook.com/business/ads-guide/instagram-reels-ads
- Shopping ads: https://www.facebook.com/business/m/instagram-shopping
