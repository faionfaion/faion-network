<!-- purpose: upstream PR description template for UPSTREAM-PR / hybrid actions -->
<!-- consumes: FixDecision + repro details -->
<!-- produces: PR body following upstream CONTRIBUTING patterns -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150 tokens when loaded as reference -->

# Upstream PR template

## Summary

<1-2 sentences: what this PR does, why now>

## Linked issue

Closes #<issue-number> if exists, otherwise link to public issue or repro.

## Test plan

- [ ] Added unit tests for the new behaviour.
- [ ] Updated docs / CHANGELOG as required by the project.
- [ ] CI green.

## Context for maintainers

We hit this while building <Faion project>. Our internal FixDecision evaluated the change as ≥ UPSTREAM-PR (strategic_dependency=3); we run a fork-pin in parallel and will drop it as soon as this PR merges.

## Faion FixDecision link

`decisions/<YYYY-MM-DD>-<library>-fix.md` (internal)
