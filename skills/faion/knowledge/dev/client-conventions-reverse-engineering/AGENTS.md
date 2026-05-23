# Client Conventions Reverse Engineering

## Summary

**One-sentence:** Produces a single AGENTS.md / repo-rules.md guardrail file extracted from a client's lint config, naming, branching, dependency, and structural conventions so an AI coding agent stops producing convention-violating PRs.

**One-paragraph:** P4-outsource developers face AI-pain: a coding agent produces functionally correct code that violates the client's conventions, drowning the actual change in style noise. This methodology reverses the dynamic — extract conventions FIRST (lint/formatter, naming, branching, dependency policy, layering rules, test placement), encode them in a single guardrail file (AGENTS.md / repo-rules.md / CLAUDE.md style), and feed it into the agent's prompt or system context.

**Ефективно для:**

- P4-outsource dev із Claude Code/Cursor/Copilot на чужій codebase.
- Стиль-diff топить change у PR — repo-rules.md прибирає шум.
- Lint config + naming + branching + dep policy — все в одному файлі.
- Re-run-able: артефакт versioned, оновлюється кожні N PR.

## Applies If (ALL must hold)

- Developer uses a coding agent on a client codebase they do not own.
- Client codebase is more than 3 months old (has accumulated conventions).
- At least one PR cycle was rejected due to convention violations.
- Read access to repo, lint configs, and recent merged PRs.

## Skip If (ANY kills it)

- Greenfield project where conventions are being authored as part of the work.
- Client provides a fully-written contributor guide and uses it consistently.
- Short engagement (< 5 PRs) where guardrail authoring exceeds payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Client repo read access | git | client |
| Lint/formatter configs | .eslintrc / pyproject.toml / etc. | client repo |
| Recent merged PR sample (>= 20) | diff history | client repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[software-developer]] | Operating context for the outsource developer role |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/05-examples.xml` | medium | One fully-worked example matching the output schema | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-lint-rules` | haiku | Mechanical capture of explicit lint/formatter configs. |
| `infer-implicit-conventions` | sonnet | Per-PR judgment on naming + structure + commit style. |
| `synthesize-guardrail-file` | sonnet | Compose AGENTS.md from explicit + implicit findings. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/repo-rules.md` | Guardrail Markdown skeleton with the canonical 6 sections. |
| `templates/repo-rules.schema.json` | JSON skeleton matching the output contract. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-conventions-reverse-engineering.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/validate-client-conventions-reverse-engineering.py` | Validator script. | after subagent returns, before downstream consumer reads |

## Related

- [[code-review-slo-and-rubric]]
- [[codemod-recipe-library]]

## Decision tree

See `content/06-decision-tree.xml`. Tree decides extraction-only vs extraction-plus-inference based on lint config completeness and PR sample availability.
