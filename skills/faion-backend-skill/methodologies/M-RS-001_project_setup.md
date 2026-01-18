# M-RS-001: Rust Project Setup with Cargo

## Metadata
- **Category:** Development/Backend/Rust
- **Difficulty:** Beginner
- **Tags:** #dev, #rust, #backend, #cargo, #methodology
- **Agent:** faion-code-agent

---

## Problem

Rust projects require understanding Cargo, workspace organization, and the unique aspects of Rust's build system. Without proper setup, compile times suffer and dependency management becomes painful.

## Promise

After this methodology, you will have a professional Rust project with proper Cargo configuration, workspace structure, and development tooling.

## Overview

Rust uses Cargo for building, testing, and dependency management. This methodology covers setup for both library and binary projects, including web APIs with Axum.

---

## Framework

### Step 1: Rust Installation

```bash
# Install Rust via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Verify
rustc --version
cargo --version

# Update Rust
rustup update

# Add components
rustup component add clippy rustfmt rust-analyzer

# Install useful tools
cargo install cargo-watch cargo-edit cargo-audit cargo-tarpaulin
```

### Step 2: Create Project

**Binary project:**

```bash
cargo new my-app
cd my-app
```

**Library project:**

```bash
cargo new my-lib --lib
```

**Workspace:**

```bash
mkdir my-workspace && cd my-workspace
cargo new api --name my-api
cargo new core --lib --name my-core
cargo new shared --lib --name my-shared
```

### Step 3: Project Structure

**Binary project:**

```
my-app/
├── Cargo.toml
├── Cargo.lock
├── .gitignore
├── README.md
├── src/
│   ├── main.rs
│   ├── lib.rs           # Library code
│   ├── config.rs
│   ├── error.rs
│   ├── routes/
│   │   ├── mod.rs
│   │   └── users.rs
│   └── handlers/
│       ├── mod.rs
│       └── users.rs
├── tests/
│   └── integration_test.rs
└── benches/
    └── benchmark.rs
```

**Workspace:**

```
my-workspace/
├── Cargo.toml           # Workspace root
├── Cargo.lock
├── .gitignore
├── api/
│   ├── Cargo.toml
│   └── src/
│       └── main.rs
├── core/
│   ├── Cargo.toml
│   └── src/
│       └── lib.rs
└── shared/
    ├── Cargo.toml
    └── src/
        └── lib.rs
```

### Step 4: Cargo Configuration

**Cargo.toml (binary):**

```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
description = "My Rust application"
license = "MIT"
repository = "https://github.com/username/my-app"
rust-version = "1.75"

[dependencies]
# Async runtime
tokio = { version = "1.35", features = ["full"] }

# Web framework
axum = "0.7"
tower = "0.4"
tower-http = { version = "0.5", features = ["trace", "cors"] }

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Database
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres", "migrate"] }

# Error handling
thiserror = "1.0"
anyhow = "1.0"

# Configuration
config = "0.14"
dotenvy = "0.15"

# Logging
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

# Validation
validator = { version = "0.16", features = ["derive"] }

[dev-dependencies]
tokio-test = "0.4"
reqwest = { version = "0.11", features = ["json"] }
fake = { version = "2.9", features = ["derive"] }

[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true

[profile.dev.package.sqlx-macros]
opt-level = 3  # Speed up sqlx compile-time checks
```

**Cargo.toml (workspace root):**

```toml
[workspace]
members = ["api", "core", "shared"]
resolver = "2"

[workspace.package]
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
license = "MIT"

[workspace.dependencies]
tokio = { version = "1.35", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
tracing = "0.1"
thiserror = "1.0"
anyhow = "1.0"

# Internal crates
my-core = { path = "core" }
my-shared = { path = "shared" }
```

### Step 5: Development Commands

```bash
# Build
cargo build
cargo build --release

# Run
cargo run
cargo run --release

# Test
cargo test
cargo test -- --nocapture  # Show println output

# Watch mode
cargo watch -x run
cargo watch -x "test -- --nocapture"

# Check (faster than build)
cargo check

# Format
cargo fmt
cargo fmt --check

# Lint
cargo clippy
cargo clippy -- -D warnings  # Fail on warnings

# Audit dependencies
cargo audit

# Update dependencies
cargo update

# Documentation
cargo doc --open
```

### Step 6: Configuration Pattern

**src/config.rs:**

```rust
use config::{Config, ConfigError, Environment, File};
use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct Settings {
    pub server: ServerSettings,
    pub database: DatabaseSettings,
    pub logging: LoggingSettings,
}

#[derive(Debug, Deserialize, Clone)]
pub struct ServerSettings {
    pub host: String,
    pub port: u16,
}

#[derive(Debug, Deserialize, Clone)]
pub struct DatabaseSettings {
    pub url: String,
    pub max_connections: u32,
}

#[derive(Debug, Deserialize, Clone)]
pub struct LoggingSettings {
    pub level: String,
}

impl Settings {
    pub fn new() -> Result<Self, ConfigError> {
        let run_mode = std::env::var("RUN_MODE").unwrap_or_else(|_| "development".into());

        Config::builder()
            // Start with default values
            .set_default("server.host", "127.0.0.1")?
            .set_default("server.port", 3000)?
            .set_default("database.max_connections", 5)?
            .set_default("logging.level", "info")?
            // Load environment-specific config
            .add_source(File::with_name(&format!("config/{}", run_mode)).required(false))
            // Override with environment variables (APP_SERVER__PORT, etc.)
            .add_source(Environment::with_prefix("APP").separator("__"))
            .build()?
            .try_deserialize()
    }
}
```

---

## Templates

**.gitignore:**

```
# Cargo
/target/
Cargo.lock  # Keep for binaries, ignore for libraries

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local

# OS
.DS_Store

# Coverage
*.profraw
*.profdata
coverage/
```

**Dockerfile:**

```dockerfile
# Build stage
FROM rust:1.75-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /app
COPY . .

RUN cargo build --release --locked

# Runtime stage
FROM alpine:3.19

RUN apk add --no-cache ca-certificates

WORKDIR /app
COPY --from=builder /app/target/release/my-app .

EXPOSE 3000
CMD ["./my-app"]
```

**rust-toolchain.toml:**

```toml
[toolchain]
channel = "1.75"
components = ["rustfmt", "clippy", "rust-analyzer"]
```

---

## Examples

### Main Entry Point

```rust
// src/main.rs
use anyhow::Result;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

mod config;
mod error;
mod routes;

#[tokio::main]
async fn main() -> Result<()> {
    // Load environment
    dotenvy::dotenv().ok();

    // Initialize logging
    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    // Load configuration
    let settings = config::Settings::new()?;

    // Build application
    let app = routes::create_router();

    // Start server
    let addr = format!("{}:{}", settings.server.host, settings.server.port);
    tracing::info!("Starting server on {}", addr);

    let listener = tokio::net::TcpListener::bind(&addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
```

### Simple Axum Router

```rust
// src/routes/mod.rs
use axum::{routing::get, Router};
use tower_http::trace::TraceLayer;

pub mod users;

pub fn create_router() -> Router {
    Router::new()
        .route("/health", get(health_check))
        .nest("/api/users", users::router())
        .layer(TraceLayer::new_for_http())
}

async fn health_check() -> &'static str {
    "OK"
}
```

---

## Common Mistakes

1. **Not using workspace for multi-crate** - Organize large projects
2. **Ignoring Cargo.lock for binaries** - Commit it for reproducibility
3. **Missing release optimizations** - Configure profile.release
4. **Slow compile times** - Use cargo check, optimize sqlx
5. **No rustfmt.toml** - Configure formatting preferences

---

## Checklist

- [ ] Rust installed via rustup
- [ ] rust-toolchain.toml for version pinning
- [ ] Cargo.toml with proper metadata
- [ ] Development tools installed (clippy, rustfmt)
- [ ] Configuration pattern implemented
- [ ] Release profile optimized
- [ ] Dockerfile ready
- [ ] .gitignore complete

---

## Next Steps

- M-RS-002: Rust Web Frameworks (Axum)
- M-RS-003: Rust Testing
- M-RS-004: Rust Error Handling

---

*Methodology M-RS-001 v1.0*
