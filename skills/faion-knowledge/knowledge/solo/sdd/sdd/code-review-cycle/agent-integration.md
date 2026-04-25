# Agent Integration — Code Review Cycle

## When to use
- After any SDD task execution, before marking the task `done/` — run AI pre-screening + human spot-check
- When PRs are consistently > 300 lines — AI pre-review cleans up style issues before human review
- Setting up a multi-model review pipeline (Claude writes, GPT or Kiro reviews) for higher coverage
- Integrating SDD reflexion: post-review findings feed into `patterns.md` and `mistakes.md`
- After detecting a spike in change failure rates — add AI review as a quality gate in CI/CD

## When NOT to use
- Single-file configuration changes — linter is sufficient
- Trivial one-line bug fixes — peer review + merge is faster
- First pass in a new codebase where patterns aren't established — establish patterns first, then review against them
- When the human reviewer has deep domain knowledge and AI review is likely to produce false positives that erode trust

## Where it fails / limitations
- AI reviewers (CodeRabbit, Copilot Review) miss business logic errors — they pattern-match but don't understand domain intent
- Change failure rates increase 30% when AI output exceeds human verification capacity — AI review without human review is worse than no AI review
- AI security scanning flags patterns but misses context-dependent vulnerabilities (e.g., an SQL query that's safe because of upstream validation)
- False positives from AI review erode team trust over time; track false positive rate and tune rules
- Multi-model review produces overlapping findings; without deduplication and merge, reviewers spend time triaging AI noise rather than reading code

## Agentic workflow
The review cycle runs as a 3-step agentic pipeline after task execution: (1) AI pre-screen agent reads the diff and flags style, anti-patterns, and missing tests; (2) parallel review agents (Claude fresh-context + Kiro or Codex if available) each produce structured finding lists; (3) a merge agent deduplicates findings, classifies by severity (BLOCK / WARN / NOTE), and produces a unified review report. The executor agent then addresses BLOCK findings and optionally WARN findings, then re-runs L1-L6 quality gates. This mirrors the SDD Phase 5 review flow.

### Recommended subagents
- Fresh-context Claude subagent — primary reviewer; reads spec + design + test-plan + code diff with no implementation bias
- `faion-sdd-execution` skill — drives the full review → fix → test cycle with quality gates
- Codex CLI (if installed) — cross-model secondary reviewer for checks-and-balances
- Kiro CLI (if installed) — spec-implementation alignment check during review

### Prompt pattern
```
You are an independent code reviewer. You did NOT write this code.
Context: spec.md, design.md, test-plan.md (attached). Diff: [git diff output].
Review for:
1. Correctness: does the implementation match all FR-X and AC-X?
2. Security: input validation, auth checks, injection risks
3. Test coverage: are error paths tested, not just happy paths?
4. Patterns: consistent with existing codebase conventions?
Output: structured list with severity BLOCK | WARN | NOTE for each finding.
Do not approve without checking every AC explicitly.
```

```
Merge these review findings from [N] reviewers. Deduplicate.
Keep unique findings from each reviewer. Classify final severity.
Output unified review report in markdown table: finding | severity | reviewer | file:line.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `codex` (OpenAI CLI) | Cross-model review in review pipeline | https://github.com/openai/codex |
| `kiro` | Spec-implementation validation during review | https://kiro.dev |
| `semgrep` | Security pattern scanning (SAST) | https://semgrep.dev |
| `gh` (GitHub CLI) | Create/manage PRs for review; post review comments via API | https://cli.github.com |
| `bandit` | Python security linter | `pip install bandit` |
| `eslint` | JS/TS lint for style and anti-patterns | `npm install -g eslint` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| CodeRabbit | SaaS | Yes | Structured PR review with 40+ linters; GitHub/GitLab webhooks; API available |
| GitHub Copilot Review | SaaS | Yes | Native GitHub inline comments; zero setup |
| Qodo (Codium) | SaaS | Yes | Context-aware review + test generation; VS Code + GitHub integration |
| SonarCloud | SaaS | Yes | Code quality metrics + security scanning; CI/CD gates |
| Sourcery | SaaS | Yes | Python-focused refactoring suggestions; GitHub integration |
| Snyk | SaaS | Yes | Dependency vulnerability scanning; CLI + CI/CD |

## Templates & scripts
See `templates.md` for PR description template, conventional comment format, and review report template.

AI pre-screen script (inline):
```bash
#!/usr/bin/env bash
# ai-prereview.sh <base_branch>
# Runs AI pre-screening review before creating PR
set -euo pipefail
BASE=${1:-main}
DIFF=$(git diff "$BASE"...HEAD)
if [ -z "$DIFF" ]; then
  echo "No changes to review"
  exit 0
fi
echo "=== AI Pre-Screen Review ==="
echo "$DIFF" | claude --print "You are a code reviewer. Review this diff for:
1. Style guide compliance (project uses ruff for Python, eslint for JS)
2. Common anti-patterns (N+1 queries, missing error handling, exposed secrets)
3. Missing tests for changed logic
4. Documentation gaps
Output: list of issues with BLOCK | WARN | NOTE severity."
```

## Best practices
- Run AI pre-screen locally before pushing — cleaner diffs for human reviewers reduce review fatigue
- Use generation model + separate review model: the model that wrote the code is blind to its own assumptions; a different model catches different failure modes
- Configure AI reviewers with team-specific rules (custom ruff/eslint config, project conventions) — generic AI review produces generic feedback
- Track false positive rate quarterly; if > 20%, tune rules — uncalibrated AI review trains teams to ignore findings
- Integrate reflexion: post-review patterns feed directly into `patterns.md`; recurring issues become ruff/eslint rules

## AI-agent gotchas
- An AI reviewer that generated the code will approve its own work — always use a fresh-context agent with no knowledge of the implementation session
- AI reviewers produce BLOCK findings for stylistic preferences; without clear BLOCK vs WARN classification, teams treat all AI findings as optional
- The 30% change failure rate increase from unverified AI output is real; AI review is a forcing function for human verification, not a replacement
- Parallel review agents produce overlapping findings; without a merge step, the executor agent may fix the same issue multiple times or miss unique findings
- Post-merge reflexion is the most skipped step; require it explicitly in the task definition — "review cycle is not complete until patterns.md is updated"

## References
- https://google.github.io/eng-practices/review/ — Google Engineering Practices, code review
- https://conventionalcomments.org/ — Conventional Comments format
- https://docs.coderabbit.ai/ — CodeRabbit documentation
- https://arxiv.org/html/2505.20206v1 — Evaluating LLMs for Code Review (2025)
- https://addyo.substack.com/p/code-review-in-the-age-of-ai — Addy Osmani, code review in the age of AI
- https://docs.github.com/en/copilot/using-github-copilot/code-review — GitHub Copilot code review
