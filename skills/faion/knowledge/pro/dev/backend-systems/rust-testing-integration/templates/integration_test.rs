// purpose: Rust integration test skeleton: oneshot + testcontainers + insta.
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml (rust-testing-integration)
// depends-on: content/01-core-rules.xml
// token-budget-impact: small (template is loaded only when an artefact is being authored)
use axum::body::Body;
use axum::http::{Request, StatusCode};
use tower::ServiceExt;

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn it_returns_user_on_get_users_id() {
    let app = my_app::build_router(test_db_pool().await).await;
    let resp = app
        .oneshot(
            Request::builder()
                .uri("/users/1")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .expect("router should respond");
    assert_eq!(resp.status(), StatusCode::OK);
    let body = axum::body::to_bytes(resp.into_body(), 64 * 1024).await.unwrap();
    insta::assert_json_snapshot!(serde_json::from_slice::<serde_json::Value>(&body).unwrap());
}

async fn test_db_pool() -> sqlx::PgPool {
    // Per-test schema: CREATE SCHEMA test_<uuid>, run migrations, DROP on teardown.
    todo!("replace with project-specific fixture")
}
