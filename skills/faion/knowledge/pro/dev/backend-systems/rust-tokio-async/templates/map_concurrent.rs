// src/concurrent.rs
// Generic bounded-parallel helper using futures::stream::buffer_unordered + Semaphore.
// Collects all results (Ok or Err) without short-circuiting.
// For fail-fast, use .try_collect() instead of .collect().
use std::sync::Arc;

use futures::{stream, StreamExt, TryStreamExt};
use tokio::sync::Semaphore;

/// Run `f` on each item with at most `concurrency` concurrent tasks.
/// Returns Ok(Vec<R>) if all succeed, Err on first failure (try_collect).
pub async fn map_concurrent<T, R, E, F, Fut>(
    items: Vec<T>,
    concurrency: usize,
    f: F,
) -> Result<Vec<R>, E>
where
    T: Send + 'static,
    F: Fn(T) -> Fut + Send + Sync + 'static,
    Fut: std::future::Future<Output = Result<R, E>> + Send,
    R: Send + 'static,
    E: Send + 'static,
{
    let sem = Arc::new(Semaphore::new(concurrency));
    let f = Arc::new(f);

    stream::iter(items)
        .map(|item| {
            let sem = sem.clone();
            let f = f.clone();
            async move {
                // acquire_owned: permit lives as long as the task, not a borrow scope.
                let _permit = sem.acquire_owned().await.expect("semaphore closed");
                f(item).await
            }
        })
        .buffer_unordered(concurrency)
        .try_collect()
        .await
}
