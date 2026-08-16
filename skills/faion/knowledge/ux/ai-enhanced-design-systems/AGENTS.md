# AI-Enhanced Design Systems (UX/UI)

## Summary

**One-sentence:** Produces a UX/UI design-system automation config (auto-docs + token scan + Figma-to-code diff + variant generator) that requires a solid token foundation and consistent naming.

**One-paragraph:** Distinct from the ui-designer counterpart by Figma-to-code diff integration — bridging design source-of-truth with code consumers. This methodology produces a YAML config wiring four pipelines: (1) auto-doc generation from component code + Figma component metadata, (2) token-violation scanner, (3) Figma-to-code diff (drift detector at the boundary), (4) variant generator gated by visual regression. Requires mature tokens + consistent naming as prerequisite.

**Ефективно для:** UX/UI staff designer, що автоматизує DS bridge між Figma + code — auto-docs / token scan / Figma-code diff.

## Applies If (ALL must hold)

- Mature DS with tokens + naming consistency + ≥80 % story coverage.
- Figma library is the design source-of-truth and code repo mirrors it.
- Visual regression provider integrated.

## Skip If (ANY kills it)

- Tokens not codified.
- Figma library is decorative (not source-of-truth).
- Naming inconsistent across components.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Token map (Style Dictionary / JSON) | JSON | DS team |
| Figma library file key | string | design |
| Component source root | filesystem path | engineering |
| Visual regression creds | secret | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[ai-design-assistant-patterns]] (ux-ui-designer) | Sibling: AI assistant pattern catalogue. |
| [[design-system-drift-dashboard]] | Drift instrumentation companion. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end. | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-config` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/ds-automation.config.yaml` | YAML config: ds_root + figma + tokens + doc_gen + scanner + figma-code diff + variant + review. |
| `templates/figma-diff.config.json` | Figma-to-code diff config: file_key + glob + drift threshold. |
| `templates/_smoke-test.yaml` | Filled minimum-viable config example. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-enhanced-design-systems.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-design-assistant-patterns]]
- [[design-system-drift-dashboard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the config; mis-routing leads to producing the wrong artefact shape.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ds-automation.config.yaml`

```yaml
# ds-automation.config.yaml — AI-Enhanced Design Systems (UX/UI)
# Fill per task; validator: scripts/validate-ai-enhanced-design-systems.py

ds_root: packages/ds
figma_file_key: AbCdEf1234567890
token_map: packages/ds/tokens.json
doc_generator: {"source": "packages/ds/src", "story_root": "packages/ds/stories", "figma_metadata": "true", "output": "packages/ds/docs"}
token_scanner: {"block_on_violation": true}
figma_code_diff: {"block_on_drift": true}
variant_generator: {"visreg_provider": "chromatic"}
human_review_required: true
```

### `templates/figma-diff.config.json`

```json
{
  "ds_root": "FILL_ME",
  "figma_file_key": "FILL_ME",
  "token_map": "FILL_ME",
  "doc_generator": {
    "source": "packages/ds/src",
    "story_root": "packages/ds/stories",
    "figma_metadata": "true",
    "output": "packages/ds/docs"
  },
  "token_scanner": {
    "block_on_violation": true
  },
  "figma_code_diff": {
    "block_on_drift": true
  },
  "variant_generator": {
    "visreg_provider": "chromatic"
  },
  "human_review_required": true
}
```

### `templates/_smoke-test.yaml`

```yaml
# _smoke-test.yaml — AI-Enhanced Design Systems (UX/UI)
# Fill per task; validator: scripts/validate-ai-enhanced-design-systems.py

ds_root: packages/ds
figma_file_key: AbCdEf1234567890
token_map: packages/ds/tokens.json
doc_generator: {"source": "packages/ds/src", "story_root": "packages/ds/stories", "figma_metadata": "true", "output": "packages/ds/docs"}
token_scanner: {"block_on_violation": true}
figma_code_diff: {"block_on_drift": true}
variant_generator: {"visreg_provider": "chromatic"}
human_review_required: true
```
