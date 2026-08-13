# One Command Dev Env Template

## Summary

**One-sentence:** Produces a versioned decision-record artefact that captures the team's canonical "one command to reset local dev env" choice — the tool, the script entry point, the data fixtures it loads, and the named owner.

**Ефективно для:** Teams onboarding new developers on a product repo where local dev currently requires five tribal-knowledge steps and the runbook is stale or missing.

**One-paragraph:** Codifies the recurring `role-software-developer/Local dev env reset` decision into a single auditable record. The output names one accountable owner (no "we"/"team"), cites the input artefacts that justified the choice, carries semver + last_reviewed for decay control, and refuses untraceable claims. Designed for the gap identified by the role-software-developer playbook: per-language `make dev-up` templates exist for Python and JS in isolation, but no canonical decision-record exists for a product repo's full reset story.

## Applies If (ALL must hold)

- Task is an instance of `role-software-developer/Local dev env reset` OR a closely-adjacent variant.
- The operator has the artefacts named in Prerequisites available before starting.
- Output will be consumed by a downstream agent or human reviewer (not discarded).
- Tier == free or higher (gating enforced by tier-manifest).
- A single accountable owner can be named (no "team" / "we").

## Skip If (ANY kills it)

- The team already maintains a working artefact for this gap — replace, do not duplicate.
- The change being decided is a greenfield prototype with no production users.
- Regulatory / compliance context overrides any in-methodology guidance (defer to legal).
- Dev env is fully managed by the platform team (no per-repo decision needed).

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Recent context for `Local dev env reset` task (last 30 days) | text / chat log | engineering ticket |
| Write-access to the artefact store (repo / wiki / decision log) | repo path | repo admin |
| Named owner accountable for the output downstream | handle / email | team roster |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `free/dev/software-developer` | Parent role skill providing the operating context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate based on preconditions | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation. |
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|---|---|
| `templates/one-command-dev-env-template.json` | JSON schema for the output contract (machine-validatable). |
| `templates/one-command-dev-env-template.md` | Markdown skeleton with the required fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-one-command-dev-env-template.py` | Enforce the output contract. | After the subagent returns, before downstream consumer reads. |

## Related

- [[role-software-developer]] — parent role skill.
- Upstream playbook: `role-software-developer/Local dev env reset`.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? owner nameable? store writable?) and routes the decision into either "run-it" (produce the record) or "skip-it" (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/one-command-dev-env-template.json`

```json
{
  "_purpose": "JSON Schema for the One Command Dev Env Template decision-record output.",
  "_consumes": "nothing \u2014 schema only.",
  "_produces": "schema document.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~180 tokens.",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/one-command-dev-env-template.json",
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
      "pattern": "^[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
