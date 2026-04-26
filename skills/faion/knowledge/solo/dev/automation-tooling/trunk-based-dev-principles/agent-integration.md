# Agent Integration — Trunk-Based Development: Principles

## When to use
- Setting branching policy for a new repo: this reference is the policy text the agent can paste into `CONTRIBUTING.md`.
- Auditing an existing repo's git practices and producing a TBD-readiness report (test coverage, CI time, branch lifetime, PR size).
- Choosing between Pure Trunk / Short-Lived Branches / Release Branches for a given team size + compliance posture.
- Defining DORA-aligned metrics dashboards (deploy frequency, lead time, change failure rate, MTTR).

## When NOT to use
- For *how* to do TBD safely (feature flags, branch-by-abstraction, dark launch) — see sibling `trunk-based-dev-patterns`.
- Strict GitFlow shops with mandated long-lived `develop` branches (regulated industries with audit trails) — use principles only as a target state.
- OSS projects with public PRs from external contributors — they need feature branches by default for review/security; trunk only for maintainers.
- Mobile/desktop apps gated by app-store review cycles — release branches dominate; trunk is upstream of them.

## Where it fails / limitations
- "TBD requires strong tests" is necessary but not sufficient — flaky tests destroy trunk confidence; reference doesn't quantify flakiness budget (target < 1%).
- Roadmap phases are written week-bound but no way to grade exit criteria; agent translates "Phase 1 complete" without measuring CI time.
- Pure Trunk subsection ("commit directly to main") is dangerous for teams > 3 — agents take it as an option without flagging the risk.
- Release-branch flow ("cherry-pick fixes back to trunk") is correct in principle but easy to mis-execute; the README doesn't describe the merge-direction tooling.
- DORA targets quoted ("deploy multiple per day, lead time < 1h") are 2021-era elite values; pair them with cohort context — not all teams should target elite.

## Agentic workflow
Use this reference as input to a *git-policy generator* and as the rubric for a *branch hygiene auditor*. The agent can: (1) read repo state via `gh`, (2) compare to principles (branch lifetime, PR size, CI time), (3) emit a markdown audit + action list, (4) propose CONTRIBUTING.md / branch-protection settings. Pair with `trunk-based-dev-patterns` to actually implement the changes.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the rollout phases as SDD tasks; each phase exit-criterion becomes an acceptance criterion.
- `review` skill — code-review subagent already aligned to "small PR" principle.

### Prompt pattern
```
Audit github.com/<org>/<repo> against TBD principles
(solo/dev/automation-tooling/trunk-based-dev-principles/README.md).
Report:
- avg branch lifetime (last 50 merged PRs) vs target < 1 day
- p50 PR size vs target < 200 lines
- CI wall time (median) vs target < 10 min
- main branch protection state (required checks, required reviews)
Produce a phased rollout plan referencing the README's Implementation Roadmap.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | PR/branch/protection inspection | https://cli.github.com |
| `git log --since` + custom scripts | Branch lifetime + PR size metrics | built-in |
| `four-keys` | DORA metrics dashboard from VCS + CI | https://github.com/dora-team/fourkeys |
| `metrik` | OSS DORA metrics tool | https://github.com/thoughtworks/metrik |
| `gitleaks` / `trufflehog` | Pre-trunk secret scan | required when committing direct to main |
| `semantic-release` | Auto-versioning on trunk merges | https://semantic-release.gitbook.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sleuth | SaaS | Yes — webhooks + REST | DORA tracking, deploy-frequency dashboards. |
| LinearB | SaaS | Yes — REST | DORA + cycle-time + PR-size analytics. |
| Swarmia | SaaS | Yes — REST | Engineering effectiveness + DORA. |
| GitHub Insights / Pull Request Insights | SaaS | Partial | Native, decent for branch lifetime. |
| Jellyfish | SaaS | Yes | Enterprise eng metrics. |
| Mergify | SaaS | Yes — config-as-code | Auto-merge queue keeps trunk green at scale. |
| Trunk.io merge queue | SaaS | Yes | Drop-in MQ + linter aggregator. |

## Templates & scripts
Branch-protection snippet via `gh` (idempotent), an agent can run after PR review:

```bash
gh api -X PUT repos/$OWNER/$REPO/branches/main/protection \
  -F required_status_checks.strict=true \
  -F 'required_status_checks.contexts[]=ci/build' \
  -F enforce_admins=true \
  -F required_pull_request_reviews.required_approving_review_count=1 \
  -F required_pull_request_reviews.dismiss_stale_reviews=true \
  -F restrictions= \
  -F required_linear_history=true \
  -F allow_force_pushes=false \
  -F allow_deletions=false
```

PR-size lint inline (CI step) keeps PRs small:

```bash
ADD=$(git diff --shortstat origin/main... | awk '{print $4}')
test "${ADD:-0}" -le 400 || { echo "PR adds $ADD lines, cap 400"; exit 1; }
```

## Best practices
- Track branch lifetime weekly; alert when p90 > 2 days. Long-lived branches kill TBD before tests do.
- Squash on merge → linear history → painless `git bisect`. Never allow merge commits on `main`.
- Pair "always releasable" with deploy-on-merge to a *staging* env; production gate is human/canary, not branch-based.
- CI fast lane: under 10 min for the main pipeline. Move flaky/slow suites (browser E2E, perf) to nightly + per-area triggers, not main pipeline.
- Forbid commits to `main` outside PRs *including* admins (`enforce_admins=true`). One bypass and the discipline is gone.
- Tag a single "Trunk Sheriff" rotation; first responder when CI red. Without ownership, broken trunk normalises.
- Track DORA *trends*, not absolute targets. A team going from "weekly deploy" to "daily" is winning even if it doesn't hit "elite".

## AI-agent gotchas
- Agent suggests "create develop branch" reflex from training data — TBD has no `develop`. Force the rule in the prompt.
- Agent treats "rebase frequently from main" as optional during long branches; without a hard rule, branches drift and accumulate conflicts.
- Pure-Trunk option in the README is a foot-gun for unattended agents — never let an agent push directly to `main` even if policy allows it.
- DORA metric calculation is sensitive to bot PRs (Renovate, Dependabot); agent reading raw numbers reports inflated deploy frequency. Filter authors first.
- Agent recommends raising required reviewers to 2+ "for safety" — kills TBD merge speed. Keep at 1 + strong CI; review SLA matters more than reviewer count.
- Human-in-loop checkpoint: branch-protection rule changes (especially turning off `enforce_admins`) need explicit human approval; agents must propose-not-apply.
- CHANGELOG-style cherry-picks across release branches: agent forgets to apply to trunk when starting on the release branch — leaves divergent histories. Always merge trunk-first, cherry-pick to release.

## References
- https://trunkbaseddevelopment.com/ — canonical reference
- https://itrevolution.com/accelerate-book/ — Forsgren, Humble, Kim — DORA evidence
- https://continuousdelivery.com/ — Jez Humble — supporting practices
- https://dora.dev/ — DORA research site, current cohort thresholds
- https://martinfowler.com/articles/branching-patterns.html — Fowler comparison of branching models
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository — branch protection reference
