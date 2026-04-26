"""
Production evaluator with persistent JSONL logging.
Input:  log_path (JSONL file path), sample_rate (0.0-1.0)
Output: appends evaluation records to JSONL file; returns record dict or None
"""
import json
import random
import logging
from datetime import datetime
from pathlib import Path


class PersistentProductionEvaluator:
    ERROR_PATTERNS = ["sorry, i cannot", "as an ai", "i'm unable", "i cannot assist"]

    def __init__(self, log_path: str, sample_rate: float = 0.1):
        self.log_path = Path(log_path)
        self.sample_rate = sample_rate
        self.logger = logging.getLogger(__name__)

    def evaluate_request(
        self, input: str, output: str, metadata: dict = None
    ) -> dict | None:
        if random.random() >= self.sample_rate:
            return None

        checks = {
            "non_empty": len(output.strip()) > 0,
            "reasonable_length": 10 < len(output) < 10_000,
            "no_error_patterns": not any(
                p in output.lower() for p in self.ERROR_PATTERNS
            ),
        }
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "input_length": len(input),
            "output_length": len(output),
            "checks": checks,
            "metadata": metadata or {},
        }
        with self.log_path.open("a") as f:
            f.write(json.dumps(record) + "\n")

        failed = {k for k, v in checks.items() if not v}
        if failed:
            self.logger.warning("Quality checks failed: %s", failed)

        return record
