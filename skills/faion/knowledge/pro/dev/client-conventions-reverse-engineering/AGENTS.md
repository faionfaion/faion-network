---
slug: client-conventions-reverse-engineering
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "750d7b16b19e21a0"
summary: Systematically extracts a client's lint rules, branching model, dependency policy, and naming conventions and packages them as guardrails for an AI coding agent so generated code stops violating local norms.
tags: [outsource, client-conventions, ai-agent-guardrails, codebase-onboarding, p4-outsource]
---
# Client Conventions Reverse Engineering

## Summary

**One-sentence:** Extracts the implicit rules of a client's codebase — lint config, branch model, dependency policy, naming and structural conventions — and packages them into an AI-agent guardrail file so generated code matches the local norm on the first commit.

**One-paragraph:** P4 outsource developers (Daria's archetype) face a recurring AI-pain: a coding agent produces functionally correct code that violates the client's conventions. The result is a PR full of style and structural diff noise that drowns the actual change. Most teams "just review more carefully" — which fails when the agent is making 50 PRs a week. This methodology reverses the dynamic: extract the conventions FIRST, encode them in a single guardrail document (AGENTS.md / repo-rules.md / CLAUDE.md style), and feed it into the agent's prompt or system context. Conventions covered: lint and formatter config, naming conventions for files/classes/functions, branching and commit-message style, dependency-update policy, layering rules (e.g., no DB calls from controllers), test placement. Output: a versioned guardrail file the agent reads on every task.

## Applies If (ALL must hold)

- Developer is using a coding agent (Claude Code, Cursor, Copilot, aider) on a client codebase they do not own.
- Client codebase is more than 3 months old (has accumulated conventions).
- At least one PR cycle has been rejected/heavily-revised due to convention violations.
- Read access to the repo, lint configs, and recent merged PRs.

## Skip If (ANY kills it)

- Greenfield project where conventions are still being established — set them, do not reverse them.
- Client explicitly forbids AI tools — methodology is moot.
- Client provides their own AI guardrail file — use theirs, do not produce a parallel one.
- &lt; 5 merged PRs in the repo's history — sample too small for pattern extraction.

## Prerequisites

- Repo cloned locally.
- Access to last 30 days of merged PRs.
- Lint/format configs identified (`.eslintrc`, `pyproject.toml`, `.editorconfig`, `Makefile`, etc.).
- A target guardrail file path chosen (typically AGENTS.md or .cursorrules or CLAUDE.md).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer/codebase-onboarding` | General onboarding (architecture map, build) — done first. |
| `geek/sdlc-ai/kb-agents-md-context-pyramid` | Format and structure of the guardrail file. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: lint-first, evidence-from-PRs, structural extraction, dependency policy, write-back loop | ~1000 |
| `content/02-output-contract.xml` | essential | guardrail file shape; required sections; per-rule citation | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: cargo-culting, stale conventions, invented rules | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-lint-config` | haiku | Mechanical: parse config files, list active rules |
| `infer-naming-convention` | sonnet | Pattern recognition across files |
| `infer-layering-rules` | opus | Cross-file dependency analysis, judgment-heavy |

## Templates

| File | Purpose |
|------|---------|
| `templates/client-guardrails.md` | Skeleton AGENTS-style file with every required section |
| `templates/extraction-worksheet.md` | Worksheet to fill while reading PRs |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/pr-pattern-mine.py` | Pulls last N PRs, surfaces common review comments and rejection reasons | Phase 1 |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodology: `codebase-onboarding`, `agents-md-context-pyramid` (geek)
- external: [Anthropic best practices: AGENTS.md / CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code) · [aider conventions docs](https://aider.chat/docs/usage/conventions.html)
