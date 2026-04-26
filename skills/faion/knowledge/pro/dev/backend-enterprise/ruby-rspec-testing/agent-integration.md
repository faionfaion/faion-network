# Agent Integration — RSpec Testing (Rails)

## When to use
- Rails apps where you want layered specs: model specs (validations, scopes), service/query specs (PORO), request specs (HTTP boundary), system specs (browser).
- TDD or red/green/refactor with LLM agents — RSpec's BDD syntax (`describe`/`context`/`it`) maps cleanly to agent prompts.
- Codebases enforcing coverage gates (`simplecov` ≥80% for services) — RSpec + factory_bot reach coverage with low boilerplate.
- Multi-developer teams where shared examples + shared contexts reduce duplication and keep agents from re-inventing helpers.
- Refactor-heavy phases — fast model + service specs are the safety net for agent edits.

## When NOT to use
- Greenfield Hanami / Roda / Sinatra apps where Rails conventions don't apply — `rails_helper` and Rails matchers don't exist.
- Pure CLI gems — RSpec is fine, but `rails_helper` is overkill; use `spec_helper` only.
- Codebases standardized on Minitest — mixing creates two test infrastructures, two CI shapes, two sets of helpers.
- Performance benchmarks — use `benchmark/ips`, not RSpec.
- Visual regression — use Percy/Chromatic via Capybara, but the value is in the visual-diff service, not RSpec itself.

## Where it fails / limitations
- **Slow suite drift.** Naïve `let!` + `before(:each)` patterns rebuild the world per spec; suite hits 10+ min after a few hundred specs.
- **Mock-heavy specs that pass when refactored wrong.** Agents stub everything; tests assert on stubs, not behavior. Mutation testing exposes.
- **`let` laziness traps.** `let(:user) { create(:user) }` not invoked unless referenced; agents debug "missing user" by sprinkling `let!` everywhere.
- **`context` overuse.** Deep nesting hides setup; agents copy the wrong `before` block.
- **Factory bloat.** Each spec creates its own factory traits; the next agent can't find them. Trait explosion.
- **Database cleaner mode mismatches.** `truncation` vs `transaction` vs `deletion` chosen per spec; Capybara JS driver needs `truncation`, others don't. Agents miss the rule and produce intermittent failures.
- **Time-dependent specs.** `Time.now` and `Date.today` flake under timezone shifts; agents forget `Timecop.freeze` / `ActiveSupport::Testing::TimeHelpers`.
- **VCR cassette drift.** Cassettes recorded against staging, replayed in CI, miss new fields; specs pass while integration is broken.
- **Shared contexts hide behavior.** A `shared_context "as admin"` mutates state in 8 ways; agent reading the spec sees only 1 line.
- **`should`-style matchers** mixed with `expect`-style — codebases end up bilingual. RSpec disabled `should` for new specs but legacy lingers.

## Agentic workflow
Drive RSpec work as: (1) a planner subagent identifies the SUT and emits the spec layout (describe/context/it); (2) a code-writer subagent generates the spec with minimal `let`s, explicit setup, and AAA structure; (3) a coverage subagent runs `bundle exec rspec` with `simplecov` and reports per-file gaps; (4) a perf subagent runs `bundle exec rspec --profile 10` and flags any spec >1s; (5) a mutation subagent runs `mutant` on the SUT and flags surviving mutations. Persist specs in `spec/<layer>/<sut>_spec.rb`; agents must mirror the source-tree structure or coverage grouping breaks.

### Recommended subagents
- `faion-backend-agent` (referenced in README frontmatter) — implementer for spec files.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs RSpec + Rubocop + simplecov threshold before task close.
- A purpose-built **rspec-coverage-agent** (worth creating): parses `coverage/.last_run.json`, returns per-file gaps with proposed `it "..."` blocks tied to uncovered branches.
- A **mutation-test-agent** (worth creating): runs `mutant` (or `mutest`) on changed files; flags surviving mutations as "tests pass when behavior breaks."
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub VCR cassettes, fixtures, and `secrets.test.yml` before commit (often contain real bearer tokens).

### Prompt pattern
Service spec scaffold:
```
You are a Rails 7.1 + RSpec engineer. Generate
spec/services/users/create_service_spec.rb covering
Users::CreateService#call:
1. Valid params → user persisted, welcome email enqueued, returns
   Success
2. Email taken → no user persisted, no email enqueued, returns
   Failure(:email_taken)
3. Invalid params (no email) → returns Failure with errors
Use factory_bot, ActiveJob::TestHelper, shoulda-matchers where
applicable. No `let!` unless required. Run:
bundle exec rspec spec/services/users/create_service_spec.rb.
```

Suite-perf triage:
```
Run `bundle exec rspec --profile 20`. For each spec >500ms,
identify cause: (a) DB hits in `before`, (b) full Capybara boot,
(c) external HTTP without VCR, (d) factory cascade. Output spec
file:line, root cause, proposed fix (e.g., build_stubbed instead
of create, mock external call, hoist factory to shared context).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bundle exec rspec` | Run specs | `gem 'rspec-rails'` |
| `bundle exec rspec --bisect` | Find order-dependent flake | bundled |
| `bundle exec rspec --profile N` | Top-N slowest specs | bundled |
| `simplecov` | Coverage with branch tracking | `gem 'simplecov'` |
| `factory_bot` | Test data factories | `gem 'factory_bot_rails'` |
| `shoulda-matchers` | Validation/association one-liners | `gem 'shoulda-matchers'` |
| `webmock` / `vcr` | HTTP stubbing/cassettes | `gem 'webmock'`, `gem 'vcr'` |
| `database_cleaner` | DB reset between specs | `gem 'database_cleaner-active_record'` |
| `timecop` / `ActiveSupport::Testing::TimeHelpers` | Time freezing | `gem 'timecop'` |
| `mutant` / `mutest` | Mutation testing | `gem 'mutant-rspec'` (commercial) / `mutest` (OSS) |
| `bullet` | N+1 detection inside spec runs | `gem 'bullet'` |
| `rspec-retry` | Retry flaky specs (use sparingly) | `gem 'rspec-retry'` |
| `parallel_tests` | Multi-process spec run | `gem 'parallel_tests'` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions / CircleCI / Buildkite | CI | yes | Parallelize via `parallel_tests` + matrix; agents handle config. |
| Codecov / Coveralls | SaaS coverage | API yes | Per-PR coverage diff. |
| BuildPulse / Flaky.io | SaaS flake detection | API yes | Detects flaky specs across runs; agents act on top offenders. |
| Cuprite (CDP-based Capybara) | OSS | yes | Faster, more stable than Selenium for system specs. |
| Knapsack Pro | SaaS | API yes | Dynamic test parallelization across CI nodes. |
| Sentry | SaaS errors | API yes | Tag releases by spec-suite version. |
| Percy / Chromatic | SaaS visual | API yes | Visual regression on system specs. |

## Templates & scripts
See `templates.md` for model/service spec skeletons. Add a CI gate combining coverage + flake + perf (≤50 lines):

```bash
#!/usr/bin/env bash
# rspec-gate.sh — fail PR on coverage drop, flake, or slow specs.
# Usage: rspec-gate.sh [COVERAGE_MIN] [SLOW_MS]
set -euo pipefail
COV_MIN="${1:-80}"
SLOW="${2:-1000}"
LOG=$(mktemp)
COVERAGE=true bundle exec rspec --profile 50 --format documentation \
  --format json --out /tmp/rspec.json 2>&1 | tee "$LOG"
ruby -rjson -e '
cov_min = ARGV[0].to_f
slow = ARGV[1].to_i
last = JSON.parse(File.read("coverage/.last_run.json")) rescue {}
cov = last.dig("result","line") || 0
fail_msgs = []
fail_msgs << "coverage #{cov}% < #{cov_min}%" if cov < cov_min
data = JSON.parse(File.read("/tmp/rspec.json"))
slow_specs = data["examples"].select { |e| (e["run_time"] * 1000).to_i > slow }
slow_specs.each { |e| puts "SLOW #{e["full_description"]} #{(e["run_time"]*1000).to_i}ms" }
flaky = data["examples"].count { |e| e["status"] == "pending" && e["pending_message"].to_s.include?("flak") }
fail_msgs << "#{flaky} known-flaky specs" if flaky > 0
fail_msgs << "#{slow_specs.size} specs >#{slow}ms" if slow_specs.size > 5
unless fail_msgs.empty?
  puts "FAIL: " + fail_msgs.join(" | "); exit 1
end
puts "OK: cov=#{cov}% slow=#{slow_specs.size}"
' "$COV_MIN" "$SLOW"
```

Wire into `.github/workflows/ci.yml` after specs run.

## Best practices
- **Prefer `build_stubbed` over `create` whenever possible.** No DB write; specs are 10-100x faster for model unit tests.
- **One `describe` per public method, `context` per branch, `it` per assertion.** Keeps failure messages diagnostic.
- **Avoid `let!` unless setup must run regardless of usage.** Lazy `let` is the default; eager triggers DB writes you don't need.
- **`subject` named** (`subject(:service)`); unnamed `subject` makes specs unreadable when nested.
- **Use `instance_double` not `double`.** Verifies the method actually exists on the SUT.
- **Mock at the boundary, not internals.** Mock the HTTP gateway, not the service that calls the gateway. Otherwise refactor breaks tests.
- **Use shared examples for cross-cutting behavior** (auth, pagination); use shared contexts for setup blocks. Don't mix.
- **Pin time via `ActiveSupport::Testing::TimeHelpers`** (Rails 5.2+). Avoid Timecop unless you need the legacy API.
- **System specs use Cuprite headless Chrome.** Selenium is the historical default — slower and flakier.
- **Run a quick `bundle exec rspec --bisect` after any flake.** Order-dependence is debt that compounds.
- **Mutation testing on critical services** (auth, billing). Coverage alone hides assertion-free specs.
- **Tag specs with metadata** (`:slow`, `:integration`, `:flaky_known`); CI selects subsets per stage.

## AI-agent gotchas
- **Stubbing the SUT.** Agent stubs the very method under test. Spec passes regardless. Force prompts to name what's mocked vs real explicitly.
- **`let` shadowing.** Inner `context` redefines `let(:user)`; outer specs silently use a different user. Lint via Rubocop-RSpec.
- **`expect { ... }.not_to change { ... }` with stubbed AR.** When `User.create!` is stubbed, change always evaluates to false; spec passes. Don't stub the writer you're verifying.
- **Database leak across specs.** Agent uses `:truncation` strategy in one spec, `:transaction` in another; one spec creates rows the next sees. Standardize per spec type via `RSpec.configure`.
- **`build_stubbed` confusion with associations.** `build_stubbed(:user, posts: [build_stubbed(:post)])` — `posts.count` queries DB → fails. Use `allow(user).to receive(:posts).and_return([post])` for associations.
- **VCR re-records on first run only.** Agent updates the API, runs spec, VCR replays old cassette — spec passes; integration broken. Periodically run `VCR_RECORD_MODE=all` and review diffs.
- **Capybara waits + `expect(page).to have_content`.** Agent uses `page.has_content?` (no wait) instead — flake guaranteed. Always `expect(...).to have_content`.
- **`travel_to` block omitted.** Agent calls `travel_to(future)` without `travel_back`; subsequent specs run with frozen time. Use the block form always.
- **Factory association cascade.** `create(:order)` creates a user, which creates a profile, which creates an avatar. 1 spec → 5 inserts. Use `build_stubbed` or factory traits without associations.
- **`before(:all)` vs `before(:each)` mistake.** Agent puts DB setup in `before(:all)`; subsequent transactional spec rolls back the setup. Spec fails on second run.
- **Shoulda-matchers on uncalled validators.** Agent writes `it { is_expected.to validate_uniqueness_of(:email) }` but the migration has no unique index; matcher passes regardless. Pair with a request spec hitting the constraint.
- **System specs not running JS by default.** Agent assumes `Capybara.default_driver = :selenium_chrome_headless`; missed metadata `:js => true`. Spec runs without JS, asserts on missing modal.
- **Mocking `Time.current` only.** Agent stubs `Time.current` but code uses `Time.zone.now`; spec passes, prod has wrong behavior.
- **Spec depending on factory sequence.** Agent asserts `expect(user.id).to eq(1)`; works locally, fails in parallel CI. Don't assert on auto-generated IDs.

## References
- RSpec docs. https://relishapp.com/rspec
- "Better Specs" — RSpec idiom guide. https://www.betterspecs.org
- Sam Phippen — "RSpec best practices" talks. https://samphippen.com
- thoughtbot — testing best practices. https://thoughtbot.com/blog/tags/testing
- factory_bot README. https://github.com/thoughtbot/factory_bot
- shoulda-matchers README. https://github.com/thoughtbot/shoulda-matchers
- VCR README. https://github.com/vcr/vcr
- Mutant docs. https://github.com/mbj/mutant
- Sibling methodologies in this repo: `pro/dev/backend-enterprise/ruby-rails/`, `pro/dev/backend-enterprise/ruby-rails-patterns/`, `pro/dev/backend-enterprise/ruby-activerecord/`, `pro/dev/backend-enterprise/decomposition-rails/`, `pro/dev/backend-enterprise/java-junit-testing/`.
