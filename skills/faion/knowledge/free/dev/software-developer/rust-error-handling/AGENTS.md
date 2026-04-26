# Rust Error Handling

## Summary

Rust error handling uses Result&lt;T, E&gt; for fallible operations, Option&lt;T&gt; for optional values, and the ? operator for ergonomic propagation. Use thiserror for library error types and anyhow for application-level errors. Never .unwrap() in production code — propagate with ? or handle explicitly.

## Why

Rust has no exceptions. Unhandled errors that would panic in production are a design failure. The ? operator makes propagation as ergonomic as throwing, while preserving explicit, type-checked error contracts. thiserror generates boilerplate-free Display/Error impls. anyhow adds context at the application layer without requiring typed errors everywhere.

## When To Use

- All Rust projects — this is the idiomatic approach, not an option.
- Functions that can fail for expected reasons (I/O, parsing, network).
- API design with clear, typed error contracts for callers.
- Library development where callers need to match on specific errors.
- Async code with tokio where errors flow across await boundaries.

## When NOT To Use

- .unwrap()/.expect() in tests — acceptable there, not in production code.
- Unrecoverable programming errors (out-of-bounds index access) — panic is correct.
- Prototype/throwaway code — anyhow with ? is acceptable without custom types.

## Content

| File | What's inside |
|------|---------------|
| `content/01-result-option-basics.xml` | Result and Option fundamentals, ? propagation, conversions between them. |
| `content/02-custom-errors.xml` | Manual error enum with Display/Error impl, From conversions, thiserror macros. |
| `content/03-anyhow-and-combinators.xml` | anyhow for applications, context/bail macros, Result/Option combinators, async error handling. |
| `content/04-antipatterns.xml` | Unwrap in production, ignoring errors, stringly-typed errors, panic vs Result. |

## Templates

none
