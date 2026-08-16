# Launch Tier Decision Frame

## Summary

**One-sentence:** Produces a decision-record selecting one launch tier (soft / friend-circle / PH-day / HN+PH+podcast blitz) based on readiness + funnel-fit + retreat-cost.

**Ефективно для:** Solopreneurs over-investing in a PH+HN blitz before the product can handle the spike, or under-investing in a friend-circle launch when a tier-3 push was warranted.

**One-paragraph:** Solopreneurs default-pick PH+HN+podcast launches because that's what the genre teaches, ignoring readiness (server capacity, support headroom) and funnel fit (lead-gen vs. revenue product). This methodology produces a one-page decision record that scores readiness, funnel fit, and retreat cost across four tiers (soft → friend → PH-day → blitz) and locks the chosen tier with rationale.

## Applies If (ALL must hold)

- Operator is planning a launch event in the next 14-60 days.
- Product is on a usable URL with a free demo path or trial.
- Operator can name funnel goal (signups / paid / waitlist / press).
- Operator has signal on server capacity + support headroom.

## Skip If (ANY kills it)

- Launch is already scheduled and tier is locked by external commitments — decision frame is moot.
- Operator does not know funnel goal — fix funnel goal first; tier follows from goal.
- Product has no usable demo path — push to soft-tier by default, no decision needed.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| funnel goal | enum | founder |
| server capacity snapshot | rps / concurrent | infra |
| support headroom | hours-per-day | operator |
| retreat-cost estimate | string | founder |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/product/launch-comms-kit-template` | Downstream — once tier is decided, the kit gets built for it. |
| `solo/product/mvp-instrumentation-checklist` | Upstream — instrumentation must be live for tier ≥2. |

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
| `score_readiness` | haiku | Bounded checklist score per tier. |
| `compare_tiers` | sonnet | Cross-tier judgement on funnel-fit + retreat-cost. |
| `lock_decision` | opus | Synthesis + rationale write-up. |

## Templates

| File | Purpose |
|---|---|
| `templates/launch-tier-decision-frame.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/launch-tier-decision-frame.md.j2` | Markdown skeleton with the required fields. |
| `templates/launch-tier-decision-frame.md` | Markdown skeleton with the required fields. Generated from `templates/launch-tier-decision-frame.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-launch-tier-decision-frame.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[launch-comms-kit-template]] — related methodology.
- [[mvp-instrumentation-checklist]] — related methodology.
- [[shutdown-customer-email-pack]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/launch-tier-decision-frame.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/launch-tier-decision-frame.json",
  "title": "Launch Tier Decision Frame Output Contract",
  "type": "object",
  "required": [
    "launch_name",
    "funnel_goal",
    "selected_tier",
    "readiness_score",
    "retreat_cost",
    "rationale",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "launch_name": {
      "type": "string",
      "description": "named launch"
    },
    "funnel_goal": {
      "type": "string",
      "description": "enum (signups | paid | waitlist | press | qualitative)"
    },
    "selected_tier": {
      "type": "integer",
      "description": "1-4 (soft / friend / ph-day / blitz)"
    },
    "readiness_score": {
      "type": "object",
      "description": "capacity + support + rollback subscores"
    },
    "retreat_cost": {
      "type": "string",
      "description": "concrete units"
    },
    "rationale": {
      "type": "string",
      "description": "\u2265200 chars"
    },
    "owner": {
      "type": "string",
      "description": "named human owner"
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
