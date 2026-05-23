#!/usr/bin/env python3
"""
watcher.py — Auto-heal watcher for multi-service platforms.
Checks all services every 60s, restarts on failure with cooldown and max restarts.

Deploy as a systemd user service. See watcher.service.
"""

import subprocess
import time
import logging
import urllib.request
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("watcher")

CHECK_INTERVAL   = 60    # seconds between full check cycles
MAX_RESTARTS     = 3     # max restarts per service per hour
RESTART_COOLDOWN = 300   # seconds between restart attempts per service


class ServiceCheck:
    def __init__(self, name: str, check_fn, restart_cmd: str):
        self.name = name
        self.check_fn = check_fn
        self.restart_cmd = restart_cmd
        self.restart_count = 0
        self.last_restart = 0.0

    def is_healthy(self) -> bool:
        try:
            return self.check_fn()
        except Exception as e:
            log.warning(f"{self.name}: health check failed: {e}")
            return False

    def restart(self) -> None:
        now = time.time()
        if now - self.last_restart < RESTART_COOLDOWN:
            log.warning(f"{self.name}: cooldown active, skipping restart")
            return
        if self.restart_count >= MAX_RESTARTS:
            log.error(f"{self.name}: max restarts reached — manual intervention needed")
            return
        log.info(f"Restarting {self.name}...")
        subprocess.run(self.restart_cmd, shell=True, check=True)
        self.restart_count += 1
        self.last_restart = now


def check_http(url: str, timeout: int = 5):
    def _check() -> bool:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = json.loads(resp.read())
        return data.get("status") in ("ok", "degraded")
    return _check


def check_systemd(service: str):
    def _check() -> bool:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", service],
            capture_output=True, text=True,
        )
        return result.stdout.strip() == "active"
    return _check


def check_celery(venv_path: str, app_name: str):
    def _check() -> bool:
        result = subprocess.run(
            [f"{venv_path}/bin/celery", "-A", app_name, "inspect", "ping"],
            capture_output=True, text=True, timeout=10,
        )
        return "pong" in result.stdout.lower()
    return _check


# --- Configure services to monitor ---
SERVICES = [
    # ServiceCheck(
    #     "nero-core",
    #     check_celery("/srv/nero/nero-core/.venv", "nero_core"),
    #     "systemctl --user restart nero-core",
    # ),
    # ServiceCheck(
    #     "nero-channel-web",
    #     check_http("http://127.0.0.1:8100/health"),
    #     "systemctl --user restart nero-channel-web",
    # ),
    # ServiceCheck(
    #     "nero-channel-tg",
    #     check_systemd("nero-channel-tg"),
    #     "systemctl --user restart nero-channel-tg",
    # ),
]


def main() -> None:
    log.info("Auto-heal watcher started")
    while True:
        for svc in SERVICES:
            if not svc.is_healthy():
                log.warning(f"{svc.name} is unhealthy")
                svc.restart()
            else:
                svc.restart_count = max(0, svc.restart_count - 1)  # decay on success
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
