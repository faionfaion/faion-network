// src/services/users.rs
// UserService: try_join! for parallel IO, spawn_blocking for CPU-heavy password hashing.
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHasher, SaltString},
    Argon2,
};

use crate::{db::Database, error::AppError, models::User};

pub struct UserService {
    db: Database, // Database wraps Arc<PgPool>
}

impl UserService {
    pub fn new(db: Database) -> Self { Self { db } }

    /// Fetch page of users and total count in parallel.
    pub async fn list(&self, page: u32, per_page: u32) -> Result<(Vec<User>, i64), AppError> {
        let offset = ((page - 1) * per_page) as i64;
        let (users, total) = tokio::try_join!(
            self.db.fetch_users(per_page as i64, offset),
            self.db.count_users()
        )?;
        Ok((users, total))
    }

    /// Create user: check uniqueness, hash password on blocking thread, insert.
    pub async fn create(
        &self, name: &str, email: &str, password: &str,
    ) -> Result<User, AppError> {
        if self.db.fetch_user_by_email(email).await?.is_some() {
            return Err(AppError::Conflict("email already exists".into()));
        }

        // Password hashing is CPU-heavy — must not run on the async executor thread.
        let password_hash = tokio::task::spawn_blocking({
            let password = password.to_string();
            move || {
                let salt = SaltString::generate(&mut OsRng);
                Argon2::default()
                    .hash_password(password.as_bytes(), &salt)
                    .map(|h| h.to_string())
                    .map_err(|e| anyhow::anyhow!("argon2: {e}"))
            }
        })
        // First ? = JoinError (task panicked), second ? = inner Result.
        .await??;

        self.db.insert_user(name, email, &password_hash).await
    }
}
