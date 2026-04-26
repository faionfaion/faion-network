# Strategy Methods: Solution Options and Limitation Assessment

## Summary

Toolkit for weighted multi-criteria scoring of solution options, limitation/defect assessment, and BABOK 50-technique lookup. Covers: options identification with do-nothing baseline, criteria weighting, scoring matrix, sensitivity analysis, and limitation root-cause registers.

## Why

Without a structured scoring method, solution recommendations are driven by advocacy rather than evidence. Weighted criteria scoring forces explicit trade-offs; sensitivity analysis reveals whether the recommendation is robust (winner stable under ±10% weight perturbation) or brittle. Limitation registers with 5-whys root causes prevent remediation from landing on symptoms.

## When To Use

- Two or more solution options exist (build/buy/partner/SaaS/status-quo) and a sponsor needs a defensible recommendation with a numeric weighted score.
- Vendor/RFP shortlists where 3-5 finalists must be reduced to a single recommendation.
- Architecture decisions where competing patterns need comparison beyond gut feel.
- Post-deployment when users surface defects and someone must decide fix/workaround/accept/defer.
- Steering-committee decision packs requiring alternatives, criteria, weights, and sensitivity analysis.
- Quick BA technique lookup: matching a sub-task to the right BABOK technique from the 50-technique reference.

## When NOT To Use

- One option with an obvious winner — do not invent strawman alternatives to fill a matrix.
- Reversible/two-way-door decisions (feature flag, copy change, small refactor) — use a one-line ADR.
- Decisions dominated by a single hard constraint (regulatory deadline, cost ceiling) — filter on that constraint alone.
- Pure quantitative cash-flow comparisons — use NPV/IRR/payback instead.
- Limitation assessment for incidents with a known cause and an in-flight patch — use post-mortem/5-whys.

## Content

| File | What's inside |
|------|---------------|
| `content/01-options-scoring.xml` | Options identification rules, criteria weighting, anchored scoring rubric, sensitivity analysis requirement. |
| `content/02-limitation-assessment.xml` | Limitation identification, root-cause rules, severity derivation formula, remediation options. |
| `content/03-technique-reference.xml` | BABOK 50-technique lookup table with primary use cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scoring-matrix.md` | Solution options analysis with evaluation criteria, scoring matrix, and recommendation. |
| `templates/limitation-register.md` | Limitation assessment with root cause, impact, and remediation columns. |
| `templates/sensitivity.py` | Python script for ±10%/±25% weight perturbation and brittleness detection. |
