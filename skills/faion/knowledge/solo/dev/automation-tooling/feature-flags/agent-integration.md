# Agent Integration — Feature Flags

## When to use
- Trunk-based development: hide incomplete features behind release flags so main is always shippable.
- Progressive rollouts (1% → 10% → 50% → 100%) with automatic rollback on error-rate spike.
- A/B experiments where the experiment platform reads the same flag store as the app.
- Kill switches for risky integrations (third-party payments, AI calls) — flip without redeploy.
- Per-tenant features (premium tier, beta access) with attribute-based targeting.

## When NOT to use
- One-line config that never changes — env vars suffice.
- Database schema changes — flags can't gate ALTER TABLE migrations safely.
- Permanent business rules that should be encoded in domain logic, not toggles.
- Pre-production prototypes where complexity outweighs value.
- Time-critical paths where even 1ms of flag-evaluation latency matters (cache or compile out).

## Where it fails / limitations
- Flag debt: 80% of projects have flags older than 6 months still in code; cyclomatic complexity explodes.
- Cross-service flag drift: same flag name, different semantics in service A vs B → user sees broken state.
- Missing default in config: flag undefined → `is_enabled` returns False → feature stays off forever in prod.
- Auth + flag interaction: flag for premium users gated by user.role check; if role lookup fails, flag denies even paying users.
- A/B leakage: user opens two tabs, gets two variants — analytics treats as one user.
- LaunchDarkly outage = your app outage if not coded with a fail-safe default per call.

## Agentic workflow
A flag agent: (1) reads the flag registry; (2) for new features, generates a flag definition (name, type, default, owner, expiry); (3) wraps the new code path in `if flag.is_enabled(...)`; (4) writes both ON and OFF tests; (5) registers a cleanup task in the SDD backlog with the expiry date. For removal, an agent finds expired flags, generates the cleanup PR (delete the flag, remove the OFF branch, simplify the code). `faion-sdd-executor-agent` enforces "every new flag has both branches tested" as a quality gate.

### Recommended subagents
- `faion-sdd-executor-agent` — gates on "both flag branches covered by tests" + "flag has expiry".
- `faion-improver` (skill) — periodic audit pass to surface stale flags.

### Prompt pattern
```
New flag: <name>. Type: release|experiment|ops|permission|kill-switch.
Owner: <handle>. Expiry: <YYYY-MM-DD>.
Default in code: false (release/experiment) or true (kill-switch).
Generate:
1. Flag definition in flags.py / flags.ts.
2. Wrap the new branch with is_enabled().
3. Two test files: tests/<feature>_on_test.py, tests/<feature>_off_test.py.
4. SDD cleanup task in todo/ with expiry date in title.
```

```
Audit flags: list all flags with expiry < today() OR last_changed > 90 days ago.
For each: propose REMOVE if rollout=100%, ROLLBACK if errors>baseline, EXTEND with justification.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `unleash-cli` | Manage Unleash flags from CLI | `npm i -g unleash-cli` |
| `ld-cli` | LaunchDarkly CLI | `brew install launchdarkly/tap/ldcli` |
| `flagsmith-cli` | Flagsmith CLI | `npm i -g flagsmith-cli` |
| `growthbook` (CLI) | OSS A/B + flags | `npm i -g growthbook` |
| `openfeature` SDK | Vendor-neutral flag API | `pip install openfeature-sdk` / npm |
| `piranha` (Uber) | Auto-cleanup of stale flags | https://github.com/uber/piranha |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LaunchDarkly | SaaS | Yes — REST API + CLI | Industry default; pricey at scale. |
| Flagsmith | SaaS + OSS | Yes — REST + self-host | Self-hostable; agent-friendly REST. |
| Unleash | SaaS + OSS | Yes — REST | Strong OSS; gradual rollout strategies. |
| GrowthBook | SaaS + OSS | Yes — REST + SDK | Combines flags + experimentation + warehouse. |
| ConfigCat | SaaS | Yes — REST | Solo-friendly tier; simple model. |
| PostHog Feature Flags | SaaS + OSS | Yes — REST | Bundled with product analytics. |
| Statsig | SaaS | Yes — REST | Strong on experimentation. |
| OpenFeature (CNCF) | OSS spec | Yes | Use via provider; avoids vendor lock-in. |
| Cloudflare Workers KV | SaaS | Partial — KV API | DIY edge flags; no targeting UI. |

## Templates & scripts
See `templates.md` for full FlagManager + targeting starter. Stale-flag finder (≤50 lines):

```python
# find_stale_flags.py — list flags older than N days
import json, subprocess, sys
from datetime import datetime, timedelta

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 90
cutoff = datetime.utcnow() - timedelta(days=DAYS)

flags = json.loads(subprocess.check_output(
    ["ld-cli", "flags", "list", "--output", "json"]
))

for f in flags:
    last = datetime.fromisoformat(f["lastModified"].replace("Z", "+00:00"))
    if last.replace(tzinfo=None) < cutoff:
        usage = subprocess.run(
            ["git", "grep", "-l", f["key"]], capture_output=True, text=True
        ).stdout.strip().splitlines()
        print(f"STALE: {f['key']:40s} last={last:%Y-%m-%d} files={len(usage)}")
```

```yaml
# .github/workflows/flag-audit.yml — weekly stale-flag check
on:
  schedule: [{ cron: '0 9 * * 1' }]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/find_stale_flags.py 90 > stale.txt
      - run: gh issue create --title "Stale flags audit $(date -I)" --body-file stale.txt
        env: { GH_TOKEN: '${{ secrets.GITHUB_TOKEN }}' }
```

## Best practices
- Every flag has: name, type, default, owner, expiry. No exceptions.
- Default off for new code paths; default on for kill switches.
- Test both branches. Code-coverage tools should treat untested branch as a fail.
- Log flag evaluations with sample-rate; needed during incidents.
- Couple flag rollout to error-rate alerts: > 0.5% spike → automatic flip back to off.
- Keep flag eval functions pure and fast (< 1ms) — cache locally, refresh in background.
- Use OpenFeature SDK so the provider can be swapped without rewriting call sites.
- Quarterly cleanup ritual: every flag past expiry must be either removed or formally extended with new expiry.

## AI-agent gotchas
- Agents add `if flag_enabled("foo")` everywhere instead of at the decision point — scattered flags multiply branches.
- LLMs forget the OFF branch tests. Force the gate.
- When generating a flag-eval client, agents often hardcode `default=True` so "tests pass locally" — leaks features to prod.
- Removal is harder than addition: agents may delete the flag check but leave the OFF branch, or vice versa. Use `piranha` or a strict review.
- Targeting rules with attribute lookups can leak PII into the flag service; agents pass entire user objects. Whitelist attributes.
- Human-in-loop checkpoint: any new permission/kill-switch flag and any rollout percentage > 10% must be human-approved.
- Flag names tend to drift (`new_checkout_v2` → `new_checkout_v3` → `checkout_redesign`). Lock the registry; agents must rename, not duplicate.
- During incidents, agents asked to "disable feature X" sometimes flip the wrong flag. Require explicit flag key + dry-run.

## References
- "Feature Flag Best Practices" — Pete Hodgson, martinfowler.com
- LaunchDarkly docs — https://docs.launchdarkly.com/
- OpenFeature spec — https://openfeature.dev/
- Unleash docs — https://docs.getunleash.io/
- Uber Piranha (flag cleanup) — https://github.com/uber/piranha
- Sibling: `ab-testing-implementation/`, `trunk-based-dev-patterns/`, `cd-pipelines/`.
