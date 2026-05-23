---
slug: definition-of-done-template
tier: pro
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Per-artefact-type Definition of Done checklist (story / spike / bugfix / refactor / infra change) with binary done/not-done gates across tests, docs, runbook, telemetry, security, and PM signoff."
content_id: "9bf0ae068762f05e"
complexity: medium
produces: checklist
est_tokens: 4200
tags: ["dod", "checklist", "release-readiness", "sdd", "pro"]
---
# Definition of Done Template

## Summary

**One-sentence:** Per-artefact-type Definition of Done checklist (story / spike / bugfix / refactor / infra change) with binary done/not-done gates across tests, docs, runbook, telemetry, security, and PM signoff.

**One-paragraph:** DoR has wide template coverage; the sibling Definition-of-Done usually drifts as folklore. This methodology ships per-artefact-type DoD checklists (story, spike, bugfix, refactor, infra change) with binary gates: tests green, docs updated, runbook updated, telemetry added, security review passed (where applicable), PM signoff. Each checklist is keyed to the artefact-type and produces a per-story DoD record that downstream automation (release, audit, retro) can consume.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «definition of done template» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- the team commits work in trackable units (story, ticket, change request) of any sprint cadence.
- the team ships to production at least monthly OR has compliance gates that need DoD evidence.
- no current per-type DoD exists OR the existing one is verbal-only.

## Skip If (ANY kills it)

- research-only org where output is reports, not code ships.
- team < 3 people AND ships < weekly -- a verbal DoD is fine at that scale.
- the org already uses a stricter compliance regime (SOC 2 evidence ledger, ISO 27001) that subsumes DoD.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Definition of Done Template task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/sdd-planning/definition-of-ready-template` | sibling methodology: DoR gates entry into the sprint, DoD gates exit to production. |
| `pro/sdd/spike-protocol-template` | supplies the spike artefact-type DoD criteria. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
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
| `templates/dod-story.md` | Story DoD checklist with binary gates + per-gate signoff. |
| `templates/dod-spike.md` | Spike DoD checklist (question / evidence / next-action). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-definition-of-done-template.py` | Validate the checklist artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[definition-of-ready-template]]
- [[spike-protocol-template]]
- [[soc2-evidence-generator-cli]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
