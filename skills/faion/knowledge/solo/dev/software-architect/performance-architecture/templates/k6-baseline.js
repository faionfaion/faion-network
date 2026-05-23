// __faion_header_v1__
// purpose: k6 baseline script with SLO-derived thresholds.
// consumes: see content/02-output-contract.xml
// produces: spec; depends-on: content/01-core-rules.xml#r1-numeric-slos-only
// faion_header_json: {"__faion_header__":{"purpose":"k6 baseline script with SLO-derived thresholds.","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#r1-numeric-slos-only","token_budget_impact":"~150 tokens when loaded"}}
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '3m', target: 200 },
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/v1/items');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
