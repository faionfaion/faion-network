// k6-rate-limit-check.js — verify rate limit headers and 429 boundary behavior.
// Usage: k6 run -e BASE=https://api.example.com -e TOKEN=your_token k6-rate-limit-check.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = { vus: 5, duration: '90s' };

export default function () {
  const r = http.get(`${__ENV.BASE}/api/search?q=hello`, {
    headers: { Authorization: `Bearer ${__ENV.TOKEN}` },
    tags: { name: 'search' },
  });
  check(r, {
    'has RateLimit-Limit header': (x) =>
      !!x.headers['X-Ratelimit-Limit'] || !!x.headers['Ratelimit-Limit'],
    'on 429 has Retry-After': (x) =>
      x.status !== 429 || !!x.headers['Retry-After'],
    'no 5xx': (x) => x.status < 500,
  });
  sleep(0.1);
}
