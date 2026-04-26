"""Skeleton for source-grounded property-based tests.

Use one block per property class. Delete the classes that do not apply
to the function under test. NEVER commit a property without the
`# grounded: ...` comment.
"""

from hypothesis import given, settings, strategies as st

from your_module import f, g, oracle  # adjust imports


# ----- 1. round-trip -----------------------------------------------------
# grounded: docstring "<quote the round-trip claim here>"
@given(st.text())
def test_round_trip(x: str) -> None:
    assert g(f(x)) == x


# ----- 2. idempotence ----------------------------------------------------
# grounded: docstring "<quote the idempotence claim here>"
@given(st.text())
def test_idempotent(x: str) -> None:
    assert f(f(x)) == f(x)


# ----- 3. oracle-equivalence --------------------------------------------
# grounded: type signature matches reference oracle <name>.
@given(st.lists(st.integers()))
def test_oracle_equivalent(xs: list[int]) -> None:
    assert f(xs) == oracle(xs)


# ----- 4. metamorphic ---------------------------------------------------
# grounded: docstring "<quote the metamorphic relation here>"
@given(st.lists(st.integers()))
def test_metamorphic_shuffle_invariant(xs: list[int]) -> None:
    import random

    ys = xs[:]
    random.shuffle(ys)
    assert f(ys) == f(xs)  # adjust to the actual relation


# ----- 5. invariant-on-output -------------------------------------------
# grounded: docstring "<quote the output property here>"
@given(st.lists(st.integers()))
@settings(max_examples=200)
def test_output_invariant(xs: list[int]) -> None:
    out = f(xs)
    assert all(out[i] <= out[i + 1] for i in range(len(out) - 1))
