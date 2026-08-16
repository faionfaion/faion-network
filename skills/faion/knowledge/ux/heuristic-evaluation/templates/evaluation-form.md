<!--

purpose: Heuristic evaluation form — scope, per-issue findings with severity, summary table
consumes: build under evaluation + the ten heuristics
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-800 tokens when loaded as context
-->


# Heuristic Evaluation: <product_feature>

**Evaluator:** <evaluator>
**Date:** <date>
**Version evaluated:** <build_reference>

## Scope

<scope_screens>

**Focus heuristics this pass:** <focus_heuristics>

## Findings

### Issue 1

- **Location:** [Screen name → component → specific element]
- **Heuristic:** <n_heuristic_name>
- **Problem:** [Specific description of the violation — what exactly is wrong]
- **Severity:** [0-4]
- **Recommendation:** [Specific fix — actionable, not "improve this"]

### Issue 2

[Same structure — repeat for each finding]

## Summary Table

| Heuristic | Issues Found | Severity Range |
|-----------|-------------|----------------|
| #1 Visibility of system status | [Count] | [0-4] |
| #2 Match real world | [Count] | [0-4] |
| #3 User control | [Count] | [0-4] |
| #4 Consistency | [Count] | [0-4] |
| #5 Error prevention | [Count] | [0-4] |
| #6 Recognition over recall | [Count] | [0-4] |
| #7 Flexibility | [Count] | [0-4] |
| #8 Aesthetic minimalist | [Count] | [0-4] |
| #9 Error recovery | [Count] | [0-4] |
| #10 Help and docs | [Count] | [0-4] |

## Top 3 Priority Issues

1. [Severity 4/3: most critical finding with location]
2. [Severity 3: second critical finding]
3. [Severity 3/2: third priority]
