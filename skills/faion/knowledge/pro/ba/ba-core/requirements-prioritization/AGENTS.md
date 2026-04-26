# Requirements Prioritization

## Summary

Select a prioritization method by data availability (not preference) using a deterministic 6-step decision tree, then score requirements with explicit data-quality flags per factor. Methods: MoSCoW (release scope, 60/20/20 effort budget enforced mechanically), RICE (reach baseline required), Kano (survey data required), WSJF (SAFe/PI planning), weighted-sum (regulated, ≤7 criteria), Value-Effort (quick triage). Always require a REQ-XXX ID and effort estimate before scoring; include a status-quo "do nothing" baseline row.

## Why

All-Must MoSCoW, Confidence=100% RICE, and conference-room Kano produce false confidence in priority decisions. A selector that refuses to recommend a method when prerequisites are missing — and that flags data-quality problems per scored row — forces the team to surface gaps before committing resources. The sensitivity pass (±20% perturbation) identifies items whose rank is fragile.

## When To Use

- New release scope decision with ≥ 30 candidate items and only ~30-40% can ship in the window
- An "everything is Must" MoSCoW exists and you need a forcing function with numbers to break the tie
- Mid-sized backlog (50-200 items) where ordinal stack-rank no longer survives a new stakeholder's input
- SAFe or PI planning context where Cost-of-Delay matters — WSJF is the explicit fit
- Regulated or audited contexts where priority decisions must cite criteria and weights

## When NOT To Use

- Pre-PMF discovery — locking priorities on speculative requirements creates false rigor
- Internal engineering work (refactors, tech debt) — RICE and Kano measure user-facing value; use technical-debt scoring instead
- Hard regulatory deadlines — these are constraints, not priorities; force them into Must / top-N mechanically
- Items with no effort estimate from delivery — every method here divides or trades against effort
- Fewer than 10 items, single decision-maker — a stack rank by the PO is faster and just as defensible

## Content

| File | What's inside |
|------|---------------|
| `content/01-methods.xml` | All 6 methods with mechanics, known failure modes, and selection decision tree |
| `content/02-agentic.xml` | 5-pass agentic workflow, prompt patterns (method-picker and RICE scorer), AI gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/moscow-template.md` | MoSCoW table with 60/20/20 budget enforcement section |
| `templates/rice-template.md` | RICE scoring table with data-quality-flag column |
| `templates/prio_method_and_wsjf.py` | Method-picker + WSJF scorer from context.json and items.csv |
