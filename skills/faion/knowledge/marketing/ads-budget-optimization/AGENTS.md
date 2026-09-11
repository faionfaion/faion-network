# Ads Budget Optimization

## Summary

**One-sentence:** Allocates budgets via efficiency-ratio + 70-20-10 rule (70% scale / 20% optimize / 10% test) and emits a monthly reallocation spec with scale-up + scale-down triggers.

**One-paragraph:** Most paid-ads teams cut underperformers prematurely and double scaling-campaigns recklessly. This methodology imposes 70-20-10 budget discipline (70% scaling winners / 20% optimizing mid / 10% test reserve), efficiency-ratio based reallocation (ROAS / CPA / target multiple), and explicit step-rules (no > 20% budget change per week unless evidence). Output: monthly allocation spec + weekly review template + cross-channel reallocation rules.

**Ефективно для:**

- Multi-campaign PPC manager шукає reallocation framework без premature cuts.
- Заміна gut-feel allocation на 70-20-10 + efficiency-ratio rules.
- Scale-up discipline: ніяких > 20% budget jumps без evidence.
- Cross-platform reallocation: Meta vs. Google vs. LinkedIn based on ratio.

## Applies If (ALL must hold)

- Multi-campaign or multi-channel program (>= 3 campaigns OR 2 platforms).
- Spend >= $3k/month total.
- Conversion tracking accurate (variance < 15% per ads-attribution-models methodology).
- Weekly or monthly review meeting in place.

## Skip If (ANY kills it)

- Single-campaign account — no reallocation surface.
- Conversion tracking unreliable — allocate based on broken data is worse than steady-state.
- Spend < $1k/mo — allocation overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 14 testable rules with rationale + source: 70-20-10 partition, efficiency-ratio reallocation, 20% weekly step cap, premature-cut block, monthly rebalance, target CPA from LTV, efficiency ratio (target/actual CPA) as primary metric, never collapse test budget, 2-week learning threshold, 30% scaling increment, stop scaling at +40% CPA, cross-channel by efficiency ratio, incrementality before cutting a channel | ~1900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns (symptom/root-cause/fix): premature cut, single-step doubling, no test reserve, equal distribution, one-step doubling, test budget cut under pressure, 3-4 day cut, CPA without downstream quality | ~1100 |
| `content/04-procedure.xml` | essential | 5 generic steps plus the monthly rebalance cycle: pacing check, reallocation decision matrix, incrementality pause before channel cuts; weekly-review and monthly-allocation template references | ~1150 |
| `content/05-examples.xml` | essential | End-to-end worked example plus working formulas and tables: target CPA from LTV, efficiency ratio scale, 70-20-10 tranches, reallocation decision matrix, diminishing returns, pacing formula, cross-channel comparison, one reallocation pass, incrementality outcomes | ~1450 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml: spend, attribution variance, test reserve, step size, CPA-vs-target bands (0.7 / 1.0 / 1.3 / 2.0), CPA increase on scale | ~850 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-budget-optimization` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md.j2` | Markdown spec skeleton |
| `templates/spec.md` | Markdown spec skeleton Generated from `templates/spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md.j2` | Minimum viable filled spec |
| `templates/_smoke-test.md` | Minimum viable filled spec Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

| `templates/monthly-allocation.md.j2` | legacy template for ads-budget-optimization — monthly-allocation |
| `templates/monthly-allocation.md` | legacy template for ads-budget-optimization — monthly-allocation Generated from `templates/monthly-allocation.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/weekly-review.md.j2` | legacy template for ads-budget-optimization — weekly-review |
| `templates/weekly-review.md` | legacy template for ads-budget-optimization — weekly-review Generated from `templates/weekly-review.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-budget-optimization.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
