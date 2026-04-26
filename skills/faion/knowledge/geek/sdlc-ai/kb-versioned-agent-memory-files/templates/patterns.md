# patterns.md

Append-only log of proven implementations an agent should reuse.

Schema per entry:

```
## YYYY-MM-DD — <pattern name>
**What.** <one-paragraph description>
**Where.** <repo paths or symbol links>
**When to apply.** <concrete triggers>
**Citation.** commit:<sha> · pr:<url>
```

---

## 2026-04-26 — Idempotent webhook handler
**What.** Webhook endpoints store `(provider_id, event_id)` in an `idempotency` table before processing; a duplicate insert short-circuits to 200 OK without re-running side effects.
**Where.** `apps/webhooks/handlers/` — see `_idempotent_handler` decorator.
**When to apply.** Any inbound webhook from a third party that may retry on its end (Stripe, GitHub, Linear).
**Citation.** commit:b27d4f1 · pr:github.com/org/repo/pull/812
