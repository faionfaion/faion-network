---
type: backlog
title: "Jinja template migration — what shipped, what is left, what needs a decision"
created: 2026-08-23
status: open
affected_components: [faion-network/skills/faion/knowledge, faion-network/skills/faion/tools/template-builder, faion-network/skills/faion/templates]
relates_to: ".aidocs/conventions/template-jinja-migration.md; .aidocs/improvements/CR-013-placeholders-the-converter-gets-wrong.md; .aidocs/improvements/variable-dictionary-findings.md"
---

# Jinja migration — backlog

Written at the end of the migration loop so the remaining work survives the session that
found it. **Every number here was measured on disk at `88946ebac`, not carried over from a
report.** Re-measure before acting: the commands are given so the figure can be reproduced
rather than trusted.

## Shipped

| | count |
|---|--:|
| declared templates | 2,878 |
| migrated (`.md.j2` + `.vars.schema.json` + `.html.j2`, all three present) | **2,875** |
| declared but unconvertible | 3 |
| undeclared `.md` on disk (38 of them `_smoke-test*`) | 41 |
| dictionary entries (`templates/vars-dictionary.schema.json`) | 66 |
| resolver rules (`templates/vars-resolver.json`) | 30 |
| self-test checks across the five tools | 191 pass / 0 fail |

Source of truth is `<name>.md.j2` + `<name>.vars.schema.json`; `<name>.html.j2` and `<name>.md`
are **generated outputs**. The `.md` survives because the framework consumes it as a page — it
is not a second source, and editing it is a change that the next generate erases.

The three refusals are honest, not skipped: two are Mustache loops (§2.3 has no `{% for %}`)
and one is a `CHANGELOG.md` whose heading this repo's own pre-commit hook greps for, so
templating it would break the gate that guards it.

## Open work — no decision needed, only execution

### 1. CR-013 §1 — CLOSED 2026-09-10: the repair had already landed, and the path recommended below would have regressed 55 templates

> **Correction.** This section said *"the scanner fix landed; the corpus repair did not"* and set
> **161 templates / 1,055 tokens** as the repair target. Both halves were wrong, and the repair it
> recommended is actively harmful. Verified by running the converter, not by re-running the regex.
>
> **The repair landed.** In `3700e6566 fix: see a mixed-case brace placeholder`,
> `ae71dde1e fix: reconvert 158 templates with braces` and
> `5f1dd8b9d fix: re-convert 45 templates under new rules` — all three **before** `88946ebac`, the
> commit this document says it measured at. The residual 1,055 tokens are not unrepaired files.
> They are **what the corrected scanner deliberately leaves literal**, which is the documented
> behaviour: a prose placeholder, a per-row cell, a collision and a code-fence placeholder are each
> reported by reason and left alone.
>
> **Method.** For each of the 161: restore the pre-migration `.md` (`git show <add-commit>^:<path>`),
> re-run `--migrate` once with the current scanner, compare the regenerated `.md.j2` against
> `git show HEAD:<path>`.
>
> | | |
> |---|--:|
> | already byte-identical to the fresh conversion | **104** |
> | differs, but **only in the header** — braces identical | **55** |
> | differs in braces — and the reconvert would leave one **more** literal (`{Month}`) | 1 |
> | refused: `header line 3: flow mappings are not supported` | 1 |
>
> **So the recommended path is a regression on 55 files.** Restoring a pre-migration source
> discards every fix made to that template *after* its migration commit — and
> `d7e6222fd fix: require the header to be commented`, `dce921cda` and `51328ea21` are exactly
> that. Following this section's own instructions deletes the five-key header from 55 templates and
> leaves validator 5 failing on each declared one. Measured: 1,006 deletions against 34 insertions
> across 140 files.
>
> **What remains, and it is a queue not a bug.** 452 distinct residual tokens. Some are
> unmistakably prose (`{Restate the methodology goal in one sentence.}` ×11,
> `{named human; never 'team' / 'we' / 'us'}` ×11). Others read like parameters — `{artefact_id}`
> ×40, `{name}` ×37, `{description}` ×21, `{Title}` ×15 — and are left literal by §2's refusal rule
> because they bind more than one substitution site under different headings. That is the
> asymmetry §2 chose on purpose: **a false negative costs one line in a queue a human is already
> reading; a false positive ships a document with the wrong value in it.** Promoting any of them is
> per-file editorial judgement, which is §2's work below, not a mechanical pass.
>
> **The lesson, stated because it is the second time this week.** The 161/1,055 figure was measured
> correctly and attached to a premise nobody checked — the same failure as CR-010's "never
> delivered". This document even supplied the command to reproduce the number, which made the
> number trustworthy and the *sentence* no more true. **Ship the query with the claim, not only
> with the count.**

The original text follows, for the record.

**161 templates, 1,055 tokens.** The scanner fix landed; the corpus repair did not. These files
were converted by the *old* scanner, which recognised only ALL-CAPS `{BRACE}`, so a `{Product}`
was never seen — not flagged `unclear`, not declared, not refused. It renders literally into a
delivered document.

```bash
python3 - <<'PY'
import pathlib, re
BRACE = re.compile(r'(?<!\{)\{([A-Za-z][^{}\n]{0,60})\}(?!\})')
def strip_code(t):
    out, fenced = [], False
    for line in t.splitlines():
        if line.lstrip().startswith('```'): fenced = not fenced; out.append(''); continue
        out.append('' if fenced else re.sub(r'`[^`\n]*`', '', line))
    return "\n".join(out)
f=t=0
for p in pathlib.Path('skills/faion/knowledge').rglob('*.md.j2'):
    h=[x for x in BRACE.findall(strip_code(p.read_text(errors='replace'))) if not x.startswith(('%','#'))]
    if h: f+=1; t+=len(h)
print(f, t)
PY
```

A narrower regex — one demanding a bare identifier between the braces — reports **105 / 939**.
The gap is placeholders like `{one-line decision the artefact records}`, which are the *most*
obviously unfillable of the set. Use the figure above; the narrower one understates the repair.

### 2. CR-013 §2 — one variable bound to several substitution sites

**216 templates, 340 variables** appear at 2+ sites. Filling once fills all of them identically,
which is wrong wherever the sites are distinct slots (`## Competitor A: {{ name }}` three times).
The count includes legitimate repeats — one owner named twice on one page is correct — so this
figure is the **review queue**, not the damage. Triage is per-file and cannot be automated: that
is the point of §2's refusal rule, not a gap in it.

### The trap in both repairs

**`--migrate` must NOT be re-run on an already-converted template.** The regenerated `.md`
carries no `variables:` block — it moved into the schema — so a second pass re-proposes from
scratch and demotes backticked tokens to examples. Re-running it across the corpus rewrote **78
templates backwards** on 2026-08-16. `--check` being drift-free does not license re-migration:
it proves the generator is self-consistent against its *current* source and says nothing about
feeding a generated output back in as source.

Restore each affected template from its **pre-migration** source (`git show <commit>:<path>`)
and convert that, once, with the corrected scanner.

**And that instruction is itself a trap — see the correction in §1.** A pre-migration source
predates every fix applied to the template afterwards, so restoring it silently reverts them. On
this corpus it would have stripped the five-key header from 55 templates. If a template genuinely
needs re-conversion, restore the pre-migration source, re-apply the post-migration fixes to it
first, and only then convert.

## Blocked on the owner

Three calls I am not entitled to make. None of them blocks the two repairs above.

### A. Split `sensitive` into two flags

`x-faion-sensitive` currently conflates **"does not travel to the server"** with **"is not cached
locally"**. They are different surfaces with different threat models, and collapsing them costs
real coverage: `owner_full_name` is a field of 814 templates and can never be auto-filled while
one flag means both.

The contract lives in the monorepo — `faion-net/.aidocs/conventions/retrieval-content-contracts.md`
§5a, ratified — and governs the backend as well as this repo. **Not this repo's file to change.**

### B. The §2.3 ban on loops

**5,543 placeholders across 731 templates** sit in repeating table rows. They can never become
variables without `{% for %}`, so today they stay literal. The SSTI argument that justified the
ban was already retired by §0 (the renderer never treats a rendered result or a user-supplied
value as template source). The ban now rests on nothing that is still true — but lifting it is a
change to the rendering contract, not a cleanup.

### C. The 38 `_smoke-test*.md` filled examples

Undeclared on purpose: they are filled worked examples, not templates a user fills. Declaring
them would offer a "template" that is actually a sample. Their delivery is a content-taxonomy
question, not a migration one.

## Recommendations on A, B, C — 2026-09-10, for the owner to accept or reject

Written after every other open item in this repo was closed. Each is one decision with one
recommended answer; none is executed.

**A. Split `sensitive` into two flags — recommend YES, as two booleans, not one enum.**
`x-faion-no-transit` (the value never leaves the client; server emits the placeholder) and
`x-faion-no-cache` (the client does not persist it in the project store). Today's single flag is
the conjunction, so `owner_full_name` — a field of 814 templates — is refused by both surfaces
when only the first one has a threat model. Two flags default to "both true" for every entry
currently marked sensitive, so the change is additive and no template gets weaker. Cost: one
line in `retrieval-content-contracts.md` §5a, a `tpl-params.py` / `tpl-render.py` branch each,
and re-marking `owner_full_name` (and its 10 person-naming siblings from CR-013) as no-transit
only. The monorepo file is the owner's to change; this repo carries the two-flag reader either
way, because reading a flag that is not yet written is harmless.

**B. The §2.3 ban on loops — recommend LIFT it for `{% for %}` over a declared array variable,
and keep everything else banned.** The SSTI argument died with §0: the renderer never treats a
rendered result or a user-supplied value as template source, so a loop over data the schema
declares (`type: array`, `items: {…}`) adds no injection surface. What it buys is real:
5,543 placeholders in 731 templates sit in repeating table rows and are literal today. What
stays banned is what SSTI actually needs — expressions, filters, `include`, `import`, attribute
access on anything but the declared item shape. `SandboxedEnvironment` already refuses the
rest. The change is to the rendering contract, so it is the owner's call; the implementation is
one allow-list entry in `tpl-render.py` and a `validate-methodology-templates.py` check that a
`{% for %}` iterates a declared array and nothing else.

**C. The 38 `_smoke-test*.md` filled examples — recommend DECLARE them under a new column
value, not as templates.** They are what the row says they are — a filled artefact — and a user
who follows a `## Templates` row into one gets a sample, not a skeleton. Today they are
undeclared, so they ship (everything under `templates/` ships) and nobody is pointed at them.
Add `| File | Purpose | Kind |` with `Kind ∈ {template, example}` to the `## Templates` table,
declare the 38 as `example`, and have validator 5 skip the `variables:` and placeholder checks
for that kind. Deleting them loses 38 worked examples; leaving them undeclared keeps 38 files
nobody can find. This is a content-taxonomy decision and one column is its whole cost.

## Backend, not this repo

The render/search endpoint does not exist yet. Two properties it must have, both established by
the runtime flow in `template-jinja-migration.md` §1b:

- it must **dereference `$ref`** before answering a search, because the schema is the wire format
  and `$ref` coverage *is* the client's auto-fill rate;
- it must **reject sensitive values** rather than store them — the server emits the placeholder
  and the client substitutes locally.

## What this migration actually bought

Worth recording, because the templates were never the valuable part. Six defects surfaced that
no gate caught, and **four were mine**:

- `x-faion-sensitive` went invisible to the renderer — a real person's name would have shipped;
- 638 sensitive slots were marked `required`, so the client asked for exactly what the server
  must refuse;
- 177 templates carried placeholders the scanner could not see, reporting `variables=0` and
  exit 0;
- 358 variables collapsed three distinct slots into one name;
- `[[wikilink]]` was eaten and promoted to a mandatory parameter;
- an uncommented header rendered into the delivered document while passing every check.

The one worth keeping is the fifth-order lesson from the multi-site rule: it lived in
`build_plan()`, and the path that actually writes files never called it. **Self-test green,
writer unchanged.** Asking "is this rule correct?" is not the same question as "how many sites
will it fire on?", and only the second one finds this.
