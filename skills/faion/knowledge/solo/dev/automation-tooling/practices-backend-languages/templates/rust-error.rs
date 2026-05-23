// purpose: Rust error type via thiserror + async fn
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for practices-backend-languages
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

use thiserror::Error;

#[derive(Error, Debug)]
pub enum OrderError {
    #[error("order not found: {0}")]
    NotFound(String),
    #[error("database error")]
    Db(#[from] sqlx::Error),
}

pub async fn charge_order(pool: &sqlx::PgPool, id: &str) -> Result<Order, OrderError> {
    let row = sqlx::query_as::<_, Order>("SELECT * FROM orders WHERE id = $1")
        .bind(id)
        .fetch_optional(pool)
        .await?;
    row.ok_or_else(|| OrderError::NotFound(id.to_string()))
}
