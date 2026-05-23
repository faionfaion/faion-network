---
slug: ai-debt-detection
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Detection protocol for AI-generated code that compiles but is conventionally wrong: shadow names, abandoned variables, wrapper-on-wrapper, copy-paste duplication, mis-named symbols -- with thresholds and remediation routes."
content_id: "e00ba7c1e717f147"
complexity: medium
produces: report
est_tokens: 4900
tags: ["ai-debt", "code-quality", "detection", "sdlc-ai", "pro"]
---
# AI Debt Detection

## Summary

**One-sentence:** Detection protocol for AI-generated code that compiles but is conventionally wrong: shadow names, abandoned variables, wrapper-on-wrapper, copy-paste duplication, mis-named symbols -- with thresholds and remediation routes.

**One-paragraph:** AI coding agents produce code that compiles, passes the tests written by the same agent, and is conventionally wrong: shadow names, redundant wrappers, copy-paste duplication across files, mis-named symbols, abandoned helper variables. This silent debt accrues fast in agent-heavy repos. This methodology defines the detection signals (4 testable patterns), the per-signal thresholds, the report format (severity-ranked), and the remediation routes (in-line fix / refactor ticket / convention update). The output is a recurring AI-debt report fed into the team's debt-reduction backlog.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «ai debt detection» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- at least 30% of recent commits are AI-agent-authored (Copilot, Claude Code, Cursor).
- you have read access to the full repo history and a SAST/AST tool you can run.
- the team agrees to act on the report (otherwise it ships as documentation only).

## Skip If (ANY kills it)

- AI-agent use < 10% of commits -- signal-to-noise is poor.
- the repo is being deprecated -- debt cleanup is wasted effort.
- an external code-quality platform (SonarQube, CodeClimate) already implements equivalent detection.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the AI Debt Detection task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdlc-ai/ai-agent-guardrails-pack` | guardrails prevent some debt patterns at write time; this methodology catches what slipped through. |
| `pro/sdlc-ai/citation-contract-back-to-source` | supplies the source-tracing format the report uses to point back to code. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
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
| `templates/ai-debt-report.md` | Report skeleton: signals / thresholds / severity-ranked findings / routes. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-debt-detection.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[ai-agent-guardrails-pack]]
- [[citation-contract-back-to-source]]
- [[methodology-as-json-feed]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
