# Agent Integration — Extreme Programming (XP)

## When to use
- Small teams (2-12) with rapidly changing requirements and direct customer access.
- Greenfield projects where you can establish TDD, CI, pair programming as ground rules from day one.
- Recovering a brownfield codebase where quality has rotted — XP's TDD + refactoring + collective ownership is a culture reset.
- Solo + AI dev: most XP practices map cleanly onto a human-in-loop with Claude as the pair.
- Teams adopting agile but failing on engineering excellence (Scrum-without-XP common failure).

## When NOT to use
- Compliance-heavy / regulated work where every change needs upfront sign-off (medtech, aerospace) — XP's "embrace change" clashes.
- Distributed teams with poor async culture and no shared timezone — pair programming and on-site customer fall apart.
- Outsourced "throw spec over the wall" arrangements where the customer is unreachable.
- Hardware / firmware where the cycle time of "test → refactor" is dominated by hardware-in-loop, not code.
- Research / exploratory ML where most code is thrown away — TDD overhead exceeds value.

## Where it fails / limitations
- Pair programming productivity claims are noisy in research; in practice, half-day pairing + half-day solo beats all-day pairing for most teams.
- TDD on UI / visual code is awkward; visual regression tests + storybook fit better than pure red-green-refactor.
- Collective ownership without strong CI + tests + standards is a license to make things worse, faster.
- "On-site customer" is rarely real; PMs and proxies make decisions, not real users.
- Sustainable pace gets crushed at startups; XP without management buy-in is window-dressing.
- "Simple design" + YAGNI breaks down at architectural seams; some upfront design (ADRs, C4) is necessary.
- Story-point estimation drifts; teams either game it or stop using it after 2-3 sprints.

## Agentic workflow
Use Claude as the pair partner. A planner subagent breaks a story into a TDD task list (red tests, green code, refactor steps). An implementer subagent writes the failing test, then the minimum code to pass, then the refactor — three commits. A reviewer subagent enforces simplicity rules (no unused flexibility, DRY, smallest set of classes). A retrospective subagent reads the last N PRs and surfaces recurring smells (large diffs, skipped tests, no refactor commits).

### Recommended subagents
- `faion-sdd-executor-agent` — drives the TDD red→green→refactor loop with quality gates.
- A user-defined `tdd-pair` (model: sonnet) — converts a story into a list of failing tests; never writes production code first.
- A user-defined `simplicity-reviewer` (model: sonnet) — flags speculative generality, premature interfaces, and dead branches.
- A user-defined `retro-analyst` (model: opus) — pulls last 2 weeks of git history + CI runs, returns themes for the iteration retro.

### Prompt pattern
- "Story: `<X>`. Read `xp-extreme-programming/README.md`. Break into a TDD plan: list failing tests in order. Do not write production code. Output as a numbered list with file paths and assertions."
- "Apply Kent Beck's four rules of simple design (passes tests / reveals intent / no duplication / fewest elements) to `<file>`. List violations with line numbers and a concrete refactor for each. Don't change behavior."
- "Iteration retro: read commits since `<date>`, group by theme. Surface 3 things to keep, 3 to change. No fluff."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pre-commit` | Enforce coding standards on every commit (XP "Coding Standards" practice) | `pip install pre-commit` |
| `pytest` / `vitest` / `jest` / `cargo test` / `go test` | TDD red-green loop | per language |
| `mutmut` / `cosmic-ray` (Py), `stryker` (JS/TS) | Mutation testing — proves tests actually test | `pip install mutmut`, `npm i -D @stryker-mutator/core` |
| `coverage.py` / `c8` / `nyc` | Coverage gate (≥ project bar, e.g. 80%) | per language |
| `git rebase -i` (informational) | Encourages small, focused commits | bundled |
| `commitlint` | Enforce commit message style (consistency = standards) | `npm i -D @commitlint/cli` |
| `tcr` (test && commit \|\| revert) | Kent Beck's discipline-enforcer; punishes failed tests | https://github.com/murex/TCR |
| `Tuple` / `VS Code Live Share` / `Pop` | Pair-programming over the network | https://tuple.app, etc. |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions / GitLab CI | SaaS / OSS | Yes | The "Continuous Integration" practice substrate. |
| Linear / Jira / Notion | SaaS | Partial | Story tracking; Linear cleanest for XP cadence. |
| Miro / FigJam | SaaS | Limited | Planning-game whiteboards for remote teams. |
| Tuple / Pop / VS Code Live Share | SaaS / built-in | Limited | Real-time pairing UI; agents can't drive these. |
| Mob.sh | OSS | Yes | CLI-driven mob/pair handover; agents can run it. |
| Stryker Dashboard | SaaS | Yes | Mutation score history. |

## Templates & scripts
See `templates.md`. A pre-commit config that enforces XP-style discipline (tests must pass, lint clean, no print/debug) — drop into any new repo:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix, --select, "E,F,I,B,UP,T20,SIM"]
      - id: ruff-format
  - repo: local
    hooks:
      - id: pytest-fast
        name: pytest (fast suite, must pass)
        entry: pytest -q --maxfail=1 -m "not slow"
        language: system
        pass_filenames: false
        types: [python]
      - id: no-skip-or-xfail
        name: no test skips/xfails sneaking in
        entry: bash -c '! grep -RnE "@pytest\\.mark\\.(skip|xfail)" tests/'
        language: system
        pass_filenames: false
```

## Best practices
- Run the **fast** test suite on every save; full suite on every push; mutation tests nightly.
- Keep commits small enough that `git rebase -i` is mechanical; the XP rhythm is "test passes → commit".
- Pair sessions of 60-90 min with explicit "driver" rotation; longer sessions burn out, shorter waste warm-up.
- Pair on **risky** code (auth, payments, schema migrations); solo or AI-pair on boring CRUD.
- "Ten-minute rule": if your test suite takes >10 min, split into fast/slow and run fast on every push.
- Make the build's red status visible (Slack #ci-status, dashboard); fix-forward or revert within 10 minutes.
- Track velocity in a simple spreadsheet, not a tool — the moment teams "estimate to hit the velocity", the metric is dead.
- Refactor in a **separate** commit from feature changes — reviewers can read either lens cleanly.
- For solo + AI: Claude as pair is great for drivers' "what's the next test" prompt, but bad as the navigator (it doesn't push back enough). Have a human review every refactor commit.
- Keep a "do not pair on" list (admin tasks, exploratory spikes) so pairing doesn't become a tax.

## AI-agent gotchas
- LLMs love to write production code first and tests second — invert with explicit "tests first, no implementation in this turn".
- LLMs over-test trivial getters; ask for **behavior** tests, not coverage tests.
- Refactor steps from agents often change behavior subtly (off-by-one, error-type swap). Always run full test suite between micro-refactors.
- Agents skip the "fewest elements" rule and add interfaces / strategies / factories preemptively. Reject any abstraction without 2+ concrete implementations.
- "Pair with AI" can degenerate into LLM-driven coding without review; institutionalize a human gate per PR.
- Agents can't enforce sustainable pace — but they can flag patterns: same human committing past 22:00 daily, weekend pushes, increasing test-skips. A retro subagent can surface this.
- TCR (test-commit-revert) discipline is hostile to LLMs: they revert often. Use TCR mode only when you trust the test suite stability.
- Human-in-loop checkpoint: never let an agent unilaterally change the coding standards file or the CI test thresholds; those are team-level decisions.
- Mob/pair handover scripts: when using `mob` CLI with agent committers, ensure the agent identity is distinct from human committers (separate git author) so retros can analyze contribution sources.

## References
- Kent Beck, "Extreme Programming Explained" (2nd ed.) — https://www.amazon.com/Extreme-Programming-Explained-Embrace-Change/dp/0321278658
- extremeprogramming.org — http://www.extremeprogramming.org/
- C2 wiki — https://wiki.c2.com/?ExtremeProgramming
- Beck, Test-Driven Development by Example — https://www.oreilly.com/library/view/test-driven-development/0321146530/
- Mob.sh — https://mob.sh
- Stryker (JS/TS mutation) — https://stryker-mutator.io
- TCR origin (Kent Beck) — https://medium.com/@kentbeck_7670/test-commit-revert-870bbd756864
