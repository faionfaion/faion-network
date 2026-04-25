# Agent Integration — YouTube Strategy

## When to use
- Building a content marketing channel around a technical or educational product (SaaS, course, consulting)
- Generating search-driven top-of-funnel awareness where blog SEO has become too competitive
- Repurposing existing written content (blog posts, documentation) into video format
- Building brand authority for a personal brand or solopreneur practice
- Adding a YouTube component to an existing content distribution stack

## When NOT to use
- No defined niche or ICP — YouTube rewards consistent niche focus; generalist channels rarely grow
- No commitment to publishing at least 2 videos per month for 6+ months — YouTube is a compounding channel, not a quick traffic source
- Product has no visual or demonstrable component and audience is not on YouTube (e.g., B2B enterprise compliance software)
- Production bottleneck is unresolved — if writing scripts, recording, and editing cannot be systematized, consistency will break

## Where it fails / limitations
- Thumbnail CTR is the most important growth lever and is entirely visual — agents cannot design thumbnails
- YouTube's algorithm heavily weights watch time and session time, not just views; long videos with poor hooks produce negative signals
- Keyword research tools (VidIQ, TubeBuddy) require platform-specific APIs that are not freely accessible to agents
- Growth is nonlinear: most channels see very slow growth for 6-12 months before compounding; premature strategy pivots kill momentum
- Shorts and long-form require separate optimization strategies that often conflict — a Shorts-first strategy does not convert viewers to long-form subscribers effectively

## Agentic workflow
Claude agents are well-suited for pre-production tasks: keyword research briefs, script outlines, full script drafts, title and description writing, and timestamp generation from a transcript. Sonnet handles script drafting given a topic and outline; Opus is appropriate for strategy design (niche selection, content pillar mapping, 12-week content calendar). Post-production and publishing (upload, thumbnail creation, card/end-screen setup) are human-only steps. Agents can generate 5-10 title variants for A/B testing and draft the full video description optimized for YouTube search.

### Recommended subagents
- `faion-sdd-executor-agent` — for managing a YouTube launch as a structured SDD initiative
- General Claude Sonnet subagent — for script drafting, description writing, title variants
- General Claude Haiku subagent — for timestamp extraction from a transcript, tag list generation

### Prompt pattern
```
Write a YouTube video script for the topic: [topic].
Target keyword: [keyword]. Target audience: [ICP].
Format: Hook (0:00-0:30) → Intro (0:30-1:00) → Content sections with headings →
Recap → CTA (subscribe + [product/newsletter]).
Length: ~10 minutes (approx 1500 words spoken). Conversational tone.
```

```
Write 8 YouTube title variants for a video about [topic].
Primary keyword: [X]. ICP: [Y].
Use these formats: How-to, Number list, "I tried X", Contrarian, Question.
Include keyword naturally. Max 60 characters each.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `yt-dlp` | Download video metadata, transcripts, subtitles | `pip install yt-dlp` / github.com/yt-dlp/yt-dlp |
| `youtube-transcript-api` | Fetch transcripts via Python | `pip install youtube-transcript-api` |
| `ffmpeg` | Video processing, trimming, format conversion | ffmpeg.org |
| `whisper` | OpenAI ASR for transcription (local) | `pip install openai-whisper` |
| `tubebuddy-api` (unofficial) | Keyword research data | TubeBuddy API docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| YouTube Studio | SaaS | Partial — Data API | Upload, analytics, chapters via API; thumbnail upload requires UI |
| VidIQ | SaaS | Partial — API (paid) | Keyword scores, competitor research, SEO tags |
| TubeBuddy | SaaS | Partial — API (paid) | Title A/B testing, SEO score, best-time-to-publish |
| Descript | SaaS | Partial | AI-powered editing from transcript; not fully headless |
| Opus Clip | SaaS | No API | Auto-generates Shorts clips from long-form video |
| CapCut | SaaS/desktop | No API | Editing with auto-captions; popular for Shorts |
| Morning Fame | SaaS | No | Analytics and channel health monitoring |
| Canva | SaaS | Yes — API | Thumbnail generation from templates; automatable |

## Templates & scripts
See `templates.md` for the tutorial script template and video idea template.

Minimal Python script to fetch a YouTube video's transcript and word count:
```python
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join(entry["text"] for entry in transcript)
    return text

def estimate_spoken_minutes(text: str) -> float:
    # Average spoken rate: 130 words per minute
    return len(text.split()) / 130

video_id = "dQw4w9WgXcQ"  # replace with target video
text = get_transcript(video_id)
print(f"Word count: {len(text.split())}")
print(f"Estimated duration: {estimate_spoken_minutes(text):.1f} min")
```

## Best practices
- Write the hook before the rest of the script — the first 30 seconds determine whether viewers stay; a good hook doubles effective watch time
- Thumbnail and title should be designed together as a single unit — the combination drives CTR, not either element alone
- Optimize for "search intent" videos early in channel lifecycle (tutorials, how-to, "X for beginners") before attempting "discovery" content (opinion, commentary)
- Use chapters (timestamps in description) on all videos above 8 minutes — YouTube surfaces individual chapters in search results, increasing impressions
- Reply to every comment in the first 48 hours — early engagement signals boost YouTube's distribution algorithm
- Cross-post the video link to email newsletter, Twitter, and LinkedIn within 2 hours of publishing — external traffic in the first 24 hours is a strong positive signal
- Repurpose long-form video into Shorts clips (best 60-second moment) to drive channel discovery without additional production

## AI-agent gotchas
- Agents cannot assess visual quality, camera framing, or audio quality — production decisions are entirely human
- Script word counts from agents are estimates; actual spoken duration depends on pacing — always record a timing run before full production
- Title keyword research requires external tool data (VidIQ, TubeBuddy search volume) — agents guessing keyword demand without data produce unreliable recommendations
- Thumbnail design cannot be delegated to agents in text-only mode; Canva API integration is needed for automated thumbnail generation
- Agents tend to produce overly long scripts; specify target word count explicitly: "10-minute video = ~1,300 words at a natural spoken pace"
- Tags and description keywords produced by agents should be validated against actual YouTube search autocomplete before publishing

## References
- https://creatoracademy.youtube.com/
- https://vidiq.com/blog/
- https://www.tubebuddy.com/blog
- https://morningfame.com/youtube-analytics/
- https://developers.google.com/youtube/v3
