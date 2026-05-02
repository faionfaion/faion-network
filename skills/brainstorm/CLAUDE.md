# Brainstorm Skill

> **Entry Point:** `/faion:brainstorm` — user-invocable

## When to Use

- Technical audits and improvement plans
- Architecture decision exploration
- Feature ideation and prioritization
- "What should we build/fix/improve?" questions
- Any task requiring diverse perspectives at scale

## Overview

Multi-agent brainstorming with structured diverge-converge-review cycle. Produces prioritized, reviewer-validated recommendations.

**Phases:** 4 | **Default agents:** 10 research + 8 review | **Output:** Tiered recommendation document

## Quick Reference

| Phase | Agents | Key Principle |
|-------|--------|--------------|
| Diverge | 10 research (3 parallel) | Distinct personas, independent generation |
| Converge | 1 synthesis | Dedup, consensus count, tier ranking |
| Review | 8 adversarial (3 parallel) | Assigned attack vectors, no rubber-stamping |
| Finalize | 1 synthesis | Incorporate feedback, adjust estimates |

## Process Details

See [SKILL.md](SKILL.md) for full process description.

## Lessons Learned

From initial deployment (2026-03-21, NERO platform audit):

| Issue | Fix |
|-------|-----|
| Identical agent prompts → groupthink | Assign distinct personas/focus areas |
| 510 raw recs with massive overlap | Add dedicated dedup step before synthesis |
| Infrastructure bias, zero user features | Include "user perspective" and "devil's advocate" in research agents |
| Optimistic effort estimates | Always include feasibility reviewer with specific callouts |
| Auth failures in 3/20 agents | Add retry mechanism for failed agents |
| All savings invisible to users | Require at least 20% of recommendations be user-facing |

## Related

- Uses: Agent tool for parallel execution
- Peers: faion-researcher, faion-product-planning, faion-software-architect
