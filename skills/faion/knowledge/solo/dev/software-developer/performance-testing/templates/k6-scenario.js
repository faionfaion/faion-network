// purpose: k6 load-test scenario with steady + spike stages and SLO thresholds.
// consumes: see content/02-output-contract.xml inputs for performance-testing
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    steady: {
      executor: 'constant-arrival-rate',
      rate: 500, timeUnit: '1s', duration: '10m',
      preAllocatedVUs: 200, maxVUs: 500,
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<300', 'p(99)<800'],
    http_req_failed: ['rate<0.01'],
  },
  discardResponseBodies: true,
};

export default function () {
  const r = http.get('https://staging.example.com/api/users/123');
  check(r, { 'status 200': (res) => res.status === 200 });
}
