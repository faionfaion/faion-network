---
slug: vdi-vs-byod-decision-matrix
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: VDI vs BYOD decision matrix: scored decision record picking between virtual desktop infrastructure and bring-your-own-device per client engagement using data-class, residency, audit, and cost axes.
content_id: "ee2e651c0c6c9afc"
complexity: medium
produces: decision-record
est_tokens: 4500
tags: [infra, pro, vdi, byod, decision-matrix, outsource]
---
# VDI vs BYOD Decision Matrix

## Summary

**One-sentence:** VDI vs BYOD decision matrix: scored decision record picking between virtual desktop infrastructure and bring-your-own-device per client engagement using data-class, residency, audit, and cost axes.

**One-paragraph:** VDI vs BYOD Decision Matrix pins the discipline that turns VDI vs BYOD from tribal knowledge into a reviewable, owned, version-controlled operating artefact. The methodology constrains input shape, output shape, evidence anchors, and named ownership; the JSON Schema in 02-output-contract drives a stdlib validator at commit time. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without a named owner are tagged stale.

## Applies If (ALL must hold)

- The team operates the system the methodology targets (`vdi-vs-byod-decision-matrix` scope).
- A named human owner is available to sign the artefact.
- The artefact lives in a version-controlled or wiki-style space with diff history.
- Tier ≥ pro (gated by tier-manifest).

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single doc, not a versioned artefact.
- A regulator mandates a different shape — use the regulator's template.
- No named owner is available — anonymous artefacts rot; defer until ownership resolved.

**Ефективно для:**

- Команд, де VDI vs BYOD жив досі у головах SRE / DevOps, а не в репозиторії.
- Регулярного quarterly review зі стабільним owner і review cadence.
- Audit-ready артефактів під SOC2 / ISO27001 / GDPR без паніки за тиждень до аудиту.
- Onboarding нових інженерів — артефакт замість усної традиції.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo or wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | Parent role skill — operating context for this methodology. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in SDD space. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source; includes skip-this-methodology guard | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: pick correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/vdi-vs-byod-decision-matrix.md` | Working skeleton for the `vdi-vs-byod-decision-matrix` artefact with required fields and `not_applicable: <reason>` markers per row. |
| `templates/_smoke-test.md` | Minimum viable filled artefact used by the validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vdi-vs-byod-decision-matrix.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only; supports `--help` and `--self-test`. | CI on artefact change; pre-commit. |

## Related

- [[capacity-safety-floor-policy]]
- [[prr-checklist-canonical]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, owner presence, trigger naming, evidence presence) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
