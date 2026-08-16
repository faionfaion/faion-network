# Interface Analysis

## Summary

**One-sentence:** Per-interface specification pipeline (catalog → classify → specify → reconcile) producing the integration landscape: data elements, protocol, frequency, volume, security, error-handling per boundary.

**One-paragraph:** Identifies and documents all boundaries and connections between a solution and external systems, users, hardware, and communication channels, then specifies data elements, protocols, frequency, volume, security, and error handling for each. Output: a per-interface specification linked to the integration landscape register, ready for integration-test design and contract validation.

**Ефективно для:**

- System replacement, де список boundaries — це surface ризику.
- Enterprise integration ≥5 інтерфейсів зі змішаними protocols.
- Регульований handoff (PCI / HIPAA / GDPR) з документованою security per interface.
- Decommissioning: треба перерахувати всіх consumers перед shutdown.

## Applies If (ALL must hold)

- System replacement / migration where boundary list is the failure surface.
- Enterprise integration (ESB, iPaaS, event bus) with ≥5 interfaces.
- Regulated handoff (PCI, HIPAA, GDPR) requiring documented per-interface security.
- Vendor onboarding where SLA + protocol + error-handling must be contractual.
- Decommissioning where every consumer must be enumerated before shutdown.

## Skip If (ANY kills it)

- Single-codebase change with no external boundary.
- Pure UI/UX redesign with no backend contract change.
- Prototype / spike where boundaries are still volatile.
- Existing integration landscape register is authoritative and fresh — read it, do not re-author.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Solution scope | Markdown | BA / architect |
| Integration landscape register seed | JSON / Markdown | enterprise architecture |
| Protocol catalog | Markdown | API governance |
| Security policy | Markdown / PDF | compliance |
| Volume / frequency baseline | JSON | ops / monitoring |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/data-analysis` | Data elements per interface drive from the data dictionary. |
| `pro/ba/business-analyst/requirements-documentation` | Per-interface spec is a class of solution requirement. |

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
| `boundary-discovery` | sonnet | Trace boundaries from scope to external touchpoints. |
| `interface-classification` | haiku | Tag interface type: system | user | hardware | communication. |
| `spec-drafting` | sonnet | Compose the per-interface spec from templates. |
| `landscape-merge` | sonnet | Reconcile new specs into the integration register. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interface-catalog.md.j2` | Catalog index: id, name, type, owner, status. |
| `templates/interface-catalog.md` | Catalog index: id, name, type, owner, status. Generated from `templates/interface-catalog.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/interface-specification.md.j2` | Per-interface spec: data elements, protocol, frequency, volume, security, errors. |
| `templates/interface-specification.md` | Per-interface spec: data elements, protocol, frequency, volume, security, errors. Generated from `templates/interface-specification.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/landscape-merge.sh` | Merge new specs into the integration register with diff. |
| `templates/landscape-register.md.j2` | Top-level integration landscape register skeleton. |
| `templates/landscape-register.md` | Top-level integration landscape register skeleton. Generated from `templates/landscape-register.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in interface spec. |
| `templates/_smoke-test.md` | Minimum viable filled-in interface spec. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-interface-analysis.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[data-analysis]]
- [[requirements-documentation]]
- [[modern-ba-framework]]
- [[business-process-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/landscape-merge.sh`

```bash
set -euo pipefail

echo "[interface-analysis] skeleton helper — replace with real logic."

# Example: list candidate frameworks for the current KA.
KA="${1:-KA-1}"
echo "KA: $KA"
```
