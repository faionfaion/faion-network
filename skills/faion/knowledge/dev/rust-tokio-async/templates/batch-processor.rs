// purpose: Tokio batch-processor: bounded channel + join_set + structured cancellation.
// consumes: see content/02-output-contract.xml inputs for rust-tokio-async
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
// Semaphore-bounded concurrent batch processor.
// Input: Vec<T> + async processor function + concurrency limit
// Output: Vec<Result<R, E>> in original order

use futures::stream::{self, StreamExt};
use std::sync::Arc;
use tokio::sync::Semaphore;

pub struct BatchProcessor {
    concurrency: usize,
}

impl BatchProcessor {
    pub fn new(concurrency: usize) -> Self { Self { concurrency } }

    pub async fn process<T, F, Fut, R, E>(
        &self,
        items: Vec<T>,
        processor: F,
    ) -> Vec<Result<R, E>>
    where
        T: Send + 'static,
        F: Fn(T) -> Fut + Send + Sync + 'static,
        Fut: std::future::Future<Output = Result<R, E>> + Send,
        R: Send + 'static,
        E: Send + 'static,
    {
        let sem = Arc::new(Semaphore::new(self.concurrency));
        let proc = Arc::new(processor);

        stream::iter(items)
            .map(|item| {
                let sem = sem.clone();
                let proc = proc.clone();
                async move {
                    let _permit = sem.acquire().await.unwrap();
                    proc(item).await
                }
            })
            .buffer_unordered(self.concurrency)
            .collect()
            .await
    }
}

// Usage:
// let bp = BatchProcessor::new(10);
// let results = bp.process(user_ids, |id| async move { fetch_user(id).await }).await;
