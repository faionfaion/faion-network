# Ruby Sorbet Strict Floor with Tapioca RBI

## Summary

For any Ruby file an AI agent is allowed to modify autonomously, declare `# typed: true` (or stricter), generate Tapioca RBIs for every gem and Rails DSL, and require `bundle exec srb tc` plus `bundle exec tapioca check-shims` to pass before a PR is opened. Sorbet's typecheck becomes the deterministic refusal channel: agent-hallucinated method calls and wrong arities fail at compile-equivalent time, not at runtime in production.

## Why

Ruby is dynamic enough that LLMs reliably invent methods (`User.find_by_email_and_active`), wrong scopes, or non-existent association names. Sorbet — built by Shopify specifically for very large Ruby codebases — gives Ruby a real static type system. Tapioca closes the metaprogramming gap by runtime-introspecting Rails DSLs (`has_many`, `scope`, `belongs_to`, ActiveRecord columns) and emitting static RBIs Sorbet can read. With `# typed: strict` on a file, Sorbet refuses untyped methods, `T.untyped` returns, and missing nilability — exactly the shapes agents emit when guessing. The combined gate (`srb tc` + `tapioca check-shims`) makes "tests are green but the call doesn't exist" structurally impossible.

## When To Use

- Rails monoliths over ~50 KLOC where agents author non-trivial PRs.
- Multi-team Ruby orgs where a shared type contract reduces cross-team breakage.
- Any gem or service consumed by other internal projects (RBI doubles as the consumer-facing type spec).
- Codebases ratcheting strictness: start at `# typed: false` baseline, promote files to `true` then `strict` per PR.

## When NOT To Use

- Toy gems, single-file Sinatra services, and one-off scripts — Sorbet bootstrap and Tapioca regen costs exceed the value.
- Spike or exploratory branches where the file shape is intentionally fluid.
- Codebases pinned to Ruby below 3.0 — Sorbet's runtime requires 3.0+ for current versions.

## Content

| File | What's inside |
|------|---------------|
| `content/01-strict-typed-floor.xml` | `# typed: strict` rule, agent pre-flight commands, refusal mechanic. |
| `content/02-tapioca-rbi-pipeline.xml` | Tapioca DSL/gem RBI generation, `check-shims` discipline, baseline strategy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sorbet-config` | `sorbet/config` with strict path includes and ignore list. |
| `templates/tapioca.yml` | Tapioca config for DSL compilers, gem RBIs, and shim verification. |
