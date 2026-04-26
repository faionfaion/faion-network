# Code Review

## Summary

A systematic examination of source code before merging, using five comment types — BLOCKING (bugs, security, standard violations), SUGGESTION (improvements), NITPICK (style), QUESTION (unclear intent), PRAISE (good code) — and six review categories: correctness, design, maintainability, testing, performance, security. Keep PRs under 400 lines; agent review quality drops sharply above that threshold.

## Why

Code review catches bugs before production, distributes knowledge across the team, and enforces standards. Reviews prevent rework that costs 5-10x more to fix post-merge than pre-merge. The structured comment taxonomy (BLOCKING vs SUGGESTION vs NITPICK) eliminates ambiguity about what the author must fix versus what is optional, which is the primary source of review friction in teams.

## When To Use

- All code changes before merging, with at least one human approval required.
- Security-sensitive change classes: auth, data access, file uploads, deserialization — run a dedicated security pass.
- Architectural changes requiring broader review.
- Large refactors where reviewers lack bandwidth for line-by-line scan; agent flags hotspots for human attention.
- Consistency enforcement: PR style, naming, test coverage thresholds.

## When NOT To Use

- Non-code reviews (design docs, RFCs, copy edits) — use a doc-review workflow instead.
- Hotfixes during active incidents where speed outweighs review depth.
- Closed-source third-party SDK code where source cannot be loaded.
- One-line dependency bumps — Renovate/Dependabot plus automated tests is sufficient.
- Subjective architecture debates without team context — agent will pick a side arbitrarily.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Five core principles, comment type taxonomy with blocking rules, six review categories with checks per category. |
| `content/02-antipatterns.xml` | Agent failure modes: hallucinated APIs, diff truncation, phantom security warnings, style noise drowning design issues. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-review.yml` | GitHub Actions workflow: pre-flight secret scan, agent review on PR open/sync, post comment back to PR. |
