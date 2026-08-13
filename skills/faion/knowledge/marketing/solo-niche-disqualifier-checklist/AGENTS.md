# Solo Niche Disqualifier Checklist

## Summary

**One-sentence:** Generates a 5-signal disqualifier checklist (wrong industry, below floor, vague brief, no decision-maker, AI-spam) that rejects a cold lead in under 5 minutes without negotiation.

**Ефективно для:** Specialised freelancers whose discovery-call funnel is choked with poor-fit leads and whose specialisation premium leaks because they say yes too often.

**One-paragraph:** Specialisation is what lets a freelancer command 2-4x generalist rates, but it only works if the freelancer says no to most inbound. Without a written disqualifier list, every lead becomes a 30-minute discovery call that ends in a polite decline. This checklist names the signals (wrong industry, sub-floor rate, brief under 100 words, no named decision-maker, AI-spam outreach) that let the freelancer reply 'not a fit' in one paragraph and protects the specialisation premium.

## Applies If (ALL must hold)

- Freelancer has a stated specialisation (vertical, technical, or buyer-persona).
- Inbound exceeds capacity (>2 cold replies/week).
- A floor rate is defined (in $/hour or $/project).
- LinkedIn / email cold inbound is the primary channel.

## Skip If (ANY kills it)

- Freelancer wants generalist work — disqualifiers are anti-specialisation tools.
- Inbound is below capacity — disqualifiers without a queue are premature.
- Floor rate not yet defined — without a floor there's no rejection criterion.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| written specialisation statement (1 line) | string | founder decision |
| floor rate ($/hour or $/project) | number | founder decision |
| ≥5 named industries / project types on the hard-no list | list | founder decision |
| rejection reply template (≤60 words) | markdown | internal copy bank |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/single-operator-funnel-rubric` | Adjacent solo-ops rubric. |

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
| `score_lead_signals` | haiku | Bounded 5-signal scoring. |
| `draft_rejection_reply` | sonnet | Personal but firm rejection copy. |
| `audit_disqualifier_drift` | opus | Weekly cross-lead audit on rejection consistency. |

## Templates

| File | Purpose |
|---|---|
| `templates/solo-niche-disqualifier-checklist.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/solo-niche-disqualifier-checklist.md` | Markdown skeleton with the required fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-solo-niche-disqualifier-checklist.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[single-operator-funnel-rubric]] — funnel rhythm.
- [[shutdown-customer-email-pack]] — sunset comms variant.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/solo-niche-disqualifier-checklist.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/solo-niche-disqualifier-checklist.json",
  "title": "Solo Niche Disqualifier Checklist Output Contract",
  "type": "object",
  "required": [
    "operator",
    "specialisation_statement",
    "floor_rate",
    "hard_no_list",
    "disqualifier_signals",
    "rejection_reply_template",
    "max_eval_minutes",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "operator": {
      "type": "string",
      "description": "named freelancer"
    },
    "specialisation_statement": {
      "type": "string",
      "description": "1-line"
    },
    "floor_rate": {
      "type": "object",
      "description": "{value, unit}"
    },
    "hard_no_list": {
      "type": "array",
      "description": "\u22655 named industries/project shapes",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "disqualifier_signals": {
      "type": "array",
      "description": "exactly 5 signal definitions",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "rejection_reply_template": {
      "type": "string",
      "description": "\u226460 words"
    },
    "max_eval_minutes": {
      "type": "integer",
      "description": "\u22645"
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
