# AGENT-03: JavaScript/TypeScript Tooling for AI-Augmented SDLC

**Summary line 1:** The deterministic JS/TS floor in 2026 is `tsc --strict` + Biome v2 (or ESLint flat config when type-aware rules require typescript-eslint) + Vitest 3 + Playwright, glued by lefthook/husky pre-commit gates and pnpm catalogs.
**Summary line 2:** AI agents (Cursor, Claude Code) ride on top of that floor — they reuse `tsserver` diagnostics, fail loudly on `noUncheckedIndexedAccess`, and are sandboxed by mutation testing (Stryker), property tests (fast-check), contract tests (Pact-JS), and supply-chain scanners (Socket.dev) so generated code can't silently regress.

---

## 1. `lang-ts-strict-isolated` — TypeScript strict mode + isolatedDeclarations + project references

**Rule:** Every `tsconfig.json` in a workspace turns on `"strict": true`, `"noUncheckedIndexedAccess": true`, `"exactOptionalPropertyTypes": true`, `"isolatedDeclarations": true` (for libraries), and uses project references (`"composite": true` + `references`) so each package builds against its dependency's `.d.ts` rather than its source. Enables Biome/swc/oxc to emit declarations without invoking `tsc` for inference.

**Real URL:** [TypeScript: TSConfig Option: isolatedDeclarations](https://www.typescriptlang.org/tsconfig/isolatedDeclarations.html), [TypeScript Project References — moonrepo](https://moonrepo.dev/docs/guides/javascript/typescript-project-refs)

**When to use:** Any monorepo with ≥2 packages, any published library, any codebase >10k LOC. Required floor before LLM-generated code is trusted — strict mode makes the AI's mistakes type-errors instead of runtime bugs.

**When NOT:** Tiny scripts, throwaway prototypes, single-file Deno/Bun snippets. Don't enable `isolatedDeclarations` on app code (only libraries / shared packages) — the annotation overhead is wasted on app entrypoints.

**Snippet:**
```jsonc
// packages/core/tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "isolatedDeclarations": true,
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "module": "NodeNext",
    "moduleResolution": "NodeNext"
  },
  "references": [{ "path": "../shared" }]
}
```

---

## 2. `lint-biome-v2-type-aware` — Biome v2 as default linter+formatter, ESLint only for type-aware exotica

**Rule:** Use Biome v2.x as the single linter+formatter (replaces ESLint+Prettier). Adopt `noFloatingPromises` and other type-aware rules from Biome v2 — they catch ~75% of typescript-eslint's coverage at 10–25× speed. Fall back to ESLint flat config + `typescript-eslint` only for the long tail of project-specific rules Biome doesn't yet ship (e.g., `no-misused-promises` edge cases, custom RTL rules).

**Real URL:** [Biome v2 announcement](https://biomejs.dev/blog/biome-v2/), [Biome vs ESLint vs Oxlint 2026 — PkgPulse](https://www.pkgpulse.com/blog/eslint-vs-biome-2026)

**When to use:** New projects, any monorepo where pre-commit lint takes >2s, teams who want one tool for format+lint+import-sort. Biome v2 added nested configs (`"extends": "//"`) so monorepos no longer need duplicated `biome.json`.

**When NOT:** Projects heavily dependent on ecosystem ESLint plugins (e.g., `eslint-plugin-react-hooks` exhaustive-deps with custom hook patterns, `eslint-plugin-jsx-a11y` rich rules) — Biome's coverage there is still partial. Don't dual-run Biome + ESLint format; pick one formatter to avoid CRLF/LF wars.

**Snippet:**
```jsonc
// biome.json (root)
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "nursery": { "noFloatingPromises": "error" }
    }
  },
  "formatter": { "enabled": true, "indentStyle": "space", "indentWidth": 2 }
}
// packages/web/biome.json
{ "extends": "//", "linter": { "rules": { "style": { "useNamingConvention": "off" } } } }
```

---

## 3. `test-vitest-3-projects` — Vitest 3 with `projects` config + browser mode

**Rule:** Standardize on Vitest 3.x. Use `projects` (renamed from `workspace` in 3.2) for monorepos so each package gets its own config but a single test run. Use `--browser.enabled` (Playwright provider) for component tests instead of jsdom whenever DOM/CSS fidelity matters. Migrate Jest by find/replace (`jest` → `vi`, `jest.config.js` → `vitest.config.ts`); 90%+ of suites run unchanged.

**Real URL:** [Vitest Migration Guide](https://vitest.dev/guide/migration.html), [Vitest Browser Mode](https://vitest.dev/guide/browser/), [Vitest 3 vs Jest 30 2026 — PkgPulse](https://www.pkgpulse.com/blog/vitest-3-vs-jest-30-2026)

**When to use:** Any Vite-powered project (default win, 3–8× faster). Greenfield Node libraries (better ESM story). Anything with React/Vue/Svelte components — browser mode replaces jsdom hacks.

**When NOT:** Pure CommonJS legacy with deep `jest.mock()` factory abuse — migration cost can exceed benefit. React Native (Jest's `react-native` preset still owns this niche). Tests that rely on Jest-specific snapshot serializers from the React Native ecosystem.

**Snippet:**
```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config'
export default defineConfig({
  test: {
    projects: [
      { test: { name: 'unit', include: ['src/**/*.test.ts'], environment: 'node' } },
      { test: { name: 'dom',  include: ['src/**/*.browser.test.tsx'],
                browser: { enabled: true, provider: 'playwright', instances: [{ browser: 'chromium' }] } } }
    ],
    coverage: { provider: 'v8', thresholds: { lines: 80, branches: 75 } }
  }
})
```

---

## 4. `test-playwright-codegen-traces` — Playwright as the default E2E + AI-augmented codegen

**Rule:** Playwright (not Cypress) for E2E. Always run with `trace: 'retain-on-failure'` and `--reporter=html` so failures produce inspectable traces (network + DOM snapshots + actionability log). Use `npx playwright codegen` to bootstrap tests — its locator inference (`getByRole`, `getByLabel`) produces semantic locators that survive DOM churn better than CSS selectors. AI-native layers (Shiplight, Momentic) build on Playwright; staying on Playwright keeps the upgrade path.

**Real URL:** [Playwright docs](https://playwright.dev/), [Playwright vs Cypress 2026 — Shiplight](https://www.shiplight.ai/blog/playwright-vs-cypress)

**When to use:** All cross-browser E2E in 2026. Multi-tab flows, multiple origins (Cypress chokes here). CI parallelism (Playwright shards for free; Cypress charges via Cloud).

**When NOT:** Teams already invested in Cypress component testing with strong DX wins; switching cost dominates. Pure component tests inside a Storybook/Vite stack — use the Vitest addon (#9) instead of Playwright Component Testing.

**Snippet:**
```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'
export default defineConfig({
  testDir: 'e2e',
  fullyParallel: true,
  use: { trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] } }
  ]
})
```

---

## 5. `test-pact-consumer-driven` — Pact-JS contracts for service boundaries

**Rule:** Every consumer of an internal HTTP/GraphQL API writes a Pact consumer test that produces a contract artifact. Provider verifies against the broker on every PR. Pact tests run in unit-test cycle (consumer-side) so they're fast and deterministic — no shared staging environment required. Pact v3 (state of 2026) supports message contracts (Kafka/SNS) too.

**Real URL:** [Pact Docs](https://docs.pact.io/), [Pact JS Consumer Tests](https://docs.pact.io/implementation_guides/javascript/docs/consumer)

**When to use:** ≥3 services owned by ≥2 teams. Microservice rollouts where breaking a downstream consumer is expensive. Public-API SDKs (consumer = SDK, provider = your API).

**When NOT:** Single monorepo where you can do typed cross-package imports — TypeScript types are a stronger contract than Pact JSON. Single-team services that deploy together. Rapidly evolving experimental APIs (contract churn dominates value).

**Snippet:**
```ts
// orders.consumer.pact.test.ts
import { PactV3, MatchersV3 } from '@pact-foundation/pact'
const { like, integer } = MatchersV3
const provider = new PactV3({ consumer: 'web', provider: 'orders-api' })
provider
  .given('order 42 exists')
  .uponReceiving('a request for order 42')
  .withRequest({ method: 'GET', path: '/orders/42' })
  .willRespondWith({ status: 200, body: like({ id: integer(42), total: 99.5 }) })
```

---

## 6. `test-stryker-mutation` + `test-fast-check-property` — quality gates that stress LLM-generated tests

**Rule:** Run Stryker mutation testing on critical packages (auth, billing, parsing) at ≥80% mutation score. Use the `@stryker-mutator/typescript-checker` plugin so type-error mutants are dropped (saves CPU). Pair with fast-check for property-based tests on pure functions — generators expose corner cases LLMs forget (NaN, empty strings, surrogate pairs). Both run nightly, not per-commit (too slow).

**Real URL:** [Stryker JS](https://stryker-mutator.io/docs/stryker-js/introduction/), [@stryker-mutator/typescript-checker](https://stryker-mutator.io/docs/stryker-js/typescript-checker/), [fast-check](https://fast-check.dev/)

**When to use:** Code paths where coverage % is a lie (LLM-written tests often hit lines without verifying behavior). Mature libraries before publishing 1.0. Anything with branching logic that handles money, auth, or user input.

**When NOT:** UI components (visual regression is the better tool — see Storybook). I/O-heavy code where mutants don't change observable behavior. Pre-1.0 churn (rewrites invalidate the mutation report constantly).

**Snippet:**
```js
// stryker.config.js
export default {
  testRunner: 'vitest',
  checkers: ['typescript'],
  tsconfigFile: 'tsconfig.json',
  mutate: ['src/billing/**/*.ts', '!src/**/*.test.ts'],
  thresholds: { high: 85, low: 70, break: 65 },
  incremental: true   // only re-mutate changed files in CI
}
```
```ts
// money.property.test.ts
import fc from 'fast-check'
import { add } from './money'
test('add is associative', () => {
  fc.assert(fc.property(fc.integer(), fc.integer(), fc.integer(),
    (a, b, c) => add(add(a, b), c) === add(a, add(b, c))))
})
```

---

## 7. `lint-lefthook-or-husky-staged` — pre-commit gate (the AI guardrail)

**Rule:** Every repo has a pre-commit hook that runs Biome/ESLint on staged files only. Choose **lefthook** (Go binary, parallel by default, single YAML, ~10× faster on large repos) for monorepos; **husky + lint-staged** for small Node-only repos where the ecosystem familiarity wins. Pre-commit blocks: format, lint, secret-scan. Pre-push: `tsc --noEmit`, unit tests. Never `--no-verify`.

**Real URL:** [Lefthook](https://lefthook.dev/), [Husky](https://typicode.github.io/husky/), [husky vs lefthook vs lint-staged 2026](https://www.pkgpulse.com/blog/husky-vs-lefthook-vs-lint-staged-git-hooks-nodejs-2026)

**When to use:** Every project. This is the layer that catches AI-generated `console.log`, `any` types, malformed imports before they hit CI. Lefthook for monorepos (root-scoped commands, parallel jobs); husky for solo-repo Node projects.

**When NOT:** Solo experimental repos where speed-of-thought matters more than hygiene. Server-side build pipelines that already run identical checks (don't double-pay). Don't put slow checks (full test suite, full type-check on huge repo) in pre-commit — push to pre-push instead.

**Snippet:**
```yml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    biome:
      glob: "*.{ts,tsx,js,jsx,json}"
      run: pnpm biome check --apply --no-errors-on-unmatched {staged_files}
      stage_fixed: true
    secrets:
      run: gitleaks protect --staged --redact
pre-push:
  commands:
    typecheck: { run: pnpm -r exec tsc --noEmit }
    test:      { run: pnpm vitest run --changed origin/main }
```

---

## 8. `lang-pnpm-catalogs` — pnpm workspaces + dependency catalogs as the monorepo default

**Rule:** Use pnpm 9+ with `workspaces` and the `catalog:` protocol for shared dependency versions. Catalogs eliminate version drift across packages — one bump in `pnpm-workspace.yaml` updates every workspace. Use `workspace:*` for internal package refs, `catalog:` for external. Bun 1.3+ has catalogs too but pnpm's monorepo tooling (filtering, `--filter ...{path}`, strict peer-dep resolution) is still ahead in 2026.

**Real URL:** [pnpm catalogs](https://pnpm.io/catalogs), [pnpm workspaces](https://pnpm.io/workspaces), [pnpm vs Bun vs Yarn 2026](https://dev.to/pockit_tools/pnpm-vs-npm-vs-yarn-vs-bun-the-2026-package-manager-showdown-51dc)

**When to use:** Any repo with ≥2 packages. Any team that has ever fought "package A wants react@19.0, package B wants react@19.1" merge conflicts.

**When NOT:** Single-package apps where npm/Bun is fine. Bun-native runtime projects (use `bun install` natively to keep `bun.lockb` parity with runtime). Yarn 4 PnP shops with working constraints — the migration cost rarely pays back.

**Snippet:**
```yaml
# pnpm-workspace.yaml
packages: ['packages/*', 'apps/*']
catalog:
  react: ^19.0.0
  typescript: ^5.7.0
  vitest: ^3.0.0
```
```jsonc
// packages/web/package.json
{ "dependencies": { "react": "catalog:", "@org/core": "workspace:*" } }
```

---

## 9. `test-storybook-vitest-addon` — Storybook stories as Vitest tests

**Rule:** Replace the legacy `@storybook/test-runner` (Playwright-driven) with the **Storybook Vitest addon** (Storybook 8.3+) that turns every `play()` function into a real Vitest browser test. One test command runs unit + interaction + a11y. Stories double as documentation, fixtures, and tests — DRY for component teams.

**Real URL:** [Storybook Vitest addon](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon), [Test runner (deprecated path)](https://storybook.js.org/docs/writing-tests/integrations/test-runner)

**When to use:** Any Vite-powered Storybook (React, Vue, Svelte, Angular Vite). Component libraries. Design systems where stories already exist.

**When NOT:** Webpack5-only Storybooks (test runner still applies). Heavily mocked unit tests that don't benefit from a real browser. Server components / RSC stories where the runtime model isn't yet covered.

**Snippet:**
```ts
// .storybook/vitest.setup.ts
import { setProjectAnnotations } from '@storybook/react'
import * as preview from './preview'
setProjectAnnotations(preview)
// Button.stories.ts
export const Clicked: Story = {
  args: { label: 'Save' },
  play: async ({ canvas, userEvent }) => {
    await userEvent.click(canvas.getByRole('button'))
    await expect(canvas.getByText('Saved')).toBeVisible()
  }
}
```

---

## 10. `sec-socket-snyk-attw` — supply chain + types-shape gates in CI

**Rule:** Run three security/quality gates on every PR:
1. **Socket.dev** (or `socket-cli`) for behavioral analysis of new dependencies — catches malicious packages before a CVE exists (post-Shai-Hulud, post-axios-March-2026 incidents this is non-optional).
2. **Snyk** or `npm audit --audit-level=high` as a CVE backstop.
3. **`@arethetypeswrong/cli`** (`attw`) on every published package — verifies your `.d.ts` resolves under all module systems (CJS, ESM, Node10, bundler).

Combined, these block the three classes of attack that bypass type-checks: typosquats, install-time RCE, and broken types that force consumers to `any`.

**Real URL:** [Socket.dev](https://socket.dev/), [Are The Types Wrong](https://arethetypeswrong.github.io/), [attw on GitHub](https://github.com/arethetypeswrong/arethetypeswrong.github.io), [Snyk npm best practices](https://snyk.io/articles/npm-security-best-practices-shai-hulud-attack/)

**When to use:** Every published package — `attw` is mandatory before `npm publish`. Every app with >50 transitive deps — Socket alerts on suspicious install scripts. Anything internal that pulls from public registries (still 99% of malware vector).

**When NOT:** Air-gapped vendored deps with no install-time scripts (Socket has nothing to analyze). Pure first-party monorepos. `attw` is irrelevant for non-published apps.

**Snippet:**
```yaml
# .github/workflows/ci.yml (excerpt)
- run: npx socket-cli ci             # block on supply-chain risk
- run: npm audit --audit-level=high
- run: pnpm -r exec attw --pack       # check every public package
```

---

## 11. `ai-agent-tsserver-skill` — Cursor/Claude-Code TypeScript-aware skills

**Rule:** Configure your AI agent (Cursor `.cursor/rules/`, Claude Code `.claude/skills/`) so it (a) reads `tsconfig.json` to know strict-mode flags, (b) runs `tsc --noEmit` after edits via tool-use to verify, (c) prefers `getByRole`/`getByLabel` over CSS selectors in tests, (d) avoids `any` and `as unknown as T` casts. Pair-program: agent edits → pre-commit hook + `tsc` block bad output → agent retries with diagnostics in context.

**Real URL:** [Claude Code Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills), [Cursor Rules](https://docs.cursor.com/context/rules-for-ai), [10 Must-Have Skills for Claude 2026](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051)

**When to use:** Any team with Claude Code or Cursor in the loop. Any repo where an agent has edit/commit privileges. Skills should encode project conventions (naming, error types, test patterns) so the agent doesn't reinvent style.

**When NOT:** Solo prototyping where the cost of writing a skill exceeds the value. Languages outside JS/TS — these skills don't transfer (write per-language skills instead). Don't put secrets/private API surface in skills (they're prompt content).

**Snippet:**
```md
<!-- .claude/skills/ts-edit/SKILL.md -->
# ts-edit — TypeScript-aware editing

## Rules
- Never introduce `any`. If a type is unknown, narrow with `unknown` + type guards.
- Every exported function in `packages/*` MUST have an explicit return type
  (isolatedDeclarations is on).
- After every edit, run `pnpm -w exec tsc --noEmit -p <changed-package>`.
  If it fails, read the diagnostic and fix BEFORE returning to the user.
- Prefer `getByRole` over `data-testid` in test files under `**/*.test.tsx`.
```

---

## Mapping back to the four buckets

| Bucket | Methodologies |
|---|---|
| `lang-` | #1 ts-strict-isolated, #8 pnpm-catalogs |
| `lint-` | #2 biome-v2, #7 lefthook-or-husky-staged |
| `test-` | #3 vitest-3-projects, #4 playwright-codegen, #5 pact-consumer-driven, #6 stryker+fast-check, #9 storybook-vitest |
| `sec-`  | #10 socket-snyk-attw |
| (cross) | #11 ai-agent-tsserver-skill — meta-rule that ties the rest to AI agents |

---

## Cross-cutting note: the AI-augmented JS/TS loop

The deterministic floor (strict TS + Biome + Vitest + Playwright) is what makes AI-augmented SDLC work in JS/TS. Every methodology above produces a machine-readable diagnostic the agent can read on tool-use failure: `tsc` JSON errors, Biome's structured output, Vitest's `--reporter=json`, Stryker's HTML+JSON report, Pact broker's verification status, Socket's `--json` audit. An agent without that floor hallucinates plausible code that compiles but fails at runtime; with the floor, the same agent produces code that survives `pnpm verify` (typecheck + lint + test + audit) — and that's the unit of trust for letting it commit.

## Sources

- [Biome v2 announcement](https://biomejs.dev/blog/biome-v2/)
- [Biome vs ESLint vs Oxlint 2026 — PkgPulse](https://www.pkgpulse.com/blog/eslint-vs-biome-2026)
- [TypeScript: TSConfig — isolatedDeclarations](https://www.typescriptlang.org/tsconfig/isolatedDeclarations.html)
- [TypeScript Project References — moonrepo](https://moonrepo.dev/docs/guides/javascript/typescript-project-refs)
- [Vitest Migration Guide](https://vitest.dev/guide/migration.html)
- [Vitest 3 vs Jest 30 2026 — PkgPulse](https://www.pkgpulse.com/blog/vitest-3-vs-jest-30-2026)
- [Playwright vs Cypress 2026 — Shiplight](https://www.shiplight.ai/blog/playwright-vs-cypress)
- [Pact Docs](https://docs.pact.io/)
- [Pact JS Consumer Tests](https://docs.pact.io/implementation_guides/javascript/docs/consumer)
- [Stryker JS](https://stryker-mutator.io/docs/stryker-js/introduction/)
- [@stryker-mutator/typescript-checker](https://stryker-mutator.io/docs/stryker-js/typescript-checker/)
- [husky vs lefthook vs lint-staged 2026 — PkgPulse](https://www.pkgpulse.com/blog/husky-vs-lefthook-vs-lint-staged-git-hooks-nodejs-2026)
- [pnpm vs Bun vs Yarn 2026 — DEV/Pockit](https://dev.to/pockit_tools/pnpm-vs-npm-vs-yarn-vs-bun-the-2026-package-manager-showdown-51dc)
- [Snyk: NPM Security Best Practices post-Shai-Hulud](https://snyk.io/articles/npm-security-best-practices-shai-hulud-attack/)
- [Storybook Vitest addon](https://storybook.js.org/docs/writing-tests/integrations/vitest-addon)
- [Storybook Test runner (legacy)](https://storybook.js.org/docs/writing-tests/integrations/test-runner)
- [10 Must-Have Skills for Claude 2026 — Medium](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051)
- [Cursor vs Claude Code 2026 — DEV](https://dev.to/whoffagents/cursor-vs-claude-code-which-ai-coding-tool-is-actually-better-in-2026-3c2p)
