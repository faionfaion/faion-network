# Ruby on Rails Framework Fundamentals

## Summary

**One-sentence:** Use Rails 7/8 idioms: convention over configuration, RESTful routing, Strong Parameters, callbacks, concerns for shared logic, and config-environment isolation.

**One-paragraph:** Rails is opinionated; fighting conventions costs months. Adopt the patterns: RESTful resourceful routing (resources :orders), Strong Parameters for mass-assign safety, model callbacks only for invariants (not external side effects), concerns for ≥2-model shared logic, generators for scaffolding, credentials.yml for secrets, and environment-isolated config. Mixing Sinatra-style ad-hoc routes or skipping Strong Parameters defeats Rails' security posture.

**Ефективно для:**

- Greenfield Rails 7/8 проєкти — задати ідіоматичну structure.
- Refactor non-RESTful routes у resources + member/collection convention.
- Migration від config-soup до credentials.yml + environment-specific config.
- Onboarding нових Ruby-devs — methodology як reading list + conventions.

## Applies If (ALL must hold)

- Rails 7+ project (Hotwire-aware).
- Application serves HTML and/or JSON.
- Team commits to Rails conventions (vs Sinatra ad-hoc style).
- Strong Parameters enabled (Rails default).

## Skip If (ANY kills it)

- Rails API-only mode with separate FE — no Hotwire/Turbo; methodology applies but skip view-layer rules.
- Project standardized on Hanami/Roda instead of Rails — different framework.
- Trivial app — convention overhead > benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource definition | Ruby class + table | domain |
| Routes file | config/routes.rb | repo |
| Credentials | config/credentials.yml.enc + master key | ops |

## Assumes Loaded

none — methodology is self-contained.

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: restful-resources, strong-parameters, credentials-not-env, concern-for-shared-multi-model, callback-only-for-invariants | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `refactor-routes` | sonnet | Mechanical grouping by resource. |
| `decide-callback-vs-service` | opus | Distinguishing invariant vs side effect is judgment. |
| `lint-strong-params` | haiku | Mechanical regex. |

## Templates

| File | Purpose |
|------|---------|
| `templates/routes.rb` | RESTful routes with member/collection convention |
| `templates/orders_controller.rb` | RESTful controller with Strong Parameters + Pundit authorization |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-rails.py` | Validate the Rails module artefact against the schema | Pre-commit + CI |

## Related

- [[ruby-rails-patterns]]
- [[ruby-activerecord]]
- [[ruby-rspec-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
