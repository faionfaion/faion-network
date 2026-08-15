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
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source | ~1200 |
| `content/02-output-contract.xml` | essential | artefact JSON Schema + spec-file contract + forbidden spec shapes | ~1400 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns with symptom / root-cause / fix | ~1400 |
| `content/04-procedure.xml` | essential | 5-step artefact procedure + 5-step spec-authoring sub-procedure | ~1400 |
| `content/05-examples.xml` | recommended | two end-to-end worked examples | ~1000 |
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
| `templates/model-spec.rb` | Model spec skeleton: validations, scopes, shoulda-matchers one-liners |
| `templates/service-spec.rb` | Service spec skeleton with named subject and instance_double collaborators |
| `templates/place_order_service_spec.rb` | Fully worked isolated service spec (spec_helper only, three contexts) |
| `templates/shared_examples_auditable.rb` | `shared_examples_for "auditable"` — the cross-class invariant pattern |
| `templates/rspec-gate.sh` | CI gate: runs the suite with SimpleCov thresholds and `--profile` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ruby-rspec-testing.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/ruby-rspec-testing.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^rspec\\-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
