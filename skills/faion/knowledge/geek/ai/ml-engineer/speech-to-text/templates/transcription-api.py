"""
FastAPI transcription endpoint with sync and async (webhook) modes.
Requires: pip install fastapi python-multipart httpx

Run: uvicorn transcription_api:app --reload
"""

from __future__ import annotations

import os
import tempfile
import uuid
from pathlib import Path
from typing import Optional

import httpx
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from transcription_service import TranscriptionConfig, TranscriptionProvider, TranscriptionService

app = FastAPI(title="Transcription API", version="1.0.0")

# Singleton service — primary: GPT-4o Mini, fallback: faster-whisper
_service = TranscriptionService(TranscriptionConfig(
    provider=TranscriptionProvider.OPENAI_GPT4O_MINI,
    fallback_provider=TranscriptionProvider.FASTER_WHISPER,
    word_timestamps=True,
))

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".webm", ".mp4"}


class TranscriptionResponse(BaseModel):
    success: bool
    text: Optional[str] = None
    segments: Optional[list] = None
    duration: Optional[float] = None
    fallback_used: Optional[bool] = None
    error: Optional[str] = None


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_sync(
    file: UploadFile = File(...),
    language: Optional[str] = None,
) -> TranscriptionResponse:
    """Synchronous transcription. Returns result immediately (use for files <5 min)."""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format {ext!r}. Allowed: {sorted(ALLOWED_EXTENSIONS)}")

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        _service.config.language = language
        result = _service.transcribe(tmp_path)
        return TranscriptionResponse(**result)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@app.post("/transcribe/async")
async def transcribe_async(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    webhook_url: Optional[str] = None,
    language: Optional[str] = None,
) -> JSONResponse:
    """Async transcription. Returns job_id immediately; posts result to webhook_url when done."""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {ext}")

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    job_id = str(uuid.uuid4())
    background_tasks.add_task(_process_async, job_id, tmp_path, webhook_url, language)
    return JSONResponse({"job_id": job_id, "status": "queued"})


async def _process_async(job_id: str, file_path: str, webhook_url: str | None, language: str | None) -> None:
    """Background task: transcribe and deliver via webhook."""
    try:
        _service.config.language = language
        result = _service.transcribe(file_path)
        payload = {"job_id": job_id, "result": result}

        if webhook_url:
            async with httpx.AsyncClient(timeout=30) as client:
                await client.post(webhook_url, json=payload)
    finally:
        Path(file_path).unlink(missing_ok=True)
