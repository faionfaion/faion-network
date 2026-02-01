---
id: perf-test-tools
name: "Performance Testing Tools"
domain: DEV
skill: faion-software-developer
category: "development"
parent: "performance-testing"
---

# Performance Testing Tools

## Overview

Tools and frameworks for load testing, stress testing, and performance monitoring. Includes Locust (Python), k6 (JavaScript), and CI/CD integration patterns.

## Locust Load Testing

```python
# locustfile.py
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import json
import random

class WebsiteUser(HttpUser):
    """Simulates typical user behavior."""

    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    host = "https://api.example.com"

    def on_start(self):
        """Called when user starts. Login and setup."""
        response = self.client.post("/auth/login", json={
            "email": f"user{random.randint(1, 1000)}@example.com",
            "password": "testpassword"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}

    @task(10)  # Weight: 10x more likely than weight 1
    def browse_products(self):
        """Simulate browsing products."""
        self.client.get("/api/products", headers=self.headers)

    @task(5)
    def view_product_detail(self):
        """View a specific product."""
        product_id = random.randint(1, 100)
        self.client.get(f"/api/products/{product_id}", headers=self.headers)

    @task(3)
    def search_products(self):
        """Search for products."""
        terms = ["laptop", "phone", "headphones", "camera", "tablet"]
        self.client.get(
            f"/api/products/search?q={random.choice(terms)}",
            headers=self.headers
        )

    @task(1)
    def add_to_cart(self):
        """Add item to cart."""
        self.client.post("/api/cart/items", json={
            "product_id": random.randint(1, 100),
            "quantity": random.randint(1, 3)
        }, headers=self.headers)

    @task(1)
    def checkout(self):
        """Complete checkout (less frequent)."""
        self.client.post("/api/orders", json={
            "payment_method": "card",
            "shipping_address_id": 1
        }, headers=self.headers)


class AdminUser(HttpUser):
    """Simulates admin operations (fewer users)."""

    wait_time = between(2, 10)
    weight = 1  # 1/10th of regular users

    @task
    def view_dashboard(self):
        self.client.get("/admin/dashboard", headers=self.admin_headers)

    @task
    def export_report(self):
        self.client.get("/admin/reports/sales?format=csv", headers=self.admin_headers)


# Custom metrics
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, **kwargs):
    """Log custom metrics."""
    if response_time > 2000:  # > 2 seconds
        print(f"SLOW REQUEST: {name} took {response_time}ms")

# Run with: locust -f locustfile.py --host=https://api.example.com
# Or headless: locust -f locustfile.py --headless -u 100 -r 10 -t 5m
```

## k6 Load Testing

```javascript
// k6-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const loginDuration = new Trend('login_duration');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
    errors: ['rate<0.05'],             // Custom error rate < 5%
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export function setup() {
  // Run once before test
  const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
    email: 'loadtest@example.com',
    password: 'testpassword',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  return { token: loginRes.json('access_token') };
}

export default function(data) {
  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type': 'application/json',
  };

  // Test scenario: Browse and purchase
  const scenarios = [
    () => browseProducts(headers),
    () => searchProducts(headers),
    () => viewProduct(headers),
    () => addToCart(headers),
  ];

  // Random scenario selection
  const scenario = scenarios[Math.floor(Math.random() * scenarios.length)];
  scenario();

  sleep(Math.random() * 3 + 1);  // 1-4 seconds between requests
}

function browseProducts(headers) {
  const res = http.get(`${BASE_URL}/api/products?page=1&limit=20`, { headers });

  check(res, {
    'products status is 200': (r) => r.status === 200,
    'products list not empty': (r) => r.json('data').length > 0,
  }) || errorRate.add(1);
}

function searchProducts(headers) {
  const terms = ['laptop', 'phone', 'tablet'];
  const term = terms[Math.floor(Math.random() * terms.length)];

  const res = http.get(`${BASE_URL}/api/products/search?q=${term}`, { headers });

  check(res, {
    'search status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);
}

function viewProduct(headers) {
  const productId = Math.floor(Math.random() * 100) + 1;
  const res = http.get(`${BASE_URL}/api/products/${productId}`, { headers });

  check(res, {
    'product detail status is 200': (r) => r.status === 200,
    'product has name': (r) => r.json('name') !== undefined,
  }) || errorRate.add(1);
}

function addToCart(headers) {
  const payload = JSON.stringify({
    product_id: Math.floor(Math.random() * 100) + 1,
    quantity: 1,
  });

  const res = http.post(`${BASE_URL}/api/cart/items`, payload, { headers });

  check(res, {
    'add to cart successful': (r) => r.status === 201 || r.status === 200,
  }) || errorRate.add(1);
}

// Run with: k6 run k6-test.js
// Or with cloud: k6 cloud k6-test.js
```

## CI/CD Performance Gates

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  load-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Start application
        run: |
          docker-compose up -d
          sleep 30  # Wait for startup

      - name: Run k6 load test
        uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/performance/k6-test.js
          flags: --out json=results.json

      - name: Check performance thresholds
        run: |
          python scripts/check_performance.py results.json

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: performance-results
          path: results.json

  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run benchmarks
        run: |
          pytest tests/benchmarks/ \
            --benchmark-only \
            --benchmark-json=benchmark.json \
            --benchmark-compare-fail=mean:10%  # Fail if 10% slower

      - name: Store benchmark result
        uses: benchmark-action/github-action-benchmark@v1
        with:
          tool: 'pytest'
          output-file-path: benchmark.json
          fail-on-alert: true
          alert-threshold: '150%'
```

## References

- [Locust Documentation](https://docs.locust.io/)
- [k6 Documentation](https://k6.io/docs/)
- [GitHub Actions for Performance Testing](https://docs.github.com/en/actions)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement perf-test-tools pattern | haiku | Straightforward implementation |
| Review perf-test-tools implementation | sonnet | Requires code analysis |
| Optimize perf-test-tools design | opus | Complex trade-offs |

