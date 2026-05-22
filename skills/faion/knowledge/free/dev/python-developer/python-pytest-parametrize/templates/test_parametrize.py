"""
purpose: Skeleton: simple parametrize, stacked decorators (cartesian), pytest.param with id+marks, indirect=True.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import pytest


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("hello", True, id="non-empty"),
        pytest.param("", False, id="empty"),
        pytest.param("   ", False, id="whitespace"),
    ],
)
def test_is_meaningful_string(value, expected):
    assert bool(value.strip()) is expected


@pytest.mark.parametrize("a", [1, 2, 3])
@pytest.mark.parametrize("b", [10, 20])
def test_cartesian_product(a, b):
    assert a + b > 0
