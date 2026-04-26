# Agent Integration — Trunk-Based Development: Patterns

## When to use
- Agent is implementing a multi-step feature behind a flag (Keystone Interface, Branch by Abstraction) — give it this reference for the pattern shape.
- Setting up the pre-commit hook + CI pipeline so trunk stays releasable; the YAML/`.pre-commit-config.yaml` blocks are copy-pastable.
- Dark-launch a new implementation in parallel and diff results — the snippet is the canonical shape.
- Migrating a long-lived feature branch to a series of trunk-merged increments; agent uses Branch-by-Abstraction to chunk it.

## When NOT to use
- Branching/lifetime principles, DORA metrics, GitFlow comparison — see sibling `trunk-based-dev-principles`.
- Feature flag *infrastructure* itself (provider choice, evaluation engine) — see `feature-flags` methodology.
- Release engineering for mobile/desktop where store review breaks daily-merge cadence.
- Codebases with no test gate — TBD without tests is "trunk is always broken".

## Where it fails / limitations
- Pattern code is illustrative — `feature_flags.is_enabled("name")` assumes a real provider; agent will leave a stub and forget to wire it.
- Branch-by-Abstraction snippet skips the cleanup phase ("delete LegacyPaymentProcessor"); agents drop the abstraction and never collapse it back, leaving permanent indirection.
- Dark-launch comparison `if result != new_result` only works for deterministic, equality-comparable outputs — float / list-order cases need a tolerant diff.
- Pre-commit example runs the full `pytest` on commit; on real repos this is too slow and devs disable the hook. Use `pre-commit run --hook-stage` properly or scope to changed files.
- CI snippet has no branch protection / required-status check details — agent forgets to set `Require status checks` on `main`.

## Agentic workflow
The agent's job is to *land small, safe diffs frequently*. Use this reference when generating the wrapper code for a flagged change: read the parent feature's spec, write the smallest increment, gate it with a flag, ship via short-lived branch, and surface the cleanup task once the flag is rolled to 100%. Maintain a tracking artifact (`.aidocs/feature-flags.md` or similar) so flags don't outlive their reason.

### Recommended subagents
- `faion-sdd-executor-agent` — natural fit: it already enforces task lifecycle and quality gates aligned to "task done = merged to trunk".
- `faion-feature-executor` — for the sequential task chain inside one feature, with each task = one trunk merge.

### Prompt pattern
```
Implement payment-rewrite increment 3/5 using Branch by Abstraction.
Reference: solo/dev/automation-tooling/trunk-based-dev-patterns/README.md.
Constraints:
- abstraction PaymentProcessor exists in src/billing/abc.py
- add NewStripeProcessor; gate via flag "billing.use_new_processor"
- DO NOT delete LegacyPaymentProcessor yet
- update CHANGELOG, open SDD subtask "remove flag billing.use_new_processor"
- branch: feat/billing-stripe-3; squash-merge same day
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | GitHub PR + branch protection from CLI | https://cli.github.com |
| `pre-commit` | Local commit-time gates | `pip install pre-commit` · https://pre-commit.com |
| `lefthook` | Faster Go-based git hooks | https://github.com/evilmartians/lefthook |
| `git-absorb` | Auto-fixup commits onto right base — keeps PRs clean | https://github.com/tummychow/git-absorb |
| `gh-stack` / `git-spice` / `Graphite` CLI | Stacked PRs (small increments) | https://graphite.dev/cli |
| `act` | Run GH Actions locally before push | https://github.com/nektos/act |
| `flagsmith-cli` / `unleash-edge` / `growthbook` | Manage flags from the command line | per provider |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LaunchDarkly | SaaS | Yes — REST + webhooks | Industry default for flag infra; agents can flip flags via `ldcli`. |
| Flagsmith | SaaS / OSS | Yes — REST | OSS self-host option; cheaper. |
| Unleash | OSS | Yes — REST | Self-hosted, Apache-2.0. |
| GrowthBook | OSS / SaaS | Yes — REST | Pairs flagging with experimentation. |
| Statsig | SaaS | Yes — REST | Flags + experimentation; generous free tier. |
| GitHub branch protection | SaaS | Yes — REST/GraphQL | Required statuses + required reviews enforce TBD. |
| ConfigCat | SaaS | Yes — REST | Lightweight, simple. |
| Split.io | SaaS | Yes — REST | Enterprise flagging + ramps. |

## Templates & scripts
Minimal Branch-by-Abstraction skeleton an agent can drop in (Python):

```python
# billing/abc.py
from typing import Protocol
class PaymentProcessor(Protocol):
    def process(self, amount: "Decimal") -> "PaymentResult": ...

# billing/legacy.py
class LegacyPaymentProcessor:
    def process(self, amount): return self._gw.charge(amount)

# billing/stripe_impl.py
class StripePaymentProcessor:
    def process(self, amount): return self._stripe.create_charge(amount)

# billing/factory.py
from .flags import flags
def get_processor() -> "PaymentProcessor":
    if flags.is_enabled("billing.use_new_processor"):
        return StripePaymentProcessor()
    return LegacyPaymentProcessor()
```

See `templates.md` for the dark-launch wrapper and the keystone-API shape.

## Best practices
- Branch lifetime cap: < 24h. Rebase onto `main` before opening the PR; squash on merge so trunk history stays linear.
- One flag = one task = one cleanup ticket. File the cleanup ticket the moment the flag is born; otherwise flags accumulate to dozens.
- Flag naming: `<area>.<verb>_<thing>` (e.g., `billing.use_stripe_v2`); ban boolean negatives (`disable_x`) — they invert mid-rollout and confuse agents.
- CI must be < 10 min wall time. If it isn't, parallelise tests, cache deps, drop slow integration suites to a nightly job. Slow CI kills TBD.
- Auto-revert on red trunk: a PR that broke `main` is reverted by bot, not by humans (`git revert -m 1`); fix forward in a fresh PR.
- Forbid direct push to `main` from anyone except automation; require linear history + signed commits.
- Run dark launches at < 1% traffic for at least one diurnal cycle before scaling — bug surfaces look identical at 0.01% and 1% but error budgets diverge.

## AI-agent gotchas
- LLMs forget to remove the abstraction layer after rollout; always file the "collapse abstraction" follow-up before merging the introduction.
- Agent generates flag *checks* with hard-coded `True` defaults during local dev and forgets to revert — gate via env (`FLAGS_DEFAULT=off` in CI) and grep for literal `is_enabled(... True)`.
- Dark-launch comparison code re-raises in production paths — wrap in `try/except` at all costs; the README example does, the agent often skips it.
- Squash-merge loses commit-level granularity; agents writing 200-line PRs as one commit are fine, agents writing 2000-line PRs need a stacked-PR workflow instead.
- Agent will "fix" pre-commit failures by adding `# type: ignore` / `# noqa` instead of fixing the issue; require diff review before any new pragma.
- Human-in-loop checkpoint: any flag flip from < 50% → 100% on a billing/auth-critical path. Agent can stage the rollout but a human approves the final percent.
- Branch protection state drift: agent adding a job to CI may leave `main` not requiring it — verify via `gh api repos/:owner/:repo/branches/main/protection` after CI changes.

## References
- https://trunkbaseddevelopment.com/ — Paul Hammant's canonical site
- https://martinfowler.com/articles/feature-toggles.html — flag types & lifecycle
- https://martinfowler.com/bliki/BranchByAbstraction.html — Fowler
- https://martinfowler.com/bliki/DarkLaunching.html — dark launch
- https://itrevolution.com/accelerate-book/ — DORA metrics tied to TBD
- https://graphite.dev/blog/stacked-prs-for-trunk-based-development — stacked PRs
