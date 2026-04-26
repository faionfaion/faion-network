# RSpec Testing (Rails)

## Summary

Layered RSpec testing strategy for Rails applications: model specs (validations, scopes), service/PORO specs, request specs (HTTP boundary), and system specs (browser). Uses factory_bot, shoulda-matchers, and SimpleCov to achieve coverage gates with minimal boilerplate. BDD syntax (`describe`/`context`/`it`) maps cleanly to agent prompts and produces self-documenting failure output.

## Why

RSpec's BDD structure enforces a single behavior per `it` block, making failure messages diagnostic without reading the test body. `build_stubbed` eliminates DB writes for model unit tests (10-100x faster). Layer isolation — model specs test validations, service specs test business logic, request specs test HTTP contracts — means agent edits to one layer do not invalidate tests for another. SimpleCov branch tracking finds uncovered conditional paths that line coverage misses.

## When To Use

- Rails app with layered behavior: models with validations, PORO services, REST endpoints.
- TDD or red/green/refactor cycles with LLM agents — RSpec DSL maps to agent prompts well.
- Codebases enforcing coverage gates (`simplecov` >=80% for services).
- Multi-developer teams using shared examples and shared contexts to reduce duplication.
- Refactor-heavy phases where fast model + service specs are the safety net.

## When NOT To Use

- Greenfield Hanami/Roda/Sinatra apps — `rails_helper` and Rails matchers don't apply.
- Pure CLI gems — `spec_helper` only; `rails_helper` is overkill.
- Codebases standardized on Minitest — mixing creates two test infrastructures.
- Performance benchmarks — use `benchmark/ips`, not RSpec.
- Visual regression — that value comes from the visual-diff service (Percy/Chromatic), not RSpec itself.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Naming, one-assert-per-it, `build_stubbed` preference, database cleaner strategy. |
| `content/02-examples.xml` | Model spec with shoulda-matchers, service spec with factory_bot, request spec outline. |
| `content/03-antipatterns.xml` | `let` laziness traps, mock-heavy specs, `before(:all)` vs `before(:each)` confusion. |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-spec.rb` | RSpec model skeleton with shoulda-matchers validations and scope examples. |
| `templates/service-spec.rb` | Service spec skeleton with `described_class`, `subject`, factory_bot, AAA structure. |
| `templates/rspec-gate.sh` | CI script: check SimpleCov threshold, flag slow specs, report flaky count. |
