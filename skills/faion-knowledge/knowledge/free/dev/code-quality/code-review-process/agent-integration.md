# Agent Integration — Code Review Process

## When to use
- Standardizing PR-description quality with an agent that fills the template from commit messages, diff, and linked issue.
- Wiring CI checks (lint, test, coverage, PR-size) so the human + agent reviewer see the same signal before commenting.
- Generating reviewer comment scaffolding for the four canonical scenarios (bug, design, security, performance) — agent recognizes the class and pulls the matched response template.
- Tracking review metrics (time to first review, cycle time, rework rate) and producing weekly health reports.

## When NOT to use
- Replacing the human review verdict — process scaffolding only, not approval.
- Greenfield repos without conventions yet — process implementation amplifies bad habits.
- Tiny teams (1-2 devs) where overhead exceeds value — use lightweight inline review instead.
- Spike/throwaway branches — process is a tax that doesn't pay back.

## Where it fails / limitations
- Agents fill PR descriptions plausibly but inaccurately when commits are noisy ("WIP", "fix", "tweak"). Garbage in, polished garbage out.
- CI workflow YAML drifts; templated workflows in `templates.md` need adapting per repo (caching, secrets, matrix).
- Review metrics from Git/GH alone undercount — pair-review and offline conversations are invisible. Don't optimize what you don't measure.
- Scenario detection (bug vs design vs security) is heuristic; agent miscategorizes ~15-20% of issues. Human re-tags.
- Performance-issue detection (N+1, allocations) needs runtime tracing; static review hits surface only.

## Agentic workflow
Three loops. Pre-PR: a `pr-describer` agent fills the description template from the diff + linked issue. CI: standard checks (lint, test, coverage, PR size). Review: `pr-reviewer` agent writes structured comments tagged by category, mapping issues to the matched scenario template (bug/design/security/perf). Post-merge: a `metrics-collector` cron agent updates weekly review-health dashboards. Human reviewer decides verdict; agent supplies scaffolding and consistency.

### Recommended subagents
- `pr-describer` — template-aware PR description writer; pulls commits, issue body, and changed-file summary. Sonnet.
- `pr-reviewer` — see code-review/agent-integration.md; writes scenario-tagged comments.
- `pr-size-guard` — non-LLM CI step that warns above 500 LOC and blocks above 1500 LOC.
- `metrics-collector` — weekly Bash + jq over `gh api` to compute review metrics; no LLM needed.
- `faion-sdd-executor-agent` — when reviewing SDD-task PRs, validates the change against `spec.md` / `test-plan.md`.

### Prompt pattern
PR describer:
```
You are filling the project PR description template (see attached).
Inputs: linked issue body <issue.md>, full diff <diff.patch>, recent commits <log.txt>.
Output: filled template ONLY (no commentary).
Rules: do not invent test results; if no tests changed, say so. Mark unchecked checkboxes literally.
```

Scenario classifier (inside reviewer):
```
Classify this finding into exactly ONE of: bug | design | security | performance | style.
Then emit a comment using the matched template format from review-scenarios.
Quote the offending lines verbatim. Provide a corrected snippet only when the fix fits in <15 lines.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | PRs, comments, descriptions, metrics via `gh api` | https://cli.github.com |
| `glab` | GitLab equivalent | https://gitlab.com/gitlab-org/cli |
| `pre-commit` | Run linters/formatters before review even starts | https://pre-commit.com |
| `commitlint` | Enforce Conventional Commits → cleaner PR descriptions | https://commitlint.js.org |
| `danger-js` / `danger-ruby` | PR-policy automation (size, missing changelog, etc.) | https://danger.systems |
| `git-pr-stats` / custom `gh api` | Time-to-first-review, cycle time | https://cli.github.com/manual/gh_api |
| `pytest --cov` / `nyc` / `go test -cover` | Coverage gate per CI workflow snippet | per language |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions | SaaS | Yes — agent can read/write artifacts, comment on PR | Reference workflow in templates.md is GitHub-flavored. |
| GitLab CI | SaaS/OSS | Yes — equivalent semantics | Use `glab` instead of `gh`. |
| Buildkite / CircleCI | SaaS | Yes — REST APIs | Wire agent step like any other. |
| Codecov / Coveralls | SaaS | Yes — webhooks + API | Coverage delta on PR. |
| Danger Systems | OSS | Yes — JS/Ruby DSL | Encode PR-policy rules as code. |
| LinearB / Code Climate Velocity | SaaS | Yes | Review metrics dashboards if rolling your own is too much. |
| Conventional Commits + Release Please | OSS | Yes | Tighten commit hygiene → cleaner agent-generated PR descriptions. |

## Templates & scripts
See `templates.md` for full PR template, CI workflow YAML, scenario-comment library, and metrics list. Minimal PR-size guard:

```bash
#!/usr/bin/env bash
# pr-size-guard.sh — fail loud above threshold
set -euo pipefail
BASE="${BASE:-origin/main}"
git fetch -q origin "${BASE#origin/}"
LINES=$(git diff --shortstat "$BASE"...HEAD | awk '{n=$4+$6} END{print n+0}')
WARN=400; FAIL=1500
echo "PR adds/removes $LINES lines"
if [ "$LINES" -ge "$FAIL" ]; then echo "::error::PR too large ($LINES). Split it."; exit 1; fi
if [ "$LINES" -ge "$WARN" ]; then echo "::warning::PR large ($LINES). Consider splitting."; fi
```

## Best practices
- Tie PR template to issue template — fields propagate cleanly into agent prompts.
- Run lint/test BEFORE the agent review step in CI; failed builds shouldn't waste agent tokens.
- Make the four scenario templates from `code-review-process/README.md` first-class prompts the reviewer agent must select from. Forces consistent comment shape.
- Track rework rate (PRs needing >1 review iteration). Spikes signal unclear specs or weak agent precision.
- Cap CI cost: cache deps, run agent only on `opened` + `ready_for_review` + manual rerun — not every push.
- Document a "trust ladder": agent suggestions advisory → blocking only when paired with deterministic check (linter, test, semgrep rule).
- Re-evaluate review metrics monthly; bad metrics drive worse behavior (gaming time-to-first-review with rubber-stamp approvals).

## AI-agent gotchas
- PR descriptions hallucinate test results and screenshots. Strip those sections from the agent prompt unless they're verifiable from CI artifacts.
- Scenario classifier flips based on diff order. Run classifier per finding, not per PR.
- Code suggestions exceed `git apply` patch size; reviewer copies broken multi-file blocks. Constrain code suggestions to single-file, ≤15 lines.
- Metrics agent over-reports: a PR opened-and-closed-as-draft inflates time-to-first-review. Filter draft transitions before computing.
- Privacy in CI: never log full diffs or agent prompts to stdout in public CI. They surface in build logs.
- Workflow drift: copy-pasting CI YAML across repos produces stale references (action versions, secret names). Pin and audit quarterly.
- Auto-comment storms when agent reruns on every push. Use `concurrency: pr-review-${{pr.number}}` with `cancel-in-progress: true`.

## References
- Google Engineering Practices — Code Review Developer Guide
- GitHub Docs — About Pull Requests / Reviews API
- "Modern Code Review: A Case Study at Google" (FSE 2018)
- "Code Review Quality: How Developers See It" (ICSE 2016)
- LinearB — Engineering Benchmarks Reports (review velocity)
