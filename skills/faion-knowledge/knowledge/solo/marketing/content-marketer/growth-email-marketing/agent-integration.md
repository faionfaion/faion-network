# Agent Integration — Email Marketing

## When to use
- Launching a new product and need to build an email list from scratch
- Setting up automated welcome and nurture sequences for an existing audience
- Converting social media followers to an owned channel (email)
- Running a promotional campaign (product launch, sale, cohort open)
- Re-engaging an inactive or cold subscriber list

## When NOT to use
- Audience is still undefined — list-building without ICP clarity creates churn, not subscribers
- You have fewer than 50 subscribers and no consistent content cadence — focus on content first
- Your product is pure B2B enterprise with procurement-driven sales — email alone won't close
- Compliance requirements prevent automated outreach (certain financial or healthcare contexts)

## Where it fails / limitations
- Deliverability degrades fast if you send to a cold or purchased list — ISP blacklisting is hard to reverse
- Open rate metrics are unreliable since iOS Mail Privacy Protection inflates them; click-through rate is the real signal
- Automation complexity grows nonlinearly — advanced segmentation requires dedicated ops time to maintain
- Without a lead magnet, organic list growth is near-zero on most platforms
- Personalization at scale requires clean CRM/product data; bad data produces broken merge tags in production

## Agentic workflow
An agent can draft full email sequences (welcome, nurture, re-engagement) given a brief with ICP, product description, and tone guidelines. Claude Sonnet handles email copywriting efficiently; Opus is appropriate for designing the full segmentation strategy or a multi-touch launch sequence. Agents should not send emails autonomously — every batch should pass a human review checkpoint before delivery. Behavioral trigger logic (e.g., "send only if user has not logged in for 7 days") must be configured inside the ESP, not hallucinated by the agent.

### Recommended subagents
- `faion-sdd-executor-agent` — for systematic planning and implementing the welcome sequence as a tracked SDD task
- General Claude Sonnet subagent — for drafting individual email copy given subject + goal + tone constraints

### Prompt pattern
```
Write a 5-email welcome sequence for [Product].
ICP: [description]. Goal: drive first action — [action].
Tone: [conversational/professional]. Each email: subject line, preview text, body (≤150 words), one CTA.
```

```
Segment: inactive subscribers (no opens in 90 days).
Write a 3-email re-engagement sequence. If no click by email 3, end with unsubscribe offer.
Brand: [X]. Current offer: [Y].
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mailpit` | Local SMTP capture for testing sequences | `brew install mailpit` / github.com/axllent/mailpit |
| `litmus-cli` (unofficial) | Email client preview via API | docs.litmus.com/developer |
| `mjml` | Responsive email template compiler | `npm install -g mjml` / mjml.io |
| `curl` | Direct ESP API calls (ConvertKit, Mailchimp, Beehiiv REST) | Standard |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ConvertKit / Kit | SaaS | Yes — REST API | Tag-based segmentation, automations, broadcast API |
| Beehiiv | SaaS | Yes — REST API | Built for newsletter growth; referral native; good deliverability |
| Mailchimp | SaaS | Yes — REST API | Broad feature set; API well-documented; expensive at scale |
| ActiveCampaign | SaaS | Yes — REST API | Best-in-class behavioral automation; steeper learning curve |
| Customer.io | SaaS | Yes — REST API | Ideal for behavioral/trigger email for SaaS products |
| Postmark | SaaS | Yes — REST API | Transactional email with high deliverability; not for marketing broadcasts |
| Resend | SaaS | Yes — REST API | Developer-first transactional; MJML support; cheap at low volume |
| Mail-Tester | SaaS | Partial | Paste-test deliverability score; no automation API |
| Listmonk | OSS | Yes — REST API | Self-hosted; Postgres-backed; good for privacy-first setups |

## Templates & scripts
See `templates.md` for the full welcome sequence and newsletter templates.

Inline — minimal Python script to send a broadcast via ConvertKit API:
```python
import requests

CONVERTKIT_API_SECRET = "your_secret"
BROADCAST_URL = "https://api.convertkit.com/v3/broadcasts"

payload = {
    "api_secret": CONVERTKIT_API_SECRET,
    "subject": "Your subject line",
    "content": "<p>Your HTML content</p>",
    "email_address": "from@yourdomain.com",
    "thumbnail_alt": "",
}

response = requests.post(BROADCAST_URL, json=payload)
print(response.status_code, response.json())
```

## Best practices
- Write subject lines last — after the body is finalized, you'll know what actually matters
- Send from a personal name (`Alex from Acme`) rather than a brand name — higher open rates across all platforms
- Include a reply-to that actually works; agent-collected replies are signal for segmentation
- Plain-text emails outperform HTML for personal-tone sequences; use HTML only for designed newsletters
- Set up SPF, DKIM, DMARC on your sending domain before first broadcast — fix deliverability before you need it
- Re-engage or remove subscribers inactive for 180+ days before they hurt your sender reputation
- Never purchase or rent lists; spam complaints above 0.1% trigger Google/Yahoo bulk sender sanctions (2024+ rules)

## AI-agent gotchas
- Agents can draft copy but must not determine send timing autonomously — ESP scheduling is a human checkpoint
- Merge tag validation (`{{first_name}}` vs `{first_name}` varies by ESP) — always specify the ESP format in the prompt
- Segmentation logic produced by agents must be verified in the ESP UI before automation activation; wrong conditions silently fire to the wrong segment
- Agents tend to write longer emails than needed — specify a word count constraint in every prompt
- Subject lines with excessive punctuation or spam trigger words (FREE!!!, 100% guaranteed) produced by LLMs will tank deliverability; always run through a subject line checker before scheduling
- A/B test copy variants should be staged in the ESP, not run simultaneously by multiple agent calls

## References
- https://convertkit.com/resources
- https://www.mailchimp.com/resources/email-marketing-benchmarks/
- https://www.litmus.com/blog/
- https://postmarkapp.com/guides
- https://reallygoodemails.com/
