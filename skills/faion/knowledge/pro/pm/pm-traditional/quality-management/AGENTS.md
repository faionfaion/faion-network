# Quality Management

## Summary

Three-process quality discipline: Plan Quality (define standards and measurable thresholds), Manage Quality / Assurance (ensure processes produce quality), and Control Quality (verify deliverables meet standards via deterministic gates). Quality gates are computed from CI artifacts and threshold files — never from narrative opinion. Every gate decision (release / hold / abort) requires human approval; agents emit recommendations only.

## Why

Rework consumes 20–40% of project effort on most software programs. Prevention is cheaper than detection: a linter rule that catches a bug in CI is cheaper than an escaped production defect by 1–2 orders of magnitude. The Cost-of-Quality model quantifies this: prevention + appraisal costs must be weighed against internal-failure + external-failure costs. Most teams under-invest in prevention because failure cost is invisible until it happens.

## When To Use

- Software programs with external acceptance criteria (UAT sign-off, FDA/EMA submission, ISO 9001 audits)
- Multi-team programs where Definition of Done drift creates integration defects
- Regulated domains needing a documented Quality Plan and QC records
- Programs with SLA/SLO obligations where escape defect rates are contractual
- Quality gates in CI/CD pipelines that block merges, releases, and deployments

## When NOT To Use

- Pre-PMF startups iterating on prototypes — heavy quality plans slow learning; use basic CI checks and `code-quality/`
- Throwaway spikes or POCs where the deliverable is "demo runs once"
- One-person side projects — checklist overhead exceeds defect cost
- When the real bottleneck is requirements clarity — fix scope and requirements first

## Content

| File | What's inside |
|------|---------------|
| `content/01-plan-and-assurance.xml` | Quality Plan structure, DoD rules, assurance activities, Cost of Quality |
| `content/02-control-and-gates.xml` | Quality gate rules, defect triage, escape analysis, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/quality-gate.py` | Pass/fail PR against quality-plan.yaml thresholds from CI JSON artifact |
