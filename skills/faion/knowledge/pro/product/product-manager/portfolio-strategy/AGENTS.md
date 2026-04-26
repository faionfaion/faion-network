# Portfolio Strategy (70/20/10)

## Summary

Allocates product investment across three horizons: 70% Core (H1, known market, 0-12 months), 20% Adjacent (H2, new segments, 12-24 months), 10% Transformational (H3, breakthrough bets, 24-36 months). In economic downturns shift to 80/15/5; in growth periods to 60/25/15. The PM-level focus is separating single-product PM execution from portfolio-PM cross-product trade-offs.

## Why

Without explicit horizon allocation, PMs optimize locally — all backlog items drift to H1 because launches are rewarded over long bets. At scale, the aggregate portfolio becomes 95% H1 with no transformational work. The 70/20/10 model forces a written allocation memo that makes cross-product trade-offs visible and defensible.

## When To Use

- A single PM owns two or more shipped products and backlogs are starting to collide.
- Promoting an IC PM to Group PM / Portfolio PM: their decision frame must shift from feature-level to cross-product investment.
- Two product squads both have defensible quarterly plans but the org cannot fund both at full speed.
- Defining the handoff line between portfolio strategy (CPO) and product PM execution.
- Quarterly review when product-level OKRs are met but the portfolio is unbalanced (all H1, no H3).

## When NOT To Use

- Single-product PM with one product line — use feature-prioritization (RICE / WSJF / Kano) instead; no portfolio exists at the PM level.
- Pure team-topology or hiring decisions — use Team Topologies, not portfolio strategy.
- Roadmap-internal trade-offs inside one product (feature A vs feature B in the same SKU).
- Resource arguments that are really about sprint capacity or on-call rotation.
- Crisis quarter where one product is on fire — defer portfolio review until the fire is out.

## Content

| File | What's inside |
|------|---------------|
| `content/01-horizon-model.xml` | Three-horizon definitions, allocation ratios by economic condition, per-PM role taxonomy (product vs portfolio vs mixed). |
| `content/02-agentic-workflow.xml` | Three-pass pipeline: product-PM pass, portfolio-PM pass, reconciliation pass. Subagent recommendations and prompt patterns. |
| `content/03-antipatterns.xml` | Role ambiguity, local-optimization drift, solo-founder collapse, cross-product synergy invisibility, PM career skew. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pm-role-skew.sh` | Detects single-product vs portfolio PM patterns from a CSV; flags H1-only, H3-zombie, bimodal-no-bridge. |
| `templates/prompt-portfolio-pm.txt` | LLM prompt for portfolio-PM pass: aggregates per-product allocations, detects role-level anti-patterns. |
| `templates/prompt-product-pm.txt` | LLM prompt for single-product PM defending allocation within portfolio targets. |
