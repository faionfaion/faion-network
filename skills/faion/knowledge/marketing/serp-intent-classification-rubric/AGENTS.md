# SERP Intent Classification Rubric

## Summary

**One-sentence:** Tags every target query with one primary intent (I/C/T/N) + optional secondary anchored to falsifiable top-10 SERP signals — rejects gut-feel classifications.

**Ефективно для:** Solo SEO operators producing AI-assisted drafts who keep shipping format-mismatched content because the human author never made the intent explicit.

**One-paragraph:** AI-generated drafts miss intent because the human author never made it explicit. This rubric forces the tagger to (a) pick exactly one primary intent from a closed set (Informational / Comparative / Transactional / Navigational), (b) cite ≥2 independent SERP signals justifying the pick, (c) flag intent-mixed queries that should be split, (d) tag ambiguous SERPs as needing research not classification. Output is a one-line intent label that downstream methodologies (`search-intent-to-brief`, `on-page-seo-checklist-2026`) consume.

## Applies If (ALL must hold)

- A target query (head or long-tail) is on the desk.
- A live top-10 SERP for the query can be pulled (manual or API).
- Drafting content against the query is the next action.

## Skip If (ANY kills it)

- The query is purely navigational for a known brand AND you are that brand.
- The query has <10 monthly searches AND no cluster value.
- The brand explicitly does not target organic search for the term.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| target query string | string | keyword research export |
| top-10 SERP snapshot | screenshot or HTML | incognito browser or SERP API |
| optional: related-searches list | list of strings | GSC or keyword tool |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/search-intent-to-brief` | Downstream consumer of the intent label. |
| `solo/marketing/seo-manager/topical-authority` | Cluster context for the query. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 4 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `extract_serp_signals` | haiku | Structured pull from top-10 — bounded transformation. |
| `apply_rubric` | sonnet | Classification with cited evidence. |
| `flag_intent_mix_or_ambiguity` | sonnet | Meta-judgement on SERP split. |

## Templates

| File | Purpose |
|---|---|
| `templates/serp-intent-classification-rubric.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/serp-intent-classification-rubric.md` | Markdown skeleton with the required fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-serp-intent-classification-rubric.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[search-intent-to-brief]] — downstream brief generator.
- [[seo-manager]] — domain context.
- [[zero-click-search-adaptation]] — paired AIO methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/serp-intent-classification-rubric.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/serp-intent-classification-rubric.json",
  "title": "SERP Intent Classification Rubric Output Contract",
  "type": "object",
  "required": [
    "query",
    "primary_intent",
    "primary_subtype",
    "secondary_intent",
    "serp_evidence",
    "recommendation",
    "classifier",
    "classified_at"
  ],
  "properties": {
    "query": {
      "type": "string",
      "description": "verbatim target query"
    },
    "primary_intent": {
      "type": "string",
      "description": "one of I / C / T / N"
    },
    "primary_subtype": {
      "type": "string",
      "description": "e.g., I:how-to, C:vs, T:buy, N:brand"
    },
    "secondary_intent": {
      "type": "string",
      "description": "null unless \u226530% of top-10 serve a different class"
    },
    "serp_evidence": {
      "type": "array",
      "description": "\u22652 independent signals with type+value",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "recommendation": {
      "type": "string",
      "description": "SINGLE_BRIEF | SPLIT | AMBIGUOUS_BLOCK"
    },
    "classifier": {
      "type": "string",
      "description": "named human / agent"
    },
    "classified_at": {
      "type": "string",
      "description": "ISO timestamp",
      "format": "date-time"
    }
  },
  "additionalProperties": true
}
```
