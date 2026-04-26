# Agent Integration — Webinar Planning & Promotion

## When to use
- Generating registration page copy and email promotion sequences for a planned webinar
- Creating a full slide deck outline from a topic brief and defined audience
- Drafting a multi-channel promotion timeline (email, social, partners) for a specific event date
- Selecting the best webinar format (educational/demo/panel/workshop) for a given marketing objective
- Writing speaker/co-host outreach emails for panel or interview-style webinars

## When NOT to use
- Picking the webinar topic — topic validation requires ICP interviews, not agent synthesis
- Technical platform setup (Zoom/Demio/Livestorm account configuration, recording settings)
- Real-time webinar moderation or chat management
- Estimating expected registrations without historical benchmark data from prior webinars
- When the product has no established audience to promote to (webinar will draw zero attendees)

## Where it fails / limitations
- Registration page conversion rates depend on the existing email list size and audience trust; agents cannot compensate for a cold audience
- Promotion timeline assumes multi-channel access (email list, social following, partners); solo founders with small lists need adjusted cadence
- Partner outreach effectiveness depends on relationship history, not the quality of the outreach email
- Slide deck outlines are structurally correct but will contain placeholder content that requires product/domain expertise to fill
- Webinar metrics (registration rate, show-up rate) vary enormously by niche and offer — benchmarks in README.md are directional only

## Agentic workflow
A Claude subagent is most effective here as a campaign planner and copywriter. Provide the topic, target audience, date/time, platform choice, and whether there is an existing email list. The agent produces: registration page copy, a 3-email promotion sequence for existing subscribers, 5-7 social posts for each channel, a slide outline with presenter notes scaffold, and a partner outreach email template. All outputs are drafts for human review before any scheduling or sending.

### Recommended subagents
- No dedicated webinar agent exists in the current agents/ directory
- Use a content/copywriting subagent role: registration copy, email sequences, social posts
- Use a planning subagent role: promotion timeline, slide outline, checklist generation

### Prompt pattern
```
You are planning a webinar promotion campaign.
Inputs:
- Topic: [TOPIC]
- Target audience: [ICP]
- Date/time: [DATE TIME TIMEZONE]
- Email list size: [N] subscribers
- Platform: [ZOOM/DEMIO/LIVESTORM]
- Goal: [lead gen / product demo / community]

Produce:
1. Registration page copy (headline, 4 benefit bullets, host bio 2 sentences, CTA)
2. 3-email promotion sequence (subject + 150-word body each, send on days -14, -7, -1)
3. 3 social post variants (Twitter/X format, under 280 chars each)

Output as JSON: {"registration_page": {...}, "emails": [...], "social_posts": [...]}
```

```
Create a 20-slide outline for a [FORMAT] webinar on [TOPIC] for [AUDIENCE].
Duration: 60 minutes (45 content + 15 Q&A).
For each slide: slide number, title, content type (text/visual/demo/poll),
presenter note (1 sentence on what to say).
Include: poll at slide 4, soft pitch at slide 16, Q&A placeholder at slide 17.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `calendly` API | Schedule guest/speaker availability for panel webinars | developer.calendly.com |
| `zoom` API | Create webinar, manage registrants, pull attendee list | marketplace.zoom.us/docs/api-reference |
| `demio` API | Create events, registration, attendee export | dev.demio.com |
| `livestorm` API | Full webinar lifecycle management | developers.livestorm.co |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Demio | SaaS | Yes — REST API | Best API surface for registration/attendee management |
| Livestorm | SaaS | Yes — REST API | Strong API; built-in email sequences |
| Zoom Webinars | SaaS | Yes — REST API | Requires Webinar add-on; most commonly used |
| WebinarJam | SaaS | Partial — webhook only | Limited API; mainly push notifications |
| ConvertKit | SaaS | Yes — REST API | Registration landing page + email sequences |
| Mailchimp | SaaS | Yes — REST API | Promotion email sequences; audience segmentation |
| Eventbrite | SaaS | Yes — REST API | Registration + discovery; works for free webinars |
| Canva | SaaS | Partial — API (limited) | Slide template generation; limited programmatic control |

## Templates & scripts
See `templates.md` for registration page copy, slide deck outline template, and promotion email sequences.

Minimal Python script to create a Zoom webinar via API:

```python
import requests, os

ZOOM_TOKEN = os.environ["ZOOM_JWT_TOKEN"]

response = requests.post(
    "https://api.zoom.us/v2/users/me/webinars",
    headers={"Authorization": f"Bearer {ZOOM_TOKEN}", "Content-Type": "application/json"},
    json={
        "topic": "Your Webinar Title",
        "type": 5,  # 5 = Webinar
        "start_time": "2026-05-15T14:00:00Z",
        "duration": 60,
        "timezone": "America/New_York",
        "settings": {
            "registrants_email_notification": True,
            "practice_session": True,
        }
    }
)
data = response.json()
print(f"Webinar ID: {data['id']}")
print(f"Registration URL: {data['registration_url']}")
```

## Best practices
- Lock the topic, date, and platform before asking an agent for copy — changing any of these after drafting requires full regeneration
- Always prompt the agent to write the registration page headline as a problem statement, not a feature statement ("Stop losing deals in demos" not "Join our product webinar")
- Partner outreach emails should be highly personalized; agent drafts need audience overlap data inserted manually before sending
- Build the follow-up (webinar-delivery) email sequence at the same time as the promotion sequence — they are one campaign
- For first-time webinars with no historical data, use 500 registrations as a rough planning target and work backward to channel requirements
- Set up UTM parameters on all registration links before the promotion starts, not after

## AI-agent gotchas
- Agents default to generic benefit copy ("Learn proven strategies"); push back with "write benefits as specific outcomes with a number" to get higher-converting copy
- Slide outlines from agents tend to pack too much content per slide; add explicit constraint "max 3 bullets per slide, no full sentences"
- Email promotion sequences often read like newsletters, not event invitations; specify urgency and countdown framing explicitly
- Agent-generated partner outreach emails are too formal and templated — recipients can tell; require personalization tokens with actual notes about the partner's audience
- Do not delegate the "why attend" value proposition to an agent without first providing customer pain quotes or interview data

## References
- https://blog.hubspot.com/marketing/webinar-marketing
- https://www.on24.com/resources/webinar-benchmarks/ (industry benchmarks)
- https://developers.livestorm.co/ (Livestorm API)
- https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#tag/Webinars (Zoom API)
