---
slug: trunk-based-dev-principles
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Emits a TBD-readiness checklist artefact scoring four principles (single trunk, small commits, releasable trunk, fast CI) with per-check fixes and a go/no-go verdict.
content_id: "df85cfb7c256085d"
complexity: medium
produces: checklist
est_tokens: 4000
tags: [trunk-based-development, branching-strategy, continuous-integration, devops, high-performance]
---
# Trunk-Based Development: Principles

## Summary

**One-sentence:** Scores a repo against the four trunk-based-development principles (single trunk, small frequent commits, always-releasable trunk, fast CI) and emits a go/no-go verdict with field-level fixes.

**One-paragraph:** Trunk-Based Development (TBD) is a source-control branching model where developers collaborate on a single branch — "main" / "trunk" — and resist long-lived feature branches. Small daily commits, automated gates, and feature flags make this safe. This methodology turns the principles into a deterministic checklist: each of the four pillars is scored, the repo gets a 0-100 total, and the verdict is `adopt`, `partial-adopt`, or `not-ready`. The verdict surfaces what is missing (CI under 10 min, feature-flag plumbing, max-branch-age policy, auto-revert on red trunk) so the gap can be closed before the team switches.

**Ефективно для:**

- Solo developer or outsource lead deciding whether their repo can adopt TBD safely.
- Tech lead pitching TBD adoption to a wider team; the checklist becomes the readiness evidence.
- AI-assisted dev workflow where small daily commits are the norm — verifies the surrounding gates exist.
- DORA-metrics improvement programme: TBD is the highest-leverage lever after test automation.

## Applies If (ALL must hold)

- Team or solo dev practicing CI/CD or wants to.
- Project has automated tests AND a CI pipeline (or commitment to build one).
- Feature-flag infrastructure exists or will exist before adoption.
- Releases happen at least weekly (or the team wants to move there).

## Skip If (ANY kills it)

- Weak test coverage and no plan to build it — TBD without tests = "trunk is always broken".
- No CI/CD pipeline and no roadmap for one.
- Regulatory compliance requiring branch isolation or per-branch audit trails (FDA, aviation).
- Open-source project with external contributors that need long review cycles.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo handle | URL | tracker |
| CI pipeline definition | YAML (.github/workflows/, .gitlab-ci.yml) | repo |
| Branching policy | Markdown | team handbook |
| Test coverage report | JSON / lcov | last CI run |
| Feature-flag inventory | YAML / JSON | flag service |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/trunk-based-feature-flags` | Companion: flag plumbing that makes "always-releasable trunk" feasible. |
| `solo/dev/ci-quality-gate-design` | The CI gates that enforce "trunk is releasable". |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules: single trunk, small commits, releasable trunk, CI under 10 min, run-the-checklist + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the readiness checklist + valid/invalid examples + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: ghost long-lived branches, CI > 10 min normalized, flag-less merge, auto-revert disabled | 700 |
| `content/04-procedure.xml` | medium | 5-step adoption procedure: assess → fix gates → pilot → ramp → cleanup policy | 700 |
| `content/06-decision-tree.xml` | essential | Routes per-principle pass/fail to verdict adopt / partial-adopt / not-ready | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-principles` | haiku | Mechanical: count branches > 2 days old, measure CI duration, check flag inventory. |
| `draft-fix-comment` | sonnet | Author-facing prose explaining missing gates. |
| `verdict-aggregate` | haiku | Sum & route per the decision tree. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trunk-based-dev-principles.json` | JSON Schema for the readiness checklist artefact. |
| `templates/branch-policy.md` | Markdown snippet for `BRANCHING.md`: max branch age, naming, merge rules. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trunk-based-dev-principles.py` | Validate a checklist JSON against the schema and consistency rules. | After scorer emits the checklist, before posting verdict back. |

## Related

- [[trunk-based-feature-flags]] — flag plumbing required for "trunk is releasable".
- [[changelog-automation-conventional-commits]] — small commits feed the changelog.
- [[ci-quality-gate-design]] — the gates that block red-trunk merges.

## Decision tree

See `content/06-decision-tree.xml`. The tree walks the four principles in order (single trunk → small commits → releasable trunk → fast CI). Any FAIL on the first two principles → verdict not-ready. FAIL only on principles 3 or 4 with a fix-plan → verdict partial-adopt. ALL PASS → adopt. Each leaf references a rule in `01-core-rules.xml`.
