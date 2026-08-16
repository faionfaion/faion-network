# Feature Discovery

## Summary

**One-sentence:** Systematically discover, prioritize, and validate product features before engineering — produces a RICE-scored feature-discovery board feeding the roadmap.

**One-paragraph:** Feature ideas arrive faster than capacity. Without a discovery layer they become roadmap clutter or vibe-driven pulls. This methodology pins the discovery flow: capture (feature request log), classify (Job / Pain / Outcome), score (RICE: Reach × Impact × Confidence ÷ Effort), validate (≥3 evidence sources), promote (top 5 to roadmap), park (rest in board with revisit trigger). Output: a feature-discovery board with RICE scores, validation evidence, and named owners for the top 5.

**Ефективно для:**

- Solo PM drowning in feature requests.
- Indie operator pulled toward shiny features by single-customer voice.
- Founder whose roadmap is 30 items long and ships nothing.
- Researcher producing a feature-discovery report for stakeholders.

## Applies If (ALL must hold)

- ≥10 candidate features captured from research / support / sales.
- RICE scoring weights are agreed by the team.
- Each feature can be linked to ≥1 evidence source.
- Operator can commit to the top 5 in the next planning cycle.

## Skip If (ANY kills it)

- <10 candidates — capture more before scoring.
- Team uses an alternate scoring framework (WSJF, ICE) — adopt one, not both.
- All features are single-customer requests — run problem-validation first.
- Operator over-pivots; the artefact will not change the next planning decision.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature request log | csv / Notion | support + sales + research |
| RICE weights | agreed values | team agreement |
| Evidence source inventory | Reddit / interview / ticket | research repo |
| Capacity for next planning cycle | hours / sprint | team plan |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/jobs-to-be-done` | Job tag feeds RICE Reach + Impact estimates |
| `solo/research/researcher/pain-point-research` | Pain candidates feed feature requests |

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
| `draft-feature-discovery` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-discovery.md.j2` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/feature-discovery.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml Generated from `templates/feature-discovery.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/feature-discovery.schema.json` | JSON Schema seed + filled fixture for the report artefact |
| `templates/feature-discovery-board.md.j2` | Quarterly feature-discovery board -- collected ideas, Kano classification, ODI opportunity score, RICE prioritization, validation plan, rejected list. |
| `templates/feature-discovery-board.md` | Quarterly feature-discovery board -- collected ideas, Kano classification, ODI opportunity score, RICE prioritization, validation plan, rejected list. Generated from `templates/feature-discovery-board.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/feature-request-log.md.j2` | Single feature-request record -- metadata, problem, proposed solution, impact assessment, validation, decision. |
| `templates/feature-request-log.md` | Single feature-request record -- metadata, problem, proposed solution, impact assessment, validation, decision. Generated from `templates/feature-request-log.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-discovery.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `[[jobs-to-be-done]]`
- `[[pain-point-research]]`
- `[[problem-validation]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feature-discovery.schema.json`

```json
{
  "artefact_id": "REPLACE-WITH-ULID",
  "trigger": "Feature Discovery engagement",
  "rules_applied": [
    "REPLACE-WITH-RULE-ID"
  ],
  "evidence": [
    {
      "rule_id": "REPLACE-WITH-RULE-ID",
      "citation": "REPLACE-WITH-VERIFIABLE-CITATION",
      "source_type": "url"
    }
  ],
  "output_payload": {
    "status": "draft"
  },
  "consumer": "REPLACE-WITH-NAMED-CONSUMER",
  "owner": "REPLACE-WITH-NAMED-OWNER",
  "last_touched": "2026-05-23T10:00:00Z"
}
```
