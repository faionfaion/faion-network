---
slug: ai-agent-guardrails-pack
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Reusable prompt + system-rule + lint-aligned scaffold pack that constrains Copilot, Claude Code, and Cursor to client conventions in regulated codebases (FinTech, HIPAA, multi-tenant SaaS)."
content_id: "4e1de97518ff0ef9"
complexity: deep
produces: config
est_tokens: 4200
tags: ["ai-agent", "guardrails", "compliance", "copilot", "claude-code", "cursor", "sdlc-ai", "pro"]
---
# AI Agent Guardrails Pack

## Summary

**One-sentence:** Reusable prompt + system-rule + lint-aligned scaffold pack that constrains Copilot, Claude Code, and Cursor to client conventions in regulated codebases (FinTech, HIPAA, multi-tenant SaaS).

**One-paragraph:** Outsource and agency teams ship into regulated codebases where Copilot Business, Claude Code, and Cursor must obey client conventions: no PII echo, no secret paste, no cross-tenant context, lint parity, framework-version pin. This methodology defines the guardrails directory shape, the cross-agent rule format (each rule expressed once, translated per agent), the lint-alignment pass (every guardrail also fires as a lint rule), and the legal/security signoff gate. Output is a portable `guardrails/` directory the client legal team can review once and the dev team can keep updated.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «ai agent guardrails pack» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- the client codebase is under FinTech, HIPAA, GDPR, PCI-DSS, SOC 2, or equivalent regime OR the contract enumerates AI-coding constraints.
- the team uses at least one of: GitHub Copilot Business, Claude Code, Cursor, Continue, or a comparable in-editor agent.
- the client has an existing lint/format stack (eslint, ruff, golangci-lint) the pack can align to.

## Skip If (ANY kills it)

- the codebase is greenfield with no compliance regime AND no plan to acquire one.
- AI-agent use is forbidden -- ship a 'no-agent' notice instead.
- the client already maintains a guardrails system you are slotting into; defer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the AI Agent Guardrails Pack task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/client-conventions-as-code` | the conventions.yaml is the upstream source the guardrails enforce. |
| `pro/sdlc-ai/ai-agent-prompt-handover` | handover pattern for transferring the guardrails to a new team. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/guardrails.yaml` | Neutral rule source: deny patterns + lint mapping + signoff block. |
| `templates/copilot-rules.md` | Per-agent rendered example for Copilot Business. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-agent-guardrails-pack.py` | Validate the config artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[client-conventions-as-code]]
- [[ai-agent-prompt-handover]]
- [[ai-debt-detection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
