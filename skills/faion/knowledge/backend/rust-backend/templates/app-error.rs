// purpose: AppError enum with IntoResponse mapping to RFC 7807
// consumes: handler return values
// produces: HTTP response with RFC 7807 ProblemDetail
// depends-on: scripts/validate-rust-backend.py
// token-budget-impact: ~250 tokens
// templates/app-error.rs
// AppError enum with IntoResponse mapping to RFC 7807 ProblemDetail.
// Import and extend; every variant must appear in the match arm below.

use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};
use serde::Serialize;

#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),

    #[error("conflict: {0}")]
    Conflict(String),

    #[error("validation: {0}")]
    Validation(String),

    #[error("unauthorized")]
    Unauthorized,

    #[error(transparent)]
    Db(#[from] sqlx::Error),

    #[error(transparent)]
    Join(#[from] tokio::task::JoinError),
}

#[derive(Serialize)]
struct Problem<'a> {
    #[serde(rename = "type")]
    ty: &'a str,
    title: &'a str,
    status: u16,
    detail: String,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, ty, title) = match &self {
            AppError::NotFound(_) =>
                (StatusCode::NOT_FOUND, "/errors/not-found", "Not Found"),
            AppError::Conflict(_) =>
                (StatusCode::CONFLICT, "/errors/conflict", "Conflict"),
            AppError::Validation(_) =>
                (StatusCode::BAD_REQUEST, "/errors/validation", "Validation Error"),
            AppError::Unauthorized =>
                (StatusCode::UNAUTHORIZED, "/errors/unauthorized", "Unauthorized"),
            AppError::Db(_) | AppError::Join(_) =>
                (StatusCode::INTERNAL_SERVER_ERROR, "/errors/internal", "Internal Error"),
        };
        tracing::error!(error = %self, "request failed");
        (status, Json(Problem {
            ty,
            title,
            status: status.as_u16(),
            detail: self.to_string(),
        })).into_response()
    }
}
