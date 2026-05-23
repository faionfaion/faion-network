---
slug: agents-md-for-receiving-team
tier: pro
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Hand-over AGENTS.md / CLAUDE.md template that captures the receiving team's AI-agent rituals, gotchas, and 'do not let the agent do X here' clauses for engagements transitioning out."
content_id: "4a7e41e3d0901c3d"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["agents-md", "handover", "ai-agent", "sdd", "pro"]
---
# AGENTS.md for Receiving Team

## Summary

**One-sentence:** Hand-over AGENTS.md / CLAUDE.md template that captures the receiving team's AI-agent rituals, gotchas, and 'do not let the agent do X here' clauses for engagements transitioning out.

**One-paragraph:** Faion has `project-docs-convention` (geek tier, AI-internal). It does not cover the transition-grade AGENTS.md a leaving dev should hand the receiving team: a document tuned to the new team's AI-agent setup, capturing rituals, gotchas, and explicit no-go zones for the agent. This methodology defines the four mandatory sections (project context, agent rituals, gotchas + landmines, no-go zones), the receiving-team validation gate (incoming team uses the file on a real task within 7 days), and the version lifecycle. Output is a versioned AGENTS.md committed to the receiving team's repo.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «agents.md for receiving team» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- an engagement / employment is transitioning code ownership to a different team.
- the receiving team uses AI coding agents (Copilot, Claude Code, Cursor, Continue).
- the repo's existing AGENTS.md/CLAUDE.md is missing OR tuned to the leaving team's setup, not the new one.

## Skip If (ANY kills it)

- the receiving team explicitly refuses AI-agent use -- write a human-only runbook instead.
- the engagement was <2 weeks -- there is not enough accumulated context to warrant the format.
- the receiving team has its own preferred handover convention -- defer to it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the AGENTS.md for Receiving Team task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdd/dark-knowledge-extraction-protocol` | this AGENTS.md consumes the dark-knowledge pack as one of its inputs. |
| `pro/sdd/decision-log-reconstruction-from-git` | supplies the 'why' the agent rituals exist. |

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
| `templates/AGENTS-handover.md` | Four-section skeleton: context / rituals / gotchas / no-go zones. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agents-md-for-receiving-team.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[dark-knowledge-extraction-protocol]]
- [[decision-log-reconstruction-from-git]]
- [[client-conventions-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
