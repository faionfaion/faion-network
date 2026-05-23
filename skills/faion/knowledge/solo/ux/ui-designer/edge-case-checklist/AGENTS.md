---
slug: edge-case-checklist
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Closed checklist of 10 edge cases (long text, RTL, slow network, no-data, error, offline, dark mode, small screen, a11y screen reader, time zone) applied to every shipped component so the production-bug surface drops by an order of magnitude.
content_id: "95a567b5ca18f071"
complexity: medium
produces: checklist
est_tokens: 3600
tags: ["edge-cases", "defensive-design", "checklist", "ux", "handoff"]
---
# Edge-Case Checklist

## Summary

**One-sentence:** Closed checklist of 10 edge cases (long text, RTL, slow network, no-data, error, offline, dark mode, small screen, a11y screen reader, time zone) applied to every shipped component so the production-bug surface drops by an order of magnitude.

**One-paragraph:** Production bugs cluster on the same edge cases: long text overflowing, RTL flipping wrong, slow-network skeletons missing, empty states designed-out. This checklist pins 10 closed cases that every component must answer YES / NO / N/A before handoff. The list is intentionally short to be runnable; longer lists become aspirational and get skipped.

**Ефективно для:**

- Solo founder shipping new components weekly.
- Pre-handoff designer checklist before triggering design-to-dev process.
- AI agent generating component variants — checklist tells the agent what variants are mandatory.
- Pre-launch QA where regression on edge cases must be near-zero.

## Applies If (ALL must hold)

- A component or screen is ready for handoff or release.
- Edge-case variants can be expressed in the design tool.
- ≤10 minutes of designer time is available per checklist run.
- Eng will consume the checklist as part of AC.

## Skip If (ANY kills it)

- Marketing static image with no interactive states.
- Throwaway prototype with no production users.
- Component is internal-tool only and the team has accepted edge-case debt.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component design | Figma URL | Design canvas |
| Locale list (for RTL) | list | Product i18n config |
| Network-condition test mode | browser devtools or staging env | Frontend QA |
| Designer time budget | ≤10 min | Designer calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/handoff-spec-template` | Spec consumes the edge-case answers. |
| `solo/ux/ui-designer/design-to-dev-handoff` | Handoff process consumes the checklist. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-edge-case-answers` | sonnet | Per-case judgement on YES / NO / N/A + visual treatment. |
| `validate-checklist-coverage` | haiku | Deterministic check that all 10 cases have an answer. |
| `flow-level-edge-case-audit` | opus | Cross-component synthesis for a flow. |

## Templates

| File | Purpose |
|------|---------|
| `templates/edge-case-checklist.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/edge-case-checklist.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-edge-case-checklist.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[handoff-spec-template]]
- [[design-to-dev-handoff]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
