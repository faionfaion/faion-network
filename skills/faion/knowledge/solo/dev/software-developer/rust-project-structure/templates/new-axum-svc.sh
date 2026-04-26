#!/usr/bin/env bash
# Usage: ./new-axum-svc.sh <service-name>
# Bootstraps an Axum service with the layered module structure.
set -euo pipefail

NAME=${1:?Provide service name}
cargo new --bin "$NAME"
cd "$NAME"

cargo add axum tokio --features tokio/full
cargo add tower-http --features tower-http/trace
cargo add tracing tracing-subscriber
cargo add serde --features serde/derive
cargo add serde_json
cargo add anyhow thiserror
cargo add validator --features validator/derive

mkdir -p src/{routes,handlers,services,db,models,middleware}
for d in routes handlers services db models middleware; do
  printf '// %s module root\n' "$d" > "src/$d/mod.rs"
done

cat > src/error.rs <<'EOF'
use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};

#[derive(thiserror::Error, Debug)]
pub enum AppError {
    #[error("not found")]
    NotFound,
    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let status = match self {
            Self::NotFound => StatusCode::NOT_FOUND,
            Self::Internal(_) => StatusCode::INTERNAL_SERVER_ERROR,
        };
        (status, self.to_string()).into_response()
    }
}
EOF

cat > src/main.rs <<'EOF'
mod error;
mod handlers;
mod middleware;
mod models;
mod routes;
mod services;
mod db;

use axum::Router;

#[derive(Clone)]
pub struct AppState {}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    let state = AppState {};
    let app = Router::new()
        .nest("/api/v1", routes::api_routes())
        .with_state(state);
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    tracing::info!("listening on http://0.0.0.0:3000");
    axum::serve(listener, app).await?;
    Ok(())
}
EOF

cat > src/routes/mod.rs <<'EOF'
use axum::{routing::get, Router};
use crate::AppState;

pub fn api_routes() -> Router<AppState> {
    Router::new().route("/health", get(|| async { "OK" }))
}
EOF

echo "Scaffolded $NAME — run: cd $NAME && cargo check"
