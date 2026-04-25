# AGENT-07 — Test Patterns + AI Agents

**Summary line 1:** Tests are the load-bearing guardrail when an LLM writes code; the strongest patterns (TDD, property-based, mutation, contract) are also the ones that give an agent a *machine-readable* feedback signal.
**Summary line 2:** Snapshot/E2E/visual layers survive an AI rewrite only if their assertions encode *intent*, not just *output* — otherwise the agent re-snapshots its own bugs and calls them green.

---

## CAND-T01: tdd-agent-loop

- **Category:** test-
- **Source:** https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/ , https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
- **Status:** new
- **Why valuable:** TDD only works with an agent if the test-writer and the implementer run in *separate* contexts; otherwise the implementer cheats by reading what the test was meant to check.
- **One-line rule:** Run RED in a sub-agent that has only the spec, then run GREEN in a sub-agent that has only the failing test output and the codebase — never let one Claude window own both.
- **When-to:** Agent-driven feature work where the spec is testable in pure functions or HTTP responses (parsers, validators, calculators, API endpoints).
- **When-NOT:** Pure UI styling, exploratory spikes, throw-away scripts — TDD overhead is wasted there.
- **Snippet (Claude Code skill split):**

```yaml
# .claude/skills/tdd-red.md  -> isolated subagent
description: "Write the smallest failing test for the AC. Output test file + failing pytest line."
allowed_tools: [Read, Write]   # NO Edit on src/
# .claude/skills/tdd-green.md  -> isolated subagent
description: "Make the failing test pass. You MAY NOT modify the test file."
allowed_tools: [Read, Edit]    # NO Write on tests/
```

---

## CAND-T02: property-based-claude

- **Category:** test-
- **Source:** https://red.anthropic.com/2026/property-based-testing/ , https://arxiv.org/abs/2510.09907 , https://hypothesis.readthedocs.io/en/latest/ghostwriter.html
- **Status:** new
- **Why valuable:** Anthropic's own agent ran Hypothesis on 100 popular Python pkgs (NumPy/SciPy/Pandas), generated 984 bug reports across 786 modules, with 56% true-bug rate on a manual-review sample and 86% on top-ranked. LLMs *infer* properties from docstrings/types better than they invent example tests.
- **One-line rule:** For any pure function with a docstring, run an agent that proposes invariants (round-trip, idempotence, commutativity, monotonicity, equivalence) and writes them as `@given` Hypothesis tests *before* writing example-based tests.
- **When-to:** Pure logic — serialization, parsing, math, sorting, dedup, schema validators, anything with an inverse or an algebraic property.
- **When-NOT:** Stateful side-effecting code without clear invariants, UI rendering, anything where the "spec" is "whatever the current output is."
- **Snippet:**

```python
# Agent prompt fragment baked into a skill
RUBRIC = """Propose properties grounded in: (1) function name, (2) docstring,
(3) type signature, (4) one example call. For each, choose a class:
round-trip, idempotence, oracle-equivalence, metamorphic, invariant-on-output.
Reject any property you cannot justify from the source text."""

@given(st.text())
def test_quote_roundtrip(s):
    assert unquote(quote(s)) == s   # round-trip property
```

---

## CAND-T03: mutation-as-agent-feedback

- **Category:** test-
- **Source:** https://testdouble.com/insights/keep-your-coding-agent-on-task-with-mutation-testing , https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/ , https://arxiv.org/abs/2501.12862
- **Status:** new
- **Why valuable:** Coverage % is a near-useless signal for AI-written code (one DEV.to author's "93% coverage" was 34% mutation score). Mutation score is the cheapest *truth-bearing* signal you can hand an agent. Meta's ACH (FSE 2025) extends this: LLMs *generate the mutants* for the area you care about (privacy, compliance), then generate tests guaranteed to kill them. 73% of ACH-suggested tests were merged at Messenger/WhatsApp.
- **One-line rule:** After the agent writes/changes tests, run Stryker/mutmut on changed files only and pipe the surviving-mutants report back as the next prompt — keep looping until score ≥ threshold or agent gives up explicitly.
- **When-to:** Critical business logic (payments, auth, pricing, rules engines), CI quality gates on PRs from coding agents, retrofitting tests on legacy code.
- **When-NOT:** Slow test suites (mutation cost = N_mutants × test_time), generated/serialization code where mutants are mostly equivalent, prototype phase.
- **Snippet:**

```bash
# Stryker run scoped to changed files, fed back to agent
{ git diff --name-only -z HEAD -- src/ ; \
  git ls-files --others --exclude-standard -z -- src/ ; } \
  | xargs -0 stryker run -m
# stryker.conf.json
{ "thresholds": { "high": 80, "low": 60, "break": 70 } }   # break -> CI red
```

---

## CAND-T04: consumer-contract-from-openapi

- **Category:** test-
- **Source:** https://docs.pact.io/ai_tools/pactflow-skill , https://pactflow.io/blog/pactflow-mcp-server/ , https://pactflow.io/ai/
- **Status:** new
- **Why valuable:** Pact's traditional weakness — consumer teams have to *write* the contract test — disappears when an MCP server reads OpenAPI/HTTP traffic/client code and generates the consumer Pact. PactFlow reports up to 60% reduction in test creation time, and the AI-generated contract is deterministic enough to gate provider deploys with `can-i-deploy`.
- **One-line rule:** Don't let an LLM hand-write Pacts; point its MCP/skill at the OpenAPI spec or recorded HTTP traffic and have it emit consumer Pact tests, then commit those as the source of truth — never edit them manually after.
- **When-to:** Microservices with > 2 consumers per provider, polyglot stacks where mocks drift, autonomous agents that consume third-party APIs.
- **When-NOT:** Single-consumer monoliths, GraphQL with strong codegen (use schema diff instead), one-off internal cron-callers.
- **Snippet:**

```typescript
// PactFlow MCP skill prompt
"contract-testing_generate_pact_tests --spec ./openapi.yaml \
  --consumer billing-ui --provider billing-api --lang ts"
// → produces pact/billing-ui-billing-api.json + matching jest test
```

---

## CAND-T05: e2e-codegen-then-refactor

- **Category:** test-
- **Source:** https://playwright.dev/docs/codegen , https://testdino.com/blog/playwright-ai-codegen/ , https://www.checklyhq.com/blog/generate-end-to-end-tests-with-ai-and-playwright/
- **Status:** new
- **Why valuable:** Playwright `codegen` captures the real DOM truth (modals, redirects, animations) faster than any human or LLM staring at the spec. But raw codegen output is brittle (CSS selectors, missing assertions). The 2026 sweet spot is *codegen records → AI refactors → human reviews*. Pure AI-from-scratch produces hallucinated selectors.
- **One-line rule:** Generate the *trace* with `npx playwright codegen`, then feed the recording to an agent with a strict refactor prompt: replace CSS selectors with role/test-id locators, extract page objects, add explicit `expect()` assertions tied to ACs.
- **When-to:** New user flows on existing UI, smoke-test backfill, regression coverage after a bug.
- **When-NOT:** Headless API flows (use contract tests), flows behind 2FA / captcha / OTP without test-mode bypass.
- **Snippet:**

```bash
npx playwright codegen --target=playwright-test https://app.local
# pipe the recorded test through the agent:
# "Replace every page.locator('css=...') with page.getByRole(...) or
#  getByTestId(...). Extract repeated steps into Page Object methods.
#  Add expect(page).toHaveURL(...) and toHaveText(...) for every AC."
```

---

## CAND-T06: visual-ai-diff-not-pixel

- **Category:** test-
- **Source:** https://www.chromatic.com/storybook , https://percy.io/blog/ai-visual-testing-tools , https://applitools.com/blog/test-your-components-where-you-build-with-the-applitools-storybook-addon/
- **Status:** new
- **Why valuable:** Pixel-diff visual tests (classic Loki/old-Percy) drown in false positives from font hinting, sub-pixel rendering, and ad/timestamp churn. Perceptual/AI diff (Applitools Visual AI, Percy AI Review Agent, Chromatic's intelligent diff) lets the test *understand* "this is a layout shift" vs "this is anti-aliasing noise." Without it, devs rubber-stamp every diff and the test loses signal.
- **One-line rule:** Run visual regression at the Storybook component level (not E2E pages), and choose a tool whose diff engine ignores rendering noise — pixel-perfect diffs are an anti-pattern in 2026.
- **When-to:** Design systems, component libraries, marketing sites where layout integrity matters more than logic.
- **When-NOT:** Stateful flows (use Playwright assertions), backend services, anything without a stable visual reference (charts with live data).
- **Snippet:**

```yaml
# .github/workflows/chromatic.yml
- run: npx chromatic --project-token=$CHROMATIC \
        --only-changed --exit-zero-on-changes
# Block merge only if reviewer rejects, not on every pixel diff
```

---

## CAND-T07: load-test-scenarios-from-traffic

- **Category:** test-
- **Source:** https://medium.com/@zilliz_learn/how-to-load-test-an-llm-api-with-gatling-9620fb1e0557 , https://www.vervali.com/blog/best-load-testing-tools-in-2026-definitive-guide-to-jmeter-gatling-k6-loadrunner-locust-blazemeter-neoload-artillery-and-more/ (NeoLoad MCP)
- **Status:** new
- **Why valuable:** Hand-written load scenarios are always wrong because they reflect *what the engineer imagined users do*, not what they actually do. NeoLoad's MCP server (first perf tool to ship MCP, 2026) and equivalent k6/Artillery patterns let an agent ingest production traces, OpenAPI, or RUM data and synthesize realistic mixed-workload scenarios.
- **One-line rule:** Feed the agent (production access logs ∪ OpenAPI ∪ SLO doc) and ask it to emit a k6 scenario with weighted endpoints, think-times, and ramp shapes that reproduce *yesterday's traffic*, not a uniform burst.
- **When-to:** Pre-launch capacity planning, post-incident regression, SLO verification before a refactor.
- **When-NOT:** Smoke testing (use HTTP probes), single-user perf debugging (use a profiler), brand-new features with no production data.
- **Snippet:**

```javascript
// k6 scenario synthesized from access.log frequencies
import http from 'k6/http';
export const options = {
  scenarios: {
    realistic: { executor: 'ramping-arrival-rate',
      stages: [{ target: 50, duration: '2m' },
               { target: 200, duration: '5m' }] }}};
export default function () {
  const r = Math.random();
  if (r < 0.62) http.get('/api/feed');     // 62% of prod traffic
  else if (r < 0.91) http.get('/api/me');  // 29%
  else http.post('/api/comment', payload); // 9%
}
```

---

## CAND-T08: bdd-gherkin-by-llm-from-stories

- **Category:** test-
- **Source:** https://www.humanizingwork.com/ai-for-better-bdd/ , https://medium.com/@bart.rosa/the-use-of-large-language-models-in-behavior-driven-development-example-using-gpt-4-and-gherkin-6f12f069610b , https://arxiv.org/pdf/2403.14965
- **Status:** new
- **Why valuable:** BDD's traditional friction is *writing* Given-When-Then; LLMs are great at this exact transformation (user story → Gherkin). GPT-4-class models produce error-free Gherkin in studies. But agents trained on bad public Gherkin will reproduce bad Gherkin — guard with a style rubric.
- **One-line rule:** Treat the user story as the *prompt* and require the agent to emit Gherkin that uses domain language only — reject any scenario that mentions UI elements, CSS selectors, or HTTP verbs.
- **When-to:** Stakeholder-facing features where PMs/QA/devs share a language; regulated domains where ACs need to be auditable.
- **When-NOT:** Internal libraries, infra code, throw-away prototypes — Gherkin is overhead there.
- **Snippet:**

```gherkin
# Bad (rejected by rubric): "When I click button#submit"
# Good (accepted):
Feature: Refund a paid order
  Scenario: Customer requests refund within 14 days
    Given a delivered order placed 5 days ago
    When the customer requests a refund
    Then the refund is approved automatically
    And the customer is notified by email
```

---

## CAND-T09: snapshot-only-with-intent-comment

- **Category:** test-
- **Source:** https://selleo.com/blog/when-to-use-jest-snapshots , https://news.ycombinator.com/item?id=46205015 , https://jestjs.io/docs/snapshot-testing
- **Status:** new
- **Why valuable:** Snapshot tests survive an AI rewrite *only* when the developer cannot just press `-u` and call it done. Without intent encoded next to the snapshot, an agent confronted with a failing snapshot will simply update it — re-snapshotting the bug. Snapshots and golden-master tests are the same technique; the difference is the discipline around accepting diffs.
- **One-line rule:** Every snapshot file must carry a sibling `.intent.md` (or a docstring above the test) describing *what semantic property* the snapshot defends; reviewers (and agents) must justify any diff against that intent before `-u` is allowed.
- **When-to:** Big serialized structures (rendered React tree, generated SQL, API response shape) where explicit assertions would be 100 lines.
- **When-NOT:** Simple props, logic with < 5 outputs (write explicit `expect()`), anything containing timestamps/UUIDs/random IDs without normalization.
- **Snippet:**

```typescript
// invoice-render.test.tsx
// INTENT: snapshot defends three properties:
//   1. tax line appears below subtotal
//   2. currency symbol matches user locale
//   3. discount, if zero, is hidden
expect(render(<Invoice {...props} />)).toMatchSnapshot();
```

---

## CAND-T10: golden-master-for-legacy-rewrite

- **Category:** test-
- **Source:** https://news.ycombinator.com/item?id=46205015 (golden-master + LLM thread) , https://medium.com/blogfoster-engineering/how-to-use-the-power-of-jests-snapshot-testing-without-using-jest-eff3239154e5
- **Status:** new
- **Why valuable:** When you ask an agent to rewrite a 5000-line legacy module, you have no spec — you have *current behavior*. Capture inputs/outputs from production (or from a fuzzer) into a golden-master corpus; the agent's rewrite must reproduce every output bit-for-bit (or with documented diffs). This is the only test that scales to AI-driven rewrites of untested legacy.
- **One-line rule:** Before letting an agent touch unknown legacy, generate a golden-master corpus of (input, output) pairs from production traffic; the rewrite passes only if it matches the corpus or the diff is approved row-by-row.
- **When-to:** Legacy rewrites, language ports (Python→Rust), library upgrades with behavior risk, "I don't trust the existing tests" situations.
- **When-NOT:** Greenfield code (no behavior to preserve), code with pervasive nondeterminism (need normalization first), tiny modules (just write unit tests).
- **Snippet:**

```python
# golden_master_test.py
import json, pathlib
from legacy import process
CORPUS = pathlib.Path("tests/golden/corpus.jsonl")

def test_golden_master():
    for line in CORPUS.read_text().splitlines():
        case = json.loads(line)
        assert process(**case["input"]) == case["expected"], case["id"]
```

---

## CAND-T11: self-healing-locator-with-audit

- **Category:** test-
- **Source:** https://testdino.com/blog/playwright-ai-ecosystem/ , https://www.browserstack.com/docs/automate/playwright/self-healing , https://medium.com/@Amr.sa/healwright-let-your-playwright-tests-heal-their-own-selectors-on-the-fly-d0178568f9bc
- **Status:** new
- **Why valuable:** Healer agents (Microsoft's reference benchmark: 75%+ success on selector-related failures via accessibility tree) cut maintenance ~33% in the first quarter. Critically, accessibility-tree-based healing (`Role: button, Name: Checkout`) is ~10× more stable than DOM-based healing (`div.checkout-btn-v3`). But auto-healing without an audit trail = silent test rot.
- **One-line rule:** Allow self-healing only when the new locator targets the same role+accessible-name; every heal must open a PR diff that a human approves before the next CI run consumes the healed selector.
- **When-to:** Large E2E suites (>200 tests), frequent UI churn, design-system migrations.
- **When-NOT:** High-stakes flows (payments, auth) where a wrong heal = wrong button = silent prod bug; small suites where human maintenance is cheaper.
- **Snippet:**

```typescript
// Healer rule
expect(page.getByRole('button', { name: /^Check ?out$/i })).toBeVisible();
// Heal only if new candidate has same role + name regex; emit
// healed-selectors.diff for review, fail CI if diff unreviewed.
```

---

## CAND-T12: faker-deterministic-property-stochastic

- **Category:** test-
- **Source:** https://arxiv.org/pdf/2401.17626 , https://hypothesis.readthedocs.io/ , https://www.tasman.ai/news/how-to-generate-fake-user-data-for-testing
- **Status:** new
- **Why valuable:** Two failure modes in 2026: (a) teams replace Faker with LLM data generation and tests become slow + flaky; (b) teams stay on Faker and never find edge cases. The right split: Faker for *deterministic seeded fixtures* (CI reproducibility), Hypothesis/`fast-check`/`proptest` for *stochastic shrinking* (edge-case discovery), LLMs only to *write the generator*, not to be the generator at runtime.
- **One-line rule:** Use Faker (seeded) for fixture data, property-based strategies for boundary/edge exploration, and an LLM-generated *generator function* (committed to the repo) for domain-specific synthetic data — never call an LLM during the test run itself.
- **When-to:** Any test that needs varied input — APIs, services, ORM, parsers.
- **When-NOT:** Inline test cases for a specific bug regression (just hard-code the input).
- **Snippet:**

```python
# Faker for fixtures
from faker import Faker
fake = Faker(); Faker.seed(42)
user = User(email=fake.email(), name=fake.name())

# Hypothesis for edges
from hypothesis import given, strategies as st
@given(st.emails())
def test_normalize_email_idempotent(e):
    assert normalize(normalize(e)) == normalize(e)
```

---

## Notes for the curator

- Strongest accept candidates (highest signal-to-noise for AI-augmented SDLC): **T02 property-based-claude**, **T03 mutation-as-agent-feedback**, **T04 consumer-contract-from-openapi**, **T11 self-healing-locator-with-audit**.
- T01 (TDD agent loop), T05 (codegen+refactor), T06 (visual AI diff) are well-trodden — accept if there's category quota.
- T09/T10 (snapshot intent / golden master) are *defensive* patterns specifically against AI rewrites — keep at least one.
- T07 (load from traffic) and T08 (BDD by LLM) are slightly more niche — defer if quota tight.
- T12 (faker + property + LLM-as-generator-author) is the cross-cutting test-data rule that prevents the common "LLM-at-runtime" anti-pattern.

## Sources

- https://red.anthropic.com/2026/property-based-testing/
- https://arxiv.org/abs/2510.09907
- https://hypothesis.readthedocs.io/en/latest/ghostwriter.html
- https://testdouble.com/insights/keep-your-coding-agent-on-task-with-mutation-testing
- https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/
- https://arxiv.org/abs/2501.12862
- https://docs.pact.io/ai_tools/pactflow-skill
- https://pactflow.io/blog/pactflow-mcp-server/
- https://pactflow.io/ai/
- https://playwright.dev/docs/codegen
- https://testdino.com/blog/playwright-ai-codegen/
- https://www.checklyhq.com/blog/generate-end-to-end-tests-with-ai-and-playwright/
- https://testdino.com/blog/playwright-ai-ecosystem/
- https://www.browserstack.com/docs/automate/playwright/self-healing
- https://medium.com/@Amr.sa/healwright-let-your-playwright-tests-heal-their-own-selectors-on-the-fly-d0178568f9bc
- https://www.chromatic.com/storybook
- https://percy.io/blog/ai-visual-testing-tools
- https://applitools.com/blog/test-your-components-where-you-build-with-the-applitools-storybook-addon/
- https://medium.com/@zilliz_learn/how-to-load-test-an-llm-api-with-gatling-9620fb1e0557
- https://www.vervali.com/blog/best-load-testing-tools-in-2026-definitive-guide-to-jmeter-gatling-k6-loadrunner-locust-blazemeter-neoload-artillery-and-more/
- https://www.humanizingwork.com/ai-for-better-bdd/
- https://medium.com/@bart.rosa/the-use-of-large-language-models-in-behavior-driven-development-example-using-gpt-4-and-gherkin-6f12f069610b
- https://arxiv.org/pdf/2403.14965
- https://selleo.com/blog/when-to-use-jest-snapshots
- https://news.ycombinator.com/item?id=46205015
- https://jestjs.io/docs/snapshot-testing
- https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/
- https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
- https://arxiv.org/pdf/2401.17626
