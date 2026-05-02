---
name: testing-intro-python
description: Install pytest and write your first 3 automated tests for a Python function, then run them and see green output.
tier: free
group: dev-fundamentals
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working pytest test suite with three tests for an `add()` function — happy path, zero inputs, and negative numbers — and you will have seen them all pass with `pytest -v` green output.

## Prerequisites

- Python 3.9+ installed (`python3 --version`).
- Either `pip` or `uv` available in your shell.
- A project directory where you can create files (no framework required).

## Steps

1. Install pytest into your project's dev dependencies.

   With pip:
   ```bash
   pip install pytest
   ```

   With uv (preferred for new projects):
   ```bash
   uv add --dev pytest
   ```

2. Create the module under test. Save the following as `calculator.py` in your project root:

   ```python
   def add(a: int | float, b: int | float) -> int | float:
       return a + b
   ```

3. Create the `tests/` directory and an empty `__init__.py` so pytest discovers it:

   ```bash
   mkdir tests
   touch tests/__init__.py
   ```

4. Create the test file at `tests/test_calculator.py`:

   ```python
   from calculator import add


   def test_add_happy_path():
       assert add(2, 3) == 5


   def test_add_with_zero():
       assert add(0, 99) == 99
       assert add(42, 0) == 42


   def test_add_negative_numbers():
       assert add(-4, -6) == -10
       assert add(-1, 1) == 0
   ```

5. Run pytest with verbose output from your project root:

   ```bash
   pytest -v
   ```

   You will see output similar to:

   ```
   collected 3 items

   tests/test_calculator.py::test_add_happy_path PASSED
   tests/test_calculator.py::test_add_with_zero PASSED
   tests/test_calculator.py::test_add_negative_numbers PASSED

   3 passed in 0.01s
   ```

## Verify

Run the suite and confirm all three tests are green:

```bash
pytest -v tests/test_calculator.py
```

All three test names must appear with `PASSED` and the summary line must read `3 passed`. Any `FAILED` or `ERROR` line indicates an issue — re-read the error message; pytest prints the exact assertion that failed.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'calculator'` | pytest runs from a directory where `calculator.py` is not on the Python path | Run `pytest -v` from the project root (same dir that contains `calculator.py`), not from inside `tests/` |
| `command not found: pytest` | pytest not installed in the active virtualenv | Activate your venv first (`source .venv/bin/activate`), then re-run `pip install pytest` or `uv add --dev pytest` |
| `collected 0 items` | Test file or function names do not match pytest's discovery conventions | Rename the file to `test_*.py` and all test functions to start with `test_` |
| `SyntaxError` on `int \| float` type hint | Python version < 3.10 | Replace `int | float` with `Union[int, float]` (import from `typing`) or use Python 3.10+ |

## Next

- Add `pytest-cov` to measure coverage: `pip install pytest-cov` then `pytest --cov=calculator tests/`.
- Read the `testing-pytest` methodology to learn fixtures, parametrize, and markers for larger test suites.
- Move on to `python-first-project` if you need a project scaffold with tests wired into a proper package layout.

## References

- [knowledge/free/dev/testing-developer/testing-pytest](../../../knowledge/free/dev/testing-developer/testing-pytest) — provides the pytest configuration patterns, discovery rules, and fixture scopes that underpin every step in this playbook; specifically the `testpaths` and naming conventions that make Step 5 work without extra config.
