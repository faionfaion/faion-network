"""
daily_runner.py — guarded daily report job with retry and dry-run flag

Input:
    client: GoogleAdsClient instance
    customer_ids: list of account IDs (as strings, no hyphens)
    query_fn: callable(customer_id) -> GAQL query string
    sink_fn: callable(customer_id, rows) -> None (writes to warehouse/file)
    dry_run: if True, fetch data but do not call sink_fn

Usage:
    from daily_runner import run_daily
    run_daily(client, ["1234567890"], query_fn, sink_fn, dry_run=False)
"""

import logging
import time

from google.ads.googleads.errors import GoogleAdsException

logger = logging.getLogger("ads-report")

MAX_ATTEMPTS = 3
INITIAL_BACKOFF_SECONDS = 30


def run_daily(client, customer_ids, query_fn, sink_fn, dry_run=False):
    """Run a daily report job across multiple accounts with retry on quota errors."""
    ga = client.get_service("GoogleAdsService")

    for cid in customer_ids:
        for attempt in range(MAX_ATTEMPTS):
            try:
                rows = []
                for batch in ga.search_stream(customer_id=cid, query=query_fn(cid)):
                    rows.extend(batch.results)
                logger.info("%s: %d rows fetched", cid, len(rows))
                if not dry_run:
                    sink_fn(cid, rows)
                break
            except GoogleAdsException as ex:
                is_quota = any(
                    e.error_code.quota_error for e in ex.failure.errors
                )
                if is_quota and attempt < MAX_ATTEMPTS - 1:
                    sleep_seconds = INITIAL_BACKOFF_SECONDS * (2 ** attempt)
                    logger.warning(
                        "quota error on %s attempt %d; sleeping %ss",
                        cid, attempt + 1, sleep_seconds
                    )
                    time.sleep(sleep_seconds)
                else:
                    logger.error(
                        "non-retryable error on %s: request_id=%s",
                        cid, ex.request_id
                    )
                    break
