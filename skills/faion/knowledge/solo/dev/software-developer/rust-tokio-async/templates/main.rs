// purpose: Tokio service skeleton: multi_thread runtime, JoinSet, timeout, CancellationToken shutdown.
// consumes: see content/02-output-contract.xml inputs for rust-tokio-async
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context

use std::time::Duration;
use tokio::sync::mpsc;
use tokio::task::JoinSet;
use tokio::time::timeout;
use tokio_util::sync::CancellationToken;

#[tokio::main(flavor = "multi_thread", worker_threads = 8)]
async fn main() -> anyhow::Result<()> {
    let shutdown = CancellationToken::new();
    let (tx, mut rx) = mpsc::channel::<u64>(1024);

    let mut set = JoinSet::new();
    for n in 0..16u64 {
        let token = shutdown.clone();
        let tx = tx.clone();
        set.spawn(async move {
            tokio::select! {
                _ = token.cancelled() => Ok::<(), anyhow::Error>(()),
                r = timeout(Duration::from_secs(3), do_work(n)) => {
                    let v = r??;
                    tx.send(v).await?;
                    Ok(())
                }
            }
        });
    }
    drop(tx);

    let _ = tokio::signal::ctrl_c().await;
    shutdown.cancel();
    while let Some(res) = set.join_next().await {
        let _ = res?;
    }
    while let Some(_v) = rx.recv().await {}
    Ok(())
}

async fn do_work(n: u64) -> anyhow::Result<u64> { Ok(n * 2) }
