# Error-Tracker to Draft-PR Pipeline

## Summary

When a production exception crosses a tunable event-count and fixability threshold inside an error tracker (Sentry Seer/Autofix, Bugsink, Rollbar, Starsling), a coding agent ingests the structured signal `{stack_trace, breadcrumbs, distributed_trace, linked_repo, recent_diffs}`, proposes a code patch plus a regression test, and opens a **draft** pull request that is bidirectionally linked to the alert. The PR is never auto-merged: the alert URL lives in the PR body, the alert page links back to the PR, and a human in CODEOWNERS clicks Merge after review. Sentry Seer is the canonical implementation, with `min_events: 10` and `min_fixability: 0.7` as the standard auto-run gate.

## Why

A repeating production exception with a clean stack trace is the highest-signal input a coding agent can receive: the failure is reproducible, the file/line is already pinned, and the breadcrumbs disambiguate the call site. Letting the tracker open a draft PR collapses the "alert → triage → ticket → branch → fix → PR" chain into one artifact, while the draft state plus CODEOWNERS gate prevents the failure mode where bots ship unreviewed patches. The thresholds (events + fixability score) filter out one-off network blips that no patch can fix and concentrate agent tokens on the truly fixable. Sentry's published Seer/Autofix docs and changelog entries describe this exact pipeline as the production behavior since 2025; Bugsink and Starsling reproduce the pattern on self-hosted or third-party stacks.

## When To Use

- Production runtime errors with a clean stack trace and source map (NullPointer, KeyError, IntegrityError, TypeError).
- Repeatable exceptions whose first frame maps 1:1 to a code line in a linked repository.
- Cross-service errors where a distributed trace already correlates the failure across BE+FE.
- Repos where Sentry, Bugsink, or Rollbar is already wired and SCM Settings can list the GitHub/GitLab repo.

## When NOT To Use

- One-off errors below the event threshold (< 10 events) — noisy, expensive, low fixability.
- Errors with no stack trace (network timeout, OOM, kernel panic, SIGKILL) — the agent has nothing to anchor to.
- Business-logic bugs where the "fix" is a product decision, not a code edit — agent will pattern-match the wrong shape.
- Strict-compliance repos where draft PRs from bots are still treated as production code on import — escalate to human-only triage.
- Solo or hackathon repos where the operational overhead exceeds the fix value.

## Content

| File | What's inside |
|------|---------------|
| `content/01-trigger-thresholds.xml` | The two-gate threshold rule (`min_events` + `min_fixability`) and why both are required. |
| `content/02-pr-body-bidirectional-link.xml` | Mandatory PR body shape: alert URL, root cause, test path; alert page must link back to PR. |
| `content/03-draft-bot-identity-gate.xml` | PR opens as draft, authored by a dedicated bot identity, gated by CODEOWNERS review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/seer-org-config.yml` | Sentry Seer `auto_run` config with thresholds, repo list, draft mode, body template. |
| `templates/pr-body.md` | Reusable PR body skeleton with alert link, root-cause section, test path, reviewer checklist. |
