---
slug: shadcn-ui-architecture
tier: solo
group: dev
domain: frontend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: shadcn/ui architecture spec: vendored components/ui/ layer, CVA + cn() helpers, design-token bridge to Tailwind config, and the lift-path from ui/ → composed feature components.
content_id: "3062a208b38aab3e"
complexity: medium
produces: spec
est_tokens: 4900
tags: [shadcn-ui, architecture, component-layering, tailwind, cva]
---
# shadcn/ui Architecture

## Summary

**One-sentence:** shadcn/ui architecture spec: vendored components/ui/ layer, CVA + cn() helpers, design-token bridge to Tailwind config, and the lift-path from ui/ → composed feature components.

**One-paragraph:** shadcn/ui architecture spec: vendored components/ui/ layer, CVA + cn() helpers, design-token bridge to Tailwind config, and the lift-path from ui/ → composed feature components. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script `scripts/validate-shadcn-ui-architecture.py` enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- shadcn/ui Architecture — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `shadcn-ui-architecture` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Product needs a layered component system on top of vendored shadcn primitives.
- Multiple features share interaction patterns that should not be re-built per route.
- Design tokens (colors, radii, spacing) flow from a single source into Tailwind theme.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Single-page demo / throwaway prototype — layered architecture overkill.
- Team rejects vendored components and wants npm-only — wrong architecture root.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[shadcn-ui]] | Workflow context: related methodology in the same family |

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
| `fill-shadcn-ui-architecture-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-shadcn-ui-architecture.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shadcn-ui-architecture.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[shadcn-ui]]
- [[tailwind-architecture]]
- [[ui-lib-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (layering depth, token source, a11y coverage) to ui-only / ui+compounds / ui+compounds+feature-kits. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
