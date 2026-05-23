# purpose: FastAPI graceful-shutdown handler — SIGTERM flips readiness to 503, drain completes in-flight reqs
# consumes: SIGTERM signal + readiness probe path
# produces: drain_on_sigterm=true segment of content/02-output-contract.xml artefact
# depends-on: content/01-core-rules.xml (drain-on-sigterm)
# token-budget-impact: ~300 tokens when loaded as context

from __future__ import annotations

import asyncio
import signal

from fastapi import FastAPI, Response

app = FastAPI()
_is_shutting_down: bool = False


@app.on_event("startup")
async def _install_handlers() -> None:
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, _handle_sigterm)
    loop.add_signal_handler(signal.SIGINT,  _handle_sigterm)


def _handle_sigterm() -> None:
    global _is_shutting_down
    _is_shutting_down = True
    # readiness probe will return 503 on next poll;
    # LB removes this backend within one health-check interval (≤ 10–30 s)


@app.get("/health/live")
async def live(response: Response):
    return {"status": "alive"}


@app.get("/health/ready")
async def ready(response: Response):
    if _is_shutting_down:
        response.status_code = 503
        return {"status": "shutting_down"}
    return {"status": "ready"}


@app.get("/")
async def root():
    return {"hello": "world"}
