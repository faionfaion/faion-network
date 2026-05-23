---
slug: ai-generated-code-compliance-validation
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "7-step validation pass that a senior dev runs on AI-shipped diffs before opening a client PR \u2014 client coding-standard lint, compliance-posture check (SOC 2 / HIPAA / PCI / GDPR), license / SBOM diff, forbidden-API scan, secret + PII regex, per-finding PR-comment composition."
content_id: "610142e4a712197a"
complexity: medium
produces: report
est_tokens: 5000
tags: [sdlc-ai, pro, compliance, ai-codegen, license, forbidden-api, outsource]
---
# AI-Generated Code Compliance Validation

## Summary

**One-sentence:** 7-step validation pass that a senior dev runs on AI-shipped diffs before opening a client PR — client coding-standard lint, compliance-posture check (SOC 2 / HIPAA / PCI / GDPR), license / SBOM diff, forbidden-API scan, secret + PII regex, per-finding PR-comment composition.

**One-paragraph:** 7-step validation pass that a senior dev runs on AI-shipped diffs before opening a client PR — client coding-standard lint, compliance-posture check (SOC 2 / HIPAA / PCI / GDPR), license / SBOM diff, forbidden-API scan, secret + PII regex, per-finding PR-comment composition. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- A team is producing report for the topic 'AI-Generated Code Compliance Validation'.
- Output is reviewed by a named human on a published cadence.
- Inputs and constraints fit the rules in `content/01-core-rules.xml`.

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single doc, not a versioned artefact.
- Regulated context that mandates a different template — use the regulator's.
- No named owner is available — defer until ownership is resolved.

**Ефективно для:**

- Senior devs reviewing AI-shipped diffs before opening a client-side PR.
- Enforcing per-client coding standards (naming, log shape, error wrappers, retry policies).
- License / SBOM drift detection for AI-introduced dependencies (especially AGPL).
- Forbidden-API scans tied to client's compliance posture (HIPAA / PCI / SOC 2 / GDPR).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev` | Parent role context. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from header + section list. |
| `populate-evidence` | sonnet | Per-row evidence link + summary judgment. |
| `outcome-synthesis` | opus | Cross-cycle synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Report skeleton with frontmatter + sections + evidence anchors per row. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-generated-code-compliance-validation.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[client-conventions-reverse-engineering]]
- [[sec-secrets-defense-in-depth]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
