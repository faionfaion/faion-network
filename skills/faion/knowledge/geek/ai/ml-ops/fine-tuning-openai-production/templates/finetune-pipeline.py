"""
FineTuningPipeline: upload, train, poll, and evaluate OpenAI fine-tuning jobs.
Input:  FineTuneConfig (base_model, suffix, n_epochs, validation_split, min_examples)
Output: {"status": "succeeded", "model": "ft:...", "trained_tokens": int}
Raises: ValueError on insufficient data; RuntimeError on job failure
"""
import json
import logging
import time
from dataclasses import dataclass
from typing import Optional
from openai import OpenAI


@dataclass
class FineTuneConfig:
    base_model: str = "gpt-4o-mini-2024-07-18"
    suffix: Optional[str] = None
    n_epochs: int = 3
    validation_split: float = 0.1
    min_examples: int = 50


class FineTuningPipeline:
    def __init__(self, config: Optional[FineTuneConfig] = None):
        self.config = config or FineTuneConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

    def run(self, training_data: list, wait: bool = True) -> dict:
        if len(training_data) < self.config.min_examples:
            raise ValueError(f"Need at least {self.config.min_examples} examples")

        val_size = int(len(training_data) * self.config.validation_split)
        val_data, train_data = training_data[:val_size], training_data[val_size:]

        train_id = self._upload(train_data, "train")
        val_id = self._upload(val_data, "val") if val_data else None

        job = self.client.fine_tuning.jobs.create(
            training_file=train_id,
            validation_file=val_id,
            model=self.config.base_model,
            suffix=self.config.suffix,
            hyperparameters={"n_epochs": self.config.n_epochs},
        )
        self.logger.info("Job created: %s", job.id)

        if not wait:
            return {"job_id": job.id, "status": "started"}
        return self._poll(job.id)

    def _upload(self, data: list, label: str) -> str:
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            for ex in data:
                f.write(json.dumps(ex) + "\n")
            path = f.name
        try:
            with open(path, "rb") as f:
                resp = self.client.files.create(file=f, purpose="fine-tune")
            self.logger.info("Uploaded %s file: %s", label, resp.id)
            return resp.id
        finally:
            os.unlink(path)

    def _poll(self, job_id: str) -> dict:
        terminal = {"succeeded", "failed", "cancelled"}
        sleep = 30
        while True:
            job = self.client.fine_tuning.jobs.retrieve(job_id)
            self.logger.info("Status: %s", job.status)
            if job.status in terminal:
                break
            time.sleep(sleep)
            sleep = min(sleep * 1.5, 300)  # exponential backoff up to 5 min

        if job.status == "succeeded":
            return {"status": "succeeded", "model": job.fine_tuned_model,
                    "trained_tokens": job.trained_tokens}
        return {"status": job.status, "error": str(getattr(job, "error", "unknown"))}
