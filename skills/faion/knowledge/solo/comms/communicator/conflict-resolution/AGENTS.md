---
slug: conflict-resolution
tier: solo
group: comms
domain: comms
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Selects a Thomas-Kilmann mode and emits a Nonviolent Communication message (Observation → Feeling → Need → Request) that stays factual and actionable.
content_id: "8096916c998b59e9"
complexity: medium
produces: spec
est_tokens: 4200
tags: [conflict-resolution, nvc, thomas-kilmann, communication, boundaries]
---
# Conflict Resolution

## Summary

**One-sentence:** Selects a Thomas-Kilmann mode and emits a Nonviolent Communication message (Observation → Feeling → Need → Request) that stays factual and actionable.

**One-paragraph:** Conflict resolution combines two frameworks: Thomas-Kilmann's five modes (Competing, Collaborating, Compromising, Avoiding, Accommodating) to select a strategy for a situation, and Marshall Rosenberg's Nonviolent Communication four-step formula (Observation → Feeling → Need → Request) to structure the message. Mode selection determines the approach; NVC ensures the message stays factual and actionable rather than evaluative and inflammatory.

**Ефективно для:**

- Peer-to-peer disagreement that has gone passive-aggressive.
- Setting a boundary with a recurring scope-creep stakeholder.
- Co-founder disputes where mode mismatch is killing the partnership.
- Cross-team friction on a shared deliverable.

## Applies If (ALL must hold)

- Disagreement is interpersonal, not purely technical.
- Both parties remain in the relationship (no termination case).
- The author has time to prepare the message asynchronously.
- Observable facts exist (not just feelings).

## Skip If (ANY kills it)

- Active emergency / safety issue — escalate, do not negotiate.
- Power-asymmetric disciplinary process — defer to HR / legal protocol.
- Anonymous feedback channel — different methodology applies.
- Conflict already escalated to mediator — mediator owns the protocol.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Observable facts | what happened, dates, quotes | author |
| Stake assessment | high / medium / low importance and time-pressure | author |
| Other party's likely interest | what they want from this | author |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[active-listening]] | upstream — RASA pass before drafting message |
| [[difficult-conversations]] | neighbouring methodology for high-stakes script form |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `mode-selection` | sonnet | Light judgment on stakes/relationship. |
| `observation-strip` | haiku | Mechanical removal of evaluative words. |
| `draft-nvc` | sonnet | Tone-sensitive composition. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nvc-message.md` | NVC 4-line message skeleton with field-level cues |
| `templates/prompt-mode-selection.txt` | Prompt to apply TK matrix to a conflict description |
| `templates/prompt-nvc-rewrite.txt` | Prompt to rewrite an evaluative draft into observation/feeling/need/request |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-conflict-resolution.py` | Validate conflict-resolution artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[difficult-conversations]]
- [[active-listening]]
- [[feedback]]
- [[stakeholder-communication]]

## Decision tree

See `content/06-decision-tree.xml`. Routes by stakes × relationship matrix to one of the five TK modes, then to NVC structuring. Avoiding leaf is the only one that maps to skip-this-methodology.
