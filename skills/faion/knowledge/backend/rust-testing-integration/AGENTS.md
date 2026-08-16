# Rust Integration Testing — Axum/Tower and Testcontainers

## Summary

**One-sentence:** Produces Rust integration tests that drive the real Axum/Actix router via tower::ServiceExt::oneshot, isolate DB state via testcontainers + per-test schema, and snapshot output with insta.

**One-paragraph:** Integration tests drive the real router in-process via tower::ServiceExt::oneshot — no listener, no port races. Database tests use testcontainers-rs with per-test schema isolation (CREATE SCHEMA test_<uuid>) or transaction-rollback wrappers so parallel runs never leak state. Snapshot output uses insta to avoid noisy diffs and migrations run inside test setup.

**Ефективно для:**

- Axum/Actix/Tonic — драйв router через `oneshot`, без `bind(:0)`-race.
- Постгрес у тесті — `testcontainers` + per-test schema або transaction rollback.
- Великий JSON/HTML output — `insta` snapshot замість 50-рядкових `assert_eq!`.
- Перевірка міграцій у CI — `sqlx migrate run` всередині setup.

## Applies If (ALL must hold)

- Rust service on Axum/Actix/Tonic where router + middleware + DB must be tested together.
- Handler reads/writes a database; mocks would just assert the mock setup.
- Pagination/filtering/ordering logic requires real SQL execution.
- Multiple components interact and unit-level boundaries miss the integration bug.

## Skip If (ANY kills it)

- Pure business logic with no I/O — unit test with mockall is cheaper.
- Benchmarks — use criterion, not cargo test.
- Cross-compile targets where running on the host is unrepresentative.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Axum/Actix application | Rust crate | service repo |
| Migrations directory | SQL files | `migrations/` |
| testcontainers-rs dev-dep | Cargo dependency | `Cargo.toml` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[rust-testing-unit]] | Defines colocated unit-test placement; integration tests live in tests/ and must not collide |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-test-module` | sonnet | Author the tests/ module with router setup + container fixture. |
| `write-snapshot-assertions` | sonnet | insta snapshot lookup + descriptive name. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/integration_test.rs` | Rust integration test skeleton: oneshot + testcontainers + insta. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-testing-integration.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rust-testing-unit]]
- [[rust-testing-ci-toolchain]]
- [[rust-testing-property]]

## Decision tree

See `content/06-decision-tree.xml`. Tree picks unit vs integration-with-mock vs integration-with-testcontainers based on whether the SUT touches I/O and what state isolation is feasible.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/integration_test.rs`

```rust
use axum::body::Body;
use axum::http::{Request, StatusCode};
use tower::ServiceExt;

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn it_returns_user_on_get_users_id() {
    let app = my_app::build_router(test_db_pool().await).await;
    let resp = app
        .oneshot(
            Request::builder()
                .uri("/users/1")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .expect("router should respond");
    assert_eq!(resp.status(), StatusCode::OK);
    let body = axum::body::to_bytes(resp.into_body(), 64 * 1024).await.unwrap();
    insta::assert_json_snapshot!(serde_json::from_slice::<serde_json::Value>(&body).unwrap());
}

async fn test_db_pool() -> sqlx::PgPool {
    // Per-test schema: CREATE SCHEMA test_<uuid>, run migrations, DROP on teardown.
    todo!("replace with project-specific fixture")
}
```
