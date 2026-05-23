// purpose: buffer_unordered + Semaphore bounded-concurrency stream.
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml (rust-tokio-async)
// depends-on: content/01-core-rules.xml
// token-budget-impact: small (template is loaded only when an artefact is being authored)
use futures::stream::{self, StreamExt};
use std::sync::Arc;
use tokio::sync::Semaphore;
use tokio::time::{timeout, Duration};

pub async fn process_bounded<I, T, F, Fut, E>(
    inputs: I,
    concurrency: usize,
    per_call_timeout: Duration,
    work: F,
) -> Vec<Result<T, E>>
where
    I: IntoIterator<Item = u64>,
    F: Fn(u64) -> Fut + Clone + Send + Sync + 'static,
    Fut: std::future::Future<Output = Result<T, E>> + Send,
    T: Send + 'static,
    E: From<tokio::time::error::Elapsed> + Send + 'static,
{
    let sem = Arc::new(Semaphore::new(concurrency));
    stream::iter(inputs)
        .map(|id| {
            let sem = sem.clone();
            let work = work.clone();
            async move {
                let _permit = sem.acquire_owned().await.expect("semaphore closed");
                match timeout(per_call_timeout, work(id)).await {
                    Ok(res) => res,
                    Err(elapsed) => Err(elapsed.into()),
                }
            }
        })
        .buffer_unordered(concurrency)
        .collect()
        .await
}
