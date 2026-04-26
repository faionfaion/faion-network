# Agent Integration — Instagram Growth Tactics

## When to use
- Generating Reel script outlines (hook, body, CTA) for educational and tutorial content types
- Drafting caption batches for a defined content pillar (educational, BTS, testimonial, CTA-driven)
- Writing DM automation trigger copy ("DM 'GUIDE' to get…") for lead generation posts
- Producing a weekly content calendar with Reel + Story + carousel distribution per the README schedule
- Scripting Story sequences (polls, question boxes, countdown stickers) for engagement campaigns

## When NOT to use
- Generating Reel video itself — the agent produces scripts and concepts, not video files
- Hashtag generation at scale (30 hashtags) — the README explicitly flags this as a shadowban risk; agent should produce 3-5 targeted tags only
- Automated commenting on other accounts — Instagram detects and shadowbans bot-style engagement; human must execute the 30-min daily engagement routine
- Audience analysis without exported data — the agent cannot pull Instagram Insights directly

## Where it fails / limitations
- Reel performance is heavily dependent on the first 1-3 seconds of video; agent scripts the hook but cannot judge if the delivery is compelling
- Instagram algorithm weights are undocumented and shift frequently; recommended posting frequencies (14 Reels/week) are community estimates, not official specs
- DM automation setup requires a third-party tool (ManyChat, Manychat-compatible chatbots) that operates in a grey zone of Instagram ToS
- Story engagement prompts (polls, quizzes) require the human to monitor and respond; the agent can draft them but cannot react to responses
- Local and niche hashtag effectiveness varies by category; agent hashtag suggestions need manual validation against actual hashtag search volumes

## Agentic workflow
Use the agent for two tasks: (1) content batch production — given content pillars, ICP, and the weekly schedule template, produce 14 Reel script hooks + body points + CTAs, 7 Story prompt sequences, and 2-3 carousel outlines per week; (2) performance analysis — given an Instagram Insights CSV export, identify top-performing content types and suggest next week's pillar distribution adjustments. Human films, edits, and posts Reels; agent never touches the upload flow.

### Recommended subagents
- `faion-sdd-executor-agent` — execute weekly Instagram content production tasks from a spec
- `password-scrubber-agent` — sanitize DM conversation exports before feeding into lead analysis

### Prompt pattern
```
You are an Instagram content strategist for <niche>. ICP: <icp>. Brand voice: <voice>.

Generate this week's Reel scripts:
- 2 educational tips (hook + 3 key points + CTA)
- 2 behind-the-scenes (narrative arc + authenticity note)
- 1 trend/entertainment (format suggestion + hook)
- 1 user testimonial (story structure)
- 1 inspirational (emotional hook + lesson)

Each script: hook line (max 5 words), body (3-5 bullet points), CTA (specific action), caption (150 chars max), 3 hashtags.
```

```
Analyze this Instagram Insights export:
<csv_data>

Identify: (1) top 3 Reels by reach %, (2) common hook patterns in high performers, (3) best posting times by engagement, (4) Story completion drop-off points. Recommend content adjustments for next week.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `instagrapi` (Python) | Unofficial Instagram API: read insights, schedule posts | `pip install instagrapi` / https://instagrapi.readthedocs.io |
| `later` API | Scheduled posting for Reels, carousels, stories | https://developers.later.com |
| `manychat` API | DM automation flows (keyword triggers) | https://developers.manychat.com |
| `ffmpeg` | Batch video processing for Reel format compliance | `apt install ffmpeg` / https://ffmpeg.org |
| `pillow` | Auto-generate Story frames and carousel slide images | `pip install pillow` / https://pillow.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Later | SaaS | Yes (REST API) | Best scheduling for Instagram Reels; visual planner |
| ManyChat | SaaS | Yes (API) | DM automation for keyword triggers; ToS-compliant approach |
| Meta Business Suite | SaaS | Yes (Graph API) | Official insights export; limited granularity |
| Canva | SaaS | Yes (Apps SDK) | Carousel slide and highlight cover generation |
| CapCut | SaaS | No API | Reel editing; manual use |
| Hootsuite | SaaS | Yes (REST API) | Scheduling + analytics; more expensive than Later |
| Metricool | SaaS | Yes (REST API) | Cross-platform analytics including Instagram |

## Templates & scripts
See `templates.md` for weekly posting schedule and DM automation script templates.

```python
# Generate carousel slide text from a how-to topic
def carousel_slides(topic, key_points, cta):
    """Produce 10-slide carousel text outline."""
    slides = [
        {"slide": 1, "type": "Hook", "text": f"The complete guide to {topic}"},
        {"slide": 2, "type": "Promise", "text": f"In this carousel: {', '.join(key_points[:3])}"},
    ]
    for i, point in enumerate(key_points, start=3):
        slides.append({"slide": i, "type": "Value", "text": point})
    slides.append({"slide": len(slides) + 1, "type": "Summary", "text": "To recap: " + " | ".join(key_points)})
    slides.append({"slide": len(slides) + 1, "type": "CTA", "text": cta})
    return slides

for s in carousel_slides("Instagram growth", ["Post Reels daily", "Engage 30 min/day", "Use DM triggers"], "Follow for weekly tips"):
    print(f"Slide {s['slide']} [{s['type']}]: {s['text']}")
```

## Best practices
- The hook of a Reel must work with the sound off — text overlay and visual action in the first 1-2 seconds are mandatory
- Reels get redistributed via Explore; feed posts do not — prioritize Reels over static posts for reach goals
- Story polls and question boxes are the highest-engagement Story formats; use them daily rather than passive image stories
- DM trigger campaigns ("DM me 'GUIDE'") convert 3-5x better than link-in-bio clicks for lead magnets — use them for every major value offer
- Post carousels as the second slide hook (a teaser image that implies more content) — carousel swipe rate is the key metric for feed reach
- Batch film content in 2-3 hour sessions weekly; editing and posting daily from scratch leads to inconsistency

## AI-agent gotchas
- **Video production gap:** Agent produces scripts and storyboards; the filming and editing step is entirely human — plan for this production time when generating volume
- **DM automation ToS risk:** ManyChat-style automation is permitted under Instagram's official partner program, but non-partner tools (instagrapi DM sending) are against ToS and risk account suspension
- **Hashtag shadowban:** Agent should never generate 30-hashtag lists; 3-5 highly relevant hashtags is the current safe range
- **Insights access:** Instagram Graph API provides page-level insights only; personal account insights require manual export from the app
- **Algorithm drift:** Reel distribution rules (audio usage, original audio vs trending audio) change frequently; agent recommendations reflect training data, not current algorithm state

## References
- https://about.instagram.com/blog/announcements/instagram-ranking-explained
- https://creators.instagram.com/
- https://later.com/blog/instagram-growth/
- https://blog.hootsuite.com/how-to-get-more-instagram-followers/
- https://developers.facebook.com/docs/instagram-api — Meta Graph API docs
