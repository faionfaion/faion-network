---
slug: indirect-prompt-injection-defense
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a layered defense spec against indirect prompt injection — trust-boundary diagram, span-tainting middleware, dual-LLM split, output canary, eval harness with adversarial fixtures.
content_id: "73960df637e179b5"
complexity: deep
produces: spec
est_tokens: 4400
tags: [security, prompt-injection, agent-safety, trust-boundary, ai-agents]
---
# Indirect Prompt Injection Defense

## Summary

**One-sentence:** Produces a layered defense spec against indirect prompt injection — trust-boundary diagram, span-tainting middleware, dual-LLM split, output canary, eval harness with adversarial fixtures.

**One-paragraph:** Indirect prompt injection (IPI) is the agent-era equivalent of XSS — instructions arriving inside data that a tool retrieved (web page, email, PDF, ticket comment, RAG chunk) hijack the model's next action. Prompt hardening alone never reaches a security boundary; defense requires architectural controls: an explicit trust boundary between system/developer text and tool-returned content, structured separation tags that span-taint every untrusted span, a dual-LLM split where a privileged planner never sees raw untrusted input, exfiltration canaries that detect data leakage attempts, and an adversarial eval suite (Spotlight, embedded-URL fetch, base64 instruction smuggling) that runs in CI. This methodology assembles those layers into an auditable specification a reviewer can sign off on.

**Ефективно для:** agent systems that read untrusted content (web fetch, email, GitHub issues, RAG corpus, OCR'd docs), MCP servers exposing filesystem/network tools, IDE-side AI assistants (Antigravity-class), customer-support copilots ingesting user-supplied transcripts.

## Applies If (ALL must hold)

- The agent receives content from at least one source the user cannot fully vouch for (web, email, third-party API, RAG corpus, file upload).
- The agent has at least one tool whose misuse has business or security impact (write files, send messages, call paid APIs, exfiltrate data).
- A named owner can sign off on the resulting spec and own the CI eval suite.
- The runtime stack permits structural input separation (system + user + tool blocks, or equivalent).

## Skip If (ANY kills it)

- Closed-loop agent operating only on developer-supplied prompts and own-generated text (no external read).
- Read-only agent with no consequential tools — exfiltration via response is the only risk and a single output filter suffices.
- Throwaway prototype with no production exposure — defer until the system has users.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Agent tool inventory | YAML/JSON list of `{name, description, scopes, side-effects}` | `tools.yaml` or registry |
| Data-source inventory | YAML list of `{source, trust_level, max_size, content_type}` | architecture spec |
| Threat model draft | Markdown | security review or `architecture/threats.md` |
| Sample untrusted payloads | text files | adversarial corpus or `fixtures/ipi/` |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[guardrails-basics]]` | Output-side filters cover what IPI defense input-side does not. |
| `[[ai-failure-mode-taxonomy]]` | Names the failure shape so the eval suite picks correct categories. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: trust boundary mandatory, span-tainting tags, dual-LLM split, no overlapping scopes, canary tokens, deny-by-default tools, eval-in-CI | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for defense spec: boundaries, taint-rules, eval-cases, canary-config | ~800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: prompt-only defense, allow-list trust, classifier as boundary, single-LLM with mixed roles, missing exfil canary, eval-skipped-in-CI | ~700 |
| `content/04-procedure.xml` | medium | 7-step procedure: inventory inputs → draw boundaries → choose split pattern → wire tainting → add canaries → write eval set → gate CI | ~1000 |
| `content/05-examples.xml` | medium | One full spec walk-through for a customer-support agent ingesting Zendesk tickets | ~600 |
| `content/06-decision-tree.xml` | essential | Root: "does the agent read content from sources the user cannot vouch for?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Inventory tools + data sources | sonnet | Mechanical extraction from registry. |
| Draft trust-boundary diagram | opus | Cross-system reasoning. |
| Generate adversarial eval cases | opus | Adversarial creativity, Spotlight-class novelty. |
| Validate spec against schema | haiku | Pure JSON Schema check, no judgement. |

## Templates

| File | Purpose |
|---|---|
| `templates/defense-spec.schema.json` | JSON Schema for the IPI defense specification. |
| `templates/trust-boundary.md` | Markdown skeleton with diagram, sources table, taint-rules table. |
| `templates/ipi-eval-set.jsonl` | Seed adversarial eval cases: Spotlight, base64-smuggle, embedded-URL fetch, exfil canary. |
| `templates/_smoke-test.md` | Minimum viable filled spec for a single-source agent. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-indirect-prompt-injection-defense.py` | Validates a defense-spec.json against the schema and asserts every untrusted source has ≥1 taint-rule + ≥1 eval-case. | Pre-commit on the spec file; CI on every PR. |

## Related

- parent skill: `geek/ai/`
- `[[guardrails-basics]]` — output-side companion
- `[[ai-failure-mode-taxonomy]]` — names the failure categories
- `[[jailbreak-eval-suite-bootstrap]]` — sibling eval methodology

## Decision tree

The decision tree at `content/06-decision-tree.xml` gates whether IPI defense applies and at what depth. The root asks whether the agent reads content from sources the operator cannot vouch for; if yes, it branches on tool blast radius (read-only → output-side guardrail only; write/send/charge → full layered defense per this methodology); if no, it routes to "skip-this-methodology".
