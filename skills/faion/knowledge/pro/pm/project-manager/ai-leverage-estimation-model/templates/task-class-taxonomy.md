<!-- purpose: Six-class taxonomy used by ai-leverage-estimation-model to bucket leaf tasks -->
<!-- consumes: WBS leaves -->
<!-- produces: per-leaf task_class assignment for the leverage estimate -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400 tokens when loaded -->

# Task-class taxonomy

## glue

CRUD, API wiring, config plumbing, type definitions, simple data mapping. Highly templated. Typical observed multiplier band: 2.0x - 4.0x.

Boundary: if the task requires non-trivial domain rules, it is `business-logic`, not glue.

## scaffold

New project setup, framework boilerplate, build configuration, deploy pipelines, dependency wiring. Typical band: 2.5x - 5.0x.

Boundary: if scaffolding is for a regulated stack with mandatory audit hooks, it is `regulated`.

## tests

Unit tests, integration tests, fixtures, mocks, snapshot baselines for known code. Typical band: 2.0x - 3.5x.

Boundary: property-based testing of a novel algorithm is `novel`, not tests.

## business-logic

Domain rules, pricing engines, eligibility checks, workflow state machines. Requires correctness, not just shape. Typical band: 1.5x - 2.5x.

Boundary: if domain is regulated (HIPAA, SOX, GDPR processing rules), promote to `regulated`.

## regulated

Code with statutory or contractual correctness requirements: healthcare, finance, identity, payments, audit logging. Typical band: 1.0x - 1.5x.

Boundary: even when AI accelerates draft, the validation and review overhead dominates; multipliers stay close to 1.

## novel

First-of-kind algorithms, formal verification, research-grade work, problems with no AI training data. Typical band: 1.0x - 1.2x.

Boundary: do not assign `novel` unless the operator can show no comparable problem in their throughput log.
