"""
End-to-end OpenAI fine-tuning: upload file, create job, poll, return model ID.
Input:  training_file (JSONL path), model, suffix, n_epochs
Output: fine_tuned_model ID string
Raises: RuntimeError if job fails or is cancelled
"""
import time
from openai import OpenAI


def submit_finetune_job(
    training_file: str,
    model: str = "gpt-4o-mini-2024-07-18",
    suffix: str = "v1",
    n_epochs: int = 3,
    poll_interval_secs: int = 60,
) -> str:
    client = OpenAI()

    # Upload training file
    with open(training_file, "rb") as f:
        upload = client.files.create(file=f, purpose="fine-tune")
    print(f"Uploaded: {upload.id}")

    # Create fine-tuning job
    job = client.fine_tuning.jobs.create(
        training_file=upload.id,
        model=model,
        suffix=suffix,
        hyperparameters={"n_epochs": n_epochs},
    )
    print(f"Job created: {job.id}")

    # Poll until terminal state
    terminal = {"succeeded", "failed", "cancelled"}
    while job.status not in terminal:
        time.sleep(poll_interval_secs)
        job = client.fine_tuning.jobs.retrieve(job.id)
        print(f"Status: {job.status}")

    if job.status == "succeeded":
        print(f"Fine-tuned model: {job.fine_tuned_model}")
        return job.fine_tuned_model

    raise RuntimeError(
        f"Fine-tuning {job.status}: {getattr(job, 'error', 'no details')}"
    )
