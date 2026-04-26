# Agent Integration — Webinar Delivery & Follow-up

## When to use
- Generating follow-up email sequences after a completed webinar
- Drafting Q&A answer briefs for anticipated attendee questions before the live event
- Repurposing a recorded webinar into blog posts, social clips, and newsletter editions
- Scoring attendee engagement to prioritize sales follow-up (high/mid/low intent buckets)
- Writing replay landing page copy with embedded conversion CTA

## When NOT to use
- Real-time delivery itself — agent cannot moderate live chat or respond to attendees in real time
- Audio/video production decisions (codec, bitrate, platform encoding settings)
- Setting up the webinar platform technically (Zoom/Demio account configuration)
- Defining the webinar topic or audience — that belongs in webinar-planning

## Where it fails / limitations
- Agents cannot transcribe audio directly; they require a transcript or captions file as input
- Follow-up sequence personalization is limited to name/segment tokens — behavioral personalization (attended vs. watched replay) requires ESP segmentation logic
- Repurposed content quality depends on transcript fidelity; auto-captions from Zoom/OBS are noisy and need cleaning first
- Conversion attribution from follow-up emails requires UTM tracking set up before the webinar, not after
- Show-up rate prediction is unreliable without historical benchmark data from prior webinars

## Agentic workflow
After the webinar recording is available, an agent pipeline can process the transcript to extract key quotes, generate timestamped chapter markers, draft the 5-email follow-up sequence, and produce repurposed formats (blog post, LinkedIn article, 10 tweet-length takeaways). The pipeline should run sequentially: clean transcript → extract insights → draft assets → human review → schedule sends. Human approval is mandatory before any email sequence is queued or any content is published.

### Recommended subagents
- `faion-sdd-executor-agent` — execute structured content repurposing tasks from a task file
- No dedicated webinar agent exists; use a content/copywriting subagent role for email drafting

### Prompt pattern
```
You have a webinar transcript below. Extract:
1. Top 5 actionable insights (each under 50 words)
2. 3 memorable quotes suitable for social media
3. A 400-word blog post introduction based on the opening problem statement

Transcript:
<transcript>{{TRANSCRIPT}}</transcript>

Output as JSON: {"insights": [...], "quotes": [...], "blog_intro": "..."}
```

```
Write a 5-email post-webinar follow-up sequence for [product].
Webinar topic: [TOPIC]. Offer: [OFFER]. Deadline: [DEADLINE].
Sequence: Day 0 replay+CTA, Day 1 takeaways+resources, Day 2 case study,
Day 3 FAQ+deadline, Day 5 extension (if applicable).
Tone: direct, value-first. Each email under 200 words.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `descript` | Transcription + clip extraction (desktop app, no CLI) | descript.com |
| `yt-dlp` | Download recorded webinar from YouTube/Zoom share link | `pip install yt-dlp` / github.com/yt-dlp/yt-dlp |
| `ffmpeg` | Extract audio-only version from recorded video | `brew install ffmpeg` / ffmpeg.org |
| `whisper` (OpenAI) | Local transcription of audio file | `pip install openai-whisper` / github.com/openai/whisper |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Descript | SaaS | Partial — no public API | Best transcript+clip workflow; manual trigger |
| Otter.ai | SaaS | Partial — export only | REST API for transcript export; no editing |
| Riverside.fm | SaaS | Partial | API access on Enterprise plan only |
| Demio | SaaS | Yes — REST API | Webinar platform with attendee export API |
| Livestorm | SaaS | Yes — REST API | Attendee data, registration, replay access |
| ConvertKit | SaaS | Yes — REST API | ESP for follow-up sequences; tag-based segmentation |
| ActiveCampaign | SaaS | Yes — REST API | More complex automations; webhooks for triggers |
| Opus Clip | SaaS | No public API | AI clip extraction; manual workflow only |

## Templates & scripts
See `templates.md` for full post-webinar email sequence (5 emails).

Minimal shell pipeline to extract audio and transcribe locally:

```bash
#!/bin/bash
# Usage: ./transcribe-webinar.sh recording.mp4
INPUT="$1"
AUDIO="${INPUT%.mp4}.wav"

ffmpeg -i "$INPUT" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$AUDIO"
whisper "$AUDIO" --language en --model medium --output_format txt
echo "Transcript saved to ${AUDIO%.wav}.txt"
```

## Best practices
- Clean the transcript before feeding it to any agent: remove filler words, fix speaker labels, fix proper nouns
- Segment your follow-up list by attendance status (live vs. replay vs. no-show) before the sequence runs; each segment needs a different day-0 email
- Include a hard deadline in the follow-up offer — "until Friday" outperforms "limited time"
- Pin the replay link to all follow-up emails, not just email 1; many people only open email 3 or 4
- Create one 60-90 second highlight clip for social distribution within 24 hours of the event
- Track replay completion rate as a lead scoring signal — viewers who watch >70% are higher-intent than registrants who never watched

## AI-agent gotchas
- Transcript timestamps from Zoom auto-captions drift; always verify chapter markers manually before publishing
- Agents tend to write follow-up emails that are too long — constrain to under 200 words per email explicitly
- Q&A answer generation requires the agent to know the product deeply; provide a product brief or README as context, not just the webinar transcript
- Never let an agent send follow-up emails directly — always route through a human approval step and ESP preview
- Case study emails generated by agents need real customer data injected; placeholder "[Customer Name]" text shipped to production is a common failure mode

## References
- https://demio.com/blog/webinar-follow-up-emails/
- https://www.on24.com/resources/webinar-benchmarks/
- https://riverside.fm/blog/webinar-recording
- Descript repurposing workflow: descript.com/blog/repurpose-webinar
