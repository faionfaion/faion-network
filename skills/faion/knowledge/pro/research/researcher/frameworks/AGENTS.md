# Research Frameworks

## Summary

A toolbox of eight named pre-revenue research frameworks — 7Ps ideation, Paul Graham questions, niche evaluation (50-point matrix), validation criteria, Jobs-to-be-Done, TAM/SAM/SOM, competitive intelligence, and Value Proposition Canvas — treated as a router: the agent picks the smallest subset that answers the current decision, not all eight at once.

## Why

Framework theater — producing a 50/50 niche score with zero primary research — is worse than no score. The router approach forces the agent to justify which frameworks are relevant, locks the ICP in one sentence before any framework runs, and requires a URL + retrieval date on every external number. Downstream SDD agents (`faion-sdd`) ingest the artifacts directly.

## When To Use

- Founder at the "what should I build?" stage needing a structured idea funnel.
- Investor pitch requiring TAM/SAM/SOM plus a competitive table.
- Pivot review: re-score current niche against the same matrix to make stay/pivot defensible.
- GTM repositioning: rebuild the Value Proposition Canvas before rewriting the homepage.
- Multi-idea triage: score N ideas in parallel and rank by niche score.

## When NOT To Use

- Already shipping with paying customers — use cohort analysis and retention curves instead.
- Single-question clarifications ("should I charge $19 or $29?") — use a pricing experiment.
- Pure technical scoping (architecture, API design) — use SDD `design.md`.
- Hobby projects, internal tools, OSS side projects with no revenue goal.
- Two-sided marketplaces pre-launch where supply/demand dynamics dominate.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework-router.xml` | Router logic, decision map (idea/validate/size/position/pivot), pipeline steps 1-8. |
| `content/02-ideation-frameworks.xml` | 7Ps of Ideation, Paul Graham questions, usage rules. |
| `content/03-evaluation-frameworks.xml` | 50-point niche matrix, validation criteria (frequency/intensity/WTP/search/competition), JTBD statement template. |
| `content/04-sizing-and-positioning.xml` | TAM/SAM/SOM three-method triangulation, Value Proposition Canvas fit check, competitive table. |

## Templates

| File | Purpose |
|------|---------|
| `templates/framework-router.sh` | Shell router: prints relevant framework names for a given decision mode. |

## Scripts

none
