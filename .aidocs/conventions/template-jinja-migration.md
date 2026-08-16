---
type: convention
title: "Templates become Jinja, variables become JSON Schema, names become one dictionary"
created: 2026-08-16
status: ratified
supersedes_parts_of: ".aidocs/conventions/template-builder.md §1, §2, §3 and its §2.3 inheritance"
applies_to: [skills/faion/knowledge/*/*/templates, skills/faion/tools/template-builder]
---

# Jinja migration

Three changes, decided together because each is weaker alone:

1. Every artefact template becomes **two Jinja templates** — `<name>.md.j2` and `<name>.html.j2`.
2. Variables are declared in **JSON Schema**, in a sibling file, not in a YAML-ish comment header.
3. All schemas draw their names from **one corpus-wide variable dictionary**, so a variable that
   appears in two templates means the same thing in both.

## 0. What this reverses, and the reasoning that was wrong

`template-builder.md` §2.3 inherited a prohibition from `retrieval-content-contracts.md`:
*"No expressions, loops, nesting, partials-in-partials or filters"*, justified as **SSTI on a
multi-tenant assembler**.

**That justification does not survive contact with the actual threat model.** Server-side template
injection requires an attacker who controls the *template*. Here the corpus authors every template
and the user supplies only **values**. Jinja binds values as context, never as source — so unless
the renderer double-renders (renders output as a template again, which this one must never do), a
value cannot become syntax. Under `SandboxedEnvironment`, with autoescape on for HTML, there is no
injection surface that the old `{{name}}`-only substitution did not equally have.

The other two reasons in §2.3 — author-learning cost and validator cost — were real and are
answered rather than dismissed: authors write **no Jinja by hand** (the converter does), and the
validator cost is paid once, in JSON Schema, which the corpus already validates in 2,081 places.

**What stays prohibited: double rendering.** The renderer takes a template and a value map. It never
treats a rendered result, a value, or anything a user supplied as template source. That single rule
is what keeps the SSTI surface at zero, and it is worth more than the whole ban it replaces.

## 1. Two templates, not one with branches

`<name>.md.j2` and `<name>.html.j2` are siblings, share one schema, and are rendered from the same
value map.

They are **not** one template with `{% if fmt == 'html' %}` in it. A conditional on output format
puts two documents in one file and guarantees they drift — the corpus already has 187 cases of
exactly that failure mode between template files and their inlined copies. Two files that a
generator writes together drift only if someone edits one by hand, which the converter can detect.

Markdown is authored; HTML is generated **from the Markdown source structure**, not by piping
rendered Markdown through a converter at runtime. The HTML template carries its own inline CSS and
must be self-contained — no external stylesheet, font or image.

## 1a. Where rendering happens, and why the `.md` survives

**Ratified 2026-08-16, after the owner corrected a question I had asked from a false premise.**

**Templates are assembled and filled on the BACKEND; a finished document is returned to the
client.** Nobody hand-fills a `.md`. That settles two things at once.

First, it removes the objection I was about to raise — that a `.md.j2` needs Jinja installed before
anyone can use it. Jinja lives on the server. `jinja2` 3.1.2 is already importable in the backend
environment and `KNOWLEDGE_ROOT` is already wired; the render endpoint itself does not exist yet and
belongs to `faion-net-be`, not here.

Second, and less comfortably: it makes `retrieval-content-contracts.md` §2.2's *"the assembler runs
on behalf of other accounts"* **the literal architecture rather than a hypothetical**. So the nine
`x-faion-sensitive` dictionary entries are not caution — their values must never reach the backend
at all. The server emits the placeholder; substitution is client-side. This also sharpens §8 of
`variable-dictionary-findings.md`: the client's local store and the multi-tenant backend are now
demonstrably **two different surfaces**, which is the whole of the argument for splitting the flag.

### The `.md` is not deleted — it becomes an output

A template exists in **both** a standalone form and a framework-consumable one. So:

| File | Role |
|---|---|
| `<name>.md.j2` | **source of truth** |
| `<name>.vars.schema.json` | **source of truth** |
| `<name>.html.j2` | generated |
| `<name>.md` | generated — the standalone artefact, and what the framework consumes |

The reason the `.md` cannot simply go away is concrete, not sentimental.
`faion-solo-framework/scripts/init_project.py` is *"the one supported way to instantiate the
template"*. It substitutes four fixed tokens — `<PROJECT>`, `<project>`, `<domain>`, `<org>` — by
literal string replacement, and its `--check` mode exits 1 if any placeholder survived. That
pipeline eats Markdown with angle-bracket tokens. It does not eat Jinja, and — worse — it would pass
straight over a `{{ var }}` without substituting it *and* without `--check` flagging it.

Drift is answered exactly as §1 answers it: **one generator writes every form in a single pass**, so
they drift only when someone hand-edits an output, which a `--check` that regenerates and compares
can detect. That is the same shape `init_project.py --check` already has.

## 1b. The runtime flow, and what it makes load-bearing

**Ratified 2026-08-16.** The owner described the actual sequence:

1. Client searches. The server answers **ascetically**: a template id plus the list of variables with
   their descriptions.
2. The **CLI fills what it can fill unambiguously** from project context and the project store.
3. Everything left goes back into the main agent's context — to look up, or to put to the user.
4. When every variable has a value, the client sends them to the backend.
5. The **backend renders** the documents from the template.

Three consequences, none of them cosmetic.

### The schema is the wire format, so `description` is product copy

`<name>.vars.schema.json` is not documentation about the template — it **is** what step 1 returns.
`description` is the sentence an agent shows a human in step 3. A thin one (`"Requirement."`,
`"Validated."`) is a defect at the protocol level, not an untidy comment. Measured on a 25-template
sample: **3 of 45 variables** are too thin to ask a human with. That is a review-queue item, not a
crisis — but it is now a product surface.

### The server MUST dereference `$ref` before answering

**16 of those 45 variables (36%) carry their description only in the dictionary**, because a `$ref`d
property correctly holds no local `description`. A server that returns the schema verbatim hands the
client an empty description for a third of its variables, and the agent then asks the user about
something the corpus already explains.

This is a hard requirement on the render/search endpoint in `faion-net-be`, and it is invisible
until someone tests with a dictionary-backed variable. Written here because that endpoint does not
exist yet and this is the note its author needs.

### `$ref` coverage IS the auto-fill rate

Step 2 can only fill a variable it can look up, and a lookup is only meaningful when the name is
canonical. `owner_handle` can be resolved from the project store; `name` cannot, because nothing
knows what it names. So the dictionary's coverage — **23.1%** of proposed declarations today — is not
a tidiness metric. It is the share of variables the user is *not* asked about.

**And this is where §8 of the findings stops being theoretical.** A `sensitive` variable is never
written to the project store, so it can never be auto-filled in step 2. `owner_full_name` is carried
by **814 templates**. Under the current rule, the corpus's single most common variable is the one
question the user is asked every single time, forever — while the backend, which is the surface
§2.2 was protecting, never needed to see it anyway.

### Sensitive values do not travel in step 4

Step 4 sends values to the backend. A `sensitive` value must not be among them. §2.2's mechanism
already says what happens instead: the assembler emits the `placeholder`, and the client substitutes
the real value into the returned document. Whoever writes the endpoint must implement that, because
the obvious implementation — send everything, render everything — puts a named human on a
multi-tenant server.

## 2. Variables live in JSON Schema

```
templates/<name>.md.j2
templates/<name>.html.j2
templates/<name>.vars.schema.json
```

Draft-07, matching the 2,081 output contracts the corpus already ships. Every property carries:

| keyword | meaning here |
|---|---|
| `type` | `string` · `integer` · `boolean` · `array` |
| `title` | the short label |
| `description` | **the question put to the author** — this is the load-bearing field |
| `enum` | closed vocabulary where one applies |
| `default` | used when the author does not answer |
| `x-faion-compose` | `true` when an LLM writes the prose from the author's answer (the old `text` type) |
| `x-faion-sensitive` | `true` for a credential **or personal data**; carries `x-faion-placeholder` |
| `$ref` | **into the dictionary — see §3** |

JSON Schema replaces the YAML-ish subset because it is machine-readable by tools that already exist,
it composes with `$ref` (15 contracts already use it), and it removes a hand-written parser that has
already been the source of two blockers this week.

### 2a. Why these paths and not tidier ones — verified against the packer

**A `.json` reaches a user's disk from under a `templates/` path segment and from nowhere else.**
`packablePath` in `faion-cli/tools/vfs-pack/pack.go` ships `.md` and `.xml` from anywhere, `.py`/`.sh`
only from `scripts/`, `.tsv`/`.txt` only from `lexicon/`, and — F036/AD-024 — **everything** under a
`templates/` segment, deliberately not extension-gated. Everything else is excluded, and `meta.json`
is excluded everywhere as packer input.

Proven by a test written against the real packer, not by reading it:
`faion/templates/vars-dictionary.schema.json` → ships; `faion/knowledge/<d>/<s>/templates/x.vars.schema.json`,
`x.md.j2` and `x.html.j2` → ship; `faion/schemas/vars-dictionary.schema.json` → **does not**.

So the layout in §2 and §3 is load-bearing, not cosmetic. Moving the dictionary into a `schemas/`
directory — the obvious tidy — makes it invisible on every user's machine while every validator in
this repo stays green, because validators read the disk and the packer decides delivery. That is
exactly the shape of CR-010, and it is why this note exists.

The same rule kills the alternative of parking the dictionary inside the tool pack: `syncPack`
materialises only each tool's script, its card and its nested helpers, so a data file there is packed
and never lands. A tool that needs the dictionary at runtime reads it from the corpus, or embeds it
with a `--file` override — the standing rule in `skills/faion/tools/AGENTS.md`.

### 2b. How §1a's four forms are actually written — `tpl-jinja --migrate`

One invocation, **atomic per template**: the three Jinja files, the `.md` regenerated from the new
`.md.j2`, the methodology's `## Templates` rows, and its inline `## Template Contents` body — or none
of them. Partial application is the outcome that must be impossible, because a `.md.j2` written
without its row makes `validate-methodology-templates.py` fail with *declared template missing*.
`--check` re-derives every generated form and diffs it, the shape `init_project.py --check` already
has. Four decisions fall out of §1a and are recorded here because the waves depend on them.

**What the regenerated `.md` puts where a variable was: `<name>`.** The incumbent angle convention,
because it is what §1a's instantiator substitutes and what its `--check` scans for. §1 of
`template-builder.md` rejected `<Angle>` as the *builder's input*, where a hand-written `<one
paragraph>` cannot be told apart from a variable; that argument does not reach an output generated
from a declared schema, where every angle token is a schema property name in snake_case. The form is
lossy in one direction — a placeholder inside a code span and a real variable become the same token
— and it was equally lossy before the migration, so nothing is given up.

**What the `## Templates` table names: two rows** — `templates/<name>.md.j2` (source) and
`templates/<name>.md` (generated) — never the `.html.j2` or the schema.
`validate-methodology-templates.py` header-checks whatever the table names, and the five-key header
exists for a human opening the file: it rides through the conversion into the `.md.j2` and back out
into the `.md`, while the `.html.j2` has no comment header at all and the schema would need a
`__faion_header__` restating its own `title`. Delivery is unaffected either way — `packablePath`
ships everything under a `templates/` segment — so the table is a reading guide, and the rule is
*name what a human opens*.

**A template no table row names is refused** (exit 5; 414 of the 2,919 are in that state). Adding a
row is a documentation decision, and CR-010 is the shape of making one silently.

**A methodology with no `## Template Contents` section keeps none.** The section exists for files the
packer does not ship standalone, and both `.md` and `.md.j2` ship by path; creating 2,505 inlines
would duplicate delivered bytes into the file every retrieval loads first. Where an inline already
exists it is regenerated, as the `.md.j2` source verbatim, by the call that writes the `.md.j2`.

## 3. The variable dictionary — the point of the whole exercise

```
skills/faion/templates/vars-dictionary.schema.json
```

One file. Every canonical variable, defined once, with its type, its meaning and its question. A
template's schema `$ref`s into it and adds only what is genuinely local.

**Convergence means fewer ambiguous names, which usually means MORE names.** This is the part that
is easy to get backwards. The most common proposed name in the corpus today is `name`, at **682
occurrences** — and that is the single worst variable we have, because it means 682 different
things. Collapsing `product_name`, `project_name` and `team_name` into `name` would make the count
look tidier and make the project store carry the wrong value silently, which is the exact opposite
of the goal.

So the rule is:

> **A dictionary entry is a name plus a meaning. Two uses share a name only when they share the
> meaning — well enough that a value carried from one artefact to the other is still correct.**

That last clause is the operational test, because the project store *does* carry values between
artefacts. If `owner` on a risk register and `owner` on a design doc would legitimately be different
people, they are two entries, not one.

Seeds, measured across the corpus by the migration tool, with their current occurrence counts —
these are candidates to *disambiguate*, not to bless: `name` 682, `date` 269, `value` 175,
`source` 116, `url` 116, `email` 111, `slug` 92, `action` 89, `artefact_id` 76, `full_name` 74.

## 4. Where Jinja may be imported

`validate-tools.py` enforces stdlib-only imports in tool-pack scripts, and it has **zero** baseline
entries — a clean gate, and weakening it with a blanket exemption would be a bad trade for one
dependency.

Instead: **a pack declares its dependencies in `meta.json`, and the validator checks imports against
stdlib plus what is declared.** The gate stays meaningful, an undeclared third-party import still
fails, and the dependency becomes visible in the manifest rather than hidden in a source file.

The rule the stdlib constraint exists to protect is unchanged and still binds: a tool must run on a
user's machine. So a tool that needs Jinja must **fail with an actionable message** when it is
absent, never half-work.

## 5. Migration is generated, then adjudicated

2,919 Markdown templates become 5,838 Jinja files plus their schemas. That is a converter's job.

The converter proposes; a human or an agent adjudicates the cases it flags. It has already been
measured on this corpus: of 1,469 templates carrying placeholders, **57% of placeholders map
mechanically but only 11.5% of templates need no human at all.** Those numbers set the plan — this
is batch conversion with a review queue, not an unattended script, and any schedule that assumes
otherwise is wrong.

The converter must refuse rather than guess. A placeholder that is prose (`<Optional: 'ready for
owner review'>`) is guidance to a reader, not a variable, and declaring it produces a build that
refuses by name for a parameter that should never have existed.

## 6. What is out of scope

- **Non-Markdown templates.** The 1,705 `.json`, 799 `.py`, 546 `.yaml` and 257 `.sh` templates are
  code and config scaffolds, not documents. They keep their current form.
- **Runtime substitution.** A template needing values filled per-invocation rather than per-artefact
  (`ai-core/judge-calibration-protocol`) is still unserved; §5b of the builder doc records it.
- **The 1,183 already-HTML-escaped placeholders.** They must be un-escaped before they can be
  variables at all. That is a prerequisite, not part of this.
