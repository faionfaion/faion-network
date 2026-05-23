<!-- purpose: application-service dispatch sequence (collect after commit) -->
<!-- consumes: aggregate command + DB session -->
<!-- produces: ordered call sequence reference -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150 tokens when loaded as reference -->

# Dispatch sequence (collect-after-commit)

```text
1. begin transaction
2. repo.add(aggregate) or repo.update(aggregate)
3. session.commit()         # state is durable from here
4. events = aggregate.collect_events()
5. outbox.append_events_to_outbox(events)   # if broker target
   or in_process_dispatcher.dispatch(events) # if in-process target
6. session.commit()         # second commit ONLY if outbox writes are in a fresh tx
```

Critical invariants:
- `collect_events()` MUST run after step 3 (commit) — never before.
- If using outbox, steps 2 + 4 + 5 MUST share a single transaction; rollback discards both aggregate state and outbox rows together.
- Idempotency: relay re-dispatches on retry; consumers dedup by `event_id`.
