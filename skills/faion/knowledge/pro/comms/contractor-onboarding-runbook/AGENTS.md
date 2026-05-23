---
slug: contractor-onboarding-runbook
tier: pro
group: comms
domain: comms
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Contractor-specific 3-5 week onboarding runbook covering access, IP, paired-shadow, and day-30 review — does NOT reuse the FT employee onboarding-30-day template.
content_id: "a53c55a96ca57cd3"
complexity: medium
produces: playbook-step
est_tokens: 4200
tags: [contractor, onboarding, runbook, micro-agency, comms]
---
# Contractor Onboarding Runbook

## Summary

**One-sentence:** Contractor-specific 3-5 week onboarding runbook covering access, IP, paired-shadow, and day-30 review — does NOT reuse the FT employee onboarding-30-day template.

**One-paragraph:** Contractor-specific 3-5 week onboarding runbook covering access, IP, paired-shadow, and day-30 review — does NOT reuse the FT employee onboarding-30-day template. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned playbook-step artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- agency onboard contractor під real-client engagement.
- access provisioning + IP коректно з day 0 (NDA, scope, deliverable IP).
- paired-shadow проходить, не «read the wiki».
- day-30 review з go/no-go рішенням, не extension by default.
- runbook є replicated для кожного нового contractor → масштаб.

## Applies If (ALL must hold)

- task is 'p5-micro-agency-founder/Hire and onboard a new contractor (3–5 weeks)' or close variant.
- operator has the artefacts named in Prerequisites available before starting.
- output will be consumed by a downstream agent or human reviewer.
- tier == pro or higher.

## Skip If (ANY kills it)

- team already maintains a working onboarding runbook — replace, do not duplicate.
- single-use throwaway engagement — overhead is not justified.
- regulatory / compliance context overrides any in-methodology guidance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the playbook-step artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/contractor-onboarding-runbook.md` | Working playbook-step skeleton with 5-line header |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contractor-onboarding-runbook.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[contractor-audition-flow]]
- [[graceful-offboard-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
