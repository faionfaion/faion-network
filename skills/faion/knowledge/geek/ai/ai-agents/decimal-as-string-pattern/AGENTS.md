# Decimal as Pattern-Constrained String

## Summary

For money, prices, exact decimals, large IDs, phone numbers, and any value where lossy float conversion would corrupt data, declare the schema field as `str` with a regex `pattern`, not `float` or `number`. The receiving side parses with `Decimal()` (or the language equivalent) only after the model has produced a known-good token sequence. The pattern constraint is enforced at sampling time on strict-mode and grammar-backed decoders, so the model cannot emit `19.999` when the schema demands two decimal places.

## Why

LLMs encode numbers as per-digit base-10 representations and frequently emit them as quoted strings even when asked for a number. Forcing a `float` field invites silent precision loss (`0.1 + 0.2 != 0.3` problem); forcing a JSON `number` lets the model emit any digit count. A regex-constrained string locks the surface form to exactly what downstream parsers expect — two decimals for currency, exactly 12 digits for an account number, semver shape for a version. The constraint masks invalid digit sequences at decode time, eliminating the common "$19.99" vs `19.989999` drift reported by the Promptfoo evaluation guide and the Base-10 digit-encoding paper.

## When To Use

- Currency (USD, EUR, BTC, etc.) — always.
- Exact decimals in finance, science, or engineering reports.
- Big integers larger than 2^53 (JSON number cannot hold them safely).
- Account numbers, credit cards, phone numbers, postal codes, ISBNs.
- Version strings (semver), date-time stamps when ISO-8601 is mandatory.

## When NOT To Use

- Counts, ranks, indices, scores — `int` is fine and saves tokens.
- Floating-point measurements where a few ULPs of drift do not matter (sensor noise, ML scores).
- Free-form numerics where the format is genuinely unknown — pattern-less string is safer than a wrong pattern.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | Core rule, mechanism, currency and big-integer examples. |
| `content/02-patterns-catalog.xml` | Reference patterns for currency, semver, ISO-8601, phone, account numbers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decimal_schema.py` | Pydantic invoice model with regex-patterned price and big-int ID fields. |
