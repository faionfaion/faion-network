# Agent Integration — Extreme Programming (XP)

## When to use
- Solo developer using Claude as the "pair" — TDD, simple design, small releases map cleanly to agentic loops.
- Small team (2-12) co-located or strong-sync, building a product with churning requirements.
- Greenfield product where you can enforce coding standards and CI from day one.
- Codebases that already have high test coverage — XP feedback loops only work when the suite is fast and trusted.

## When NOT to use
- Compliance-heavy domains (medical, aerospace) requiring big upfront design and signed change controls.
- Distributed async-only teams that cannot do real-time pairing or daily sync (use Kanban/async Scrum instead).
- Projects without an accessible customer/PM proxy — the on-site customer practice collapses.
- Maintenance-mode systems where pace is dictated by external SLAs, not iterations.

## Where it fails / limitations
- "AI as pair" hype skips the disagreement function of pairing — humans push back; LLMs default to compliance.
- Collective ownership without strong tests = chaos. Without 80%+ coverage, "anyone changes anything" breaks main daily.
- Sustainable pace gets ignored when the founder is solo and motivated; XP discipline degrades.
- Pair programming over screen-share has measured ~30% lower defect-catch rate than co-located pairing.
- Refactoring without acceptance tests creates regression debt; XP assumes both layers exist.

## Agentic workflow
Treat Claude as the "navigator" while the human is "driver", or vice versa: human writes the failing test (Red), Claude implements (Green), Claude proposes refactor, human approves. Run a test-runner agent on every commit so CI feedback is sub-minute. Use `faion-sdd-executor-agent` to enforce the gate sequence (test → impl → refactor → commit). For solo XP, simulate planning game with a brainstorm agent: feed customer notes, get prioritized story list, estimate in tokens not days.

### Recommended subagents
- `faion-sdd-executor-agent` — gates each task on green tests + lint, enforcing TDD discipline.
- `faion-brainstorm` (skill) — runs the diverge/converge for a planning-game session when no human PM is available.

### Prompt pattern
```
Role: XP navigator. I am the driver.
Step 1: I will paste a failing test. You explain in 2 sentences why it fails.
Step 2: Propose the SIMPLEST code that makes it green (no extra features — YAGNI).
Step 3: After test goes green, suggest ONE refactor that reduces duplication.
Stop after each step and wait. Never write code before I see Step 1's analysis.
```

```
Planning game: here are 12 user stories <paste>.
Estimate each in story points (1,2,3,5,8,13). Split anything > 13.
Output: prioritized table <story | points | risk | dependency>.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest --tb=short -x` | Fast XP test loop, fail fast | bundled |
| `vitest --watch` | JS/TS sub-second TDD loop | `npm i -D vitest` |
| `mutmut` / `stryker` | Mutation testing — XP "test all the things" | `pip install mutmut` / `npm i -D @stryker-mutator/core` |
| `pre-commit` | Coding-standards gate before push | `pip install pre-commit` |
| `gh pr checks --watch` | CI feedback inside terminal | gh CLI |
| `entr` / `watchexec` | Auto-run tests on save (solo pairing loop) | `cargo install watchexec-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tuple | SaaS | No (UI only) | Real-time pairing; not agent-driven. |
| VS Code Live Share | Free | Partial | Human-only; agents can read shared workspace via SSH. |
| GitHub Actions | SaaS | Yes | Required for fast CI feedback loop. |
| Linear | SaaS | Yes — GraphQL API | Story tracking; agents can create/update issues. |
| Trunk.io | SaaS + OSS | Yes — CLI + checks | Enforces coding standards at PR time. |
| Codecov | SaaS | Yes | Track coverage trend; XP requires it doesn't drop. |

## Templates & scripts
See `templates.md` for planning-game and pairing scripts. Auto-run-tests-on-save (solo XP loop):

```bash
# Watch and run tests on every Python file change — sub-second TDD
watchexec -e py -- pytest --tb=short -x -q
```

```bash
# Pre-push hook enforcing XP "never break the build"
cat > .git/hooks/pre-push <<'EOF'
#!/bin/bash
set -e
pytest --tb=short -x
ruff check . && ruff format --check .
EOF
chmod +x .git/hooks/pre-push
```

## Best practices
- Solo XP: write the failing test FIRST in your prompt, don't let the agent invent both test and impl in one shot.
- Cap iterations at 1 week for solo, 2 weeks for teams. Anything longer hides estimation errors.
- "Done" definition stays in the repo (`DONE.md`): tests pass, docs updated, CHANGELOG entry, no TODOs.
- Refactor in the same commit as the green test only when behavior is unchanged; otherwise split commits — agents lose blame.
- Track velocity in completed stories per iteration, not LOC; LLMs inflate LOC.
- When the agent proposes "future-proofing", reject it and cite YAGNI.

## AI-agent gotchas
- LLMs default to over-engineering — explicitly tell them "passes all tests, reveals intention, no duplication, fewest elements" in priority order.
- Pair-programming substitution: if Claude is the only "partner", schedule a weekly human review; agents won't catch architectural drift.
- TDD discipline breaks when an agent edits both test and source in one tool call. Forbid this — test edit must be a separate commit before the impl edit.
- Collective ownership with agents = no ownership. Tag every agent commit with the responsible human in the trailer.
- Sustainable pace doesn't apply to LLM tokens — but burning context on long sessions degrades quality. Reset/compact every 100k tokens.

## References
- Kent Beck, "Extreme Programming Explained: Embrace Change" 2nd ed.
- Ron Jeffries, "The Nature of Software Development" — XP practices in practice.
- http://www.extremeprogramming.org/ — original C2 wiki sources.
- "TDD with AI" — Tim Ottinger 2024 talk on red-green-refactor with copilots.
- Sibling: `tech-debt-management/` for the refactor budget piece XP doesn't cover.
