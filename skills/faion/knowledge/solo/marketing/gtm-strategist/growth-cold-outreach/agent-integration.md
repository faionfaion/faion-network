# Agent Integration — Cold Outreach

## When to use
- Zero inbound pipeline; need customers this week, not in 3 months
- Launching a B2B SaaS or consulting service targeting a specific role/company type
- Testing product-market fit with a specific niche via direct conversation (not ads)
- Researching prospect pain points before building features — outreach doubles as customer discovery
- Follow-up sequence needs to be built for an existing prospect list

## When NOT to use
- B2C consumer products with low ARPU — CAC via cold outreach will exceed LTV in most consumer segments
- No defined ICP (Ideal Customer Profile) — mass outreach without targeting destroys deliverability and reputation
- Product is not functional — cold outreach that lands a meeting you can't fulfill with a real product causes permanent reputation damage
- High-trust regulated sectors (healthcare, legal, financial) where unsolicited outreach raises compliance concerns without a proper opt-in

## Where it fails / limitations
- Domain warmup takes 2-4 weeks; agents cannot accelerate this; launching at scale before warmup guarantees spam folder
- Email personalization at scale is a sliding scale: deeper personalization means fewer emails per hour a human or agent can process
- Apollo, Hunter, and Clay all have rate limits and require API keys; bulk prospect building cannot be fully automated in a single session
- Reply rates are highly sensitive to offer framing, timing, and market conditions — agent copy variants must be A/B tested with real sends
- GDPR/CAN-SPAM compliance: agents must be instructed to include unsubscribe links and comply with data handling rules; hallucinating compliance is a legal risk

## Agentic workflow
Cold outreach is one of the highest-leverage areas for agent automation: prospect research, email drafting, and follow-up sequencing are all text tasks agents excel at. A typical setup has an agent ingest a prospect CSV (name, company, title, LinkedIn URL, trigger signal), enrich each row with a personalization hook via web search or provided notes, draft the initial email and 4 follow-ups per prospect, and output a ready-to-import CSV for Instantly or Smartlead. Human review is required for a sample of 10-20% of drafts before launching the full sequence. The agent should not configure sending infrastructure, manage deliverability, or mark prospects as replied.

### Recommended subagents
- `faion-email-agent` (referenced in README) — email drafting, sequence generation, personalization
- A `prospect-enrichment-agent` could take a raw company list and add pain signal context by searching recent news, job postings, and LinkedIn posts

### Prompt pattern
```
You are a cold email copywriter for [Product/Service] targeting [Role] at [Company Type].
ICP: [detailed description]
Value proposition: [2-3 sentences]
Social proof: [result or customer name if available]

Prospect data:
- Name: [First Last]
- Company: [Company]
- Title: [Title]
- Trigger/hook: [Recent post, news, job posting signal]

Write a 5-email sequence:
Email 1 (Day 0): Full pitch — 4-5 sentences max, low-friction CTA.
Email 2 (Day 3): Value bump — add one new insight or case study.
Email 3 (Day 7): Different angle — reframe the problem.
Email 4 (Day 14): Case study — one concrete result, one sentence.
Email 5 (Day 21): Break-up — short, no pressure, leave door open.

Rules: No jargon. First-person. Subject lines max 6 words. No "I hope this finds you well."
Output: structured markdown with subject line + body per email.
```

```
Here is a CSV of 100 prospects with columns: name, company, title, trigger_signal.
For each prospect, write a 2-sentence personalized opening that references the trigger_signal.
Output: CSV with added column: personalized_opening.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Apollo CLI / API | Prospect search, email finding, sequence management | https://apolloio.github.io/apollo-api-docs/ |
| Hunter API | Email finding and verification by domain | https://hunter.io/api-documentation |
| NeverBounce API | Bulk email verification before sending | https://docs.neverbounce.com |
| ZeroBounce API | Email validation and deliverability scoring | https://www.zerobounce.net/docs/ |
| Instantly API | Sequence management, sending, analytics | https://developer.instantly.ai |
| Smartlead API | Campaign creation, inbox rotation, analytics | https://api.smartlead.ai |
| Clay API | Prospect enrichment with multiple data sources | https://clay.com/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apollo.io | SaaS | Yes — REST API | All-in-one prospecting + sending; generous free tier |
| Instantly | SaaS | Yes — REST API | Sending + warmup + analytics; agent can create campaigns |
| Smartlead | SaaS | Yes — REST API | Multi-inbox rotation; good for scale |
| Hunter.io | SaaS | Yes — REST API | Email finding; 25 free searches/month |
| Clay | SaaS | Yes — REST API | Enrichment waterfall (LinkedIn + news + AI) |
| Lemlist | SaaS | Yes — REST API | Personalized images in email; high visual engagement |
| Pipedrive | SaaS | Yes — REST API | CRM for tracking replied prospects and deals |
| Warmbox | SaaS | Yes — API | Domain warmup automation; pairs with Instantly |

## Templates & scripts
See templates.md for: cold email template, LinkedIn connection request, post-connection message.

Inline script — validate prospect CSV and flag missing personalization hooks before drafting:

```python
import csv, sys

REQUIRED_FIELDS = ["name", "company", "title", "email", "trigger_signal"]

def validate_prospect_csv(path: str) -> dict:
    rows = list(csv.DictReader(open(path)))
    errors = []
    missing_trigger = []
    for i, row in enumerate(rows, 1):
        for field in REQUIRED_FIELDS:
            if field not in row or not row[field].strip():
                errors.append(f"Row {i}: missing '{field}'")
        if not row.get("trigger_signal", "").strip():
            missing_trigger.append(row.get("name", f"Row {i}"))

    return {
        "total": len(rows),
        "errors": errors[:10],  # cap output
        "missing_trigger_pct": f"{100*len(missing_trigger)/len(rows):.0f}%",
        "ready_for_drafting": len(errors) == 0,
    }

print(validate_prospect_csv(sys.argv[1]))
```

## Best practices
- Never send cold email from your primary business domain — use a separate domain (e.g., `[yourname]-hq.com`) with proper SPF/DKIM/DMARC to protect deliverability of your main domain
- Start at 20 emails/day per inbox and ramp by 10/day each week; never jump to 50+/day on a new domain without 3+ weeks of warmup
- Write every email as if you're sending it to one person — mass-sounding copy gets low reply rates regardless of personalization tokens
- Trigger events (funding round, new hire, product launch, leadership change) multiply reply rates; invest in enrichment to find them per prospect
- Track positive reply rate (not just open rate) as the primary KPI — open rate is inflated by Apple Mail Privacy Protection and bot opens
- Build a "not interested" suppression list and honor it permanently; re-contacting opted-out prospects is CAN-SPAM/GDPR violation territory

## AI-agent gotchas
- Agents may generate emails that are too long for the format (> 5 sentences); enforce length limits explicitly in the system prompt
- Personalization hooks hallucinated from vague trigger_signal data (e.g., "recent activity") produce obviously fake opening lines that destroy credibility — require the agent to flag missing or ambiguous trigger data instead of inventing context
- GDPR compliance: agents must include unsubscribe mechanism language in every email draft; this is non-negotiable for EU prospects
- Subject line generation is highly task-specific; validate against real A/B data from your niche — what works for SaaS may fail for consulting
- Human-in-loop checkpoint: review 10-20% of drafted sequences before loading into sending tool; spot-check for tone, accuracy, and compliance
- Agents should not configure sending infrastructure (Instantly campaigns, inbox rotation, warmup settings) — these require understanding of current domain reputation state that agents cannot assess without live data

## References
- https://instantly.ai/blog/cold-email-guide — Cold email infrastructure, deliverability, and scaling
- https://apolloio.github.io/apollo-api-docs/ — Apollo API for prospecting and sending automation
- https://www.zerobounce.net/email-deliverability/ — Technical email deliverability setup guide
- https://reply.io/resources/ — Multi-channel outbound playbooks
- Predictable Revenue by Aaron Ross — outbound SDR methodology (Salesforce.com origin story) (book)
- https://developer.instantly.ai — Instantly API docs for campaign automation
