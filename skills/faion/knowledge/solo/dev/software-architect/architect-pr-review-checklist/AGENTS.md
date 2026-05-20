---
slug: architect-pr-review-checklist
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Tier-appropriate PR review checklist for the architectural surface — distinct from generic peer code review; also serves as the solo dev's self-review checklist for AI-generated code.
content_id: "067ca0aab7729bf6"
tags: [dev, architecture, code-review, pr-review, ai-generated-code, self-review]
---

# Architect PR Review Checklist

## Summary

**One-sentence:** A 6-section review checklist scoped to architectural surface (boundaries, contracts, data flow, failure modes, performance budget, security posture) that an architect runs in 10-15 min instead of either over-reviewing every line or rubber-stamping the PR.

**One-paragraph:** Generic code-review checklists (free/code-quality) cover style, naming, test coverage. Architects need a different filter: does this PR honor the ADRs, stay within module boundaries, respect data-flow rules, leave failure-modes addressable, fit the perf budget, and maintain the security posture? Same checklist serves the solo SaaS builder doing self-review on AI-generated code — that mode is structurally identical to architect review (you're checking that the generator stayed within the system's invariants). Primary output: a per-PR architect-review record with annotated findings + a merge / changes-needed / escalate decision.

## Applies If (ALL must hold)

- repo has documented architectural decisions (ADRs) OR established module boundaries OR a constitution.md / design.md
- PR touches more than a trivial file (>= 1 file with logic, not just typo / version-bump)
- reviewer wears an architect hat (or is the solo author doing AI-self-review)
- a generic code-review process already exists (peer review for style / tests); architect review is layered on top

## Skip If (ANY kills it)

- PR is a strictly mechanical change (formatter run, dependency version-only bump with no behavior change) — peer review handles it
- repo has no architectural decisions documented yet — establish ADRs first (`solo/sdd/sdd/architecture-decision-records`)
- reviewer is going to do a line-by-line read regardless — checklist becomes overhead, not focus
- PR is a hotfix incident response — apply emergency-fix checklist instead (different scope)

## Prerequisites

- ADRs accessible from the repo (linked or co-located)
- module boundary definitions (visible in folder structure, imports, or explicit dependency rules)
- perf budget per critical path documented (if perf is a concern for the project)
- security posture documented (threat model, OWASP top 10 stance, data classification)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/architecture-decision-records` | Reviewer checks PR against ADRs; consume ADR format |
| `solo/sdd/sdd/code-review-cycle` | Generic code review runs in parallel; this methodology layers on top |
| `solo/dev/software-architect/module-boundaries` | Defines the boundary rules the reviewer enforces |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 6-section coverage, 15-min cap, escalate-not-stall, AI-generated-code-flagging, ADR-honoring | ~1000 |
| `content/02-output-contract.xml` | essential | Review record schema + escalation contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (rubber-stamp, scope-creep into style, AI-code-blindness, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pr_diff_classification` | haiku | Identify section relevance (boundaries / contracts / data flow / perf / security) |
| `adr_alignment_check` | sonnet | Match PR changes vs existing ADR claims |
| `failure_mode_audit` | sonnet | Walk the changed code paths for unhandled failure modes |
| `cross_module_synthesis` | opus | When PR spans modules — synthesis check across boundaries |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-record.json` | JSON Schema for one architect-review record per PR |
| `templates/ai-self-review-card.md` | Printable card the solo author uses when self-reviewing AI-generated code |
| `templates/escalation-template.md` | Format for escalating PR to broader architecture discussion |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/scope-pr.py` | Walks PR diff, classifies sections (boundary / contract / data flow / perf / security / style-only) | Before starting the architect review |
| `scripts/audit-review-quality.py` | Audits past reviews for rubber-stamp pattern (review duration too short / no findings recorded) | Quarterly |

## Related

- parent skill: `solo/dev/software-architect/`
- peer methodologies: `module-boundaries`, `architecture-decision-records`, `code-review-cycle`
- external: [The Pragmatic Programmer — Review Patterns](https://pragprog.com/) · [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/) · [Software Architecture: The Hard Parts (Richards / Ford)](https://www.oreilly.com/library/view/software-architecture-the/9781492086888/)
