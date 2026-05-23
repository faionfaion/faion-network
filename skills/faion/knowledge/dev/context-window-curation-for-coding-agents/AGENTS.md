# Context Window Curation for Coding Agents

## Summary

**One-sentence:** Curates a per-task context bundle for a coding agent (Claude Code / Cursor) — ≤6K tokens of relevant code + glossary — replacing 50K-token blind dumps with deterministic, minimal context.

**One-paragraph:** AI-pair coding fails when the agent loads 50K tokens of irrelevant code: latency rises, the model anchors on noise, edits drift. The fix is per-task context curation: identify the change area, pick the minimum files needed (target + 1-2 callers + relevant types + AGENTS.md), add a 200-token glossary of project-specific terms, and budget the total to ≤6K tokens. This methodology emits a bundle artefact: list of files + tokens-per-file, glossary excerpt, and the "what's deliberately excluded" record so the reviewer can spot missing context. Output: a curated bundle the agent loads instead of letting it crawl.

**Ефективно для:**

- Solo dev pair-coding with Claude Code / Cursor on a multi-file change.
- Outsource lead bounding an AI agent's context to keep edits focused.
- AI-context cost optimisation: ~2K tokens of relevant context, not 50K-token context dumps.
- Onboarding a new LLM model — the curated bundle is the model's first read.

## Applies If (ALL must hold)

- Task is bounded (one feature, one bug, one refactor) — not "improve the codebase".
- Coding agent (Claude Code, Cursor, Copilot Chat) is the executor.
- Repo has AGENTS.md / CONVENTIONS.md OR they will be authored in the same session.
- Token budget is constrained (cost or context-window pressure).

## Skip If (ANY kills it)

- Task is exploratory ("understand this codebase") — full crawl is the goal, not curation.
- Repo is &lt; 5K total lines — load it all.
- Coding agent has no token concern (unlimited model + cost-neutral).
- Task is purely codemod / deterministic transform — the agent doesn't need context, the codemod does.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task description | text | tracker |
| Repo file map | tree | `find . -name '*.py'` |
| AGENTS.md / CONVENTIONS.md | Markdown | repo |
| Project glossary | Markdown | repo or to-be-authored |
| Token budget | number | team handbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/code-quality/framework-decomposition-patterns` | Bounded files = bounded context; sibling. |
| `solo/dev/code-quality/ai-code-review-checklist` | Downstream review of the agent's output. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ rules: minimum-files, glossary, budget cap, exclusion-record, AGENTS.md first, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the bundle artefact + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: bulk-dump, no-glossary, missing-exclusions, AGENTS.md-skipped | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: scope → pick-files → glossary → budget-check → emit-bundle | 700 |
| `content/06-decision-tree.xml` | essential | Tree: scope clear? files identified? budget met? → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-change-area` | sonnet | Parse task + repo layout → target file(s). |
| `pick-callers` | sonnet | Walk imports / refs; pick 1-2 highest-coupling callers. |
| `budget-check` | haiku | Mechanical: token-count each file, sum, compare to cap. |

## Templates

| File | Purpose |
|------|---------|
| `templates/context-window-curation-for-coding-agents.json` | JSON Schema for the bundle artefact. |
| `templates/glossary-snippet.md` | 200-token project-glossary template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-context-window-curation-for-coding-agents.py` | Validate bundle JSON against schema + budget rule. | Before handing bundle to the agent. |

## Related

- [[code-quality/framework-decomposition-patterns]] — bounded files → bounded context.
- [[changelog-automation-conventional-commits]] — small commits keep change area small.
- [[code-quality/ai-code-review-checklist]] — review output of an agent given this context.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks scope clarity (one feature / bug / refactor — not "improve everything"). It then verifies AGENTS.md is in the bundle, target file is included, ≤2 callers picked, glossary present, total ≤ budget. Leaves emit `commit-bundle`, `block-no-scope`, `block-over-budget`, or `block-no-agents-md`. Each leaf references a rule in `01-core-rules.xml`.
