# Research Frameworks Router

## Summary

**One-sentence:** Router methodology that takes a research goal and routes the agent to the correct framework (TAM/SAM/SOM, Five Forces, JTBD, OST, Lean Canvas, Kano) instead of mixing them.

**One-paragraph:** Picking the wrong framework wastes 10-50k tokens. This methodology is a router: given a research goal phrasing, it emits a decision-record naming the correct framework (TAM/SAM/SOM, Porter Five Forces, JTBD, Opportunity-Solution Trees, Lean Canvas, Kano model, RACI, RICE, ICE, MoSCoW) plus a rationale and the methodology slug to load next. Stops agents from mashing 3 frameworks together.

**Ефективно для:**

- Дослідницька задача має кілька можливих frameworks; треба обрати один.
- Agent починає 'TAM/SAM/SOM + Lean Canvas + JTBD одночасно' - треба зупинити.
- Solopreneur не пам'ятає, для чого який framework призначений.
- Передача задачі іншому subagent - потрібен явний decision-record вибору framework.
- Перегляд старого артефакту: переконатися, що використано правильний framework.

## Applies If (ALL must hold)

- Research goal has multiple plausible frameworks; agent must pick one before drilling in.
- Agent begins mashing 3 frameworks together; the router prevents the mash.
- Solopreneur does not remember which framework solves which question.
- Task handoff between subagents requires an explicit framework-selection decision-record.
- Reviewing an old artefact to confirm the right framework was used.

## Skip If (ANY kills it)

- Goal is already framework-specific ('do TAM/SAM/SOM') - skip router and load the framework directly.
- Pure mechanical task (file scan, citation check) - no framework needed.
- Strategic brainstorm with no defined goal yet - run idea-generation first.
- Tool-only question ('what does PostHog do') - look up tool docs, not a framework.
- Sensitive / regulated subject area where the framework is fixed by compliance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Goal statement | 1-2 sentences | user / orchestrator |
| Stage tag | ideation / pre-PMF / post-PMF / scale | founder / orchestrator |
| Output shape required | report / spec / decision / scoring | downstream consumer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[methodologies-index]] | supplies the catalog of frameworks the router maps onto |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-goal` | haiku | Pattern-match goal phrasing against framework keywords. |
| `emit-decision-record` | haiku | Mechanical decision-record output with picked slug. |

## Templates

| File | Purpose |
|------|---------|
| `templates/framework-router.sh` | CLI router: takes goal + stage and prints the picked framework slug |
| `templates/framework-decision.md` | Decision-record skeleton (goal + candidates + verdict + rationale) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-frameworks.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[methodologies-index]]
- [[methodologies-detail]]
- [[workflows]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
