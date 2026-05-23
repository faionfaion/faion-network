# Customer Journey Mapping

## Summary

**One-sentence:** Generate a current-state customer journey map (stage × row matrix with persona, actions, touchpoints, thoughts, emotions, pain points, opportunities) grounded in cited research evidence.

**One-paragraph:** Visualise the complete experience a user has with a product over time. Inputs: persona definition + cited research artefacts (interview IDs, support tickets, analytics events). Output: a stage × row matrix covering all eight components (persona, stages, actions, touchpoints, thoughts, emotions, pain points, opportunities), every cell either citing an evidence ID or marked "no data". Use to find cross-channel friction and align stakeholders on the current-state experience before designing improvements.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Designing or redesigning a multi-step flow (onboarding, checkout, support, offboarding).
- Research data exists (interviews, observation, analytics, support tickets, surveys).
- A specific persona and journey scope (start point + end point) can be named.

## Skip If (ANY kills it)

- No research data exists — a purely imagined map creates false consensus.
- Single isolated interaction with no multi-step journey.
- Stakeholders want quantitative evidence; journey maps are qualitative synthesis, not metrics.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Persona definition (specific, research-based) | doc | UX research |
| Cited research artefacts (interview IDs, ticket IDs, analytics events) | spreadsheet or doc | research / ops |
| Journey scope (start + end point + persona) | one-paragraph | PM / UX |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/user-interviews` | Map cells must cite interview IDs. |
| `solo/ux/ux-ui-designer/usability-testing` | Pain points often surface in usability findings. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the journey-map artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 7-step procedure: scope → research → stages → rows → emotions → pain → opportunities | ~700 |
| `content/05-examples.xml` | medium | Worked e-commerce purchase journey end-to-end | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `synthesise-map` | sonnet | Stage × row matrix composition from structured research. |
| `extract-evidence` | haiku | Mechanical pull of interview IDs / ticket IDs from corpus. |
| `score-emotional-arc` | opus | Identify sharp dips vs smooth averages; rejects LLM smoothing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/journey-map.md` | Full journey map: stage × row matrix. |
| `templates/stage-detail.md` | Single-stage deep-dive template. |
| `templates/prompt-map.txt` | Agent prompt skeleton for journey-map synthesis. |
| `templates/funnel-to-stages.py` | Convert funnel CSV to stage summaries for ingest. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-journey-mapping.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[user-interviews]]
- [[usability-testing]]
- [[wireframing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named persona + scope, research evidence reachable) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
