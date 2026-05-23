# AI Plugin Ecosystem (Figma)

## Summary

**One-sentence:** Decision record that catalogues which Figma AI plugins fit which design task and where the agent/plugin boundary lies (no headless plugin API).

**One-paragraph:** Decision record that catalogues which Figma AI plugins fit which design task and where the agent/plugin boundary lies (no headless plugin API). This methodology codifies the rules, output contract, failure modes, and decision tree needed for a decision-record produced by an agent applying ai plugin ecosystem (figma). The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible decision-record for ai plugin ecosystem (figma) across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- team is evaluating which Figma AI plugins to adopt for a recurring workflow (content fill, icon gen, audit)
- automation target is repetitive design work (bulk rename, content population, icon generation) over ≥20 components
- adoption decision needs to be recorded with accessibility and brand guardrails

## Skip If (ANY kills it)

- final production asset export — AI plugin outputs require human QA before handoff
- design system architecture decisions — plugins assist but cannot own system architecture
- small one-off task (<20 components) where plugin setup time exceeds manual effort
- data-privacy-sensitive contexts (healthcare, finance PII) where plugin sends data to external services

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inventory of repetitive tasks | spreadsheet / Notion table | design ops |
| Brand styles in Figma (variables, type styles) | Figma library | design-system team |
| Plugin shortlist with versions | list of 3-7 candidate plugins | designer evaluation |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[figma-ai-ecosystem]] | Broader Figma AI surface — plugins are one slice |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plugin_capability_match` | sonnet | Compare plugin spec to task list; rank fit. |
| `data_privacy_check` | sonnet | Trace plugin data flow to external services; flag PII risk. |
| `decision_record_write` | sonnet | Compose final ADR-style decision. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | ADR-style decision record skeleton for plugin adoption |
| `templates/plugin-capability-matrix.json` | Capability vs task matrix skeleton |
| `templates/_smoke-test.md` | Minimum viable filled-in plugin-adoption ADR |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-plugin-ecosystem.py` | Validate the decision-record artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[figma-ai-ecosystem]]
- [[ai-generated-layout-review-checklist]]
- [[generative-ui-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
