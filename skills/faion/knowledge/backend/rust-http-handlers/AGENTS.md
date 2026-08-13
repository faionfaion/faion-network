# Rust HTTP Handlers (Axum)

## Summary

**One-sentence:** Handler shape for Axum / Actix: typed DTOs with validator, Arc<AppState>, AppError IntoResponse, #[tracing::instrument] per handler, public message scrubbing.

**One-paragraph:** Handler pattern for Axum (and Actix-web): typed request/response DTOs with validator derives, shared AppState behind Arc, AppError enum implementing IntoResponse, and #[tracing::instrument] on every handler. Public response messages are scrubbed; internal details stay in tracing fields. Output is a handler module set + AppError module + integration tests.

**Ефективно для:**

- Standardising every handler in a service on the same DTO + state + error shape.
- Adding tracing instrumentation across all routes without manual span construction.
- Scrubbing internal error detail from public responses while preserving telemetry.
- Replacing ad-hoc StatusCode returns with a typed AppError → IntoResponse pipeline.

## Applies If (ALL must hold)

- Service uses Axum or Actix-web.
- Team can mandate the same handler skeleton across all routes.
- Telemetry stack (tracing + Jaeger / OpenTelemetry) is in place.
- Validation library (validator) is acceptable.

## Skip If (ANY kills it)

- Service uses tonic / pure gRPC — handler shape differs.
- Service is a Lambda function — different entry pattern.
- Quick prototype where typing every DTO is overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Route list + DTOs | yaml / md | team |
| AppState fields | yaml | team |
| Tracing exporter | config | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems/rust-backend/AGENTS.md` | layout precedes handlers |
| `pro/dev/backend-systems/rust-error-handling/AGENTS.md` | AppError is shared |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-handler-shape` | sonnet | DTO + extractor wiring needs judgement. |
| `review-public-messages` | sonnet | Message scrubbing needs language judgement. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/handler_example.rs` | Axum CRUD handler skeleton |
| `templates/app_error.rs` | AppError with IntoResponse + scrubbed public messages |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-http-handlers.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[rust-backend]]
- [[rust-error-handling]]
- [[rust-project-structure]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/handler_example.rs`

```rust
// src/handlers/users.rs
// CRUD handler set for Axum: list, get, create, update, delete.
use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    Json,
};
use serde::{Deserialize, Serialize};
use validator::Validate;

use crate::{error::AppError, models::User, services::UserService, AppState};

#[derive(Debug, Deserialize)]
pub struct ListParams {
    #[serde(default = "default_page")]
    page: u32,
    #[serde(default = "default_per_page")]
    per_page: u32,
}
fn default_page() -> u32 { 1 }
fn default_per_page() -> u32 { 20 }

#[derive(Debug, Serialize)]
pub struct ListResponse { data: Vec<UserResponse>, total: i64, page: u32, per_page: u32 }

#[derive(Debug, Serialize)]
pub struct UserResponse { id: i32, name: String, email: String }

impl From<User> for UserResponse {
    fn from(u: User) -> Self { Self { id: u.id, name: u.name, email: u.email } }
}

#[derive(Debug, Deserialize, Validate)]
pub struct CreateUserRequest {
    #[validate(length(min = 2, max = 100))] name: String,
    #[validate(email)]                       email: String,
    #[validate(length(min = 8))]             password: String,
}

pub async fn list(
    State(state): State<AppState>,
    Query(params): Query<ListParams>,
) -> Result<Json<ListResponse>, AppError> {
    let svc = UserService::new(&state.db);
    let (users, total) = svc.list(params.page, params.per_page).await?;
    Ok(Json(ListResponse {
        data: users.into_iter().map(UserResponse::from).collect(),
        total, page: params.page, per_page: params.per_page,
    }))
}

pub async fn get(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<UserResponse>, AppError> {
    let svc = UserService::new(&state.db);
    Ok(Json(svc.get_by_id(id).await?.into()))
}

pub async fn create(
    State(state): State<AppState>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<UserResponse>), AppError> {
    payload.validate()?;
    let svc = UserService::new(&state.db);
    let user = svc.create(&payload.name, &payload.email, &payload.password).await?;
    Ok((StatusCode::CREATED, Json(user.into())))
}

pub async fn delete(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<StatusCode, AppError> {
    UserService::new(&state.db).delete(id).await?;
    Ok(StatusCode::NO_CONTENT)
}
```

### `templates/app_error.rs`

```rust
// src/error.rs
// Axum AppError: thiserror enum + IntoResponse with public message scrubbing.
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("not found")]
    NotFound,
    #[error("unauthorized")]
    Unauthorized,
    #[error("validation: {0}")]
    Validation(#[from] validator::ValidationErrors),
    #[error("conflict: {0}")]
    Conflict(String),
    #[error("database: {0}")]
    Database(#[from] sqlx::Error),
    #[error("upstream: {0}")]
    Upstream(#[from] reqwest::Error),
    #[error("internal: {0}")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code) = match &self {
            AppError::NotFound      => (StatusCode::NOT_FOUND,                "NOT_FOUND"),
            AppError::Unauthorized  => (StatusCode::UNAUTHORIZED,             "UNAUTHORIZED"),
            AppError::Validation(_) => (StatusCode::UNPROCESSABLE_ENTITY,    "VALIDATION_ERROR"),
            AppError::Conflict(_)   => (StatusCode::CONFLICT,                "CONFLICT"),
            AppError::Database(_)
            | AppError::Upstream(_)
            | AppError::Internal(_) => (StatusCode::INTERNAL_SERVER_ERROR,   "INTERNAL_ERROR"),
        };
        // Public message hides internal details for 5xx variants.
        let msg = match &self {
            AppError::Database(_)
            | AppError::Upstream(_)
            | AppError::Internal(_) => "internal error".to_string(),
            other => other.to_string(),
        };
        tracing::error!(error = %self, "request failed");
        (status, Json(json!({ "error": { "code": code, "message": msg } }))).into_response()
    }
}
```
