# AWS Well-Architected Framework

## Summary

**One-sentence:** Quarterly Well-Architected review report: six pillars (Op Excellence, Security, Reliability, Performance, Cost, Sustainability) with finding-per-question, named owner per finding, remediation plan with due date.

**One-paragraph:** Quarterly Well-Architected review report: six pillars (Op Excellence, Security, Reliability, Performance, Cost, Sustainability) with finding-per-question, named owner per finding, remediation plan with due date. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Production AWS workload exists with paying users / internal SLAs.
- Quarterly review cadence is required or chosen.
- Named architect can lead the review + assign per-finding owners.

## Skip If (ANY kills it)

- Pre-revenue prototype with no SLA.
- Workload reviewed within last 90 days with no major changes since.
- Team uses a different framework (e.g. Azure WAF, GCP architecture review) for the same workload.

**Ефективно для:**

- Команди з production AWS workloads що мають проходити review (для customer audit, SOC2, AWS Partner).
- Quarterly cadence reviews per workload з named owner.
- Pre-launch архітектурні reviews для критичних запусків.
- Use of AWS Well-Architected Tool для structured assessment.

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
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
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
| `scripts/validate-aws-well-architected-framework.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
