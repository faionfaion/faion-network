// Integration test skeleton for Axum handlers using tower::ServiceExt::oneshot.
// Replace `myapp::app` and `myapp::test_state` with your actual module paths.
//
// Run with: cargo nextest run --test-threads=4
// or: cargo test --test <test_file>

use axum::body::Body;
use axum::http::{Request, StatusCode};
use http_body_util::BodyExt;
use serde_json::{json, Value};
use tower::ServiceExt;

// Import your app factory and test-state helper
// use myapp::{app, test_state};

/// Sends a JSON request to the app and returns (status, parsed body).
async fn call(
    router: axum::Router,
    method: &str,
    uri: &str,
    body: Option<Value>,
) -> (StatusCode, Value) {
    let body_bytes = match body {
        Some(v) => Body::from(v.to_string()),
        None => Body::empty(),
    };
    let mut builder = Request::builder()
        .method(method)
        .uri(uri)
        .header("content-type", "application/json");
    let req = builder.body(body_bytes).unwrap();

    let resp = router.oneshot(req).await.unwrap();
    let status = resp.status();
    let bytes = resp.into_body().collect().await.unwrap().to_bytes();
    let json: Value = serde_json::from_slice(&bytes).unwrap_or(Value::Null);
    (status, json)
}

#[tokio::test]
async fn create_resource_201() {
    // let state = test_state().await;
    // let (status, body) = call(
    //     app(state),
    //     "POST",
    //     "/v1/resources",
    //     Some(json!({"name": "example", "email": "a@example.com", "password": "longenough"})),
    // ).await;
    // assert_eq!(status, StatusCode::CREATED);
    // assert_eq!(body["email"], "a@example.com");
}

#[tokio::test]
async fn create_resource_422_validation() {
    // let state = test_state().await;
    // let (status, _body) = call(
    //     app(state),
    //     "POST",
    //     "/v1/resources",
    //     Some(json!({"name": "x", "email": "not-an-email", "password": "short"})),
    // ).await;
    // assert_eq!(status, StatusCode::UNPROCESSABLE_ENTITY);
}

#[tokio::test]
async fn get_resource_404() {
    // let state = test_state().await;
    // let (status, _body) = call(app(state), "GET", "/v1/resources/99999", None).await;
    // assert_eq!(status, StatusCode::NOT_FOUND);
}
