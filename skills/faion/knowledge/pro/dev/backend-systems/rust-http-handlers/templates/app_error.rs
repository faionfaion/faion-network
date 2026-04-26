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
