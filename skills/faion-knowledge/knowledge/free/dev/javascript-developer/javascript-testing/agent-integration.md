# Agent Integration — JavaScript Testing (Vitest / Jest)

## When to use
- Bootstrapping a test suite for a new TS/React/Node project (Vitest preferred, Jest acceptable).
- Adding tests around a refactor — agent writes characterization tests first, then refactors under green.
- Building a component test harness with React Testing Library + userEvent + jsdom.
- Mocking modules, network (MSW), timers, or filesystem during tests.
- CI gate authoring: `vitest run --coverage` with thresholds and JUnit output.

## When NOT to use
- E2E flows that require a real browser and full backend — use Playwright/Cypress methodologies instead.
- Performance benchmarking — use `vitest bench`/`mitata`/`tinybench` patterns, not unit-test files.
- Visual regression — Storybook + Chromatic / Loki, not RTL.
- Type-level tests for libraries — use `tsd`/`expect-type`, not Vitest assertions.

## Where it fails / limitations
- README's `vi.mock` examples for ESM are correct but fragile under Vitest's deep-import behavior; some packages need `vi.hoisted` or `__esModule` shims.
- Mocking timers around real promises (`vi.useFakeTimers` + `await fetch`) frequently misbehaves; agents must reach for `await vi.advanceTimersByTimeAsync`.
- `jsdom` does not implement everything (`IntersectionObserver`, `ResizeObserver`, `matchMedia`); agents need explicit polyfills in setup.
- Coverage thresholds tempt agents into writing tests for uncovered branches that are inherently dead — coverage must be paired with mutation testing (Stryker) for trustworthy signal.

## Agentic workflow
Author-test-first when refactoring: a planner subagent reads the target module, lists behaviors (input → output, side effects, error cases), and emits a test plan as a table. An implementer subagent writes one `describe` per behavior class with named `it(...)` cases. A reviewer subagent checks for: arrange/act/assert separation, no `expect.anything()` blanket asserts, no leaked timers/spies, proper `cleanup` between tests. Run coverage gate as the final step, not the first.

### Recommended subagents
- `faion-feature-executor` — sequential test additions per behavior; gate is `vitest run` green plus coverage delta.
- `faion-sdd-execution` — pattern memory of canonical test idioms (MSW handler shapes, fake-timer dance, RTL queries).
- `faion-improver` — periodic audit: flaky tests (re-runs fail), missing cleanup, `it.only`/`describe.only` left in.

### Prompt pattern
```
Produce a test plan for <module>: list behaviors as `name | input | expected
output | side effects | error cases`. Identify mocks needed (which modules,
which network endpoints). Do NOT write tests yet.
```
```
Implement Vitest tests against the plan. Rules: arrange/act/assert blocks,
RTL queries by role/label first (no test-id unless justified), MSW for HTTP,
no `as any` in mocks. Run `vitest run --coverage` and report deltas only for
the touched files.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vitest` | Test runner (Vite-native, ESM-first) | vitest.dev |
| `jest` | Alternative runner (legacy / RN compat) | jestjs.io |
| `@testing-library/react` + `@testing-library/user-event` | Component DOM testing | testing-library.com |
| `msw` v2 | Network mocking via Service Worker / Node interceptor | mswjs.io |
| `happy-dom` | Faster jsdom alternative for Vitest | github.com/capricorn86/happy-dom |
| `@vitest/coverage-v8` | Coverage provider (V8) | vitest.dev/guide/coverage |
| `stryker-mutator` | Mutation testing for coverage trust | stryker-mutator.io |
| `vitest --ui` | Local UI; not for CI | vitest.dev/guide/ui |
| `jest-image-snapshot` (legacy) | Image snapshot when needed | github.com/americanexpress/jest-image-snapshot |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | Standard CI: install, build, `vitest run --coverage --reporter=junit` |
| Codecov / Coveralls | SaaS | Yes | Upload `coverage-final.json`; agents wire via Action |
| Allure / ReportPortal | OSS | Yes | Richer test reports; only worth it at scale |
| Stryker | OSS | Partial | Mutation-test runs in CI nightly, not per-PR |
| MSW | OSS | Yes | Same handlers in unit + Storybook + Playwright |
| Sentry | SaaS | Yes | Capture failures from CI runs; useful for flake triage |

## Templates & scripts
See `templates.md` for the `vitest.config.ts`, RTL setup, and MSW handler patterns. Inline starter `setup.ts` for jsdom polyfills:

```ts
// src/test/setup.ts
import '@testing-library/jest-dom/vitest';
import { afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

// Polyfills jsdom omits
class IO { observe(){} unobserve(){} disconnect(){} takeRecords(){return []} root=null; rootMargin=''; thresholds=[] }
class RO { observe(){} unobserve(){} disconnect(){} }
Object.defineProperty(globalThis, 'IntersectionObserver', { writable: true, value: IO });
Object.defineProperty(globalThis, 'ResizeObserver',       { writable: true, value: RO });
Object.defineProperty(window, 'matchMedia', { writable: true, value: (q: string) => ({
  matches: false, media: q, onchange: null, addListener: () => {}, removeListener: () => {},
  addEventListener: () => {}, removeEventListener: () => {}, dispatchEvent: () => false,
})});
```

CI gate one-liner:

```bash
npx vitest run --coverage --reporter=junit --outputFile=./reports/junit.xml \
  --coverage.thresholds.lines=80 --coverage.thresholds.functions=80
```

## Best practices
- Query order in RTL: `getByRole` → `getByLabelText` → `getByText` → `getByDisplayValue` → `getByTestId` (last resort). Reviewer must reject `getByTestId` without justification.
- Use `userEvent` (not `fireEvent`) for all user-driven interactions to mimic real browser behavior (focus changes, paste events).
- MSW handlers live in `src/test/handlers.ts` and are reusable across unit, Storybook, and Playwright. Don't fork mocks per test type.
- `vi.mock` factories execute before imports — keep them stateless. Use `vi.hoisted` if you need shared state.
- Fake timers: prefer `vi.advanceTimersByTimeAsync` for async paths; restore in `afterEach`.
- Snapshot tests: only for truly stable serializable output; reject snapshots on freshly-generated React HTML — they ratify whatever the LLM wrote.

## AI-agent gotchas
- LLMs use `getByTestId` as the default; acceptable only when no role/label exists. Reviewer must require justification.
- Agents copy Jest patterns into Vitest: `jest.fn()` calls slip through, work because of compat shims, then break when shims drop. Use `vi.fn()` everywhere in Vitest projects.
- `vi.mock` placed below imports has no effect — Vitest hoists statically; if the agent uses dynamic conditions, they must use `vi.doMock` instead.
- Tests tied to implementation detail (private function calls, useState internals) break on every refactor; reviewer must steer to behavior assertions.
- Coverage chasing leads to assertion-free tests that "exercise" code without checking outcomes. Pair coverage with mutation testing or branch-asserts.
- Human-in-loop checkpoint: when the agent is asked to "fix the failing test" — verify root cause is in production code, not the test. Agents will silently weaken assertions to make red turn green.

## References
- Vitest docs — https://vitest.dev/guide/
- Testing Library queries — https://testing-library.com/docs/queries/about
- userEvent — https://testing-library.com/docs/user-event/intro
- MSW v2 — https://mswjs.io/docs/
- Kent C. Dodds testing principles — https://kentcdodds.com/blog/write-tests
- Stryker mutation testing — https://stryker-mutator.io/
