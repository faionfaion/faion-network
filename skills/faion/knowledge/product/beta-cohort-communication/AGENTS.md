# Beta Cohort Communication

## Summary

**One-sentence:** Weekly broadcast + targeted-feedback flow keeping beta cohorts engaged from recruit through graduation — pinned cadence, three message types, single ask per send.

**One-paragraph:** Beta cohorts collapse silently when communication drifts. This methodology pins three message types (weekly recap, single-ask survey, milestone announcement), one ask per send, and a recruit-through-graduation flow. Cadence: weekly recap every Tuesday, single-ask survey at week 2 + week 6, milestone announcement at week 4. Replies feed back into the beta charter's success metric.

**Ефективно для:**

- Solo founder running a closed beta with 5-20 users.
- Course creator nurturing a cohort over 4-8 weeks.
- Indie maker maintaining engagement during a 30-day private beta.
- Tech lead running internal stakeholder updates on a phased rollout.

## Applies If (ALL must hold)

- An active beta cohort exists (recruited and onboarded).
- Founder owns the channel (newsletter / Slack / dedicated email).
- A success metric is defined (from `beta-charter-template`).
- Cohort size ≤50.

## Skip If (ANY kills it)

- No beta charter exists — author one first.
- Cohort >50 — switch to broadcast marketing tactics.
- Founder cannot maintain the weekly cadence — kill the beta instead.
- Channel ownership is contested (e.g., shared team Slack).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Beta charter | md | beta-charter-template output |
| Beta candidate roster | csv with name + handle + segment | recruiting flow |
| Channel access | newsletter / Slack workspace | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/beta-charter-template` | charter defines cadence + metric |
| `solo/comms/communicator` | communicator skill operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-beta-cohort-communication` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/beta-cohort-communication.md` | Markdown skeleton for the playbook-step artefact, matching content/02-output-contract.xml |
| `templates/beta-cohort-communication.schema.json` | JSON Schema seed + filled fixture for the playbook-step artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-beta-cohort-communication.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[beta-charter-template]]`
- `[[feedback-loop-customer-reply-templates]]`
- `[[mvp-instrumentation-checklist]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
