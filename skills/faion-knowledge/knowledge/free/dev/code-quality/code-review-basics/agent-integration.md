# Agent Integration — Code Review Basics

## When to use
- Pre-review pass on every PR before a human reviewer is assigned: agent surfaces obvious bugs, missing tests, security issues, style nits.
- Self-review automation for diffs produced by Claude itself — catch AI-generated mistakes before pushing.
- Mentoring junior contributors at scale: agent leaves educational comments with explanations.
- Bulk-review of dependabot/renovate PRs where the change is mechanical but breaking-change risk varies.

## When NOT to use
- Architecture/design PRs that need product context the agent doesn't have — humans only.
- Security-sensitive merges where regulatory sign-off is required (e.g., PCI, HIPAA scope changes); agent can advise but cannot approve.
- Trivial single-line fixes already covered by lint+CI; adding an agent comment is noise.
- Repos where rubber-stamping is *already* the failure mode — adding another rubber-stamp signal makes it worse, not better.

## Where it fails / limitations
- Agents don't know intent. They flag style preferences as bugs and miss cross-cutting design issues.
- Hallucinated bugs ("this can NPE" on code that already null-checks) erode trust faster than missed bugs.
- Long PRs (>800 lines) blow context; the agent reviews the first half and approves the rest.
- "Polite" LLM tone makes everything sound like a suggestion → authors ignore the blockers.
- Agents can't run the code; runtime concerns (perf regression, race conditions) are usually missed unless tests fail in CI.

## Agentic workflow
Run review as a CI step on every PR. The pipeline: (1) lint/type/tests must pass first — no agent review on red CI; (2) reviewer subagent reads the diff plus the touched files (not the whole repo), grouped by file; (3) it emits **Conventional Comments** (`blocking:`, `suggestion:`, `nit:`, `question:`, `praise:`) with line anchors; (4) `blocking` items become required-changes via the GitHub API; suggestions and nits are inline comments; (5) human reviewer is auto-requested only after the agent pass.

### Recommended subagents
- `review` skill (built-in) — reviews PR; pair with `security-review` for sec-sensitive PRs.
- `faion-sdd-executor-agent` — when the PR comes from an SDD task, it already knows the spec and can verify acceptance criteria.
- Reviewer subagent (Sonnet) — line-level comments per file.
- Security-review subagent (Opus) — only triggered on diffs touching auth, crypto, IO boundaries, secrets.

### Prompt pattern
```
Review the diff at <PR URL>. Constraints:
- Only comment on changed lines (+ ±3 lines context).
- Use Conventional Comments labels (blocking/suggestion/nit/question/praise).
- Skip style nits already enforced by the linter config in .eslintrc / pyproject.toml.
- Output JSON list: [{"path","line","label","body"}].
- Max 20 comments; prioritise correctness > security > maintainability > nits.
```
```
Self-review the patch you just produced before requesting human review.
For each hunk, answer: bug? edge case? test coverage? security? perf?
If unsure, mark `question:` and ask the human, do not silently ship.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh pr diff` / `gh pr view` | Pull diff + metadata for the agent | https://cli.github.com |
| `glab mr diff` | Same for GitLab | https://gitlab.com/gitlab-org/cli |
| `git diff --merge-base origin/main` | Local pre-push self-review surface | git docs |
| `reviewdog` | Posts agent/linter findings as PR review comments | https://github.com/reviewdog/reviewdog |
| `danger` / `danger-js` | Custom PR rules (CHANGELOG, PR size, missing tests) | https://danger.systems |
| `pr-agent` (CodiumAI) | Open-source LLM PR reviewer; useful as reference impl | https://github.com/Codium-ai/pr-agent |
| `pre-commit` | Block bad diffs before they reach review | https://pre-commit.com |
| `semgrep` | Rule-driven static analysis; agent can author rules | https://semgrep.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Copilot Code Review | SaaS | Yes | Native LLM PR review; complements custom agents |
| CodiumAI PR-Agent | OSS + SaaS | Yes (CLI + GitHub App) | Drop-in LLM reviewer; can be self-hosted |
| Graphite | SaaS | Yes (CLI + API) | Stacked-PR workflow ideal for small reviewable diffs |
| Reviewable | SaaS | Partial | Rich review UX; API for posting agent comments |
| Sourcery | SaaS | Yes (GitHub App) | Suggests refactors inline |
| GitHub / GitLab REST API | SaaS | Yes | Authoritative way to post review comments + required-changes |
| `gerrit` | OSS | Yes (REST API) | Common in regulated/large orgs |
| Conventional Comments | spec | Yes | Standard label set the agent should always emit |

## Templates & scripts
The methodology already ships review checklists and Conventional-Comment examples in `templates.md`. Useful agent companion: a script that pulls the diff and primes the prompt.

```bash
#!/usr/bin/env bash
# pr-context.sh — emit review-ready context for an agent.
# Usage: pr-context.sh <owner/repo> <pr-number>
set -euo pipefail
REPO="$1"; PR="$2"

echo "## PR metadata"
gh pr view "$PR" --repo "$REPO" --json title,body,author,additions,deletions,changedFiles \
  | jq

echo
echo "## Files changed"
gh pr diff "$PR" --repo "$REPO" --name-only

echo
echo "## Failing CI checks (agent must skip review if any)"
gh pr checks "$PR" --repo "$REPO" --json name,state,conclusion \
  | jq '[.[] | select(.conclusion=="failure" or .state=="FAILURE")]'

echo
echo "## Diff (truncated to 1500 lines)"
gh pr diff "$PR" --repo "$REPO" | head -1500
```

## Best practices
- **Cap PR size at 400 changed lines** before the agent reviews — beyond that, ask the author to split. Track the cap with `danger`.
- Always run linters/tests first; never let the agent comment on code that the linter would flag — duplicates noise.
- Use Conventional Comments labels in every agent comment so authors can filter by severity.
- Require evidence: the agent must quote the offending lines and cite the rule/principle. No "this seems wrong".
- Combine LLM review with `semgrep` rules for known anti-patterns; semgrep handles deterministic checks, LLM handles judgement calls.
- Track agent precision/recall: sample 20 reviews/week, mark each comment as true-positive / false-positive. Below 70% precision → tighten prompt or shrink scope.
- The agent's `praise:` comments are not filler — they teach style and reduce author defensiveness.

## AI-agent gotchas
- **Hallucinated bugs.** LLMs invent NPEs/race conditions in code that's safe. Mitigation: require the agent to cite the exact line and explain the trigger; reject `blocking:` comments without a concrete failing input.
- **Approval drift.** Agent learns "approve" is the default response. Audit approval rate; if > 90% on real PRs, the prompt is too lenient.
- **Context truncation.** Big PRs → silent truncation → review of file 1, rubber-stamp on file 12. Force the agent to enumerate files reviewed and to refuse if it had to skip.
- **Conflicting personas.** Don't run two LLM reviewers with different prompt styles — authors get whiplash. Pick one.
- **Self-review bias.** When Claude reviews a Claude-authored diff, it tends to agree with itself. Always run the human review pass after.
- **Human-in-loop checkpoint.** Agent can never be the *sole* approver on a merge to `main`. Configure branch protection to require a human reviewer regardless of bot approval.
- **Secret leakage.** Don't pass full repo context to a third-party SaaS reviewer; use self-hosted Claude or scrub secrets first.

## References
- https://google.github.io/eng-practices/review/ — Google code-review guide
- https://conventionalcomments.org/ — comment label standard
- https://docs.github.com/en/rest/pulls/reviews — GitHub Reviews API
- https://github.com/Codium-ai/pr-agent — open-source LLM PR reviewer to learn from
- https://martinfowler.com/articles/preparing-codebase-for-ai.html
- https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/ — empirical limits (≤400 LoC, ≤60 min)
