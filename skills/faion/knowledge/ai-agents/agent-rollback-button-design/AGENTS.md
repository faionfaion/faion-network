# Agent Rollback Button Design

## Summary

**One-sentence:** Designs the operator-facing rollback button for an agent feature — what it reverts (prompt + schema + tools + model + eval set), what it preserves (customer state, conversation history), and the eval that gates the rollback decision.

**One-paragraph:** Rolling back an agent is harder than rolling back a microservice because prompts, output schemas, tool registries, eval sets, and model versions are coupled. This methodology produces a single spec that names the atomic rollback unit ("bundle"), the reversible-fields list, the immutable-fields list (customer messages, billing events), and the eval gate (pass-rate ± CI on a frozen golden set) that must trip before the button is enabled. Output is a versioned spec downstream platform engineers can implement against.

**Ефективно для:** Команд, де агент уже в проді й один прокол може коштувати клієнтів, але «відкатити» означає десять різних реєстрів — спека за день дає одну кнопку, яка дійсно повертає до робочого стану, без побічних ефектів на customer history.

## Applies If (ALL must hold)

- Agent feature is in production or shadow-production with real users.
- At least two prior agent versions exist (otherwise there is nothing to roll back to).
- A frozen golden eval set ≥30 examples is available.
- Per-customer state (conversation history, account artefacts) must be preserved across rollbacks.
- Named platform owner can implement the spec within one sprint.

## Skip If (ANY kills it)

- Pre-MVP exploration where the feature changes daily.
- Single-user prototype with no customer state to preserve.
- Cost-prohibitive eval gate when cheaper proxies (intermediate-metric regression) cover the risk.
- Hosted/closed agent product where prompt + schema + tools are not under your control.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Bundle definition | YAML/JSON listing prompt+schema+tools+model SHAs | Platform repo |
| Golden eval set | jsonl ≥30 examples with expected outputs | QA / data team |
| Customer-state schema | DDL or JSON Schema for messages/accounts tables | DB owner |
| Rollback runbook (prior) | Markdown | Ops |
| Named owner | handle/email | Operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-ga-readiness-checklist/AGENTS.md` | GA readiness frames rollback as one of the gates. |
| `geek/ai/ai-agents/agent-kill-switch-design/AGENTS.md` | Sibling — kill-switch is the harder cousin of rollback. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: bundled-rollback, immutable-customer-state, eval-gated, single-button, audit-log | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the rollback-button spec | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (partial rollback, lost messages, no eval gate, missing audit, race) | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: enumerate fields → split mutable/immutable → wire eval gate → draft button spec → review | ~1000 |
| `content/05-examples.xml` | medium | Worked example: rollback spec for a customer-support agent | ~1000 |
| `content/06-decision-tree.xml` | essential | Tree: bundle defined? → customer state isolated? → eval gate available? → ship/split/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate_bundle_fields` | haiku | Structured extraction from bundle YAML. |
| `partition_mutable_immutable` | sonnet | Domain judgment — which fields touch customer state. |
| `author_spec` | sonnet | Composes the spec. |
| `review_for_data_safety` | opus | High-stakes: lost customer messages cannot be recovered. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the rollback-button spec. |
| `templates/rollback-spec.example.json` | Filled minimal valid example. |
| `templates/rollback-spec.md.j2` | Markdown skeleton with required sections. |
| `templates/rollback-spec.md` | Markdown skeleton with required sections. Generated from `templates/rollback-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the spec against the JSON Schema. | After subagent emits spec, before platform team accepts ticket. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-kill-switch-design]] — kill switch is the harder version (no graceful state preservation).
- peer: [[agent-ga-readiness-checklist]] — rollback is a checklist item there.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is the rollback bundle atomically defined? (2) is customer state cleanly partitioned from agent code? (3) does an eval gate exist? Leaves point to "ship spec", "split — define bundle first", or "escalate — closed-source dependency blocks atomic rollback".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/agent-rollback-button-design/spec.json",
  "title": "Agent Rollback Button Spec",
  "description": "purpose=schema; consumes=bundle+immutable+eval; produces=rollback-button-spec; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "spec_id",
    "environment",
    "bundle_fields",
    "immutable_fields",
    "eval_gate",
    "button_label",
    "audit_log_path",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "spec_id": {
      "type": "string",
      "minLength": 3
    },
    "environment": {
      "type": "string",
      "enum": [
        "prod",
        "staging",
        "shadow"
      ]
    },
    "bundle_fields": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    },
    "immutable_fields": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    },
    "eval_gate": {
      "type": "object",
      "required": [
        "golden_set_version",
        "min_pass_rate"
      ],
      "properties": {
        "golden_set_version": {
          "type": "string"
        },
        "min_pass_rate": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "ci_width": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        }
      },
      "additionalProperties": false
    },
    "button_label": {
      "type": "string",
      "maxLength": 40
    },
    "audit_log_path": {
      "type": "string",
      "minLength": 1
    },
    "owner": {
      "type": "string",
      "minLength": 1
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

### `templates/rollback-spec.example.json`

```json
{
  "spec_id": "rollback-customer-support-agent",
  "environment": "prod",
  "bundle_fields": [
    "prompt_sha",
    "schema_version",
    "tool_registry_sha",
    "model",
    "eval_set_version",
    "retrieval_index_version"
  ],
  "immutable_fields": [
    "conversations.messages",
    "conversations.metadata",
    "accounts.*",
    "audit_log.*",
    "feedback.scores"
  ],
  "eval_gate": {
    "golden_set_version": "support-golden-v3-frozen-2026-05-15",
    "min_pass_rate": 0.78,
    "ci_width": 0.04
  },
  "button_label": "Rollback to previous stable",
  "audit_log_path": "s3://faion-ops/audit/rollbacks/",
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
