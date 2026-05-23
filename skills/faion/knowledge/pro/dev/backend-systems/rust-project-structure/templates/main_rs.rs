// purpose: main.rs ≤80 lines — config + state + router + serve
// consumes: AppState + router
// produces: bound HTTP server
// depends-on: scripts/validate-rust-project-structure.py
// token-budget-impact: ~250 tokens
// src/main.rs — ≤80 lines: config, state, router composition, serve.
use std::sync::Arc;

use axum::Router;
use tower_http::trace::TraceLayer;

mod config;
mod db;
mod error;
mod handlers;
mod middleware;
mod models;
mod routes;
mod services;

use crate::{config::Config, db::Database};

#[derive(Clone)]
pub struct AppState {
    pub db:     Database,
    pub config: Arc<Config>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let config = Config::from_env()?;
    let db = Database::connect(&config.database_url).await?;

    let state = AppState { db, config: Arc::new(config) };

    let app = Router::new()
        .nest("/api/v1", routes::api_routes())
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    tracing::info!("listening on http://0.0.0.0:3000");
    axum::serve(listener, app).await?;
    Ok(())
}
