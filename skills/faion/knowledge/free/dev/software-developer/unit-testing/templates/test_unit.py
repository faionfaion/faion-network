"""
purpose: Python AAA skeleton with mock at boundary.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import pytest


def add(a: int, b: int) -> int:
    return a + b


def test_add_returns_sum_when_both_positive():
    # Arrange
    a, b = 2, 3
    # Act
    result = add(a, b)
    # Assert
    assert result == 5
