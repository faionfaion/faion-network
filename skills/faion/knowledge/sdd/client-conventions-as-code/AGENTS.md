# Client Conventions As Code

## Summary

**One-sentence:** Codifies a foreign client's lint, branch-naming, commit-format, PR-template, and review-SLA rules into a versioned `conventions.yaml` that AI agents and humans read BEFORE faion defaults.

**One-paragraph:** Every foreign client has its own lint rules, branch naming, commit format, PR template, review-SLA. Faion ships faion-default opinions; on a client engagement those collide. This methodology defines the per-client `conventions.yaml` shape that overrides faion defaults, the precedence rule (client > faion > engine), the change-control gate (any new rule requires client signoff), and the bootstrapping path from a client style guide. The output is a versioned, signed `conventions.yaml` plus the lint/AI-agent rule files it generates.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «client conventions as code» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- engagement onboards into an existing client codebase with documented or de-facto conventions.
- an AI coding agent (Copilot, Claude Code, Cursor, Continue) will write code in the repo.
- the engagement runs >2 weeks -- one-shot patches do not need a conventions.yaml.

## Skip If (ANY kills it)

- the client has zero documented conventions AND refuses to define them -- escalate the gap before encoding.
- the engagement is read-only audit work with no code-writes.
- the client mandates a different governance tool (e.g. their own pre-commit setup) -- defer to it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Client Conventions As Code task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/client-style-guide-importer` | the upstream importer that converts a client style guide into the initial `conventions.yaml`. |
| `pro/sdlc-ai/ai-agent-guardrails-pack` | the guardrails pack that consumes the AI-agent rules generated from this file. |

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
| `templates/conventions.yaml` | Conventions skeleton: precedence + signoff + sourced rules. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-client-conventions-as-code.py` | Validate the config artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[client-style-guide-importer]]
- [[ai-agent-guardrails-pack]]
- [[dark-knowledge-extraction-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
