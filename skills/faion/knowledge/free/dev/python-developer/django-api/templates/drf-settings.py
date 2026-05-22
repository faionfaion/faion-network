# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
Complete REST_FRAMEWORK + SIMPLE_JWT + SPECTACULAR_SETTINGS config block.
Copy into settings.py (or settings/base.py).
"""

from datetime import timedelta

REST_FRAMEWORK = {
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Permissions — locked down by default, opt-in to AllowAny per view
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Renderer — JSON only in production; BrowsableAPI only in development
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Throttling — scoped per endpoint type
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "1000/day",
        "burst": "30/min",      # Write endpoints (POST/PUT/PATCH/DELETE)
        "login": "5/min",       # Auth endpoints — brute-force protection
    },
    # Pagination — always paginate list endpoints
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    # Filtering
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # Schema generation
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Versioning
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    # Exception handler
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}

# JWT Configuration — simplejwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),   # Short-lived: 15 min
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),       # 7-day refresh
    "ROTATE_REFRESH_TOKENS": True,                     # New refresh on use
    "BLACKLIST_AFTER_ROTATION": True,                  # Blacklist old refresh
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# drf-spectacular OpenAPI schema settings
SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "REST API documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Postprocessing hooks
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
    # Component naming
    "COMPONENT_SPLIT_REQUEST": True,   # Separate request/response schemas
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]+",
}
