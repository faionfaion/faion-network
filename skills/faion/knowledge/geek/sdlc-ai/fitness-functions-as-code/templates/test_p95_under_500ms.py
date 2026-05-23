# purpose: latency fitness function — checkout p95 under 500ms
# consumes: loadtests/checkout.yaml
# produces: pass/fail
# depends-on: ADR docs/adr/0012-sla.md
# token-budget-impact: ~180 tokens
import json
import subprocess


def test_checkout_p95_under_500ms() -> None:
    """ADR 0012: checkout endpoint p95 must remain under 500ms at 100 RPS."""
    out = subprocess.check_output(["k6", "run", "--summary-export=/tmp/k6.json", "loadtests/checkout.yaml"]).decode()
    with open("/tmp/k6.json") as f:
        data = json.load(f)
    p95 = data["metrics"]["http_req_duration"]["values"]["p(95)"]
    assert p95 < 500, f"p95 {p95}ms exceeds 500ms"
