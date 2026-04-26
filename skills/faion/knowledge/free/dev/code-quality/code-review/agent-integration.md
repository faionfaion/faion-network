# Agent Integration — Code Review

## When to use
- Pre-merge review of every PR — agent does first pass, human reviewer does second.
- Large refactors where reviewers don't have bandwidth for line-by-line scan; agent flags hotspots.
- Onboarding a new repo: agent reviews recent commits to learn conventions, surface inconsistencies.
- Security-sensitive change classes (auth, data access, file uploads, deserialization) — agent runs targeted checklists.
- Consistency enforcement: PR style, naming, test coverage thresholds.

## When NOT to use
- Non-code review (design docs, RFCs, copy edits) — wrong tool, use a doc-review agent.
- High-trust hotfixes during incidents where speed > review depth — agent latency hurts here.
- Closed-source third-party SDK reviews where source can't be uploaded — agent has nothing to read.
- Subjective architecture debates ("DDD vs CRUD here?") — agent will pick a side without team context.
- One-line dependency bumps — automation (Renovate/Dependabot + tests) is enough.

## Where it fails / limitations
- Agents drift toward style nits and miss design issues. The signal-to-noise ratio drops fast.
- Cross-file reasoning is shallow without a proper code graph or repomap; agents miss "X is now incompatible with Y" issues.
- Hallucinated APIs: agent suggests a function that doesn't exist on the version pinned in the repo.
- False-positive security warnings (CSRF on internal services, SQL-i on parameterized queries) erode reviewer trust.
- Cannot verify behavior without running tests; agent "approves" green-looking code that breaks integration tests.
- Token budget: PRs >2k LOC overflow — agent silently truncates and reviews only the head of the diff.

## Agentic workflow
Bind a `pr-reviewer` agent to a CI workflow that fires on PR open/sync. The agent reads the PR description, the diff, and the touched files in full (not just diff context). It produces a comment block: blocking issues, suggestions, nitpicks, questions, praise — using the comment-type taxonomy from the README. A second pass: `security-reviewer` agent runs only on changes touching auth/data/IO code paths, scoped via path filters. Human reviewer reads agent output as a checklist, not a verdict. Block auto-merge until at least one human approval; agent comments are advisory.

### Recommended subagents
- `pr-reviewer` — generic correctness/design/maintainability pass; sonnet-class.
- `security-reviewer` — auth, input validation, secret scanning, OWASP-class checks; opus-class on sensitive paths only.
- `test-coverage-reviewer` — checks new code has tests, calls out untested branches.
- `style-reviewer` — naming, structure, project conventions; haiku-class to keep cost low.
- `faion-sdd-executor-agent` — when reviewing within an SDD task, ensures change matches spec/design/test-plan.
- `password-scrubber-agent` — pre-review pass to redact secrets before sending diff to any external LLM.

### Prompt pattern
```
You are reviewing a PR. Use these comment types: BLOCKING, SUGGESTION, NITPICK, QUESTION, PRAISE.
For each finding: file:line, type, body, optional code suggestion.
Categories to cover: correctness, design, maintainability, testing, performance, security.
Hard rules:
- Quote the exact lines you reference.
- If unsure, ask a QUESTION; do not BLOCK on speculation.
- Cap NITPICK count at 5.
- End with one-line PRAISE if anything was well done.
Diff: <<<UNIFIED DIFF>>>
Repo conventions: <<<excerpt of CONTRIBUTING.md / .editorconfig / lint config>>>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh pr diff <num>` | Pull diff for agent input | `gh` CLI |
| `gh pr review --comment -F file` | Post agent's comments back to PR | gh CLI |
| `git diff --stat origin/main...HEAD` | PR size guard | git |
| `ruff` / `eslint` / `prettier` / `black` | Pre-agent lint pass — agent reviews code, not formatting | per language |
| `semgrep` | Rule-based static analysis as non-LLM safety net | `pip install semgrep` |
| `gitleaks` | Pre-flight secret scan before sending diff to LLM | `brew install gitleaks` |
| `trufflehog` | Deep secret detection across history | `pip install trufflehog3` |
| `claude` (Claude Code CLI) | `claude -p` headless review in CI | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub PRs / Reviews API | SaaS | Yes — full REST/GraphQL | Standard sink for agent comments. |
| GitLab MRs | SaaS/OSS | Yes — REST API | Equivalent agent integration. |
| Gerrit | OSS | Yes — REST + SSH | For change-based review workflows. |
| CodeRabbit | SaaS | Native AI reviewer | OOTB; check it doesn't conflict with your custom agent. |
| Greptile | SaaS | Native AI reviewer | Codebase-aware; complement to per-PR LLM. |
| Reviewable | SaaS | Yes — webhooks | Granular line-level state machine. |
| Sourcegraph Cody | SaaS | Yes | Cross-repo context for monorepos. |
| Semgrep AppSec | SaaS/OSS | Yes — CLI + cloud | Run alongside agent for rule-based catches. |

## Templates & scripts
See `code-review-process/templates.md` for PR description, CI checks, and review scenarios. Minimal CI integration:

```yaml
# .github/workflows/agent-review.yml
name: agent-review
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Pre-flight secret scan
        run: |
          curl -sSL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_x64.tar.gz | tar xz
          ./gitleaks detect --no-git --redact -v
      - name: Run agent review
        env: { ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }} }
        run: |
          gh pr diff ${{ github.event.pull_request.number }} > diff.patch
          claude -p "Review this PR per project rules in CONTRIBUTING.md. \
            Use BLOCKING/SUGGESTION/NITPICK/QUESTION/PRAISE. Output GitHub-flavored markdown." \
            < diff.patch > review.md
          gh pr comment ${{ github.event.pull_request.number }} -F review.md
```

## Best practices
- Keep PRs <400 lines; agent quality drops sharply above that. Enforce with a CI warning.
- Feed the agent the project's `CONTRIBUTING.md`, lint config, and CODEOWNERS — without conventions context, output is generic.
- Run linter/formatter before agent. Style nits from a mixed-formatter codebase poison the agent's review.
- Always run a non-LLM pass too (Semgrep, gitleaks, language linter). Agents miss what rules catch deterministically.
- Cap nitpick count via prompt; otherwise reviews are 80% noise.
- Track agent precision: % of BLOCKING comments humans agreed with. <60% means tighten the prompt or change tier (haiku→sonnet→opus).
- Never let agent auto-merge. Comments are advisory; human approval is required.
- For monorepos, scope by changed paths. Don't load the whole repo every PR.

## AI-agent gotchas
- Hallucinated functions: agent "fixes" by calling APIs that don't exist on the pinned version. Mitigate by including `package.json` / `requirements.txt` excerpt in prompt.
- Diff truncation: long PRs silently lose tail context. Either chunk by file or fail loudly above token budget.
- Phantom security issues: agent sees a SQL-looking string in a logger and yells injection. Use Semgrep as ground truth before the agent.
- Loop on auto-fix: agent suggests change → CI re-runs agent → agent suggests another change. Pin agent output to PR-open + manual rerun, not every commit.
- Style drift across reviews: agents have no memory of prior agreed-on conventions. Persist a `repo-conventions.md` and inject into every prompt.
- Secret leakage: never send a diff to a third-party LLM without gitleaks/trufflehog pre-flight + redaction. Use `password-scrubber-agent` first.
- Tone: agents default to verbose, hedging language. Add "be direct, terse, no filler" to prompt or comments will be ignored.
- Praise inflation: forced PRAISE block trains reviewers to skim. Make it optional but not mandatory.

## References
- Google Engineering Practices — Code Review Developer Guide (https://google.github.io/eng-practices/review/)
- Microsoft Research — Modern Code Review at Microsoft
- "What to Look for in a Code Review" — Trisha Gee, JetBrains
- Anthropic — Claude Code in CI Patterns
- OWASP — Code Review Guide v2.0
