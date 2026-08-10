# EARS Requirements

## Summary

**One-sentence:** Constrains exactly one field of a requirement — the statement sentence — to one of five EARS patterns with a fixed clause order, so that "is this requirement ambiguous?" becomes a question a regex answers in microseconds instead of a question a reviewer argues about.

**One-paragraph:** EARS (Easy Approach to Requirements Syntax) is five English sentence templates plus a clause-order rule, published by Alistair Mavin and colleagues at Rolls-Royce at IEEE RE'09 and unchanged since. It is the only requirements discipline in the 2026 AI-SDLC landscape that is a grammar rather than a prompt convention: a sentence either parses or it does not, and the verdict costs zero API calls. This methodology ships the grammar as data (`templates/ears-rules.json`), a fixture corpus that pins every rule to a concrete line (`templates/ears-fixtures.tsv`), and a dev-time validator that replays both. It composes with `sdd/spec-requirements` rather than replacing it: `FR-NNN` keeps identity, priority, verification method and traceability; EARS owns the sentence and nothing else. The hard limit is stated up front and never buried — **EARS makes a requirement unambiguous, it does not make it correct.** "When a customer submits the checkout form, the payment service shall charge the customer twice." is perfect EARS and a catastrophic bug.

**Ефективно для:**

- Any `spec.md` whose FR statements were written as prose and now have to be tested by someone who was not in the room.
- Teams where an agent writes the requirements: the grammar is the only part of a spec an agent cannot bluff.
- Non-technical founders — via generation from `user-flows.md`, never by asking them to type `shall`.
- Acceptance criteria that keep failing review for reasons nobody can name in one sentence.

## Applies If (ALL must hold)

- A requirement set exists or is being written, with stable identifiers (`FR-NNN` / `NFR-NNN`).
- The requirements describe a system responding to conditions — not goals, not invariants, not research questions.
- Somebody downstream (a test, a reviewer, an agent) has to act on the sentence without asking the author what it meant.

## Skip If (ANY kills it)

- The artefact is a goal, a metric or an outcome ("grow MRR to €10k") — route to `roadmap.md`, EARS has no form for it.
- The artefact is a data or domain invariant ("an Invoice belongs to exactly one Order") — route to `project-spec/`, an invariant is not a behaviour.
- The work is a spike; its output is learning, not a system response. `sdd/spec-requirements` already declares this skip and EARS inherits it.
- The requirement is a pure architectural constraint ("the system shall be modular"). It passes the grammar and means nothing; record `ears_pattern: n-a` with a reason instead of pretending.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Eight testable rules: the five patterns, the derived clause order, one-shall-one-requirement, the named actor, the composition rule with `sdd/spec-requirements`, the refusal routes, and the correctness limit. |
| `content/02-output-contract.xml` | The requirement-set artefact: `ears_pattern` enum, the mandatory `ears_pattern_na_reason` opt-out, `ears_violations[]`, forbidden patterns, and the JSON Schema the validator enforces. |
| `content/03-failure-modes.xml` | Seven ways EARS adoption fails in practice, each with symptom, cause and the rule that prevents it. |
| `content/06-decision-tree.xml` | Routing: is this a system response to a condition at all? If yes, which keyword; if no, where it goes instead. |
| `scripts/validate-ears-requirements.py` | Three-stage linter (normalize → head-marker split → classify + lint) plus artefact validation. `--self-test` replays every fixture. |
| `templates/ears-rules.json` | **The grammar, as data.** Patterns, keyword ranks, cardinality, head-marker regexes, and every E/W/I rule with severity, scope and a dated citation. Single source of truth for both the Python validator and the Go runtime. |
| `templates/ears-fixtures.tsv` | Every rule pinned to a concrete line: input → expected pattern → expected codes. Both implementations must reproduce this file exactly. |
| `templates/requirements-block.md` | Fill-in requirements table with the `ears_pattern` column wired in; ships passing its own contract. |

## Related

- `spec-requirements` — owns identity, priority, verification method and traceability. EARS owns the statement sentence. Composition rule is `r6-ears-composes-with-fr-ids`; neither methodology is usable alone.
- `user-flows-template` — the generation source. Happy path → `When`, negative path → `If … then`, precondition → `While`. Generating the keyword is 100% accurate where detecting it is a heuristic.
- `readiness-checklist` — the done-gate that should read `ears_violations[]` before a feature moves.
- `project-spec-structure` — where invariants go when EARS refuses them.
