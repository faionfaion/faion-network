# Agent Integration — Quality Gates & Confidence Checks

## When to use
- Before any phase transition in the SDD workflow — confidence check gates progression
- After LLM-generated code is produced — run L1 (syntax/lint) and L2 (unit tests) before human review
- Setting up a CI/CD pipeline for an LLM-assisted project — quality gates are the automated enforcement layer
- When using LLM-as-judge to evaluate AI output before integration into codebase
- When change failure rate spikes — tighten gate enforcement (soft block → hard block)

## When NOT to use
- Trivial configuration changes — running full L1-L6 for a config value change wastes time
- Exploratory prototypes that will be thrown away — gate overhead exceeds learning value
- When gate tooling isn't set up (no linter config, no test suite) — set up tooling first, then enforce gates
- L5/L6 (staging, production) for local development — these are deployment gates, not development gates

## Where it fails / limitations
- Confidence score calculation (Automated_Pass 40% + Coverage 20% + Risk 20% + Traceability 20%) requires accurate measurement of all four factors; agents self-report risk and traceability, inflating scores
- L1 gates (lint/format) are 100% automated but project-specific; without configured ruff/eslint rules, "zero errors" is trivially true
- L4 (code review gate, 50% automated) is the weakest gate — human review can be rubber-stamped under time pressure
- LLM hallucinated APIs pass L1 (syntax valid) but fail at runtime; L1 does not catch import-time or runtime errors
- Multi-agent validation (analyst + coder + tester + security agents) produces overlapping findings without a deduplication step

## Agentic workflow
Quality gates run as a post-generation validation pipeline: the execution agent generates code, then immediately triggers L1 (linting/types) and L2 (unit tests) via subprocess. If L1 fails, the agent re-prompts itself with the lint error output as feedback. If L2 fails, it re-prompts with test failure output. L3-L4 run after L1-L2 pass. An LLM-as-judge step (secondary agent, fresh context) evaluates correctness and completeness before human review (L4). The orchestrator enforces gates as hard blocks for L1/L2 and soft blocks for L3/L4.

### Recommended subagents
- `faion-sdd-execution` skill — drives the L1-L6 gate sequence with retry loops
- `faion-feature-executor` skill — integrates quality gates into task execution
- Secondary Claude agent (fresh context) — LLM-as-judge for L4 correctness evaluation
- Kiro/Codex CLI — additional reviewers for L4 in multi-model validation

### Prompt pattern
```
L1/L2 re-prompt loop:
You generated code that failed quality gates. Fix the issues below.
Do NOT change logic or behavior — only fix the reported errors.
Errors:
[paste lint/type/test output here]
After fixing, the code must pass: [specific command to run].
```

```
LLM-as-judge (L4 confidence check):
You are an evaluator. Input: spec.md (AC-X list), test-plan.md, implementation diff.
Score 0-100 on:
- Correctness: does implementation match all AC? (40%)
- Completeness: all requirements addressed? (20%)
- Security: obvious vulnerabilities? (20%)
- Maintainability: readable, follows patterns? (20%)
Output: score, factor breakdown, list of issues blocking L4 approval.
Confidence threshold for L4: 80% minimum.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Python lint + format (L1) | `pip install ruff`; https://docs.astral.sh/ruff |
| `mypy` | Python type checking (L1) | `pip install mypy` |
| `eslint` | JS/TS lint (L1) | `npm install -g eslint` |
| `pytest` | Python unit/integration tests (L2/L3) | `pip install pytest` |
| `jest` | JS/TS unit tests (L2) | `npm install jest` |
| `k6` | Load/performance testing (L5) | https://k6.io |
| `semgrep` | SAST security scanning (L4) | https://semgrep.dev |
| `bandit` | Python security lint (L4) | `pip install bandit` |
| `snyk` | Dependency vulnerability scan (L4) | https://snyk.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarCloud | SaaS | Yes | L1-L4 code quality + security; CI/CD gates via Quality Gate API |
| GitHub Actions | SaaS | Yes | Orchestrate full L1-L5 pipeline per PR; matrix jobs for parallel gates |
| Snyk | SaaS | Yes | Dependency and code vulnerability scanning; blocks PRs on critical issues |
| Semgrep Cloud | SaaS | Yes | Custom SAST rules; API-driven; team rule sharing |
| Codecov | SaaS | Yes | Coverage reporting; blocks PRs below coverage threshold |
| Confident AI | SaaS | Yes | LLM output evaluation and testing; aligns with LLM-as-judge pattern |

## Templates & scripts
See `templates.md` for the GitHub Actions quality-gates.yml workflow and per-gate checklists.

Automated L1-L2 gate runner (inline):
```bash
#!/usr/bin/env bash
# run-gates-l1-l2.sh
# Run L1 (lint/types) and L2 (unit tests) gates for Python project
set -euo pipefail
echo "=== L1: Syntax & Format ==="
ruff check . || { echo "GATE L1 FAIL: lint errors"; exit 1; }
ruff format --check . || { echo "GATE L1 FAIL: format errors (run: ruff format .)"; exit 1; }
mypy . --ignore-missing-imports || { echo "GATE L1 FAIL: type errors"; exit 1; }
echo "L1 PASS"

echo "=== L2: Unit Tests ==="
pytest --tb=short -q || { echo "GATE L2 FAIL: tests failed"; exit 1; }
COVERAGE=$(pytest --co -q 2>/dev/null | tail -1 | grep -oP '\d+(?=%)' || echo 0)
MIN_COVERAGE=80
if [ "$COVERAGE" -lt "$MIN_COVERAGE" ]; then
  echo "GATE L2 FAIL: coverage $COVERAGE% < $MIN_COVERAGE%"
  exit 1
fi
echo "L2 PASS (coverage: $COVERAGE%)"
echo "=== Gates L1-L2: ALL PASS ==="
```

## Best practices
- Make L1/L2 gates fast (< 5 minutes total) — slow gates kill developer/agent flow; parallelize lint and type checks
- Define gate pass criteria in `constitution.md` at project start, not per-feature — prevents negotiating thresholds under deadline pressure
- Use hard blocks for L1/L2 (no proceed if fail), soft blocks for L3/L4 (require human approval to proceed) — matches gate reliability
- Feed LLM output directly into L1 gate immediately after generation — don't accumulate multiple files before first gate check
- Use the LLM-as-judge pattern for L4 with a different model from the one that generated the code; generation model has blind spots for its own output

## AI-agent gotchas
- Agents treating confidence scores as checkboxes — an agent that self-reports "80% confidence" without running the actual measurements is unreliable; require artifact evidence (test run output, coverage report) for each gate
- L1 passes but runtime errors exist: LLMs hallucinate standard library functions that don't exist; static analysis won't catch usage of `requests.get_json()` vs `requests.get()` if both parse syntactically
- Re-prompt loops for L1/L2 can spiral: if the underlying logic is wrong, fixing syntax errors won't fix failing tests; cap re-prompt attempts at 3 before escalating to human
- Agents skip L3 (integration tests) because they require test DB or external mocks — require test infrastructure setup to be part of Wave 1 tasks, not an afterthought
- The "80% minimum" for L4 is often treated as the target, not the floor; calibrate based on feature risk — payment flows need 95%, internal tooling can accept 80%

## References
- https://addyosmani.com/blog/ai-coding-workflow/ — Addy Osmani, LLM coding workflow 2026
- https://www.sonarsource.com/resources/library/llm-code-generation/ — SonarSource, LLM code generation quality
- https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies — Confident AI, LLM testing methods
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — Anthropic, evals for AI agents
- https://docs.astral.sh/ruff — ruff documentation
