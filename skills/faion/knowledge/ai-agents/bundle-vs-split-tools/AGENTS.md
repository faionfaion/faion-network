# Bundle vs Split Tools

## Summary

**One-sentence:** Decides whether to bundle related tools into one composite with a mode arg or split them — default split below 25 tools; bundle only when modes share audience + arg shape and a 50-task eval confirms no quality loss.

**One-paragraph:** When tool count crosses ~25, model tool-selection accuracy collapses and tool-definition tokens dominate. Naive fix: bundle "search_email + search_slack + search_docs" into one search(source, query). Real fix: bundle only when the modes share an audience AND most argument shape AND the model has a training-data prior for that bundle pattern. This methodology produces one decision record per tool group recommending split / bundle / refactor and ships only after a 50-task eval shows no quality drop.

**Ефективно для:** Команд, у яких агент бачить 60+ tools і вибирає неправильний у 30% випадків; правильна декомпозиція знижує помилку у 2-3 рази без зміни моделі.

## Applies If (ALL must hold)

- Tool count is ≥ 20 OR tool-selection error rate > 5%.
- Eval set of ≥50 tasks exists or can be assembled.
- Tools are under your control (not third-party closed).
- Owner can run an A/B between split and bundled versions.
- Bundle change can be reverted on quality regression.

## Skip If (ANY kills it)

- Tool count < 20 — default to split.
- No eval set — bundling without measurement is guesswork.
- Single tool that does too much already — refactor it, don't bundle.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Tool inventory | name + description + schema | Tool catalogue |
| Tool-selection error rate | per-tool error rate from production traces | Observability |
| 50-task eval | jsonl with expected tool sequence | QA |
| Named owner | handle | Engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/enum-constraints-closed-vocabularies/AGENTS.md` | Mode-arg enum constraint. |
| `geek/ai/ai-agents/verb-object-tool-naming/AGENTS.md` | Naming rules for split tools. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 rules: threshold, decision procedure, enum-constrained mode | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision record | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: count? → shared audience+args? → eval delta? → bundle/split | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cluster_tools` | sonnet | Per-instance judgment on audience/args overlap. |
| `eval_bundle_proposal` | sonnet | Compose A/B eval design. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the decision record. |
| `templates/output.example.json` | Filled example. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the decision. | Before A/B rollout. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[enum-constraints-closed-vocabularies]] — mode enum.
- peer: [[verb-object-tool-naming]] — naming for split tools.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is tool count ≥25? (2) does a candidate group share audience + arg shape? (3) does the 50-task eval show ≤2% quality drop? Leaves point to "bundle", "split (default)", or "refactor the offending tool".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/bundle-vs-split-tools/output.json",
  "title": "Bundle Vs Split Tools Output",
  "description": "purpose=schema; consumes=brief+context; produces=artefact; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "version",
    "version_stamp",
    "produced_at",
    "rationale",
    "inputs_used"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "version_stamp": {
      "type": "string"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    },
    "fields": {
      "type": "object"
    },
    "rationale": {
      "type": "string",
      "minLength": 20
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  }
}
```

### `templates/output.example.json`

```json
{
  "artefact_id": "bundle-vs-split-tools-example-001",
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "version_stamp": "bundle-vs-split-tools@1.0.0",
  "produced_at": "2026-05-22T12:00:00Z",
  "fields": {
    "placeholder_field": "filled-by-author"
  },
  "rationale": "Example output for Bundle Vs Split Tools; references at least one named input.",
  "inputs_used": [
    "docs/brief.md"
  ]
}
```
