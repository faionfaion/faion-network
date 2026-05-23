# Product Development Trends

## Summary

**One-sentence:** Scores emerging trends on a 4-axis rubric (signal strength + adoption velocity + revenue alignment + decay risk) producing a quarterly trend brief with explicit 'bet / monitor / ignore' verdicts.

**One-paragraph:** Systematic quarterly trend research that filters hype: each candidate trend is scored on 4 axes (signal strength, adoption velocity, revenue alignment, decay risk), classified as bet / monitor / ignore, and traced back to >=3 independent sources (one academic / filing, one practitioner, one market signal). Output: trend-brief.md with the picks + rationale + kill-criteria per bet.

**Ефективно для:**

- Quarterly strategy review: куди йти у наступному кварталі.
- Roadmap-планування: чи варто інвестувати в AI / on-device / privacy / etc.
- Investor update з 'trend snapshot' секцією.
- Hiring rationale: під який trend ми наймаємо.
- Newsletter / content marketing: серія 'trend digest'.

## Applies If (ALL must hold)

- Quarterly strategy review on where to bet next.
- Roadmap planning: AI / on-device / privacy / sustainability / etc.
- Investor update with a 'trend snapshot' section.
- Hiring rationale: under which trend are we adding headcount?
- Content marketing 'trend digest' series.

## Skip If (ANY kills it)

- Acute delivery cycle (next sprint) - trends are quarterly+.
- Crisis mode (revenue cliff, outage) - solve the crisis first.
- Pure execution org with no R&D budget.
- Niche internal tool where outside trends do not apply.
- When the only goal is to add a buzzword to the deck.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Candidate trend list | markdown | PM + research team |
| Product positioning doc | markdown | marketing |
| Quarterly revenue target | currency | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[trend-analysis]] | supplies the raw signal sources that this methodology scores |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `signal-pull` | haiku | Mechanical pull of academic / filings / practitioner sources. |
| `score-axes` | sonnet | Score signal strength + velocity + alignment + decay. |
| `verdict-bet-monitor-ignore` | opus | Strategic verdict + kill criteria per bet. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trend-brief.md` | Quarterly trend brief skeleton with bet/monitor/ignore tables |
| `templates/score-signals.py` | Score a candidate trend across 4 axes; print JSON |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-development-trends.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[product-development-trends-2026]]
- [[trend-analysis]]
- [[competitive-intelligence]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
