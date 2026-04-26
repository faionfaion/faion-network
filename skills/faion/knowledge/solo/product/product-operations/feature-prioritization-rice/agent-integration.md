# Agent Integration — Feature Prioritization (RICE)

## When to use
- Backlog has 10+ candidates that need an objective, repeatable rank for the next quarter or release.
- Stakeholders disagree on priority and you need a math-based artifact to defuse HiPPO.
- A subagent is asked to draft a roadmap from a raw idea list and you need a defensible default ordering.
- You have at least funnel/MAU data plus an effort estimate per item; otherwise switch to MoSCoW.

## When NOT to use
- Single-feature decisions (RICE adds noise vs. a one-liner rationale).
- Pre-PMF / 0-to-1 products where Reach is unknowable — use opportunity solution trees or Kano.
- Compliance, security, or contractual must-haves — they bypass RICE and go straight into the plan.
- Cross-portfolio bets where strategic fit dominates the score (RICE has no strategy term).

## Where it fails / limitations
- Garbage in, garbage out: 80% of the score variance comes from Reach guesses; fabricating it produces false precision.
- Confidence inflation — agents and humans both default to 80–100% when uncomfortable. Audit confidence < 80% for novel work.
- Effort is usually under-estimated 2–3x; LLMs are worse at this than engineers.
- No discount for sequencing: a high-RICE item that depends on three low-RICE items can still be wrong to start.
- Encourages many small wins, can starve large strategic bets — pair with a "20% strategic" carve-out.

## Agentic workflow
Drive RICE as a structured-output pipeline. A discovery subagent gathers Reach evidence (analytics, ticket counts, segment sizes) and Impact evidence (test results, similar features). A scorer subagent emits one JSON row per candidate with R/I/C/E plus a `rationale` field per factor. A reviewer subagent challenges any score with C ≥ 80% that lacks cited evidence, and any E ≤ 1 that has no decomposition. Final ranked table is committed under `.aidocs/.../prioritization/rice-<quarter>.md` and linked from the roadmap.

### Recommended subagents
- `faion-mlp-feature-proposer-agent` — RICE-specific scorer named in this methodology's metadata.
- `faion-mvp-scope-analyzer-agent` — sanity-checks Effort estimates against MVP scope.
- `faion-spec-reviewer-agent` — validates that each high-RICE item already has a usable spec before it enters "Now".
- General-purpose `researcher` (analyst-style) — pulls Reach numbers from analytics dumps.

### Prompt pattern
```
Score the following N features with RICE. For each, output JSON with fields:
  id, reach (users/quarter, integer), reach_source (citation),
  impact (3|2|1|0.5|0.25), impact_rationale,
  confidence (0.5|0.8|1.0), confidence_evidence,
  effort (person-months, decimal), effort_breakdown.
Then compute rice = (reach*impact*confidence)/effort and rank descending.
Reject any row where confidence>=0.8 has no citation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `productboard` CLI / API | Pull feature backlog, push RICE scores back as custom fields | https://developer.productboard.com |
| `linear-cli` / Linear API | Read issues, write `priority` / custom RICE field | https://developers.linear.app |
| `jira` REST API + `jira-cli` (ankitpokhrel) | Bulk-update Jira tickets with RICE score field | https://github.com/ankitpokhrel/jira-cli |
| `gh` CLI + GitHub Projects v2 GraphQL | Manage RICE on Issues / Projects fields | https://cli.github.com |
| Notion API (`@notionhq/client`) | Read/write a RICE database row | https://developers.notion.com |
| Airtable API | Spreadsheet-style RICE store with formulas | https://airtable.com/developers/web/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Yes (REST + webhooks) | Native prioritization frameworks incl. RICE |
| Airfocus | SaaS | Yes (REST) | Built-in RICE/Value-vs-Effort scoring |
| Craft.io | SaaS | Yes (REST) | RICE plus custom scorecards |
| Linear | SaaS | Yes (GraphQL) | Use custom fields for R/I/C/E; agents can mutate |
| Notion / Airtable | SaaS | Yes (REST) | Cheapest agent-writable backing store |
| Aha! | SaaS | Yes (REST) | Strategy + RICE; useful for theme-anchored RICE |
| OpenProject | OSS | Yes (REST) | Self-hosted alt for RICE custom fields |

## Templates & scripts
See `templates.md` for the scoring spreadsheet and decision record. Minimal scoring helper for an agent to call:

```python
# rice.py — feed JSON list, get ranked output
import json, sys
def rice(r, i, c, e):
    if e <= 0: raise ValueError("effort must be > 0")
    return round((r * i * c) / e, 1)

rows = json.load(sys.stdin)
for row in rows:
    row["score"] = rice(row["reach"], row["impact"], row["confidence"], row["effort"])
rows.sort(key=lambda x: x["score"], reverse=True)
for n, row in enumerate(rows, 1):
    row["rank"] = n
json.dump(rows, sys.stdout, indent=2)
```

## Best practices
- Anchor Impact on the standardized scale (3 / 2 / 1 / 0.5 / 0.25) — never invent intermediate values; it kills cross-feature comparability.
- Require an evidence URL for any Confidence ≥ 80%. No URL → cap at 50%.
- Re-score quarterly; archive prior scoring file with a date stamp so you can see drift.
- Express Reach in the same unit (users/quarter) for the entire batch; mixing month/quarter inflates some rows 3x.
- Apply a "strategic override" lane outside RICE for top-2 bets so they aren't crowded out by easy wins.
- Pair RICE with WSJF or Cost of Delay when sequencing matters more than absolute score.

## AI-agent gotchas
- LLMs gravitate to round numbers (5000, 10000, 1.0) — force decimal Reach where analytics gives it.
- Effort is the most-hallucinated factor; require breakdown into design / dev / QA / docs sub-estimates and sum them.
- An agent that scores its own proposed feature has obvious bias; route scoring to a different subagent than the proposer.
- Watch for "confidence cascade": if upstream Reach is fabricated, downstream scores are precise nonsense. Gate scoring on `reach_source` being a real URL or table reference.
- Human-in-loop checkpoint: any item with score > 2x the median should be reviewed by a human before it lands in "Now".
- Never let an agent silently demote items below threshold — emit the full ranked list with cut line, not just the survivors.

## References
- Sean McVey, Intercom — "RICE: Simple prioritization for product managers" https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
- ProductPlan — "RICE Scoring Model" https://www.productplan.com/glossary/rice-scoring-model/
- Roman Pichler — "10 Tips for Agile Product Roadmapping" (on score drift) https://www.romanpichler.com/blog/
