# EARS Notation
**Layer:** 2 — Decomposition · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

EARS — **Easy Approach to Requirements Syntax** — is a constrained-natural-language template set for writing requirements. It is not a tool, not a format, not a schema: it is five sentence shapes plus a fixed clause order. You still write English; EARS just removes the freedom that produces ambiguity.

It was created by **Alistair Mavin** and colleagues at **Rolls-Royce plc** while analysing airworthiness regulations for a jet-engine control system, and first published at the **IEEE International Requirements Engineering Conference (RE'09), 2009** — "Easy Approach to Requirements Syntax (EARS)", Mavin, Wilkinson, Harwood, Novak.

The Rolls-Royce case study identified **eight** problem classes in existing natural-language requirements — ambiguity, vagueness, complexity, omission, duplication, wordiness, inappropriate implementation, untestability — and reported that rewriting in EARS "demonstrated a significant reduction in all eight problem types" (Terzakis, Intel, ICCGI 2013 tutorial, slide "EARS Background", citing Mavin et al.).

Adoption named on Wikipedia (fetched 2026-08-03): Airbus, Bosch, Dyson, Honeywell, Intel, NASA, Rolls-Royce, Siemens; plus universities in China, France, Germany, Sweden, UK, USA. Domains: aviation, automotive, medical devices — i.e. places where an ambiguous requirement kills people, which is why the notation is so unglamorously strict.

**Why it matters to us:** EARS is the only piece in the entire 2026 AI-SDLC landscape that is (a) 17 years old and battle-proven, (b) five rules a non-programmer can learn in twenty minutes, and (c) **mechanically checkable with a regex engine and no dependencies**. Every other "spec-driven" idea in the landscape is a prompt convention. This one is a grammar.

## Current state

| Fact | Value | Dated |
|------|-------|-------|
| Original publication | RE'09, IEEE Int'l Requirements Engineering Conference | **2009** |
| Authors | Alistair Mavin, Philip Wilkinson, Adrian Harwood, Mark Novak (Rolls-Royce plc) | 2009 |
| Canonical reference today | https://alistairmavin.com/ears/ — "EARS: Easy Approach to Requirements Syntax, Official Guide" | fetched **2026-08-03**; page carries "© 2026 Alistair Mavin // All Rights Reserved" |
| Version | **Unversioned.** EARS has no version number, no release cadence, no changelog. The five patterns are unchanged since 2009. | 2026-08-03 |
| Maintainer | Alistair Mavin personally (alistairmavin.com); no foundation, no standards body, no repo | 2026-08-03 |
| License | **None stated.** Copyright asserted on the guide text. The *notation itself* — five English sentence templates using ordinary keywords — is not a copyrightable artefact and is used freely by Intel, AWS, Wikipedia and others without attribution licences. | 2026-08-03 |
| Price | **$0.** There is no product. Mavin sells training/consulting; the notation is free. | 2026-08-03 |
| Standardisation | Not an ISO/IEEE standard. Complements ISO/IEC/IEEE 29148 and the INCOSE *Guide for Writing Requirements*, but is not part of either. | 2026-08-03 |

**Staleness footnote:** because EARS is unversioned and maintained by one person on one page, the *notation* is essentially frozen and safe to build on. The risk is not that EARS changes; it is that the canonical page goes offline. Mirror it.

## Mechanics

### Generic ruleset

From Mavin's official guide (fetched 2026-08-03), an EARS requirement contains:

> Zero or many preconditions; Zero or one trigger; One system name; One or many system responses.

and

> The clauses of a requirement written in EARS always appear in the same order.

The generic form:

```
While <optional precondition(s)>, when <optional trigger>, the <system name> shall <system response>
```

The RE'09 paper expresses the same skeleton as `[Precondition]* [Trigger]? [Feature]`.

Terzakis (Intel, 2013) frames the same idea as a generic functional-requirement syntax with optional items in brackets:

```
[Trigger] [Precondition] Actor Action [Object]
```

worked as: *"When an Order is shipped and Order Terms are not 'Prepaid', the system shall create an Invoice."* — Trigger = "When an Order is shipped"; Precondition = "Order Terms are not 'Prepaid'"; Actor = "the system"; Action = "create"; Object = "an Invoice".

### The five patterns

Verified against **Mavin's official guide** and cross-checked against **Wikipedia** and **Terzakis/ICCGI 2013**, all fetched 2026-08-03. Angle brackets are Mavin's own placeholder names.

| # | Pattern | Keyword | Template (Mavin, verbatim) |
|---|---------|---------|----------------------------|
| 1 | **Ubiquitous** | *(none)* | `The <system name> shall <system response>` |
| 2 | **State-driven** | `While` | `While <precondition(s)>, the <system name> shall <system response>` |
| 3 | **Event-driven** | `When` | `When <trigger>, the <system name> shall <system response>` |
| 4 | **Optional feature** | `Where` | `Where <feature is included>, the <system name> shall <system response>` |
| 5 | **Unwanted behaviour** | `If` … `then` | `If <trigger>, then the <system name> shall <system response>` |

**All five templates in the task brief are correct.** Nothing to fix. Three cosmetic notes:

- Mavin writes the templates **without a trailing period**; the period belongs to the requirement, not the template.
- Mavin's placeholders are `<system name>` and `<system response>`, not `<system>`/`<response>`. Immaterial, but use his names in our docs so a reader arriving from his page recognises them.
- `If` is the **only** pattern with a second obligatory keyword (`then`). That asymmetry is load-bearing for the linter — it is the cheapest disambiguator we get for free.

Pattern semantics, in the words of the sources:

- **Ubiquitous** — "Define a fundamental property of the system"; "Have no preconditions or trigger"; "Do not require a pattern keyword" (Terzakis 2013). Mavin's guide: ubiquitous requirements are always active, so there is no keyword. Terzakis's warning is the important one: *"Question ubiquitous requirements: Things that may seem universal are often subject to unstated triggers or preconditions"* — and *"Most requirements are not ubiquitous."* His examples of things that *look* ubiquitous but are not: "The software shall wake the PC from standby", "The software shall log the date, time and username of failed logins" — both **missing a trigger**.
- **State-driven** — "Are triggered while the system is in a specific state"; keyword `While`, *"or optionally the keyword 'During'"* (Terzakis 2013). A state persists; it has duration.
- **Event-driven** — "Are initiated when and only when a trigger occurs or is detected" (Terzakis 2013). An event is instantaneous.
- **Optional feature** — "Are invoked only in systems that include the particular optional feature" (Terzakis 2013). This is about **build/configuration variance**, not runtime state. That distinction is the #1 confusion in practice: `Where` = "this deployment has the feature at all", `While` = "the feature is currently on".
- **Unwanted behaviour** — "Handle unwanted behaviours including error conditions, failures, faults, disturbances and other undesired events" (Terzakis 2013).

Canonical examples from Terzakis 2013 (verbatim), one per pattern:

| Pattern | Example |
|---------|---------|
| Ubiquitous | "The software package shall include an installer." |
| Event-driven | "When a DVD is inserted into the DVD player, the OS shall spin up the optical drive." |
| Unwanted | "If the memory checksum is invalid, then the software shall display an error message." |
| State-driven | "While the heater is on, the software shall close the water intake valve." |
| Optional | "Where hardware encryption is installed, the software shall encrypt data using the hardware instead of using a software algorithm." |

### Complex / compound patterns

Mavin's official guide gives one canonical complex form:

```
While <precondition(s)>, When <trigger>, the <system name> shall <system response>
```

and notes that unwanted-behaviour complex requirements also incorporate the `If`/`Then` keywords. Terzakis describes complex requirements as those that *"describe complex conditional events involving multiple triggers, states and/or optional features"*, using *"a combination of the keywords When, If/Then, While and Where"*, with generic form `<Multiple Conditions>, the <system name> shall <system response>`.

Terzakis's three complex examples, verbatim — these are the evidence for the ordering rule:

1. *"When the landing gear button is depressed once, if the software detects that the landing gear does not lock into position, then the software shall sound an alarm."* → `when` before `if…then`
2. *"Where a second optical drive is installed, when the user selects to copy disks, the software shall display an option to copy directly from one optical drive to the other optical drive."* → `where` before `when`
3. *"While in start up mode, when the software detects an external flash card, the software shall use the external flash card to store photos."* → `while` before `when`

#### Canonical ordering rule (derived)

EARS states that clauses "always appear in the same order" but no primary source prints a single total ordering of all four condition keywords. Combining Mavin's `While … when …` with Terzakis's `Where … when …` and `When … if … then …` yields one consistent total order, which we adopt:

```
Where ≺ While ≺ When ≺ If/Then ≺ the <system name> shall <system response>
```

Rank assignment used by the linter: `where`=0, `while`/`during`=1, `when`=2, `if`=3. The rank sequence across a requirement's condition clauses must be **non-decreasing**.

Cardinality, from Mavin's ruleset:

- `where` — at most 1 (optional-feature scope is singular)
- `while` / `during` — **0..n** ("zero or many preconditions")
- `when` — at most 1 ("zero or one trigger")
- `if` — at most 1, and **requires** a matching `then` immediately before the actor
- `when` + `if` may co-occur (example 1 above): `when` carries the normal trigger, `if` carries the unwanted condition
- exactly 1 system name; 1..n system responses

**Documented as derived, not quoted.** If a future primary source contradicts the `Where ≺ While` edge, only that one comparison moves; the rest is directly sourced.

#### Where the primary sources disagree

Terzakis's event-driven template is:

```
WHEN <trigger> <optional precondition> the <system name> shall <system response>
```

i.e. precondition **after** the trigger, unmarked, no comma. Mavin's guide puts the precondition **first**, marked with `While`, comma-separated. These are incompatible.

**Adjudication:** follow **Mavin**. He is the author, his guide is current (2026), and his form is the one that is parseable — an unmarked, uncommaed precondition floating after a trigger cannot be machine-separated from the trigger itself. Terzakis 2013 is a high-quality secondary teaching source and we cite it for examples and the problem taxonomy, not for grammar. The linter rejects Terzakis's event-driven form in strict mode.

---

# The linter

This section is the deliverable. Target: **Go standard library only** — `regexp` (RE2), `strings`, `unicode`. No modules, no NLP, no POS tagger. RE2 means **no backreferences and no lookaround**; every expression below respects that.

## Design shape

Not one monolithic regex per pattern. Monolithic patterns break on any condition clause containing a comma or the word "the", and they give useless error messages. Instead: **three stages**.

```
Normalize  →  Split (head-marker anchoring)  →  Classify + Lint
```

- **Stage 1 — Normalize.** Strip markdown list markers and requirement IDs, fold smart quotes/dashes/NBSP to ASCII, collapse whitespace.
- **Stage 2 — Split.** Find the **last** occurrence of the *head marker* `[, ]the <name> shall`. Everything before it is the condition prefix; the captured name is the system; everything after is the response. Anchoring on the *last* match is what makes conditions containing "the" safe.
- **Stage 3 — Classify + Lint.** Parse the prefix into ordered keyword clauses → classify into one of five (or Complex, or reject). Then run independent lint rules over the parts.

This is the same architecture the only extant Go implementation uses (`labeth/ears-lint-go`: "shell parsing, pattern classification, boolean clause parsing, catalog matching"; MIT; 0 stars, fetched 2026-08-03) — arrived at independently, which is mild evidence it is the right decomposition.

## Stage 1 — Normalization

```go
package earslint

import (
	"regexp"
	"strings"
)

var (
	reWS       = regexp.MustCompile(`\s+`)
	reListMark = regexp.MustCompile(`^\s*(?:[-*+]|\d+[.)])\s+`)
	reReqID    = regexp.MustCompile(`^\s*(?:\*\*)?(?:FR|NFR|AC|REQ)-\d+(?:\*\*)?\s*[:.\x{2013}\x{2014}-]\s*`)

	folder = strings.NewReplacer(
		"‘", "'", "’", "'",
		"“", `"`, "”", `"`,
		"–", "-", "—", "-",
		" ", " ", "…", "...",
	)
)

// Normalize prepares one candidate requirement line for parsing.
func Normalize(line string) string {
	s := folder.Replace(line)
	s = reListMark.ReplaceAllString(s, "")
	s = reReqID.ReplaceAllString(s, "")
	return reWS.ReplaceAllString(strings.TrimSpace(s), " ")
}
```

Note `\x{2013}` inside the character class — Go's `regexp` accepts `\x{...}` for literal runes; putting a raw `–` in a class also works but is easy to corrupt on copy-paste.

## Stage 2 — Head-marker split

```go
// Strict: the actor must be preceded by start-of-line or a comma.
var reHeadStrict = regexp.MustCompile(
	`(?i)(?:^|,\s*)(then\s+)?the\s+([A-Za-z][A-Za-z0-9 _/.\-]{1,58}?)\s+shall\s+`)

// Lenient: also allow a bare space before the actor, for Kiro-style
// "WHEN a user submits valid data THE SYSTEM SHALL create an account".
var reHeadLenient = regexp.MustCompile(
	`(?i)(?:^|[,\s]\s*)(then\s+)?the\s+([A-Za-z][A-Za-z0-9 _/.\-]{1,58}?)\s+shall\s+`)

type Split struct {
	Prefix   string // condition clauses, may be ""
	HasThen  bool
	System   string
	Response string
	OK       bool
}

func SplitLine(s string, lenient bool) Split {
	re := reHeadStrict
	if lenient {
		re = reHeadLenient
	}
	ms := re.FindAllStringSubmatchIndex(s, -1)
	if len(ms) == 0 {
		return Split{}
	}
	m := ms[len(ms)-1] // LAST match wins — this is the whole trick

	sp := Split{OK: true}
	sp.Prefix = strings.TrimRight(strings.TrimSpace(s[:m[0]]), ",")
	sp.HasThen = m[2] != -1
	sp.System = strings.TrimSpace(s[m[4]:m[5]])
	sp.Response = strings.TrimSpace(s[m[1]:])
	sp.Response = strings.TrimSuffix(sp.Response, ".")
	return sp
}
```

Why the system-name class excludes `,`: it is what prevents `"When the user opens the form, the app shall …"` from splitting at `"the form"`. The class allows spaces (multi-word component names like `billing service`) but never a comma, so a candidate actor can never straddle a clause boundary. Combined with **last-match-wins**, this handles every realistic sentence without a parser.

## Stage 3a — Clause parsing and classification

```go
type Pattern string

const (
	PatUbiquitous Pattern = "ubiquitous"
	PatState      Pattern = "state-driven"
	PatEvent      Pattern = "event-driven"
	PatOptional   Pattern = "optional-feature"
	PatUnwanted   Pattern = "unwanted-behaviour"
	PatComplex    Pattern = "complex"
	PatInvalid    Pattern = "invalid"
)

var reClauseKW = regexp.MustCompile(`(?i)^(while|during|when|where|if)\b\s*(.*)$`)

var kwRank = map[string]int{
	"where": 0, "while": 1, "during": 1, "when": 2, "if": 3,
}

type Clause struct {
	KW   string // lowercased
	Body string
}

// ParseClauses splits the condition prefix on commas; every segment must
// open with an EARS keyword.
func ParseClauses(prefix string) ([]Clause, []string) {
	var out []Clause
	var errs []string
	if strings.TrimSpace(prefix) == "" {
		return out, errs
	}
	for _, seg := range strings.Split(prefix, ",") {
		seg = strings.TrimSpace(seg)
		if seg == "" {
			continue
		}
		m := reClauseKW.FindStringSubmatch(seg)
		if m == nil {
			errs = append(errs, "E004 clause does not open with an EARS keyword: "+seg)
			continue
		}
		out = append(out, Clause{KW: strings.ToLower(m[1]), Body: strings.TrimSpace(m[2])})
	}
	return out, errs
}

func Classify(cl []Clause, hasThen bool) (Pattern, []string) {
	var errs []string

	// ordering: ranks must be non-decreasing
	last := -1
	for _, c := range cl {
		r := kwRank[c.KW]
		if r < last {
			errs = append(errs, "E005 clause order violates Where<While<When<If: "+c.KW+" appears too late")
		}
		last = r
	}
	// cardinality
	count := map[string]int{}
	for _, c := range cl {
		k := c.KW
		if k == "during" {
			k = "while"
		}
		count[k]++
	}
	for _, k := range []string{"where", "when", "if"} {
		if count[k] > 1 {
			errs = append(errs, "E007 more than one '"+k+"' clause")
		}
	}
	if count["if"] > 0 && !hasThen {
		errs = append(errs, "E006 'If' clause without matching 'then' before the actor")
	}
	if count["if"] == 0 && hasThen {
		errs = append(errs, "E006 'then' present without an 'If' clause")
	}

	switch {
	case len(errs) > 0:
		return PatInvalid, errs
	case len(cl) == 0:
		return PatUbiquitous, errs
	case len(cl) > 1:
		return PatComplex, errs
	}
	switch cl[0].KW {
	case "when":
		return PatEvent, errs
	case "while", "during":
		return PatState, errs
	case "where":
		return PatOptional, errs
	case "if":
		return PatUnwanted, errs
	}
	return PatInvalid, append(errs, "E004 unrecognised keyword")
}
```

## Stage 3b — Lint rules

Every rule is an independent regex over one of `{whole line, prefix, clause body, system, response}`. Severity: **E** = error (blocks), **W** = warning (annotates).

```go
var (
	reShall   = regexp.MustCompile(`(?i)\bshall\b`)
	reWeakMod = regexp.MustCompile(`(?i)(?:^|,\s*)(?:then\s+)?the\s+[A-Za-z][^,]{1,58}?\s+(must|will|should|may|can|might|is\s+able\s+to|needs?\s+to)\b`)
	rePassive = regexp.MustCompile(`(?i)^(?:be|been|being)\s+[a-z]+(?:ed|en)\b`)
	reAndOr   = regexp.MustCompile(`(?i)\s(?:and|or)\s|\band/or\b`)
	reBoolAnd = regexp.MustCompile(`(?i)\band\b`)
	reBoolOr  = regexp.MustCompile(`(?i)\bor\b`)
	rePronoun = regexp.MustCompile(`(?i)\b(it|they|them|these|those)\b`)
	reEscape  = regexp.MustCompile(`(?i)\b(if possible|as appropriate|as required|as needed|where feasible|to the extent (?:practical|possible)|and so on|etc\.?)\b`)
	reRate    = regexp.MustCompile(`(?i)\b(quickly|slowly|soon|periodically|regularly|frequently|immediately|in a timely manner|real[- ]time)\b`)
	reVague   = regexp.MustCompile(`(?i)\b(fast|quick|easy|easily|simple|robust|scalable|efficient|flexible|user[- ]friendly|intuitive|seamless|modern|reliable|appropriate|adequate|sufficient|reasonable|minimal|optimal|approximately|about|roughly|some|several|many|most|few|various|normal|typical|usual|state[- ]of[- ]the[- ]art|best practice)\b`)
	reWeasel  = regexp.MustCompile(`(?i)^(support|handle|process|manage|deal with|take care of|address)\b`)
	reVagueSys = regexp.MustCompile(`(?i)^(system|software|application|app|product|platform|tool|it|we)$`)
	rePeriod  = regexp.MustCompile(`\.$`)
)
```

Rule table:

| ID | Sev | Applies to | Test | Rationale / source |
|----|-----|-----------|------|--------------------|
| E001 | error | line | `!reShall.MatchString(line)` and no weak modal | No obligation → not a requirement |
| E002 | error | line | `len(reShall.FindAllString(line,-1)) > 1` | Two `shall` = two requirements in one line (Rolls-Royce "complexity"/"duplication") |
| E003 | error | line | `!Split.OK` while `shall` present | Missing actor / passive construction — nobody is responsible |
| E004 | error | prefix | clause does not open with a keyword | Unparseable condition |
| E005 | error | clauses | rank sequence decreasing | "The clauses … always appear in the same order" (Mavin) |
| E006 | error | clauses | `if` without `then`, or `then` without `if` | Mavin's unwanted-behaviour template |
| E007 | error | clauses | >1 `where` / `when` / `if` | "Zero or one trigger" (Mavin ruleset) |
| E008 | error | line | `reWeakMod` matches and no `shall` | must/will/should/may ≠ shall; **auto-fixable** |
| E009 | error | clause body | `reBoolAnd && reBoolOr && !strings.Contains(body,"(")` | Mixed and/or without parens has no defined precedence |
| E010 | error(strict) / warn | line | `!rePeriod` | Sentence terminator; cheap, catches truncation |
| W101 | warn | response | `rePassive` | Passive response hides the object of the action |
| W102 | warn | response | `reAndOr` | Compound response usually hides two requirements — **split it** |
| W103 | warn | line | `reVague` | Vagueness (Rolls-Royce problem #2); superset of our existing r5 list |
| W104 | warn | line | `reEscape` | INCOSE "optional escape clause" — unverifiable get-out |
| W105 | warn | response | `rePronoun` | Ambiguous referent. Deliberately excludes `this`/`that` (too many relative-clause false positives) |
| W106 | warn | `if` body | matches `(?i)\b(?:the\s+)?(?:user\|customer\|visitor\|admin\|client)\s+\w*(?:click\|submit\|select\|enter\|request\|upload\|tap\|choose\|open\|press)` | `if` used for a *normal* event → should be `When` |
| W107 | warn | `when` body | matches `(?i)\b(fail\|fails\|error\|invalid\|timeout\|times out\|unavailable\|denied\|expired\|corrupt\|exceeds?\|rejected\|missing\|unauthori[sz]ed)\b` | `when` used for a *failure* → should be `If … then` |
| W108 | warn | line | `reRate` | Unquantified rate/latency — needs a number and a unit |
| W109 | warn | response | `>30` words | Wordiness (Rolls-Royce problem #6) |
| W110 | warn | clauses | `len(clauses) > 3` | "Requirements with excessive preconditions can produce unwieldy single sentences" (Wikipedia, EARS limitations, fetched 2026-08-03) |
| W111 | warn | system | `reVagueSys` | "the system" is legal EARS but useless traceability — name the component |
| W112 | warn | response | `reWeasel` | Terzakis's own example: *"The software shall support a water level sensor." — What does the word 'support' mean?* |
| W113 | warn | pattern | `PatUbiquitous` on a line whose response contains a verb of reaction | "Most requirements are not ubiquitous" (Terzakis) — prompt the author for the missing trigger |

W113 is deliberately a **prompt, not a check**: any ubiquitous classification emits an informational "is there an unstated trigger here?" That single nudge is where Terzakis reports most real defects live.

### The `if` vs `when` trap, stated plainly

This is the single most common EARS error and it is **not** syntactically detectable — both forms parse. The semantic rule:

- `When` = an expected event on the happy path. It **will** happen in normal operation.
- `If` = an undesired condition. You would rather it never happened.

W106/W107 are heuristics on vocabulary, and they are honestly lossy. They should be warnings forever, never errors. The correct product answer is not a better regex — it is to **generate** the keyword from context: our `user-flows.md` already separates "Happy path" from "Negative paths", so an EARS generator reading that file knows which keyword to emit with 100% accuracy. Detection is hard; generation is trivial. Lean on generation.

### Other ambiguity traps the linter must own

| Trap | Why regex catches it | Why regex is not enough |
|------|----------------------|-------------------------|
| **Missing actor** | `shall` with no `the <X> shall` → E003 | Author may write "the user shall" — grammatically fine, semantically wrong: EARS constrains the *system*, not the human. Needs a role check against a catalogue. |
| **Passive voice** | `shall be <verb>ed` → W101 | `shall be logged` is caught; `shall log` with an unnamed logger is not. |
| **and/or compounds** | W102 on the response | `and` in a *condition* is legal boolean composition, not a defect. Rule must apply to the response only — which is why the split stage matters. |
| **Two `shall`s** | E002 | Cheap and reliable. Highest-yield rule in the set. |
| **Unquantified everything** | W103/W108 | A number without a unit ("within 5") passes. Add a paired check: a bare integer in the response with no unit token nearby → W114. |
| **Incomplete logic** | not caught | Terzakis, verbatim: *"If a boot disk is detected in the system, the software shall boot from it. — What if a boot disk is not present? The logic is incomplete."* **No line-level linter can catch this.** It is a set-level coverage check: for every `If X` requirement, does a requirement covering `not X` exist? Ship it as a separate `faion lint requirements --coverage` pass over the whole file. |

## CLI shape

```
faion lint requirements <path>... [--strict] [--lenient] [--json] [--fix]
```

Candidate-line extraction from Markdown, in order of precedence:
1. Table rows under a column headed `Statement` / `Requirement` / `Acceptance criteria`
2. List items under a heading matching `(?i)^#{2,4}\s*(requirements|acceptance criteria)`
3. Lines matching `^\s*(?:[-*]\s*)?(?:\*\*)?(?:FR|NFR|AC)-\d+`

Output: `path:line:col  SEVERITY  CODE  message` — the standard compiler shape, so any editor's problem matcher picks it up with zero integration work.

Exit codes: `0` clean · `1` at least one error · `2` usage/IO failure.
`--fix` handles exactly one class safely: **E008 modal normalisation** (`must`/`will`/`should` → `shall`). Nothing else is auto-fixable without changing meaning.

## Worked examples

**PASS**

| Line | Classified | Notes |
|------|-----------|-------|
| `The billing service shall retain invoices for 7 years.` | ubiquitous | clean |
| `When a customer submits the checkout form, the payment service shall create a charge intent.` | event-driven | clean |
| `While the account is in trial state, the billing service shall reject all charge attempts.` | state-driven | clean |
| `Where the multi-currency feature is enabled, the dashboard shall display amounts in the account currency.` | optional-feature | clean |
| `If the payment provider returns a declined status, then the checkout page shall display the message "Card declined".` | unwanted-behaviour | clean |
| `While the account is in trial state, when a customer submits the checkout form, the billing service shall display the upgrade prompt.` | complex | ranks 1,2 — non-decreasing |
| `When the export job starts, if the storage quota is exceeded, then the export service shall abort the job.` | complex | ranks 2,3 — matches Terzakis's landing-gear shape |

**FAIL**

| Line | Codes | Why |
|------|-------|-----|
| `The app should be fast.` | E001, E008, W103, W111 | no `shall`; weak modal; "fast"; actor is "app" |
| `Users get an email when they sign up.` | E001, E003 | no obligation, no system actor |
| `Data is backed up regularly.` | E001, E003, W108 | passive, actorless, unquantified rate |
| `The system shall validate the input and shall persist the record.` | E002 | two `shall` = two requirements |
| `When the payment fails, the billing service shall retry.` | W107 | failure under `When` → should be `If … then` |
| `If the user clicks Export, the report service shall generate a CSV.` | E006, W106 | missing `then`; normal event under `If` |
| `The export service shall generate a CSV and email it to the account owner.` | W102, W105 | compound response hides two requirements; `it` is ambiguous |
| `When the trial ends, the system shall be notified.` | W101, W111 | passive response; unnamed actor |
| `The system shall support a water level sensor.` | W112, W111 | Terzakis's own example — "support" means nothing |
| `The API shall respond within 200 if the load is normal or the cache is warm and the region is EU.` | E005, E009, W103, W114 | `if` after the actor (order); mixed and/or without parens; "normal"; `200` with no unit |

## Ten before → after rewrites

Realistic solopreneur-SaaS scenarios. Each names precisely which ambiguity the rewrite removed.

**1. Latency**
- ❌ `The app should be fast.`
- ✅ `The checkout service shall return a response to POST /orders within 400 ms at the 95th percentile under 50 concurrent sessions.`
- Removed: weak modal (`should`→`shall`); vague token `fast`; unnamed actor (`app`→`checkout service`); unmeasurable → threshold + percentile + load condition, all of which a load test can assert.

**2. Signup email**
- ❌ `Users get an email when they sign up.`
- ✅ `When a visitor submits the signup form with a valid email address, the onboarding service shall send the welcome email within 60 seconds.`
- Removed: no actor (who sends?); "get" as a system response; unstated validity precondition; no timing bound. Also flipped the subject from user to system — EARS constrains the system, never the human.

**3. Payment failure (and the compound trap)**
- ❌ `Handle payment failures gracefully.`
- ✅ `If the payment provider returns a declined status, then the checkout page shall display the message "Card declined — try another card".`
- ✅ `If the payment provider returns a declined status, then the cart service shall retain the cart contents for 24 hours.`
- Removed: weasel verb `handle`; vague `gracefully`; missing actor; and — critically — **one prose sentence was two requirements**. The first draft of the fix (`…shall display X and retain Y`) trips W102; splitting is the point.

**4. Feature-flag vs runtime state**
- ❌ `The dashboard shows revenue in the user's currency, if they set one.`
- ✅ `Where the multi-currency feature is enabled for the account, the dashboard shall display revenue amounts in the account's configured currency.`
- Removed: `if`/`where` confusion — this is deployment/plan configuration, not an error condition; ambiguous pronoun `they`; `shows` → `shall display`.

**5. Trial billing**
- ❌ `While the trial is active users can't be charged.`
- ✅ `While the account is in trial state, the billing service shall reject every charge request for that account.`
- Removed: negative capability phrasing (`can't be charged` — by whom?); missing comma boundary; no actor. Prohibitions get restated as a positive system response ("shall reject"), which is testable; "shall not" is not.

**6. Account lockout**
- ❌ `The system will lock the account after too many login attempts.`
- ✅ `When the count of consecutive failed login attempts for an account reaches 5 within 15 minutes, the auth service shall lock the account for 30 minutes.`
- Removed: modal `will`; `too many` (no threshold); no window; no lock duration; anonymous `the system`.

**7. Export formats**
- ❌ `Export should support CSV and PDF.`
- ✅ `When an account owner requests an export in CSV format, the report service shall produce a UTF-8 CSV file.`
- ✅ `When an account owner requests an export in PDF format, the report service shall produce a PDF/A-2b file.`
- Removed: `should`; weasel `support`; `and`-compound hiding two independent requirements with different acceptance criteria; missing trigger (export happens on request, it is not a ubiquitous property).

**8. Keyword misuse**
- ❌ `If the user clicks Export, the system generates a file.`
- ✅ `When an account owner selects Export, the report service shall generate a download file.`
- Removed: `If` used for a happy-path event (W106); missing `then` had `If` been correct (E006); missing `shall`; anonymous actor.

**9. Backups**
- ❌ `Data is backed up regularly.`
- ✅ `The backup job shall write a full snapshot of the primary database to object storage every 24 hours.`
- Removed: passive voice with no agent; `regularly` (W108) → explicit period; unstated scope (which data?) → named source and destination. Correctly classified **ubiquitous** — it is a standing property, no trigger.

**10. The one that should not be an EARS requirement at all**
- ❌ `The onboarding flow needs to be intuitive for non-technical users.`
- ✅ (requirement) `The onboarding wizard shall complete account setup in no more than 4 screens.`
- ✅ (not a requirement) The *goal* "non-technical users can self-onboard" moves to `roadmap.md` success metrics with a measured target: first-session activation rate ≥ 60%, measured over 30 days.
- Removed: `intuitive` is unverifiable at the sentence level. This is the most important rewrite in the list because it demonstrates the limit: **EARS's correct answer to a quality goal is to refuse it and route it elsewhere**, not to dress it in `shall`.

## Honest limits

**EARS makes a requirement unambiguous. It does not make it correct.**

`When a customer submits the checkout form, the payment service shall charge the customer twice.` is perfect EARS. It parses clean, classifies as event-driven, trips zero lint rules, and is a catastrophic bug. Every claim we make about the linter must respect this line: it is a **grammar checker for requirements**, in exactly the sense that `gofmt` is not a type checker. Selling it as anything more is a lie that the first customer will catch.

Specifically, EARS does **not** give you:

1. **Correctness.** See above.
2. **Completeness of the set.** Terzakis's boot-disk example — an `If X` with no coverage of `not X` — is invisible to a line-level linter. This needs a separate set-level pass and is the highest-value follow-on feature.
3. **Consistency between requirements.** Two requirements can each be valid EARS and directly contradict each other.
4. **Non-conflicting priority or scope.** That is what our FR-NNN priority field is for.
5. **A fit for goals.** "Grow MRR to €10k" is not a system response to a condition. Route to `roadmap.md`.
6. **A fit for most quality attributes.** Wikipedia's own limitations note (fetched 2026-08-03): EARS "suits conditional behaviour poorly for architectural constraints and non-functional requirements not expressible as system responses to conditions." Some NFRs *are* expressible ("The service shall encrypt data at rest using AES-256") — those should use EARS. Architectural constraints ("the system shall be modular") should not: they pass the grammar and mean nothing. **Rule for us: EARS is mandatory for FR-*, advisory for NFR-*.**
7. **A fit for research/spike work.** A spike's output is learning, not a system response. Our `spec-requirements` methodology already declares this in its Skip-If block; EARS inherits that skip.
8. **A fit for data model and domain definitions.** "An Invoice belongs to exactly one Order" is an invariant, not a behaviour. Route to `project-spec/`.
9. **Readable output under load.** Wikipedia: requirements with excessive preconditions "can produce unwieldy single sentences." At 4+ condition clauses the sentence becomes worse than a table. W110 warns; the correct fix is usually to lift the preconditions into a state machine and write one requirement per transition.
10. **Temporal richness.** EARS has no `until`, no `for the duration of`, no `at most N times per`, no probabilistic form. All of that gets smuggled into free-text `<system response>` where the linter cannot see it.

What EARS *does* give you, and nothing else in the landscape does: **a requirement either parses or it does not, and that verdict costs microseconds and zero API calls.** For a Go single binary sold to solopreneurs, that economic property is the entire reason this is Layer 2's best borrowable idea.

## Does anything machine-validate EARS today?

Directly relevant to whether a faion linter is a differentiator. Evidence, all dated:

| Tool | Validates EARS? | Detail | Verified |
|------|-----------------|--------|----------|
| **Kiro** (AWS) | **No** | EARS is a writing convention in `requirements.md`. No mention of validate/lint/parse/enforce in kiro.dev/docs/specs or the requirements-first page. | 2026-08-03 |
| **GitHub spec-kit** | **No** | Issue **#1356** "Feature Request: EARS Integration" (opened **2025-12-20**) proposed templates, lint suggestions and an EARS slash command. **Closed**, not implemented. | 2026-08-03 |
| **QVscribe** (QRA Corp) | **Yes** | v2.10 announcement **2019-08-21**: "automated templating and compliance checking of the Easy Approach to Requirements Syntax (EARS) and INCOSE Guidelines". NLP-based. Integrates with DOORS Next, Jama, Polarion, Word, Excel. Enterprise-priced; not publicly listed. | 2026-08-03 |
| **IBM DOORS / Jama / Polarion** | **Not natively** | They are the host; QVscribe is the analyser layer on top. | 2026-08-03 |
| **`labeth/ears-lint-go`** | **Yes** | MIT-licensed Go library — shell parsing, pattern classification, boolean clause parser (`and`/`or`/`not`/parens), catalog matching, clause-order and vague-language rules. **0 stars**, last update April. Genuinely a working library, not a stub. | 2026-08-03 |
| **`tbhb/vale-ears`** | **Partially** | MIT Vale style package. Four rules: `ears.Syntax` (five-pattern conformance), `ears.Shall`, `ears.PassiveVoice`, `ears.WeakWords`. **0 stars**. Requires Vale (Go binary, but an external dependency). | 2026-08-03 |
| **`chubozeko/EARS-Rule-Detection`** | Research | Python NLP coursework (University of Oulu) detecting EARS structure. Not a product. | 2026-08-03 |

**Committed answer:** *Yes, EARS is machine-validated today — but only in enterprise requirements suites (QVscribe, ~2019 onward) and in two zero-star hobby repos.* **No tool in the AI-agent SDLC segment validates EARS as of 2026-08-03.** Kiro writes it and never checks it; spec-kit considered and declined.

So the honest framing for faion is **not** "we invented EARS validation" — that claim is falsifiable in one search and would burn credibility. It is: **"the first EARS validator that ships inside your coding agent's workflow, in a single binary, for a solo founder — no DOORS, no Jama, no seat licence."** That is true, defensible, and still a real wedge. It also means `labeth/ears-lint-go` (MIT) should be **read before we write ours** — either as prior art to learn from or as a dependency-free vendoring candidate.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|--------------|---------|
| 1 | EARS Official Guide — Alistair Mavin | https://alistairmavin.com/ears/ | **Authoritative.** Five templates verbatim, complex pattern, ruleset (0..n preconditions / 0..1 trigger / 1 system / 1..n responses), "clauses always appear in the same order" | 2026-08-03 |
| 2 | Terzakis, *EARS: The Easy Approach to Requirements Syntax*, Intel, ICCGI 2013 tutorial (v1.0, 2013-07-21, Nice) | https://www.iaria.org/conferences2013/filesICCGI13/ICCGI_2013_Tutorial_Terzakis.pdf | **Best teaching source.** Pattern table, 3 examples per pattern, 3 complex examples, the 8 Rolls-Royce problem types, the requirements-issues taxonomy, Planguage integration, before/after rewrites. Extracted locally via `pdftotext` | 2026-08-03 |
| 3 | Mavin, Wilkinson, Harwood, Novak — *Easy Approach to Requirements Syntax (EARS)*, RE'09 | https://ccy05327.github.io/SDD/08-PDF/Easy%20Approach%20to%20Requirements%20Syntax%20(EARS).pdf | Original paper; `[Precondition]* [Trigger]? [Feature]` skeleton, industrial results. ⚠️ Fetched via summariser — treat quotes from this row as **unverified paraphrase**, see staleness | 2026-08-03 |
| 4 | Wikipedia — Easy Approach to Requirements Syntax | https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax | Independent confirmation of all five templates + complex; adoption list; **limitations section**; notes Kiro's 2025 EARS adoption | 2026-08-03 |
| 5 | Kiro — Requirements-First Workflow | https://kiro.dev/docs/specs/feature-specs/requirements-first/ | Kiro's EARS framing, `WHEN … THE SYSTEM SHALL …` dialect, **no validation language** | 2026-08-03 |
| 6 | QRA Corp — Introducing QVscribe 2.10 | https://qracorp.com/news/introducing-qvscribe-2-10-automated-ears-requirements-templating-incose-compliance/ | Published **2019-08-21**. Automated EARS templating + compliance checking; DOORS/Jama/Polarion/Office integration | 2026-08-03 |
| 7 | GitHub spec-kit issue #1356 | https://github.com/github/spec-kit/issues/1356 | Opened 2025-12-20, **closed**. Proposed EARS templates / lint / slash command. Not implemented | 2026-08-03 |
| 8 | `labeth/ears-lint-go` | https://github.com/labeth/ears-lint-go | MIT Go EARS linter — parser architecture, boolean clause grammar, catalog matching, strict mode. 0 stars | 2026-08-03 |
| 9 | `tbhb/vale-ears` | https://github.com/tbhb/vale-ears | MIT Vale package — `ears.Syntax`, `ears.Shall`, `ears.PassiveVoice`, `ears.WeakWords`. 0 stars | 2026-08-03 |

## What to borrow for faion

1. **The five patterns, verbatim and unmodified.** No faion dialect, no renamed keywords, no localised syntax. The whole value is that it is a 17-year-old standard other people already know.
2. **The linter, in Go, in `faion-cli`.** `faion lint requirements` per the design above. Stdlib-only, no runtime Python — this is the concrete artefact the whole dossier exists to justify.
3. **The clause-order rule as a *derived* total order** `Where ≺ While ≺ When ≺ If/Then`, published with its evidence so the derivation is auditable.
4. **Terzakis's problem taxonomy as the warning catalogue.** The eight Rolls-Royce problem types map almost one-to-one onto our W-rules. Free, sourced rationale for every warning we emit — which is exactly what makes a linter credible instead of nagging.
5. **`user-flows.md` → EARS generation.** Our happy-path/negative-path split *already encodes the `When`/`If` distinction* that the linter cannot reliably detect. Generating EARS acceptance criteria from user flows is a higher-value feature than linting hand-written ones, and it is nearly free.
6. **The set-level coverage pass** (`If X` with no `not X` counterpart). Sourced directly to Terzakis's boot-disk example. Nobody in the segment does this.

## What NOT to borrow — and why

1. **Kiro's ALL-CAPS comma-less dialect.** `WHEN … THE SYSTEM SHALL …` loses the comma boundary that makes parsing cheap and unambiguous. Accept it in `--lenient`, never canonicalise it.
2. **Terzakis's event-driven template** with an unmarked precondition trailing the trigger. Unparseable. Follow Mavin.
3. **EARS for everything.** Do not apply it to NFRs wholesale, goals, spikes, data invariants or UX quality. §Honest limits enumerates the routes; a maximalist rollout is how a good idea gets a bad reputation.
4. **An NLP/POS-tagger implementation.** A dependency-free RE2 pipeline gets ~95% of the value at 0% of the binary weight. `chubozeko/EARS-Rule-Detection` is the cautionary example: research-grade, unshippable.
5. **Vale as the delivery vehicle.** `vale-ears` is decent prior art, but Vale is an external binary and a config format. faion-cli must not require it.
6. **Hard-blocking on day one.** Ship as warnings, add `--strict` for CI, and only then consider a blocking `PreTaskExec`-style gate. A linter that blocks before its false-positive rate is known gets disabled permanently in week one.
7. **The claim "we're the first to validate EARS."** False. See §Does anything machine-validate EARS.

## Mapping to our corpus

`~/workspace/projects/faion-net/faion-network` — 2622 methodologies over 23 domains under `skills/faion/knowledge/<domain>/<slug>/`; `skills/tier-manifest.json` v8 = 3070 entries.

### `sdd/spec-requirements/` — EARS **composes**, does not replace

Our existing methodology (read 2026-08-03) defines: FR-NNN / NFR-NNN stable numbering (r1), one declarative sentence each (r2), mandatory verification method (r3), priority must/should/could (r4), banned vague tokens `fast, easy, simple, robust, scalable` (r5), traceability to impl-plan and test-plan (r6). Output contract requires `verification_method` non-empty and rejects non-empty `vague_tokens_found` in a final artefact.

EARS touches **one field**: the requirement's `statement`. Everything else in our methodology is orthogonal metadata that EARS has no opinion about — and that EARS badly needs. This is a clean composition, not a competition:

| Our element | Relationship to EARS |
|-------------|----------------------|
| FR-NNN / NFR-NNN (r1) | **Keep.** EARS has no identity or traceability concept at all. This is our layer, and it is the layer that makes requirements referenceable forever. |
| One declarative sentence (r2) | **Upgrade.** r2 is today a prose rule an agent may or may not honour. EARS turns it into a machine check: E002 (two `shall`) is exactly "you wrote two requirements". |
| Verification method (r3) | **Keep, and exploit.** EARS makes a requirement testable; r3 records *how* it is tested. The pattern even suggests the default: event-driven → integration test; state-driven → state-machine test; unwanted → negative test; ubiquitous → property/monitor; optional-feature → matrix/flag test. Auto-suggest `verification_method` from `ears_pattern`. |
| Priority (r4) | **Keep.** EARS is silent on priority. |
| Vague tokens (r5) | **Replace with a superset.** Our five tokens become W103's ~30, plus W104 escape clauses, W108 unquantified rates, W112 weasel verbs. Source each to Terzakis so the rejection is arguable, not arbitrary. |
| Traceability (r6) | **Keep.** Orphan detection is unaffected. |

Concrete edits proposed:

- `content/01-core-rules.xml` — add **r7-ears-conformance**: *"Every FR statement conforms to one of the five EARS patterns; NFR statements conform where the requirement is expressible as a system response to a condition."* Rationale source: Mavin RE'09 + Rolls-Royce eight-problem reduction. Rewrite **r5** to point at the linter's token list rather than an inline five-word list.
- `content/02-output-contract.xml` — add per-requirement fields `ears_pattern` (enum: `ubiquitous|state-driven|event-driven|optional-feature|unwanted-behaviour|complex|n-a`) and top-level `ears_violations` (array). Add **forbidden pattern f5**: *"any FR whose statement fails EARS classification while the artefact is submitted as final"*. Note `n-a` exists specifically so NFRs and architectural constraints can opt out **explicitly and visibly**, rather than silently.
- `scripts/validate-spec-requirements.py` — keep Python for repo-side pre-commit; it validates the JSON artefact. The **Go linter is a separate deliverable in faion-cli** and validates the Markdown prose. Two surfaces, one rule set. Do not try to share code across the language boundary; share the rule table as data.
- `AGENTS.md` — add `[[ears-notation]]` to Related; add a Prerequisites row.

### `sdd/user-flows-template/` — the strongest integration, and it is already non-technical

Our template (read 2026-08-03) is:

```
- Happy path:
  1. <action> → <expected result>
- Negative paths:
  - <case>:
    - Trigger: <what causes the error>
    - Expected UX: <what the user sees>
- Playwright spec: `<path/to/spec.ts>`
```

The mapping is one-to-one and mechanical:

| user-flows.md element | EARS output |
|-----------------------|-------------|
| Happy-path `<action> → <expected result>` | `When <action>, the <system> shall <expected result>.` — **event-driven** |
| Negative `Trigger:` + `Expected UX:` | `If <trigger>, then the <system> shall <expected UX>.` — **unwanted behaviour** |
| `Preconditions:` | `While <precondition>, …` prepended — **state-driven** / complex |
| `Actor:` | supplies the human role; the *system name* still has to be asked for once per flow |
| `Playwright spec:` | the `verification_method` for every requirement generated from that flow |

This is the answer to the non-technical question in operational form: **the founder writes the flow, the tool writes the EARS.** The only field the tool must ask for is the system/component name, and it can default that per feature.

### New methodology

Propose **one** new leaf: `skills/faion/knowledge/sdd/ears-requirements/` (2622 → 2623), following the standard shape (AGENTS.md + CLAUDE.md + `content/01..06` + templates + scripts). Content maps directly to sections of this dossier: 01-core-rules ← §Mechanics + rule table; 02-output-contract ← the `ears_pattern` enum; 03-failure-modes ← §Honest limits + the trap table; 04-procedure ← the three-stage pipeline; 05-examples ← the ten rewrites; 06-decision-tree ← "is this a system response to a condition? → EARS; else route to roadmap/project-spec/spike".

No new domain. No `tier-manifest.json` structural change — one new entry.

### faion-cli

`faion-cli` is a Go single binary with **no runtime Python dependency, ever**. The linter lives there as an internal package (`internal/earslint`) exposed as `faion lint requirements`. Stdlib `regexp`/`strings`/`unicode` only; the rule table is a Go slice of structs, not a config file, so it compiles into the sealed binary along with the corpus. `labeth/ears-lint-go` is MIT and should be read first — vendoring it is a legitimate option if its API and quality hold up on inspection.

## The non-technical question — committed answer

**Question:** a CX designer or a solo non-technical founder has to be able to write these. Is `shall` ceremony a barrier? Is there a plain-language variant that keeps machine-checkability?

**Committed answer, in five parts.**

**1. Yes, `shall` is a real barrier — and it is the cheapest barrier available.** People who have never written a requirement find `shall` archaic, legalistic and faintly absurd. That reaction is genuine and should not be argued with. But `shall` is doing enormous work: it is a single unambiguous token that marks *this clause states an obligation on the system*, it appears in no ordinary English sentence by accident, and it is therefore the anchor the entire parser hangs on. Every proposed replacement is worse: `must` collides with prose ("the user must click"), `will` collides with future tense, `should` is explicitly non-binding in RFC-2119 and its descendants, `does` is indistinguishable from description. Removing `shall` does not simplify the notation; it deletes the parse anchor and hands you back the ambiguity you were paying to remove.

**2. Therefore: keep `shall` as the canonical stored form, and never require a human to type it.** This is the resolution and it is not a compromise. Split authoring from storage:

- **Storage / lint / traceability surface:** canonical EARS with `shall`. Machine-checkable, stable, standard, portable to anyone who knows EARS.
- **Authoring surface:** three plain questions, no jargon.
  - *What has to happen first?* → `While …` (skip if "always")
  - *What sets this off?* → `When …` (skip if "nothing, it's always true") / *"and what if it goes wrong?"* → `If … then …`
  - *What does the app do?* → `the <component> shall <response>`

  The tool emits the sentence. The founder reads it back and confirms. Reading `shall` is not a barrier; **writing** it is.

**3. Accept a lenient input dialect and normalise, gofmt-style.** If someone types `must`, `will`, `has to`, `needs to` — accept it and rewrite it to `shall` with an **info**-level note, auto-fixed by `--fix` (E008). Same for `WHEN … THE SYSTEM SHALL …` without a comma. **Never reject a founder's sentence over a modal verb.** Rejection at the authoring surface is what kills adoption of every requirements discipline ever shipped; normalisation costs one regex.

**4. Do not invent a plain-language variant of the notation itself.** The tempting move — rename the keywords, drop `shall`, invent "faion-lite requirements" — is a trap for three reasons: it forfeits the 17-year credibility that is EARS's entire selling point; it forfeits interoperability with Kiro, QVscribe, spec-kit and every aerospace engineer who already knows it; and it does not actually help, because the hard part for a non-technical author was never the keywords. Watch a founder try: they will not struggle with `While` versus `When`. They will struggle to name the system, and they will write two requirements in one sentence. Those are exactly E003 and E002 — both caught, both explainable in one line of plain English. **The barrier is decomposition, not vocabulary,** and the linter already addresses the barrier that actually exists.

**5. The evidence that this works is already in our own repo.** `user-flows.md` is prose — `action → expected result`, plus negative cases with a trigger and an expected UX — and it is demonstrably writable by non-technical people; that is why it replaced `test-plan.md`. It is also, structurally, EARS with the keywords removed. So the non-technical path is not hypothetical and does not need designing: **generate EARS from user flows, lint the generated output, show the founder the flow and never the grammar.** The `shall` sentences become an artefact the *machine* reads — the same relationship the founder already has with a Playwright spec file.

**One caveat, stated plainly:** this answer is English-only. EARS is keyword-driven, and the keyword table is English. A Ukrainian-language authoring surface is feasible (the *questions* localise fine), but the stored canonical form stays English, and a Ukrainian-language corpus of requirements would need a keyword mapping table that no primary source provides. Ship English canonical, localise the prompts, defer localised syntax indefinitely.

## Open questions / staleness risk

- **Low notation risk, real link risk.** EARS is unversioned and unchanged since 2009; the grammar will not move under us. The failure mode is `alistairmavin.com/ears/` disappearing — **mirror the guide text into the methodology folder** with attribution and the 2026-08-03 fetch date.
- **RE'09 paper quotes are unverified.** Row 3 of the docs table was fetched through a summariser that returned a paraphrase, and its "optional feature" template (`The system shall <action>, where <condition>`) **contradicts** Mavin's guide and Terzakis — i.e. that fetch is demonstrably unreliable. Nothing in this dossier's grammar rests on it. **Do not quote row 3 without re-extracting the PDF locally.** (Terzakis's PDF *was* extracted locally with `pdftotext`; row 2 quotes are trustworthy.)
- **The `Where ≺ While` ordering edge is derived, not quoted.** It rests on Terzakis's optical-drive example plus Mavin's generic form. If a primary source states a different total order, only this one comparison changes — but it would change linter rule E005.
- **QVscribe pricing unknown.** Not publicly listed. Relevant to positioning ("enterprise-priced") — that adjective is an inference from its DOORS/Jama/Polarion market, not a sourced fact.
- **`labeth/ears-lint-go` not read.** Only its README was fetched. Before writing our own, read the source: it may be better than what is designed here, and it is MIT.
- **Unaudited surfaces (web-search budget exhausted at 200/200 on 2026-08-03):** the VS Code Marketplace was not searched for EARS extensions — one search result described "a VS Code extension for writing requirements faster using intuitive EARS syntax, supported by syntax highlighting and code completion", which was **never located or verified**. Also unchecked: StrictDoc, Doorstop, rmtoo and the wider Python requirements-tooling ecosystem for EARS grammar support, and the MCP-server EARS plugins alluded to by Wikipedia. **Any of these could weaken the "nothing in the AI-SDLC segment validates EARS" claim — re-run before that claim appears in marketing.**
- **False-positive rates are unmeasured.** W105 (pronouns), W106/W107 (`if` vs `when`) and W112 (weasel verbs) are heuristics with no corpus behind them. Before shipping `--strict`, run the rule set over a real corpus — our own `spec.md` files across the SDD repos are the obvious first test set — and tune. A linter's credibility is spent on its first false positive.
