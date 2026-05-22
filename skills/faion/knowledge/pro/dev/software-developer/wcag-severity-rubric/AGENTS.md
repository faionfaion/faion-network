---
slug: wcag-severity-rubric
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "1353ca83c993209e"
summary: Triage rubric for accessibility audit findings into blocker / serious / moderate / minor with assistive-tech, WCAG level, and user-journey criteria.
tags: [accessibility, a11y, wcag, severity, triage, audit, rubric]
---
# WCAG Severity Triage Rubric

## Summary

**One-sentence:** Triage rubric for accessibility audit findings into blocker / serious / moderate / minor with assistive-tech, WCAG level, and user-journey criteria.

**One-paragraph:** Accessibility audits surface 30-300 findings; without a shared severity rubric every finding becomes "p1" and the backlog stalls. Mechanism: each finding is scored on 3 axes — (a) WCAG conformance level (A / AA / AAA), (b) user impact (blocks task vs. degrades vs. annoyance), (c) assistive-tech population affected (screen reader, keyboard-only, low vision, cognitive). The cross-product collapses to a 4-tier severity (blocker / serious / moderate / minor), each with an SLA. Aligns Deque / WebAIM / axe-core severity definitions so a designer, dev, and QA all triage the same way. Primary output: triaged audit report ready for sprint planning.

## Applies If (ALL must hold)

- an a11y audit (manual or automated) has produced raw findings without severity
- the product targets WCAG 2.1 AA or higher conformance
- multiple roles (PM, dev, designer, QA) will touch the backlog — triage must be reproducible
- you have a fix-effort estimate column or can produce one per finding

## Skip If (ANY kills it)

- single finding or &lt; 5 findings — just fix them
- product targets only screen-reader users (specialist tool) — use a deeper population-weighted rubric
- regulatory-driven (ADA Title II 2026, EAA 2025) — the legal threshold replaces this rubric for "must fix"
- VPAT writeup — severity-by-tier is a different lens; use `regulatory-compliance-2026`
- AAA-targeted product (gov, healthcare) — all findings are blocker by definition

## Prerequisites (must be true before starting)

- raw audit findings with: WCAG SC reference, location (page + selector), reproduction steps
- the product's WCAG target level (AA is standard)
- the target population breakdown (estimate %screen-reader, %keyboard-only, %low-vision, %cognitive)
- a fix-effort scale (1-5 or t-shirt sizes)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/accessibility-specialist/wcag-22-compliance` | Source of SC mapping used by the rubric |
| `pro/ux/accessibility-specialist/a11y-testing` | Source of reproduction steps and AT validation |
| `pro/ux/ux-ui-designer/a11y-annotation-pattern-library` | Used during fix design to prevent re-occurrence |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 3-axis scoring, blocker = task-block, AT-population gate, SLA per tier, sample-validate triage | ~900 |
| `content/02-output-contract.xml` | essential | Triaged finding schema, severity-distribution report, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (everything-p1, AT-erasure, fix-effort confound, automated-only, stale rubric, regression backlog) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_finding_severity_score` | sonnet | Bounded 3-axis scoring with deterministic outputs |
| `audit_summary_report` | sonnet | Roll-up of severity distribution + critical-journey impact |
| `cross-finding_dedup` | opus | Detect that 15 findings share a root cause (e.g., a single missing alt-text pattern) |
| `sla_assignment_per_finding` | haiku | Template fill: severity → SLA window from a table |

## Templates

| File | Purpose |
|------|---------|
| `templates/triaged-finding.json` | Per-finding schema with severity, axes scores, SLA |
| `templates/severity-distribution-report.md` | Audit roll-up table for stakeholder review |
| `templates/sla-table.md` | Severity → fix-by date and gating policy |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/triage-findings.py` | Apply rubric to raw axe-core / WAVE / Lighthouse output | Right after raw audit |
| `scripts/cluster-by-root-cause.py` | Group findings by likely shared root cause | After triage, before sprint planning |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodologies: `wcag-22-compliance`, `a11y-testing`, `a11y-annotation-pattern-library`
- external: [Deque - axe-core impact](https://docs.deque.com/axe/4.0/devtools-extension/#impact) · [WebAIM Million](https://webaim.org/projects/million/) · [W3C - WCAG Conformance Levels](https://www.w3.org/WAI/WCAG21/Understanding/conformance.html)
