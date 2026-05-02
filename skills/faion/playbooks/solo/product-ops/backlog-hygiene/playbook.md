---
name: backlog-hygiene
description: Run a weekly 30-min triage of .aidocs/backlog/ to kill stale features, merge duplicates, and archive superseded work before clutter kills momentum.
tier: solo
group: product-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a trimmed `.aidocs/backlog/` where every surviving feature is either actionable within the next 3 months or explicitly ice-boxed, and everything older than 90 days without re-validation is closed. Real-world result: a 60-item backlog collapses to 12 items you can actually act on.

## Prerequisites

- A project with an `.aidocs/` SDD layout (`backlog/ → todo/ → in-progress/ → done/`).
- Familiarity with the SDD feature lifecycle (see `spec.md` format, acceptance criteria conventions).
- `git` available in the working directory (features are committed, so closure is a commit too).
- Optional: a notes file such as `backlog-hygiene-log.md` to capture decisions across sessions.

## Steps

1. **Count and timestamp the starting state.**
   ```bash
   find .aidocs/backlog -mindepth 1 -maxdepth 1 -type d | sort > /tmp/backlog-before.txt
   wc -l /tmp/backlog-before.txt
   ```
   Record the count. This is your "before" metric.

2. **Flag features older than 90 days for review.**
   ```bash
   find .aidocs/backlog -mindepth 1 -maxdepth 1 -type d -not -newer $(date -d '90 days ago' +%Y-%m-%d 2>/dev/null || date -v-90d +%Y-%m-%d) | sort
   ```
   Any feature folder whose `spec.md` `created` or `last_updated` field is more than 90 days old is a candidate for closure unless you can immediately name the user who asked for it and the metric it moves.

3. **Read each flagged spec.md and apply the four-question test.**
   For each flagged feature, open its `spec.md` and answer:
   - Is the problem it solves still real? (Yes / No / Unsure)
   - Has shipped work already solved it? (check `done/` folder)
   - Does another backlog feature overlap ≥70% in scope?
   - Can this start within the next 3 months given current focus?
   If two or more answers are No/Yes (problem solved)/overlap/blocked → close it.

4. **Close features that fail the test.**
   Move to an `.aidocs/backlog/.archive/` folder (create if missing) and append a one-line reason to the feature's `spec.md`:
   ```bash
   mkdir -p .aidocs/backlog/.archive
   mv .aidocs/backlog/feature-023-dark-mode/ .aidocs/backlog/.archive/
   echo "\n> Archived 2026-05-02: superseded by design-token-system shipped in feature-031." >> .aidocs/backlog/.archive/feature-023-dark-mode/spec.md
   ```

5. **Merge near-duplicate features.**
   When two features share the same root problem (e.g., `feature-041-email-notifications` and `feature-055-digest-emails`), keep the one with the more complete spec, copy any unique acceptance criteria from the other into it, then archive the duplicate.
   ```bash
   # Copy unique ACs from the duplicate into the keeper
   cat .aidocs/backlog/feature-055-digest-emails/spec.md >> .aidocs/backlog/feature-041-email-notifications/spec.md
   mv .aidocs/backlog/feature-055-digest-emails/ .aidocs/backlog/.archive/
   echo "\n> Archived 2026-05-02: merged into feature-041; unique ACs copied." >> .aidocs/backlog/.archive/feature-055-digest-emails/spec.md
   ```

6. **Mark surviving stale features as ice-box.**
   Features that are still valid but cannot start within 3 months get an ice-box marker so they don't pollute sprint planning:
   ```bash
   echo "\n> Ice-boxed 2026-05-02: valid but not schedulable this quarter." >> .aidocs/backlog/feature-049-multi-tenant/spec.md
   ```
   Add the prefix `[icebox]` to the feature folder name if your tooling supports it, or maintain a list in `.aidocs/backlog/ICEBOX.md`.

7. **Re-validate features you keep active.**
   For each surviving feature without ice-box status, confirm the `spec.md` has: problem statement, ≥1 acceptance criterion, and a rough priority label (`P1 / P2 / P3`). If any field is missing, fill it in now or archive the feature — a spec without acceptance criteria cannot be acted on.

8. **Count the result and commit.**
   ```bash
   find .aidocs/backlog -mindepth 1 -maxdepth 1 -type d -not -path '*/.archive/*' | sort > /tmp/backlog-after.txt
   wc -l /tmp/backlog-after.txt
   git add .aidocs/backlog/
   git commit -m "chore: backlog hygiene $(date +%Y-%m-%d) — $(wc -l < /tmp/backlog-before.txt) → $(wc -l < /tmp/backlog-after.txt) features"
   ```

## Verify

Run this after the session:

```bash
find .aidocs/backlog -mindepth 1 -maxdepth 1 -type d -not -path '*/.archive/*' | wc -l
```

The number must be lower than before. Every surviving feature folder must contain a `spec.md` with a non-empty `## Acceptance Criteria` section:

```bash
for d in .aidocs/backlog/*/; do
  grep -q "Acceptance Criteria" "$d/spec.md" 2>/dev/null || echo "MISSING AC: $d"
done
```

Zero output means the backlog is clean. Any output names features that need immediate attention.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `find` returns no results for 90-day filter | macOS vs. Linux date syntax mismatch | Use `git log --diff-filter=A --format="%ai %n" -- .aidocs/backlog/feature-*/spec.md` to get creation dates from git history instead |
| A feature was closed but a stakeholder objects | Decision was made without their input | Open a new feature with the re-validated problem statement and updated ACs; don't un-archive the old one (git history preserves it) |
| Backlog grows back within two weeks | New features added without a hygiene gate | Add a `pre-push` hook or a calendar block: no new feature enters `backlog/` without first checking if an existing feature covers it |
| Two features were merged but the keeper spec is now too large | The problems were distinct enough to warrant separate features | Un-merge: create a new feature for the unique ACs you copied in, archive neither, keep both active |
| Ice-boxed features are invisible in planning | `ICEBOX.md` is out of date | Regenerate with `grep -rl "Ice-boxed" .aidocs/backlog/ > .aidocs/backlog/ICEBOX.md` |

## Next

- Run `roadmap-for-one-person` playbook to slot surviving active features into a 3-month roadmap with clear P1/P2 ordering.
- After three consecutive clean hygiene sessions, reduce triage cadence to bi-weekly.
- Promote any ice-boxed feature that becomes urgent directly into `todo/` — no need to re-run full hygiene.

## References

- [knowledge/solo/product/product-operations/backlog-management](../../../knowledge/solo/product/product-operations/backlog-management) — DEEP principle (Detailed-top, Emergent-bottom, Estimated, Prioritized) directly drives Steps 3 and 7: top items need AC detail, bottom items can remain rough, but all must be prioritized before surviving triage.
