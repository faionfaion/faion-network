---
slug: ai-plugin-ecosystem
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a Figma REST API client that performs the work usually attempted via UI plugins — contrast audits, style extraction, bulk renames — without a designer at the keyboard.
content_id: "4006ce2d0c98ada2"
complexity: medium
produces: code
est_tokens: 4200
tags: [figma-plugins, figma-automation, accessibility-audit, design-automation, rest-api]
---
# AI Plugin Ecosystem (Figma REST)

## Summary

**One-sentence:** Produces a Figma REST API client that performs the work usually attempted via UI plugins — contrast audits, style extraction, bulk renames — without a designer at the keyboard.

**One-paragraph:** Figma AI plugins (Magician, Automator, Content Reel, Stark, Similayer, Diagram) live inside the Figma desktop/browser UI. Agents cannot trigger them. The REST API is the actual integration surface for repeatable pipelines — contrast ratio computation from node fills, style extraction for handoff, bulk rename operations. This methodology produces a Python client that performs the most common plugin tasks via REST so the work runs unattended in CI.

**Ефективно для:** automation engineer, що замінює designer-driven plugin runs на CI-driven REST jobs (a11y audit / asset export / rename).

## Applies If (ALL must hold)

- Repeatable Figma operation needed (a11y audit, bulk rename, asset export, style extraction).
- Operation must run unattended (CI, schedule, webhook).
- Figma Personal Access Token or OAuth app available.

## Skip If (ANY kills it)

- Operation is one-off — use the plugin in the desktop UI.
- Operation requires writes that REST API cannot perform — Figma REST is read-only for most node mutations.
- Operation is interactive (designer needs to confirm each step) — keep the plugin path.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Figma file key | string | design team |
| Figma PAT or OAuth token | secret | secrets manager |
| Operation spec (a11y / rename / export) | YAML | ops |
| Output destination (S3, GitHub artefact) | URI | ops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[figma-ai-ecosystem]] | Companion: agent boundaries with AI suite. |
| [[adobe-firefly-integration]] | Companion: commercial-safe asset generation surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-code` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/figma_client.py` | Python Figma REST client with rate-limiter + audit log + per-operation handlers. |
| `templates/operation-spec.yaml` | YAML schema for operation + file_key + auth + output_uri. |
| `templates/_smoke-test.yaml` | Filled minimum-viable a11y-audit operation spec. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-plugin-ecosystem.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[figma-ai-ecosystem]]
- [[adobe-firefly-integration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the code; mis-routing leads to producing the wrong artefact shape.
