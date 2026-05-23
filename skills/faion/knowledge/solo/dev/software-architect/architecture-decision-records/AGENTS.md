---
slug: architecture-decision-records
tier: solo
group: architecture
domain: architecture
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Captures one architecturally significant decision per ADR with Context, Decision, Consequences, Alternatives. Lock format; CI-enforce; treat as first-class artefacts.
content_id: "115d2db9c2ade6a9"
complexity: medium
produces: decision-record
est_tokens: 3900
tags: [adr, architecture, decision-records, documentation, governance]
---
# Architecture Decision Records (ADRs)

## Summary

**One-sentence:** Captures one architecturally significant decision per ADR with Context, Decision, Consequences, Alternatives. Lock format; CI-enforce; treat as first-class artefacts.

**One-paragraph:** An ADR is a short document capturing one architecturally significant decision. Standard format (Nygard or MADR), locked in ADR-0001, enforced by CI. Output is an ADR file in `docs/adr/` plus an updated ADR index. Status fields (Proposed, Accepted, Deprecated, Superseded) demand periodic review; pair with `adr-staleness-audit` quarterly.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'architecture decision record' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- An architecturally significant decision is being made (technology, pattern, boundary).
- More than one option was considered.
- The decision will affect future work or be referenced by ≥2 people.

## Skip If (ANY kills it)

- Trivial implementation choice with no cross-cutting impact.
- Reversible-without-cost dev-tooling tweak.
- Same decision already documented in an existing ADR.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision context | problem statement | the deciding engineer |
| Alternatives explored | ≥2 options | design discussion |
| ADR-0001 (format lock) | ADR file | repo ADR folder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/adr-reversibility-tagging` | Optional pairing — tag reversibility on every ADR. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the ADR record + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: scope → alternatives → draft → review → merge | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-adr` | sonnet | Template-driven ADR composition. |
| `synthesize-alternatives` | sonnet | Generate rejected options + reasons. |
| `audit-adr-portfolio` | opus | Cross-ADR consistency and staleness audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-nygard.md` | Nygard-format ADR template (Title, Status, Context, Decision, Consequences). |
| `templates/adr-madr.md` | MADR-format ADR template (with Considered Options and Pros/Cons of the Decision). |
| `templates/adr-lint.sh` | CI lint script — filename/status/sections/superseded-ref checks across `docs/adr/`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-architecture-decision-records.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[adr-reversibility-tagging]]
- [[architect-pr-review-checklist]]
- [[decision-tree-architecture-style]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
