# Agent Integration — Trunk-Based Development

## When to use
- Solo or small teams shipping multiple times per day where merge friction is the bottleneck
- Codebases with strong CI (<10 min) and ≥70% meaningful test coverage
- Products with feature flag infrastructure (LaunchDarkly, Flagsmith, Unleash, GrowthBook, OpenFeature)
- LLM-driven dev loops — short branches keep agent context windows shallow and rebases cheap
- Migrations to CD: TBD is the prerequisite branching model for elite DORA metrics

## When NOT to use
- Pre-CI projects: TBD without automated tests is "trunk is always broken"
- Regulated industries that mandate per-feature branch isolation and signed reviews (some FDA/Aerospace contexts)
- OSS with external contributors — fork-and-PR is structurally a long-lived branch
- Mobile apps with infrequent store releases — release branches still beat pure trunk
- Junior-heavy teams without code review SLA — fast-merge culture amplifies bad commits

## Where it fails / limitations
- "Always releasable" is a discipline, not a property — it decays without a fast CI gate
- Feature flag debt accumulates: agents add flags but rarely remove them after rollout
- Agents producing 1000-line LLM PRs break the small-batch rule; size gate must be enforced in CI
- Force-pushes from rebase-heavy agent workflows can clobber teammates' refs — protect main branch and require linear history via PRs
- Hotfix flows are awkward without release branches when multiple paying customers run different versions
- Distributed teams across timezones can't hit <4h review SLA — async mitigations (pair coding, pre-approved owners) are required

## Agentic workflow
Wire agents to a "branch-per-task" loop with explicit lifetime caps: agent creates a short-lived branch from main, makes one focused change, runs tests, opens PR, and self-merges only if (a) CI passes, (b) diff <200 lines, (c) feature flag wraps any user-visible change. A `branch-watchdog` agent runs hourly and pings or auto-closes branches >48h old. A `flag-debt` agent scans monthly for flags whose rollout reached 100% and proposes removal PRs.

### Recommended subagents
- `faion-sdd-executor-agent` — sequential SDD task execution; one task = one short-lived branch
- `faion-feature-executor` — chains tasks with quality gates that match TBD's "trunk always green" rule
- A custom `branch-watchdog` (haiku) — list branches with `git for-each-ref`, age them, file follow-up tasks
- A custom `flag-debt-collector` (sonnet) — scans for flags at 100% rollout and removes call sites + flag definition

### Prompt pattern
```
Task: implement <X> on a short-lived branch.
Constraints:
- Branch from origin/main, name feat/<slug>.
- Wrap user-visible behavior behind feature flag <flag>.
- Diff target: <=200 lines. If exceeded, split into N tasks.
- CI must pass before opening PR. No --no-verify.
Output: branch name, PR URL, flag key, rollout plan.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | GitHub PR/branch management from agents | https://cli.github.com |
| `glab` | Same for GitLab | https://gitlab.com/gitlab-org/cli |
| `pre-commit` | Local quality gate before push | `pip install pre-commit` · https://pre-commit.com |
| `lefthook` / `husky` | Faster polyglot Git hooks | https://lefthook.dev · https://typicode.github.io/husky |
| `act` | Run GitHub Actions locally to validate CI before push | https://github.com/nektos/act |
| `git-town` | Helpers for short-lived branch flows (`git town hack/sync/ship`) | https://www.git-town.com |
| `gitleaks` | Block secrets pre-merge | https://github.com/gitleaks/gitleaks |
| `goose` (DORA) / Sleuth / LinearB | DORA metric collection — measures TBD payoff | https://github.com/etsy/goose · https://www.sleuth.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LaunchDarkly | SaaS | Yes | REST API + Terraform; agents can flip flags safely |
| Unleash | OSS | Yes | Self-host; OpenAPI for agent control |
| Flagsmith | OSS+SaaS | Yes | API-first, good for solo |
| GrowthBook | OSS | Yes | A/B + feature flags with experiments |
| OpenFeature | OSS spec | Yes | Vendor-neutral SDK so agents target one interface |
| GitHub branch protection + auto-merge | SaaS | Yes | Enforces TBD invariants (status checks, linear history) |
| Mergify / Kodiak / GitHub auto-merge | SaaS | Yes | Bot-merges PRs once CI green — pairs naturally with agents |
| Sleuth / LinearB / Faros | SaaS | Yes | DORA dashboards; feed metrics back to agent improvement loop |

## Templates & scripts
See `examples.md` for the keystone-interface and dark-launch patterns. Inline branch-watchdog snippet that lists stale branches:

```bash
#!/usr/bin/env bash
# stale-branches.sh — list branches older than N days
set -euo pipefail
DAYS=${1:-2}
NOW=$(date +%s)
git fetch --prune origin >/dev/null
git for-each-ref --format='%(refname:short) %(committerdate:unix) %(authorname)' refs/remotes/origin \
  | while read -r ref ts author; do
      [[ "$ref" == "origin/main" || "$ref" == "origin/HEAD" ]] && continue
      age_days=$(( (NOW - ts) / 86400 ))
      if (( age_days > DAYS )); then
        printf '%-50s %3d days  %s\n' "$ref" "$age_days" "$author"
      fi
    done
```

## Best practices
- Pin a hard branch-lifetime SLA (24-48h) and automate the warning + close
- Pin a hard PR-size SLA (200 lines diff, excluding lockfiles); agents that exceed must split
- Require CI <10 min; if it grows, treat as a P1 incident — TBD breaks down silently when feedback slows
- Wrap every user-visible change behind a flag, even for solo dev — kill-switching beats reverting
- Pair "feature flag added" PRs with a scheduled "flag retired" task to avoid debt
- Use Branch by Abstraction for refactors so the seam stays on trunk and reviewers see incremental change
- Forbid `--no-verify`, `--force-with-lease` on shared branches, and `git push --force` on main; configure server-side too
- Track DORA metrics with a lightweight script — TBD is only justified if deploy frequency and lead time improve

## AI-agent gotchas
- Agents love to "stack" branches; in TBD, prefer landing the base PR fast and rebuilding the next on green main
- Agents add feature flags then forget them; require a `flag-removal-by` date in the PR body and a follow-up task
- Long-running LLM tasks may produce 1000-line PRs; enforce size cap in CI, not in code review
- Rebases triggered by agents on shared branches can drop teammates' commits — limit rebase-on-write to branches owned by that agent's session
- Agents misread "trunk-based" as "no branches at all" and push directly to main, bypassing CI — block direct pushes server-side
- Human-in-loop checkpoint: enabling a flag for >5% of users is a release event; require explicit human approval, not automation
- "Trunk is broken" must page someone; agents need an escalation path, not a retry loop

## References
- https://trunkbaseddevelopment.com
- https://martinfowler.com/articles/feature-toggles.html
- https://itrevolution.com/accelerate-book/ — Accelerate (Forsgren et al.)
- https://continuousdelivery.com — Jez Humble
- https://dora.dev — DORA metrics framework
- https://openfeature.dev — vendor-neutral feature flag spec
- https://www.git-town.com — short-lived branch tooling
