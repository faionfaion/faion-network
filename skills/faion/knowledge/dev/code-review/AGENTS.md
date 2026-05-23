# Code Review

## Summary

**One-sentence:** Produces a code-review pipeline: PR size limit (<400 lines), automated gates (lint/type/test/coverage green before review), agentic pre-review pass, and reviewer focus narrowed to correctness + design.

**One-paragraph:** Produces a code-review pipeline: PR size limit (<400 lines), automated gates (lint/type/test/coverage green before review), agentic pre-review pass, and reviewer focus narrowed to correctness + design. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- Repository hosts a CI pipeline that can post status checks (GitHub, GitLab, Bitbucket).
- The team has agreed on a PR size convention (< 400 lines default).
- Lint / type / test / coverage gates exist or are about to be added.
- Reviewers are humans, not just AI bots.

## Skip If (ANY kills it)

- Solo developer with no review reviewer available (use AI review only as a stopgap; not enough).
- Codebase auto-merges trusted bot PRs (dependency bumps); manual review not applicable.
- Repository is read-only (vendored library) — patches happen upstream.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output target path | string | constitution / SDD spec |
| Owner (role:person) | string | team roster |
| Trigger event | event/threshold/schedule | constitution |
| Evidence anchor (URL / ticket / commit) | string | upstream context |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/best-practices-2026` | Constitution rules reviewers enforce. |
| `free/dev/software-developer/code-coverage` | Coverage gate the review pipeline consumes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to code-review | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pre-review pass (lint/types/coverage/security) | sonnet | Mechanical gates, deterministic. |
| Reviewer-facing summary + risk callout | opus | Cross-file synthesis, design judgement. |
| Auto-suggest doc/test additions | sonnet | Templated. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-balance.sh` | Pre-commit guard: reject PRs over 400 lines unless labeled `large-pr-approved`. |
| `templates/pr-checks.yml` | Required GitHub Actions checks (lint, types, tests, coverage, oasdiff, security). |
| `templates/pr-description.md` | PR description template with risk / scope / test sections. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-review.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[best-practices-2026]] — see methodology AGENTS.md for context.
- [[code-coverage]] — see methodology AGENTS.md for context.
- [[api-testing]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.
