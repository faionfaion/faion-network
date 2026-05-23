// purpose: Rust #[cfg(test)] mod tests skeleton with mockall + explicit tokio flavor.
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml (rust-testing-unit)
// depends-on: content/01-core-rules.xml
// token-budget-impact: small (template is loaded only when an artefact is being authored)
#[cfg(test)]
mod tests {
    use super::*;
    use mockall::mock;

    mock! {
        pub Repo {}
        impl crate::Repo for Repo {
            fn fetch(&self, id: u64) -> Result<String, crate::Error>;
        }
    }

    #[tokio::test(flavor = "current_thread")]
    async fn fetches_user_when_repo_returns_ok() {
        let mut repo = MockRepo::new();
        repo.expect_fetch().with(mockall::predicate::eq(1)).returning(|_| Ok("alice".into()));
        let svc = crate::Service::new(Box::new(repo));
        let result = svc.user_label(1).await.expect("service should return label");
        assert_eq!(result, "alice");
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn timeout_completes_under_virtual_time() {
        tokio::time::pause();
        let fut = tokio::time::sleep(std::time::Duration::from_secs(60));
        tokio::time::advance(std::time::Duration::from_secs(61)).await;
        fut.await;
    }
}
