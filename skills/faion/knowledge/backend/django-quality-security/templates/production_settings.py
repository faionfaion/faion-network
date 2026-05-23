# purpose: drop-in HTTPS/CSP/cookie baseline for config/settings/production.py
# consumes: SECURE_PROXY_SSL_HEADER known from reverse-proxy config
# produces: production-safe transport security flags + CSP middleware wiring
# depends-on: Django >= 5.2 (Django 6.0+ for native CSP; otherwise django-csp)
# token-budget-impact: ~220 tokens

from .base import *  # noqa: F401, F403

DEBUG = False

# Transport
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# HSTS — ramp 300 -> 3600 -> 31536000 across deploys; START AT 300
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# CSP (Django 6.0+ native). Start report-only; switch to enforce after telemetry clean.
MIDDLEWARE.insert(1, "django.middleware.csp.ContentSecurityPolicyMiddleware")  # noqa: F405
CONTENT_SECURITY_POLICY_REPORT_ONLY = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "'nonce-<CSP_NONCE_SENTINEL>'"],
    "style-src": ["'self'", "'nonce-<CSP_NONCE_SENTINEL>'"],
    "img-src": ["'self'", "data:", "https:"],
    "font-src": ["'self'", "https://fonts.gstatic.com"],
    "connect-src": ["'self'"],
    "frame-ancestors": ["'none'"],
    "form-action": ["'self'"],
}

# Before deploy:
#   python manage.py check --deploy --fail-level WARNING --settings=config.settings.production
