# purpose: queue consumer worker — picks job, calls async-api client, post-processes
# consumes: redis stream entries OR SQS messages
# produces: code (worker module)
# depends-on: redis-py / boto3 + async-api client + ffmpeg
# token-budget-impact: ~200 tokens if loaded into LLM context
"""Worker consumer for video gen jobs."""
from __future__ import annotations

import subprocess
import sys


def process_one(job: dict) -> dict:
    # 1. submit via async-api client
    video_job = submit_async(job["prompt"], job["params"], provider=job["provider"],
                             idempotency_key=job["idempotency_key"])
    # 2. poll
    while True:
        status = poll(video_job.job_id)
        if status in ("succeeded", "failed-permanent", "timeout"):
            break
    # 3. on success, post-process
    if status == "succeeded":
        local = download(video_job.artefact_url)
        for op in job["post_processing"]:
            local = apply_ffmpeg_op(op, local)
        s3_url = upload(local)
        return {"status": "succeeded", "artefact_url": s3_url}
    return {"status": status}


def apply_ffmpeg_op(op: str, in_path: str) -> str:
    out_path = in_path.replace(".mp4", f"_{op}.mp4")
    if op == "concat":
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-i", "list.txt", "-c", "copy", out_path], check=True)
    elif op == "overlay-watermark":
        subprocess.run(["ffmpeg", "-y", "-i", in_path, "-i", "watermark.png", "-filter_complex", "overlay=10:10", out_path], check=True)
    elif op == "transcode-h264-720p":
        subprocess.run(["ffmpeg", "-y", "-i", in_path, "-vf", "scale=-1:720", "-c:v", "libx264", out_path], check=True)
    return out_path


def submit_async(prompt, params, provider, idempotency_key): ...
def poll(jid): ...
def download(url): ...
def upload(path): ...


if __name__ == "__main__":
    sys.exit(0)
