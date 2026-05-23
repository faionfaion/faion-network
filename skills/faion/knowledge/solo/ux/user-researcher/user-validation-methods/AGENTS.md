---
slug: user-validation-methods
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Router methodology covering four validation lenses (JTBD, Persona, Problem Validation, Pain Mining); produces a routing decision artefact that selects the correct sub-methodology per research question and pins the rationale."
content_id: "ca843a19dd92bb93"
complexity: medium
produces: spec
est_tokens: 4800
tags: ["research", "validation", "user-research", "routing", "discovery"]
---
# User Validation Methods

## Summary

**One-sentence:** Router methodology covering four validation lenses (JTBD, Persona, Problem Validation, Pain Mining); produces a routing decision artefact that selects the correct sub-methodology per research question and pins the rationale.

**One-paragraph:** Discovery sprints often need multiple validation lenses in sequence. This router methodology takes a research question, classifies it against four lens types (JTBD = why users hire products; Persona = who users are; Problem Validation = does this problem exist and matter; Pain Mining = where users express frustration publicly), and emits a routing decision that names the chosen sub-methodology with rationale. Output: a routing decision spec downstream researchers consume to avoid defaulting to the methodology they know best rather than the one that answers the question.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Start of a discovery sprint with multiple open research questions.
- Onboarding a new researcher who needs the lens-selection rationale.
- Quarterly review of past research outputs to check whether the right lens was chosen each time.
- Pre-budget defence — pin which lenses were chosen and why, before stakeholders ask.

## Skip If (ANY kills it)

- The research question is already crystal-clear and matches one obvious lens.
- The team has only one lens available (e.g., no users yet — only Pain Mining is feasible).
- Substituting this router for actually running a lens — the router does not produce evidence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Research question list | one question per row | discovery brief |
| Lens availability matrix | which lenses the team can run | capability audit |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/jobs-to-be-done` | lens 1 — why users hire products |
| `solo/ux/user-researcher/problem-validation` | lens 3 — does this problem exist and matter |
| `solo/ux/user-researcher/pain-point-research` | lens 4 — where users express frustration |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-validation-methods.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-user-validation-methods.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-validation-methods.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[jobs-to-be-done]]
- [[problem-validation]]
- [[pain-point-research]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
