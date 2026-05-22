# purpose: Django system checks for SECRET_KEY default + missing SENTRY_DSN + LocMemCache in prod
# consumes: settings.SECRET_KEY, settings.SENTRY_DSN, settings.CACHES, settings.DEBUG
# produces: Error / Warning on `manage.py check --deploy` for misconfigurations
# depends-on: Django checks framework (stdlib of Django)
# token-budget-impact: ~180 tokens

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register


@register(Tags.security)
def check_secret_key_not_default(app_configs, **kwargs):
    errors = []
    key = settings.SECRET_KEY or ""
    if key.startswith("django-insecure-") or key == "django-insecure-change-me":
        errors.append(
            Error(
                "SECRET_KEY is the django-insecure default.",
                hint=(
                    "Generate via python -c 'from django.core.management.utils "
                    "import get_random_secret_key; print(get_random_secret_key())' "
                    "and load from env."
                ),
                id="security.E001",
            )
        )
    return errors


@register(Tags.security, deploy=True)
def check_sentry_dsn_present(app_configs, **kwargs):
    warnings = []
    if not getattr(settings, "SENTRY_DSN", None) and not settings.DEBUG:
        warnings.append(
            Warning(
                "SENTRY_DSN is not configured for production.",
                hint="Set SENTRY_DSN env var; load it in production.py.",
                id="monitoring.W001",
            )
        )
    return warnings


@register()
def check_cache_not_locmem_in_prod(app_configs, **kwargs):
    warnings = []
    if not settings.DEBUG:
        backend = settings.CACHES.get("default", {}).get("BACKEND", "")
        if "LocMemCache" in backend:
            warnings.append(
                Warning(
                    "Using LocMemCache in production.",
                    hint="Configure Redis/Memcached for production caching.",
                    id="caching.W001",
                )
            )
    return warnings
