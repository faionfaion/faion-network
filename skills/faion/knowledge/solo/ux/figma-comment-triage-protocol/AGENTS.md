---
slug: figma-comment-triage-protocol
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 30-minute daily Figma comment sweep that categorises every open comment into FIX / DECIDE / ANSWER / IGNORE with a named owner so comments do not silt up the canvas.
content_id: "aee642c730e17cc0"
complexity: medium
produces: report
est_tokens: 4200
tags: ["figma", "comment-triage", "design-sweep", "ux", "daily-ritual"]
---
# Figma Comment Triage Protocol

## Summary

**One-sentence:** 30-minute daily Figma comment sweep that categorises every open comment into FIX / DECIDE / ANSWER / IGNORE with a named owner so comments do not silt up the canvas.

**One-paragraph:** Figma canvases accumulate uncategorised comments faster than designers can respond. This protocol pins a daily 30-min sweep that classifies each open comment using a closed taxonomy (FIX action / DECIDE design choice / ANSWER question / IGNORE noise), assigns a named owner per row, and either resolves, replies, or routes to the design-decision-log. Sweep results are captured as an artefact so the queue depth is auditable.

**Ефективно для:**

- Solo designer running a daily Figma sweep before standup.
- Cross-team handoff where comments accumulate from PM / eng without an owner.
- Pre-launch design freeze where unresolved comments must be zero before sign-off.
- AI-assisted review where the agent must triage comments before generating a design ticket.

## Applies If (ALL must hold)

- Figma file in active iteration with ≥5 open comments older than 24h.
- At least one designer or agent has 30 minutes blocked daily.
- Comment authors are reachable (DM / Slack / email) for clarification.
- Design-decision-log or sprint board exists where DECIDE / FIX rows can be routed.

## Skip If (ANY kills it)

- Figma file is read-only / archived.
- All comments are from a single author and should be addressed in a focused review, not a sweep.
- Comments are auto-generated noise from a plugin; disable the plugin first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Figma file URL | URL | Figma file picker |
| Open-comments list | array | Figma comments API or sidebar export |
| Author roster | map handle → role | Team directory |
| Owner handle for sweep | string | Designer / agent registry |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/design-decision-log-template` | DECIDE rows route into the log. |
| `solo/ux/anti-pattern-rationale-template` | Repeat FIX rows feed the bank. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-comments` | sonnet | Per-comment judgement on category + owner. |
| `dedupe-and-resolve` | haiku | Deterministic resolve of duplicate or already-fixed comments. |
| `weekly-sweep-audit` | opus | Cross-day pattern detection (e.g. same comment 5 days in a row). |

## Templates

| File | Purpose |
|------|---------|
| `templates/figma-comment-triage-protocol.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/figma-comment-triage-protocol.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-figma-comment-triage-protocol.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-decision-log-template]]
- [[anti-pattern-rationale-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
