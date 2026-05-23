<!--
purpose: Markdown snippet for the PR template's blast self-score block.
consumes: nothing — copy into .github/pull_request_template.md or equivalent.
produces: per-PR blast scoring fields that the bot reads.
depends-on: PR template support in tracker (GitHub, GitLab, Linear).
token-budget-impact: ~120 tokens when copied into a PR body.
-->

## Blast radius (required — bot reads this)

**Services touched:** 1 (one module) / 3 (one service) / 5 (multi-service or shared lib) →
**Users affected:** 1 (&lt;1% MAU) / 3 (≤10% MAU) / 5 (&gt;10% MAU) →
**Reversibility:** 1 (feature flag) / 3 (redeploy fix) / 5 (irreversible migration or external side-effect) →

**Total (sum 3-15):**

**Override category fired:** none | auth | payments | rbac | secrets | migrations | deletions | money | pii | cron

### Rollback plan (REQUIRED when Reversibility=5)
- Trigger (what observable signals rollback):
- Commands (exact, copy-paste-runnable):
- Verification (what proves rollback succeeded):
- People (who to page if rollback fails):
