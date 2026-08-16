# Growth Loops

## Summary

**One-sentence:** Generates a growth-loop spec (input -> action -> output -> fuel-back) with stage metrics, friction map, and steady-state projection.

**One-paragraph:** Generates a growth-loop spec (input -> action -> output -> fuel-back) with stage metrics, friction map, and steady-state projection. Use it when funnel-only thinking буксує на cac payback — потрібен loop. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Funnel-only thinking буксує на CAC payback — потрібен loop.
- Existing user behaviour produces fuel for new users.
- Час відстежити loop steady-state >=90d.
- Stable instrumentation per loop stage (acquisition / action / output).

## Applies If (ALL must hold)

- The producing agent has read access to the inputs named in Prerequisites.
- The downstream consumer expects an artefact whose shape matches `produces=spec`.
- A named human reviewer is available for signoff before any binding action.
- The task has more than a one-shot scope — output will be re-read or extended later.

## Skip If (ANY kills it)

- Pre-discovery: inputs unstable, problem not named — pick a discovery methodology instead.
- One-shot prompt task that nobody else will reuse — write a plain prompt, not a methodology call.
- Output consumer wants a different shape than `produces=spec` — pick a methodology whose contract matches.
- Hard real-time path where the output-contract validator can't run in budget.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Brief / inputs | Markdown or JSON | requester / upstream methodology |
| Domain context | text | parent skill `pro/marketing/growth-marketer/` |
| Output destination | path or system | downstream owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example for produces=spec | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-growth-loops.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-loops.spec.md.j2` | Markdown spec skeleton with 5-line header |
| `templates/growth-loops.spec.md` | Markdown spec skeleton with 5-line header Generated from `templates/growth-loops.spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/growth-loops.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-loops.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-loops.example.json`

```json
{
  "slug": "growth-loops",
  "owner": "growth lead",
  "review_deadline": "2026-06-15",
  "summary": "Spec for Growth Loops covering preconditions, procedure, output, and review gate.",
  "sections": [
    {
      "name": "preconditions",
      "content": "All Applies If items confirmed in writing."
    },
    {
      "name": "procedure",
      "content": "Steps 1..n executed per content/04-procedure.xml."
    },
    {
      "name": "review",
      "content": "Human reviewer signed off on date."
    }
  ],
  "deviation_log_reference": "ops/deviation-log.md#L42",
  "signoff": {
    "reviewer": "growth lead",
    "date": "2026-06-10"
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "slug": "growth-loops",
  "owner": "growth lead",
  "review_deadline": "2026-06-15",
  "summary": "Spec for Growth Loops covering preconditions, procedure, output, and review gate.",
  "sections": [
    {
      "name": "preconditions",
      "content": "All Applies If items confirmed in writing."
    },
    {
      "name": "procedure",
      "content": "Steps 1..n executed per content/04-procedure.xml."
    },
    {
      "name": "review",
      "content": "Human reviewer signed off on date."
    }
  ],
  "deviation_log_reference": "ops/deviation-log.md#L42",
  "signoff": {
    "reviewer": "growth lead",
    "date": "2026-06-10"
  }
}
```
