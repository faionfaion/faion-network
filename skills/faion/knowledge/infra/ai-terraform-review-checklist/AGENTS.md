# AI Terraform Review Checklist

## Summary

**One-sentence:** Per-PR checklist that catches the 2026 AI-generated Dockerfile / Helm / Terraform failure patterns (USER 0, latest tag, missing resource limits, broken templating) before they reach production.

**One-paragraph:** Per-PR checklist that catches the 2026 AI-generated Dockerfile / Helm / Terraform failure patterns (USER 0, latest tag, missing resource limits, broken templating) before they reach production. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- AI assistant produces ≥ 1 Dockerfile / Helm chart / Terraform PR per week.
- Named SRE / DevOps reviewer owns each PR.
- Org policy already lists at least one forbidden pattern (e.g. USER 0, hardcoded namespaces).

## Skip If (ANY kills it)

- No AI assistant is producing IaC in this repo.
- Greenfield prototype with no production users.
- PRs are already gated by a stricter policy-as-code engine (OPA / Conftest) and adding a checklist duplicates effort.

**Ефективно для:**

- PR-гейт для AI-згенерованих Docker/Helm/Terraform змін.
- Команди де Claude/Cursor пишуть IaC, людина ревʼює.
- AI-output який потрібно зіставити з org-policy.
- Аудити після інцидентів через AI hallucinations в IaC.

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
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `apply-checklist` | haiku | Per-item binary check against artefact. |
| `classify-decision` | sonnet | Mitigated / accepted / deferred / N-A judgment. |
| `escalate-stride-conflict` | opus | Cross-category interaction analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Checklist with category headings + decision-per-prompt rows. |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-terraform-review-checklist.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[code-review-checklist]]
- [[sdd-document-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
