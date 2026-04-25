# Agent Integration — Refactoring Patterns

## When to use
- Preparatory refactoring before a feature lands ("make the change easy, then make the easy change").
- Reducing cyclomatic complexity / function length flagged by linters or code review.
- Eliminating duplication detected by `jscpd`, `pylint duplicate-code`, or similar.
- Modernizing legacy modules: replacing magic constants, decomposing god classes, extracting strategies.
- Pre-test refactoring to make seams for mocks before adding tests.
- Post-merge cleanup pass over a freshly delivered feature.

## When NOT to use
- During the same change as a behavior modification — refactoring requires "tests stay green and behavior unchanged".
- When tests do not exist or do not cover the affected code paths. Add characterization tests first.
- Hot paths where the "messy" form is intentional (manual loop unrolling, allocation reuse).
- Right before a release window — defer to next cycle.
- Generated code, vendored libraries, or migration scripts.

## Where it fails / limitations
- README is Python-centric (`@dataclass`, `Decimal`, `Enum`); pattern names map cleanly to other languages but examples need translation.
- Polymorphism example introduces an ABC + 4 classes for a small discount table — over-application is real risk; agents will Strategy-ify everything.
- "Boy Scout Rule" is invoked but not bounded — agents drift from the task into adjacent rewrites; needs explicit scope.
- No discussion of refactoring at the **module / package** level (move file, split package, dependency inversion across boundary).
- Doesn't cover tooling-driven refactors (codemods, AST transforms) which are safer than free-form edits for agents.

## Agentic workflow
Refactoring with agents is a **strict loop**: characterize → micro-edit → run tests → commit → repeat. Never let the agent batch edits across multiple patterns; one Fowler refactor per commit. Pair an "edit" subagent with a "verify" subagent that runs tests + diff review and rejects the commit if behavior coverage drops or unrelated files were touched. Use `git stash` and `git diff --stat` between steps to keep blast radius visible.

### Recommended subagents
- `faion-sdd-executor-agent` — when refactoring is tracked as SDD task with explicit AC ("complexity below N", "no duplicates").
- `simplify` skill — built-in, scans changed code for reuse/quality issues; ideal post-feature pass.
- General-purpose subagent constrained to a single file with a single named refactor (`extract_method`, `replace_conditional_with_polymorphism`).

### Prompt pattern
```
Refactor target: <file>:<symbol>. Pattern: Extract Method.
Constraint: behavior must be unchanged. Run pytest -k <symbol> after every micro-edit.
Output: one commit per extraction. If tests fail, revert and report.
Do not touch other files. Do not modify tests except to add characterization tests for uncovered branches.
```

```
Audit only: list code smells in <file> (long method, magic numbers, feature envy, primitive obsession).
For each: name the Fowler refactor that would address it. Do NOT edit.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` / `flake8` (`C901`) | Cyclomatic complexity threshold | https://docs.astral.sh/ruff/rules/#mccabe-c90 |
| `radon` | Complexity & maintainability index | https://radon.readthedocs.io/ |
| `vulture` | Dead-code finder | https://github.com/jendrikseipp/vulture |
| `jscpd` | Cross-language copy-paste detector | https://github.com/kucherenko/jscpd |
| `pylint --disable=all --enable=duplicate-code` | Duplication in Python | https://pylint.pycqa.org/ |
| `eslint` (`complexity`, `max-lines-per-function`, `no-magic-numbers`) | JS/TS smells | https://eslint.org/docs/latest/rules/ |
| `ast-grep` | Structural search/replace | https://ast-grep.github.io/ |
| `comby` | Lightweight structural rewrite | https://comby.dev/ |
| `gopls`/`rust-analyzer`/`pyright` | LSP-driven extract/rename | language-specific |
| `codemod` / `jscodeshift` | Mass JS/TS AST transforms | https://github.com/facebook/jscodeshift |
| `git rebase -i` (manual only) | Squash micro-commits before merging | docs.git-scm.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SonarQube / SonarCloud | SaaS+OSS | Yes | Long-term smell tracking; rules align with Fowler catalog. |
| Codacy / CodeClimate | SaaS | Yes | Per-PR maintainability scores. |
| GitHub CodeQL | SaaS | Yes | Custom queries for project-specific smells. |
| Refactoring.guru | SaaS (free reading) | Reference | Visual catalog matching the README. |
| `pre-commit` framework | OSS | Yes | Wire `ruff`, `radon`, `vulture` as gates. |

## Templates & scripts
See `templates.md` for refactor-by-refactor scripts. One useful guard — a pre-commit hook that fails if the diff touches more than N files in a refactor commit:

```bash
#!/usr/bin/env bash
# scripts/refactor-scope-guard.sh — block sprawling "refactor:" commits.
set -euo pipefail
msg=$(git log -1 --format=%s)
[[ "$msg" =~ ^refactor: ]] || exit 0
files=$(git diff --cached --name-only | wc -l)
if (( files > 5 )); then
  echo "refactor commit touches $files files (max 5). Split the change."
  exit 1
fi
# Tests must be present in the staged changes or already passing.
pytest -q --collect-only >/dev/null
```

## Best practices
- One refactor pattern per commit. Commit message names the pattern (`refactor: extract method validate_order`).
- Add characterization tests before touching code you don't fully understand — they are the safety net.
- Use IDE/LSP refactors over hand edits for `rename`, `extract method`, `inline`, `move`. Lower error rate.
- Strangle gradually: introduce the new shape alongside the old, redirect callers, delete the old. Never big-bang rewrite.
- For polymorphism replacement, add the strategy and switch one caller at a time; keep the conditional and the strategy coexisting briefly.
- Track maintainability metrics (`radon mi`, SonarQube debt ratio) before/after to prove improvement, not just "feels cleaner".

## AI-agent gotchas
- Agents over-apply patterns: a 4-branch `if` becomes a 4-class hierarchy. Cap with a rule like "polymorphism only if branches > 5 AND each is non-trivial".
- LLMs may "improve" types (e.g. switch `int` → `Decimal`) — this changes behavior subtly (rounding, comparison). Forbid type changes inside refactor commits.
- Renames often miss external references (string-based reflection, JSON keys, DB column names). Require the agent to grep the whole repo for the old name before claiming done.
- Test pass != behavior preservation if coverage is sparse. Require a coverage delta of zero or positive on the touched files.
- Agents sometimes "refactor" tests, removing meaningful assertions. Forbid edits to assertion contents during a refactor commit.
- Human-in-loop checkpoint: any change to a public API signature (parameter list, return type) must be approved before merge.
- The `Replace Magic Numbers` example introduces `ShippingConfig` constants — agents will create a constants class even when one already exists elsewhere. Require a duplicate-search step.

## References
- https://refactoring.com/
- https://refactoring.com/catalog/
- https://refactoring.guru/refactoring/catalog
- https://www.oreilly.com/library/view/working-effectively-with/0131177052/
- https://martinfowler.com/articles/preparatory-refactoring-example.html
- https://martinfowler.com/bliki/OpportunisticRefactoring.html
