# purpose: Sentry SDK init + scrub_sensitive_data scrubber for config/settings/production.py
# consumes: SENTRY_DSN env var, ENVIRONMENT env var
# produces: live Sentry capture with traces_sample_rate=0.1, send_default_pii=False, scrubbed payloads
# depends-on: sentry-sdk>=2 (+ celery integration if Celery in use)
# token-budget-impact: ~200 tokens when included verbatim in settings

import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

PII_KEYS = ("password", "token", "secret", "credit_card", "api_key", "authorization")


def scrub_sensitive_data(event, hint):
    """Mutate PII fields out of the event before send. Never return None unless explicitly dropping."""
    request = event.get("request") or {}
    data = request.get("data")
    if isinstance(data, dict):
        for key in PII_KEYS:
            data.pop(key, None)
    headers = request.get("headers")
    if isinstance(headers, dict):
        for key in list(headers):
            if key.lower() in PII_KEYS:
                headers.pop(key, None)
    return event


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    send_default_pii=False,
    environment=os.environ.get("ENVIRONMENT", "production"),
    before_send=scrub_sensitive_data,
)
