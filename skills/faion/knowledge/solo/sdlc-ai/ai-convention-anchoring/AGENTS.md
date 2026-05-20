---
slug: ai-convention-anchoring
tier: solo
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Three-layer anchoring (CONVENTIONS.md + CLAUDE.md/AGENTS.md context pyramid + lint gates) that stops AI from generating compilable code that silently violates the team's conventions.
content_id: 614edf42898839e6
---

# AI Convention Anchoring

## Summary

The recurring failure mode across global dev flows is AI generating code that compiles, passes tests, looks plausible — and silently breaks the team's conventions (file layout, naming, error handling, logging, lint rules, framework idioms). One-shot prompt rules don't survive a 100k-token context window. This methodology anchors the agent with a three-layer pyramid: a human-curated `CONVENTIONS.md` at the repo root, per-module `AGENTS.md` files that hand specific context to the agent on load, and lint/format gates that mechanically reject convention violations before commit. The three layers together force "compiles" to coincide with "conforms".

## Applies If

- The codebase has at least one convention not enforced by language defaults (custom file layout, naming, error pattern, log schema, lint config).
- The team uses an agentic coding tool (Claude Code, Cursor, Continue, Copilot Workspace) that respects in-repo context files.
- A lint or format toolchain exists and runs in pre-commit or CI.
- New code volume is high enough that one-shot review of every diff is not sustainable.

## Skip If

- The codebase has no conventions worth enforcing — write them first, then anchor.
- The agent ignores in-repo context files (raw API call without context loader) — fix the integration before anchoring.

## Content
See `content/01-core-rules.xml`.

## Related
- [[ai-agent-guardrails-pack]]
- [[agents-md-per-module-bootstrap]]
- [[context-window-curation-for-coding-agents]]
- [[bug-pattern-to-lint-rule-conversion]]
