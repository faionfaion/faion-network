---
slug: usability-testing
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produce a usability-test artefact (plan + session script + findings report) with scenario-based tasks, success criteria, and four-level severity ratings tied to participant-blocked counts.
content_id: "a6fd93373f75147c"
complexity: medium
produces: report
est_tokens: 3700
tags: [usability, user-research, testing, ux-validation, qualitative]
---
# Usability Testing

## Summary

**One-sentence:** Produce a usability-test artefact (plan + session script + findings report) with scenario-based tasks, success criteria, and four-level severity ratings tied to participant-blocked counts.

**One-paragraph:** Observe real users completing tasks with a product to discover what works, what confuses, and where users struggle. Inputs: feature or flow ready for testing + recruitment pool (≥5 per segment). Output: a test plan (scope, tasks, success criteria), a session script with neutral phrasing, and a findings report — each finding tagged severity 1-4 by blocked-count + 60% threshold.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- A feature, prototype, or flow is reachable for participants to interact with.
- A recruitment pool of ≥5 participants per distinct segment is reachable.
- Stakeholders need evidence to validate or reject a design decision.

## Skip If (ANY kills it)

- Nothing testable yet (no wireframe or prototype) — nothing to observe.
- Fewer than 3 participants available — no pattern detection at that scale.
- Large-N quantitative benchmarking (SUS, statistical significance) — use surveys.
- Agent-as-facilitator — non-verbal cues + real-time probing are human-only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Testable prototype or live build | URL / file | engineering / UX |
| Recruitment pool with segment tags | list | UX ops |
| Feature spec / acceptance criteria | doc | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/prototyping` | Source of the prototype that gets tested. |
| `solo/ux/ux-ui-designer/user-interviews` | Pre-test interviews surface terminology and goals. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the usability-test artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: scope → tasks → script → run → rate → human-review | ~600 |
| `content/05-examples.xml` | medium | Worked findings report for a checkout flow test | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-tasks` | sonnet | Scenario-based task drafting. |
| `synthesise-findings` | sonnet | Cluster observations by symptom + frequency. |
| `severity-rate` | opus | Apply severity rubric with edge-case judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-plan.md` | Test plan skeleton. |
| `templates/session-script.md` | Session script skeleton with neutral phrasing. |
| `templates/finding-format.md` | Finding entry format with severity + frequency. |
| `templates/prompt-test-plan.txt` | Agent prompt for plan draft. |
| `templates/prompt-synthesize.txt` | Agent prompt for findings synthesis. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-usability-testing.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[prototyping]]
- [[user-interviews]]
- [[journey-mapping]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, prototype reachable, recruitment ≥5/segment) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
