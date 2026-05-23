---
slug: design-system-drift-audit
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design System Drift Audit delivers a concrete, testable methodology that turns the recurring task of 'Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance' into an auditable artefact, addressing the gap: AI-generated layouts and unsupervised PRs c
content_id: "15c29c88d1f4301f"
complexity: medium
produces: report
est_tokens: 4400
tags: [product, pro, audit, methodology]
---
# Design System Drift Audit

## Summary

**One-sentence:** Design System Drift Audit delivers a concrete, testable methodology that turns the recurring task of 'Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance' into an auditable artefact, addressing the gap: AI-generated layouts and unsupervised PRs cause silent drift between Figma library and prod. Need a recurring audit methodology (token diff, component-usage scan, hardcoded-value detector).

**One-paragraph:** AI-generated layouts and unsupervised PRs cause silent drift between Figma library and prod. Need a recurring audit methodology (token diff, component-usage scan, hardcoded-value detector). Design System Drift Audit closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance' (role-ux-ui-designer, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

**Ефективно для:**

- AI-generated layouts і unsupervised PRs ламають design-system token coherence.
- Storybook → Figma library → PR → governance потребує drift-detection routine.
- Дизайн-команда веде scheduled audit з ranked remediation backlog.

## Applies If (ALL must hold)

- The triggering activity 'Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance' (role: role-ux-ui-designer) is in your current workload at least once per cycle.
- You have authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the artefact — human reviewer OR downstream agent.
- An auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems / dashboards / docs that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design_system_drift_audit_template_fill` | haiku | Template fill, no judgment |
| `design_system_drift_audit_evidence_check` | sonnet | Bounded comparison + judgment |
| `design_system_drift_audit_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-system-drift-audit.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/design-system-drift-audit.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-design-system-drift-audit.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-system-drift-audit.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/product/` (see neighbouring methodologies)
- triggering activity: `role-ux-ui-designer/Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
