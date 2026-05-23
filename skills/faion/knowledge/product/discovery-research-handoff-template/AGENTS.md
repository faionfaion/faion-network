# Discovery Research Handoff Template

## Summary

**One-sentence:** One-page discovery handoff bundling problem statement, persona, JTBD, evidence quotes, success metric — the canonical artefact PMs hand to design + engineering after discovery.

**One-paragraph:** Discovery work loses value when the handoff is a slack thread or 30-page deck. This methodology pins a one-page handoff with five sections: (1) problem statement (1 sentence + impact + segment), (2) persona snapshot, (3) JTBD (when... I want to... so I can...), (4) evidence — ≥3 verbatim quotes with source + date, (5) success metric. The artefact is signed by the PM and the receiving lead (design or engineering) before any solutioning work begins.

**Ефективно для:**

- Solo PM finishing discovery and starting solutioning.
- Indie operator handing context to a contractor designer or engineer.
- Tech-lead receiving discovery output and skeptical of its readiness.
- Product team running continuous discovery with regular handoffs.

## Applies If (ALL must hold)

- Discovery has surfaced a real problem with ≥3 customer interviews behind it.
- Solutioning work is about to start in the next sprint.
- PM owns the handoff artefact and can require sign-off.
- Receiving lead is named (designer or engineer).

## Skip If (ANY kills it)

- Problem is too vague to compress to one sentence — return to discovery.
- Same problem was handed off ≤90 days ago and is still in flight — update, do not redo.
- Discovery was abandoned (kill criterion hit) — no handoff needed.
- Solutioning is exploratory spike with no commitment — defer handoff until commitment.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interview notes (≥3) | md | research repo |
| Persona definition | md | research repo or persona library |
| Receiving lead name + handle | string | engagement charter |
| Success metric draft | 1 sentence | PM notes |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent operating context |
| `pro/research/researcher` | interview-evidence shape |
| `solo/product/demo-hypothesis-template` | hypothesis-evidence link |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-discovery-research-handoff-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/discovery-research-handoff-template.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/discovery-research-handoff-template.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-discovery-research-handoff-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[demo-hypothesis-template]]`
- `[[friction-to-backlog]]`
- `[[kano-prioritization]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
