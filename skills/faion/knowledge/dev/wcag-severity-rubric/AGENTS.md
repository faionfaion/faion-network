# WCAG Severity Rubric

## Summary

**One-sentence:** Three-axis triage rubric (assistive-tech blocker × WCAG level × user-journey criticality) that buckets a11y findings into blocker / serious / moderate / minor with SLAs.

**One-paragraph:** Three-axis triage rubric (assistive-tech blocker × WCAG level × user-journey criticality) that buckets a11y findings into blocker / serious / moderate / minor with SLAs. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-wcag-severity-rubric.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Post-audit triage коли VPAT/ACR returns 200+ findings і треба швидко вибрати fix order.
- Procurement / compliance gates (Section 508, EAA, ADA) з SLA per severity tier.
- QA-engineer організовує bug board і потрібен консистентний severity mapping.
- Roadmap-planning, де accessibility findings конкурують з feature work за пріоритет.

## Applies If (ALL must hold)

- Audit produced ≥20 findings that need prioritisation
- Team has WCAG knowledge (2.0 or 2.1, AA or AAA target)
- Findings include at-population context (which user journey, which AT, which device)
- Bug tracker supports severity field used by triage process

## Skip If (ANY kills it)

- <20 findings — triage by hand is faster than rubric overhead
- No assistive-technology testing was done — can't apply the AT-blocker axis
- Procurement context where the rubric must match the buyer's (use the buyer's)
- Pre-audit scoping phase — rubric is for outputs, not inputs

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-wcag-severity-rubric` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | JSON instance with axis scores |
| `templates/rubric.md.j2` | Rubric skeleton with weighted axes |
| `templates/rubric.md` | Rubric skeleton with weighted axes Generated from `templates/rubric.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wcag-severity-rubric.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/dev/INDEX.xml`
- [[storybook-as-source-of-truth]]
- [[test-suite-audit-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rubric.json`

```json
{
  "artefact_id": "wcag-severity-rubric-2026Q2-001",
  "owner": "ruslan@faion.net",
  "axes": [
    {
      "name": "cost",
      "weight": 0.4,
      "score": 7
    },
    {
      "name": "latency",
      "weight": 0.3,
      "score": 8
    },
    {
      "name": "ops",
      "weight": 0.3,
      "score": 6
    }
  ],
  "scoring": {
    "method": "weighted-sum",
    "total": 7.0
  },
  "rationale": "Closes the gap surfaced by the parent skill \u2014 input artefact 'task-brief.md' explicitly names the constraint set; output ties decisions to rule r1.",
  "inputs_used": [
    "task-brief.md",
    "constitution.md"
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-23"
}
```
