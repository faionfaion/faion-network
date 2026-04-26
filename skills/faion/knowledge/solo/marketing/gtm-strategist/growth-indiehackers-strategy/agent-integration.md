# Agent Integration — IndieHackers Strategy

## When to use
- Early-stage product (pre-revenue or < $1K MRR) needs a build-in-public audience
- Monthly update posts need to be drafted consistently without burning the founder on writing
- Specific feedback is needed from fellow solopreneurs (pricing, naming, positioning)
- Milestone just hit (first sale, $1K MRR, profitable month) and needs a structured post for leverage
- Planning a content calendar of IH posts for the next quarter

## When NOT to use
- Product targets enterprise buyers, CTOs, or procurement teams — IH audience is indie makers and solopreneurs, not enterprise decision-makers
- Expecting IH posts to drive significant B2B pipeline — it works for peer validation and early adopters, not sales velocity at scale
- No genuine product or business to share — IH community detects and ignores accounts that only post promotional content without a real journey
- The founder is not willing to share real metrics (even zeros) — transparency is the IH social contract; vague posts get ignored

## Where it fails / limitations
- IndieHackers has no public API for posting or analytics; all content must be posted manually via the web interface
- Community engagement is relationship-based; agent-generated content that lacks authentic voice will be recognized and receive poor engagement
- IH audience is global and niche-diverse; product-market fit signal from IH validation is relevant mainly for other solopreneurs as an audience, not broader markets
- Consistent posting requires 2-4 weeks of community participation before promotional content gains traction — agents cannot shortcut the reputation-building phase
- Monthly update posts require real metrics; agents must be given accurate data, not asked to invent plausible numbers

## Agentic workflow
An agent is most useful for drafting the structured content (monthly updates, milestone posts, feedback request posts) from raw inputs the founder provides: this month's metrics, what worked, what failed, what they learned. The agent formats this into the IH post templates, writes in a first-person conversational style, and generates specific community questions to embed. The founder reviews and adjusts for authentic voice before posting. Agents can also help plan a 90-day content calendar: which milestones to post about, which feedback to seek, which questions to pose to the community.

### Recommended subagents
- `faion-social-agent` (referenced in README) — post drafting, milestone post generation, monthly update formatting
- A `build-in-public-agent` could ingest a weekly metrics snapshot and draft a weekly update post for IH, Twitter/X, and LinkedIn simultaneously

### Prompt pattern
```
You are a ghostwriter for an indie maker on IndieHackers.
Voice: first-person, honest, direct, builder-focused. No hype. No corporate language.

Monthly metrics:
- MRR: $[X] ([+/-Y]% from last month)
- Active users: [N]
- Churn: [Z]%
- Key win: [description]
- Key failure: [description]
- Top learning: [description]
- Next month focus: [description]

Task: Write a monthly update post for IndieHackers using the standard template.
Include 1-2 specific questions for the community at the end.
Max length: 400 words.
Output: post-ready markdown.
```

```
We just hit [milestone] after [X] months.
Key milestones on the way: [list].
What worked: [list].
What didn't: [list].
What we'd do differently: [list].

Write a milestone post for IndieHackers:
- Headline following the formula: "I just hit [Milestone]! Here's what I learned"
- Journey narrative (100 words)
- What worked section (3 bullets with brief explanations)
- What I'd do differently section (2 bullets)
- End with open "Ask me anything!"
Output: post-ready markdown.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Typefully API | Schedule and cross-post IH content to Twitter/X | https://typefully.com/developers |
| Buffer API | Multi-platform scheduling including Twitter/X and LinkedIn | https://buffer.com/developers/api |
| Plausible API | Pull weekly traffic data to include in update posts | https://plausible.io/docs/stats-api |
| Stripe CLI | Get MRR and subscriber count for update posts | https://stripe.com/docs/stripe-cli |
| Baremetrics API | Pre-formatted SaaS metrics for update posts | https://developers.baremetrics.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| IndieHackers.com | SaaS | No public API — manual only | All posting via web; no automation possible |
| Typefully | SaaS | Yes — API | Repurpose IH posts to Twitter/X threads |
| Buffer | SaaS | Yes — API | Cross-post to Twitter/X and LinkedIn on same schedule |
| Stripe | SaaS | Yes — REST API | Revenue data for transparent update posts |
| Plausible | SaaS | Yes — REST API | Privacy-first analytics; pull traffic metrics for posts |
| CleanShot X | SaaS (Mac) | No — manual | Screenshot tool for product visuals in posts |

## Templates & scripts
See templates.md for: intro post, monthly update template, feedback request template, weekly update.

Inline script — generate a metrics summary from Stripe for use in update posts:

```python
import stripe, os
from datetime import datetime, timedelta

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

def get_mrr_snapshot() -> dict:
    """Pull current MRR and active subscriber count from Stripe."""
    subs = list(stripe.Subscription.list(status="active", limit=100).auto_paging_iter())
    mrr = sum(
        s["items"]["data"][0]["price"]["unit_amount"] / 100
        for s in subs
        if s["items"]["data"][0]["price"]["recurring"]["interval"] == "month"
    )
    return {
        "mrr": round(mrr, 2),
        "active_subscribers": len(subs),
        "as_of": datetime.now().strftime("%Y-%m-%d"),
    }

print(get_mrr_snapshot())
```

## Best practices
- Share real numbers, including zero — "MRR: $0 (launched today)" earns more engagement than omitting metrics; IH culture rewards vulnerability
- Frame failure posts as learnings, not complaints — "We tried X, it failed, here's why" gets 5-10x more comments than "X doesn't work for us"
- End every update post with a specific, answerable question — open-ended "any feedback?" gets ignored; "How do you handle pricing objections for a $49/month tool?" gets 20 replies
- Cross-post monthly updates to Twitter/X as a thread within 24 hours of the IH post to maximize reach and IH follower growth
- Apply for the IH podcast or interview at $10K MRR — it's the single highest-leverage IH content format, but only after achieving a real milestone
- Comment on 2-3 other makers' posts before publishing your own each week; IH feed algorithms and community norms reward reciprocal engagement

## AI-agent gotchas
- Agent-drafted posts sound too polished and structured — IH community values genuine imperfection; instruct agent to use casual phrasing, contractions, and first-person narrative; then review and rough up the language
- Monthly update posts require accurate current metrics; never ask the agent to estimate metrics — provide real numbers from Stripe/Plausible and let agent format them
- Agents may generate community questions that are too generic ("What do you think?") — instruct agent to write questions that are specific to your product's current challenge
- Human-in-loop checkpoint: all posts must be reviewed and personally adjusted by the founder before publishing — voice authenticity is the primary differentiator in build-in-public content
- IH has no API; agents cannot check whether a post was received well, what comments came in, or whether to follow up — all community monitoring is manual
- Cross-posting identical text to IH, Twitter/X, and LinkedIn without platform-specific adaptation performs poorly on each platform — agent should produce 3 separate versions from the same source material

## References
- https://www.indiehackers.com/ — Official platform; browse top posts to calibrate expected format and tone
- https://www.indiehackers.com/podcasts — Founder interviews; use as reference for voice and storytelling style
- https://www.indiehackers.com/post/how-to-get-traffic-ama-19b23a0638 — Courtland Allen AMA on IH growth tactics
- https://www.indiehackers.com/products — Browse revenue milestone posts for formatting reference
- https://typefully.com/developers — Typefully API for cross-posting IH content to Twitter/X
