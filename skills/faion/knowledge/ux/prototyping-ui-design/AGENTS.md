# Prototyping

## Summary

**One-sentence:** Build the smallest interactive prototype that can falsify a single hypothesis in 1-3 hours, then use evidence-collection to decide kept / rolled-back / shipped-with-changes.

**One-paragraph:** Prototyping fails when scope is undefined and outcome is opinion-based. This methodology pins a four-step loop: scope to one falsifiable hypothesis, build the smallest possible variant (Figma click-through or low-code), collect evidence (5-user test, click metric, internal review), decide outcome. Each loop produces a log row via prototype-iteration-log-template. Loops longer than 3 hours are split.

**Ефективно для:**

- Solo designer with 1-3hr sprints multiple times per week.
- Founder running pre-build prototype rounds before committing eng time.
- AI agent generating prototype variants where the human must judge outcome.
- Pre-launch design where last-mile prototypes inform final scope cuts.

## Applies If (ALL must hold)

- A falsifiable hypothesis exists (IF / THEN form).
- A prototyping tool is available (Figma, Codepen, Framer, no-code builder).
- Evidence collection mechanism exists (5-user test / metric / review).
- 1-3 hour time budget can be blocked.

## Skip If (ANY kills it)

- Hypothesis not falsifiable — refine first.
- Production design (not prototype) — use design-to-dev-handoff instead.
- No evidence mechanism — prototype produces opinion only.
- Time budget > 8 hours — split into multiple iterations.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Falsifiable hypothesis | string (IF / THEN) | Researcher / designer / agent |
| Prototyping tool URL | URL | Figma / Codepen / Framer |
| Evidence-collection method | string | Test plan |
| Time-box (1-3 hr) | integer | Designer calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/prototype-iteration-log-template` | Log row produced per iteration. |
| `solo/ux/critical-issue-triage-protocol` | Findings from the prototype triage feed downstream. |

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
| `draft-prototype-plan` | sonnet | Per-iteration judgement on scope + variant choice. |
| `validate-iteration-output` | haiku | Deterministic check that log row + evidence link are present. |
| `sprint-retro-pass` | opus | Cross-iteration pattern detection across a sprint. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prototyping.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/prototyping.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prototyping.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[prototype-iteration-log-template]]
- [[critical-issue-triage-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
