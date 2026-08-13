# UTM Taxonomy Discipline

## Summary

**One-sentence:** Produces a UTM taxonomy config (closed source/medium/campaign vocabulary + naming rules + validation regex) for one-piece-into-10-channels atomization without attribution noise.

**Ефективно для:** Solo growth marketers atomizing one piece of content into 10 channels and losing attribution because UTM fields are ad-hoc, free-text, and case-inconsistent.

**One-paragraph:** Atomization-first content workflows produce 10 destinations per asset and 10 attribution noise sources unless the UTM vocabulary is closed and validated. This methodology produces a config file with a closed source/medium vocabulary (twitter / linkedin / threads / newsletter / podcast / partner / referral / direct / email / paid-search), a kebab-case naming rule, a campaign-id pattern (yyyymmdd-asset-slug), and a validation regex that rejects free-text noise before links ship. Output is consumed by the operator's link-builder + analytics dashboard.

## Applies If (ALL must hold)

- Operator atomizes ≥1 asset into ≥3 channels.
- Analytics tool (Plausible/GA4/Fathom) reads UTM params.
- Operator can enforce link-builder usage (no manual UTM typing).
- A naming convention can be agreed and frozen.

## Skip If (ANY kills it)

- Single-channel publishing — UTM discipline is overkill.
- Analytics tool ignores UTMs — fix attribution stack first.
- Operator unwilling to use the link-builder — discipline depends on tooling.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| closed source vocabulary (≤12 values) | list | founder decision |
| medium vocabulary (≤6 values) | list | founder decision |
| campaign-id pattern | regex string | founder decision |
| link-builder tool (Bitly/Switchy/internal) | URL/tool | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/single-operator-funnel-rubric` | Funnel reads cleaned attribution. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `validate_utm_string` | haiku | Regex match check. |
| `propose_campaign_id` | haiku | Deterministic slug from date+asset. |
| `audit_taxonomy_drift` | opus | Cross-month consistency review. |

## Templates

| File | Purpose |
|---|---|
| `templates/utm-taxonomy-discipline.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/utm-taxonomy-discipline.md` | Markdown skeleton with the required fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-utm-taxonomy-discipline.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[single-operator-funnel-rubric]] — downstream consumer.
- [[solo-content-calendar-template]] — feeds asset slugs.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/utm-taxonomy-discipline.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/utm-taxonomy-discipline.json",
  "title": "UTM Taxonomy Discipline Output Contract",
  "type": "object",
  "required": [
    "operator",
    "source_vocabulary",
    "medium_vocabulary",
    "campaign_id_pattern",
    "validation_regex",
    "link_builder_url",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "operator": {
      "type": "string",
      "description": "named taxonomy owner"
    },
    "source_vocabulary": {
      "type": "array",
      "description": "\u226412 kebab-case values",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "medium_vocabulary": {
      "type": "array",
      "description": "\u22646 kebab-case values",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "campaign_id_pattern": {
      "type": "string",
      "description": "regex (yyyymmdd-asset-slug shape)"
    },
    "validation_regex": {
      "type": "string",
      "description": "full URL regex"
    },
    "link_builder_url": {
      "type": "string",
      "description": "tool URL"
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
