<!-- purpose: per-stage agent prompt fragments -->
<!-- consumes: aggregate name + ubiquitous-language glossary -->
<!-- produces: prompt strings to send to the codegen agent -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~250 tokens when loaded as reference -->

# Stage prompts

## Stage 1 — aggregate-design
```
You are designing an event-sourced aggregate.

Constraints:
- Event names MUST be past-tense business facts (OrderPlaced, ItemAdded).
- DO NOT propose generic Update*/Set*/Change* events.
- Commands: present-tense verbs (place, ship, cancel).
- List invariants explicitly.

Output: markdown sections "Events", "Commands", "Invariants".
```

## Stage 2 — event-class-codegen
```
Generate event classes + aggregate using <library>.

Constraints:
- Events: @dataclass(frozen=True) with event_id + occurred_at + <aggregate>_id.
- Command methods validate + emit; never mutate state directly.
- State mutation lives ONLY in _apply_<EventName>(self, event) handlers.
- Repository: load(stream_id) -> Aggregate; save(stream_id, events, expected_version).
- Use ONLY APIs documented in the library docs supplied below.
```

## Stage 3 — projection-codegen
```
Generate projection handlers for read model <name>.

Constraints:
- Each handler takes (event) and performs UPSERT/INSERT/DELETE only.
- NO email/HTTP/file/queue side effects.
- NO domain-event emission.
- Track checkpoint (stream_id, position) in projection_checkpoint table.
```

## Stage 4 — tests-codegen
```
Generate tests for <aggregate>.

Constraints:
- Assert event emission, not getter equality.
- Cover: command success, command failure, replay matches live, concurrency conflict.
- Use Given/When/Then style with explicit event lists.
```

## Stage 5 — antipattern-review
```
Review the artefacts against rules:
  past-tense-event-names, apply-only-mutation, expected-version-enforced,
  no-invented-apis, projection-no-side-effects.
Emit JSON: {accepted: bool, rejected_rule_ids: [string], notes: [string]}.
```
