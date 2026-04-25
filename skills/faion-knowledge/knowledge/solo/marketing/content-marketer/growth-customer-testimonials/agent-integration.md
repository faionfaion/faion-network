# Agent Integration — Customer Testimonials & Social Proof

## When to use
- Landing page conversion rate is below benchmark and social proof is absent or weak
- Launching a new product and need to systematically build the first testimonial bank
- Preparing a case study library to support a sales or marketing campaign
- Redesigning an existing landing page where testimonials are generic or buried
- Setting up a post-purchase automation to collect testimonials at scale

## When NOT to use
- No existing customers yet — fabricated or placeholder testimonials are worse than none
- Product is under NDA or in a regulated industry where customer quotes require legal review before publication
- Customer relationships are too early (first 2 weeks post-purchase) to ask for testimonials without damaging trust
- B2B enterprise sales where case studies require formal approval chains spanning months — use a lighter proof format (logo wall + usage stats) instead

## Where it fails / limitations
- Asking too broadly ("How do you like the product?") produces vague quotes that are unusable
- Video testimonial collection requires production logistics that agents cannot manage
- Testimonial approval workflows (customer review of edited quotes) add unpredictable latency
- Fake or heavily fabricated testimonials are reputationally catastrophic if exposed; all quotes must be authentic
- Display effectiveness depends on page design and placement — an agent can recommend placements but cannot implement or A/B test them

## Agentic workflow
Claude agents are well-suited for: drafting testimonial request email sequences, generating follow-up questions for specifics, transforming weak quotes into stronger versions (with human review for accuracy), writing case study templates, and identifying optimal testimonial placements per page type. Haiku handles mechanical tasks (formatting testimonial cards, extracting quotes from interview transcripts); Sonnet handles email drafting and quote transformation; Opus for designing the full social proof strategy across the buyer journey. No testimonial content should be published without explicit customer approval — this is always a human checkpoint.

### Recommended subagents
- `faion-sdd-executor-agent` — for managing the testimonial collection program as a tracked initiative
- General Claude Sonnet subagent — for drafting request emails, follow-up prompts, and case study outlines
- General Claude Haiku subagent — for formatting quote cards, extracting key phrases from interview transcripts

### Prompt pattern
```
Transform the following weak testimonial quote into a stronger version.
Rules: preserve the customer's voice, do not invent specific numbers,
use the original meaning, add specificity where implied.
Submit the transformed version for customer approval before use.

Original: "[paste weak quote]"
Customer name: [X]. Role: [Y]. Company: [Z].
```

```
Write a 3-email testimonial request sequence for customers who just
achieved [milestone] with [Product].
Email 1: ask. Email 2: follow-up (Day 5). Email 3: final ask (Day 10).
Include specific guiding questions to get result-oriented quotes.
Tone: personal, not corporate.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` | Testimonial.to API, Senja API, G2 API calls | Standard |
| `loom-cli` (unofficial) | Manage Loom recording links | Loom API docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Testimonial.to | SaaS | Yes — REST API | Dedicated collection platform; text + video; widget embed |
| Senja | SaaS | Yes — REST API | Collection + display; Notion-like management; good free tier |
| Trustpilot | SaaS | Partial — API | Public review platform; G2 is better for B2B SaaS |
| G2 | SaaS | Partial — API | B2B SaaS reviews; high trust with buyers |
| Capterra | SaaS | Partial | SMB software reviews; broad reach |
| Delighted | SaaS | Yes — REST API | NPS + CSAT survey; can trigger testimonial ask on high scores |
| Customer.io | SaaS | Yes — REST API | Automate testimonial request emails triggered by product events |
| Proof | SaaS | Partial | Social proof notification popups ("X just signed up") |
| Fomo | SaaS | Partial | Similar to Proof; real-time social proof display |

## Templates & scripts
See `templates.md` for the testimonial request email sequence and case study template.

Minimal Python script to fetch testimonials from Senja API:
```python
import requests

SENJA_API_KEY = "your_api_key"
WALL_ID = "your_wall_id"

url = f"https://app.senja.io/api/testimonials"
headers = {
    "Authorization": f"Bearer {SENJA_API_KEY}",
    "Content-Type": "application/json",
}
params = {"wallId": WALL_ID, "status": "published"}

resp = requests.get(url, headers=headers, params=params)
testimonials = resp.json().get("data", [])

for t in testimonials[:5]:
    name = t.get("name", "Anonymous")
    quote = t.get("content", "")[:100]
    print(f"{name}: {quote}...")
```

## Best practices
- Ask for testimonials at the moment of peak satisfaction — immediately after a measurable win (first result, milestone reached, renewal) not at a random interval
- Guide the customer with specific questions rather than open-ended requests: "What result did you achieve?" produces better copy than "How do you like it?"
- Follow up twice (Day 5, Day 10) after the initial request — response rate increases from ~15% to ~35% with two follow-ups
- Always get written approval on any edited or transformed quote before publishing; track approval status in a CRM field
- Match testimonial format to the buying stage: logo walls and user counts for awareness; detailed quotes with photos for consideration; video testimonials for decision
- Prioritize testimonials from customers who match the ICP of your target buyer — a testimonial from a 5-person startup will not resonate with enterprise buyers
- Refresh testimonials annually — stale testimonials (dated language, old logos, no longer relevant roles) signal an inactive customer base

## AI-agent gotchas
- Agents must never invent specific numbers in transformed quotes — if a customer says "it saved time," the agent cannot substitute "saved 10 hours/week" without customer confirmation
- Testimonial request emails drafted by agents tend to sound too corporate; request explicitly "write as a personal email from the founder, not a company template"
- Customer approval workflow cannot be automated — always flag this as a manual step in any agent-produced collection plan
- Placement recommendations from agents (e.g., "add testimonial near the CTA") are starting points; A/B testing on the actual page is required to validate impact
- Case studies drafted by agents will require factual review against the actual customer data — treat all agent-produced case study drafts as structured templates, not finished content

## References
- https://testimonial.to/blog
- https://senja.io/blog
- https://cxl.com/blog/social-proof/
- https://www.nielsen.com/insights/
- https://www.brightlocal.com/research/
