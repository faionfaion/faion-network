<!-- purpose: smoke checklist for rust-testing-antipatterns -->
<!-- consumes: PR diff -->
<!-- produces: review verdict -->
<!-- depends-on: scripts/validate-rust-testing-antipatterns.py -->
<!-- token-budget-impact: ~250 tokens -->

# Rust test review checklist

- [ ] No tokio::time::sleep in tests — use tokio::test(start_paused=true) + advance.
- [ ] No Utc::now() in assertion paths — inject a Clock trait.
- [ ] No static mut / shared global state across tests.
- [ ] No hardcoded ports — bind to 0 and read the assigned port.
- [ ] mockall predicates referenced from the documented API (cargo check passes).
- [ ] clippy denies: unwrap_used, expect_used active in test target.
