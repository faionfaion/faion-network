# Company Prompt Library Pattern

## Summary

**One-sentence:** Produces a versioned spec describing a company's checked-in `prompts/` library — namespace map (per-role / per-task), the override layer between faion defaults and company patterns, the eval gate, and the named owner.

**Ефективно для:** Engineering organisations adopting an LLM agent (Faion / Claude Code / Cursor) where every dev currently copy-pastes prompts from chat UIs, prompts are not versioned, and there is no canonical company tone / context / coding-convention layer.

**One-paragraph:** Pins the recurring "adopt agent org-wide and override with company patterns" decision into one auditable spec. The spec names a single accountable owner, a layered namespace (faion defaults → role-pack → company override → repo override), an eval gate that blocks prompt PRs without a rubric pass, and a regression-detection plan. Designed for teams that have already passed the "should we use an LLM" gate and now need the prompt artefacts to be first-class citizens in the software lifecycle — tested, governed, and deployed with the same rigour as code.

## Applies If (ALL must hold)

- Team has ≥3 developers all interacting with an LLM coding agent independently.
- No checked-in `prompts/` directory exists, OR existing one has no owner / no eval gate.
- A single accountable owner can be named (no "team" / "we").
- Output will be consumed by a downstream PR template + CI eval job (not a one-off doc).
- Tier == geek or higher (gating enforced by tier-manifest).

## Skip If (ANY kills it)

- The team already runs a working prompt library with evals and an owner — improve, do not rewrite.
- The org has < 3 LLM-using devs — overhead is not justified.
- Regulatory regime mandates a vendor governance platform — defer to vendor's authoring flow.
- Single-use throwaway tool — versioned library is overkill.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Inventory of currently-used prompts across the org (last 30 days) | csv / sheet | manual sweep + git log + chat history |
| Existing role definitions (PM / dev / QA / SRE) | text / wiki | team roster |
| Company tone-of-voice doc, if any | md | brand / comms repo |
| Repo's CONVENTIONS.md / AGENTS.md | md | code repo root |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/llm-integration` | parent skill — provides operating context for LLM-using teams |
| `geek/ai/claude-code` | required when the agent is Claude Code |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-named-namespace, r2-layered-override, r3-eval-gate, r4-versioned-prompt, r5-owner-on-every-pack | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the spec output + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: shared-clipboard / hidden-prompts / no-eval / drift-without-detection / scope-creep | ~900 |
| `content/04-procedure.xml` | essential | 6-step procedure: inventory → namespace → override → eval gate → owner → rollout | ~1100 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + namespace-size branching | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `inventory_existing_prompts` | haiku | Bounded grep + summarise |
| `draft_namespace_map` | sonnet | Per-org judgment with bounded inputs |
| `synthesize_eval_gate_spec` | opus | High-stakes architecture decision |

## Templates

| File | Purpose |
|---|---|
| `templates/company-prompt-library-pattern.json` | JSON schema for the spec output contract |
| `templates/company-prompt-library-pattern.md.j2` | Markdown skeleton with the required fields |
| `templates/company-prompt-library-pattern.md` | Markdown skeleton with the required fields Generated from `templates/company-prompt-library-pattern.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-company-prompt-library-pattern.py` | Enforce the output contract | After the subagent returns, before downstream consumer reads |

## Related

- [[eval-contract-template]] — wire up the eval gate this methodology mandates.
- Upstream playbook: `p6-product-dev-team/Adopt faion org-wide and override with company patterns`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question tree: (1) preconditions present? (inventory + owner + ≥3 devs) → no = skip; yes (2) library size < 20 prompts? → emit single-file library spec; ≥20 → emit per-role-pack namespace spec. Both terminal branches reference rules in `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/company-prompt-library-pattern.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/company-prompt-library-pattern.json",
  "type": "object",
  "required": [
    "spec_id",
    "owner",
    "namespace_map",
    "override_layers",
    "eval_gate",
    "role_packs",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "spec_id": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "namespace_map": {
      "type": "object",
      "patternProperties": {
        "^prompts/(role|task)/[a-z0-9-]+/$": {
          "type": "string",
          "minLength": 1
        }
      },
      "additionalProperties": false,
      "minProperties": 1
    },
    "override_layers": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "faion-defaults",
          "role-pack",
          "company-override",
          "repo-override"
        ]
      },
      "minItems": 4,
      "maxItems": 4,
      "uniqueItems": true
    },
    "eval_gate": {
      "type": "object",
      "required": [
        "scorers",
        "threshold",
        "block_on_fail"
      ],
      "properties": {
        "scorers": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "minItems": 1
        },
        "threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "block_on_fail": {
          "type": "boolean",
          "const": true
        }
      }
    },
    "role_packs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "owner",
          "count"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "owner": {
            "type": "string",
            "minLength": 1
          },
          "count": {
            "type": "integer",
            "minimum": 0
          }
        }
      }
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "status": {
      "type": "string",
      "enum": [
        "draft",
        "active",
        "deprecated"
      ]
    }
  }
}
```
