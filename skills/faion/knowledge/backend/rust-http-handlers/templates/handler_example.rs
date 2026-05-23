// purpose: Axum CRUD handler skeleton (list/get/create/update/delete)
// consumes: typed DTOs + Arc<AppState>
// produces: HTTP response
// depends-on: scripts/validate-rust-http-handlers.py
// token-budget-impact: ~300 tokens
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
