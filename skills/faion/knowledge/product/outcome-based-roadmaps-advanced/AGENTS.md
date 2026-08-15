# Outcome Based Roadmaps Advanced

## Summary

**One-sentence:** Produces an advanced outcome-roadmap spec (multi-quarter outcome chains + dependency edges + confidence-decay model + portfolio-level swim lanes) for teams beyond single-quarter horizons.

**Ефективно для:** Senior solopreneur PMs whose 1-quarter outcome roadmap is fine but cross-quarter chains, dependencies, and confidence-decay over 6+ months are invisible.

**One-paragraph:** Single-quarter outcome roadmaps work for 1 product / 1 team / 1 stakeholder. Beyond that, outcomes chain across quarters, solutions develop hard dependencies, and confidence decays predictably the further out you plan. This advanced methodology produces a multi-quarter outcome chain with explicit dependency edges, a confidence-decay model (high < 1Q, medium 1-2Q, low > 2Q), and portfolio-level swim lanes per product. It also anchors the horizon downward: a falsifiable business goal at the root, a causal hypothesis and one weekly-readable leading indicator per outcome, experiments with pre-registered criteria, and four audience views (customer, board, engineering, sales) rendered from the one source tree. Output is consumed by board / stakeholder reviews + strategic planning.

## Applies If (ALL must hold)

- Operator runs a roadmap across ≥2 quarters / ≥2 products.
- Cross-product or cross-outcome dependencies are real (not just preferences).
- Stakeholders need a multi-quarter horizon.
- Confidence-decay tradeoffs are accepted (not 'just guarantee Q4').

## Skip If (ANY kills it)

- Single-quarter horizon — outcome-based-roadmaps (the base methodology) is enough.
- Single product + no cross-outcome dependencies — base methodology suffices.
- Stakeholders demand exact long-horizon dates — use a date-bound plan instead.
- Pre-PMF — long-horizon planning is theatre at this stage.
- No analytics instrumentation for weekly leading indicators — the chain cannot be steered between quarter closes.
- Compliance or regulatory work where the outcome is dictated externally.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| multi-quarter horizon dates | ISO range | operator |
| portfolio swim lanes (per product) | array | operator |
| dependency graph candidates | DAG | operator |
| instrumented metrics per outcome | object | analytics |
| business goal statement | metric + current + target + deadline | leadership |
| audience list | table | stakeholder map |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/outcome-based-roadmaps` | Base — this is the advanced layer atop the quarterly method. |
| `solo/product/multi-product-portfolio-management` | Sibling — portfolio swim lanes mirror portfolio config. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 10 testable rules with rationale + source — r1-r5 multi-quarter chain, r6-r10 goal decomposition + multi-audience | ~1600 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 8 failure modes with detector + repair | ~1300 |
| `content/04-procedure.xml` | essential | 9 step-by-step procedure: anchor goal -> chain -> dependencies -> decay -> lanes -> hypotheses -> indicators -> experiments -> publish | ~1200 |
| `content/05-examples.xml` | essential | Worked end-to-end examples incl. an ARR goal decomposed over three quarters | ~1000 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_multi_q_chain` | sonnet | Bounded judgement on outcome chain across quarters. |
| `attach_dependency_edges` | sonnet | Per-edge judgement on dependency type (hard/soft). |
| `apply_confidence_decay` | opus | Cross-horizon synthesis with decay model. |
| `portfolio_swim_lane_synthesis` | opus | Per-product swim lane reconciliation. |

## Templates

| File | Purpose |
|---|---|
| `templates/outcome-based-roadmaps-advanced.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/outcome-based-roadmaps-advanced.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-outcome-based-roadmaps-advanced.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[outcome-based-roadmaps]] — related methodology.
- [[multi-product-portfolio-management]] — related methodology.
- [[okr-setting]] — related methodology.
- [[feature-prioritization-rice]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/outcome-based-roadmaps-advanced.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/outcome-based-roadmaps-advanced.json",
  "title": "Outcome Based Roadmaps Advanced Output Contract",
  "type": "object",
  "required": [
    "horizon",
    "swim_lanes",
    "outcomes_by_quarter",
    "dependency_edges",
    "confidence_decay_applied",
    "quarter_reviews",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "horizon": {
      "type": "object",
      "description": "ISO start/end across \u22652 quarters"
    },
    "swim_lanes": {
      "type": "array",
      "description": "per-product lanes \u22652",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "outcomes_by_quarter": {
      "type": "object",
      "description": "quarter \u2192 outcomes[]"
    },
    "dependency_edges": {
      "type": "array",
      "description": "from/to/type/rationale objects",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "confidence_decay_applied": {
      "type": "boolean",
      "description": "true means decay applied unless cited"
    },
    "quarter_reviews": {
      "type": "array",
      "description": "per closed quarter review entry",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "owner": {
      "type": "string",
      "description": "named owner"
    },
    "version": {
      "type": "string",
      "description": "semver"
    },
    "last_reviewed": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    }
  },
  "additionalProperties": true
}
```

### `templates/_smoke-test.json`

```json
{
  "horizon": {
    "k": "v"
  },
  "swim_lanes": [
    {
      "k": "v"
    }
  ],
  "outcomes_by_quarter": {
    "k": "v"
  },
  "dependency_edges": [
    {
      "k": "v"
    }
  ],
  "confidence_decay_applied": true,
  "quarter_reviews": [
    {
      "k": "v"
    }
  ],
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
