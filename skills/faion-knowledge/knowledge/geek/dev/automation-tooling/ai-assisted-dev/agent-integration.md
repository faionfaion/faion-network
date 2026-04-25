# Agent Integration — AI-Assisted Development

## When to use
- Setting up a new project workflow where Claude Code, Cursor, or Copilot will be primary development tools.
- Deciding which AI tool to assign to which task type (planning vs. implementation vs. inline completion).
- Building a CI step that uses AI for automated test generation or code review commentary.
- Onboarding a developer who has not used AI coding tools before — establishing safe review habits.

## When NOT to use
- Security-critical auth or payment logic where AI-suggested code must never be accepted without line-by-line human review regardless of workflow.
- Compliance-sensitive environments (healthcare, finance) where AI tool output has not been approved by legal/compliance.
- When the team lacks the experience to review AI output critically — premature AI adoption can create hidden defect accumulation.

## Where it fails / limitations
- "Prompt and publish" pattern: accepting AI output without review leads to 4x higher defect rate (per 2025 research cited in README).
- AI test generation produces tests that pass trivially (testing mocks, not behavior). Human must verify test assertions are meaningful.
- Self-healing test tools (Virtuoso, mabl) introduce non-determinism: tests may silently change meaning when UI changes are detected.
- AI tools don't have access to internal architecture context unless explicitly provided via CLAUDE.md / system prompts; vague prompts produce generic code.
- Multi-tool workflows (Claude Code + Cursor + Copilot) create context fragmentation — each tool sees different history.

## Agentic workflow
Use Claude Code as the planning and large-refactor agent (long context, no IDE dependency), Cursor for flow-state implementation in the editor, and Copilot inline for boilerplate. An agentic CI pipeline can use Claude Code's `--print` mode to review PRs, generate test stubs from diff, and post structured review comments. For test generation, a subagent reads source files and generates pytest/jest test suites in a parallel worktree.

### Recommended subagents
- `faion-sdd-executor-agent` — executes structured development tasks with quality gates; wraps AI-generated code in a review step before commit.

### Prompt pattern
```
Context: Django REST API, Python 3.11, pytest. Task: Generate tests for UserService.create_user(). Requirements: cover validation error, duplicate email, successful creation, missing required field. Use pytest fixtures, parametrize where applicable, follow AAA pattern.
```

```
Review the following diff for security issues, missing error handling, and test coverage gaps. Output structured JSON: {"security_issues": [], "missing_error_handling": [], "coverage_gaps": []}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` | Claude Code CLI — agentic tasks, large refactors, file generation | https://docs.anthropic.com/en/docs/claude-code |
| `ruff` | Python linter/formatter; run after AI-generated code to catch style violations | https://docs.astral.sh/ruff |
| `pytest` | Test runner; AI-generated tests need a green run to be accepted | https://docs.pytest.org |
| `jest` / `vitest` | JS test runners for AI-generated test suites | https://vitest.dev |
| `gh` (GitHub CLI) | Post AI review comments to PRs, create issues from AI analysis | https://cli.github.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Copilot | SaaS | Partial (API preview) | IDE extension; Copilot Workspace has agentic features |
| Cursor | SaaS/Electron | No public API | Best for human-in-loop; not automatable by other agents |
| Claude Code | OSS CLI | Yes — native | Full CLI automation, worktree isolation, subagent dispatch |
| Katalon | SaaS | Yes — REST API | AI test generation pipeline; REST-triggerable |
| mabl | SaaS | Yes — REST API | AI-driven e2e test creation; CI-integrated |
| Sourcegraph Cody | SaaS/OSS | Partial | Code search + AI; REST API for enterprise |
| GitHub Actions | SaaS | Yes | Host AI review/generation workflows |

## Templates & scripts
Inline script — AI-assisted test stub generator (call Claude Code in `--print` mode):

```bash
#!/usr/bin/env bash
# gen-tests.sh <source_file>
# Generates pytest test stubs using Claude Code
SOURCE=$1
if [ -z "$SOURCE" ]; then
  echo "Usage: gen-tests.sh <source_file>" && exit 1
fi

OUTFILE="tests/test_$(basename "$SOURCE" .py).py"
echo "Generating tests for $SOURCE → $OUTFILE"

claude --print "Generate pytest tests for the following Python file.
Cover: happy path, validation errors, edge cases, exception handling.
Use pytest fixtures. Follow AAA pattern. Output only the Python code, no explanation.

$(cat "$SOURCE")" > "$OUTFILE"

echo "Review $OUTFILE before committing."
```

## Best practices
- Match tool to task: Claude Code for documentation and refactors (needs long context); Cursor for feature implementation (needs real-time feedback); Copilot for autocomplete (needs inline speed).
- Provide structured context in every AI prompt: tech stack, constraints, expected output format. Vague prompts produce vague code.
- AI-generated tests must be reviewed for meaningful assertions — a test that calls `assert result is not None` proves nothing.
- Establish a team-wide "AI review checklist" so all members apply the same scrutiny to AI output before merging.
- For security-sensitive areas (auth, payment, data access), require a second human reviewer even if AI already reviewed the PR.
- Track defects introduced by AI code vs. human code separately in your bug tracker for 3 months; use the data to calibrate how much review AI outputs need.
- Run `ruff check --fix` and type checkers immediately after AI code generation; AI frequently produces type errors and unused imports.

## AI-agent gotchas
- An agent generating tests that it also runs can certify its own incorrect output as passing. Human must spot-check a random subset of AI tests for logical correctness, not just green CI.
- AI coding tools trained on public data reproduce patterns from outdated library versions. Always pin versions in requirements and verify AI-generated API calls against current docs.
- When Claude Code operates in an automated pipeline (no human in loop), it may accept ambiguous instructions and make architectural decisions. Use `--print` mode and diff review before any automated commit.
- Multi-turn AI sessions accumulate context errors: an early incorrect assumption propagates through subsequent responses. For long coding sessions, reset context and re-state requirements periodically.
- AI-generated code may pass tests but violate security constraints (e.g., logging sensitive fields). Static analysis tools (Semgrep, Bandit) must run in CI regardless of AI involvement.

## References
- https://docs.anthropic.com/en/docs/claude-code — Claude Code documentation
- https://testguild.com/7-innovative-ai-test-automation-tools-future-third-wave/ — AI testing tools landscape
- https://wavespeed.ai/blog/posts/cursor-vs-claude-code-comparison-2026/ — Cursor vs Claude Code comparison
- https://medium.com/@saad.minhas.codes/ai-coding-assistants-in-2026-github-copilot-vs-cursor-vs-claude-which-one-actually-saves-you-4283c117bf6b — AI coding assistants comparison 2026
- https://semgrep.dev — Static analysis for security issues in AI-generated code
