# Agency Risk Register Template

## Summary

**Ефективно для:**

- Micro-agency / consultancy з 3-25 людей.
- Weekly 30-min cadence з 8-column register.
- Revenue concentration, key-person, FX, contractor classification, pipeline.
- Auto-bumped score для будь-якого клієнта ≥40% trailing-90d revenue.

A weekly 30-minute risk-register cadence focused on agency-level risks (not just per-project): revenue concentration by client, key-person dependency, currency exposure, contractor classification, and pipeline thinness. Outcome: a one-page register the founder/PM can refresh every Monday in under 30 minutes, with each risk owned, scored, and given a trigger that escalates it from monitored to actioned.

## Applies If
- You run a micro-agency or consultancy with 3-25 people
- You bill foreign currency or hire across borders (FX or classification risk)
- You have >20% of revenue from a single client (concentration risk)
- You have at least one annual planning cycle and want a Monday cadence in between

## Skip If
- You are a solo freelancer with a single client (use freelancer-client-scorecard instead)
- You are an in-house product team (use project-level risk register)
- The agency has a dedicated CFO or COO who already runs enterprise-risk reviews
- You cannot commit 30 min/week for at least 8 weeks (without cadence, the register decays)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operating-trigger event | log / calendar / ticket | upstream observability |
| Methodology preconditions checklist | YAML | this methodology's `templates/agency-risk-register-template.md` |
| Named owner contact | string | team RACI / org chart |
| Write-access to artefact store | URL | team's knowledge space |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/proposal-from-discovery-template` | Upstream artefact template that anchors this methodology's recurring loop. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)
| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 7 testable rules: 6 agency-level risk classes, 8-column rows, 90-day concentration rule, key-person bus-factor, 30-min refresh, ≥15 score action, closed-risk archive |
| `content/03-failure-modes.xml` | 6 antipatterns with description + reason + repair |
| `content/02-output-contract.xml` | JSON Schema the artefact must satisfy. |
| `content/06-decision-tree.xml` | Routes observable inputs to a rule; read before drafting. |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour at the next iteration? |

## Templates

| File | Purpose |
|------|---------|
| `templates/agency-risk-register-template.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/agency-risk-register-template.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-risk-register-template.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related
- [[client-health-scorecard-agency]]
- [[capacity-vs-ask-balancer]]
- [[regulatory-uncertainty-buffer]]
- [[vendor-risk-assessment-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/agency-risk-register-template.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/agency-risk-register-template.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 3
    },
    "decision": {
      "type": "string",
      "minLength": 3
    },
    "rationale": {
      "type": "string",
      "minLength": 30
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```
