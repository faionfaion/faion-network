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

## Templates

| File | Purpose |
|------|---------|
| `templates/ears-rules.json` | **The grammar, as data.** Patterns, keyword ranks, cardinality, head-marker regexes, and every E/W/I rule with severity, scope and a dated citation. Single source of truth for both the Python validator and the Go runtime. |
| `templates/ears-fixtures.tsv` | Every rule pinned to a concrete line: input → expected pattern → expected codes. Both implementations must reproduce this file exactly. |
| `templates/requirements-block.md` | Fill-in requirements table with the `ears_pattern` column wired in; ships passing its own contract. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- `spec-requirements` — owns identity, priority, verification method and traceability. EARS owns the statement sentence. Composition rule is `r6-ears-composes-with-fr-ids`; neither methodology is usable alone.
- `user-flows-template` — the generation source. Happy path → `When`, negative path → `If … then`, precondition → `While`. Generating the keyword is 100% accurate where detecting it is a heuristic.
- `readiness-checklist` — the done-gate that should read `ears_violations[]` before a feature moves.
- `project-spec-structure` — where invariants go when EARS refuses them.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ears-rules.json`

```json
{
  "version": "1.0.0",
  "notation_version": "unversioned; five patterns unchanged since Mavin et al., IEEE RE'09 (2009)",
  "last_reviewed": "2026-08-04",
  "regex_dialect": "RE2-safe: no backreferences, no lookaround. Python's re accepts every expression here; Go's regexp accepts them unchanged.",
  "patterns": [
    {
      "id": "ubiquitous",
      "keyword": null,
      "template": "The <system name> shall <system response>",
      "semantics": "A fundamental property of the system. No precondition, no trigger, always active.",
      "verification_hint": "property test or monitor",
      "source": "Mavin, alistairmavin.com/ears/, fetched 2026-08-03"
    },
    {
      "id": "state-driven",
      "keyword": "While",
      "keyword_aliases": [
        "During"
      ],
      "template": "While <precondition(s)>, the <system name> shall <system response>",
      "semantics": "Active while the system is in a specific state. A state persists; it has duration.",
      "verification_hint": "state-machine test",
      "source": "Mavin, fetched 2026-08-03; 'or optionally the keyword During' per Terzakis, Intel, ICCGI 2013"
    },
    {
      "id": "event-driven",
      "keyword": "When",
      "template": "When <trigger>, the <system name> shall <system response>",
      "semantics": "Initiated when and only when a trigger occurs or is detected. An event is instantaneous and expected.",
      "verification_hint": "integration test",
      "source": "Mavin, fetched 2026-08-03"
    },
    {
      "id": "optional-feature",
      "keyword": "Where",
      "template": "Where <feature is included>, the <system name> shall <system response>",
      "semantics": "Invoked only in systems that include the optional feature. Build or plan configuration, NOT runtime state.",
      "verification_hint": "flag matrix test",
      "source": "Mavin, fetched 2026-08-03"
    },
    {
      "id": "unwanted-behaviour",
      "keyword": "If",
      "second_keyword": "then",
      "template": "If <trigger>, then the <system name> shall <system response>",
      "semantics": "Handles unwanted behaviour: error conditions, failures, faults, disturbances, undesired events.",
      "verification_hint": "negative test",
      "source": "Mavin, fetched 2026-08-03; the only pattern with a second obligatory keyword"
    },
    {
      "id": "complex",
      "keyword": null,
      "template": "<multiple condition clauses>, the <system name> shall <system response>",
      "semantics": "Two or more condition clauses combined. Legal, and bounded by the clause-order rule.",
      "verification_hint": "derive from the strongest clause present",
      "source": "Mavin complex form 'While <precondition(s)>, When <trigger>, ...'; Terzakis complex examples, both fetched 2026-08-03"
    }
  ],
  "clause_order": {
    "rule": "Rank sequence across a statement's condition clauses must be non-decreasing; a condition keyword after the actor is a violation.",
    "total_order": "where < while|during < when < if/then",
    "ranks": {
      "where": 0,
      "while": 1,
      "during": 1,
      "when": 2,
      "if": 3
    },
    "derivation": "DERIVED, not quoted. No primary source prints a total ordering of all four keywords. This is the unique order consistent with Mavin's 'While ... when ...' complex form plus Terzakis's 'Where ... when ...' (optical drive) and 'When ... if ... then ...' (landing gear) examples, all fetched 2026-08-03. If a primary source contradicts the Where<While edge, only that comparison moves and only E005 changes."
  },
  "cardinality": {
    "where": "0..1",
    "while": "0..n",
    "when": "0..1",
    "if": "0..1, and requires a matching 'then' immediately before the actor",
    "system_name": "exactly 1",
    "system_response": "1..n",
    "source": "Mavin generic ruleset: 'Zero or many preconditions; Zero or one trigger; One system name; One or many system responses', fetched 2026-08-03"
  },
  "pipeline": {
    "stages": [
      "normalize",
      "split-on-last-head-marker",
      "classify-and-lint"
    ],
    "note": "Not one monolithic regex per pattern. Monolithic patterns break on any condition clause containing a comma or the word 'the', and give useless error messages. The same three-stage decomposition is used by labeth/ears-lint-go (MIT, fetched 2026-08-03), arrived at independently."
  },
  "regex": {
    "whitespace": "\\s+",
    "list_marker": "^\\s*(?:[-*+]|\\d+[.)])\\s+",
    "req_id": "^\\s*(?:\\*\\*)?(?:FR|NFR|AC|REQ)-\\d+(?:\\*\\*)?\\s*[:.\\u2013\\u2014-]\\s*",
    "head_strict": "(?i)(?:^|,\\s*)(then\\s+)?the\\s+([A-Za-z][A-Za-z0-9 _/.-]{1,58}?)\\s+(shall|must|will|should|may|can|might|has to|have to|needs to|need to|is able to)\\s+",
    "head_lenient": "(?i)(?:^|[,\\s]\\s*)(then\\s+)?the\\s+([A-Za-z][A-Za-z0-9 _/.-]{1,58}?)\\s+(shall|must|will|should|may|can|might|has to|have to|needs to|need to|is able to)\\s+",
    "clause_keyword": "(?i)^(while|during|when|where|if)\\b\\s*(.*)$",
    "shall": "(?i)\\bshall\\b",
    "weak_modal": "(?i)^(must|will|should|may|can|might|has to|have to|needs to|need to|is able to)$",
    "passive_response": "(?i)^(?:be|been|being)\\s+[a-z]+(?:ed|en)\\b",
    "and_or": "(?i)\\s(?:and|or)\\s|\\band/or\\b",
    "bool_and": "(?i)\\band\\b",
    "bool_or": "(?i)\\bor\\b",
    "pronoun": "(?i)\\b(it|they|them|these|those)\\b",
    "escape_clause": "(?i)\\b(if possible|as appropriate|as required|as needed|where feasible|to the extent (?:practical|possible)|and so on|etc\\.?)\\b",
    "rate": "(?i)\\b(quickly|slowly|soon|periodically|regularly|frequently|immediately|in a timely manner|real[- ]time)\\b",
    "vague": "(?i)\\b(fast|quick|easy|easily|simple|robust|scalable|efficient|flexible|user[- ]friendly|intuitive|seamless|modern|reliable|appropriate|adequate|sufficient|reasonable|minimal|optimal|approximately|roughly|several|various|normal|typical|usual|state[- ]of[- ]the[- ]art|best practice)\\b",
    "weasel_response": "(?i)^(support|handle|process|manage|deal with|take care of|address)\\b",
    "vague_system": "(?i)^(system|software|application|app|product|platform|tool|it|we)$",
    "normal_event_in_if": "(?i)\\b(?:the\\s+)?(?:user|customer|visitor|admin|client)\\s+\\w*(?:click|submit|select|enter|request|upload|tap|choose|open|press)",
    "failure_in_when": "(?i)\\b(fail|fails|error|invalid|timeout|times out|unavailable|denied|expired|corrupt|exceeds?|rejected|missing|unauthori[sz]ed)\\b",
    "bare_integer": "(?<![\\w/-])\\d+(?![\\w-])",
    "number_with_unit": "(?i)(?<![\\w/-])\\d+\\s*(ms|s|sec|secs|second|seconds|min|mins|minute|minutes|h|hr|hrs|hour|hours|day|days|week|weeks|month|months|year|years|%|percent|byte|bytes|kb|mb|gb|tb|char|chars|characters|item|items|row|rows|record|records|request|requests|user|users|session|sessions|attempt|attempts|screen|screens|file|files|px|rpm|rps|qps)\\b",
    "reaction_verb": "(?i)\\b(send|display|return|notify|alert|respond|reply|redirect|show|emit|trigger|log)\\b"
  },
  "note_on_bare_integer": "The negative lookbehind/lookahead in bare_integer and number_with_unit is Python-only convenience; the Go implementation achieves the same exclusion by rejecting a digit run whose neighbouring byte is a word character, '/' or '-'. This keeps identifiers such as UTF-8, PDF/A-2b, HTTP/2 and ordinals such as 95th out of the numeric checks.",
  "rules": [
    {
      "code": "E001",
      "severity": "error",
      "scope": "line",
      "test": "no 'shall' token anywhere on the line",
      "message": "no obligation stated: a requirement without 'shall' is a description",
      "citation": "Mavin generic ruleset, fetched 2026-08-03"
    },
    {
      "code": "E002",
      "severity": "error",
      "scope": "line",
      "test": "more than one 'shall' token",
      "message": "two 'shall' means two requirements; split into two identifiers",
      "citation": "Mavin et al. RE'09 problem taxonomy: complexity, duplication",
      "short_circuits": true,
      "short_circuit_reason": "further linting of a bundled statement is noise; split first, then classify each half"
    },
    {
      "code": "E003",
      "severity": "error",
      "scope": "line",
      "test": "no 'the <system name> <modal>' head marker found",
      "message": "no system actor: nobody is responsible for this behaviour",
      "citation": "Terzakis, Intel, ICCGI 2013 \u2014 missing-actor class"
    },
    {
      "code": "E004",
      "severity": "error",
      "scope": "prefix",
      "test": "a condition clause does not open with while/during/when/where/if",
      "message": "unparseable condition clause: it must open with an EARS keyword",
      "citation": "Mavin, fetched 2026-08-03"
    },
    {
      "code": "E005",
      "severity": "error",
      "scope": "clauses+response",
      "test": "clause rank sequence decreases, OR a condition keyword appears in the response after the actor",
      "message": "clause order violates Where < While < When < If/Then",
      "citation": "Mavin: 'The clauses of a requirement written in EARS always appear in the same order', fetched 2026-08-03"
    },
    {
      "code": "E006",
      "severity": "error",
      "scope": "clauses",
      "test": "'if' without matching 'then', or 'then' without 'if'",
      "message": "the unwanted-behaviour pattern requires both 'If' and 'then'",
      "citation": "Mavin unwanted-behaviour template, fetched 2026-08-03"
    },
    {
      "code": "E007",
      "severity": "error",
      "scope": "clauses",
      "test": "more than one where / when / if clause",
      "message": "cardinality violated: at most one where, one when, one if",
      "citation": "Mavin: 'Zero or one trigger', fetched 2026-08-03"
    },
    {
      "code": "E008",
      "severity": "error",
      "scope": "line",
      "test": "the head-marker modal is a weak modal rather than 'shall'",
      "message": "weak modal instead of 'shall'; auto-fixable",
      "citation": "RFC 2119 semantics; must/will/should/may are not obligations",
      "auto_fixable": true
    },
    {
      "code": "E009",
      "severity": "error",
      "scope": "condition",
      "test": "a condition contains both 'and' and 'or' with no parentheses",
      "message": "mixed and/or without parentheses has no defined precedence",
      "citation": "labeth/ears-lint-go boolean clause parser, fetched 2026-08-03"
    },
    {
      "code": "E010",
      "severity": "warn",
      "severity_strict": "error",
      "scope": "line",
      "test": "the statement does not end with a period",
      "message": "missing sentence terminator; cheap catch for truncation",
      "citation": "ISO/IEC/IEEE 29148 sentence discipline"
    },
    {
      "code": "W101",
      "severity": "warn",
      "scope": "response",
      "test": "response opens with be/been/being + past participle",
      "message": "passive response hides who acts",
      "citation": "Mavin et al. RE'09 problem taxonomy: ambiguity"
    },
    {
      "code": "W102",
      "severity": "warn",
      "scope": "response",
      "test": "response contains ' and ' / ' or ' / 'and/or'",
      "message": "compound response usually hides two requirements; split it",
      "citation": "Mavin et al. RE'09 problem taxonomy: duplication"
    },
    {
      "code": "W103",
      "severity": "warn",
      "scope": "line",
      "test": "a vague token is present",
      "message": "vague language cannot be tested",
      "citation": "Mavin et al. RE'09 problem taxonomy: vagueness. Strict superset of the five-token list previously inline in sdd/spec-requirements r5-no-vague-language"
    },
    {
      "code": "W104",
      "severity": "warn",
      "scope": "line",
      "test": "an escape clause is present",
      "message": "optional escape clause makes the requirement unverifiable",
      "citation": "INCOSE Guide for Writing Requirements \u2014 optional escape clause rule"
    },
    {
      "code": "W105",
      "severity": "warn",
      "scope": "response",
      "test": "response contains it/they/them/these/those",
      "message": "ambiguous referent",
      "citation": "Mavin et al. RE'09 problem taxonomy: ambiguity. Deliberately excludes 'this'/'that' \u2014 too many relative-clause false positives"
    },
    {
      "code": "W106",
      "severity": "warn",
      "scope": "if-body",
      "test": "the 'if' body describes a normal user action",
      "message": "'If' used for an expected event; probably 'When'",
      "citation": "heuristic, unmeasured \u2014 must remain a warning forever (see r5-if-vs-when-generated-not-guessed)"
    },
    {
      "code": "W107",
      "severity": "warn",
      "scope": "when-body",
      "test": "the 'when' body describes a failure",
      "message": "'When' used for an unwanted condition; probably 'If ... then'",
      "citation": "heuristic, unmeasured \u2014 must remain a warning forever"
    },
    {
      "code": "W108",
      "severity": "warn",
      "scope": "line",
      "test": "an unquantified rate or latency word is present",
      "message": "unquantified rate: needs a number and a unit",
      "citation": "Mavin et al. RE'09 problem taxonomy: untestability"
    },
    {
      "code": "W109",
      "severity": "warn",
      "scope": "response",
      "test": "response exceeds 30 words",
      "message": "wordiness",
      "citation": "Mavin et al. RE'09 problem taxonomy: wordiness"
    },
    {
      "code": "W110",
      "severity": "warn",
      "scope": "clauses",
      "test": "more than three condition clauses",
      "message": "excessive preconditions produce an unwieldy sentence; lift them into a state machine and write one requirement per transition",
      "citation": "Wikipedia, Easy Approach to Requirements Syntax, limitations section, fetched 2026-08-03"
    },
    {
      "code": "W111",
      "severity": "warn",
      "scope": "system",
      "test": "the system name is system/software/application/app/product/platform/tool/it/we",
      "message": "unnamed component: legal EARS, useless traceability",
      "citation": "practitioner rule \u2014 a requirement with no named component cannot be mapped to a test file or an owner"
    },
    {
      "code": "W112",
      "severity": "warn",
      "scope": "response",
      "test": "response opens with support/handle/process/manage/deal with/take care of/address",
      "message": "weasel verb: state what the system actually does",
      "citation": "Terzakis, Intel, ICCGI 2013 \u2014 'The software shall support a water level sensor. What does the word support mean?'"
    },
    {
      "code": "W114",
      "severity": "warn",
      "scope": "response",
      "test": "response contains a bare integer and no integer paired with a unit",
      "message": "number without a unit",
      "citation": "Mavin et al. RE'09 problem taxonomy: untestability"
    },
    {
      "code": "I113",
      "severity": "info",
      "scope": "pattern",
      "test": "the statement classified as ubiquitous and emitted no error",
      "message": "most requirements are not ubiquitous \u2014 is there an unstated trigger or precondition here?",
      "citation": "Terzakis, Intel, ICCGI 2013: 'Question ubiquitous requirements ... Most requirements are not ubiquitous'",
      "prompt_not_check": true
    }
  ],
  "modes": {
    "default": "warnings-only, exit 0. Errors are reported; the process still succeeds.",
    "strict": "opt-in, CI-only. Any E-code fails the run; E010 is promoted to error. Do not enable before the rule set has been run over a real corpus and tuned.",
    "lenient": "accepts a bare space before the actor, so Kiro-style comma-less ALL-CAPS 'WHEN ... THE SYSTEM SHALL ...' parses. Accepted, never canonicalised.",
    "fix": "handles exactly one class safely \u2014 E008 modal normalisation to 'shall'. Nothing else is auto-fixable without changing meaning."
  },
  "not_covered": [
    "correctness \u2014 a statement can parse clean and be a catastrophic bug",
    "completeness of the set \u2014 an 'If X' with no 'not X' counterpart needs a separate set-level coverage pass",
    "consistency \u2014 two requirements can each be valid EARS and contradict each other",
    "temporal richness \u2014 EARS has no 'until', no 'for the duration of', no 'at most N times per'; all of it smuggles into free-text response where no rule can see it",
    "localisation \u2014 the keyword table is English; questions localise, stored syntax does not"
  ],
  "prior_art": [
    {
      "tool": "QVscribe (QRA Corp)",
      "validates_ears": true,
      "detail": "automated EARS templating and compliance checking since v2.10, announced 2019-08-21; NLP-based; DOORS Next / Jama / Polarion / Word / Excel",
      "verified": "2026-08-03"
    },
    {
      "tool": "labeth/ears-lint-go",
      "validates_ears": true,
      "detail": "MIT Go library: shell parsing, pattern classification, boolean clause parser, catalog matching, clause-order and vague-language rules. 0 stars",
      "verified": "2026-08-03"
    },
    {
      "tool": "tbhb/vale-ears",
      "validates_ears": "partially",
      "detail": "MIT Vale style package: ears.Syntax, ears.Shall, ears.PassiveVoice, ears.WeakWords. Requires Vale as an external binary",
      "verified": "2026-08-03"
    },
    {
      "tool": "Kiro (AWS)",
      "validates_ears": false,
      "detail": "EARS is a writing convention in requirements.md; no validate/lint/parse language anywhere in the docs",
      "verified": "2026-08-03"
    },
    {
      "tool": "GitHub spec-kit",
      "validates_ears": false,
      "detail": "issue #1356 'Feature Request: EARS Integration', opened 2025-12-20, closed without implementation",
      "verified": "2026-08-03"
    }
  ],
  "positioning": "The defensible claim is 'the first EARS validator that runs inside your coding agent \u2014 one binary, no DOORS, no Jama, no seat licence.' Never 'nobody has built this': QVscribe has machine-validated EARS since 2019 and labeth/ears-lint-go exists.",
  "unaudited_surfaces": "As of 2026-08-04 the VS Code Marketplace, StrictDoc, Doorstop and rmtoo have NOT been checked for EARS grammar support (the 2026-08-03 research pass exhausted its search budget, and a re-check on 2026-08-04 could not run for the same reason). Any of them could weaken the segment claim. Re-verify before this positioning appears in customer-facing copy."
}
```

### `templates/ears-fixtures.tsv`

```tsv
#
# Columns (tab-separated): statement <TAB> expected_pattern <TAB> expected_codes <TAB> mode
# expected_codes: comma-separated, sorted; "-" means a clean parse.
# mode: default | lenient
# Sources for the canonical lines: Mavin (alistairmavin.com/ears/) and Terzakis (Intel, ICCGI 2013), both fetched 2026-08-03.
#
# --- PASS: the five patterns and Complex ---
The billing service shall retain invoices for 7 years.	ubiquitous	I113	default
When a customer submits the checkout form, the payment service shall create a charge intent.	event-driven	-	default
While the account is in trial state, the billing service shall reject all charge attempts.	state-driven	-	default
Where the multi-currency feature is enabled, the dashboard shall display amounts in the account currency.	optional-feature	-	default
If the payment provider returns a declined status, then the checkout page shall display the message "Card declined".	unwanted-behaviour	-	default
While the account is in trial state, when a customer submits the checkout form, the billing service shall display the upgrade prompt.	complex	-	default
When the export job starts, if the storage quota is exceeded, then the export service shall abort the job.	complex	-	default
#
# --- PASS: the "after" side of the ten rewrites ---
The checkout service shall return a response to POST /orders within 400 ms at the 95th percentile under 50 concurrent sessions.	ubiquitous	I113	default
When a visitor submits the signup form with a valid email address, the onboarding service shall send the welcome email within 60 seconds.	event-driven	-	default
When the count of consecutive failed login attempts for an account reaches 5 within 15 minutes, the auth service shall lock the account for 30 minutes.	event-driven	-	default
When an account owner requests an export in PDF format, the report service shall produce a PDF/A-2b file.	event-driven	-	default
The backup job shall write a full snapshot of the primary database to object storage every 24 hours.	ubiquitous	I113	default
The onboarding wizard shall complete account setup in no more than 4 screens.	ubiquitous	I113	default
#
# --- FAIL: errors ---
The app should be fast.	invalid	E001,E008,W103,W111	default
Users get an email when they sign up.	invalid	E001,E003	default
Data is backed up regularly.	invalid	E001,E003,W108	default
The system shall validate the input and shall persist the record.	invalid	E002	default
Assuming the user is logged in, the profile service shall display the avatar.	invalid	E004	default
The API shall respond within 200 if the load is normal or the cache is warm and the region is EU.	invalid	E005,E009,W102,W103,W114	default
When the export starts, while the account is active, the export service shall queue the job.	invalid	E005	default
If the user clicks Export, the report service shall generate a CSV.	invalid	E006,W106	default
When the export starts, then the export service shall log the start.	invalid	E006	default
When the cart is updated, when the user checks out, the pricing service shall recalculate totals.	invalid	E007	default
If the load is normal or the cache is warm and the region is EU, then the API shall serve from cache.	invalid	E009,W103	default
The billing service shall retain invoices for 7 years	ubiquitous	E010,I113	default
#
# --- FAIL: warnings only (default mode still exits 0) ---
When the trial ends, the system shall be notified.	event-driven	W101,W111	default
When an account owner requests a full data export, the export service shall assemble every invoice every payment every refund every customer record and every audit entry belonging to that account into a single archive file that is then written to object storage for later download by the owner.	event-driven	W102,W109	default
The report service shall archive old reports as needed.	ubiquitous	I113,W104	default
The export service shall generate a CSV and email it to the account owner.	ubiquitous	I113,W102,W105	default
When the payment fails, the billing service shall retry.	event-driven	W107	default
Where the audit feature is enabled, while the account is active, while the region is EU, when a user exports a report, the audit service shall write an audit record.	complex	W110	default
If the memory checksum is invalid, then the software shall display an error message.	unwanted-behaviour	W111	default
The system shall support a water level sensor.	ubiquitous	I113,W111,W112	default
#
# --- lenient mode: Kiro-style comma-less ALL-CAPS input is accepted, never canonicalised ---
WHEN a user submits valid data THE SYSTEM SHALL create an account.	event-driven	W111	lenient
```
