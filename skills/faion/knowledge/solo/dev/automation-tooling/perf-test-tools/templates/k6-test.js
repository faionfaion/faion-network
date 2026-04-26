// k6-test.js — k6 load test starter with staged ramp and thresholds
// Run: k6 run k6-test.js
// Smoke: k6 run --vus 5 --duration 30s k6-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 50 },
    { duration: '5m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],     // error rate < 1%
    errors: ['rate<0.05'],
  },
};

const BASE_URL = __ENV.BASE_URL;
if (!BASE_URL) { throw new Error('BASE_URL env var required'); }

export function setup() {
  const res = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
    email: 'loadtest@example.com', password: 'testpassword',
  }), { headers: { 'Content-Type': 'application/json' } });
  return { token: res.json('access_token') };
}

export default function(data) {
  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type': 'application/json',
  };

  const res = http.get(`${BASE_URL}/api/products`, { headers });
  check(res, {
    'status 200': (r) => r.status === 200,
    'has data': (r) => r.json('data') !== undefined,
  }) || errorRate.add(1);

  sleep(Math.random() * 3 + 1);  // 1-4s think time
}
