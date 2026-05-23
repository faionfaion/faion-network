---
slug: requirements-lifecycle
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a lifecycle policy declaring states (draft / reviewed / approved / implemented / verified / retired), transitions, owners, and SLAs per requirement.
content_id: "9152c6c20988be18"
complexity: medium
produces: spec
est_tokens: 4300
tags: [ba, lifecycle, requirements, workflow, governance]
---
# Requirements Lifecycle

## Summary

**One-sentence:** Produces a lifecycle policy declaring states (draft / reviewed / approved / implemented / verified / retired), transitions, owners, and SLAs per requirement.

**One-paragraph:** Produces a lifecycle policy declaring states (draft / reviewed / approved / implemented / verified / retired), transitions, owners, and SLAs per requirement. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Large requirement-set (>20), де ad-hoc tracking занепадає.
- Multiple-owner context: BA пише, dev імплементує, QA verify'ить — потрібна явна state-машина.
- Compliance (ISO/SOC2/HIPAA), де треба timestamped transitions.
- Cross-team initiative, де 'чи це done?' постійно дискутується.

## Applies If (ALL must hold)

- Requirements set is large enough (>20) that ad-hoc state tracking decays.
- Multiple owners touch the same requirement across release cycles.
- Compliance requires explicit state transitions with timestamps.
- Cross-team initiative where 'is this requirement done?' is contested.

## Skip If (ANY kills it)

- Backlog is small (≤10 requirements) where status field is sufficient.
- Continuous-discovery product where requirements churn faster than transitions can be tracked.
- Pure agile context where requirements live as user stories with Jira workflow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements register | Output of requirements-documentation | BA |
| Tooling decision (Jira / Confluence / GitHub) | ADR | PMO |
| Approver roster | Output of ba-planning T3 | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ba-requirements-mgmt]] | lifecycle is the workflow inside the management framework |
| [[requirements-traceability]] | lifecycle state feeds traceability columns |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-states` | haiku | Mechanical listing of states + transitions. |
| `assign-owners-slas` | sonnet | Match states to owners + SLAs against approver roster. |
| `write-policy` | sonnet | Synthesise policy document. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lifecycle-policy.md` | Lifecycle policy document skeleton. |
| `templates/state-transition-matrix.md` | Matrix of allowed transitions per state. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-lifecycle.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[ba-requirements-mgmt]]
- [[requirements-traceability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
