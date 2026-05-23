// purpose: Rust async unit test using tokio::test
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for testing-backend-languages
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn charge_marks_order_as_charged() {
        let pool = test_pool().await;
        let order = create_order(&pool, 1000).await.unwrap();
        let result = charge_order(&pool, &order.id).await.unwrap();
        assert_eq!(result.status, "charged");
    }
}
