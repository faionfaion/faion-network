# IaC Pull-Request Review Checklist

## Summary

**One-sentence:** Reviewer checklist for IaC / Helm / GitHub-Actions pull requests covering blast radius, IAM, state safety, secrets and rollback procedure.

**One-paragraph:** Reviewer checklist for IaC / Helm / GitHub-Actions pull requests covering blast radius, IAM, state safety, secrets and rollback procedure. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `checklist` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-iac-pr-review-checklist.py` before publication.

**Ефективно для:**

- Code review Terraform / Helm / GHA PR.
- Перевірка blast radius перед apply.
- Контроль IAM-змін у great-blast-radius PR.

## Applies If (ALL must hold)

- Input matches the methodology scope (iac-pr-review-checklist) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `checklist` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Diff scope | list of changed files + their modules | PR author |
| Plan output | terraform plan or helm diff result | PR author |
| Blast radius map | module → impacted environments | ownership matrix |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[github-actions-cicd]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-checklist-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/checklist.md` | Checklist skeleton with id / rule / MUST/SHOULD / evidence columns |
| `templates/_smoke-test.md` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-iac-pr-review-checklist.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[github-actions-cicd]]
- [[helm-charts]]
- [[image-digest-pinning-policy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `blast-radius-named` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
