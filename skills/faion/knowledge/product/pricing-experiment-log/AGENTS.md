# Pricing Experiment Log

## Summary

**One-sentence:** Produces a versioned pricing experiment log (hypothesis → toggle → window → result → decision per flip) so price changes stop being folklore and become a reviewable operating tool.

**Ефективно для:** Solopreneurs A/B-flipping prices ad-hoc across a year without a log, then losing track of which flip caused which MRR change.

**One-paragraph:** Pricing-experiment playbooks exist but no living log/template tracks hypotheses → result → decision across a year of flips. This methodology produces a versioned log: one row per experiment with hypothesis (≥1 falsifiable claim), toggle (what changed), measurement window, observed result vs control, and decision (keep / revert / iterate). Output is consumed by the operator's pricing review + financial forecast.

## Applies If (ALL must hold)

- Operator runs ≥1 pricing experiment per quarter.
- Operator owns the artefact (or escalates ownership to a named role).
- A version-controlled or wiki-style space hosts the log.
- The toggle event fires at a published cadence (calendar slot, threshold, A/B platform).

## Skip If (ANY kills it)

- One-shot price test with no recurrence — write a single doc.
- Operator runs <3 experiments per year — log cadence costs more than it returns.
- Pricing is contractually locked — log has nothing to record.
- No named owner — defer until ownership resolved.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| hypothesis statement (falsifiable) | string | founder |
| toggle definition | string | operator |
| baseline MRR + conversion % | snapshot | Stripe |
| measurement window | datetime range | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/product/metric-deviation-hypothesis-framework` | Sibling — hypothesis discipline carries over. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `scaffold-artefact` | haiku | Template fill from header + per-experiment rows. |
| `populate-evidence-fields` | sonnet | Per-row judgement: select correct evidence link, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-experiment synthesis at quarterly review. |

## Templates

| File | Purpose |
|---|---|
| `templates/pricing-experiment-log.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/pricing-experiment-log.md.j2` | Markdown skeleton with the required fields. |
| `templates/pricing-experiment-log.md` | Markdown skeleton with the required fields. Generated from `templates/pricing-experiment-log.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-pricing-experiment-log.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[metric-deviation-hypothesis-framework]] — related methodology.
- [[subscription-lifecycle-edge-cases]] — related methodology.
- [[vanity-metrics-audit]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pricing-experiment-log.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/pricing-experiment-log.json",
  "title": "Pricing Experiment Log Output Contract",
  "type": "object",
  "required": [
    "experiment_id",
    "hypothesis",
    "toggle",
    "baseline",
    "measurement_window",
    "observed",
    "decision",
    "evidence_links",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "experiment_id": {
      "type": "string",
      "description": "unique id"
    },
    "hypothesis": {
      "type": "string",
      "description": "falsifiable claim with numeric expectation"
    },
    "toggle": {
      "type": "object",
      "description": "before/after pricing config"
    },
    "baseline": {
      "type": "object",
      "description": "mrr + conversion% at toggle_at"
    },
    "measurement_window": {
      "type": "object",
      "description": "ISO start/end locked pre-toggle"
    },
    "observed": {
      "type": "object",
      "description": "post-window mrr + conversion%"
    },
    "decision": {
      "type": "string",
      "description": "keep | revert | iterate"
    },
    "evidence_links": {
      "type": "array",
      "description": "Stripe + dashboard URLs",
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
