# Agent Integration — TikTok Growth Strategies

## When to use
- Generating hook variants (5+ per video) in different formula types (curiosity/challenge/promise/controversy/relatability) for A/B testing
- Analyzing watch-time drop-off patterns from TikTok Analytics exports and recommending structural changes
- Drafting trend adaptation scripts where a trending sound/format is provided and the agent adapts it to a specific niche
- Creating a duet/stitch strategy brief: which competitor or niche creators to engage and what angle to take
- Generating cliffhanger sequences ("Part 1" / "Part 2" content arcs) for a series content strategy

## When NOT to use
- Real-time trend identification — agents cannot browse the TikTok Discover page or For You Page
- Selecting which trending sounds to use — sound trend data expires in 24-48 hours; agents' training data is too stale
- Predicting which specific video will go viral — virality is probabilistic and platform-specific
- Running TikTok Ads campaigns — that is a paid media task with its own budget/bidding workflow
- Any automated posting to TikTok — violates ToS and risks account ban

## Where it fails / limitations
- Hook formula effectiveness is niche-dependent; what works for coding content fails for B2B SaaS
- Algorithm signals (watch time, completion, shares) cannot be predicted before publishing; agents can only optimize based on structural principles, not predicted outcomes
- TikTok's search algorithm is distinct from FYP distribution; agents lack real-time keyword search volume data for the platform
- Growth loop tactics (duets, stitches, collaborations) require relationship context that agents do not have
- Advanced tactics like TikTok Shop integration require seller account setup that is entirely human-operated

## Agentic workflow
The most effective agentic workflow for TikTok strategies is hook factory + series planning. Provide the agent with: the top 3 performing video topics (from Analytics), the ICP, and the current content pillars. The agent generates 5 hook variants per topic (one per formula type), drafts a 4-part series outline with cliffhanger transitions, and suggests 3 duet targets from a provided list of niche creator handles. Human validates hooks and films the top 2-3 per week. A second agent pass analyzes the Analytics CSV export weekly to surface watch-time drop patterns and recommend video length adjustments.

### Recommended subagents
- No dedicated TikTok strategy agent exists in the current agents/ directory
- Use a content subagent role: hook generation, series planning, trend adaptation scripting
- Use an analytics subagent role: process Analytics CSV exports, identify drop-off patterns, output recommendations

### Prompt pattern
```
Generate 5 hook variants for a TikTok video on the topic: "[TOPIC]"
Target audience: [ICP]
Product context: [PRODUCT ONE-LINER]

Each hook: one formula type, spoken text (max 10 words) + on-screen text (max 6 words, can differ).
Formula types to cover: curiosity, challenge, promise, relatability, controversy.

Output as JSON:
[{"formula": "curiosity", "spoken": "...", "on_screen": "..."}, ...]
```

```
You have a TikTok Analytics export for the past 30 days.
Top 5 videos by watch time:
{{VIDEO_DATA}}

For each video, the watch-time graph shows the following drop-off points:
{{DROPOFF_DATA}}

Analyze:
1. What structural element caused the largest drop (hook, transition, section length)
2. Recommended change per video with expected completion rate improvement
3. One content format to test in the next 14 days based on patterns

Output as JSON: {"analysis": [...], "test_format": "..."}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `yt-dlp` | Download competitor TikTok videos for structural analysis | `pip install yt-dlp` / github.com/yt-dlp/yt-dlp |
| `ffmpeg` | Extract frame at drop-off timestamp for visual analysis | `brew install ffmpeg` / ffmpeg.org |
| `whisper` | Transcribe competitor videos to analyze hook phrasing | `pip install openai-whisper` |
| TikTok Research API | Academic/verified access to TikTok data | developers.tiktok.com/products/research-api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Pentos | SaaS | Partial — data export | Best TikTok analytics tracker; CSV export for agent analysis |
| Tokboard | SaaS | No API | Viral video tracker; manual monitoring only |
| TikTok Creative Center | SaaS (free) | No API | Trend and hashtag data; manual access only |
| Later | SaaS | Yes — REST API | Scheduling; requires manual video upload; useful for posting timing |
| Sprout Social | SaaS | Yes — REST API | Analytics aggregation across platforms including TikTok |
| Opus Clip | SaaS | No public API | Clip extraction; identifies viral-potential moments |
| CapCut | Mobile/Desktop | No API | Native TikTok editing; auto-captions included |

## Templates & scripts
See `templates.md` in `growth-tiktok-basics/` for educational, build-in-public, and demo script templates. This methodology extends those with advanced hook and series patterns.

Minimal Python script to process TikTok Analytics CSV and surface watch-time patterns:

```python
import csv, json, sys

def analyze_analytics(filepath):
    videos = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            videos.append({
                "title": row.get("Video Title", ""),
                "views": int(row.get("Video Views", 0)),
                "avg_watch_pct": float(row.get("Average Watch Time", "0").replace("%", "") or 0),
                "shares": int(row.get("Shares", 0)),
            })
    videos.sort(key=lambda x: x["views"], reverse=True)
    top5 = videos[:5]
    avg_completion = sum(v["avg_watch_pct"] for v in top5) / len(top5) if top5 else 0
    print(json.dumps({"top5": top5, "avg_completion_top5": round(avg_completion, 1)}, indent=2))

analyze_analytics(sys.argv[1])
```

## Best practices
- Run at least 5 hook variants per topic before concluding which formula works for your niche — sample size below 5 is statistically meaningless
- Cliffhanger series ("Part 2 drops tomorrow") increase profile visit rate by 3-5x but only work if Part 2 publishes within 24 hours — do not start a series without the full script ready
- Duet/stitch content targeting creators with 50K-500K followers in your niche delivers better follow-back rate than targeting mega-creators
- Post your highest-effort content during your audience's peak activity window (check Analytics > Followers > Activity); the first 30 minutes of engagement velocity determines FYP distribution
- Watch-time optimization is more important than posting frequency; 3 videos at 70%+ completion outperform 7 videos at 40% completion
- Build a content bank of 10-14 videos before launching a new series format; consistency during algorithm testing phase is critical

## AI-agent gotchas
- Agents generate hooks that are grammatically correct but tonally flat — TikTok hooks need urgency and pattern interruption, which requires explicit prompting ("write this hook as if the viewer is about to scroll away")
- Series content drafted by agents often lacks a genuine cliffhanger — the "reveal" in Part 2 must be compelling enough to justify a follow; validate manually before posting Part 1
- Watch-time analysis requires actual data; agents asked to "predict" drop-off points without data will hallucinate statistics
- Trend adaptation scripts sound generic unless the trend's exact sound, text overlay style, and visual pattern are described in detail to the agent
- Do not ask an agent to select which hashtags to use — TikTok hashtag strategy is real-time and requires Creative Center access; use 3-5 niche hashtags chosen by a human

## References
- https://www.tiktok.com/creators/ (TikTok Creator Portal)
- https://buffer.com/library/tiktok-analytics/ (analytics guide)
- https://sproutsocial.com/insights/tiktok-marketing/ (marketing research)
- https://influencermarketinghub.com/tiktok-stats/ (benchmark stats)
- developers.tiktok.com/products/research-api (TikTok Research API docs)
