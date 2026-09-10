"""
purpose: Periodic eval-probe runner.
consumes: see AGENTS.md ## Prerequisites
produces: spec
depends-on: content/02-output-contract.xml schema for llm-observability
token-budget-impact: ≤500 tokens to fill
"""
# Rule r2: run held-out probes on a schedule (>= daily) and alert on a drop.
# Schedule with cron, e.g.  0 9 * * *  python3 eval-probe-runner.py  (09:00 UTC).
# Probe file: JSONL, one {"id": ..., "question": ..., "expected": ...} per line.
# Env vars: EVAL_PROBES (path), EVAL_METRICS_FILE (Prometheus textfile-collector
# target), EVAL_STATE_FILE (previous run), EVAL_DROP_PP (alert threshold, pp).
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from langfuse import get_client

# Rule r5: evals are never sampled. Set before the client is created.
os.environ["LANGFUSE_SAMPLE_RATE"] = "1.0"

PROBES = Path(os.environ.get("EVAL_PROBES", "probes/held-out.jsonl"))
METRICS_FILE = Path(os.environ.get("EVAL_METRICS_FILE", "/var/lib/node_exporter/llm_eval.prom"))
STATE_FILE = Path(os.environ.get("EVAL_STATE_FILE", ".eval-state.json"))
DROP_PP = float(os.environ.get("EVAL_DROP_PP", "5"))  # matches 05-examples: >5pp
RUN_NAME = "<spec-name>-daily"


def answer(question: str) -> str:
    """Production entry point under test; must already be traced (rule r1)."""
    raise NotImplementedError("wire to the traced application call")


def score(expected: str, actual: str) -> float:
    """1.0 / 0.0 per probe. Swap for an LLM-judge rubric if exact match is too strict."""
    return 1.0 if expected.strip().lower() in actual.strip().lower() else 0.0


def load_probes() -> list[dict]:
    return [json.loads(line) for line in PROBES.read_text().splitlines() if line.strip()]


def run() -> float:
    langfuse = get_client()
    probes = load_probes()
    total = 0.0
    with langfuse.start_as_current_span(name=RUN_NAME, input={"probes": len(probes)}) as run_span:
        for probe in probes:
            actual = answer(probe["question"])
            value = score(probe["expected"], actual)
            total += value
            # One score per probe keeps per-question history queryable in the vendor UI.
            langfuse.create_score(name="eval_accuracy", value=value, comment=probe["id"])
        accuracy = total / max(len(probes), 1)
        run_span.update(output={"accuracy": accuracy})
    langfuse.flush()
    return accuracy


def write_metrics(accuracy: float, probes: int) -> None:
    """Prometheus textfile-collector format; alert rules read llm_eval_accuracy."""
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    METRICS_FILE.write_text(
        "# TYPE llm_eval_accuracy gauge\n"
        f'llm_eval_accuracy{{run="{RUN_NAME}"}} {accuracy:.4f}\n'
        "# TYPE llm_eval_probes_total gauge\n"
        f'llm_eval_probes_total{{run="{RUN_NAME}"}} {probes}\n'
        "# TYPE llm_eval_last_run_timestamp gauge\n"
        f'llm_eval_last_run_timestamp{{run="{RUN_NAME}"}} {int(time.time())}\n'
    )


def main() -> int:
    previous = json.loads(STATE_FILE.read_text())["accuracy"] if STATE_FILE.exists() else None
    accuracy = run()
    write_metrics(accuracy, len(load_probes()))
    STATE_FILE.write_text(json.dumps({"accuracy": accuracy, "at": int(time.time())}))
    if previous is not None and (previous - accuracy) * 100 > DROP_PP:
        # Non-zero exit is the alert hook: cron mail, systemd OnFailure, or a pager wrapper.
        print(f"ALERT eval accuracy dropped {previous:.3f} -> {accuracy:.3f}", file=sys.stderr)
        return 2
    print(f"eval accuracy {accuracy:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
