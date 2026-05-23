# Claude-Driven UX Methodology Bundle

## Summary

**One-sentence:** Playbook step that selects which UX-methodology bundle Claude should load given the design task at hand (heuristic eval, generative UI, plugin choice, spatial, VUI).

**One-paragraph:** Playbook step that selects which UX-methodology bundle Claude should load given the design task at hand (heuristic eval, generative UI, plugin choice, spatial, VUI). This methodology codifies the rules, output contract, failure modes, and decision tree needed for a playbook-step produced by an agent applying claude-driven ux methodology bundle. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible playbook-step for claude-driven ux methodology bundle across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- designer or design-PM is at the start of a UX task and needs Claude to load the right methodology
- the task is one of: heuristic eval, generative UI build, plugin selection, spatial design, conversational UI
- the routing decision must be deterministic + auditable

## Skip If (ANY kills it)

- task is non-UX (engineering, marketing, ops) — use the relevant domain methodology
- task is research synthesis or quant analysis only — use research domain methodology
- user already knows which methodology to load — bypass the router

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task description | 1-3 sentences | user prompt |
| Known constraints | device, surface, modality, AI involvement | user prompt |
| Methodology catalog snapshot | current list of geek/ux methodologies | L2 INDEX.xml |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[AGENTS.md]] | Parent skill context |

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
| `task_signal_extract` | haiku | Lift signals from prompt: surface, modality, AI involvement. |
| `methodology_match` | sonnet | Apply routing rules to pick 1-3 methodologies. |
| `load_and_brief` | sonnet | Compose the loading instruction for downstream agent. |

## Templates

| File | Purpose |
|------|---------|
| `templates/routing-step.md` | Playbook-step skeleton for the routing decision |
| `templates/signal-extraction.json` | Signal extraction JSON skeleton |
| `templates/_smoke-test.md` | Minimum viable filled-in routing step |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-CLAUDE-methodologies.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[ai-generated-layout-review-checklist]]
- [[generative-ui-design]]
- [[multimodal-vui-design]]
- [[ai-plugin-ecosystem]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
