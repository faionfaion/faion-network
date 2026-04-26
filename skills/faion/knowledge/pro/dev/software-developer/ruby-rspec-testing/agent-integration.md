# Agent Integration — RSpec Testing (Rails)

## When to use
- Backfilling tests on a Rails monolith that has shipped without sufficient model/controller/service coverage.
- Driving TDD on a new Rails app where RSpec + FactoryBot + Shoulda Matchers + Capybara is the team standard.
- Standardizing a mixed Minitest/RSpec codebase to a single style; or generating RSpec specs from existing fixtures.
- Adding request specs to lock down API contracts before a controller refactor or migration to GraphQL.
- Writing service-object specs for Trailblazer / Interactor / dry-monads-style command objects extracted from fat controllers.
- Generating system / feature specs with Capybara + Selenium / Cuprite for happy-path regression coverage.

## When NOT to use
- Sinatra / Roda apps, gems with no Rails dependency — drop the `rails_helper`, use plain RSpec or Minitest.
- Performance-sensitive Ruby microservices where startup tax of `rails_helper` (>3s) breaks CI throughput. Consider Minitest or `rspec` without `rails_helper`.
- Codebases standardized on Minitest / Test::Unit — don't impose RSpec.
- Jobs / mailers heavy on third-party APIs without a contract layer — mocks in RSpec drift; use VCR + Pact.
- Throwaway prototypes / Hanami / dry-system experiments where Shoulda Matchers / FactoryBot don't apply.

## Where it fails / limitations
- **`should` syntax everywhere.** Pre-RSpec-3 idioms (`it { should validate_presence_of(:email) }`) still ship in tutorials. RSpec 3+ prefers `is_expected.to`. Agents trained on stale data emit deprecated form.
- **Shoulda Matchers does not cover all validations.** Conditional validations, custom validators, model callbacks need explicit specs; matchers create false confidence.
- **`let!` evaluation order vs. `before`.** Order matters for state setup; agents mix idioms and produce flaky tests.
- **`build_stubbed` vs. `create` confusion.** Tests use `create` everywhere → CI grinds. `build_stubbed` is faster but does not run callbacks; agents pick the wrong tool.
- **DatabaseCleaner / transactional fixtures.** `DatabaseCleaner` strategy choice (`transaction` vs. `truncation`) interacts with Capybara JS drivers in painful ways; agents rarely diagnose this.
- **System spec flake.** Capybara + Selenium / Chrome headless tests are inherently flaky on CI; without `Capybara.default_max_wait_time` tuning + `wait_for_ajax` helpers, suite is unreliable.
- **`request` vs. `controller` specs.** Rails 5+ deprecated `assigns` / `assert_template`; agents emit `controller specs` with old API. Always prefer `request` specs.
- **VCR cassette drift.** Agents add `VCR.use_cassette` blocks but never re-record; tests pass on stale fixtures while production behavior changes. No automatic invalidation.

## Agentic workflow
Drive RSpec scaffolding as a four-stage pipeline: (1) a slice agent reads the class under test (model/controller/service/job/mailer) and picks the right spec type with the right helper requires; (2) a spec-gen agent emits `describe`/`context`/`it` blocks with `is_expected.to` matchers, FactoryBot factories, and Shoulda matchers where applicable; (3) a flake hunter runs new specs in random order with `--seed` rotation and `rspec-retry` disabled to surface flakes; (4) a fixture-cleanup agent prunes orphaned `let`/`before` setups and merges duplicate factories. Use `faion-sdd-executor-agent` to drive one spec per SDD task; tests must run green before close.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — opus model fits because Rails spec design (request vs. system, mock vs. VCR) is decision-heavy.
- `faion-feature-executor` skill — sequential mode: model spec → service spec → request spec → system spec, gating on green at each step.
- A purpose-built **rspec-style-lint agent** (worth adding under `agents/`): linter on top of `rubocop-rspec` for the README's preferred idioms (`is_expected.to`, no `should`, no `controller` specs, `build_stubbed` over `create` where possible).
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before committing VCR cassettes; cassettes leak API keys, bearer tokens, and PII into git. Mandatory.
- For factory hygiene, pair with sibling `pro/dev/testing-developer/property-based-testing/` if it exists and use `rantly` / `prop_check` for input fuzzing.

### Prompt pattern
Spec generation:
```
You are writing RSpec 3.13 specs for a Rails 7.1 application using
FactoryBot, Shoulda Matchers, and rspec-rails. Given the class:
- ActiveRecord model: write `spec/models/<name>_spec.rb` with describe
  blocks for validations (Shoulda), associations (Shoulda), scopes,
  and instance methods. Use `is_expected.to`, never `should`.
- Service object / Interactor: write `spec/services/<name>_spec.rb`
  with `describe '#call'` + `context` per branch. Use FactoryBot
  `build_stubbed` unless DB persistence is required.
- Controller: write a REQUEST spec at `spec/requests/<resource>_spec.rb`
  with `get/post/put/delete` + `expect(response).to have_http_status`.
  Never use controller specs; never use `assigns`.
- Background job: write `spec/jobs/<name>_spec.rb` with
  `have_enqueued_job` matcher and `perform_now` for behavior.
- Mailer: `spec/mailers/<name>_spec.rb` with `have_been_made` /
  ActionMailer::Base.deliveries.
- Each example one assertion focus. Name with `describe '#method'` /
  `context 'when X'` / `it 'does Y'`.
```

Anti-pattern review:
```
You are reviewing a PR adding RSpec specs. Flag any of:
(1) controller spec with `assigns(:user)` / `assert_template` (deprecated),
(2) `should` syntax instead of `is_expected.to`,
(3) `create` used where `build_stubbed` would suffice (no DB needed),
(4) `Time.now` / `Date.today` in spec body (use travel_to / Timecop),
(5) VCR.use_cassette without record: :none — cassette can re-record
   silently in CI,
(6) any `sleep` in a system spec (use have_content / have_selector
   with default wait),
(7) factories defined inside spec files instead of spec/factories/.
Cite file:line. Do not propose fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rspec` | Test runner | `bundle exec rspec` ; https://rspec.info |
| `rspec-rails` | Rails integration generators | https://github.com/rspec/rspec-rails |
| `factory_bot_rails` | Test factories | https://github.com/thoughtbot/factory_bot_rails |
| `shoulda-matchers` | Built-in matchers for AR validations / associations | https://matchers.shoulda.io |
| `capybara` + `selenium-webdriver` / `cuprite` | System / feature specs | https://teamcapybara.github.io/capybara |
| `rubocop` + `rubocop-rspec` | Style + RSpec idiom enforcement | https://rubocop.org |
| `simplecov` | Coverage reports | https://github.com/simplecov-ruby/simplecov |
| `vcr` + `webmock` | HTTP request recording / blocking | https://github.com/vcr/vcr |
| `rspec-retry` | Auto-retry flaky specs (use sparingly) | https://github.com/NoRedInk/rspec-retry |
| `parallel_tests` | Multi-process test runner; CPU-bound CI speedup | https://github.com/grosser/parallel_tests |
| `database_cleaner-active_record` | DB cleanup strategies for non-transactional tests | https://github.com/DatabaseCleaner/database_cleaner-active_record |
| `mutant` / `mutant-rspec` | Mutation testing | https://github.com/mbj/mutant |
| `bullet` | N+1 detection during tests | https://github.com/flyerhzm/bullet |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions / Buildkite / CircleCI | SaaS | yes | All have first-class RSpec + parallel_tests support. |
| Codecov / Coveralls / SimpleCov-LCOV | SaaS | yes | Coverage reporting + PR comments. |
| Knapsack Pro | SaaS | yes | Dynamic test splitting across CI nodes; major savings on big suites. |
| Heroku CI | SaaS | yes | Native RSpec runner; pairs with Heroku Postgres for IT. |
| Sauce Labs / BrowserStack | SaaS | yes | Browsers for system specs running on Capybara + Selenium. |
| Percy / Chromatic | SaaS | yes | Visual regression on system specs. |
| WireMock / VCR / Pact | OSS | yes | HTTP test doubles + contract testing. |
| LocalStack | OSS | yes | AWS service emulation for IT. |
| TestRail / Allure | SaaS / OSS | yes | Reporting layer over RSpec runs. |
| `factory_bot` consult ENVs | OSS | yes | Factories support inheritance; agents tend to flatten — hold the line. |

## Templates & scripts

The methodology already ships model/service/request spec templates in `README.md` and `templates.md`. Gap: a quick lint that enforces the README's preferred idioms (request over controller specs, `is_expected.to`, factory placement). Inline drop-in (≤50 lines) — `scripts/rspec-style-lint.sh`:

```bash
#!/usr/bin/env bash
# rspec-style-lint.sh — enforce README idioms beyond rubocop-rspec.
# Usage: rspec-style-lint.sh <project-root>
set -euo pipefail
root="${1:?usage: rspec-style-lint.sh PROJECT_ROOT}"
fail=0
echo "# RSpec style lint ($root)"

echo "## Controller specs (deprecated — use request specs)"
find "$root/spec/controllers" -name '*_spec.rb' 2>/dev/null \
  | tee /tmp/rs.ctrl || true
[[ -s /tmp/rs.ctrl ]] && fail=1

echo "## Legacy 'should' syntax"
grep -rEn '\bit\s*\{\s*should\b' "$root/spec" --include='*.rb' \
  | tee /tmp/rs.should || true
[[ -s /tmp/rs.should ]] && fail=1

echo "## assigns / assert_template usage"
grep -rEn '\bassigns\(|\bassert_template\b' "$root/spec" --include='*.rb' \
  | tee /tmp/rs.assigns || true
[[ -s /tmp/rs.assigns ]] && fail=1

echo "## Factories defined inside spec files (move to spec/factories/)"
grep -rEn '^\s*FactoryBot\.define\b' "$root/spec" --include='*_spec.rb' \
  | tee /tmp/rs.inline-fac || true
[[ -s /tmp/rs.inline-fac ]] && fail=1

echo "## sleep in system specs (use Capybara wait)"
grep -rEn '^\s*sleep\b' "$root/spec/system" "$root/spec/features" 2>/dev/null --include='*.rb' \
  | tee /tmp/rs.sleep || true
[[ -s /tmp/rs.sleep ]] && fail=1

echo "## VCR cassettes without record: :none"
grep -rEn 'use_cassette' "$root/spec" --include='*.rb' \
  | grep -v 'record: :none' \
  | tee /tmp/rs.vcr || true
[[ -s /tmp/rs.vcr ]] && fail=1

exit "$fail"
```

Wire into pre-commit (`overcommit` / `lefthook`) or CI.

## Best practices
- **`is_expected.to` over `should`.** Modern RSpec syntax; enforce via `rubocop-rspec` rule `RSpec/ImplicitExpect: is_expected`.
- **Request specs, not controller specs.** Rails 5+ deprecated `assigns`. Request specs exercise routes + middleware + auth. README correctly uses request specs in `templates.md`.
- **`build_stubbed` first, `build` second, `create` last.** Stubbed: no DB, fast, fine for most model/service tests. Persisted: only when the test requires it.
- **Factories under `spec/factories/`, never inline.** One file per model. Use `traits` for variations, not nested factories.
- **`travel_to` for time-dependent code.** ActiveSupport ships it; no need for `Timecop` unless project already uses it. Reset with `travel_back` in `after`.
- **System specs with Cuprite, not Selenium.** Cuprite (Ferrum/CDP) is faster, no driver bin headache. https://github.com/rubycdp/cuprite
- **VCR cassettes with `record: :none` in CI.** New cassettes are a human action (`record: :new_episodes` locally → commit), never silent.
- **`parallel_tests` for >2-min suites.** 4–8x speedup on multi-core CI for free.
- **`bullet` in spec env.** Surface N+1 queries during the test run; agents emit eager-loading once warned.
- **Coverage gate via `simplecov` ratchet.** Never below current; raise floor over time.
- **Mutation testing (`mutant`) on critical paths.** Domain calculation services / money handlers; PRs that don't kill new mutants need human review.
- **Avoid `let!` unless side-effect setup.** Lazy `let` keeps specs fast; eager `let!` runs even for skipped contexts.
- **Cleanup strategy: transactional for non-JS, truncation for system specs.** DatabaseCleaner config in `rails_helper.rb` must distinguish.

## AI-agent gotchas
- **Stale RSpec idioms.** Agents emit `it { should validate_presence_of(:email) }`, `RSpec.configure` with deprecated config keys, controller specs with `assigns`. Pin RSpec + Rails versions in the prompt.
- **`create` everywhere.** Agents reach for `create(:user)` even when `build_stubbed` works, multiplying CI time. Force the rule: "if test does not query DB, use build_stubbed".
- **Hidden test order coupling.** Agents share state via instance vars (`@user = create(:user)` in `before(:all)`). RSpec random order surfaces it; force `--order random` in `.rspec`.
- **`Time.current` / `DateTime.now` baked in.** Agents hard-code timestamps in specs; tests fail on Feb 29 or DST. Force `travel_to(Time.zone.local(...))`.
- **VCR drift.** Agents add `VCR.use_cassette('foo')` and never re-record. Cassettes encode API behavior at moment-of-record forever. Force `record: :none` + an annual re-record review.
- **System spec flake from Capybara waits.** Agents add `sleep 1` or `wait_for_ajax`. Use Capybara's matchers (`have_content`, `have_selector`) which auto-wait.
- **Controller specs reflex.** Agents trained on Rails 4 era emit controller specs. Reject in review.
- **Inline factories.** Agents define `FactoryBot.define { factory :user do ... end }` inside the spec file. Move to `spec/factories/`.
- **Mocking what you don't own.** `allow_any_instance_of(HTTP::Client)` mocks the lib, not the boundary. Force a `RemoteService` wrapper class and stub that.
- **Coverage chasing.** Asked to "raise coverage", agents write tests that call methods and assert nothing. Use mutation testing as the gate, not lines.
- **Test names that re-state the code.** "it returns true if condition is true". Force describe-it style: `describe '#admin?' / context 'when role is admin' / it 'returns true'`.
- **DatabaseCleaner thrash.** Agents add `DatabaseCleaner.strategy = :truncation` globally and CI doubles. Use `:transaction` by default; only switch for JS-driven system specs.
- **Human-in-the-loop on flaky disable.** Agents `skip` flaky specs to make CI green. Disabled tests must be reviewed by a human within 24h.

## References
- RSpec docs — https://relishapp.com/rspec
- Better Specs — https://www.betterspecs.org (canonical idiom guide)
- thoughtbot — Factory Bot Best Practices. https://thoughtbot.com/blog/tags/factorybot
- Shoulda Matchers — https://matchers.shoulda.io
- Capybara — https://teamcapybara.github.io/capybara
- Cuprite (CDP driver) — https://github.com/rubycdp/cuprite
- Mutant — https://github.com/mbj/mutant
- VCR — https://github.com/vcr/vcr
- Rails Testing Guide — https://guides.rubyonrails.org/testing.html
- Knapsack Pro — Test splitting. https://knapsackpro.com
- Sibling methodologies in this repo: `pro/dev/software-developer/ruby-rails/`, `ruby-rails-patterns/`, `ruby-activerecord/`, `ruby-sidekiq-jobs/`, `php-phpunit-testing/`, `java-junit-testing/`.
