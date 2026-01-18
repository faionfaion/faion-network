# M-RS-002: Rust Web Development with Axum

## Metadata
- **Category:** Development/Backend/Rust
- **Difficulty:** Intermediate
- **Tags:** #dev, #rust, #axum, #web, #methodology
- **Agent:** faion-code-agent

---

## Problem

Building web APIs in Rust requires understanding async patterns, extractors, and error handling. Without clear patterns, code becomes verbose and hard to maintain.

## Promise

After this methodology, you will build Axum web APIs that are type-safe, performant, and maintainable. You will use Rust's type system to prevent bugs.

## Overview

Axum is a modern Rust web framework built on Tower and Tokio. It uses extractors for request handling and provides excellent async support.

---

## Framework

### Step 1: Application Structure

```
src/
├── main.rs
├── lib.rs
├── config.rs
├── error.rs
├── extractors/
│   ├── mod.rs
│   └── auth.rs
├── handlers/
│   ├── mod.rs
│   └── users.rs
├── models/
│   ├── mod.rs
│   └── user.rs
├── repositories/
│   ├── mod.rs
│   └── user.rs
├── services/
│   ├── mod.rs
│   └── user.rs
├── routes/
│   ├── mod.rs
│   └── users.rs
└── state.rs
```

### Step 2: Application State

```rust
// src/state.rs
use sqlx::PgPool;
use std::sync::Arc;

#[derive(Clone)]
pub struct AppState {
    pub db: PgPool,
    pub config: Arc<crate::config::Settings>,
}

impl AppState {
    pub fn new(db: PgPool, config: crate::config::Settings) -> Self {
        Self {
            db,
            config: Arc::new(config),
        }
    }
}
```

### Step 3: Router Setup

```rust
// src/routes/mod.rs
use axum::{
    routing::{get, post, put, delete},
    Router,
};
use tower_http::{
    cors::{Any, CorsLayer},
    trace::TraceLayer,
};

use crate::state::AppState;

pub mod users;

pub fn create_router(state: AppState) -> Router {
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    Router::new()
        .route("/health", get(health_check))
        .nest("/api/v1", api_routes())
        .layer(TraceLayer::new_for_http())
        .layer(cors)
        .with_state(state)
}

fn api_routes() -> Router<AppState> {
    Router::new()
        .nest("/users", users::router())
}

async fn health_check() -> &'static str {
    "OK"
}
```

### Step 4: Handlers

```rust
// src/handlers/users.rs
use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    Json,
};
use serde::{Deserialize, Serialize};
use validator::Validate;

use crate::{
    error::AppError,
    models::user::{User, CreateUser, UpdateUser},
    services::user::UserService,
    state::AppState,
};

#[derive(Debug, Deserialize)]
pub struct ListQuery {
    pub page: Option<u32>,
    pub per_page: Option<u32>,
}

#[derive(Debug, Serialize)]
pub struct UserResponse {
    pub id: i32,
    pub email: String,
    pub name: String,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

impl From<User> for UserResponse {
    fn from(user: User) -> Self {
        Self {
            id: user.id,
            email: user.email,
            name: user.name,
            created_at: user.created_at,
        }
    }
}

pub async fn list(
    State(state): State<AppState>,
    Query(query): Query<ListQuery>,
) -> Result<Json<Vec<UserResponse>>, AppError> {
    let service = UserService::new(&state.db);
    let users = service
        .find_all(query.page.unwrap_or(1), query.per_page.unwrap_or(20))
        .await?;

    Ok(Json(users.into_iter().map(Into::into).collect()))
}

pub async fn get(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<UserResponse>, AppError> {
    let service = UserService::new(&state.db);
    let user = service.find_by_id(id).await?;

    Ok(Json(user.into()))
}

pub async fn create(
    State(state): State<AppState>,
    Json(payload): Json<CreateUser>,
) -> Result<(StatusCode, Json<UserResponse>), AppError> {
    payload.validate()?;

    let service = UserService::new(&state.db);
    let user = service.create(payload).await?;

    Ok((StatusCode::CREATED, Json(user.into())))
}

pub async fn update(
    State(state): State<AppState>,
    Path(id): Path<i32>,
    Json(payload): Json<UpdateUser>,
) -> Result<Json<UserResponse>, AppError> {
    payload.validate()?;

    let service = UserService::new(&state.db);
    let user = service.update(id, payload).await?;

    Ok(Json(user.into()))
}

pub async fn delete(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<StatusCode, AppError> {
    let service = UserService::new(&state.db);
    service.delete(id).await?;

    Ok(StatusCode::NO_CONTENT)
}
```

### Step 5: Error Handling

```rust
// src/error.rs
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Resource not found")]
    NotFound,

    #[error("Validation error: {0}")]
    Validation(#[from] validator::ValidationErrors),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Unauthorized")]
    Unauthorized,

    #[error("Internal error: {0}")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code, message) = match &self {
            AppError::NotFound => (StatusCode::NOT_FOUND, "NOT_FOUND", self.to_string()),
            AppError::Validation(errors) => {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(json!({
                        "code": "VALIDATION_ERROR",
                        "message": "Validation failed",
                        "errors": errors.field_errors()
                    })),
                )
                    .into_response();
            }
            AppError::Unauthorized => {
                (StatusCode::UNAUTHORIZED, "UNAUTHORIZED", self.to_string())
            }
            AppError::Database(err) => {
                tracing::error!("Database error: {:?}", err);
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    "INTERNAL_ERROR",
                    "Internal server error".to_string(),
                )
            }
            AppError::Internal(err) => {
                tracing::error!("Internal error: {:?}", err);
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    "INTERNAL_ERROR",
                    "Internal server error".to_string(),
                )
            }
        };

        let body = Json(json!({
            "code": code,
            "message": message,
        }));

        (status, body).into_response()
    }
}
```

### Step 6: Models with Validation

```rust
// src/models/user.rs
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sqlx::FromRow;
use validator::Validate;

#[derive(Debug, FromRow, Serialize)]
pub struct User {
    pub id: i32,
    pub email: String,
    pub name: String,
    pub password_hash: String,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Deserialize, Validate)]
pub struct CreateUser {
    #[validate(email(message = "Invalid email format"))]
    pub email: String,

    #[validate(length(min = 2, max = 100, message = "Name must be 2-100 characters"))]
    pub name: String,

    #[validate(length(min = 8, message = "Password must be at least 8 characters"))]
    pub password: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct UpdateUser {
    #[validate(length(min = 2, max = 100, message = "Name must be 2-100 characters"))]
    pub name: Option<String>,
}
```

---

## Templates

### User Routes

```rust
// src/routes/users.rs
use axum::{
    routing::{get, post, put, delete},
    Router,
};

use crate::{handlers::users, state::AppState};

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/", get(users::list).post(users::create))
        .route("/:id", get(users::get).put(users::update).delete(users::delete))
}
```

### Service Layer

```rust
// src/services/user.rs
use sqlx::PgPool;

use crate::{
    error::AppError,
    models::user::{CreateUser, UpdateUser, User},
};

pub struct UserService<'a> {
    db: &'a PgPool,
}

impl<'a> UserService<'a> {
    pub fn new(db: &'a PgPool) -> Self {
        Self { db }
    }

    pub async fn find_all(&self, page: u32, per_page: u32) -> Result<Vec<User>, AppError> {
        let offset = (page - 1) * per_page;

        let users = sqlx::query_as!(
            User,
            r#"SELECT * FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2"#,
            per_page as i64,
            offset as i64
        )
        .fetch_all(self.db)
        .await?;

        Ok(users)
    }

    pub async fn find_by_id(&self, id: i32) -> Result<User, AppError> {
        sqlx::query_as!(User, r#"SELECT * FROM users WHERE id = $1"#, id)
            .fetch_optional(self.db)
            .await?
            .ok_or(AppError::NotFound)
    }

    pub async fn create(&self, input: CreateUser) -> Result<User, AppError> {
        let password_hash = hash_password(&input.password)?;

        let user = sqlx::query_as!(
            User,
            r#"
            INSERT INTO users (email, name, password_hash)
            VALUES ($1, $2, $3)
            RETURNING *
            "#,
            input.email,
            input.name,
            password_hash
        )
        .fetch_one(self.db)
        .await?;

        Ok(user)
    }

    pub async fn delete(&self, id: i32) -> Result<(), AppError> {
        let result = sqlx::query!(r#"DELETE FROM users WHERE id = $1"#, id)
            .execute(self.db)
            .await?;

        if result.rows_affected() == 0 {
            return Err(AppError::NotFound);
        }

        Ok(())
    }
}

fn hash_password(password: &str) -> Result<String, AppError> {
    // Use argon2 or bcrypt
    Ok(format!("hashed_{}", password)) // Placeholder
}
```

---

## Examples

### Custom Extractor

```rust
// src/extractors/auth.rs
use axum::{
    async_trait,
    extract::FromRequestParts,
    http::{request::Parts, StatusCode},
    RequestPartsExt,
};
use axum_extra::{
    headers::{authorization::Bearer, Authorization},
    TypedHeader,
};

use crate::error::AppError;

pub struct AuthUser {
    pub user_id: i32,
}

#[async_trait]
impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
{
    type Rejection = AppError;

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        let TypedHeader(Authorization(bearer)) = parts
            .extract::<TypedHeader<Authorization<Bearer>>>()
            .await
            .map_err(|_| AppError::Unauthorized)?;

        let user_id = validate_token(bearer.token())?;

        Ok(AuthUser { user_id })
    }
}

fn validate_token(token: &str) -> Result<i32, AppError> {
    // JWT validation logic
    Ok(1) // Placeholder
}

// Usage in handler
pub async fn get_me(auth: AuthUser) -> Json<UserResponse> {
    // auth.user_id is available
}
```

---

## Common Mistakes

1. **Blocking in async** - Use spawn_blocking for CPU work
2. **Not using extractors** - Let Axum handle parsing
3. **Missing error conversion** - Implement IntoResponse
4. **Ignoring validation** - Validate all input
5. **State cloning issues** - Use Arc for expensive state

---

## Checklist

- [ ] Axum with Tower layers
- [ ] State management with Arc
- [ ] Custom error type with IntoResponse
- [ ] Validation with validator
- [ ] Extractors for common needs
- [ ] Service layer for business logic
- [ ] SQLx for database
- [ ] Tracing for logging

---

## Next Steps

- M-RS-003: Rust Testing
- M-RS-004: Rust Error Handling
- M-API-001: REST API Design

---

*Methodology M-RS-002 v1.0*
