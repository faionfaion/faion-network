<!-- purpose: Problem-validation report with a scored evidence log and a PROCEED/PIVOT/KILL decision -->
<!-- consumes: problem statement draft, kill threshold, evidence collected (Prerequisites) -->
<!-- produces: filled validation-report markdown -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~250 tokens filled -->

# Problem Validation Report

## Problem Statement
<who> struggles with <what> because <why>

## Kill Threshold (defined before collection)
{e.g., fewer than 3/10 confirm at 7+/10 intensity → KILL}

## Evidence Collected

| Type | Tier | Source | Finding |
|------|------|--------|---------|
| Interview | stated | User 1 | "I spend 3 hours/week on this" |
| Interview | committed | User 2 | "Would pay $50/month" |
| Forum | anecdote | Reddit | 50 upvotes on complaint post |
| Review | stated | G2 | "Missing feature X" (repeated 10x) |
| Search | — | Google | "solve X problem" — 5K/month |

## Assessment

| Criterion | Threshold | Score | Evidence |
|-----------|-----------|-------|---------|
| Frequency | Weekly+ | Weekly | Interviews |
| Intensity | 7+/10 | 8/10 | Interviews |
| WTP | Yes | 4/5 would pay | Interviews |
| Search | Exists | 5K/month | Google |
| Competition | Exists | 3 competitors | Market research |

## Decision
**<proceed_pivot_kill>** — {one-sentence rationale}
