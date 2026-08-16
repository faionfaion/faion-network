# Swipe File Tweet Hooks

## Summary

**One-sentence:** Produces a tagged swipe-file config (hook taxonomy, source URL, performance baseline, attribution) for build-in-public audience growth (0 → 5K).

**Ефективно для:** Indie hackers building in public who keep re-deriving hooks from scratch and have no record of what hook shapes converted in their own history.

**One-paragraph:** Swipe files exist as random docs of tweets; they don't usually carry a hook taxonomy, source URL, or performance baseline. This methodology produces a config file with each entry tagged by hook-shape (contrarian / curious-gap / list-of-N / personal-failure / data-reveal), the verbatim hook, the source URL + author handle (for attribution), and the baseline impressions the original hit. Output is consumed by the operator's drafting tool to seed new tweets without plagiarism.

## Applies If (ALL must hold)

- Operator runs build-in-public on X for audience growth (0 → 5K range).
- Operator can curate ≥20 hooks before first use.
- Attribution discipline is acceptable (no plagiarism).
- Storage path for the swipe file is decided.

## Skip If (ANY kills it)

- Operator copies hooks verbatim into own tweets — that's plagiarism, not swipe-filing.
- B2B audience where hook shapes are different (LinkedIn-style).
- Curation < 20 entries — file too thin to be useful.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| ≥20 high-performing source tweets identified | list of URLs | manual curation |
| hook taxonomy (5+ shapes) | list | internal decision |
| storage path (JSON or YAML) | file path | founder decision |
| attribution policy (cite author when adapting) | string | founder decision |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-twitter-x-growth` | Downstream growth playbook. |
| `solo/marketing/smm-manager/tweet-thread-launch-template` | Downstream launch template. |

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
| `tag_hook_shape` | haiku | Bounded classification. |
| `draft_adapted_hook` | sonnet | New-hook generation from swipe shape. |
| `audit_attribution` | opus | Cross-source plagiarism + credit check. |

## Templates

| File | Purpose |
|---|---|
| `templates/swipe-file-tweet-hooks.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/swipe-file-tweet-hooks.md.j2` | Markdown skeleton with the required fields. |
| `templates/swipe-file-tweet-hooks.md` | Markdown skeleton with the required fields. Generated from `templates/swipe-file-tweet-hooks.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-swipe-file-tweet-hooks.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-twitter-x-growth]] — consumer.
- [[tweet-thread-launch-template]] — consumer.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/swipe-file-tweet-hooks.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/swipe-file-tweet-hooks.json",
  "title": "Swipe File Tweet Hooks Output Contract",
  "type": "object",
  "required": [
    "operator",
    "entries",
    "hook_shapes",
    "attribution_policy",
    "storage_path",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "operator": {
      "type": "string",
      "description": "named curator"
    },
    "entries": {
      "type": "array",
      "description": "\u226520 hooks with shape + source + author + baseline",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "hook_shapes": {
      "type": "array",
      "description": "\u22655 shape labels",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "attribution_policy": {
      "type": "string",
      "description": "always-cite OR adapt-credit-on-similarity"
    },
    "storage_path": {
      "type": "string",
      "description": "file path / repo URL"
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
