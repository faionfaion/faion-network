---
slug: ai-agent-perimeter-policy
tier: pro
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c824f672438e45b5"
summary: Translates client NDA/MSA clauses on data residency and confidentiality into per-engagement AI-agent guardrails (no embeddings of client code, no logs to provider X, no MCP servers from list Y).
tags: [security, compliance, ai-agent, perimeter, outsource, nda, msa, data-residency, mcp]
---
# AI-Agent Perimeter Policy

## Summary

**One-sentence:** Translates client NDA/MSA clauses on data residency and confidentiality into per-engagement AI-agent guardrails (no embeddings of client code, no logs to provider X, no MCP servers from list Y).

**One-paragraph:** Outsource specialists / consultants signing client NDAs and MSAs face an invisible compliance gap: their AI coding agents (Claude Code, Cursor, Codex, Copilot, MCP-extended tools) may send client code to embedding providers, store traces in third-party logs, or call MCP servers the client never approved. Mechanism: per-engagement, extract data-handling clauses from NDA/MSA → produce a perimeter policy document → configure dev environment to enforce (env var defaults, allowed-tools lists, MCP allow-list, retention overrides, telemetry off-switches) → audit weekly. Output: a signed perimeter-policy doc + dev environment that respects it.

## Applies If (ALL must hold)

- you do client engineering work under an NDA / MSA
- you use AI coding agents (Claude Code, Cursor, Codex, GitHub Copilot, aider, Windsurf) on client code
- the NDA / MSA has data-handling clauses (residency, no third-party sharing, "all derivative work confidential")
- you have the ability to configure your dev environment (allow-list tools, env vars, MCP)
- the client expects or implies that AI tools are used (or has explicitly mentioned them)

## Skip If (ANY kills it)

- no NDA / no MSA — use a default-conservative perimeter (still applies general rules)
- client has explicitly approved a specific AI toolchain (then their approved spec is the policy)
- you're using only locally-hosted models with air-gapped infrastructure — perimeter is implicit
- you can't configure your tools (you're using a managed dev environment) — escalate to client

## Prerequisites (must be true before starting)

- copy of the client NDA + MSA (read it; don't summarize from memory)
- list of AI tools you use + their data-handling defaults (Claude Code, Cursor, etc. each have docs)
- list of MCP servers you have configured globally + which ones touch network / cloud
- env-var control surface (Claude Code allowed-tools list, Cursor privacy mode, GH Copilot enterprise settings)
- telemetry / logs / traces settings per tool

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/security-architecture` | General security principles the perimeter applies |
| `geek/sdlc-ai/sec-secrets-defense-in-depth` | Secrets handling within agent contexts |
| `geek/sdlc-ai/gov-license-compliance-scan` | License-compliance scanning for code agents emit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: clause-to-config mapping, no-default-trust, kill-switch tools, weekly audit, written escalation | ~900 |
| `content/02-output-contract.xml` | essential | Policy doc schema, dev environment config schema, forbidden patterns | ~750 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (silent embedding, telemetry leak, MCP sprawl, model-card oversight, log retention default, hand-wave compliance) | ~950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_clauses_from_nda_msa` | sonnet | Per-document parsing of data-handling clauses |
| `map_clause_to_tool_config` | opus | Cross-tool reasoning: NDA "no third-party processing" → which knobs on which tools |
| `audit_dev_environment_compliance` | sonnet | Verify env / config matches policy |
| `weekly_perimeter_drift_check` | haiku | Scan: did anyone add a new MCP / change a setting |

## Templates

| File | Purpose |
|------|---------|
| `templates/perimeter-policy.md` | Per-engagement policy doc with tool-by-tool configuration |
| `templates/clause-to-config-mapping.md` | NDA clause → tool config translation table |
| `templates/dev-environment-config.md` | Engagement-specific env vars, allow-lists, MCP allow-list |
| `templates/weekly-audit-checklist.md` | 10-min weekly compliance check |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/extract-nda-clauses.py` | Parse NDA/MSA for data-handling language | Engagement setup |
| `scripts/audit-tool-config.py` | Verify Claude Code allow-list + MCP list + Cursor privacy mode match policy | Weekly |
| `scripts/detect-perimeter-drift.py` | Diff env / config from baseline since policy signing | Weekly |

## Related

- parent skill: `pro/dev/software-architect/`
- peer methodologies: `security-architecture`, `sec-secrets-defense-in-depth`, `gov-license-compliance-scan`
- external: [Anthropic - Claude Code security](https://docs.anthropic.com/en/docs/claude-code/security) · [GitHub Copilot Enterprise data handling](https://github.blog/2024-) · [NIST SP 800-218A - SSDF for AI](https://csrc.nist.gov/)
