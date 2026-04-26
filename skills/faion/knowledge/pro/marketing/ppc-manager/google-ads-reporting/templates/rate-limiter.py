"""
rate_limiter.py — thread-safe per-day token bucket for Google Ads API

Limits API calls to max_requests_per_day (default: 15,000 for Basic Access tier).
Share one instance per account across all workers.

Usage:
    limiter = RateLimiter(max_requests_per_day=15000)
    limiter.acquire()  # raises if daily limit reached
    # ... make API call ...
    print(f"Remaining today: {limiter.remaining()}")
"""

import threading
from collections import deque
from datetime import datetime, timedelta


class RateLimiter:
    """Thread-safe per-day token bucket for Google Ads API calls."""

    def __init__(self, max_requests_per_day: int = 15000):
        self.max_requests = max_requests_per_day
        self._requests: deque = deque()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Acquire permission to make one API call. Raises RuntimeError if limit reached."""
        with self._lock:
            self._purge_old()
            if len(self._requests) >= self.max_requests:
                oldest = self._requests[0]
                wait = (oldest + timedelta(days=1) - datetime.now()).total_seconds()
                raise RuntimeError(
                    f"Daily API quota reached. Next slot in {wait:.0f}s."
                )
            self._requests.append(datetime.now())

    def remaining(self) -> int:
        """Return remaining requests available today."""
        with self._lock:
            self._purge_old()
            return self.max_requests - len(self._requests)

    def _purge_old(self) -> None:
        cutoff = datetime.now() - timedelta(days=1)
        while self._requests and self._requests[0] < cutoff:
            self._requests.popleft()
