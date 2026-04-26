# Graph-Indexed vs Diff-Only AI Reviewers

## Summary

Two architectures of AI code reviewers co-exist and behave differently. **Diff-only** reviewers (Sourcery, GitHub Copilot Code Review, Codeball) read the patch plus its nearest neighbours — fast, cheap, blind to cross-file impact. **Graph-indexed** reviewers (Greptile, CodeRabbit Pro, Qodo Merge 2.0 multi-agent) build a repo-wide knowledge graph and trace ripple effects — slower, expensive, catch cross-module breakage that the diff-only class misses entirely. Pick diff-only for monorepos with strong module isolation and <100k LOC; pick graph-indexed for legacy/polyglot codebases >500k LOC where one rename quietly breaks five callers.

## Why

Defaulting to "whatever the marketing page suggests" produces predictable failure: graph-indexed reviewers on a green-field 30k-LOC service slow PRs by minutes for negligible find rate, and diff-only reviewers on a 1M-LOC legacy monolith ship patches that break a downstream consumer in another package. The architecture choice is the dominant cost-vs-coverage knob; the rule below is a decision tree against measurable repo properties (LOC, module isolation, polyglot count, latency target) instead of vendor preference.

## When To Use

- Selecting an AI reviewer for a new repo or migrating from a basic comment bot.
- Re-evaluating after a repo crosses a size or polyglot threshold (e.g. acquisition, framework migration).
- Auditing an existing reviewer that "feels noisy" or "missed an obvious break" — usually wrong architecture.
- Cost-control reviews where the reviewer line item exceeds the budget for actual incident-prevention value.

## When NOT To Use

- One-off open-source contribution flow where the maintainer reads every PR manually anyway.
- Repos with strict zero-third-party-app policy on source — pick a self-hosted PR-Agent variant or skip entirely.
- Tiny PR pipelines (<5 PRs/day) — the per-PR cost difference is negligible; pick on UX, not architecture.

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture-decision.xml` | Diff-only vs graph-indexed: properties, costs, decision tree. |
| `content/02-reviewer-matrix.xml` | Concrete vendor mapping (Greptile, CodeRabbit, Sourcery, Copilot Review, Codeball, Qodo). |

## Templates

| File | Purpose |
|------|---------|
| `templates/reviewer-decision.yml` | Repo-property checklist that picks diff-only vs graph-indexed. |
