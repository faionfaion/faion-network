// k6-scenario.js — load test template with steady + spike scenarios and SLO thresholds
// Usage: BASE=https://staging.example.com k6 run k6-scenario.js
// Requires: k6 (https://k6.io/docs)
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  thresholds: {
    http_req_failed: ['rate<0.01'],          // error rate < 1%
    http_req_duration: ['p(95)<500', 'p(99)<1000'],  // p95 < 500ms
  },
  scenarios: {
    steady: {
      executor: 'constant-arrival-rate',
      rate: 50,
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 50,
    },
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 0,
      timeUnit: '1s',
      stages: [
        { duration: '30s', target: 200 },
        { duration: '1m',  target: 200 },
        { duration: '30s', target: 0 },
      ],
      preAllocatedVUs: 200,
      startTime: '5m30s',
    },
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE}/api/search?q=hello`);
  check(res, { 'status 200': (r) => r.status === 200 });
}
