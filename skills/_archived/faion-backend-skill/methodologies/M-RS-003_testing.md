# M-RS-003: Rust Testing

## Metadata
- **Category:** Development/Backend/Rust
- **Difficulty:** Intermediate
- **Tags:** #dev, #rust, #testing, #methodology
- **Agent:** faion-test-agent

---

## Problem

Rust testing has unique patterns due to ownership and borrowing. Async testing requires specific setup. Without proper patterns, tests become verbose and hard to maintain.

## Promise

After this methodology, you will write Rust tests that are comprehensive, fast, and leverage Rust's type system. You will test units, integrations, and async code effectively.

## Overview

Rust has built-in testing with `#[test]` and `#[tokio::test]`. This methodology covers patterns for unit tests, integration tests, and property-based testing.

---

## Framework

### Step 1: Test Organization

```
my-app/
├── src/
│   ├── lib.rs
│   └── services/
│       └── user.rs      # Unit tests inline
├── tests/
│   ├── common/
│   │   └── mod.rs       # Shared test utilities
│   ├── api_tests.rs     # Integration tests
│   └── user_tests.rs
└── benches/
    └── benchmark.rs     # Benchmarks
```

### Step 2: Unit Tests

```rust
// src/services/user.rs

pub struct UserService {
    // ...
}

impl UserService {
    pub fn validate_email(email: &str) -> bool {
        email.contains('@') && email.contains('.')
    }

    pub fn validate_password(password: &str) -> Result<(), &'static str> {
        if password.len() < 8 {
            return Err("Password must be at least 8 characters");
        }
        if !password.chars().any(|c| c.is_uppercase()) {
            return Err("Password must contain an uppercase letter");
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    mod validate_email {
        use super::*;

        #[test]
        fn accepts_valid_email() {
            assert!(UserService::validate_email("user@example.com"));
        }

        #[test]
        fn rejects_email_without_at() {
            assert!(!UserService::validate_email("userexample.com"));
        }

        #[test]
        fn rejects_email_without_dot() {
            assert!(!UserService::validate_email("user@example"));
        }

        #[test]
        fn rejects_empty_email() {
            assert!(!UserService::validate_email(""));
        }
    }

    mod validate_password {
        use super::*;

        #[test]
        fn accepts_valid_password() {
            assert!(UserService::validate_password("Password123").is_ok());
        }

        #[test]
        fn rejects_short_password() {
            let result = UserService::validate_password("Pass1");
            assert_eq!(result, Err("Password must be at least 8 characters"));
        }

        #[test]
        fn rejects_password_without_uppercase() {
            let result = UserService::validate_password("password123");
            assert_eq!(result, Err("Password must contain an uppercase letter"));
        }
    }
}
```

### Step 3: Async Tests

```rust
// src/services/user.rs

impl UserService {
    pub async fn find_by_email(&self, email: &str) -> Result<User, Error> {
        // Database lookup
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio;

    #[tokio::test]
    async fn find_by_email_returns_user() {
        // Arrange
        let pool = setup_test_db().await;
        let service = UserService::new(&pool);

        // Seed test data
        sqlx::query!("INSERT INTO users (email, name) VALUES ($1, $2)", "test@example.com", "Test")
            .execute(&pool)
            .await
            .unwrap();

        // Act
        let result = service.find_by_email("test@example.com").await;

        // Assert
        assert!(result.is_ok());
        assert_eq!(result.unwrap().email, "test@example.com");
    }

    #[tokio::test]
    async fn find_by_email_returns_error_when_not_found() {
        let pool = setup_test_db().await;
        let service = UserService::new(&pool);

        let result = service.find_by_email("nonexistent@example.com").await;

        assert!(matches!(result, Err(Error::NotFound)));
    }
}
```

### Step 4: Test Fixtures

```rust
// tests/common/mod.rs

use sqlx::{PgPool, postgres::PgPoolOptions};
use once_cell::sync::Lazy;
use tokio::sync::OnceCell;

static TEST_DB: OnceCell<PgPool> = OnceCell::const_new();

pub async fn get_test_db() -> &'static PgPool {
    TEST_DB.get_or_init(|| async {
        dotenvy::dotenv().ok();
        let url = std::env::var("TEST_DATABASE_URL")
            .expect("TEST_DATABASE_URL must be set");

        PgPoolOptions::new()
            .max_connections(5)
            .connect(&url)
            .await
            .expect("Failed to connect to test database")
    }).await
}

pub struct TestUser {
    pub id: i32,
    pub email: String,
    pub name: String,
}

impl TestUser {
    pub async fn create(pool: &PgPool) -> Self {
        let email = format!("test-{}@example.com", uuid::Uuid::new_v4());
        let name = "Test User".to_string();

        let id = sqlx::query_scalar!(
            "INSERT INTO users (email, name, password_hash) VALUES ($1, $2, 'hash') RETURNING id",
            email,
            name
        )
        .fetch_one(pool)
        .await
        .unwrap();

        Self { id, email, name }
    }

    pub async fn cleanup(&self, pool: &PgPool) {
        sqlx::query!("DELETE FROM users WHERE id = $1", self.id)
            .execute(pool)
            .await
            .ok();
    }
}
```

### Step 5: Integration Tests

```rust
// tests/api_tests.rs

mod common;

use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use tower::ServiceExt;
use serde_json::json;

use my_app::{create_app, state::AppState};

async fn setup_app() -> axum::Router {
    let pool = common::get_test_db().await.clone();
    let config = my_app::config::Settings::test_config();
    let state = AppState::new(pool, config);
    create_app(state)
}

#[tokio::test]
async fn health_check_returns_ok() {
    let app = setup_app().await;

    let response = app
        .oneshot(Request::builder().uri("/health").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}

#[tokio::test]
async fn create_user_with_valid_data() {
    let app = setup_app().await;

    let body = json!({
        "email": "new@example.com",
        "name": "New User",
        "password": "Password123"
    });

    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/api/v1/users")
                .header("Content-Type", "application/json")
                .body(Body::from(serde_json::to_string(&body).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::CREATED);
}

#[tokio::test]
async fn create_user_with_invalid_email_returns_400() {
    let app = setup_app().await;

    let body = json!({
        "email": "invalid",
        "name": "New User",
        "password": "Password123"
    });

    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/api/v1/users")
                .header("Content-Type", "application/json")
                .body(Body::from(serde_json::to_string(&body).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::BAD_REQUEST);
}
```

### Step 6: Property-Based Testing

```toml
# Cargo.toml
[dev-dependencies]
proptest = "1.4"
```

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn email_with_at_and_dot_is_valid(
        local in "[a-z]{1,10}",
        domain in "[a-z]{1,10}",
        tld in "[a-z]{2,4}"
    ) {
        let email = format!("{}@{}.{}", local, domain, tld);
        prop_assert!(UserService::validate_email(&email));
    }

    #[test]
    fn password_length_check_is_correct(password in ".{0,7}") {
        let result = UserService::validate_password(&password);
        prop_assert!(result.is_err());
    }

    #[test]
    fn valid_password_always_accepted(
        prefix in "[A-Z][a-z]{3,10}",
        suffix in "[0-9]{3,5}"
    ) {
        let password = format!("{}{}", prefix, suffix);
        prop_assert!(UserService::validate_password(&password).is_ok());
    }
}
```

---

## Templates

### Mock Trait

```rust
use async_trait::async_trait;
use mockall::automock;

#[automock]
#[async_trait]
pub trait UserRepository {
    async fn find_by_id(&self, id: i32) -> Result<User, Error>;
    async fn create(&self, user: CreateUser) -> Result<User, Error>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_with_mock() {
        let mut mock = MockUserRepository::new();

        mock.expect_find_by_id()
            .with(eq(1))
            .times(1)
            .returning(|_| Ok(User { id: 1, name: "Test".to_string() }));

        let result = mock.find_by_id(1).await;
        assert!(result.is_ok());
    }
}
```

### Test Coverage

```bash
# Install tarpaulin
cargo install cargo-tarpaulin

# Run with coverage
cargo tarpaulin --out Html --output-dir coverage

# With specific targets
cargo tarpaulin --ignore-tests --out Lcov
```

---

## Examples

### Testing Error Cases

```rust
#[test]
fn operation_fails_with_invalid_input() {
    let result = process_data("");

    assert!(result.is_err());
    assert!(matches!(result, Err(Error::InvalidInput(_))));
}

#[test]
#[should_panic(expected = "invariant violated")]
fn panics_on_invariant_violation() {
    dangerous_operation(null_ptr());
}
```

### Ignoring Tests

```rust
#[test]
#[ignore = "requires external service"]
fn test_with_external_api() {
    // Run with: cargo test -- --ignored
}
```

---

## Common Mistakes

1. **Not testing edge cases** - Test empty, null, max values
2. **Shared mutable state** - Use per-test setup
3. **Blocking in async tests** - Use spawn_blocking
4. **Missing #[tokio::test]** - Required for async tests
5. **No cleanup** - Clean up test data

---

## Checklist

- [ ] Unit tests inline in modules
- [ ] Integration tests in tests/
- [ ] Async tests with tokio::test
- [ ] Test fixtures for common setup
- [ ] Mocking with mockall
- [ ] Property-based testing
- [ ] Code coverage with tarpaulin
- [ ] CI runs all tests

---

## Next Steps

- M-RS-004: Rust Error Handling
- M-RS-002: Axum Patterns
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-RS-003 v1.0*
