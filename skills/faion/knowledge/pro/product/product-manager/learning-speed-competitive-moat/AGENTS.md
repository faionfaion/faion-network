# Learning Speed as Competitive Moat

## Summary

A framework for treating organizational learning velocity as the primary competitive advantage in markets where AI lets competitors clone product experiences in weeks. The core metric is: Learning Velocity = (Signals Noticed × Update Speed × Execution Quality) / Time. At the PM level it operates as a per-bet `bet.md` system with weekly `bet-reviewer` cycles, kill criteria, and a quarterly personal calibration scorecard.

## Why

In 2026, feature parity is achievable in weeks via AI codegen. The durable moat is how fast an org notices market changes, updates beliefs, and ships different answers. Teams that run weekly belief-update rituals outmaneuver quarterly-review orgs regardless of headcount — because the bottleneck is decision latency, not execution capacity.

## When To Use

- A PM owns a product area against a well-funded competitor where the differentiation thesis depends on shipping the right thing next, not the most things.
- Preparing for a quarterly business review and need to defend "what we changed our minds about" with evidence.
- Setting OKRs where learning velocity (not feature throughput) is the contested promotion criterion.
- Inherited a roadmap built on stale assumptions — need a 30-day belief-audit before committing to next quarter.
- Post-PMF squad where the bottleneck has moved from "does anyone want this?" to "which of 8 plausible bets do we make first?"

## When NOT To Use

- Pre-PMF founder or PM — the bottleneck is one working hypothesis, not learning velocity across many.
- Highly regulated domains (medical devices, defense, certain fintech) where weekly belief updates conflict with regulatory commitment cycles.
- A PM whose squad has not shipped in 8+ weeks — fix delivery first, then add meta-process.
- Feature-factory orgs where roadmap is set top-down by sales — personal learning velocity does not move the moat at squad level.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Learning Velocity formula, four elements to improve, weekly rituals, AI-powered signal processing, organizational infrastructure. |
| `content/02-pm-practices.xml` | Per-bet `bet.md` system, kill criteria, bet-reviewer agent loop, personal calibration, failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pm-learning-velocity.py` | Python: scores a PM's learning velocity from a `decisions.yaml` decision log (kill/reframe ratio, reversal rate, prediction hit rate). |
