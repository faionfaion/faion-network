# AGENT-09 — AI Agents That Open or Review Merge/Pull Requests

**Summary (2 lines):** April 2026 — error trackers (Sentry Seer, Dependabot), review bots (CodeRabbit,
Greptile, Qodo, Sourcery, Copilot), and dependency/refactor agents (Renovate, Codemod, Bits)
all converge on the same shape: a typed signal (alert, label, issue, diff) drives an LLM that opens a
DRAFT PR with a generated title/body/tests, gated by author identity, label policy, and CODEOWNERS.

Scope: Sentry Seer Autofix, Bugsink/Rollbar, GitHub Copilot Code Review, GitHub Copilot Coding Agent
(Dependabot handoff), Qodo Merge (ex-CodiumAI PR-Agent), CodeRabbit, Sourcery, Greptile, Codeball,
AutoPR, Renovate/Mend, Datadog Bits AI Dev Agent (flake fixer), Hypermod/Codemod (refactor codemods),
Devin (spec→PR). 11 methodologies, mapped to `mr-`, `task-`, `inc-`.

Cross-refs: AGENT-04 (issue-to-implementation pipeline), AGENT-06 (incident response), AGENT-08
(merge governance & release gates), AGENT-10 (CI/CD agents).

---

## mr-01 — Error-tracker → DRAFT-PR pipeline (the "500-to-MR" pattern)

**Rule:** When an exception in production crosses an event-count + fixability threshold, dispatch a
coding agent that ingests `{stack_trace, breadcrumbs, trace, linked_repo, recent_diffs}`, proposes a
patch + unit-test, and opens a **draft** PR cross-linked to the alert. The PR is never created
silently — the alert URL goes in the body, the alert page links back to the PR, and a human still
clicks Merge. Sentry Seer/Autofix is the canonical implementation: trigger is "10+ events AND high
fixability score" or manual `/autofix`, and the PR can span multiple repos when the trace is
distributed.

**Cite:**
- https://docs.sentry.io/product/ai-in-sentry/seer/autofix/
- https://blog.sentry.io/sentry-ai-debugger-autofix-superpower-traces/
- https://sentry.io/changelog/autofix-beta-now-available/
- https://www.starsling.dev/sentry (third-party Sentry→PR agent variant)
- https://www.bugsink.com/ (Sentry-compatible self-hosted; same DSN, same pattern works)
- https://rollbar.com/ (Rollbar MCP exposes the same trace context to coding agents)

**When to use:**
- Production runtime errors with a clean stack trace and source map.
- Repeatable exceptions (NullPointer, KeyError, IntegrityError) that map 1:1 to a code line.
- Cross-service errors where the trace already correlates the failure (auth bug across BE+FE).

**When NOT to use:**
- One-off errors (< 10 events) — noisy, expensive, low fixability.
- Errors with no stack trace (network timeout, OOM, kernel panic).
- Business-logic bugs where the "fix" is a product decision, not a code change.
- Strict-compliance repos where DRAFT PRs from bots are still treated as production code on import.

**Tiny example:**
```yaml
# Sentry → Seer → GitHub: org-level config
seer:
  autofix:
    auto_run_threshold:
      min_events: 10
      min_fixability: 0.7
    repos:
      - github.com/acme/api          # Seer SCM Settings
      - github.com/acme/web
    pr_mode: draft                    # never auto-merge
    pr_body_template: |
      Sentry alert: {alert_url}
      Root cause (LLM): {root_cause}
      Test added: {test_path}
```

---

## mr-02 — DRAFT-by-default + bot identity + required-human-approval gate

**Rule:** Every agent-authored PR opens as **draft**, authored by a dedicated bot identity
(GitHub App or `*-bot` user), labelled `agent:<name>`, and protected by a branch rule that requires
≥1 review from a human in CODEOWNERS. GitHub does NOT have a first-class "bot-only path" — you
emulate it with: (a) bypass-list for the bot on `Allow specified actors to bypass PRs` is
explicitly NOT set, (b) "Require approval of the most recent reviewable push" is ON, which already
forces n+1 approvals when a coding agent adds a commit, (c) a label-based policy tool gates merge
on `human-reviewed` label.

**Cite:**
- https://github.com/palantir/policy-bot (label/CODEOWNERS-aware merge policy)
- https://github.com/marketplace/actions/label-based-pr-policy-action
- https://github.com/orgs/community/discussions/172019 (Copilot agent + n+1 approvals semantics)
- https://igotasite4that.com/blog/securing-ai-coding-agent-workflows/ (sandbox + review gates)
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization

**When to use:**
- Any repo where you let an agent open PRs (Sentry Seer, Renovate, Copilot Coding Agent, Devin).
- Compliance-sensitive code (SOC2, HIPAA): use this even for trivial dependency bumps.

**When NOT to use:**
- Throwaway repos, hackathon code, demos — overhead exceeds value.
- Solo projects where you ARE the CODEOWNER (no one else to approve).

**Tiny example:**
```yaml
# .github/policy-bot.yml
policy:
  approval:
    - or:
        - human review on agent PR
rules:
  - name: human review on agent PR
    if:
      has_author_in: { users: ["seer-by-sentry[bot]", "dependabot[bot]", "copilot-swe-agent[bot]"] }
    requires:
      count: 1
      teams: ["acme/maintainers"]
```

---

## mr-03 — Slash-command surface for review bots (`/describe`, `/review`, `/improve`, `/autofix`)

**Rule:** Expose review-bot capabilities as PR-comment slash commands so humans steer the bot in-band
instead of via dashboards. Qodo Merge / PR-Agent set the standard: `/describe` regenerates title +
walkthrough, `/review` posts inline issues, `/improve` posts code-suggestion patches you can apply
with one click, `/ask "why does this regex differ?"` queries the diff. Auto-trigger `/describe`
+ `/review` on PR open; leave `/improve` opt-in (it's the noisy one).

**Cite:**
- https://qodo-merge-docs.qodo.ai/tools/review/
- https://docs.qodo.ai/qodo-documentation/qodo-merge/pr-agent/usage-guide/automations_and_usage
- https://github.com/qodo-ai/pr-agent
- https://docs.coderabbit.ai (`@coderabbitai` chat, `/resolve`, `/review` commands)
- https://docs.sourcery.ai/Code-Review/Overview/

**When to use:**
- Multi-author repos where humans want a "second pair of eyes" before requesting human review.
- High-PR-volume repos (>20/day) where humans drown in description-writing.

**When NOT to use:**
- Repos with strict "no third-party app on source" policy without a self-hosted PR-Agent install.
- Tiny PRs (<20 LOC) — `/review` adds more noise than it removes.

**Tiny example:**
```yaml
# .github/workflows/qodo-merge.yml
on:
  pull_request: { types: [opened, reopened, ready_for_review] }
  issue_comment: { types: [created] }   # required for /commands to work
jobs:
  pr_agent:
    runs-on: ubuntu-latest
    steps:
      - uses: qodo-ai/pr-agent@main
        env:
          OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # auto-run on open:
          GITHUB_ACTION_CONFIG.AUTO_DESCRIBE: "true"
          GITHUB_ACTION_CONFIG.AUTO_REVIEW: "true"
          GITHUB_ACTION_CONFIG.AUTO_IMPROVE: "false"
```

---

## mr-04 — Codebase-graph reviewers vs diff-only reviewers (pick one knowingly)

**Rule:** Two architectures co-exist and behave differently. **Diff-only** reviewers (Codeball,
Sourcery, GitHub Copilot Code Review) read the patch + nearest neighbours — fast, cheap, miss
cross-file impact. **Graph-indexed** reviewers (Greptile, CodeRabbit Pro, Qodo 2.0 multi-agent)
build a repo-wide knowledge graph and check ripple effects — slower, expensive, catch
cross-module breakage. Pick diff-only for monorepos with strong module isolation; pick graph-indexed
for legacy code where one file change quietly breaks five callers.

**Cite:**
- https://www.greptile.com/what-is-ai-code-review (graph-indexed)
- https://www.coderabbit.ai/ (graph + multi-agent)
- https://docs.sourcery.ai/Code-Review/Overview/ (diff + Python-static-analysis)
- https://github.com/sturdy-dev/codeball-action (deep-learning classifier, diff-only, score 0..1)
- https://en.wikipedia.org/wiki/Qodo (Qodo 2.0 Feb-2026: multi-agent + PR-history context)
- https://docs.github.com/en/copilot/concepts/agents/code-review

**When to use:**
- Graph-indexed → polyglot legacy codebases, high cross-file refactor risk, enterprise audit.
- Diff-only → green-field, well-modularised, cost-sensitive, latency-sensitive (PR < 60s feedback).

**When NOT to use:**
- Don't pay for a graph-indexed reviewer if your repo is < 50k LOC and well-isolated — diff-only is
  90% as good at 10% of the cost.
- Don't pick diff-only if your team's bug pattern is "this innocent rename broke a downstream
  consumer in another package" — exactly the case graph-indexed catches.

**Tiny example:**
```text
# decision tree
LOC > 500k OR polyglot OR weak module boundaries → Greptile / CodeRabbit Pro / Qodo Merge Pro
LOC < 100k AND strong modules AND <60s feedback target → Sourcery / Codeball / Copilot Review
mixed                                                  → Copilot Review (free) + on-demand /review
```

---

## mr-05 — `agent-fixable` label triage gate (humans pick, agent works)

**Rule:** Agents that turn issues into PRs (Devin, Copilot Coding Agent, Codex) burn tokens
spinning on issues they cannot solve. Insert a triage label — `agent-fixable`, `copilot`,
`devin-pickup` — applied by a human or a triage bot AFTER duplicate/spam/scope checks. Agent only
listens for that label. Result: ~3× higher merge rate vs "agent reads every new issue".

**Cite:**
- https://github.com/gastownhall/gastown/discussions/1703 (agent-fixable label pipeline pattern)
- https://docs.devin.ai/ (Devin reads tickets from Linear/Jira/Slack, gated by tag/queue)
- https://cognition.ai/blog/devin-review (PR merge rate 34%→67% over 2025; gating helped)
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization

**When to use:**
- Issue tracker has > 50 open items — without a gate, agent picks the wrong ones.
- Mixed agent fleet (Devin + Copilot + Codex) — same label assigns to whichever queue is free.

**When NOT to use:**
- Tiny backlogs where a human picks each issue manually anyway.
- Issues that need product-discovery, not code (the gate cannot tell — keep these labelled
  `needs-spec` and never let an agent touch them).

**Tiny example:**
```yaml
# .github/workflows/agent-pickup.yml
on:
  issues: { types: [labeled] }
jobs:
  dispatch:
    if: github.event.label.name == 'agent-fixable'
    runs-on: ubuntu-latest
    steps:
      - run: gh agent run devin --issue ${{ github.event.issue.number }}
```

---

## mr-06 — Renovate-style dependency PRs + AI handoff for breaking updates

**Rule:** Run Renovate (or Dependabot) for the deterministic 90% of dep bumps — semver-safe,
auto-merge on green CI with a Merge-Confidence score. Reserve LLM agents for the 10% where the
bump introduces breaking API changes or vulnerability fixes that need code edits. GitHub shipped
this exact split April 2026: Dependabot detects the alert, you "Assign to Agent" (Copilot/Claude/
Codex), the agent opens a DRAFT PR with the version bump + the call-site edits + test fixes. You
can assign multiple agents and pick the best PR.

**Cite:**
- https://www.mend.io/renovate/ (Merge Confidence score, 90+ package managers)
- https://docs.renovatebot.com/ (config recipes, auto-merge gating)
- https://github.blog/changelog/2026-04-07-dependabot-alerts-are-now-assignable-to-ai-agents-for-remediation/
- https://medium.com/@ankithoney/githubs-dependabot-can-now-hand-off-the-hard-fixes-to-ai-coding-agents-7e6fa127aaa7
- https://www.dynatrace.com/news/blog/dynatrace-mcp-server-and-github-copilot-coding-agent/ (runtime
  vuln context → MCP → Copilot agent → PR)

**When to use:**
- Any repo with a `package.json`/`requirements.txt`/`go.mod`/`Cargo.toml`. Free tier covers it.
- Security-alert remediation where the patch is non-trivial (call-sites moved, API changed).

**When NOT to use:**
- Don't auto-merge MAJOR version bumps even with high Merge-Confidence — let a human or an agent
  rewrite call sites first.
- Don't burn agent tokens on a Renovate-clean PR (semver-patch with all-green CI) — auto-merge it.

**Tiny example:**
```jsonc
// renovate.json
{
  "extends": ["config:base", "schedule:weekly"],
  "packageRules": [
    { "matchUpdateTypes": ["patch", "minor"], "automerge": true,
      "automergeType": "branch", "platformAutomerge": true },
    { "matchUpdateTypes": ["major"], "labels": ["agent-fixable"] }   // hand to AI agent
  ]
}
```

---

## mr-07 — Spec → PR pipeline (issue body IS the prompt)

**Rule:** Treat a labelled issue as the agent's input contract: title = goal, body = acceptance
criteria + linked design doc, code-fences with API signatures = constraints, "Out of scope" section
= negative prompts. Agent (Devin / Copilot Coding Agent / Codex) writes implementation, runs tests,
opens PR linked to issue with `Closes #N`. Specs that work: ≥ 3 clear acceptance criteria, file
paths to touch, examples. Specs that fail: vague goals, no AC, no test plan.

**Cite:**
- https://addyosmani.com/blog/good-spec/ (how to write a spec for AI agents)
- https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/
- https://medium.com/quantumblack/agentic-workflows-for-software-development-dc8e64f4a79d
- https://docs.devin.ai/
- https://docs.github.com/en/copilot/concepts/agents/code-review (assign issue → coding agent)

**When to use:**
- Routine CRUD features, well-scoped bug fixes, known-pattern refactors.
- Spec-Driven Development repos where every feature already has a `spec.md` + `test-plan.md`.

**When NOT to use:**
- Architectural decisions, novel algorithms, performance work (agent will pattern-match wrong).
- Cross-cutting refactors that need staged rollout (use mr-08 instead).

**Tiny example:**
```markdown
<!-- ISSUE TEMPLATE: agent-spec.md -->
## Goal
Add idempotency-key support to POST /payments.

## Acceptance criteria
- [ ] Header `Idempotency-Key` (UUID) parsed in `payments/views.py::PaymentCreateView`.
- [ ] Cache key in Redis 24h via `cache.set(...)`.
- [ ] Returns 409 on duplicate key with different body.

## Files to touch
- payments/views.py, payments/tests/test_views.py, docs/api.md

## Out of scope
- DB migrations, batch endpoints.

/label agent-fixable
```

---

## mr-08 — Codemod / refactor agents (rename API, framework migration)

**Rule:** Cross-cutting refactors (Angular 17→20, AI SDK 5→6, rename `User.email`→`User.contact`)
are codemods, not chat conversations. Use AST-aware tools (jscodeshift, ts-morph, libcst, semgrep,
Codemod / Hypermod) to do the deterministic 95%, then let an LLM finish the long-tail (string
templates, tests, docstrings). Open ONE PR per logical group, not one per file. Multi-agent stacks
(Architect → Migration → Validator) generate PR with summary + risk notes.

**Cite:**
- https://docs.codemod.com/changelog (npx codemod ai, MCP for AI assistants)
- https://martinfowler.com/articles/codemods-api-refactoring.html
- https://www.augmentcode.com/learn/automate-multi-file-code-refactoring-with-ai-agents-a-step-by-step-guide
- https://developers.openai.com/cookbook/examples/agents_sdk/sandboxed-code-migration/sandboxed_code_migration_agent
- https://ai-sdk.dev/docs/migration-guides/migration-guide-6-0 (real codemod-driven migration)

**When to use:**
- Framework upgrades, API renames, deprecation removals, lint-rule rollouts.
- Repos with > 100 call-sites of the symbol you're refactoring.

**When NOT to use:**
- Small renames (< 20 sites) — IDE rename is faster and safer.
- Semantic refactors where the type signature stays but behaviour changes (codemods don't see that).

**Tiny example:**
```ts
// codemod: rename User.email → User.contact across the repo
export default function (file, api) {
  const j = api.jscodeshift;
  return j(file.source)
    .find(j.MemberExpression, { property: { name: "email" } })
    .filter(p => p.value.object.type === "Identifier" && p.value.object.name === "user")
    .forEach(p => { p.value.property.name = "contact"; })
    .toSource();
}
// → npx codemod run rename-email && open PR with codemod summary + AI-written PR body
```

---

## mr-09 — Flake-detector → auto-fix PR (Bits AI / Trunk / Datadog Test Optimization)

**Rule:** Wire flaky-test telemetry (retry rate, fail-pass-without-change pattern, time-of-day
correlation) into a fixer agent. Datadog Bits AI Dev Agent is the cleanest 2026 stack: Test
Optimization clusters failures by type → Bits picks high-confidence flake categories (race, timing,
sleep, port-collision) → opens a draft PR with the fix + a quarantine fallback. Slack's pattern
(quarantine first, fix later) and Trunk's "Quarantine without code changes" are the conservative
sibling — quarantine immediately, fix-PR async.

**Cite:**
- https://www.datadoghq.com/blog/bits-ai-test-optimization/
- https://trunk.io/flaky-tests
- https://slack.engineering/handling-flaky-tests-at-scale-auto-detection-suppression/
- https://www.faros.ai/blog/github-copilot-fixes-flaky-test
- https://semaphore.io/can-ai-detect-flaky-tests-or-predict-build-failures-in-ci-cd

**When to use:**
- Repos with > 200 tests where flakes burn CI time and erode trust.
- CI providers that already emit retry/quarantine signals (CircleCI, Buildkite, Datadog CI Visibility).

**When NOT to use:**
- Tests for non-deterministic systems (LLM evals, fuzzers, integration with paid APIs) — these
  aren't "flaky", they're "stochastic by design". Fixer agent will produce wrong patches.

**Tiny example:**
```yaml
# Datadog Test Optimization → Bits trigger
flaky_test_routing:
  - if: { category: ["race", "sleep_timing"], confidence: ">0.8" }
    action: bits_open_pr
    pr_label: "agent:flake-fix"
  - if: { category: ["env", "port_collision"], confidence: "<0.5" }
    action: trunk_quarantine_only       # quarantine + open issue, no PR
```

---

## mr-10 — Rollback / revert agent on alert (one-click `git revert -m 1`)

**Rule:** Pair forward-deploy automation with a revert agent listening on a high-severity alert
channel (PagerDuty SEV-1, error-rate spike, p95 regression). On trigger: agent finds the SHA range
since last good deploy, opens a `revert/<shortsha>` PR with auto-generated body ("Reverting to
restore p95 from 800ms→200ms after 14:32 deploy"), tags `incident:auto-revert`, and pings the
on-call. Branch protection still requires 1 human approval — the human taps Approve, not
investigates root cause. LaunchDarkly's catch-and-revert pattern and Refact's Agent Rollback
formalise this.

**Cite:**
- https://launchdarkly.com/blog/catch-and-revert-ai-failures-in-production/
- https://docs.refact.ai/features/autonomous-agent/rollback/
- https://fast.io/resources/ai-agent-rollback-strategy/
- https://github.com/orgs/community/discussions/140805 (GH Actions auto-revert on later-job fail)
- https://tianpan.co/blog/2026-04-20-ai-agent-data-rollback-production (data rollback caveats)

**When to use:**
- High-traffic prod where MTTR matters more than root cause speed.
- Feature-flag-gated rollouts where the agent can flip the flag AND open the revert PR in parallel.

**When NOT to use:**
- Forward-fix culture / DB migrations (a revert PR may break schema; agent doesn't know).
- Already-flagged rollouts — flip the flag instead, no revert needed.

**Tiny example:**
```yaml
# alert → revert PR
on_alert:
  trigger: { severity: ">=SEV2", source: "datadog:p95_payments" }
  action:
    - git fetch origin main
    - LAST_GOOD=$(gh deploy list --status success --limit 1 --json sha -q '.[0].sha')
    - BAD=$(gh deploy list --limit 1 --json sha -q '.[0].sha')
    - git switch -c revert/$BAD
    - git revert --no-edit $LAST_GOOD..$BAD
    - gh pr create --draft --label incident:auto-revert \
        --title "revert: $BAD restoring p95" \
        --body "Auto-revert: alert $ALERT_URL fired at $TS"
```

---

## mr-11 — Diff-only PR description / walkthrough generator (the cheap baseline)

**Rule:** Even teams that reject AI code-review still benefit from AI PR descriptions. Auto-fill
title + body + walkthrough on PR open from `git diff`, with a structured template (Context, What
changed, Why, Risk, Test plan). Costs ~$0.001/PR with 4o-mini. PR-Agent `/describe`, AI Commit
Summary, AI-Powered PR Description Generator are interchangeable here. Keep the human-edited
section separated by an HTML comment so re-running `/describe` doesn't clobber it.

**Cite:**
- https://github.com/marketplace/actions/pr-summarizing-using-ai
- https://github.com/marketplace/actions/ai-powered-pr-description-generator
- https://github.com/marketplace/actions/pr-auto-describe
- https://qodo-merge-docs.qodo.ai/tools/review/ (`/describe` command, structured walkthrough)
- https://developers.redhat.com/articles/2026/04/21/ai-powered-documentation-updates-code-diff-docs-pr-one-comment

**When to use:**
- Any team where PR descriptions are routinely empty or "fix bug".
- Open-source repos where contributors lack institutional context to describe risk.

**When NOT to use:**
- Repos with strict, hand-curated changelogs where the description is also the release note —
  auto-text dilutes the changelog.

**Tiny example:**
```markdown
<!-- AUTO-DESCRIBE-START — managed by qodo /describe; do not edit -->
## Walkthrough
- payments/views.py: added `Idempotency-Key` header parsing (~+18 lines)
- payments/tests: 2 new tests covering duplicate + missing header
## Risk: low (additive header)
<!-- AUTO-DESCRIBE-END -->

## Notes for reviewer
<!-- HUMAN — survives re-runs of /describe -->
Coordinated with API consumers in #api-team Slack thread.
```

---

## Mapping summary

| ID    | Pattern                              | Tag(s)             |
|-------|--------------------------------------|--------------------|
| mr-01 | Error-tracker → DRAFT PR             | mr-, inc-          |
| mr-02 | Draft + bot identity + human approval| mr-, task-         |
| mr-03 | Slash-command surface                | mr-                |
| mr-04 | Graph-index vs diff-only reviewer    | mr-                |
| mr-05 | `agent-fixable` triage gate          | task-, mr-         |
| mr-06 | Renovate + AI handoff for breaking   | mr-, task-         |
| mr-07 | Spec → PR (issue = prompt)           | task-, mr-         |
| mr-08 | Codemod / refactor agent             | task-, mr-         |
| mr-09 | Flake-detector auto-fix              | mr-, inc-          |
| mr-10 | Rollback / revert agent on alert     | inc-, mr-          |
| mr-11 | Diff-only PR description generator   | mr-                |

## Cross-cutting governance checklist (apply to every mr-* pattern)

1. PR opened **as draft** unless mr-06 patch-bump auto-merge case.
2. Author = dedicated bot identity (GitHub App preferred over PAT).
3. Label mandatory: `agent:<vendor>` (e.g. `agent:seer`, `agent:copilot`, `agent:renovate`).
4. CODEOWNERS-driven required review (≥1 human, never bypass).
5. PR body links back to source signal: alert URL, issue #, codemod ID, flaky-test cluster.
6. Re-runs are idempotent (label `do-not-rerun` to freeze).
7. All actions audit-logged to a security-events stream (Microsoft governance pattern).
