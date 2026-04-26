# Agent Integration — JavaScript/TypeScript Testing

## When to use
- New Vite/Next/Svelte/Vue project — default to Vitest; share `vite.config` for zero-config TS.
- React Native or Expo project — Jest is the only sane choice (Metro bundler + RN preset).
- Component testing for React/Vue/Svelte with `@testing-library/*` — assert by accessible role/label, not implementation details.
- Network mocking for fetch/axios/httpx — use MSW once; reuse handlers across tests, Storybook, dev server.
- E2E + component-level browser tests — Playwright (broader browser support, network + emulation tools).
- Hooks/composables testing — `renderHook` from `@testing-library/react` (modern) or `@testing-library/vue`.

## When NOT to use
- Pure Node CLI scripts < 30 LOC — `node --test` (built-in since Node 18) is enough.
- Bundler-internal config (webpack rules, vite plugins) — test the output bundle, not the config.
- Visual / pixel-perfect rendering — use Chromatic / Percy / Playwright screenshots, not `toHaveTextContent`.
- Cross-browser quirks — those need Playwright/WebDriver, not Jest+jsdom (which is a partial DOM).
- Bundle size assertions — use `bundlesize` / `size-limit` not test runners.

## Where it fails / limitations
- README's "Vitest 10-20x faster" is for watch mode only — cold start of large suites is similar to Jest. Agents quote it as universal.
- ESM vs CJS confusion: Jest needs `transform` config for ESM; agents copy Vitest configs into Jest projects and break.
- `jsdom` lies about layout: `getBoundingClientRect()` returns zeros. Component tests that assert layout hit this constantly.
- React Testing Library deprecated `act()` warnings can fire from genuine bugs OR from misused async helpers — agents add `// eslint-disable` instead of awaiting.
- MSW v2 changed API (`http.get` instead of `rest.get`); blogs and StackOverflow are mostly v1 — agents copy stale snippets.
- TypeScript types in test mocks (`vi.mocked`, `jest.mocked`) are subtly different — agents mix.
- `expect(...).toBe()` vs `.toEqual()` vs `.toStrictEqual()` — the strict variant catches missing `undefined` props, others don't; agents pick wrong.
- Fake timers: `vi.useFakeTimers({ shouldAdvanceTime: true })` is needed when test code awaits real promises mixed with timers; agents miss this.

## Agentic workflow
Pin the framework in the prompt before generation (`Use Vitest with @testing-library/react`). Force the agent to: (1) import from `@testing-library/react`, query by role/label/text, NOT by class name or test ID unless the user supplies one; (2) wrap user interaction in `userEvent` (not `fireEvent`); (3) use MSW for any network call; (4) await `findBy*` for async UI, not `waitFor` + `getBy*`. For backend Node tests, use `vi.mock` / `jest.mock` with `__esModule: true` for ESM modules. CI: run with `--coverage --reporter=junit` for trend tracking.

### Recommended subagents
- `faion-test-agent` (custom) — emit Vitest/Jest tests, restricted to `*.test.ts(x)` files.
- `faion-frontend-developer` — refactors components for testability (controlled inputs, exposed callbacks).
- Reviewer subagent — flags `getByTestId` overuse (>20% of queries is a smell), `act` warnings, missing `userEvent.setup()`.
- `faion-sdd-executor-agent` — TDD loop using `vitest --watch` between phases.

### Prompt pattern
```
Component: src/components/CheckoutButton.tsx.
Generate tests in src/components/CheckoutButton.test.tsx using Vitest + @testing-library/react + userEvent.
Cover:
- Renders disabled when cart is empty.
- Calls onCheckout with cart total when clicked.
- Shows loading spinner while onCheckout promise pending.
- Surfaces error toast on rejection.
Rules:
- Query by accessible role/name first; testId only if no a11y handle exists.
- Wrap user actions in `await user.click(...)` from userEvent.setup().
- Mock network with MSW handler in tests/setup.ts.
- No `fireEvent` unless documented reason.
Run: pnpm vitest run src/components/CheckoutButton.test.tsx.
```

```
API client tests for src/api/orders.ts using Vitest + MSW.
- Spin handlers in tests/msw/handlers.ts; export server.
- Tests assert on returned data and on the request body sent (use server.events).
- Cover: 200 success, 401 retry, 5xx surface error, network failure.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vitest` | Modern Vite-native test runner | https://vitest.dev |
| `jest` | Established runner; required for React Native | https://jestjs.io |
| `@testing-library/react` | Accessibility-first component queries | https://testing-library.com |
| `@testing-library/user-event` v14+ | Simulate user input with delay/timing | https://testing-library.com/docs/user-event |
| `msw` v2 | Network-level mocking (fetch, XHR) | https://mswjs.io |
| `playwright` / `@playwright/test` | E2E + browser component tests | https://playwright.dev |
| `cypress` | Alternative E2E (good DX) | https://cypress.io |
| `happy-dom` | Faster `jsdom` alternative for Vitest | https://github.com/capricorn86/happy-dom |
| `nock` | Node-only HTTP intercept | https://github.com/nock/nock |
| `tsd` / `expect-type` | Type-level assertion testing | https://github.com/SamVerschueren/tsd |
| `stryker-mutator` | Mutation testing for JS/TS | https://stryker-mutator.io |
| `fast-check` | Property-based testing | https://fast-check.dev |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions | CI | Yes | `actions/setup-node` + cache `pnpm-lock.yaml` |
| GitLab CI | CI | Yes | `node:` image; cache `node_modules` |
| Chromatic | SaaS | Yes — CLI publish | Storybook visual regression; pairs with @testing-library |
| Percy | SaaS | Yes — CLI snapshot | Visual regression; integrates with Cypress / Playwright |
| BrowserStack / Sauce Labs | SaaS | Yes — Playwright `--project` | Cross-browser E2E |
| Codecov | SaaS | Yes — `codecov-action` | v8 / istanbul reports from Vitest |
| Trunk Flaky Tests | SaaS | Yes — JUnit ingest | Auto-quarantine flakes; supports Vitest/Jest reporters |

## Templates & scripts
See `templates.md` for ready Vitest config + MSW setup. Inline minimal MSW v2 setup:

```ts
// tests/msw/handlers.ts
import { http, HttpResponse } from 'msw';
export const handlers = [
  http.get('/api/orders', () => HttpResponse.json([{ id: 1 }])),
  http.post('/api/orders', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: 99, ...body }, { status: 201 });
  }),
];

// tests/msw/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';
export const server = setupServer(...handlers);

// vitest.setup.ts
import { server } from './tests/msw/server';
import { afterAll, afterEach, beforeAll } from 'vitest';
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Best practices
- Query by role/name first: `screen.getByRole('button', { name: /checkout/i })`. Reserve `getByTestId` for non-semantic elements.
- Always `await user.click(...)` etc.; `userEvent.setup()` v14+ returns a Promise-based API.
- Use `findByX` for async UI; `waitFor(() => expect(...))` only when no DOM-anchored assertion fits.
- Set MSW `onUnhandledRequest: 'error'` — surfaces forgotten mocks immediately.
- Coverage: Vitest with `--coverage.provider v8` is fast, accurate; istanbul if you need branch coverage in old envs.
- For mocks of TS modules, use `vi.mock('./mod', () => ({ ... }))` then `vi.mocked(fn)` for type-safe access.
- Prefer `expect.objectContaining(...)` for partial matching over exact equality on big payloads.
- Reset modules between tests when global state matters: `vi.resetModules()` in `afterEach`.
- Snapshot tests: only for stable DOM trees; never for snapshots that vary by environment.
- Co-locate tests next to source: `Button.tsx` + `Button.test.tsx`.

## AI-agent gotchas
- **MSW v1 vs v2 syntax** — agents emit `rest.get` (v1) into v2 codebases. Specify `msw v2` and `http.get` explicitly.
- **`fireEvent` vs `userEvent`**: agents reach for `fireEvent.click` (synchronous, fires DOM event) instead of `await user.click` (simulates real interaction). The latter dispatches related events (mouseover, focus) and is more accurate.
- **Async `act` warnings**: agents sprinkle `await act(async () => ...)` everywhere. Usually means the assertion should `await findBy*` instead.
- **Importing from internal paths**: `import x from '@testing-library/react/dist/...'` — agents do this when autocompleting; breaks on minor version bumps.
- **Jest in ESM project**: Jest's ESM support requires `--experimental-vm-modules` and `extensionsToTreatAsEsm` config; agents copy Vitest configs that won't apply.
- **`jest.mocked` vs `vi.mocked`** — wrong import for the runner gives runtime undefined.
- **Mocking modules at the wrong path**: `vi.mock('./api')` resolves relative to the test file, not the SUT. Agents trip on this when test and SUT live in different folders.
- **Fake timers + Promises**: `vi.useFakeTimers()` doesn't advance microtasks; need `await vi.runAllTimersAsync()` or real timers for promise chains.
- **`describe.each` / `it.each`** with template-string interpolation requires `%s` placeholders; agents use literal `${var}` and the row name silently becomes `${var}`.
- **Snapshot drift**: agents accept `--update-snapshots` blindly. Block that flag in CI; require local snapshot updates as a separate commit.
- **Type-only imports in tests**: TS strips them, leaving runtime undefined when used as mock targets. Use `import type { ... }` consciously.
- **`globals: true` vs explicit imports**: Vitest globals avoid import statements but break in ESM-strict TS projects; agents flip-flop. Pick one for the codebase.
- **`screen.debug()` in committed code**: prints DOM to stdout, slows CI. Add a lint rule banning it.

## References
- README: `./README.md`
- Sibling: `../testing-patterns/`, `../mocking-strategies/`, `../e2e-testing/`, `../unit-testing/`
- Vitest: https://vitest.dev
- Jest: https://jestjs.io
- Testing Library: https://testing-library.com
- userEvent v14: https://testing-library.com/docs/user-event/intro/
- MSW v2: https://mswjs.io/docs
- Playwright: https://playwright.dev
- Kent C. Dodds — common testing library mistakes: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
- happy-dom vs jsdom: https://github.com/capricorn86/happy-dom
