# Agent Integration — Partnership Strategy

## When to use
- Distribution-constrained: product is solid, organic + paid are saturated, and you need to reach a defined audience that already gathers around another product or community.
- Building integrations that reduce churn (e.g., become a Slack/Notion add-on so leaving means losing a workflow).
- Co-marketing webinars, bundles, or guides where a complementary tool shares your ICP at zero CAC.
- Reseller or white-label expansion when you can't justify a sales team but a partner already has those relationships.

## When NOT to use
- Pre-PMF: partnerships add coordination overhead; spend that energy on direct customer interviews.
- When your value-prop is unclear — partners can't promote what they don't understand; one-pager test fails.
- High-burn 3-month runway scenarios — partnerships compound over 6-18 months, not 90 days.
- When churn is the real problem; partnerships add top-of-funnel but won't fix retention.

## Where it fails / limitations
- One-sided proposals: 80% of cold outreach offers no value to the partner; ignored.
- No ownership: a partnership without a single named DRI on each side decays within a quarter.
- No tracking: without UTMs/codes/event-data, you can't tell which partner moved revenue → can't reinvest.
- "Strategic" partnerships with logos but no joint plan; classic vanity, zero pipeline.
- Legal drag: integration partnerships without DPAs/SCCs stall once enterprise deals appear.

## Agentic workflow
Use Claude subagents for the high-volume, low-judgement parts: prospecting, scoring, drafting outreach, summarizing partner content, and assembling a one-pager per target. Keep deal terms, contract redlining, and revenue-sharing decisions in human review. Run as a pipeline: list-build (agent) → score (agent) → personalize outreach (agent) → human-send → reply triage (agent) → human-negotiate → execution kickoff (agent prepares assets).

### Recommended subagents
- `general-purpose` — partner discovery (web research, audience overlap), scorecard population.
- `faion-content-agent` — outreach personalization, one-pager assembly, co-marketing content drafts.
- `password-scrubber-agent` — sanitize partner CRM exports / partnership trackers before sharing.

### Prompt pattern
- "List 30 SaaS tools whose ICP overlaps ours (founders 1-50 employees, marketing buyer). For each: tagline, audience size proxy, recent product news, named BD/partnerships contact via LinkedIn. Score 1-25 using the partnership scorecard."
- "For top 10, draft a 120-word outreach email referencing their recent launch + a concrete 2-week co-marketing pilot proposal. Include CTA: 15-min intro call."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Audit which OSS communities use a competitor — find adjacent partner candidates | `apt install gh` |
| `httpx` | Pull public marketing pages, About pages, customer logos | `pip install httpx` |
| `linkedin-scraper` (Selenium) | Identify BD/partnerships titles | DIY, watch ToS |
| `pandas` | Score and rank partner candidates | `pip install pandas` |
| `crossbeam` CLI/API | Account-overlap detection if both parties opt in | https://docs.crossbeam.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PartnerStack | SaaS | API yes | PRM + partner payouts, B2B SaaS |
| Crossbeam | SaaS | API yes | Account mapping for overlap detection |
| Reveal | SaaS | API yes | EU-friendly Crossbeam alternative |
| Impartner | SaaS | API yes | Enterprise PRM |
| Allbound | SaaS | API yes | Channel-partner enablement |
| HubSpot | SaaS | API yes | Lightweight partner CRM |
| Pipedrive | SaaS | API yes | Pipeline mgmt for partnership stages |
| Notion / Airtable | SaaS | API yes | Partnership tracker DIY |
| DocuSign / PandaDoc | SaaS | API yes | Co-marketing + reseller agreements |
| Zapier / n8n | SaaS / OSS | API yes | Automate partner-onboarding emails |

## Templates & scripts
See `templates.md` for one-pager and tracker. Inline scoring helper:

```python
# partner_score.py — ranks partner candidates 0-25
import pandas as pd

def score(row):
    return (
        row["reach_1_5"]
        + row["relevance_1_5"]
        + row["trust_1_5"]
        + (6 - row["effort_1_5"])
        + (6 - row["risk_1_5"])
    )

df = pd.read_csv("partner_candidates.csv")
df["score"] = df.apply(score, axis=1)
df["proceed"] = df["score"] >= 18
df.sort_values("score", ascending=False).to_csv("partner_shortlist.csv", index=False)
```

## Best practices
- Lead with the partner's win in the first paragraph; founders and BD leads scan for "what's in it for me" and bin the rest.
- Always propose a small-bet first (joint blog, single webinar) before pitching a multi-quarter integration.
- Instrument from day 1: unique UTM per partner + dedicated landing page; vague co-promo dies in attribution debates.
- Keep a 30-60-90 review cadence; partnerships rot in silence, not from explicit failure.
- Document partner roles inside your PRM; verbal agreements with no DRI evaporate when champions leave.

## AI-agent gotchas
- Models confidently invent partnership-team contact names — always validate via LinkedIn or company About page; never send to fabricated emails.
- Cold-outreach output drifts toward spammy templates; constrain with "must reference X-specific recent action" + "no superlatives" + "<150 words".
- Agents will overstate audience overlap from public data; require the agent to quote the data point ("their footer says 12K customers") rather than assert.
- Don't let an agent auto-send partner outreach — partner-network relationships are repeated games and one bad email burns goodwill across an industry segment.
- Contract drafting: never autogenerate legal terms; agents write summaries, humans (and counsel) own the redline.
- Revenue-share math: prompt agents to show the formula explicitly ("30% of $99 MRR × 12 months"); LLMs flub multi-step economics.

## References
- PartnerStack Partner Playbook: https://www.partnerstack.com/resources
- Crossbeam Ecosystem-Led Growth: https://www.crossbeam.com/resources
- "Sales as a Science" by Andrus Purde — partnership-led growth chapters
- Partnership Leaders community: https://www.partnershipleaders.com/
