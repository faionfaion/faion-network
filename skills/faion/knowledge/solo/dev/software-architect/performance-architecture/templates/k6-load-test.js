/**
 * k6-load-test.js — production-shaped load test with steady + spike scenarios,
 * SLO-aligned thresholds, and randomized key distribution to simulate Pareto access patterns.
 *
 * Usage:
 *   k6 run -e BASE_URL=https://api.example.com k6-load-test.js
 *
 * Requires: k6 >= 0.46
 * Docs: https://k6.io/docs/
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const checkoutDuration = new Trend('checkout_duration', true);

// ---------------------------------------------------------------------------
// Scenarios
// ---------------------------------------------------------------------------
export const options = {
  scenarios: {
    // Steady-state: hold 200 RPS for 5 minutes to establish baseline
    steady: {
      executor: 'constant-arrival-rate',
      rate: 200,
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
    // Spike: ramp from 200 → 1000 RPS over 1 minute, then back down
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 200,
      timeUnit: '1s',
      startTime: '5m',   // starts after steady phase completes
      preAllocatedVUs: 100,
      maxVUs: 500,
      stages: [
        { target: 1000, duration: '1m' },  // ramp up
        { target: 1000, duration: '2m' },  // hold
        { target: 200,  duration: '1m' },  // ramp down
      ],
    },
  },

  // ---------------------------------------------------------------------------
  // Thresholds — map directly to your SLOs
  // Adjust thresholds to match your tier (see content/01-slos-and-layers.xml)
  // ---------------------------------------------------------------------------
  thresholds: {
    // p95 < 300ms, p99 < 800ms (Growth tier)
    http_req_duration: ['p(95)<300', 'p(99)<800'],
    // Error rate < 0.5%
    http_req_failed: ['rate<0.005'],
    // Custom: checkout flow p95 < 500ms
    checkout_duration: ['p(95)<500'],
    // Custom error rate
    errors: ['rate<0.005'],
  },
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Simulate Pareto distribution: 20% of IDs get 80% of traffic */
function paretoId(max = 10000) {
  const u = Math.random();
  // Inverse Pareto CDF with alpha=1.16 (80/20 split)
  return Math.floor(max * (1 - Math.pow(u, 1 / 1.16))) + 1;
}

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Default function — runs once per VU iteration
// ---------------------------------------------------------------------------
export default function () {
  const itemId = paretoId(10000);
  const userId = paretoId(5000);

  // ---- Read: product detail ------------------------------------------------
  const detailRes = http.get(`${BASE_URL}/api/items/${itemId}`, {
    tags: { name: 'item_detail' },
  });

  check(detailRes, {
    'item detail: status 200': (r) => r.status === 200,
    'item detail: has id':     (r) => r.json('id') !== undefined,
  }) || errorRate.add(1);

  sleep(0.5);  // think time between requests

  // ---- Write: add to cart --------------------------------------------------
  const cartRes = http.post(
    `${BASE_URL}/api/cart`,
    JSON.stringify({ user_id: userId, item_id: itemId, qty: 1 }),
    {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: 'cart_add' },
    }
  );

  check(cartRes, {
    'cart add: status 200 or 201': (r) => r.status === 200 || r.status === 201,
  }) || errorRate.add(1);

  sleep(1);

  // ---- Write: checkout (critical path) ------------------------------------
  const start = Date.now();
  const checkoutRes = http.post(
    `${BASE_URL}/api/checkout`,
    JSON.stringify({ user_id: userId }),
    {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: 'checkout' },
      timeout: '10s',
    }
  );
  checkoutDuration.add(Date.now() - start);

  check(checkoutRes, {
    'checkout: status 200 or 202': (r) => r.status === 200 || r.status === 202,
  }) || errorRate.add(1);

  sleep(Math.random() * 2 + 1);  // 1–3s think time
}

// ---------------------------------------------------------------------------
// Teardown: print summary (optional — k6 already prints thresholds)
// ---------------------------------------------------------------------------
export function handleSummary(data) {
  return {
    'stdout': JSON.stringify({
      p95_ms:     data.metrics.http_req_duration.values['p(95)'],
      p99_ms:     data.metrics.http_req_duration.values['p(99)'],
      error_rate: data.metrics.http_req_failed.values.rate,
      rps:        data.metrics.http_reqs.values.rate,
    }, null, 2),
  };
}
