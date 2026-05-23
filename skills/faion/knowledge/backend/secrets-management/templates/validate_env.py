# purpose: Template fixture for secrets-management: validate_env.py
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
"""Environment variable validation for service startup.

Call validate_env() at the top of your application's entry point.
The service fails fast with a clear message rather than crashing later
with a cryptic AttributeError on a missing config value.

Usage:
    from validate_env import validate_env
    env = validate_env()
    # env['DATABASE_URL'] is guaranteed to be set
"""

import os
import sys
from typing import Optional


def validate_env(
    required: Optional[list[str]] = None,
    optional: Optional[dict[str, str]] = None,
) -> dict[str, str]:
    """Validate required environment variables and apply defaults for optional ones.

    Args:
        required: Variable names that must be set and non-empty. Exits if any missing.
        optional: Variable names with default values applied if not set.

    Returns:
        Dict of all validated environment variables.
    """
    if required is None:
        required = REQUIRED
    if optional is None:
        optional = OPTIONAL

    env: dict[str, str] = {}
    missing: list[str] = []

    for var in required:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        else:
            env[var] = value

    if missing:
        print(f"FATAL: Missing required environment variables: {', '.join(missing)}")
        print("Set them in .env (EnvironmentFile) or export before starting the service.")
        sys.exit(1)

    for var, default in optional.items():
        env[var] = os.getenv(var, default)

    return env


# Customize per-service:
REQUIRED = [
    "DATABASE_URL",
    "REDIS_URL",
    "ANTHROPIC_API_KEY",
    "RABBITMQ_URL",
    "JWT_SECRET",
]

OPTIONAL = {
    "LOG_LEVEL": "INFO",
    "DEBUG": "false",
    "ENVIRONMENT": "production",
}
