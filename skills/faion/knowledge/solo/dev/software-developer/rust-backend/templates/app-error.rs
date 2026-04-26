// AppError — single error type for all Axum handlers
// Usage: return Err(AppError::NotFound("User not found".into()))
// Requires: axum, thiserror, serde_json, tracing

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),
    #[error("conflict: {0}")]
    Conflict(String),
    #[error("unauthorized")]
    Unauthorized,
    #[error("validation: {0}")]
    Validation(String),
    #[error(transparent)]
    Db(#[from] sqlx::Error),
    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, msg) = match &self {
            Self::NotFound(_)   => (StatusCode::NOT_FOUND,           self.to_string()),
            Self::Conflict(_)   => (StatusCode::CONFLICT,            self.to_string()),
            Self::Unauthorized  => (StatusCode::UNAUTHORIZED,        self.to_string()),
            Self::Validation(_) => (StatusCode::UNPROCESSABLE_ENTITY, self.to_string()),
            _                   => (StatusCode::INTERNAL_SERVER_ERROR, "internal error".into()),
        };
        if status.is_server_error() {
            tracing::error!(error = ?self, "server error");
        }
        (status, Json(json!({"error": msg}))).into_response()
    }
}
