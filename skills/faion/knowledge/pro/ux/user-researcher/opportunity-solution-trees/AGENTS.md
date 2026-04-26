# Opportunity Solution Trees

## Summary

A visual discovery framework (Teresa Torres) that links one product outcome to a hierarchy of customer opportunities, candidate solutions, and experiments. The tree enforces outcome-first thinking: no solution may exist without a parent opportunity, and no opportunity is valid without customer-interview evidence.

## Why

Teams default to solution-first thinking and skip the opportunity layer, shipping features that pass internally but miss the actual customer need. OST makes the causal chain explicit and auditable — outcome → opportunity → solution → experiment — so teams can prune bad branches before building, not after. Evidence anchoring prevents the tree from becoming a brainstorm dump.

## When To Use

- Continuous-discovery cadence (weekly customer touchpoints) where a living artefact connects research to delivery.
- Quarterly planning to translate a north-star outcome into a research-grounded backlog.
- Cross-functional alignment when product, design, and engineering disagree on Solution A vs. B.
- Onboarding a new PM/designer to the team's discovery context.
- Refactoring a feature roadmap that has drifted into solution-first thinking.

## When NOT To Use

- Pre-discovery: without customer interviews an OST is fiction, not structure.
- Strict waterfall delivery where the backlog is fixed for 6+ months — OST is a discovery tool, not a Gantt.
- Single-experiment hypotheses (one-off A/B test) — overkill; use a hypothesis canvas.
- For OKR setting itself; OST starts with an outcome, it does not generate one.
- Compliance/regulatory work where outcomes are binary (pass/fail) — opportunity branching adds no value.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | OST node taxonomy, tree rules, opportunity vs. solution discipline |
| `content/02-workflow.xml` | Build, prune, and refresh cadence; agentic workflow and subagent patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost.yaml` | Agent-editable OST schema: outcome, opportunities, solutions, experiments |

## Scripts

none
