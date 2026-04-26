# Agent Integration — Instagram Basics

## When to use
- Standing up an Instagram presence (founder, brand, creator) and configuring profile, highlights, content pillars.
- Reels-first content strategy where the team can shoot/edit but needs scripts and hooks.
- Auditing an underperforming Instagram account to identify whether decline is reach, engagement, or conversion.
- Drafting carousel scripts (10 slides) and Story sequences for product launches.
- Pairing with paid social (Meta Ads) where organic posts feed retargeting audiences.

## When NOT to use
- Audience is purely B2B enterprise — LinkedIn + email outperforms; do not waste cycles here.
- Team cannot shoot/edit video; Instagram without Reels gets ~1/4 the reach of a Reels-led account.
- Brand requires text-heavy, long-form content (use blog + LinkedIn).
- Regulated industries where every visual claim needs review — cadence is incompatible with Instagram's velocity.

## Where it fails / limitations
- Organic reach is structurally low (often 1-3% of followers for photos) and shrinking — without Reels, growth stalls.
- API limits posting flexibility: Reels can be scheduled via Graph API, but Stories with stickers (polls, quizzes) often cannot.
- Hashtag strategy has weakened; Meta now favors topic understanding, so over-indexing on hashtag tiers underperforms.
- DM automation must be approved (Messenger Platform); unapproved bots get the account flagged.
- Cross-posting Reels from TikTok with the watermark suppresses reach; agents must strip and remix.

## Agentic workflow
A Claude subagent is best at scripting Reels (hook + body + CTA in 30 seconds), drafting carousel scripts (slide-by-slide), and proposing weekly Story sequences. The agent should NOT auto-post Reels (visual QA matters) but CAN schedule via Buffer/Later if approved by the operator. Pair the agent with a research subagent that pulls trending audio and competitor recent winners daily.

### Recommended subagents
- `faion-social-agent` — sonnet for ideation and copy; haiku for caption/hashtag generation; opus only when refreshing the pillar strategy quarterly.
- A `reels-script-agent` — focused on the 7-15 sec virality format: hook, payoff, retention loop, CTA.
- A `carousel-agent` — outputs 10-slide narrative with one idea per slide and a save-worthy summary slide.
- `faion-content-marketer` cross-skill agent for caption tone-matching when Instagram is one channel of many.

### Prompt pattern
```
Pillar mix: educational 40%, behind-scenes 30%, results 20%, inspirational 10%.
Brand voice <attached>. Output 5 Reels scripts: each = 1 hook (<2s), 3 body
beats with on-screen text, 1 CTA. Length 15-30s. No emojis. Mark which beat
is the retention spike (rewatch trigger).
```

```
Carousel for product launch <feature>. Audience: indie devs. 10 slides.
Slide 1 hook headline, slides 2-8 one point each (large readable text),
slide 9 summary, slide 10 CTA. Output as markdown with slide titles,
copy, and a one-line visual prompt per slide.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `instagrapi` (Python) | Read profile, fetch insights — unofficial, breakage risk | https://github.com/subzeroid/instagrapi |
| `instaloader` | Backup posts/stories/highlights for analysis | https://instaloader.github.io/ |
| `ffmpeg` | Trim, resize 9:16, strip watermarks | https://ffmpeg.org/ |
| `imagemagick` | Carousel slide generation from markdown | https://imagemagick.org/ |
| `gh-action-instagram-publisher` (community) | Scheduled publishing via Graph API | https://github.com/topics/instagram-publisher |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Instagram Graph API | SaaS (official) | Yes | Reels + posts publishing for Business/Creator accounts |
| Buffer | SaaS | Yes (API) | Reels + carousel + Stories scheduling |
| Later | SaaS | Yes (API) | Visual planner; preview grid before posting |
| Metricool | SaaS | Yes (API) | Analytics + scheduling, hashtag analyzer |
| Iconosquare | SaaS | Yes (API) | Deeper analytics, competitor tracking |
| ManyChat | SaaS | Yes (API) | Approved DM automation flows |
| Canva | SaaS | Yes (API) | Programmatic carousel generation |
| Postiz | OSS | Yes (self-host) | OSS scheduler with Instagram support |
| CapCut | SaaS (free) | Partial | Reels editing — manual; agents can output edit scripts |

## Templates & scripts
See `templates.md` for bio, Reel script, Story sequence, and carousel templates. Inline carousel-to-image helper:

```bash
#!/usr/bin/env bash
# carousel-render.sh — turn 10 markdown slides into 1080x1350 PNGs.
# Input: slides.md with one slide per --- separator; first line is title.
set -euo pipefail
mkdir -p out
csplit -s -z slides.md '/^---$/' '{*}'
i=0
for f in xx*; do
  i=$((i+1))
  TITLE=$(head -1 "$f")
  BODY=$(tail -n +2 "$f")
  convert -size 1080x1350 xc:white -gravity North \
    -font DejaVu-Sans-Bold -pointsize 64 -annotate +0+120 "$TITLE" \
    -font DejaVu-Sans -pointsize 36 -annotate +0+360 "$BODY" \
    "out/slide-$i.png"
done
rm xx*
```

## Best practices
- Pillar discipline beats clever ideas: enforce the agent's prompt to label every draft with a pillar; reject pillar-less output.
- Reels' first 1.5 seconds decide reach. Force the agent to write the hook separately and rate it 1-5; only ship 4+.
- Always include on-screen text — 80% of viewers watch muted; agents that produce voiceover-only scripts fail.
- Hashtag minimalism: 3-5 mixed tiers, not 30. Agent prompts that ask for "30 hashtags" hurt performance.
- Save a "winners library" of past top posts and inject the top 5 into every ideation prompt as positive examples.
- Pair every Reel with a Story re-share within 24h; agent should produce both in the same content brief.

## AI-agent gotchas
- LLMs over-use exclamation marks and emojis in captions; instruct explicitly and validate output.
- Hashtag suggestions go stale fast; do not let the agent pick from training data — fetch current top hashtags from a research subagent.
- Carousel scripts that put 30+ words on slide 1 fail — enforce a max-words-per-slide constraint in the prompt.
- Reel scripts written by LLMs default to listicle structure; force narrative or transformation arcs for variety.
- "Trending audio" cannot be inferred by the model; require an external lookup before generation.
- Auto-DMs without ManyChat approval get accounts limited; never let an agent send DMs via unofficial APIs.
- Brand-voice drift over a long ideation session is real; reset context every 50 drafts.

## References
- Meta for Developers, "Instagram Graph API" — https://developers.facebook.com/docs/instagram-api
- Meta Business, "Instagram Reels best practices" — https://business.instagram.com/
- Hootsuite, "Instagram algorithm explained" — https://blog.hootsuite.com/instagram-algorithm/
- Later, "Instagram strategy guides" — https://later.com/blog/instagram-tips/
- Buffer, "Reels playbook" — https://buffer.com/resources/instagram-reels/
- ManyChat, "Instagram DM automation rules" — https://manychat.com/instagram
