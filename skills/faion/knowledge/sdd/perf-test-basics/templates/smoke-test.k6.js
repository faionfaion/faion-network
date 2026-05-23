// __faion_header_v1__
// purpose: k6 smoke test asserting p95 threshold
// consumes: see content/02-output-contract.xml
// produces: spec; depends-on: content/01-core-rules.xml#slo-driven-baselines
// faion_header_json: {"__faion_header__":{"purpose":"k6 smoke test asserting p95 threshold","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#slo-driven-baselines","token_budget_impact":"~150 tokens when loaded"}}
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '60s',
  thresholds: {
    http_req_duration: ['p(95)<300'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/v1/checkout`);
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
