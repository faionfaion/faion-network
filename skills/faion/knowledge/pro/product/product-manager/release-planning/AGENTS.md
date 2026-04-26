# Release Planning

## Summary

Structured approach to bundling, scheduling, and communicating product releases across cross-functional teams. Defines what ships, when, to whom, and how readiness is verified per function (eng, docs, support, marketing, legal) before deploy.

## Why

Chaotic releases stem from missing a per-function readiness gate and a frozen manifest. The PM-flavored variant adds a release-readiness matrix (green/yellow/red per function with evidence URLs) on top of basic engineering deploy mechanics — decoupling "code is done" from "release is ready". Without an explicit readiness gate, one unverified cell ships and creates incidents or mis-sold features.

## When To Use

- Multi-team release crossing engineering, support, sales-enablement, marketing, and legal.
- Releases with paying customers where breaking changes or deprecations are present.
- Release calendar has slipped twice in a row (signal: shrink contents, shorten cycle).
- Regulated or contractual deploy windows require customer-facing change-control artifacts.
- Pre-launch GTM coordination where sales decks, support macros, and pricing copy must sequence.
- Release-train cadence reviews where the PM owns whether the train left full or empty.

## When NOT To Use

- Trunk-based / continuous deployment with feature flags at scale — use a launch plan tied to flag percentages instead.
- Pure infra/refactor with zero customer-visible behavior change.
- Solo founder shipping to fewer than 50 users — `git push` + changelog post is sufficient.
- A/B experiments — use `experimentation-design`, not a ship date.
- Hotfixes for live incidents — use the incident-response runbook; release-planning deliberation kills time-to-mitigate.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 6-step release process: goals, contents selection, readiness gate, comms plan, execution, post-release. |
| `content/02-readiness-matrix.xml` | Per-function readiness matrix rules, evidence-link requirement, agentic workflow (4 loops). |
| `content/03-antipatterns.xml` | Common failure modes: Friday shipping, train-the-monster, comms inflation, stale notes, rollback theater. |

## Templates

| File | Purpose |
|------|---------|
| `templates/release-plan.md` | Full release plan template: metadata, goals, contents, risks, rollback, comms timeline. |
| `templates/release-notes.md` | Customer-facing release notes template with required sections and anti-fluff rules. |
| `templates/release_readiness_lint.py` | Validates readiness matrix: green rows must have evidence URL, yellow/red must have named owner. |
| `templates/prompt-manifest-generation.txt` | LLM prompt for contents-freeze loop: reads tracker, validates DoD, emits manifest. |
| `templates/prompt-readiness-matrix.txt` | LLM prompt for cross-functional readiness gate with evidence-link requirement. |
| `templates/prompt-release-notes.txt` | LLM prompt for customer-facing notes with anti-fluff discipline and required sections. |
