# Requirements Validation and Sign-Off

## Summary

**One-sentence:** Four-stage validation pipeline (correctness check → completeness check → technique match → segmented review) producing a sign-off pack with quality scores, dissent log, and explicit gate before baseline.

**One-paragraph:** A four-stage process that confirms requirements build the right thing (not that they are built right): (1) per-requirement quality attribute check (atomic, complete, consistent, correct, feasible, modifiable, prioritized, testable, traceable, unambiguous); (2) match technique to requirement type; (3) segmented review (functional area chunks of ≤200 requirements); (4) explicit sign-off gate before baseline.

**Ефективно для:**

- Pre-baseline gate для будь-якого requirement pack.
- Регульований domain з validation evidence.
- Outsourced delivery з contractual sign-off.
- Spec handoff до vendor / implementation team.

## Applies If (ALL must hold)

- Pre-baseline gate for any requirement pack.
- Regulated domain requiring documented validation evidence.
- Outsourced delivery requiring contractual sign-off.
- Spec hand-off to vendor or implementation team.
- Migration: validate every legacy behaviour mapped to new requirement.

## Skip If (ANY kills it)

- Single-person agile team using story-as-contract.
- Hot fixes.
- Pre-elicitation phase.
- Pre-baseline already approved by alternative process.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Requirements pack | Markdown / YAML | requirements-documentation |
| Quality attribute checklist | Markdown | this methodology |
| Stakeholder review group | JSON | governance |
| Review technique catalog | Markdown | templates/ |
| Sign-off template | PDF / Markdown | governance |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/requirements-documentation` | Source pack. |
| `pro/ba/business-analyst/requirements-traceability` | RTM consumes the validated baseline. |
| `pro/ba/business-analyst/requirements-lifecycle` | State transitions to Verified gated by this. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `quality-attribute-scoring` | sonnet | Per-requirement 10-attribute score. |
| `technique-matching` | haiku | Pick walkthrough / inspection / prototype review. |
| `segmented-review-orchestration` | sonnet | Chunk into functional areas ≤200 reqs. |
| `sign-off-pack-compose` | sonnet | Compose sign-off pack with scores + dissent. |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-checklist.md.j2` | 10-attribute review checklist. |
| `templates/review-checklist.md` | 10-attribute review checklist. Generated from `templates/review-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/session-agenda.md.j2` | Segmented review session agenda. |
| `templates/session-agenda.md` | Segmented review session agenda. Generated from `templates/session-agenda.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/sign-off-form.md.j2` | Sign-off form with dissent block. |
| `templates/sign-off-form.md` | Sign-off form with dissent block. Generated from `templates/sign-off-form.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/req-validate.sh` | Run validation pipeline locally. |
| `templates/_smoke-test.md.j2` | Minimum filled-in sign-off pack. |
| `templates/_smoke-test.md` | Minimum filled-in sign-off pack. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-validation.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[requirements-documentation]]
- [[requirements-traceability]]
- [[requirements-lifecycle]]
- [[decision-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/req-validate.sh`

```bash
set -euo pipefail

echo "[requirements-validation] skeleton helper — replace with real logic."

# Example: list candidate frameworks for the current KA.
KA="${1:-KA-1}"
echo "KA: $KA"
```
