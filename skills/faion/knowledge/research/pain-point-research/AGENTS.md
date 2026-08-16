# Pain-Point Research

## Summary

**One-sentence:** Systematically discover and score customer pain points across public sources (Reddit, G2, App Store, Quora, Upwork) — produces a scored pain-point log feeding ideation.

**One-paragraph:** Pain-point intuition is biased toward the operator's own pains. This methodology pins a public-source scan (Reddit search, G2 reviews, App Store reviews, Quora threads, Upwork briefs) with a fixed extraction shape (pain statement + source URL + segment + frequency proxy + workaround). Pains are scored on a 5-criterion rubric (frequency / cost / urgency / workaround quality / monetisability). Output: a pain-point log with the top 10 scored entries and source links, feeding the ideation methodology.

**Ефективно для:**

- Indie operator whose ideation keeps returning the same shapes.
- Researcher building a pain-point corpus from public signals.
- PM seeking adjacencies to existing product.
- Founder needing evidence to argue against a vanity feature.

## Applies If (ALL must hold)

- Operator can spend ≥4 hours mining 3+ public sources.
- Target segment is reachable via at least one public surface.
- Pains will feed downstream ideation or feature-discovery.
- Operator accepts that pains lacking workaround data are weak signals.

## Skip If (ANY kills it)

- Target segment is private (enterprise CIO) — public mining will miss the signal.
- Existing pain-point log is fresh (<30 days).
- Operator already has interview cohort access — skip to JTBD.
- Operator wants narrative pain stories rather than scored log — different methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source list | Reddit subs / G2 / App Store / Quora / Upwork | operator brief |
| Extraction template | csv (pain + URL + segment + freq + workaround) | this methodology |
| Scoring rubric | 5-criterion 1–5 scale | this methodology |
| Downstream consumer | ideation OR feature-discovery | research plan |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/idea-generation` | downstream ideation consumes the scored log |
| `solo/research/researcher/jobs-to-be-done` | JTBD interviews can validate top-scored pains |

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
| `draft-pain-point-research` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pain-point-research.md.j2` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/pain-point-research.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml Generated from `templates/pain-point-research.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pain-point-research.schema.json` | JSON Schema seed + filled fixture for the report artefact |
| `templates/pain-point-log.md.j2` | Structured pain-point log scored on frequency/severity/reach/spend/alternatives with a prioritized top 5. |
| `templates/pain-point-log.md` | Structured pain-point log scored on frequency/severity/reach/spend/alternatives with a prioritized top 5. Generated from `templates/pain-point-log.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/reddit-mining.md.j2` | Subreddit-mining session log extracting pain points with verbatim quotes and cross-platform observations. |
| `templates/reddit-mining.md` | Subreddit-mining session log extracting pain points with verbatim quotes and cross-platform observations. Generated from `templates/reddit-mining.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pain-point-research.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[idea-generation]]`
- `[[jobs-to-be-done]]`
- `[[problem-validation]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pain-point-research.schema.json`

```json
{
  "artefact_id": "REPLACE-WITH-ULID",
  "trigger": "Pain-Point Research engagement",
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
