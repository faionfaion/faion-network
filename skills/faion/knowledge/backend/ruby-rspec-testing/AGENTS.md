# RSpec Testing for Rails Applications

## Summary

**One-sentence:** Produces a layered RSpec test plan + skeleton (model / service / request / system specs) with factory_bot, shoulda-matchers, SimpleCov branch coverage gates and one-behaviour-per-it discipline.

**Ефективно для:**

- Rails apps with layered behaviour (models + PORO services + REST endpoints).
- TDD / red-green-refactor cycles driven by LLM agents.
- Coverage gates ≥80% per service (SimpleCov branch).
- Multi-developer teams using shared examples / shared contexts.
- Refactor-heavy phases where fast model+service specs are the safety net.

**One-paragraph:** Layered RSpec strategy: model specs test validations and scopes; service specs test business logic; request specs test HTTP contracts; system specs test browser behaviour. Uses factory_bot for data, shoulda-matchers for one-liners, SimpleCov branch tracking for uncovered paths. BDD `describe/context/it` enforces one behaviour per block and makes failure messages diagnostic.

## Applies If (ALL must hold)

- Rails app with layered behavior: models with validations, PORO services, REST endpoints.
- TDD or red/green/refactor cycles with LLM agents — RSpec DSL maps to agent prompts well.
- Codebases enforcing coverage gates (simplecov ≥80% for services).
- Multi-developer teams using shared examples and shared contexts to reduce duplication.
- Refactor-heavy phases where fast model + service specs are the safety net.

## Skip If (ANY kills it)

- Greenfield Hanami/Roda/Sinatra apps — rails_helper and Rails matchers do not apply.
- Pure CLI gems — spec_helper only; rails_helper is overkill.
- Codebases standardized on Minitest — mixing creates two test infrastructures.
- Performance benchmarks — use benchmark/ips, not RSpec.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Rails app skeleton | directory | team |
| RSpec + factory_bot Gemfile entries | Gemfile lines | team |
| SimpleCov coverage thresholds | .simplecov | team |
| Spec layer matrix (model/service/request/system) | decision doc | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[ruby-rails]]` | host framework conventions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-spec-layer` | haiku | Maps method shape to model/service/request/system. |
| `draft-specs` | sonnet | Light judgment: matchers + subject naming + factories. |
| `review-spec-quality` | sonnet | Audits stub-the-SUT, let-shadow, factory cascade. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ruby-rspec-testing.json` | JSON Schema for the RSpec Testing for Rails Applications output contract |
| `templates/ruby-rspec-testing.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a ruby-rspec-testing record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rspec-testing.py` | Enforce the RSpec Testing for Rails Applications output contract | After subagent returns, before downstream consumer reads |

## Related

- [[ruby-rails]]
- [[ruby-rails-patterns]]
- [[ruby-activerecord]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
