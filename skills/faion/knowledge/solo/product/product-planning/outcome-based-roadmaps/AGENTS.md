# Outcome-Based Roadmaps

## Summary

An outcome-based roadmap replaces feature commitments with measurable metric targets
as the unit of planning. Each quarterly slot carries a verb+metric+delta+timeframe
outcome ("Reduce churn from 8% to 5% by Q2"), a list of candidate solutions marked
"to-validate", and an explicit "not doing" list. Solutions are mutable mid-quarter;
outcomes are frozen once set. This format keeps the roadmap valid across experiments
and prevents stakeholders from treating it as a delivery contract.

## Why

Feature roadmaps commit to solutions before problems are validated. When a feature
ships and fails to move the needle, the roadmap is wrong but the commitment is set.
Outcome roadmaps shift the commitment to the goal — teams retain freedom to pivot
solutions while preserving alignment on what success looks like. The format also
surfaces planning slack: "Reduce support tickets by 30%" can be achieved by a chat
feature, better docs, or a redesign — the roadmap survives any of those choices.

## When To Use

- Quarterly planning where the best solution is still uncertain.
- Stakeholders conflate feature lists with contractual commitments.
- Discovery loop is active and the roadmap must survive the next experiment.
- Multiple teams or contractors need goal alignment without locking solutions.

## When NOT To Use

- Contractually committed deliverables (RFPs, enterprise SLAs, regulatory deadlines) — use a timeline roadmap.
- Pure execution phase with fully scoped and validated work — use a sprint/release plan.
- No metrics pipeline; outcome roadmaps require trustworthy baselines to be meaningful.
- Pre-PMF zero-to-one stage where finding any user is the priority, not moving a metric.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Outcome roadmap format: outcome block anatomy, contrast with feature roadmap, quarterly template structure. |
| `content/02-rules.xml` | Concrete rules: outcome wording (verb+metric+delta+timeframe), cap at 3/5 outcomes, mandatory "not doing", freeze window, two-tier publishing. Agent gotchas absorbed from agent-integration.md. |
| `content/03-antipatterns.xml` | Vanity outcomes, outcome inflation, disconnect from delivery backlog, confusing activities with outcomes, weak stakeholder buy-in. |

## Templates

| File | Purpose |
|------|---------|
| `templates/outcome-roadmap.md` | Quarterly outcome roadmap: outcome blocks with metric, baseline, target, evidence, candidate solutions, not-doing. |
| `templates/lint-outcomes.py` | Python validator: checks each outcome row for required fields and movement verb; fails CI if malformed. |
