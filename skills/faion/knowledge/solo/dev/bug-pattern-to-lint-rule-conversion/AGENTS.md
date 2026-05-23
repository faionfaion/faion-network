---
slug: bug-pattern-to-lint-rule-conversion
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a decision-record artefact converting a recurring bug pattern (3+ instances in 30 days) into a lint / static-check / test rule with a detector defined before the fix.
content_id: "2c770040f2a054bf"
complexity: medium
produces: decision-record
est_tokens: 3800
tags: [pre-commit, lint, static-analysis, bug-prevention, ruff, eslint, dev-loop]
---
# Bug Pattern to Lint Rule Conversion

## Summary

**One-sentence:** Turns a recurring bug pattern (≥3 instances in 30 days) into an automated lint / static / test rule with a detector defined before the fix; emits a versioned decision-record so future readers can audit the conversion.

**One-paragraph:** Every team accumulates the same five bugs over and over. Most teams react with "add it to the code review checklist", which is a non-detector — readers skim, agents skip. This methodology pins the conversion: collect the pattern (3+ instances within 30 days), name it, write the detector FIRST (ruff rule id, ESLint rule, custom regex, test name), wire the detector into the pre-commit hook, and only then propose the corrective action. Output is a decision-record artefact (pattern_id, detector, fix, owner, version, last_reviewed) checked into `decisions/`. The CI hook starts to bite immediately; the team stops re-finding the same bug.

**Ефективно для:**

- Solo dev / outsource lead noticing "we keep doing this" — ruff/ESLint already lints, what's missing is the rule-add habit.
- Post-mortem follow-through: every actionable post-mortem should produce at least one detector.
- Pre-commit hook tune-up — the team's hook is the artefact this methodology populates.
- AI code review feedback loop — when the AI catches the same shape repeatedly, codify it.

## Applies If (ALL must hold)

- The bug pattern has occurred ≥3 times in the past 30 days (or 5 times in 90 days).
- The codebase has a working lint / static / pre-commit infrastructure (ruff, ESLint, pre-commit hooks).
- A named owner can be assigned to maintain the rule.
- The detector can be expressed mechanically (regex, AST visitor, type-check, test name) — not just human review.

## Skip If (ANY kills it)

- The pattern is a one-off, not recurring.
- The detector requires runtime tracing — use observability + alerting instead.
- The rule would generate &gt;5% false-positive rate — refine the pattern first.
- The team has no lint infrastructure — bootstrap `ci-quality-gate-design` first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bug ticket cluster (3+ links) | URL list | tracker |
| Lint tool inventory | YAML / json | repo |
| Pre-commit config | YAML | `.pre-commit-config.yaml` |
| Owner email | string | tracker |
| Sample bad code + sample good code | code | tickets |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/ci-quality-gate-design` | The CI gate this rule plugs into. |
| `free/dev/bug-report-quality-rubric` | Upstream: incoming bug reports need the rubric so this methodology can cluster them. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: 3-instance threshold, detector-first, named owner, false-positive ceiling, versioned record, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision-record + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: checklist-not-detector, false-positive flood, no-owner, rule-bitrot | 800 |
| `content/04-procedure.xml` | medium | 5-step procedure: cluster → detector → wire → measure FP → record | 700 |
| `content/06-decision-tree.xml` | essential | Tree: recurrence count → detector available? → FP rate → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cluster-tickets` | haiku | Mechanical: group bug tickets by error class / file path. |
| `draft-detector` | sonnet | Coding task: regex / AST visitor / lint rule id. |
| `false-positive-scan` | haiku | Mechanical: run detector against last-90-days codebase, count fires that aren't bugs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bug-pattern-to-lint-rule-conversion.json` | JSON Schema for the decision-record artefact. |
| `templates/bug-pattern-to-lint-rule-conversion.md` | Markdown skeleton authors fill before wiring the rule. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bug-pattern-to-lint-rule-conversion.py` | Validate a decision-record JSON against schema + threshold rules. | After the record is drafted, before the rule is wired into pre-commit. |

## Related

- [[ci-quality-gate-design]] — the gate this rule joins.
- [[bug-report-quality-rubric]] — incoming triage upstream.
- [[characterization-test-recipes]] — bug → test (orthogonal complement to bug → lint).

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks recurrence (≥3 in 30 days OR ≥5 in 90 days). It then verifies a mechanical detector exists (rule id, regex, AST visitor) and that false-positive rate against historical code ≤ 5%. Leaves emit `record-and-wire`, `block-low-recurrence`, `block-no-detector`, or `block-fp-too-high`. Each leaf references a rule in `01-core-rules.xml`.
