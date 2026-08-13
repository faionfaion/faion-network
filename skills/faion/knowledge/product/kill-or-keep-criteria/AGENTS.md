# Kill Or Keep Criteria

## Summary

**One-sentence:** Produces a checklist that scores a side-project against MRR-floor / traffic-floor / joy-floor / opportunity-cost thresholds and outputs a binary kill-or-keep decision with cited evidence.

**Ефективно для:** Solopreneurs auditing a side-project portfolio quarterly who lack a binary, evidence-anchored kill rubric and default to 'one more month' indefinitely.

**One-paragraph:** Sunsetting a side-project is taboo and underdocumented. This methodology produces a checklist that scores the project against four floors (MRR, traffic, joy, opportunity cost), demands verbatim evidence for each score, and yields a single binary kill-or-keep verdict with the next action attached. Output is consumed by the operator's portfolio review log.

## Applies If (ALL must hold)

- Operator runs a portfolio scan at a published cadence (weekly / monthly / quarterly).
- The project has been live ≥30 days so floors have signal.
- Operator has read access to MRR + traffic dashboards.
- A named owner exists to act on the verdict (write access, sign-off rights).

## Skip If (ANY kills it)

- Project is <30 days post-launch — floors are noise, not signal.
- Operator cannot access dashboards / MRR source-of-truth — paraphrased numbers are worse than skipping.
- Project is a contractual obligation — kill is blocked anyway.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| MRR snapshot | currency | Stripe / Lemonsqueezy |
| traffic snapshot | number | Plausible / GA4 |
| joy-score self-rating | 1-10 | operator |
| opportunity-cost candidate | string | operator's roadmap |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/portfolio-triage-indie` | Parent triage that consumes the verdict. |
| `solo/product/kill-criteria-template` | Upstream — pre-registered thresholds that this rubric checks against. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `kill_or_keep_criteria_template_fill` | haiku | Template fill, no judgement. |
| `kill_or_keep_criteria_evidence_check` | sonnet | Bounded comparison + judgement. |
| `kill_or_keep_criteria_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|---|---|
| `templates/kill-or-keep-criteria.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/kill-or-keep-criteria.md` | Markdown skeleton with the required fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-kill-or-keep-criteria.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[kill-criteria-template]] — related methodology.
- [[portfolio-triage-indie]] — related methodology.
- [[sunset-failed-product-playbook]] — related methodology.
- [[pivot-vs-quit-decision-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/kill-or-keep-criteria.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/kill-or-keep-criteria.json",
  "title": "Kill Or Keep Criteria Output Contract",
  "type": "object",
  "required": [
    "project_name",
    "mrr_snapshot",
    "traffic_snapshot",
    "joy_score",
    "opportunity_cost_candidate",
    "evidence_links",
    "verdict",
    "next_action",
    "template_version",
    "last_reviewed"
  ],
  "properties": {
    "project_name": {
      "type": "string",
      "description": "named side-project"
    },
    "mrr_snapshot": {
      "type": "number",
      "description": "current MRR in USD"
    },
    "traffic_snapshot": {
      "type": "number",
      "description": "current monthly visits"
    },
    "joy_score": {
      "type": "integer",
      "description": "1-10 last-7-days self-rating"
    },
    "opportunity_cost_candidate": {
      "type": "string",
      "description": "named alternative bet"
    },
    "evidence_links": {
      "type": "object",
      "description": "URL/ticket per floor"
    },
    "verdict": {
      "type": "string",
      "description": "kill | keep (binary)"
    },
    "next_action": {
      "type": "string",
      "description": "concrete action attached to verdict"
    },
    "template_version": {
      "type": "string",
      "description": "kill-criteria-template version pinned"
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
