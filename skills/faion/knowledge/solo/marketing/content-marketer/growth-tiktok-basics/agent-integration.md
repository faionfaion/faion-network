# Agent Integration — TikTok Basics & Setup

## When to use
- Generating video script outlines for educational, build-in-public, or demo formats
- Drafting bio copy and profile optimization recommendations for a new account
- Creating a 30-day content calendar with topic ideas across 3-4 defined pillars
- Analyzing competitors' TikTok accounts to extract content patterns before launch
- Writing caption variants with different hooks for A/B testing

## When NOT to use
- Filming, editing, or uploading video — agents cannot operate mobile apps or video software
- Deciding whether TikTok is the right channel for a specific business (requires audience data)
- Generating trend-based content — trends move in hours; agents working from training data are too slow
- Accounts targeting audiences in countries with TikTok restrictions or bans
- Any workflow requiring posting on behalf of the account — violates TikTok ToS

## Where it fails / limitations
- TikTok's official API is restricted to approved business partners; consumer posting automation is not available
- Hook effectiveness can only be validated through actual platform performance data, not predicted by agents
- Algorithm optimization requires A/B testing real videos; agents cannot simulate the For You Page
- Trend identification requires real-time data; agent knowledge has a cutoff date
- Content that works for one niche (e.g., SaaS founders) may completely fail for another (e.g., B2C lifestyle)

## Agentic workflow
The most useful agentic application is batch script generation: give the agent the 3-4 content pillars, the ICP, and the product description, then request a 4-week content calendar with one-paragraph script outlines per video. A second pass can expand selected outlines into full word-for-word scripts with hook/body/CTA structure. The human films and edits; the agent handles the ideation and scripting layer. Captioning and hashtag research can also be delegated to the agent given a completed video title and topic.

### Recommended subagents
- No dedicated TikTok/social agent exists in the current agents/ directory
- Use a content subagent role: given pillar + ICP + examples, produce structured script outlines
- Use a research subagent role: analyze competitor account content patterns from scraped post data

### Prompt pattern
```
You are writing TikTok video scripts for [PRODUCT] targeting [ICP].
Content pillars: [PILLAR1], [PILLAR2], [PILLAR3].
Format for each script:
- Hook (0-3 sec, spoken + on-screen text identical)
- Body (4-45 sec, 3 numbered points with brief demo note)
- CTA (final 5 sec)

Generate 7 scripts for Pillar: [EDUCATIONAL TIPS].
Each hook must be different formula type (curiosity/challenge/promise/relatability/controversy).
Output as JSON array: [{"hook": "...", "body": [...], "cta": "..."}]
```

```
Write a TikTok bio for [PRODUCT/PERSON].
Constraints: max 80 characters, must include: what you do + who it's for + one CTA word.
Generate 5 variants. No emojis unless they replace a word.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tiktok-api` (unofficial) | Read public TikTok data (use with caution — against ToS) | Various Python wrappers on PyPI |
| `yt-dlp` | Download TikTok videos for competitive research | `pip install yt-dlp` / github.com/yt-dlp/yt-dlp |
| `ffmpeg` | Trim clips, add watermark, convert formats for upload | `brew install ffmpeg` / ffmpeg.org |
| `whisper` | Transcribe competitor videos for content analysis | `pip install openai-whisper` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| TikTok Creative Center | SaaS (free) | No API | Trend and hashtag data; manual research only |
| Pentos | SaaS | Partial — data export | TikTok analytics tracking; no posting API |
| Tokboard | SaaS | No | Viral video tracker; manual only |
| Later | SaaS | Yes — REST API | Scheduling TikTok posts; requires manual video upload first |
| Hootsuite | SaaS | Yes — REST API | Same as Later; cross-platform scheduling |
| CapCut | SaaS/mobile | No API | Best free editor for TikTok-native formats |
| Opus Clip | SaaS | No public API | AI clip extraction from long-form; manual trigger |
| Vidyo.ai | SaaS | No public API | Similar to Opus Clip |

## Templates & scripts
See `templates.md` for educational script, build-in-public series, and product demo script templates.

Minimal yt-dlp command to download and analyze a competitor's recent TikToks:

```bash
# Download last 10 videos from a TikTok user for content research
yt-dlp \
  --playlist-end 10 \
  --write-info-json \
  --skip-download \
  "https://www.tiktok.com/@[USERNAME]"

# Output: JSON files with title, description, view count, duration, hashtags
```

## Best practices
- Write the hook before the rest of the script — if the hook is weak, the video fails regardless of body quality
- Provide the agent with 3-5 real examples of high-performing videos in your niche as format references
- Captions (burned-in text) are not optional — ~70% of TikTok is watched without sound; always script on-screen text alongside spoken text
- Separate the hook text (on-screen) from the spoken hook — they can differ for emphasis
- Post timing matters less than hook quality; optimize hooks before optimizing schedule
- Keep the first batch of scripts focused on educational content — it's the easiest format to execute solo without a production team

## AI-agent gotchas
- Agents generate "safe" hooks by default — they avoid controversy; explicitly prompt for controversy/challenge hooks to get high-tension openers
- Generated scripts often run too long for the format; constrain to word count per section (hook: 8-12 words, body point: 15-25 words)
- TikTok slang and trends embedded in scripts will date quickly; prefer evergreen language unless the agent has real-time trend data
- Do not ask agents to generate hashtag sets — TikTok hashtag effectiveness is volatile and requires real-time Creative Center data
- Agents cannot predict which hook formula will resonate with a specific niche audience; plan to A/B test at least 3 hook types before scaling

## References
- https://www.tiktok.com/business/en/blog (TikTok for Business official)
- https://blog.hootsuite.com/tiktok-algorithm/ (algorithm signals)
- https://later.com/blog/tiktok-marketing/ (scheduling and analytics)
- https://www.tiktok.com/creators/ (TikTok Creator Portal)
