<!--
purpose: Heuristic evaluation form — scope, per-issue findings with severity, summary table
consumes: build under evaluation + the ten heuristics
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-800 tokens when loaded as context
variables:
  - name: product_feature
    type: string
    required: true
    description: The product or flow being evaluated, named as a user would find it. Evaluate one flow properly rather than a whole product thinly - the thin pass finds only what a screenshot would.
  - name: evaluator
    type: string
    required: true
    description: Who did this pass. Heuristic evaluation is single-evaluator by nature and each one finds a different third of the issues, so the name is what makes a second pass worth running.
  - name: date
    type: string
    required: true
    description: Date of the pass, ISO. Findings are against a build that will move within days; without the date, a fixed issue reappears in the next report as a regression that never happened.
  - name: build_reference
    type: string
    required: true
    description: Exactly what you evaluated - the staging URL, the build number or the prototype link with its version. "The live site" ages between writing this and someone reading it.
  - name: scope_screens
    type: text
    required: true
    description: Which screens and flows you actually walked, and which you did not. The unwalked half is the part a reader will otherwise assume was clean, and that assumption is where the escape happens.
  - name: focus_heuristics
    type: text
    required: true
    description: Which of the ten you concentrated on and why. All ten in one pass gives each about the same attention as a glance; naming two or three is a stronger claim than pretending to cover all.
-->
# Heuristic Evaluation: {{product_feature}}

**Evaluator:** {{evaluator}}
**Date:** {{date}}
**Version evaluated:** {{build_reference}}

## Scope

{{scope_screens}}

**Focus heuristics this pass:** {{focus_heuristics}}

## Findings

### Issue 1

- **Location:** [Screen name → component → specific element]
- **Heuristic:** [#N — Heuristic name]
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
