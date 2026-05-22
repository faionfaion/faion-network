---
slug: mcp-security
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an MCP security rubric covering consent flows, prompt-injection defences, OAuth 2.1 PKCE, capability attestation, lookalike-server detection, and audit logging — graded per MCP server / client integration.
content_id: "4c9455a4a6a2d33f"
complexity: deep
produces: rubric
est_tokens: 3700
tags: [mcp, security, prompt-injection, authorization, consent]
---
# MCP Security — Consent, Injection Defenses, Access Controls

## Summary

**One-sentence:** Produces an MCP security rubric covering consent flows, prompt-injection defences, OAuth 2.1 PKCE, capability attestation, lookalike-server detection, and audit logging — graded per MCP server / client integration.

**One-paragraph:** Produces an MCP security rubric. MCP tools represent arbitrary code execution. Four security principles: explicit user consent for all data access + tool invocations; data privacy via appropriate access controls; tool safety via input sanitisation + validation; controlled LLM sampling requires host approval. Known attack vectors (2026): prompt injection via tool responses, tool-permission escalation, lookalike tool replacement, capability-attestation absence, bidirectional sampling without origin authentication, implicit trust propagation across multi-server configs.

**Ефективно для:** Security lead для MCP-stack — fixed rubric grading consent + auth + injection defences per server.

## Applies If (ALL must hold)

- Designing OR operating ≥1 MCP server / client integration.
- Need a defensible position for security review / audit / customer DPA.
- Multi-tenant or remote MCP servers in scope (raises bar).
- LLM agent has tool-invocation latitude (not just read-only).
- Compliance / regulatory pressure (GDPR / SOC2 / customer DPA).

## Skip If (ANY kills it)

- MCP not in use — out of scope.
- Single-user local desktop scenario with no remote MCP — apply r3 only and skip the rest.
- All MCP is internal-only with strong network isolation AND no PII — basic ruleset only.
- Security work owned by a separate red-team — coordinate but don't duplicate.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| MCP server / client inventory | yaml | ML lead |
| Transport map | yaml (per-server: transport, network) | infra |
| Data-residency policy | yaml | trust+safety |
| Consent UI design | markdown | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/mcp-architecture` | Source of primitive types graded. |
| `geek/ai/ml-engineer/mcp-client-integration` | Client-side controls graded. |
| `geek/ai/ml-engineer/eu-ai-act-compliance` | Article 15 robustness inputs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: inventory → grade-consent → grade-auth → grade-injection-defence → grade-audit. | ~800 |
| `content/06-decision-tree.xml` | essential | Branch by deployment scope (local / remote / multi-tenant) and grade-band. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-rubric` | haiku | Fill rubric skeleton from inventory. |
| `grade-server` | sonnet | Per-server scoring against rubric. |
| `escalate-finding` | opus | Cross-server attack-path analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/security-rubric.md` | Rubric skeleton with sections + score bands. |
| `templates/consent-flow.md` | Consent-UI flow description per primitive type. |
| `templates/oauth-config.yaml` | OAuth 2.1 + PKCE config for remote MCP servers. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mcp-security.py` | Validate the rubric (servers, consent grade, auth grade, injection grade, audit grade). | Pre-merge of every MCP security rubric PR. |

## Related

- [[mcp-architecture]] — server-side spec.
- [[mcp-client-integration]] — client-side controls.
- [[eu-ai-act-compliance]] — Article 15 robustness inputs.

## Decision tree

Decision tree at `content/06-decision-tree.xml` walks scope (local / remote / multi-tenant) and grade bands per rubric dimension; minimum band 'meets' required to pass.
