"""
watchdog-notify.py — Python NOTIFY_SOCKET sender for systemd watchdog
Requires service with: Type=notify, WatchdogSec=30
"""

import os
import socket
import asyncio
from fastapi import FastAPI

app = FastAPI()


def notify_watchdog() -> None:
    """Notify systemd watchdog that service is alive."""
    sock_path = os.environ.get("NOTIFY_SOCKET")
    if not sock_path:
        return
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        sock.connect(sock_path)
        sock.send(b"WATCHDOG=1")
    finally:
        sock.close()


async def watchdog_loop() -> None:
    """Background task to ping systemd watchdog every WatchdogSec/2 seconds."""
    while True:
        notify_watchdog()
        await asyncio.sleep(15)  # WatchdogSec=30 / 2


@app.on_event("startup")
async def start_watchdog() -> None:
    asyncio.create_task(watchdog_loop())
