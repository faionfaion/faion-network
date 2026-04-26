# mistakes.md

Append-only log of errors made and the fix; an agent must not repeat them.

Schema per entry:

```
## YYYY-MM-DD — <symptom one-liner>
**Symptom.** <observable failure>
**Root cause.** <one-paragraph diagnosis>
**Fix.** <what was actually done>
**Guard.** <test or lint rule that now prevents recurrence>
**Citation.** commit:<sha> · transcript:<hash>
```

---

## 2026-04-25 — Migration ran twice in CI
**Symptom.** `IntegrityError: duplicate key value violates unique constraint "users_email_key"` on every CI run.
**Root cause.** The autoheal agent invoked `manage.py migrate` and then `pytest` invoked it again via a fixture; the first run created seed users, the second collided.
**Fix.** Removed the fixture-side `migrate` call; CI now relies on the autoheal step only.
**Guard.** `tests/conftest.py` asserts `MIGRATIONS_RAN_BY_AUTOHEAL=1` env var before allowing `migrate` from a fixture.
**Citation.** commit:e91c2b3 · transcript:7f4a91
