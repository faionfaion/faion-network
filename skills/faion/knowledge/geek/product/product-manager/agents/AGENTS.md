# Product Manager Agents

## Summary

Two Claude subagents for product scoping work: `faion-mvp-scope-analyzer-agent` analyzes competitor features to recommend a minimum feature set for a new product; `faion-mlp-agent` upgrades an MVP to an MLP (Minimum Lovable Product) through a five-mode sequential pipeline (analyze → find-gaps → propose → update → plan). The MLP dimensions are Delight, Ease, Speed, Trust, and Personality.

## Why

Defining MVP scope without competitor grounding leads to either over-building (scope creep) or under-building (no differentiation). MLP work surfaces the "WOW" features that make a product memorable rather than just functional. The five-mode pipeline enforces sequencing discipline: gap analysis is meaningless without a current-state baseline, and spec updates should never happen before human review of proposed features.

## When To Use

- Defining MVP scope for a new product where competitor analysis is needed
- Upgrading an MVP to an MLP before a roadmap planning session
- Running structured gap analysis between current product state and MLP targets
- Sequencing MLP feature implementation when multiple WOW features compete for prioritization

## When NOT To Use

- Product is at ideation stage only with no existing specs or MVP definition — start with discovery first
- Competitor landscape is entirely novel with no comparable products (MVP scope analyzer needs comparables)
- Team is mid-sprint or in code freeze — run analyze and find-gaps only, defer update until ready
- B2B enterprise with highly custom requirements where generic MLP dimensions do not apply without significant modification

## Content

| File | What's inside |
|------|---------------|
| `content/01-agents.xml` | Agent reference cards: faion-mvp-scope-analyzer-agent and faion-mlp-agent with all five modes |
| `content/02-pipeline.xml` | Sequential pipeline rules, human-in-the-loop checkpoints, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/mlp-pipeline.py` | Sequential five-mode MLP pipeline coordinator with error handling |
