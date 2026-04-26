# Minimum Product Frameworks

## Summary

A selection matrix for choosing one of nine "minimum product" frameworks — MVP, MLP, MMP, MAC, RAT, MDP, MVA, MFP, SLC — before the first `spec.md` is written. The matrix maps market condition (blue/red ocean), buyer type (B2B/consumer), differentiator, and technical uncertainty to the right framework. Each choice must be versioned in a `framework-choice.md` with two explicit exit criteria before scoping begins.

## Why

"Just build an MVP" is the wrong default in crowded markets where users already have "good enough" alternatives. In red oceans, MVP can be strategically suicidal: users will not switch without a lovable, marketable, or technically superior alternative. The matrix forces a defensible framework choice based on market evidence, not reflex.

## When To Use

- New product or major module — before the first `spec.md` exists.
- Team is reflexively saying "let's ship an MVP" without checking market density, buyer type, or differentiator.
- Pivot moment: current build is failing on retention or conversion — re-pick the framework before re-scoping.
- Multiple stakeholders disagree on what "minimum" means — use the matrix as a forcing function.
- Pre-investment or pre-board memo: justify the chosen framework against blue/red ocean and ICP positioning.

## When NOT To Use

- Methodology already chosen and validated — go straight to that framework's scoping doc; do not re-litigate.
- Pure feature work inside a shipped product — use `release-planning`, `feature-prioritization-rice`, or MoSCoW instead.
- Hard-deadline regulated launches where scope is dictated by compliance, not strategy.
- Tiny fix-it-fast tasks (&lt;1 sprint) — framework choice overhead exceeds value.
- Internal tools with one stakeholder — pick MFP and move on.

## Content

| File | What's inside |
|------|---------------|
| `content/01-matrix.xml` | Nine frameworks with purpose and when-to-use; decision matrix by market condition; key insight on crowded-market risk. |
| `content/02-selection-process.xml` | Three-pass agentic selection flow, exit criteria requirement, framework limitations and failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/framework-choice.md` | Versioned choice document skeleton: chosen framework, rationale, exit criteria, history section. |
| `templates/pick-framework.sh` | Bash + Python: rule-based first-pass framework selection from `market-context.yml`; emits choice file for LLM review. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/pick-framework.sh` | Applies decision rules to market-context.yml; writes framework-choice.md; commits it to git. |
