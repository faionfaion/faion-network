<!-- purpose: Competitor feature-parity matrix with evidence URLs and gap-validation verdicts. -->
<!-- consumes: competitor list + feature inventory + evidence URLs -->
<!-- produces: Markdown feature matrix -->
<!-- depends-on: none -->
<!-- token-budget-impact: ~350-550 tokens when loaded as context -->

## Feature Matrix: <category>

**Date:** YYYY-MM-DD | **Top competitors:** <list> | **Quality scale:** 0=unusable, 3=best-in-class

### Feature Matrix

| Feature | Us | Comp A | Comp B | Comp C | Gap? |
|---------|-------|--------|--------|--------|------|
| <core_1> | Y/3 | Y/3 | Y/3 | Y/2 | No (table stakes) |
| <core_2> | Y/3 | Y/3 | P/1 | Y/2 | Partial opportunity |
| [Diff 1] | Y/3 | N | N | P/1 | Yes — validate demand |
| <nice_1> | unknown | N | N | N | Validate demand first |

**Cell format:** Y/P/N (quality 0-3) | Evidence URL
**Rule:** "Y" requires an evidence URL. No evidence → write "N, no public proof".

### Evidence URLs

| Competitor | Feature | Status | Quality | Evidence URL | Captured |
|------------|---------|--------|---------|-------------|---------|
| Comp A | [feature] | Y | 3 | [URL] | YYYY-MM-DD |
| Comp B | [feature] | P | 1 | [URL] | YYYY-MM-DD |
| Comp C | [feature] | N | — | no public proof | — |

### Gap Validation Results

| Gap | Why missing? | Customer demand? | Can we do better? | Verdict |
|-----|-------------|-----------------|-------------------|---------|
| [Diff 1] | [technical/reg/unprofitable/unaware] | [review quote, N mentions] | <our_advantage> | pursue/investigate/skip |

**Skip budget:** ≥40% of candidate gaps must be marked skip. Resist pursuit-bias.

### Kill List (skip with reasons)

| Gap | Skip reason | Date | Reviewer |
|-----|-------------|------|----------|
| [feature] | <why> | YYYY-MM-DD | <name> |
