# Agent Integration — Feature Flags (software-developer)

## When to use
- Trunk-based development: hide unfinished features behind release flags so `main` is always shippable.
- Progressive rollouts (1% → 10% → 50% → 100%) with auto-rollback on error/latency regression.
- A/B tests where the experiment platform reads the same flag store as the application.
- Kill switches for risky external dependencies (payments, AI inference, third-party APIs).
- Per-tenant or per-plan features (premium tier, beta access) gated by attribute targeting.
- Operational toggles (maintenance mode, circuit breaker, queue draining) flipped without redeploy.

## When NOT to use
- Static configuration that never changes per request — environment variables suffice.
- Schema migrations or storage shape changes — flags can't gate `ALTER TABLE` safely; use migration tooling.
- Permanent business rules that belong in domain logic, not toggles (flags are temporary by definition).
- Pre-product prototypes where the abstraction cost outstrips the rollout value.
- Hot paths where every microsecond matters — compile flags out for those modules instead of evaluating at runtime.

## Where it fails / limitations
- Flag debt: by industry surveys, ~80% of projects have flags older than six months still in code, raising cyclomatic complexity and obscuring intent.
- Cross-service drift: same flag key, different semantics in service A vs service B, leading to user-visible split states.
- Missing default in config: undefined flag → `is_enabled` returns False → feature stays dark in prod indefinitely.
- Auth-coupled flags: gating premium features off `user.role` lookup — when the role lookup fails, paying users get blocked.
- A/B leakage: user opens two tabs and gets two variants; analytics treats it as one user with conflicting events.
- Provider outage = your outage if no fail-safe default per call (LaunchDarkly / Statsig down → all flags evaluate to OFF, breaking premium customers).
- PII leakage: passing entire user objects to the flag service is common; it's a hidden compliance risk (GDPR, HIPAA).
- Test coverage usually stops at the ON branch; OFF branch rots and causes "ghost bugs" when the flag is removed.

## Agentic workflow
A flag-management agent owns the lifecycle. (1) For new features: it generates the flag definition (key, type, default, owner, expiry), wraps the new code path in `is_enabled(...)`, and writes both ON and OFF tests. (2) For rollouts: it observes error-rate and latency dashboards, advancing the percentage when SLOs hold, rolling back on regression. (3) For cleanup: a scheduled audit agent finds expired flags and opens cleanup PRs (delete the flag, drop the OFF branch, simplify the surrounding code with `piranha`-style transforms). `faion-sdd-executor-agent` enforces the gate "every new flag ships with both branches tested + an expiry SDD task in `todo/`". A human approves any kill-switch flip and any rollout > 25%.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate: rejects PRs adding flags without expiry, owner, or both-branch tests.
- `faion-improver` (skill at `skills/faion-improver/`) — runs the periodic stale-flag audit, opens GitHub issues with cleanup steps.
- `faion-feature-executor` (skill) — sequences the rollout playbook (1% → bake → 10% → bake → 50% → bake → 100% → cleanup task) as ordered SDD tasks.
- A **flag-cleanup** subagent (worth creating): given a flag key marked rolled-out, runs `git grep`, removes the conditional, deletes both branches, opens PR. Pairs well with `piranha`.

### Prompt pattern
New flag scaffold:
```
New flag: <key>. Type: release|experiment|ops|permission|kill-switch.
Owner: <handle>. Expiry: <YYYY-MM-DD> (mandatory unless type=permission).
Default: false (release/experiment) or true (kill-switch).
Generate:
1. Flag entry in flags.py / flags.ts registry.
2. Wrap NEW code path with is_enabled(<key>, user_id, attrs).
3. Tests: tests/<feature>_on_test.py and tests/<feature>_off_test.py.
4. SDD cleanup task in todo/ titled "remove flag <key> by <expiry>".
Reject the change if any of (1)-(4) is missing.
```

Audit pass:
```
List all flags with (expiry < today) OR (last_changed > 90d ago) OR
(rollout=100% for 30d). For each, propose REMOVE / ROLLBACK / EXTEND.
EXTEND requires a justification ≤2 sentences and a new expiry. Output
as a markdown table; do not auto-execute REMOVE on permission flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ldcli` | LaunchDarkly CLI | `brew install launchdarkly/tap/ldcli` |
| `unleash-cli` | Manage Unleash flags | `npm i -g unleash-cli` |
| `flagsmith-cli` | Flagsmith CLI | `npm i -g flagsmith-cli` |
| `growthbook` | OSS A/B + flags CLI | `npm i -g growthbook` |
| `openfeature` SDK | Vendor-neutral flag API | `pip install openfeature-sdk` / `npm i @openfeature/sdk` |
| `piranha` | Auto-removal of stale flags from source (Uber) | https://github.com/uber/piranha |
| `posthog` CLI | PostHog feature flags + analytics | https://posthog.com/docs |
| `statsig` CLI | Statsig flags + experiments | https://docs.statsig.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LaunchDarkly | SaaS | Yes — REST + CLI | Industry default; pricey at scale. |
| Flagsmith | SaaS + OSS | Yes — REST + self-host | Good solo-tier and on-prem story. |
| Unleash | SaaS + OSS | Yes — REST | Strong gradual-rollout strategies. |
| GrowthBook | SaaS + OSS | Yes — REST + SDK | Combines flags + experiments + warehouse. |
| ConfigCat | SaaS | Yes — REST | Solo-friendly; simple model. |
| PostHog | SaaS + OSS | Yes — REST | Bundled with product analytics, free tier. |
| Statsig | SaaS | Yes — REST | Strong on experimentation + cohorts. |
| Split.io | SaaS | Yes — REST | Enterprise; deep experimentation. |
| OpenFeature (CNCF) | OSS spec | Yes | Provider-neutral API, avoids lock-in. |
| Cloudflare Workers KV | SaaS | Partial — KV API | DIY edge flags; no targeting UI. |

## Templates & scripts
See `templates.md` and `examples.md` for full FlagManager + targeting code. Stale-flag audit (≤50 lines):

```python
# find_stale_flags.py — list flags older than N days; cross-check git usage.
import json, subprocess, sys
from datetime import datetime, timedelta, timezone

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 90
cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)

flags = json.loads(subprocess.check_output(
    ["ldcli", "flags", "list", "--output", "json"]
))

stale = []
for f in flags:
    last = datetime.fromisoformat(f["lastModified"].replace("Z", "+00:00"))
    if last < cutoff:
        files = subprocess.run(
            ["git", "grep", "-l", f["key"]], capture_output=True, text=True
        ).stdout.strip().splitlines()
        stale.append({"key": f["key"], "last": last.isoformat(),
                      "files": files, "rollout": f.get("rollout", "n/a")})

print(json.dumps({"days": DAYS, "stale": stale}, indent=2))
sys.exit(1 if stale else 0)
```

Wire into a weekly GitHub Actions cron + open an issue with the JSON body for `faion-improver` to triage.

## Best practices
- Every flag must carry: key, type, default, owner, expiry. CI fails the PR if any field is missing.
- Default OFF for new code paths; default ON for kill switches (so the safe state during outage is "feature off").
- Test both branches. Treat untested OFF branch as a coverage failure, not a warning.
- Log flag evaluations with low sample-rate; you'll need this during incidents.
- Couple rollout to error-rate alerts: > 0.5% spike vs 24h baseline → automatic flip back to OFF.
- Keep `is_enabled` pure and < 1ms — cache locally, refresh in background. Async network calls in hot paths are an anti-pattern.
- Use OpenFeature SDK so you can swap provider without rewriting call sites.
- Quarterly cleanup ritual: every flag past expiry must be removed or formally extended with a new expiry.
- Concentrate flag checks at decision boundaries (entry of feature module), not scattered across functions — fewer branches to test and remove.

## AI-agent gotchas
- Agents add `if flag_enabled("foo")` everywhere instead of at one decision point — multiplies branches and makes cleanup hard.
- LLMs forget the OFF-branch tests. Force the gate at PR-review time.
- When generating an eval client, agents often hardcode `default=True` so "tests pass locally" — leaks features to prod.
- Removal asymmetry: agents may delete the `if` check but leave the now-dead OFF branch (or vice versa). Use `piranha` or strict review.
- Targeting attribute leak: agents pass entire user objects to the flag service. Whitelist attributes (id + plan + region) at the SDK boundary.
- Human-in-loop checkpoint: any new permission/kill-switch flag and any rollout > 10% must be human-approved.
- Flag-name drift: agents create `new_checkout_v2` then `new_checkout_v3` instead of editing the existing flag. Lock the registry; agents must rename, not duplicate.
- Incident response: agents asked to "disable feature X" sometimes flip the wrong flag. Require explicit flag key + dry-run + diff before applying in prod.
- Rollback ambiguity: when an agent flips a flag back, it may not record the reason in the audit log — make the reason field mandatory on every flag change.

## References
- Pete Hodgson — "Feature Toggles (aka Feature Flags)". https://martinfowler.com/articles/feature-toggles.html
- LaunchDarkly Documentation — https://docs.launchdarkly.com/
- OpenFeature specification — https://openfeature.dev/
- Unleash documentation — https://docs.getunleash.io/
- Uber Piranha (stale flag cleanup) — https://github.com/uber/piranha
- "Test in Production" — Nora Jones / Charity Majors blog posts.
- Sibling methodologies in this repo: `solo/dev/automation-tooling/feature-flags/`, `solo/dev/automation-tooling/trunk-based-dev-patterns/`, `solo/dev/automation-tooling/cd-pipelines/`, `solo/dev/automation-tooling/ab-testing-implementation/`.
