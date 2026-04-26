# Discriminated-Union Structured Output

## Summary

When a structured-output schema must choose between two or more distinct shapes (different agent actions, different entity types, different intents, different events), model the output as a discriminated union — a tagged union where one literal field (`kind`, `type`, `action`) is generated FIRST and selects which branch the rest of the object must follow. The discriminator locks the JSON-Schema/grammar branch and turns shape selection into a single constrained-decoding choice instead of a probabilistic mess of optional fields.

## Why

Pydantic, JSON Schema 2020-12, and OpenAI strict mode all support `oneOf` + a `discriminator` keyword that compiles into a finite-state grammar: once the model emits the discriminator literal, only the fields of the matching branch are reachable. This eliminates the two failure modes of "flat schema with all-optional fields" — silently mixing fields from different shapes, and ambiguity over which fields are required. It also gives parsers a single key to switch on, which mirrors algebraic-data-type pattern matching in the consumer code.

## When To Use

- Agent action selection where each action has different required arguments (search vs fetch vs finish vs ask-user).
- Polymorphic entity extraction (Person vs Company vs Product vs Address) from one document.
- Router outputs that must dispatch to one of N downstream handlers.
- Event logs / message buses where each event type has its own payload schema.
- Multi-intent classification where every intent owns its own structured payload.

## When NOT To Use

- All branches share more than ~90% of their fields — flatten with optional fields and a single `kind` literal instead, the union machinery costs more than it saves.
- The set of branches is open (user-defined entity types, plug-in actions) — use a registry pattern with free-string `kind` plus a separate validation pass.
- Targets that do not honour the `discriminator` keyword (older Outlines/XGrammar versions, custom GBNF grammars without union support) — fall back to two sequential calls (classify, then extract).

## Content

| File | What's inside |
|------|---------------|
| `content/01-discriminator-rule.xml` | The core rule, mechanism, good/bad examples for an agent action picker. |
| `content/02-pitfalls.xml` | Antipatterns: bare `Union[A,B]` without discriminator, discriminator placed last, near-identical branches. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent_action_union.py` | Pydantic discriminated union for an agent action selector (search / fetch / finish). |
| `templates/agent_action.schema.json` | Equivalent JSON Schema 2020-12 with `oneOf` + `discriminator` for non-Python providers. |
