// purpose: k6 load-test probe verifying RateLimit-* headers and 429 + Retry-After behaviour.
// consumes: see content/02-output-contract.xml inputs for rate-limiting
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
// Usage: BASE=https://api.example.com TOKEN=xxx k6 run --vus 50 --duration 30s k6-rl-probe.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const URL   = __ENV.URL   || `${__ENV.BASE}/api/search`;
const TOKEN = __ENV.TOKEN || '';

export default function () {
  const res = http.get(URL, {
    headers: TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {},
  });

  check(res, {
    'has X-RateLimit-Limit header':     (r) => !!r.headers['X-Ratelimit-Limit'],
    'has X-RateLimit-Remaining header': (r) => !!r.headers['X-Ratelimit-Remaining'],
    '429 has Retry-After header':       (r) => r.status !== 429 || !!r.headers['Retry-After'],
    '429 body has retryAfter field':    (r) =>
      r.status !== 429 || r.json('error.retryAfter') !== null,
    'status is 200 or 429':             (r) => r.status === 200 || r.status === 429,
  });

  sleep(0.05);
}
