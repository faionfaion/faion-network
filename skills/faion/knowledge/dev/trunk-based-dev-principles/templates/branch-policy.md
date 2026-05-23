<!--
purpose: BRANCHING.md starter for a team adopting trunk-based development.
consumes: nothing — paste at repo root as BRANCHING.md.
produces: a written branching policy the CI gates can enforce.
depends-on: CI capable of failing PRs from stale branches.
token-budget-impact: ~180 tokens when copied.
-->

# Branching Policy

## Model

This repo uses **trunk-based development**. The default branch (`main`) is always releasable.

## Branch rules

- All work targets `main`.
- Feature branches MUST be short-lived: maximum age 2 days from creation to merge.
- Branch names follow `&lt;type&gt;/&lt;ticket-id&gt;-&lt;slug&gt;` (e.g. `feat/F-066-shadow-router`).
- Branches older than 2 days fail CI on every push until merged or closed.
- Stale branches (no commits for 7 days) are auto-closed.

## Commit rules

- Commit at least once per workday.
- Aim for &lt; 200 LoC per PR median.
- Each PR ships with passing tests, lint, typecheck.
- Incomplete features MUST be wrapped in a feature flag with a `flag_id` field in the PR template; the flag has a cleanup ticket filed at creation.

## Merge rules

- Reviewer SLA: respond within 4 hours during working hours.
- All required gates green (test, lint, typecheck, coverage, blast-radius score, flag-id when "incomplete").
- Auto-revert on red trunk is armed. A red merge is auto-reverted; the author re-fixes and re-submits.

## Cleanup

- Every feature flag has a cleanup ticket with an SLA: 30 days after reaching 100% rollout.
- Quarterly recalibration of CI gates + override category list.
