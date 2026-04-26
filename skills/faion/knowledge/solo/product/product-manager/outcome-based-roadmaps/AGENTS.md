# Outcome-Based Roadmaps

## Summary

An outcome-based roadmap replaces feature commitments with measurable metric movements — each row states a problem, an outcome ("metric from baseline to target by horizon"), and 2-3 candidate solutions rather than a single committed feature. The rule: never fewer than 2 candidate solutions per outcome; single-solution rows are feature roadmaps in disguise.

## Why

Feature roadmaps commit to solutions before validating problems, making pivoting politically difficult even when evidence changes. Outcome roadmaps preserve solution flexibility while maintaining strategic alignment — teams stay committed to the goal, not the implementation path. This enables discovery during execution and eliminates the need to renegotiate the roadmap every time a better solution emerges.

## When To Use

- Replacing a feature-list roadmap that has shipped on time but moved no metrics
- Communicating priority to engineers who keep asking "why this feature, not that one"
- Pre-PMF or post-PMF teams where the problem space is clearer than the solution space
- Any team that wants room to discover the right solution without re-renegotiating the roadmap

## When NOT To Use

- Hard-deadline contractual obligations (regulatory, partner integration with launch date) — these need a feature roadmap
- Pure execution phase of a well-validated initiative — outcome framing adds noise; "ship the redesign" is fine
- Teams without metrics infrastructure — you cannot run an outcome roadmap if you cannot measure outcomes
- Cultures that punish missed targets — outcome roadmaps require permission to report negative results

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Outcome row anatomy: problem, metric, baseline, target, horizon, candidate solutions |
| `content/02-process.xml` | How to translate a feature roadmap to outcomes; audience view generation |
| `content/03-antipatterns.xml` | Vague outcomes without metrics, single-solution rows, unbounded horizons |

## Templates

| File | Purpose |
|------|---------|
| `templates/outcome-row.yaml` | Single outcome row schema with all required fields |
| `templates/validate-outcomes.py` | Python validator: fails roadmap YAML with missing fields or fewer than 2 candidate solutions |
