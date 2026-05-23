---
slug: inc-read-only-investigation-default
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: During incidents the AI agent operates in read-only mode by default; write actions require explicit per-action approval token; trust-escalation script tracks the trust ratchet.
content_id: "4762f290d6d2e42b"
complexity: medium
produces: config
est_tokens: 4400
tags: [incident, agent-safety, rbac, read-only, trust-escalation]
---
# Read-Only Investigation by Default

## Summary

**One-sentence:** During incidents the AI agent operates in read-only mode by default; write actions require explicit per-action approval token; trust-escalation script tracks the trust ratchet.

**One-paragraph:** During production incidents, the worst AI mistake is a confident write action — a rollback to the wrong commit, a misapplied feature flag, a 'helpful' restart that destroys debug state. This methodology pins agents to read-only RBAC by default (Read, Grep, Glob, log/dashboard access, runbook fetch) and requires an explicit per-action signed approval token (`gov-approval-token-signed-jwt`) before any write. A trust-escalation script tracks the ratchet — once an agent earns write rights for a specific action class, the audit log captures the precedent.

**Ефективно для:**

- AI agent (Claude Code, custom SRE bot) participates in incident response.
- Production systems can be materially harmed by misapplied write actions (rollbacks, flags, infra mutations).
- Platform supports per-action RBAC (Kubernetes RBAC, AWS IAM, etc.) and signed approval tokens.

## Applies If (ALL must hold)

- AI agent (Claude Code, custom SRE bot) participates in incident response.
- Production systems can be materially harmed by misapplied write actions (rollbacks, flags, infra mutations).
- Platform supports per-action RBAC (Kubernetes RBAC, AWS IAM, etc.) and signed approval tokens.

## Skip If (ANY kills it)

- Agent is a chat-only assistant with no execution surface — no writes possible.
- Team has no incident-response automation at all — install the basics first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Agent RBAC config | yaml | Repo at `incident/agent-rbac.yaml` |
| Approval token verifier | config | From `gov-approval-token-signed-jwt` |
| Action class catalog | yaml | Repo at `incident/action-classes.yaml` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-inc-read-only-investigation-default` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-rbac.yaml` | Agent RBAC manifest |
| `templates/escalate_trust.py` | Trust ratchet manager |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inc-read-only-investigation-default.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[ci-eval-gate-config]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
