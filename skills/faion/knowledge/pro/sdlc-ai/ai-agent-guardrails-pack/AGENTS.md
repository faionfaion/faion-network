---
slug: ai-agent-guardrails-pack
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Reusable prompt + system-rule + lint-aligned scaffold pack that constrains Copilot, Claude, and Cursor to client conventions in regulated codebases (FinTech, HIPAA, multi-tenant SaaS).
content_id: 39858c8e7b23df5d
---

# AI Agent Guardrails Pack

## Summary

Outsource and agency teams ship into regulated codebases (FinTech, HIPAA, multi-tenant SaaS) where Copilot Business, Claude Code, and Cursor must obey client conventions: no PII echo, no secret paste, no cross-tenant context, lint parity, framework-version pin. This pack ships a set of prompt files, system rules, and lint-aligned scaffolds that compose at the client-repo level and survive across coding agents. The output is a portable `guardrails/` directory the client legal and security teams can review once and the dev team can keep updated, instead of re-litigating "is this safe for HIPAA?" per pull request.

## Applies If

- The client codebase is under FinTech, HIPAA, GDPR, PCI-DSS, SOC2, or equivalent regime, OR the contract explicitly enumerates AI-coding constraints.
- The team uses at least one of: GitHub Copilot Business, Claude Code, Cursor, Continue, or a comparable in-editor agent.
- The client has an existing lint/format stack (eslint, ruff, golangci-lint, etc.) the pack can align to.
- A named security or compliance reviewer exists who can sign off the pack contents.

## Skip If

- The codebase is greenfield with no client conventions yet — write the conventions first, then derive guardrails.
- The team uses only chat-based AI outside the IDE (no code completion, no agent edits) — guardrails-by-prompt are not enforceable there.

## Content
See `content/01-core-rules.xml`.

## Related
- [[ai-convention-anchoring]]
- [[ai-coding-agent-compliance-guardrails]]
- [[indirect-prompt-injection-defense]]
