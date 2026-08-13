# Social Proof Harvest

## Summary

**One-sentence:** Generates a four-stage harvest playbook-step (detect → capture → consent → publish) that turns spontaneous public mentions into permissioned testimonials on a wall page.

**Ефективно для:** Solo founders with ≥1 organic mention/week on public channels who leak 80% of social proof because moments fly past without capture.

**One-paragraph:** Existing testimonial methodologies cover the ASK pattern. They don't cover the HARVEST pattern: detect when someone mentions you in public, capture the quote with author identity, run a permission flow, and publish to the wall. This playbook-step defines the four-stage loop (detect → capture → consent → publish), the storage schema that lets one quote drive multiple surfaces, and the consent + citation rules that keep the harvest legal and credible.

## Applies If (ALL must hold)

- Product has ≥1 organic mention/week across public channels.
- Operator owns the website where the wall lives.
- A lightweight detection workflow (search alerts, Brand24, n8n scrape) can be set up.
- A single source-of-truth quote DB (Notion/Airtable/JSON) is chosen.

## Skip If (ANY kills it)

- Zero organic mentions — fix distribution first; harvest needs signal.
- B2B niche under NDA — switch to permissioned-customer-quote ASK pattern.
- Operator refuses to log consent — pattern is legally non-compliant without it.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| mention-detection workflow (saved search/scraper) | URL or workflow ID | self-managed |
| quote DB schema choice (Notion/Airtable/JSON) | string | founder decision |
| consent request template (DM + email variants) | markdown | internal copy bank |
| wall page template (HTML/MD) | template path | frontend repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/growth-customer-testimonials` | Adjacent ASK pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `classify_mention_relevance` | haiku | Bounded relevance filter. |
| `draft_consent_request` | sonnet | Personalised DM/email with quote in context. |
| `review_legal_exposure` | opus | Cross-input judgement on consent edge cases. |

## Templates

| File | Purpose |
|---|---|
| `templates/social-proof-harvest.json` | JSON Schema for the output contract. |
| `templates/social-proof-harvest.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-social-proof-harvest.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-customer-testimonials]] — paired ASK pattern.
- [[shutdown-customer-email-pack]] — sunset-survey quote harvest variant.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/social-proof-harvest.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/social-proof-harvest.json",
  "title": "Social Proof Harvest Output Contract",
  "type": "object",
  "required": [
    "quote_id",
    "source_url",
    "author_handle",
    "author_display_name",
    "verbatim_quote",
    "captured_at",
    "channel",
    "consent",
    "status",
    "publish_surfaces",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "quote_id": {
      "type": "string",
      "description": "stable record id"
    },
    "source_url": {
      "type": "string",
      "description": "URL of original public mention"
    },
    "author_handle": {
      "type": "string",
      "description": "platform handle"
    },
    "author_display_name": {
      "type": "string",
      "description": "name shown on the wall"
    },
    "verbatim_quote": {
      "type": "string",
      "description": "exact text \u2014 no paraphrase"
    },
    "captured_at": {
      "type": "string",
      "description": "ISO timestamp",
      "format": "date-time"
    },
    "channel": {
      "type": "string",
      "description": "twitter|linkedin|reddit|hn|discord|product-hunt|other"
    },
    "consent": {
      "type": "object",
      "description": "{requested_at, granted_at, granted_via}"
    },
    "status": {
      "type": "string",
      "description": "captured|requested|approved|published|expired"
    },
    "publish_surfaces": {
      "type": "array",
      "description": "wall|landing-hero|sales-deck|email-signature",
      "items": {
        "type": "object"
      },
      "minItems": 1
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
  "quote_id": "sample-quote_id",
  "source_url": "sample-source_url",
  "author_handle": "sample-author_handle",
  "author_display_name": "sample-author_display_name",
  "verbatim_quote": "sample-verbatim_quote",
  "captured_at": "2026-05-23T12:00:00Z",
  "channel": "value",
  "consent": {
    "key": "value"
  },
  "status": "value",
  "publish_surfaces": [
    {
      "key": "value"
    }
  ],
  "version": "sample-version",
  "last_reviewed": "2026-05-23"
}
```
