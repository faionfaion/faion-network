# Service Blueprint

## Summary

**One-sentence:** Extends a customer journey map with back-stage actors, support systems, and the line-of-visibility, producing a single artefact that ties UX friction to operational root causes.

**One-paragraph:** Journey-mapping is in the solo tier; the back-stage / service-blueprint extension is what enterprise UX, B2B, and P6 product-team work needs to ship. A journey map tells you 'the user gets frustrated here'; a service blueprint tells you 'the user gets frustrated here BECAUSE the support agent has no view into the billing system.' This methodology defines the canonical 5-swimlane blueprint (customer actions, frontstage interactions, line of visibility, backstage actions, support processes/systems), the failure-point notation, and the moment-of-truth scoring. Output is a single-page blueprint that engineering, ops, and design can all act on.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «service blueprint» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- you already have a customer journey map (or are creating one as input).
- the product involves back-stage actors (ops, support, fulfilment, finance) the user does not see.
- the goal is to reduce friction by changing back-stage processes, not just UI.

## Skip If (ANY kills it)

- the product is pure self-serve software with no back-stage human involvement.
- a service blueprint already exists < 6 months old for the same journey.
- regulatory constraint mandates a different blueprint template (defer to that template).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Service Blueprint task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent role/operating context for B2B research. |
| `solo/ux/ui-designer` | supplies the upstream journey-map artefact this methodology extends. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-blueprint.md` | Markdown skeleton: 5-swimlane table + moments-of-truth scoring section + backlog item slots. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-service-blueprint.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[jtbd-switch-interview]]
- [[thematic-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
