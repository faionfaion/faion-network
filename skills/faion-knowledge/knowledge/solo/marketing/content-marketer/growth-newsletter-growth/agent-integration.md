# Agent Integration — Newsletter Growth

## When to use
- Starting a newsletter from zero and needing a systematic subscriber acquisition plan
- Stuck below 1,000 subscribers with inconsistent growth and no referral engine
- Ready to invest in paid subscriber acquisition after proving organic unit economics
- Planning a cross-promotion or SparkLoop swap partnership
- Redesigning signup forms and lead magnet to improve opt-in conversion rate

## When NOT to use
- No consistent publishing cadence exists yet — growth tactics without content quality create churn
- Newsletter topic has no defined ICP or value proposition — positioning must precede growth
- Audience is purely B2B enterprise where email capture via newsletter is not the primary sales motion
- You are in a heavily regulated vertical where lead magnet distribution has compliance requirements

## Where it fails / limitations
- Referral programs only work after reaching ~500+ engaged subscribers; below that, the referral loop has insufficient fuel
- SparkLoop and cross-promotions require a minimum engagement rate (typically 40%+ open rate) to be accepted as a partner
- Paid acquisition (Meta, Twitter Ads) for newsletters requires significant testing budget before finding a profitable CPL — not viable under $500 test budget
- Lead magnet fatigue is real: the same freebie loses conversion power over 12-18 months
- Subscriber count growth is a vanity metric without tracking open rate and click rate concurrently

## Agentic workflow
Claude agents are well-suited to drafting positioning copy (newsletter tagline, lead magnet concepts, form headline variants), writing welcome email sequences, and generating content calendar structures. Sonnet handles copy tasks; Opus handles strategy design (referral reward tiers, growth channel prioritization). Agents cannot interact with SparkLoop's partner marketplace, ConvertKit automations, or ad platforms — those require human-in-the-loop for setup and budget decisions. All growth experiments should be proposed by the agent, reviewed, then implemented manually.

### Recommended subagents
- `faion-sdd-executor-agent` — for tracking newsletter growth as a structured SDD initiative with checklist milestones
- General Claude Sonnet subagent — for drafting lead magnet concepts, form headline variants, and welcome email copy

### Prompt pattern
```
Create 5 lead magnet concepts for a newsletter targeting [ICP].
Newsletter topic: [X]. Format per concept: title, format (PDF/checklist/tool),
one-sentence value prop, estimated conversion potential (High/Med/Low).
```

```
Write 3 variants of a signup form headline for a newsletter about [topic].
Target: [ICP]. Current headline: [X]. Goal: increase opt-in rate.
Include headline, subheadline, button text per variant.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` | ConvertKit / Beehiiv / Substack API calls | Standard |
| `plausible-cli` (custom) | Pull signup source breakdown via Plausible API | See plausible-analytics methodology |
| `mailpit` | Local email preview for welcome sequence testing | github.com/axllent/mailpit |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Beehiiv | SaaS | Yes — REST API | Best native referral + monetization; growth-focused |
| ConvertKit / Kit | SaaS | Yes — REST API | Strong automation; integrates with SparkLoop |
| Substack | SaaS | Partial — limited API | Built-in discovery network; poor for external automation |
| SparkLoop | SaaS | Partial — partner setup manual | Referral program and newsletter swaps marketplace |
| Viral Loops | SaaS | Yes — API | Generic referral platform; works with any ESP |
| The Sample | SaaS | No API | Newsletter discovery / cross-promotion network |
| OptinMonster | SaaS | Partial | Popup/form builder; A/B testing; integrates with most ESPs |
| Plausible | SaaS/OSS | Yes — REST API | Track signup source, conversion by page |

## Templates & scripts
See `templates.md` for the welcome email template and newsletter issue template.

Minimal Python script to pull subscriber growth from Beehiiv API:
```python
import requests

BEEHIIV_API_KEY = "your_key"
PUB_ID = "pub_xxxxxxxx"

url = f"https://api.beehiiv.com/v2/publications/{PUB_ID}/subscriptions"
headers = {"Authorization": f"Bearer {BEEHIIV_API_KEY}"}
params = {"limit": 1, "status": "active"}

resp = requests.get(url, headers=headers, params=params)
data = resp.json()
print(f"Total active subscribers: {data.get('total_results', 'N/A')}")
```

## Best practices
- Define the newsletter in one sentence using the positioning formula before writing any copy: "[Name] is a [frequency] newsletter for [ICP] that helps them [outcome] through [format]"
- Lead magnet must solve a specific, immediate problem — broad guides convert worse than narrow checklists
- Every piece of content published should include a CTA to the newsletter; treat it as the primary conversion goal of all content marketing
- Above-the-fold signup form on the homepage is the highest-leverage placement; A/B test headline and button text before adding more forms
- Referral reward tiers should be achievable at 1, 3, and 10 referrals — make the first reward attainable in the first week
- Cross-promotion quality control: only swap with newsletters that have similar audience ICP and engagement rate ≥ 35%
- Unsubscribe rate above 0.3% per issue is a content quality signal, not a list quality problem — investigate content before acquisition

## AI-agent gotchas
- Agents will generate positioning copy that sounds plausible but may not match actual audience language — validate against real subscriber language (survey replies, review mining)
- Lead magnet titles generated by agents tend toward generic ("The Ultimate Guide") — specify the format constraint: "[Outcome] in [timeframe] [for ICP]"
- Growth channel recommendations from agents may not account for platform-specific audience fit — cross-promotion sources must be verified manually
- Agents cannot monitor referral program performance or trigger payout workflows — these require human review of SparkLoop/Viral Loops dashboards
- Segment logic for inactive re-engagement must be set up inside the ESP; agent-produced pseudocode is a starting point, not deployable config

## References
- https://sparkloop.app/blog
- https://www.beehiiv.com/blog
- https://on.substack.com/s/resources
- https://convertkit.com/resources/newsletter-growth
- https://thesample.ai/
