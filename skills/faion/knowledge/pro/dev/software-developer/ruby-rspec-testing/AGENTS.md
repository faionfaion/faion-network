---
slug: ruby-rspec-testing
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Structure RSpec specs with describe/context/it BDD style, factory_bot for fixtures, request specs for HTTP, isolated unit specs for services, and shared_examples for cross-class invariants.
content_id: "a0ec287be4d0c6e1"
complexity: medium
produces: code
est_tokens: 5200
tags: [rspec, ruby, testing, tdd, rails]
---
# RSpec Testing Patterns

## Summary

**One-sentence:** Structure RSpec specs with describe/context/it BDD style, factory_bot for fixtures, request specs for HTTP, isolated unit specs for services, and shared_examples for cross-class invariants.

**One-paragraph:** RSpec is the Ruby BDD testing framework. Effective use: describe the SUT, context for variant conditions, it for behavior; factory_bot.build_stubbed for unit specs (no DB), factory_bot.create for integration; request specs for HTTP behavior; isolated unit specs (without rails_helper) for services; shared_examples for cross-class invariants. Avoid letting tests grow database-coupled; prefer in-memory builds where possible.

**Ефективно для:**

- Rails 7/8 проєкти з RSpec як test framework.
- Сервіси, що мають ізольовані unit specs (без Rails boot).
- Інтеграційні request specs для HTTP behavior.
- Refactor old TestUnit-style або minitest проєктів у RSpec idiom.

## Applies If (ALL must hold)

- Rails 7+ project with rspec-rails + factory_bot installed.
- Tests run in CI on every push.
- Suite size justifies investment in shared_examples + custom matchers.
- Team writes specs in TDD/BDD style (not after-the-fact).

## Skip If (ANY kills it)

- Project uses minitest exclusively — different idiom.
- Suite under 50 specs — overhead > benefit.
- Throwaway scripts.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Subject under test | Ruby class | developer |
| Factories | spec/factories/*.rb | fixtures |
| spec_helper + rails_helper | config files | repo |

## Assumes Loaded

none — methodology is self-contained.

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: describe-context-it, factory-bot-build-stubbed-default, isolated-service-specs, shared-examples-for-invariants, no-let-bang-when-not-needed | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | sonnet | Templated describe/context/it. |
| `design-cases` | opus | Identifying meaningful variants is judgment. |
| `lint-create-overuse` | haiku | Mechanical grep. |

## Templates

| File | Purpose |
|------|---------|
| `templates/place_order_service_spec.rb` | Isolated RSpec service spec (spec_helper only) |
| `templates/shared_examples_auditable.rb` | Shared examples for the 'auditable' invariant across models |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rspec-testing.py` | Validate the spec artefact against the schema | Pre-commit + CI |

## Related

- [[ruby-rails]]
- [[ruby-rails-patterns]]
- [[php-phpunit-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
