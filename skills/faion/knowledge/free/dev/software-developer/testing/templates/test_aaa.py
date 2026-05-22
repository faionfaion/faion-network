"""
purpose: Python AAA test skeleton.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import pytest


def parse_int(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None


def test_parse_int_returns_value_when_digits_only():
    # Arrange
    s = "42"
    # Act
    result = parse_int(s)
    # Assert
    assert result == 42
