# Code Review

## Summary

Code review process covering PR size limits, review checklists, automated gate setup, and agentic review pipeline. Core rule: PRs must be <400 changed lines / <20 files; CI must be green before human review; style is delegated to formatters (Prettier, ruff, gofmt) — reviewers focus on correctness, design, tests, security, and observability.

## Why

Industry data (SmartBear, Cisco) shows defect detection drops sharply above 400 changed lines and 60-90 minutes of review time. Mixing style feedback with logic review wastes both reviewer and author time; automated formatters eliminate the category entirely. LLM-authored PRs need a second review (human or agent) because agents pattern-match well but produce hallucinated APIs and missed edge cases.

## When To Use

- All PRs in a multi-engineer team — cheapest defect-detection layer.
- Before merging LLM-authored PRs — agent code requires a second pass.
- Security-sensitive paths (auth, payment, IAM, crypto) — mandatory dual review.
- Libraries/SDKs where API surface is sticky and backward compatibility must be enforced.
- Onboarding ramps where junior code benefits from senior review + automated reviewer.

## When NOT To Use

- Trunk-based solo prototypes pre-MVP — review overhead outpaces signal.
- Mechanical refactors from a codemod with green CI + full test coverage on touched code — skim, don't deep-review.
- Vendored/generated code (proto stubs, OpenAPI clients) — review the generator config, not the output.
- Documentation typos — accept fast, don't gate.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | PR size limits, CI gate order, review checklist categories, CODEOWNERS routing. |
| `content/02-review-scenarios.xml` | Concrete examples: bug, design issue, security flaw, N+1 query, with suggested patches. |
| `content/03-agentic-pipeline.xml` | Layered pipeline: automated gate → summary agent → diff-reviewer agent → human. |
| `content/04-antipatterns.xml` | LGTM culture, bikeshedding, reviewer fatigue, agent false positives. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-description.md` | PR description template with type checklist and test evidence sections. |
| `templates/pr-checks.yml` | GitHub Actions workflow: lint, test, coverage, PR size warning. |
| `templates/pr-balance.sh` | Assigns least-loaded reviewer from CODEOWNERS via `gh` CLI. |
