# Agent Integration — Product Development Trends 2026

## When to use
- Quarterly product strategy reviews where the team needs an external view of where development practice is moving (AI-augmented ideation, continuous discovery, rapid pivots).
- Drafting a new product line or pivot brief and you need a defensible answer to "what is industry-standard in 2026" for engineering+product+design ways of working.
- Onboarding a new product manager or research lead who must align on the modern Agile + Data-Driven + Cross-Functional model before opening the SDD `roadmap.md` or `spec.md`.
- Feeding `.aidocs/product_docs/market-research.md` and `executive-summary.md` with a "trends" section grounded in 2025-2026 signals rather than 2019-era playbooks.
- Selecting which methodology folders inside `pro/research/researcher/` to invoke next (e.g. `continuous-discovery`, `opportunity-solution-trees`, `experimentation-at-scale`).

## When NOT to use
- The decision is purely tactical (pick a button color, schedule a sprint) — trends research is overkill.
- You already have a recent (≤6 months) trend report on the same domain. Re-running adds noise, not insight.
- The product is in pure execution / scale-up phase with locked roadmap; trends here destabilize without buying anything.
- Regulated domains (medical devices, avionics) where waterfall + audit trail is a contractual requirement, not a fashion choice.
- Solo-founder MVP under one month from launch — speed-to-customer beats trend alignment.

## Where it fails / limitations
- Trends drift in months, not years; any artifact older than ~2 quarters should be treated as historical context, not guidance.
- "AI-augmented ideation" is overclaimed in vendor blogs. Without a concrete experiment hook, agents will return marketing copy as findings.
- Cross-functional collaboration patterns are highly company-shape dependent (50-person SaaS vs 5000-person enterprise) — generic conclusions misfire.
- Consumer trend bullets ("brands that do good", sustainability) are easily fabricated by LLMs from outdated training data; require URL-grounded citations.
- The framing here mixes process trends (Agile, discovery cadence) with topical trends (sustainability, AI). Keep them separated when handing to downstream agents or they collapse into mush.

## Agentic workflow
Drive this methodology with two passes. Pass 1: an Opus-led strategic scan that ingests `README.md`, picks 4–6 trend axes, and emits a structured JSON spec (`{trend, signal, source_url, confidence, impact}`). Pass 2: a Sonnet-led parallel sweep — one subagent per axis — fetches WebSearch + WebFetch evidence and writes a single section. A reviewer subagent merges sections, deduplicates, and flags any unsourced claim. The methodology's own "Agent Selection" table already prescribes Opus for AI-impact analysis and Sonnet for synthesis; keep that split.

### Recommended subagents
- `faion-research-agent` (in `pro/research/researcher/`) — orchestrator with 9 modes; use `market` and `niche` modes to anchor trend findings to a concrete TAM context, not floating abstractions.
- `faion-sdd-executor-agent` (repo root `agents/`) — wrap the trend write-up as an SDD task so it lands in `.aidocs/product_docs/` with a quality gate, not an ad-hoc dump.
- Companion methodologies (load via `Read`, not `Skill()`):
  - `pro/research/researcher/continuous-discovery/` for the cadence pattern.
  - `pro/research/researcher/opportunity-solution-trees/` to convert trends into actionable bets.
  - `pro/research/researcher/trend-analysis/` for signal-vs-noise scoring methodology.
  - `pro/product/product-manager/experimentation-at-scale/` for the execution leg.

### Prompt pattern
```
You are a trends-research subagent. Read TARGET/README.md.
Emit JSON: [{trend, evidence_url, last_seen_date, confidence_0_1, impact_HML, downstream_methodology}].
Reject any trend without a 2025-or-later URL. Max 6 items.
```

```
You are the merge reviewer. Inputs: N JSON arrays from sibling subagents.
Output: deduplicated table grouped by axis (process | tooling | consumer | org).
Flag unsourced rows with FLAG_NO_SOURCE. Do not paraphrase URLs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Pull recent issues / PRs from leading product-OSS repos (Linear, PostHog, Plane) for ground-truth on practice trends | https://cli.github.com |
| `curl` + `jq` | Hit Hacker News Algolia, Lobsters, Product Hunt APIs to extract dated headlines per trend axis | builtin |
| `pandoc` | Convert sourced web articles to plain text before feeding into the merge subagent (kills HTML noise that hallucinates citations) | https://pandoc.org |
| `lychee` | Validate every URL written into `agent-integration.md` and downstream reports — catches broken/hallucinated links before commit | https://lychee.cli.rs |
| WebFetch (Claude Code) | Pull and summarize a specific URL inline; pair with WebSearch for breadth | builtin |
| `dvc` / `git-lfs` | Track snapshot artifacts of trend reports across quarters so drift is auditable | https://dvc.org |
| `marker` (Datalab) | Convert research PDFs (Gartner, Forrester) to markdown for ingestion | https://github.com/VikParuchuri/marker |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Exa.ai | SaaS search API | Yes (REST + SDK) | Better than generic search for "what changed in product practice in 2026"; supports `num_results`, `start_published_date` |
| Perplexity API (sonar-pro) | SaaS | Yes | Returns answers + citations in one call; useful as a second-opinion grader for the merge subagent |
| LinkedIn Sales Nav / talent insights | SaaS | Limited (no public API) | Best signal for org-trend axis (rise of "Product Operations" titles); requires human-in-the-loop scrape |
| Crunchbase Enterprise API | SaaS | Yes | Funding rounds tagged by category track which trend categories actually attract capital |
| PostHog Cloud | SaaS / OSS | Yes (REST) | "What does data-driven product mean in 2026" — usage telemetry from a real platform beats blogs |
| Dovetail | SaaS | Yes (REST) | Industry de-facto for continuous discovery repos; their public reports are a primary signal source |
| Maze | SaaS | Yes (REST) | Rapid concept testing — embodies the "days not weeks" speed requirement |
| Linear | SaaS | Yes (GraphQL) | Public roadmap + issue corpus is a live trend telescope into modern product orgs |
| ProductBoard | SaaS | Yes (REST) | Cross-functional prioritization patterns; export feature feedback for ground-truth |
| Otter.ai / Fireflies | SaaS | Yes (REST) | Customer-call transcripts feed continuous-discovery agents directly |

## Templates & scripts

Inline trend-evidence collector (Python, ≤50 lines). Run inside the worktree to populate a `trends.jsonl` artifact before invoking the merge subagent. Requires `EXA_API_KEY` env var.

```python
#!/usr/bin/env python3
"""Collect 2025-2026 trend evidence per axis. Output: trends.jsonl."""
import json
import os
import sys
import urllib.request

AXES = ["ai-augmented-ideation", "continuous-discovery",
        "rapid-pivot-cadence", "cross-functional-team-shape"]
KEY = os.environ["EXA_API_KEY"]
URL = "https://api.exa.ai/search"

def fetch(axis: str) -> list[dict]:
    body = json.dumps({
        "query": f"product development {axis} 2025 OR 2026",
        "num_results": 8,
        "start_published_date": "2025-01-01",
        "use_autoprompt": True,
    }).encode()
    req = urllib.request.Request(
        URL, data=body,
        headers={"x-api-key": KEY, "content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    return [
        {"axis": axis, "title": x["title"], "url": x["url"],
         "published": x.get("publishedDate", ""), "score": x.get("score", 0)}
        for x in data.get("results", [])
    ]

def main() -> int:
    out = sys.argv[1] if len(sys.argv) > 1 else "trends.jsonl"
    with open(out, "w") as f:
        for axis in AXES:
            for row in fetch(axis):
                f.write(json.dumps(row) + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Pair with `lychee trends.jsonl --no-progress` before handing to the merge subagent. See `templates.md` for the executive-summary skeleton (currently empty — populate from `pro/research/researcher/trend-analysis/templates.md`).

## Best practices
- Anchor every trend to one URL with a 2025-or-later `publishedDate`. Strip anything older — the trend window for product practice is ~18 months.
- Separate process trends (how teams work) from topical trends (what users want). Mixing them in one bullet list hides which is actionable for engineering vs marketing.
- Run the methodology in pairs: `product-development-trends-2026` produces the lens, `opportunity-solution-trees` converts the lens into bets. Solo runs decay into vibes.
- Demand a "what stopped being true in 2024?" section. Trends-only reports inflate; subtraction reports are honest.
- Keep the AI-augmented-ideation axis on a tighter leash than the others (lower temperature, more sources) — it has the highest hallucination risk because the corpus is full of vendor copy.
- Quote primary sources (Linear's changelog, PostHog's product blog, Dovetail's research reports) over secondary aggregators ("top 10 product trends" listicles).
- Re-run quarterly. Diff against prior `executive-summary.md`; the diff is the actual finding.

## AI-agent gotchas
- LLM training cutoff bias: agents will assert 2023-era practices ("OKRs revival", "design sprints") as 2026 trends. Hard-require URLs with 2025+ dates and reject otherwise.
- "Cross-functional team" is a phrase agents recombine endlessly. Demand a concrete artifact: an org chart, a job posting, a public retro post.
- Agents merge sustainability/eco-friendly bullets into every report; that's pattern-matching, not evidence. Keep an axis-of-evidence table and reject empty rows.
- WebSearch returns SEO-optimized blog spam at the top. Have a reviewer subagent down-rank domains in a denylist (medium-tier vendor blogs without primary data).
- Continuous-discovery cadence is often quoted as "weekly" without source; require a named team / case study before accepting cadence claims.
- The methodology overlaps `product-development-trends/` (without the year suffix). Always disambiguate which is canonical for the current quarter; otherwise two subagents will write two reports and the merge agent will silently pick one.
- Human-in-the-loop checkpoint #1: after pass-1 JSON spec, before pass-2 sweep — confirm the 4–6 axes are the right ones for this product context.
- Human-in-the-loop checkpoint #2: before merging the trend report into `.aidocs/product_docs/executive-summary.md` — the report shapes roadmap conversations, so a human signs off on framing.

## References
- Teresa Torres, "Continuous Discovery Habits" (Product Talk) — canonical source for the discovery cadence trend.
- Marty Cagan, "Transformed" (SVPG, 2024) — cross-functional empowered-team model.
- Reforge, "Product Operations" reports (2024-2025) — org-shape trend signal.
- Dovetail "State of User Research" annual report — continuous-discovery adoption data.
- Linear public changelog (linear.app/changelog) — practice-trend telescope into a modern product org.
- PostHog product blog — data-driven product practice case studies.
- Sibling methodology: `pro/research/researcher/trend-analysis/` for signal-vs-noise scoring.
- Sibling methodology: `pro/research/researcher/continuous-discovery/` for cadence ops.
- Sibling methodology: `pro/product/product-manager/experimentation-at-scale/` for downstream execution.
