// __faion_header_v1__
// purpose: k6 load test with thresholds + stages
// consumes: see content/02-output-contract.xml
// produces: code; depends-on: content/01-core-rules.xml#tool-by-team-language
// faion_header_json: {"__faion_header__":{"purpose":"k6 load test with thresholds + stages","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#tool-by-team-language","token_budget_impact":"~150 tokens when loaded"}}
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '60s', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<300', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/v1/checkout`);
  check(res, { 'status 200': (r) => r.status === 200 });
}
