# Executive Stakeholder Demo Narrative Frame

## Summary

**One-sentence:** Tight, domain-language narrative frame for VP/SVP client demos — story arc, what to show, what to cut, signed pre-demo brief.

**One-paragraph:** Tight, domain-language narrative frame for VP/SVP client demos — story arc, what to show, what to cut, signed pre-demo brief. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- demo до VP/SVP, не до working-level team.
- 30-хв timebox з конкретною business outcome story.
- cut everything крім того, що рухає stakeholder commitment.
- pre-demo brief підписаний sponsor — не «we hope they like it».
- post-demo decision capture з owner і next step.

## Applies If (ALL must hold)

- the triggering activity 'Client demo prep + run' (role: p4-outsource-specialist) is in your workload at least once per cycle.
- you have authority to act on the artefact (write access, sign-off rights).
- a named consumer exists for the artefact — human reviewer OR downstream agent.
- an auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- one-off, never-to-repeat work — methodology overhead does not pay back.
- no named consumer — artefact will be orphaned.
- cannot access the input source-of-truth — paraphrased substitutes are worse than skipping.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/executive-stakeholder-demo-narrative-frame.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-executive-stakeholder-demo-narrative-frame.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[freelancer-payment-chase-script-library]]
- [[graceful-offboard-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
