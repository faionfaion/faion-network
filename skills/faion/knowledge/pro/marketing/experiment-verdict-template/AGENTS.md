---
slug: experiment-verdict-template
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Verdict card format closing A/B + campaign experiments on cadence — 5-verdict vocabulary, ≤5-day close-or-stop, secondary-metric gate, captured learning, routed action with named owner.
content_id: "b1dd66cee884d949"
complexity: medium
produces: spec
est_tokens: 3800
tags: [ab-testing, verdict, closure, learning, post-mortem, experiment-ops]
---
# Experiment Verdict Template

## Summary

**One-sentence:** Verdict card format closing A/B + campaign experiments on cadence — 5-verdict vocabulary, ≤5-day close-or-stop, secondary-metric gate, captured learning, routed action with named owner.

**One-paragraph:** A/B testing methodology covers design and statistics. What teams lack is a closing artefact: the single card that says "this experiment is done, here is the verdict, here is the decision, here is what we learned". Without it, experiments become zombie — left running long past their statistical close, results forgotten, learnings re-discovered. Core rules: 5-verdict vocabulary (ship-treatment / ship-control / inconclusive-iterate / inconclusive-stop / harmful-rollback); close within 5 business days of pre-registered close date or auto-stop at platform; secondary-metric gate (overriding requires named exec sign-off); captured learning with confidence tag; routed next action to a named owner. Output: a markdown + JSON verdict card persistent in the experiment ledger.

**Ефективно для:**

- A/B-tests cadence — biweekly or weekly close ritual.
- Campaign experiments — close + decision card before next quarter.
- Multi-stakeholder rollout — release owner, on-call, backlog owner all named.
- Agency / freelance handoff — verdict cards are the persistent product.

## Applies If (ALL must hold)

- ≥1 A/B test, holdout, or campaign experiment closes every 2 weeks.
- Experimentation platform (Optimizely / Statsig / GrowthBook / PostHog / GA / homemade) captures variant assignment + metrics.
- Weekly experiment review ritual exists or can be added.
- Decisions from experiments can route into product / marketing / pricing follow-ups.

## Skip If (ANY kills it)

- One-off campaign with no future cadence or learning need.
- Statistical power so low that the experiment can only produce inconclusive results — fix design first.
- No experimentation platform — instrument first.
- No named owner for the next action — verdict will not route.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pre-registration (hypothesis, primary metric, sample, close-date) | spec | growth team |
| Platform assignment + metric data | dashboard / API | experiment platform |
| Verdict template (markdown skeleton) | file | this methodology |
| Learnings database | DB / wiki | learnings-database-schema |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[experiment-hypothesis-scoring]] | Upstream producer of the pre-registration. |
| [[experiment-ledger-discipline]] | Where the verdict card persists. |
| [[ab-testing-basics]] | Statistical foundations underlying the verdict. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 5-verdict-vocabulary, close-within-5-days, secondary-metric-gate, captured-learning, routed-action | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the verdict card + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: pre-close check → write verdict → secondary review → learning capture → route action | 600 |
| `content/05-examples.xml` | essential | Worked example: pricing-page hero variant verdict with secondary-metric tension | 500 |
| `content/06-decision-tree.xml` | essential | Tree mapping primary + secondary signal to verdict + routed action | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-verdict` | sonnet | Cross-input synthesis (primary + secondary + power). |
| `capture-learning` | sonnet | Generalizable claim distillation. |
| `lint-vocabulary` | haiku | Enum check on verdict + secondary + action fields. |

## Templates

| File | Purpose |
|------|---------|
| `templates/verdict-card.md` | Markdown skeleton with the 7-field verdict card |
| `templates/verdict-card.json` | JSON example matching the output contract |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-experiment-verdict-template.py` | Validate one verdict card JSON against the schema | After verdict draft, before close in ledger |

## Related

- [[experiment-hypothesis-scoring]]
- [[experiment-ledger-discipline]]
- [[learnings-database-schema]]
- [[ab-testing-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from primary + secondary signal + power state to one of the 5 verdicts + the routed action, pinning the rule from `01-core-rules.xml`. Use it before drafting the verdict — picking the wrong verdict is the most consequential failure of the ritual.
