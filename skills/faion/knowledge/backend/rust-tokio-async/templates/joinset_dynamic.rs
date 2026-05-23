// purpose: JoinSet for dynamic task groups with cancellation on drop.
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml (rust-tokio-async)
// depends-on: content/01-core-rules.xml
// token-budget-impact: small (template is loaded only when an artefact is being authored)
use tokio::task::JoinSet;
use tokio::time::{timeout, Duration};

pub async fn fan_out<F, T>(work: Vec<F>, per_task_timeout: Duration) -> Vec<Result<T, String>>
where
    F: std::future::Future<Output = T> + Send + 'static,
    T: Send + 'static,
{
    let mut set: JoinSet<Result<T, String>> = JoinSet::new();
    for fut in work {
        set.spawn(async move {
            match timeout(per_task_timeout, fut).await {
                Ok(t) => Ok(t),
                Err(_) => Err("task timed out".into()),
            }
        });
    }
    let mut out = Vec::new();
    while let Some(res) = set.join_next().await {
        out.push(res.unwrap_or_else(|e| Err(format!("join error: {e}"))));
    }
    out
}
