# AI Failure Mode Taxonomy

## Summary

**One-sentence:** Produces a closed taxonomy of 12 LLM failure modes (hallucination, IPI, refusal-bypass, schema-drop, latency-spike, cost-blowup, etc.) with detector + severity + linked methodology, anchoring every eval, alert, and incident.

**One-paragraph:** Different teams in the same company name the same failure differently — "hallucination" / "fabrication" / "drift" — making evals incomparable, alerts inconsistent, and postmortems irreproducible. A closed taxonomy enumerates exactly 12 named failure modes (with id + definition + detector + severity + linked-methodology) and forbids ad-hoc additions. Every eval case, alert rule, and incident ticket references one mode id; reports across teams become commensurable.

**Ефективно для:** multi-team AI orgs, postmortem libraries, eval-set design, alert routing, on-call runbooks, vendor-cross-comparison.

## Applies If (ALL must hold)

- ≥2 teams build / operate LLM-backed features and share a postmortem / alert channel.
- A central owner can publish + version the taxonomy.
- Existing eval cases / incidents can be re-tagged to the new ids.
- Tooling (dashboards, alerts) can read the mode id as a column / label.

## Skip If (ANY kills it)

- Single team, single feature — overhead exceeds the benefit.
- No central owner — taxonomy will fork within months.
- Tooling cannot consume the ids — output is documentation rot.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Recent incidents | tickets / JSONL | incident log |
| Existing eval categories | strings | eval harness |
| Alert rule names | strings | observability config |
| Owner & cadence | doc | team charter |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[llm-drift-daily-triage]]` | Daily report references taxonomy ids. |
| `[[indirect-prompt-injection-defense]]` | IPI mode is part of the taxonomy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: closed 12-mode set, every mode has detector+severity, version + change log, no ad-hoc ids, eval+alert+ticket link mandatory, quarterly review | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for taxonomy.json: array of {id, name, detector, severity, linked_methodology} | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns of taxonomies themselves: open list, no detectors, severity-uniform, no link to mitigations, retire-and-forget | ~600 |
| `content/04-procedure.xml` | medium | 6-step: pull existing → cluster to 12 → write detectors → assign severity → link methodology → publish | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "≥2 teams + central owner present?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Cluster existing categories | opus | Semantic reasoning. |
| Author detectors | sonnet | Concrete signal definitions. |
| Assign severities | opus | Cross-business reasoning. |
| Wire ids into dashboards | haiku | Mechanical config edit. |

## Templates

| File | Purpose |
|---|---|
| `templates/taxonomy.schema.json` | JSON Schema for taxonomy.json. |
| `templates/taxonomy-skeleton.json` | 12-mode skeleton with placeholder detectors. |
| `templates/incident-template.md.j2` | Postmortem template that references a mode id. |
| `templates/incident-template.md` | Postmortem template that references a mode id. Generated from `templates/incident-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum valid 12-mode taxonomy. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-failure-mode-taxonomy.py` | Validates taxonomy.json: exactly 12 modes, no duplicate ids, every mode has detector+severity+linked_methodology. | Pre-commit on taxonomy.json; CI before publishing. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[llm-drift-daily-triage]]`
- `[[indirect-prompt-injection-defense]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` decides whether to formalise: single team or no owner → skip; multi-team + central owner → run procedure; mid-state (multi-team no owner) → escalate to leadership before adopting.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/taxonomy.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/ai-failure-mode-taxonomy",
  "_purpose": "Schema for the closed 12-mode taxonomy.",
  "_consumes": "operator-authored taxonomy.json",
  "_produces": "validation verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "validator only",
  "type": "object",
  "required": [
    "version",
    "owner",
    "modes"
  ],
  "properties": {
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1
    },
    "modes": {
      "type": "array",
      "minItems": 12,
      "maxItems": 12,
      "items": {
        "type": "object",
        "required": [
          "id",
          "name",
          "definition",
          "detector",
          "severity",
          "linked_methodology"
        ],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^fm\\.[a-z0-9-]+(\\.[a-z0-9-]+)+$"
          },
          "name": {
            "type": "string"
          },
          "definition": {
            "type": "string",
            "minLength": 20
          },
          "detector": {
            "type": "string",
            "minLength": 10
          },
          "severity": {
            "enum": [
              "low",
              "medium",
              "high",
              "critical"
            ]
          },
          "linked_methodology": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    }
  }
}
```

### `templates/taxonomy-skeleton.json`

```json
{
  "_purpose": "12-mode seed taxonomy; teams should adapt detectors + linked_methodology to their stack but keep ids + names stable.",
  "_consumes": "incident clustering output",
  "_produces": "taxonomy.json that passes the validator",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "docs-only",
  "version": "1.0.0",
  "owner": "ml-platform",
  "modes": [
    {
      "id": "fm.hallucination.fabricated-api",
      "name": "Fabricated API",
      "definition": "Model emits a library or endpoint that does not exist.",
      "detector": "import-check against allow-list of installed packages.",
      "severity": "high",
      "linked_methodology": "jailbreak-eval-suite-bootstrap"
    },
    {
      "id": "fm.hallucination.fabricated-fact",
      "name": "Fabricated fact",
      "definition": "Model emits a factual claim with no source.",
      "detector": "fact-claim regex without citation marker.",
      "severity": "medium",
      "linked_methodology": "judge-calibration-protocol"
    },
    {
      "id": "fm.refusal.over-refusal",
      "name": "Over-refusal",
      "definition": "Model refuses a benign request.",
      "detector": "refusal-rate spike on benign holdout.",
      "severity": "medium",
      "linked_methodology": "judge-calibration-protocol"
    },
    {
      "id": "fm.refusal.bypass",
      "name": "Refusal bypass",
      "definition": "Model complies with a request that should be refused.",
      "detector": "jailbreak eval suite case pass.",
      "severity": "critical",
      "linked_methodology": "jailbreak-eval-suite-bootstrap"
    },
    {
      "id": "fm.security.indirect-prompt-injection",
      "name": "IPI",
      "definition": "Instructions in retrieved content hijack a tool call.",
      "detector": "canary token in outbound tool payload.",
      "severity": "critical",
      "linked_methodology": "indirect-prompt-injection-defense"
    },
    {
      "id": "fm.security.exfiltration",
      "name": "Exfiltration",
      "definition": "Sensitive data leaves via outbound tool.",
      "detector": "canary or DLP regex on outbound payload.",
      "severity": "critical",
      "linked_methodology": "indirect-prompt-injection-defense"
    },
    {
      "id": "fm.output.schema-drop",
      "name": "Schema drop",
      "definition": "Required field missing in structured output.",
      "detector": "JSON Schema validation fail.",
      "severity": "high",
      "linked_methodology": "guardrails-implementation"
    },
    {
      "id": "fm.output.format-drift",
      "name": "Format drift",
      "definition": "Output type drifts (string where number expected).",
      "detector": "type check on parsed output.",
      "severity": "medium",
      "linked_methodology": "guardrails-implementation"
    },
    {
      "id": "fm.latency.spike",
      "name": "Latency spike",
      "definition": "Per-call p95 latency breaches site SLO.",
      "detector": "SLO alert.",
      "severity": "medium",
      "linked_methodology": "latency-vs-quality-decision-grid"
    },
    {
      "id": "fm.cost.blowup",
      "name": "Cost blowup",
      "definition": "Per-call cost increases >25% week-over-week.",
      "detector": "FinOps dashboard threshold.",
      "severity": "high",
      "linked_methodology": "ai-cost-attribution-schema"
    },
    {
      "id": "fm.tool.misuse",
      "name": "Tool misuse",
      "definition": "Model invokes wrong tool or wrong arguments.",
      "detector": "tool-call trace divergence from intent label.",
      "severity": "high",
      "linked_methodology": "function-calling-patterns"
    },
    {
      "id": "fm.context.bleed",
      "name": "Context bleed",
      "definition": "Prior conversation leaks into a new session.",
      "detector": "PII / prior-id appearance in new-session output.",
      "severity": "high",
      "linked_methodology": "guardrails-implementation"
    }
  ]
}
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "12-mode seed taxonomy; teams should adapt detectors + linked_methodology to their stack but keep ids + names stable.",
  "_consumes": "incident clustering output",
  "_produces": "taxonomy.json that passes the validator",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "docs-only",
  "version": "1.0.0",
  "owner": "ml-platform",
  "modes": [
    {
      "id": "fm.hallucination.fabricated-api",
      "name": "Fabricated API",
      "definition": "Model emits a library or endpoint that does not exist.",
      "detector": "import-check against allow-list of installed packages.",
      "severity": "high",
      "linked_methodology": "jailbreak-eval-suite-bootstrap"
    },
    {
      "id": "fm.hallucination.fabricated-fact",
      "name": "Fabricated fact",
      "definition": "Model emits a factual claim with no source.",
      "detector": "fact-claim regex without citation marker.",
      "severity": "medium",
      "linked_methodology": "judge-calibration-protocol"
    },
    {
      "id": "fm.refusal.over-refusal",
      "name": "Over-refusal",
      "definition": "Model refuses a benign request.",
      "detector": "refusal-rate spike on benign holdout.",
      "severity": "medium",
      "linked_methodology": "judge-calibration-protocol"
    },
    {
      "id": "fm.refusal.bypass",
      "name": "Refusal bypass",
      "definition": "Model complies with a request that should be refused.",
      "detector": "jailbreak eval suite case pass.",
      "severity": "critical",
      "linked_methodology": "jailbreak-eval-suite-bootstrap"
    },
    {
      "id": "fm.security.indirect-prompt-injection",
      "name": "IPI",
      "definition": "Instructions in retrieved content hijack a tool call.",
      "detector": "canary token in outbound tool payload.",
      "severity": "critical",
      "linked_methodology": "indirect-prompt-injection-defense"
    },
    {
      "id": "fm.security.exfiltration",
      "name": "Exfiltration",
      "definition": "Sensitive data leaves via outbound tool.",
      "detector": "canary or DLP regex on outbound payload.",
      "severity": "critical",
      "linked_methodology": "indirect-prompt-injection-defense"
    },
    {
      "id": "fm.output.schema-drop",
      "name": "Schema drop",
      "definition": "Required field missing in structured output.",
      "detector": "JSON Schema validation fail.",
      "severity": "high",
      "linked_methodology": "guardrails-implementation"
    },
    {
      "id": "fm.output.format-drift",
      "name": "Format drift",
      "definition": "Output type drifts (string where number expected).",
      "detector": "type check on parsed output.",
      "severity": "medium",
      "linked_methodology": "guardrails-implementation"
    },
    {
      "id": "fm.latency.spike",
      "name": "Latency spike",
      "definition": "Per-call p95 latency breaches site SLO.",
      "detector": "SLO alert.",
      "severity": "medium",
      "linked_methodology": "latency-vs-quality-decision-grid"
    },
    {
      "id": "fm.cost.blowup",
      "name": "Cost blowup",
      "definition": "Per-call cost increases >25% week-over-week.",
      "detector": "FinOps dashboard threshold.",
      "severity": "high",
      "linked_methodology": "ai-cost-attribution-schema"
    },
    {
      "id": "fm.tool.misuse",
      "name": "Tool misuse",
      "definition": "Model invokes wrong tool or wrong arguments.",
      "detector": "tool-call trace divergence from intent label.",
      "severity": "high",
      "linked_methodology": "function-calling-patterns"
    },
    {
      "id": "fm.context.bleed",
      "name": "Context bleed",
      "definition": "Prior conversation leaks into a new session.",
      "detector": "PII / prior-id appearance in new-session output.",
      "severity": "high",
      "linked_methodology": "guardrails-implementation"
    }
  ]
}
```
