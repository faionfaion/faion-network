// Reference async service: try_join! for parallel queries, spawn_blocking for CPU work.
// Input: &Database reference
// Output: Result<T, AppError> on all methods

use argon2::{password_hash::{rand_core::OsRng, PasswordHasher, SaltString}, Argon2};
use crate::{db::Database, error::AppError, models::User};

pub struct UserService<'a> {
    db: &'a Database,
}

impl<'a> UserService<'a> {
    pub fn new(db: &'a Database) -> Self { Self { db } }

    pub async fn list(&self, page: u32, per_page: u32) -> Result<(Vec<User>, i64), AppError> {
        let offset = ((page - 1) * per_page) as i64;
        // Both queries run in parallel — total time = max(query_a, query_b)
        let (users, total) = tokio::try_join!(
            self.db.fetch_users(per_page as i64, offset),
            self.db.count_users()
        )?;
        Ok((users, total))
    }

    pub async fn get_by_id(&self, id: i32) -> Result<User, AppError> {
        self.db.fetch_user_by_id(id).await?
            .ok_or(AppError::NotFound("User not found".into()))
    }

    pub async fn create(&self, name: &str, email: &str, password: &str) -> Result<User, AppError> {
        if self.db.fetch_user_by_email(email).await?.is_some() {
            return Err(AppError::Conflict("Email already exists".into()));
        }
        // CPU-intensive: move to blocking thread to avoid stalling the runtime
        let password_hash = tokio::task::spawn_blocking({
            let password = password.to_string();
            move || {
                let salt = SaltString::generate(&mut OsRng);
                Argon2::default()
                    .hash_password(password.as_bytes(), &salt)
                    .map(|h| h.to_string())
            }
        })
        .await??; // outer ? = JoinError, inner ? = hash error

        self.db.insert_user(name, email, &password_hash).await
    }
}
