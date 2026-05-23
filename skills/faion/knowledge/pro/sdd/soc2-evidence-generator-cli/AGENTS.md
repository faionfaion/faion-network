---
slug: soc2-evidence-generator-cli
tier: pro
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Faion `soc2 evidence` CLI subcommand + template pack that converts each merged PR into a signed JSON SOC 2 evidence stub (actor, diff hash, control IDs, approval link), so audit prep becomes a query rather than a hunt."
content_id: "4d9f5d0022e7cb25"
complexity: deep
produces: config
est_tokens: 4200
tags: ["soc2", "compliance", "cli", "evidence", "sdd", "pro"]
---
# SOC 2 Evidence Generator CLI

## Summary

**One-sentence:** Faion `soc2 evidence` CLI subcommand + template pack that converts each merged PR into a signed JSON SOC 2 evidence stub (actor, diff hash, control IDs, approval link), so audit prep becomes a query rather than a hunt.

**One-paragraph:** Compliance-grade delivery (FinTech, HIPAA, PCI) demands per-change evidence trails. Hand-curation by the developer drifts the moment urgency rises. This methodology defines the `faion soc2 evidence` CLI flow: at PR merge, a webhook (or pre-merge hook) extracts actor, diff hash, control labels, reviewer approvals, CI run IDs, and writes a signed JSON stub into the evidence store. The template pack covers the control-label vocabulary, the stub schema, the signing key policy, and the audit-time query interface. Output is one signed evidence stub per PR + a queryable evidence store an auditor can sample.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «soc 2 evidence generator cli» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- the product is in scope of SOC 2 (or PCI-DSS / HIPAA / ISO 27001 with equivalent evidence demands).
- PRs are the unit of change for production code AND infrastructure-as-code.
- a control vocabulary already exists (from an audit prep or a prior SOC 2 cycle).

## Skip If (ANY kills it)

- the product has no formal compliance regime AND no near-term SOC 2 plan.
- release model is direct-to-main without PRs -- evidence stubs cannot attach.
- an existing evidence platform (Drata, Vanta, Secureframe) already owns this surface.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the SOC 2 Evidence Generator CLI task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/definition-of-done-template` | DoD record is one of the inputs the stub references. |
| `pro/sdlc-ai/citation-contract-back-to-source` | supplies the citation pattern the stub uses to point back to the PR. |

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
| `templates/evidence-stub.json` | Signed stub schema with actor, diff hash, control labels, approval link. |
| `templates/soc2-cli.md` | CLI usage cheat-sheet: hook install + query commands. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-soc2-evidence-generator-cli.py` | Validate the config artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[definition-of-done-template]]
- [[client-conventions-as-code]]
- [[ip-sensitive-workflow-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
