---
slug: gov-sonarqube-ai-code-gate
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Repos where a meaningful share of code is AI-generated MUST run SonarQube/SonarCloud with the "Sonar way for AI Code" quality gate (or a custom gate marked Qualified for AI Code Assurance) and connect Sonar's MCP server to the coding agent.
content_id: "0d5c6c974c99a9eb"
tags: [sonarqube, quality-gate, ai-code, governance, mcp]
---
# SonarQube AI Code Quality Gate

## Summary

**One-sentence:** Repos where a meaningful share of code is AI-generated MUST run SonarQube/SonarCloud with the "Sonar way for AI Code" quality gate (or a custom gate marked Qualified for AI Code Assurance) and connect Sonar's MCP server to the coding agent.

**One-paragraph:** Repos where a meaningful share of code is AI-generated MUST run SonarQube/SonarCloud with the "Sonar way for AI Code" quality gate (or a custom gate marked Qualified for AI Code Assurance) and connect Sonar's MCP server to the coding agent. The gate enforces stricter thresholds for cognitive complexity, duplication, security-hotspot density, and the AI-code trust score; the agent reads findings via MCP and rewrites until the gate is green. PRs that do not pass the AI-tuned gate cannot be merged, regardless of who or what authored the diff.

## Applies If (ALL must hold)

- Any team where AI-authored commits exceed ~25% of weekly diff volume (Copilot, Claude Code, Cursor, Codex, Devin).
- Regulated industries (finance, healthcare, government) where audit evidence of an AI-aware quality gate is a procurement/SOC2 requirement.
- Enterprise-scale monorepos that already report quality dashboards to leadership.
- Any repo emitting libraries to other teams where shallow-test and lookalike-bug regressions are expensive to chase down.

## Skip If (ANY kills it)

- Tiny solo projects — overhead exceeds value; ruff + biome + semgrep cover most of the same surface for free.
- Pure greenfield prototypes under daily API churn — the gate's duplication metric will fight the architecture before it stabilizes.
- Read-only or vendored mirrors — there is no PR surface to gate.
- Internal demos / spike branches that will be deleted — bootstrap cost is not recoverable.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
