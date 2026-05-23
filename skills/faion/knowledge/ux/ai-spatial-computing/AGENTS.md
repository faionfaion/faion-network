# AI Spatial Computing UX

## Summary

**One-sentence:** Spec for UX in spatial computing surfaces (Vision Pro, Meta Quest, AR overlays) where AI is the primary interaction modality — gaze, gesture, voice fused with multimodal models.

**One-paragraph:** Spec for UX in spatial computing surfaces (Vision Pro, Meta Quest, AR overlays) where AI is the primary interaction modality — gaze, gesture, voice fused with multimodal models. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a spec produced by an agent applying ai spatial computing ux. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible spec for ai spatial computing ux across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- target surface is a spatial-computing device (Vision Pro, Quest, smart-glasses) with persistent overlays
- interaction model fuses gaze + gesture + voice with a multimodal AI backend
- user is in motion or hands-free for ≥30% of the session

## Skip If (ANY kills it)

- flat-screen 2D phone or desktop UI — use ordinary UI methodology instead
- single-modality interface (voice-only kiosk, gesture-only sensor) — use multimodal-vui-design or specific-modality docs
- AR is decorative only (logo overlays, marketing demos) with no AI-driven response

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hardware capability sheet | Vision Pro / Quest / glasses spec doc | device vendor docs |
| Latency budget (interaction → response) | ms target end-to-end | perf team |
| Multimodal model selection | vision + voice + reasoning model triple | ml-engineering |
| Safety constraints | motion-sickness, fatigue, privacy of bystanders | compliance team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[multimodal-vui-design]] | Voice + visual fusion baseline |
| [[wcag-22-checklist]] | A11y for non-traditional surfaces |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `hardware_constraint_extract` | sonnet | Pull constraints from device spec sheet. |
| `interaction_pattern_design` | opus | Multi-modality fusion logic with safety guardrails. |
| `safety_guardrail_review` | opus | Cross-check motion-sickness, fatigue, bystander privacy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spatial-ux-spec.md` | Spec document skeleton for spatial-AI experience |
| `templates/interaction-budget.json` | Latency + comfort budget table |
| `templates/_smoke-test.md` | Minimum viable filled-in spatial-UX spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-spatial-computing.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[multimodal-vui-design]]
- [[generative-ui-design]]
- [[llm-powered-conversational-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
