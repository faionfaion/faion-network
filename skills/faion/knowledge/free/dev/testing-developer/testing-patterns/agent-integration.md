# Agent Integration — Testing Patterns

## When to use
- Establishing house style for a fresh codebase: pick AAA vs Given-When-Then, Test Data Builder vs Object Mother, mocking conventions.
- Audit phase: scan an existing test suite for pattern inconsistencies (mixed AAA/GWT, ad-hoc fixtures, no test pyramid).
- Cross-language polyglot project where a uniform pattern vocabulary helps reviewers reason about tests in Python, JS, Go.
- Designing the test pyramid for a new system: deciding ratios of unit / integration / E2E.
- Refactoring brittle E2E suites by introducing the Page Object Model.
- Onboarding new contributors / agents — `testing-patterns/` is the shared reference.

## When NOT to use
- One-off scripts and tiny libraries — patterns add ceremony for diminishing returns.
- Highly framework-specific patterns (e.g., Django's `TestCase` lifecycle) — defer to framework-specific docs over abstract patterns.
- When the codebase has a working convention already; introducing patterns mid-stream produces mixed style and reviewer fatigue.
- Hot-fix work — apply existing pattern; don't rethink it.

## Where it fails / limitations
- README catalogs patterns but lacks decision matrix — agents pick "Builder" everywhere even when "Object Mother" is simpler for the domain.
- Test Pyramid section likely doesn't address Testing Trophy (Kent C. Dodds variant) or Honeycomb (Spotify); agents assume pyramid is the only model.
- Page Object Model examples often show getters that hide assertions — agents replicate, hiding test intent.
- "Property-based testing" mentioned but no guidance on shrinking, seeded reproducibility, or when properties are unsuitable (stateful systems).
- AAA + Given-When-Then mapping shown but agents mix both in a single test file, fragmenting style.
- Test-double taxonomy may overlap with `mocking-strategies/`; agents read just one and pick the wrong vocabulary for the wrong tool.
- No coverage of contract testing patterns (Pact / consumer-driven contracts) which are the modern alternative to fragile E2E.

## Agentic workflow
Use this skill as the **style enforcer**, not as a generator. Workflow: (1) agent reads `testing-patterns/README.md` once at session start; (2) before writing any test, picks one pattern from each axis (structure, data, doubles, isolation) and states the choice in the prompt; (3) writes tests; (4) reviewer subagent diffs against pattern catalog and rejects mismatches. Pair with `testing-pyramid` audit script to keep ratios on target.

### Recommended subagents
- `faion-test-agent` (custom) — generates tests adhering to a declared pattern set.
- `faion-software-architect` — picks layer boundaries (unit vs integration vs E2E) for the codebase, drives pyramid shape.
- Reviewer subagent — scans diffs for AAA structure, fixture reuse, role-based queries (frontend), table-driven (Go), and parametrize (pytest).
- `faion-sdd-execution` — when patterns are baked into the SDD `test-plan.md`.

### Prompt pattern
```
Codebase test conventions:
- Structure: AAA with blank lines between phases.
- Data: Test Data Builder (fluent API) for entities with > 5 fields, plain literals otherwise.
- Doubles: Fakes for repositories, MagicMock(spec=X) for external clients, no mocks of value objects.
- Isolation: function-scope fixtures; no class-level state.
- Naming: test_<behavior>_when_<context>.

Apply these to write tests for <module>.<func>.
```

```
Audit-only: scan tests/ and report violations:
- Tests missing AAA blank-line markers.
- Tests using `unittest.TestCase` style in a pytest codebase.
- Mocks of internal types (anything in our own package).
- Test names that violate <behavior>_when_<context>.
Output: file:line, violation, suggested fix. Do not edit.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Python runner; reference for AAA + parametrize | https://docs.pytest.org |
| `vitest` / `jest` | JS/TS runners | https://vitest.dev / https://jestjs.io |
| `go test` (table-driven) | Go's idiomatic pattern | https://pkg.go.dev/testing |
| `hypothesis` / `fast-check` / `proptest` | Property-based testing across languages | https://hypothesis.readthedocs.io |
| `factory_boy` | Object Mother / factories for Python | https://factoryboy.readthedocs.io |
| `@faker-js/faker` | Test data generation for JS/TS | https://fakerjs.dev |
| `pact` / `pact-broker` | Consumer-driven contract testing | https://docs.pact.io |
| `playwright` | Page Object Model for E2E | https://playwright.dev |
| `mutmut` / `stryker` | Mutation testing — validates pattern adherence | https://mutmut.readthedocs.io |
| `cohesion` / `radon` | Code complexity for tests (over-coupled tests are hard to read) | https://radon.readthedocs.io |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions / GitLab CI | CI | Yes | Required for any pyramid enforcement |
| ReportPortal | OSS / SaaS | Yes — JUnit ingest | Pattern violations as custom attributes |
| Pact Broker | OSS + SaaS | Yes — REST API | Consumer-driven contracts replace brittle E2E |
| Allure | OSS | Yes — adapter per framework | Story/Feature/Test hierarchy aligns with BDD pattern |
| BrowserStack / Sauce Labs | SaaS | Yes — Playwright runners | POM-driven E2E across browsers |
| Stryker Dashboard | SaaS | Yes — JSON upload | Track mutation score over time per pattern |

## Templates & scripts
See `templates.md` for AAA, Builder, POM scaffolds. Inline test pyramid auditor (per-package count by marker):

```python
#!/usr/bin/env python3
# scripts/test-pyramid-audit.py — count tests by marker.
import collections, pathlib, re
counts = collections.Counter()
for path in pathlib.Path("tests").rglob("test_*.py"):
    text = path.read_text()
    for marker in ("unit", "integration", "e2e"):
        # marker added via @pytest.mark.<marker>
        if re.search(rf"@pytest\.mark\.{marker}\b", text):
            # crude: count test_ functions in same file
            counts[marker] += sum(
                1 for line in text.splitlines() if line.strip().startswith("def test_")
            )
total = sum(counts.values()) or 1
for k in ("unit", "integration", "e2e"):
    print(f"{k:>11}: {counts[k]:>4} ({counts[k]/total:.0%})")
target = {"unit": 0.7, "integration": 0.2, "e2e": 0.1}
for k, t in target.items():
    actual = counts[k] / total
    if abs(actual - t) > 0.15:
        print(f"WARN {k}: {actual:.0%} target {t:.0%}")
```

## Best practices
- **Pick one structural pattern per project.** AAA OR Given-When-Then, not both. Mixed style multiplies cognitive load.
- **Prefer fakes over mocks** for repositories and adapters — survives refactors, catches contract drift.
- **POM hides DOM, not assertions.** `page.cart.totalPrice()` returns a number; the test does `expect(...)`. Resist `page.cart.assertTotalIs(N)`.
- **Object Mother for entities used by many tests; Builder for entities customized per test.** Don't pick one for all situations.
- **Keep the test pyramid honest.** 70/20/10 is the heuristic; flag when E2E grows past 20% — flakiness compounds.
- **Property-based tests pair with example-based tests.** PBT finds edge cases; example tests document intent.
- **Test names are documentation.** A reader should be able to deduce behavior from the test name alone.
- **Co-locate tests with source.** Easier to keep in sync; refactors don't drift far from their tests.
- **CI runs unit tests on every PR; integration on merge to main; E2E nightly.** Faster feedback for cheaper layers.
- **Add a per-PR coverage delta check** rather than absolute coverage threshold. Tracks drift, not arbitrary numbers.

## AI-agent gotchas
- Agents apply Builder and Object Mother to trivial value objects, multiplying boilerplate. Set a complexity threshold (e.g., > 5 fields) for Builder.
- POM gets implemented as a thin DOM wrapper; agents move the test logic into the POM, hiding intent. Forbid assertions in POM methods.
- "Test Pyramid" + "Testing Trophy" mixed in same prompt → agents try to do both, ending up with neither.
- Agents replicate the same fixture across files instead of promoting it. Reviewer subagent should flag duplicate fixture bodies.
- Property-based tests without `@settings(max_examples=...)` blow CI budgets — agents miss the cap.
- Page Object getters wrapping `page.locator(...)` without `.first` / `.nth(0)` fail on multi-element pages; agents miss this.
- Naming pattern not agreed → agents fall back to `test_function_returns_value` style; lock it in `pyproject.toml` / ESLint rule.
- Snapshot tests presented as a "structural pattern" — they're a tool, not a pattern; agents adopt them as default and the suite turns into pinned trees.
- "Sandbox" isolation pattern (per-test temp DB) confused with "fresh fixture" — agents use the wrong one, tests share state.
- Human-in-loop checkpoint: review the chosen patterns at PR template stage; agents pick patterns the codebase doesn't use.

## References
- README: `./README.md`
- Sibling: `../unit-testing/`, `../integration-testing/`, `../e2e-testing/`, `../mocking-strategies/`, `../test-fixtures/`
- xUnit Test Patterns (Meszaros): http://xunitpatterns.com
- Test Data Builders — Nat Pryce: http://www.natpryce.com/articles/000714.html
- Page Object Model — Martin Fowler: https://martinfowler.com/bliki/PageObject.html
- Test Pyramid — Martin Fowler: https://martinfowler.com/articles/practical-test-pyramid.html
- Testing Trophy — Kent C. Dodds: https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- Property-Based Testing — John Hughes: https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf
