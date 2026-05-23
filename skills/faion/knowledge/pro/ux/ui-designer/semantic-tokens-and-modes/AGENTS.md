---
slug: semantic-tokens-and-modes
tier: pro
group: ux
domain: frontend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spec for a semantic-token layer (`color.surface.brand`, `color.text.muted`) sitting between primitives and components, with mode definitions (light/dark/high-contrast/density) and Figma variable bindings.
content_id: "35190fb8dc7ad8fd"
complexity: medium
produces: spec
est_tokens: 4900
tags: [design-tokens, theming, semantic-layer, figma-variables, modes]
---
# Semantic Tokens and Modes

## Summary

**One-sentence:** Spec for a semantic-token layer (`color.surface.brand`, `color.text.muted`) sitting between primitives and components, with mode definitions (light/dark/high-contrast/density) and Figma variable bindings.

**One-paragraph:** Spec for a semantic-token layer (`color.surface.brand`, `color.text.muted`) sitting between primitives and components, with mode definitions (light/dark/high-contrast/density) and Figma variable bindings. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Adding dark-mode and high-contrast modes without forking the primitive palette.
- Eliminating per-component colour overrides that fight the system.
- Mapping semantic tokens to Figma variables so designers stop hard-coding hex.
- Auditing semantic vocabulary for naming consistency before a v2 cut.
- Wiring mode switches to OS-level prefers-color-scheme correctly.

## Applies If (ALL must hold)

- The triggering activity for semantic-tokens-and-modes appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/` parent skill context | vocabulary, neighbouring methodologies |
| [[token-organization]] | upstream context this methodology builds on |
| [[cross-platform-token-distribution]] | upstream context this methodology builds on |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-semantic-tokens-and-modes-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |


## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-<slug>.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-semantic-tokens-and-modes.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |


## Related

- [[token-organization]]
- [[cross-platform-token-distribution]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
