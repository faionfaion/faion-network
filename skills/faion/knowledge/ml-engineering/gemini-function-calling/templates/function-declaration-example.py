"""
purpose: Example tool function whose docstring + type hints define the LLM-visible schema.
consumes: nothing — illustrative
produces: typed function ready for SDK reflection
depends-on: content/01-core-rules.xml r1, r2
token-budget-impact: docs-only
"""
from __future__ import annotations


def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a location.

    Args:
        location: City name with optional country (e.g. "Kyiv, UA").
        unit: Temperature unit; "celsius" or "fahrenheit". Defaults to celsius.

    Returns:
        Dict with keys: temperature (number), conditions (string), humidity (number).
    """
    # Real implementation calls a weather API; placeholder for illustration.
    return {"temperature": 18.5, "conditions": "Cloudy", "humidity": 70}
