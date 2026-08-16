# Product Explainability (PM Angle)

## Summary

**One-sentence:** PM-side communication discipline producing one canonical feature narrative (problem -> behaviour change -> outcome) and audience-specific renders for execs / sales / support / customers.

**One-paragraph:** One canonical narrative artefact owned by PM containing {problem, who, behaviour_change, outcome_metric, evidence_link}; derived audience renders never authored independently; 90-second test for brevity + clarity; outcome line is a customer-state change, not a feature-shipped statement. Output: feature-narrative YAML + per-audience renders.

**Ефективно для:**

- Pre-roadmap review: exec питає 'що цей продукт robi?', три PM відповідають по-різному.
- Pre-launch story prep для sales/support/customer-success без Loom.
- Board narrative: 6 місяців роботи у 90-секундну відповідь.
- Cross-team feature-to-impact mapping: який OKR/outcome зрушив.

## Applies If (ALL must hold)

- Pre-roadmap-review: an exec asks 'what does this product actually do?' and three PMs answer differently.
- Pre-launch story prep for sales/support/customer-success.
- Board / investor / all-hands narrative distilling work into a 90-second answer.
- Cross-team feature-to-impact mapping.
- Post-mortem on miscommunication where customer expected X, got Y.

## Skip If (ANY kills it)

- Infra-only release with no customer-visible change.
- Pre-launch where canonical narrative belongs to GTM, not PM.
- Pure internal-tool product with no external customer narrative needed.
- Stage so early no behaviour change yet observable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Verbatim user quotes | list | continuous-discovery output |
| Outcome metric | string + baseline | product-analytics |
| Audience inventory | list {exec, sales, support, customer} | stakeholder-management |
| Feature spec | markdown | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[continuous-discovery-habits]] | Supplies verbatim quotes grounding the evidence link. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: one canonical, derived renders, evidence link, 90-second test, outcome-not-feature | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for feature-narrative | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: three-versions, independent-renders, evidence-free, feature-as-outcome | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: extract -> author canonical -> render audiences -> 90s test -> publish | 800 |
| `content/05-examples.xml` | medium | Worked feature-narrative for a checkout-redesign release | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on customer-visibility + audience count | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `story-extract` | sonnet | Extract narrative from spec/research. |
| `audience-render` | haiku | Templated per-audience render derived from canonical. |
| `ninety-second-test` | haiku | Mechanical brevity + clarity check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-narrative-gate.sh` | Gate script enforcing 90s + outcome-not-feature. |
| `templates/prompt-audience-render.txt` | Audience-render prompt template. |
| `templates/prompt-story-extraction.txt` | Story-extraction prompt template. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-explainability.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[continuous-discovery-habits]]
- [[stakeholder-management]]
- [[release-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feature-narrative-gate.sh`

```bash
set -euo pipefail
#!/usr/bin/env bash
# feature-narrative-gate.sh — block release if narrative missing required fields or contains banned tokens.
# Usage: feature-narrative-gate.sh path/to/feature-narrative.json
# Exit: 0 = valid, 1 = validation failure
set -euo pipefail
fn="${1:?usage: feature-narrative-gate.sh NARRATIVE.json}"
schema="$(dirname "$0")/feature-narrative.schema.json"

cat > "$schema" <<'JSON'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["purpose","behavior_change","measurable_outcome","limit","affected_personas"],
  "properties": {
    "purpose":{"type":"string","minLength":20,"maxLength":200},
    "behavior_change":{"type":"object",
      "required":["before","after"],
      "properties":{"before":{"type":"string"},"after":{"type":"string"}}},
    "measurable_outcome":{"type":"object",
      "required":["metric","baseline","current","isolation_method"],
      "properties":{"metric":{"type":"string"},"baseline":{"type":"string"},
                    "current":{"type":"string"},
                    "isolation_method":{"enum":["a/b","holdout","pre/post","unverified"]}}},
    "limit":{"type":"string","minLength":15},
    "affected_personas":{"type":"array","minItems":1,"items":{
      "type":"object","required":["name","job","value_received"]}},
    "risks":{"type":"array"}
  }
}
JSON

ajv validate -s "$schema" -d "$fn" --strict=true || exit 1

banned='best|leading|revolutionary|seamless|powerful|next-gen|delight|thrilled|excited|delighted'
if grep -E -i "\"($banned)\"" "$fn" >/dev/null; then
  echo "FAIL: banned marketing token in narrative"; exit 1
fi
echo "OK: feature-narrative.json passes all gates"
```

### `templates/prompt-audience-render.txt`

```text
Render the feature-narrative.json for audience={exec|sales|support|customer|ai}.

Constraints by audience:
  exec:     <=200 words, lead with outcome and cost, single risk, no jargon.
  sales:    job + pain + capability + limit (verbatim) + 2 objection-handlers; cite source line.
  support:  symptom -> cause -> fix -> known-limit (verbatim); runbook tone.
  customer: <=80 words, plain language, second-person, link to docs.
  ai:       JSON array of {capability, status, since_version, limit} triples; no prose.

Forbidden tokens across all renders:
  "best", "leading", "revolutionary", "seamless", "powerful", "next-gen",
  "delight", "thrilled", "excited", "delighted", "top-tier", "category-defining".

Hard rules:
  - measurable_outcome.metric + baseline + current must be echoed verbatim; no rephrasing of numbers.
  - limit field must appear in every render, verbatim, never summarized or softened.
  - Do not publish. Output a draft only. A human must approve before distribution.
  - Use a different model family for the comprehension probe agent than for this render.
```

### `templates/prompt-story-extraction.txt`

```text
You extract a stakeholder-ready feature narrative. Inputs:
  <prd_path>{path to PRD or spec.md}</prd_path>
  <release_notes>{path or text}</release_notes>
  <telemetry_diff>{metric deltas before/after}</telemetry_diff>
  <impl_diff>{merged PR titles or commit log}</impl_diff>
  <research_clips>{user research excerpts if any}</research_clips>

Output JSON with exactly these fields:
  purpose (one sentence, no marketing adjectives, names the user job),
  behavior_change: {before: "...", after: "..."},
  measurable_outcome: {metric, baseline, current, isolation_method (a/b|holdout|pre/post|unverified)},
  limit (what it intentionally does NOT do, why),
  affected_personas[]: [{name, job, value_received}],
  risks[]: [{description}]

Hard rules:
  - Refuse to invent outcomes. If a metric is unverified write isolation_method="unverified".
  - Every field must cite the source document path in a parallel source_citations: {} field.
  - Flag any mismatch between PRD intent and impl_diff as "conflict" and block render until PM resolves.
  - Banned tokens in any string field: best, leading, revolutionary, seamless, powerful, next-gen, delight.
  - affected_personas must match names from the project personas registry; reject unknown personas.
```
