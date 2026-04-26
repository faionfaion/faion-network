# Agent Integration — Continuous Delivery Basics

## When to use
- Onboarding a team that does manual deploys and needs CD principles, prerequisites, and a phased roadmap.
- Auditing an existing pipeline against the CD vs CI vs Continuous Deployment matrix and DORA targets.
- Designing backward-compatible migration patterns (expand-contract) so deploys are decoupled from data changes.
- Introducing feature flags as the bridge between "code shipped" and "feature released."
- Diagnosing CD blockers: large batches, slow tests, manual gates, fear-of-prod.

## When NOT to use
- For pipeline YAML and deployment-strategy mechanics. Read `cd-pipelines/` next.
- For full GitOps (Argo/Flux) — that's a `pro/infra/cicd-engineer` topic.
- For mobile app store releases — review/policy gates dominate; CD principles apply but tooling diverges.
- For environments where regulatory release boards are mandatory (medical, aviation, banking core). CD is achievable but with heavier automation around evidence capture.
- When CI is not yet in place. CD prerequisites listed in the README must be true first.

## Where it fails / limitations
- "Phase X: 2-4 weeks" timelines in the README contradict project policy "no time estimates" — agents must drop those when generating roadmaps.
- Feature-flag snippet uses an in-process cache that defeats real-time targeting; treat it as a sketch.
- Migration example is single-step "add nullable" then "make required" — real expand-contract has 3-4 deploys with a backfill in between.
- DORA metric definitions in the README are correct but compact; many teams misread "lead time for changes" as cycle time.
- "Common Challenges" gives causes + solutions but doesn't address culture/management blockers (release boards, change advisory boards).
- No coverage of release notes automation, semantic versioning, or rollback comms — all relevant to CD in practice.
- Health-check pattern is fine for stateless services; for services with warm-up (model loading, JIT), readiness needs a longer initialDelay.

## Agentic workflow
Use this file as a maturity-assessment lens before any pipeline work. The agent reads the team's current pipeline + deploy story, scores against the CD vs CD matrix and DORA elite targets, and outputs a phased roadmap of concrete tasks (drop the time estimates; use complexity tiers per project policy). Hand off to the `cd-pipelines/` agent for YAML implementation, to `feature-flags/` for flag system, and to `trunk-based-dev-*` for branch-strategy work. Never treat "we can't deploy that often" as a tooling problem alone — the agent must include checklist items for batch-size discipline and test-pyramid rebalancing.

### Recommended subagents
- `general-purpose` — assessment, roadmap drafting, single-doc edits.
- `faion-sdd-executor-agent` — when CD adoption is captured as SDD features over many tasks.
- A narrow `migration-planner` task agent — given a schema change request, outputs the expand-contract sequence (deploys 1..N) with reversibility notes.
- A `release-notes-bot` task agent — generates release notes from commits between two SHAs to lubricate frequent deploys.

### Prompt pattern
```
Read solo/dev/automation-tooling/cd-basics/README.md.
Audit <repo> for CD readiness. Score against: CI present, automated tests
adequate, IaC, feature flags, backward-compat migrations. Output a roadmap
in 5 phases (Foundation→Continuous Deployment) with task complexity tiers
(Low/Med/High), token estimates, and explicit gates between phases. Do NOT
include time estimates.
```
```
Plan an expand-contract migration to make column users.email NOT NULL.
Number deploys 1..N. For each deploy describe: code change, schema change,
data backfill, rollback plan. Verify backward compatibility at every step.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` / `glab` | Read merge cadence, PR size, deploy frequency from CI runs | github CLI / gitlab CLI |
| `dora-team/fourkeys` | Compute DORA metrics from CI + incident events | github.com/dora-team/fourkeys |
| `git log --since` + custom scripts | Estimate lead time per commit | n/a |
| `liquibase` / `flyway` / `alembic` / `sqitch` | Versioned schema migrations | tool docs |
| `pre-commit` | Enforce small-batch hygiene (lint, secret scan) before merge | pre-commit.com |
| `release-please` / `semantic-release` | Automated versioning + changelog | googleapis/release-please, semantic-release |
| `conventional-commits-parser` | Detect breaking-change commits to gate releases | npm |
| `lefthook` / `husky` | Git hooks orchestrators | tool docs |
| `gh deploy` (custom) / `gh api repos/.../deployments` | Mark deployment events | gh CLI |
| `gitleaks` / `trufflehog` | Block secrets (CD requires no secrets in repo) | tool docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LaunchDarkly | SaaS | Yes | Mature flag system; necessary for CD. |
| Unleash | OSS | Yes | Self-host; OpenAPI for agents. |
| Flagsmith | OSS + SaaS | Yes | Open-source friendly. |
| GrowthBook | OSS | Yes | Flags + experiments in one. |
| Statsig | SaaS | Yes | Flags + experiments + analytics. |
| Sleuth.io | SaaS | Yes | DORA metrics out of the box. |
| LinearB | SaaS | Yes | DORA + dev efficiency dashboards. |
| Faros AI / Apiiro | SaaS | Yes | DORA + risk; code-to-prod observability. |
| GitHub Environments / GitLab Environments | SaaS | Yes | Required-reviewer gates fit "manual approval" CD. |
| Atlassian Compass | SaaS | Partial | DORA scorecards, opinionated. |
| Honeycomb / Datadog / Grafana | SaaS / OSS | Yes | SLO burn-rate as auto-rollback signal. |
| StatusGator / Statuspage | SaaS | Partial | Surface deploy events to users. |

## Templates & scripts
See `templates.md` and `examples.md`. Minimum CD-readiness scorecard agents can fill in:

```yaml
# .aidocs/cd-readiness.yaml — fill once per service
service: <name>
ci:
  build_on_every_commit: true
  unit_test_coverage_pct: 0
  pipeline_p95_minutes: 0
tests:
  integration_automated: false
  e2e_on_staging: false
  flake_rate_pct: 0
infra:
  iac_for_app: false
  iac_for_db: false
  ephemeral_envs: false
release:
  feature_flags_in_use: false
  backward_compat_migrations: false
  rollback_rehearsed: false
  one_click_prod_deploy: false
metrics:
  deploy_frequency_per_week: 0
  lead_time_hours: 0
  change_failure_rate_pct: 0
  mttr_minutes: 0
gaps: []
next_phase: foundation|automated-testing|staging|production|continuous-deploy
```

## Best practices
- Trunk-based small batches: target <200 LOC per PR; large PRs are the #1 CD blocker.
- Every migration is reversible; expand → migrate data → contract spans multiple deploys.
- Decouple deploy from release: ship code dark behind a flag; release by toggling, not deploying.
- Track deploy outcomes (success/fail) and incidents in the same store so DORA metrics stay honest.
- Make failed deploys cheap: trivial rollback, automatic rollback on smoke-test failure, no DB lock-in.
- Keep CI under 15 minutes p95; longer pipelines cause batching.
- Pipeline-as-code in the same repo as the app; no out-of-band Jenkins jobs.
- Run staging traffic against the same DB schema migration order as prod will use; surface "expand" vs "contract" timing bugs early.

## AI-agent gotchas
- Agents will copy the README's "Phase X: Y weeks" verbatim; project policy bans time estimates. Strip and replace with complexity tiers.
- "Implement feature flags" prompts produce the README's in-process cache snippet; in production this hides flag changes for hours. Use SSE/WebSocket-based flag SDK or short TTL.
- Agents conflate Continuous Delivery and Continuous Deployment; the matrix in the README is the source of truth — quote it back.
- Migration: agents merge expand and contract into one PR ("less work"). Force two-PR rule.
- DORA: agents will compute "deploy frequency" from `git push` events; correct definition is successful production deployments. Wire to the deploy job, not push.
- "Reduce E2E to make CI faster" — agents will delete tests rather than parallelize. Add a CI-time budget and a coverage floor.
- Release boards / change tickets: agents will paste the same boilerplate ticket per deploy. Templatize once and link the deploy SHA, don't regenerate.
- Health checks: agents merge `/health` and `/health/ready` — readiness should fail when dependencies are down; liveness should not. Keep them separate.

## References
- Jez Humble, David Farley, Continuous Delivery (Pearson, 2010).
- Forsgren, Humble, Kim, Accelerate (IT Revolution, 2018).
- DORA: https://www.devops-research.com/research.html
- Martin Fowler, Continuous Delivery: https://martinfowler.com/bliki/ContinuousDelivery.html
- Expand-contract migrations: https://martinfowler.com/articles/evodb.html
- Trunk-Based Development: https://trunkbaseddevelopment.com/
- Sibling: `solo/dev/automation-tooling/cd-pipelines/`, `feature-flags/`, `continuous-delivery/`, `trunk-based-dev-principles/`.
