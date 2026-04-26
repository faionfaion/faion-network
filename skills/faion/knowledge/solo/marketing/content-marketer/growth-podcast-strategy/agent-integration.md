# Agent Integration — Podcast Strategy

## When to use
- Drafting personalized podcast pitch emails for guest appearance outreach at scale
- Generating episode question sets from a guest's bio, past interviews, and the show's topic focus
- Writing episode show notes, chapter markers, and SEO-optimized descriptions after recording
- Creating a media kit document (bio, topic angles, previous appearances) for guest outreach campaigns
- Researching target podcasts (topic fit, audience size, booking frequency) from a niche keyword list

## When NOT to use
- Recording, editing, or audio post-production — requires human operation of audio software
- Live interview facilitation — conversational quality depends on human listening and improvisation
- Deciding whether to host vs. guest-first — this is a strategic call requiring knowledge of current audience size and resources
- Pitching to podcasts with 1M+ listeners as a first step — those require established credentials and relationships

## Where it fails / limitations
- Podcast pitch personalization requires reading the specific podcast; agents need the show description and recent episode titles as input, not just the podcast name
- Episode question quality depends on how much research context the agent has about the guest; surface-level bios produce generic questions
- Show note quality degrades significantly without a transcript or detailed summary; agents hallucinate specific quotes without source material
- Podcast discovery databases (Listen Notes, Podmatch) are not fully accessible via free APIs; research tasks have data access limits
- Guest booking rate depends entirely on the host's judgment of the guest's audience value — copy quality is secondary

## Agentic workflow
Two distinct agent pipelines are useful here. For guest outreach: feed the agent a list of 20 target podcasts (name, niche, episode count, estimated audience size) plus the guest's bio and 3 topic angles; the agent produces 20 personalized pitch emails for human review and send. For hosting: after each recording, feed the agent the transcript and episode metadata; the agent produces show notes, chapter timestamps, 5-tweet thread summary, and newsletter blurb. Both pipelines require human review before any external communication or publishing.

### Recommended subagents
- No dedicated podcast agent exists in the current agents/ directory
- Use a research subagent role: podcast database lookup, audience analysis, pitch personalization research
- Use a content subagent role: show notes, chapter markers, repurposed assets from transcript

### Prompt pattern
```
Write a personalized podcast pitch email for [GUEST/PRODUCT].
Target show: [SHOW NAME]
Show description: [SHOW DESCRIPTION]
Recent episodes: [EPISODE 1 TITLE], [EPISODE 2 TITLE], [EPISODE 3 TITLE]
Guest credentials: [2-3 sentence bio]
Proposed topic angle: [SPECIFIC ANGLE]

Requirements:
- Reference one specific recent episode by name
- Lead with audience value, not the guest's credentials
- Propose 3 specific bullet points the episode will cover
- Under 200 words total
- No "I'm a huge fan" opener
```

```
Generate 10 interview questions for a podcast episode on [TOPIC].
Guest: [NAME], [ROLE], [COMPANY]
Known for: [KEY INSIGHT OR ACCOMPLISHMENT]
Show tone: [CONVERSATIONAL/TECHNICAL/STORYTELLING]
Avoid: generic "what's your background" opener, "what advice would you give" closer.
Include: one contrarian follow-up question per section.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `listennotes-api` | Search podcast database, get episode data | `pip install listennotes` / listennotes.com/api |
| `podchaser-api` | Podcast and episode metadata, guest history | podchaser.com/api |
| `whisper` | Transcribe recorded episodes locally | `pip install openai-whisper` / github.com/openai/whisper |
| `ffmpeg` | Extract audio from video recording, trim silence | `brew install ffmpeg` / ffmpeg.org |
| `transistor-api` | Publish episodes, manage RSS feed | developers.transistor.fm |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Listen Notes | SaaS | Yes — REST API | Best podcast search API; free tier has 10 req/day |
| Podmatch | SaaS | No API | Guest-host matching; manual workflow |
| MatchMaker.fm | SaaS | No API | Similar to Podmatch; profile-based matching |
| Transistor | SaaS | Yes — REST API | Hosting + RSS + analytics; full CRUD API |
| Buzzsprout | SaaS | Yes — REST API | Hosting + distribution; slightly simpler than Transistor |
| Riverside.fm | SaaS | Partial — Enterprise API | Best remote recording quality; no public API for free/pro |
| Descript | SaaS | No public API | Transcript + editing; manual workflow |
| Calendly | SaaS | Yes — REST API | Guest scheduling automation |
| Opus Clip | SaaS | No public API | AI clip extraction for social; manual trigger |

## Templates & scripts
See `templates.md` for episode outline, podcast intro script, and guest pitch template.

Minimal Listen Notes API call to find relevant podcasts by keyword:

```python
import requests, os

API_KEY = os.environ["LISTENNOTES_API_KEY"]

response = requests.get(
    "https://listen-api.listennotes.com/api/v2/search",
    headers={"X-ListenAPI-Key": API_KEY},
    params={
        "q": "SaaS founders indie hacker",
        "type": "podcast",
        "language": "English",
        "sort_by_date": 0,
        "len_min": 20,
    }
)
results = response.json()["results"]
for pod in results[:10]:
    print(f"{pod['title_original']} | {pod['total_episodes']} eps | {pod['listen_score']} score")
```

## Best practices
- Send podcast pitches from a real email address the founder or host actively monitors — pitch replies need same-day response to maintain momentum
- Personalization means referencing a specific episode; "I love your show" without a named episode signals the email was templated
- Prepare 3 distinct topic angles per guest appearance, not one — hosts often prefer a different angle than the one you lead with
- Record the first 3 episodes before publishing anything; consistency in the first 30 days matters more than launch perfection
- Show notes should target a keyword the episode topic naturally ranks for — treat them as a blog post with an embedded audio player
- For guest strategy, track booking rate per outreach batch; below 20% means the pitch angle or target list needs revision

## AI-agent gotchas
- Podcast pitches generated without reading the actual show will contain generic phrases that signal templating — always provide show-specific context
- Episode questions from agents trend toward chronological biography ("Tell me about your journey"); explicitly prompt for insight-first, story-second structure
- Show notes generated from a transcript will over-summarize; they need editing to retain the guest's voice and quotable moments
- Agents cannot estimate a podcast's actual audience quality or conversion potential — download count is a proxy, not a guarantee
- Podcast scheduling logistics (calendar, Riverside link, reminder emails) should be automated via Calendly + webhook, not an LLM agent

## References
- https://www.listennotes.com/ (podcast database and API)
- https://podmatch.com/ (guest-host matching)
- https://transistor.fm/how-to-start-a-podcast/ (hosting setup guide)
- https://riverside.fm/blog (remote recording best practices)
- Podchaser API: podchaser.com/api
