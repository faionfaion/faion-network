# M-RS-004: Rust Error Handling

## Metadata
- **Category:** Development/Backend/Rust
- **Difficulty:** Intermediate
- **Tags:** #dev, #rust, #errors, #methodology
- **Agent:** faion-code-agent

---

## Problem

Rust's error handling is powerful but requires understanding Result, Option, and error conversion. Without proper patterns, error handling becomes repetitive and error messages are unhelpful.

## Promise

After this methodology, you will handle errors in Rust idiomatically. Your errors will be informative, type-safe, and easy to handle across layers.

## Overview

Rust uses `Result<T, E>` for recoverable errors and `panic!` for unrecoverable ones. This methodology covers thiserror for library errors, anyhow for application errors, and conversion patterns.

---

## Framework

### Step 1: Error Crates

```toml
# Cargo.toml

# For defining custom errors (libraries, domain code)
thiserror = "1.0"

# For application-level error handling
anyhow = "1.0"
```

**When to use:**
- **thiserror**: Library code, domain errors, when callers need to match on error types
- **anyhow**: Application code, when you just need to propagate errors with context

### Step 2: Domain Errors with thiserror

```rust
// src/error.rs
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DomainError {
    #[error("User not found: {0}")]
    UserNotFound(String),

    #[error("Invalid email format: {0}")]
    InvalidEmail(String),

    #[error("Password too weak: {reason}")]
    WeakPassword { reason: String },

    #[error("Email already registered")]
    EmailAlreadyExists,

    #[error("Authentication failed")]
    AuthenticationFailed,

    #[error("Permission denied: {action} on {resource}")]
    PermissionDenied { action: String, resource: String },
}

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Domain error: {0}")]
    Domain(#[from] DomainError),

    #[error("Database error")]
    Database(#[source] sqlx::Error),

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("External service unavailable: {service}")]
    ServiceUnavailable { service: String },

    #[error("Internal error")]
    Internal(#[from] anyhow::Error),
}
```

### Step 3: Error Conversion

```rust
// Automatic conversion with #[from]
impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        match &err {
            sqlx::Error::RowNotFound => {
                AppError::Domain(DomainError::UserNotFound("unknown".to_string()))
            }
            _ => AppError::Database(err),
        }
    }
}

// For validation errors
impl From<validator::ValidationErrors> for AppError {
    fn from(err: validator::ValidationErrors) -> Self {
        AppError::Validation(format!("{}", err))
    }
}
```

### Step 4: Using Result and ?

```rust
use crate::error::{AppError, DomainError};

pub struct UserService {
    db: PgPool,
}

impl UserService {
    pub async fn create_user(&self, input: CreateUserInput) -> Result<User, AppError> {
        // Validation - ? propagates error
        self.validate_email(&input.email)?;
        self.validate_password(&input.password)?;

        // Check existence
        if self.email_exists(&input.email).await? {
            return Err(DomainError::EmailAlreadyExists.into());
        }

        // Create user - ? converts sqlx::Error to AppError
        let user = sqlx::query_as!(
            User,
            "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *",
            input.email,
            input.name
        )
        .fetch_one(&self.db)
        .await?;

        Ok(user)
    }

    fn validate_email(&self, email: &str) -> Result<(), DomainError> {
        if !email.contains('@') {
            return Err(DomainError::InvalidEmail(email.to_string()));
        }
        Ok(())
    }

    fn validate_password(&self, password: &str) -> Result<(), DomainError> {
        if password.len() < 8 {
            return Err(DomainError::WeakPassword {
                reason: "must be at least 8 characters".to_string(),
            });
        }
        Ok(())
    }
}
```

### Step 5: anyhow for Applications

```rust
use anyhow::{Context, Result, bail, ensure};

pub async fn run_migration() -> Result<()> {
    let db_url = std::env::var("DATABASE_URL")
        .context("DATABASE_URL must be set")?;

    let pool = PgPool::connect(&db_url)
        .await
        .context("Failed to connect to database")?;

    sqlx::migrate!()
        .run(&pool)
        .await
        .context("Failed to run migrations")?;

    Ok(())
}

pub fn process_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read config file: {}", path))?;

    let config: Config = toml::from_str(&content)
        .context("Failed to parse config")?;

    // Ensure conditions
    ensure!(config.port > 0, "Port must be positive");

    // Bail on errors
    if config.secret.is_empty() {
        bail!("Secret cannot be empty");
    }

    Ok(config)
}
```

### Step 6: HTTP Error Response

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code, message) = match &self {
            AppError::Domain(e) => match e {
                DomainError::UserNotFound(_) => {
                    (StatusCode::NOT_FOUND, "USER_NOT_FOUND", e.to_string())
                }
                DomainError::InvalidEmail(_) | DomainError::WeakPassword { .. } => {
                    (StatusCode::BAD_REQUEST, "VALIDATION_ERROR", e.to_string())
                }
                DomainError::EmailAlreadyExists => {
                    (StatusCode::CONFLICT, "EMAIL_EXISTS", e.to_string())
                }
                DomainError::AuthenticationFailed => {
                    (StatusCode::UNAUTHORIZED, "AUTH_FAILED", e.to_string())
                }
                DomainError::PermissionDenied { .. } => {
                    (StatusCode::FORBIDDEN, "FORBIDDEN", e.to_string())
                }
            },
            AppError::Validation(msg) => {
                (StatusCode::BAD_REQUEST, "VALIDATION_ERROR", msg.clone())
            }
            AppError::Database(e) => {
                tracing::error!("Database error: {:?}", e);
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    "INTERNAL_ERROR",
                    "Internal server error".to_string(),
                )
            }
            AppError::ServiceUnavailable { service } => (
                StatusCode::SERVICE_UNAVAILABLE,
                "SERVICE_UNAVAILABLE",
                format!("{} is unavailable", service),
            ),
            AppError::Internal(e) => {
                tracing::error!("Internal error: {:?}", e);
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    "INTERNAL_ERROR",
                    "Internal server error".to_string(),
                )
            }
        };

        let body = Json(json!({
            "error": {
                "code": code,
                "message": message,
            }
        }));

        (status, body).into_response()
    }
}
```

---

## Templates

### Error Result Extension

```rust
pub trait ResultExt<T> {
    fn or_not_found(self, resource: &str) -> Result<T, AppError>;
}

impl<T> ResultExt<T> for Option<T> {
    fn or_not_found(self, resource: &str) -> Result<T, AppError> {
        self.ok_or_else(|| DomainError::UserNotFound(resource.to_string()).into())
    }
}

// Usage
let user = self.find_by_id(id).await?.or_not_found("user")?;
```

### Logging Errors

```rust
impl AppError {
    pub fn log(&self) {
        match self {
            AppError::Database(e) => {
                tracing::error!(error = ?e, "Database error occurred");
            }
            AppError::Internal(e) => {
                tracing::error!(error = ?e, "Internal error occurred");
            }
            _ => {
                tracing::warn!(error = %self, "Error occurred");
            }
        }
    }
}
```

---

## Examples

### Chaining with and_then

```rust
fn process_user(id: i32) -> Result<ProcessedUser, AppError> {
    find_user(id)
        .and_then(|user| validate_user(&user))
        .and_then(|user| enrich_user(user))
        .map(ProcessedUser::from)
}
```

### Mapping Errors

```rust
let result = external_api::fetch_data()
    .await
    .map_err(|e| AppError::ServiceUnavailable {
        service: "external-api".to_string(),
    })?;
```

### Collecting Results

```rust
let users: Result<Vec<User>, AppError> = ids
    .iter()
    .map(|id| find_user(*id))
    .collect();
```

---

## Common Mistakes

1. **Using unwrap in production** - Use ? or handle errors
2. **Ignoring error context** - Add context with anyhow
3. **Leaking internal errors** - Map to user-friendly messages
4. **Missing From implementations** - Enable ? conversion
5. **Not logging errors** - Log before converting to response

---

## Checklist

- [ ] Domain errors with thiserror
- [ ] Application errors with anyhow
- [ ] Error conversion traits
- [ ] HTTP response mapping
- [ ] Context on all ? calls
- [ ] Logging for server errors
- [ ] No unwrap in production code
- [ ] User-friendly error messages

---

## Next Steps

- M-RS-001: Rust Project Setup
- M-RS-002: Axum Patterns
- M-RS-003: Rust Testing

---

*Methodology M-RS-004 v1.0*
