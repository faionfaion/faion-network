# templates/

The corpus-wide **variable dictionary**: every canonical template parameter defined once, with its type, its meaning and the question an author is asked. A per-template `<name>.vars.schema.json` `$ref`s into this file and adds only what is genuinely local, so a variable appearing in two templates means the same thing in both.

Design: [`.aidocs/conventions/template-jinja-migration.md`](../../../.aidocs/conventions/template-jinja-migration.md) §3.
Measurement behind the entry list: [`.aidocs/improvements/variable-dictionary-findings.md`](../../../.aidocs/improvements/variable-dictionary-findings.md).

## Files

| File | What |
|------|------|
| `vars-dictionary.schema.json` | Draft-07, `$defs` map, **66 entries**. Every entry carries `type` + `title` + a `description` written as the question put to the author; 9 are `x-faion-sensitive` (each with `x-faion-placeholder`), 9 are `x-faion-compose`, 8 are enums |
| `meta.json` | Tier gate for this directory — `free`, and it has to be: a gated dictionary means a free-tier template cannot render at all. Same argument F031 made for the lexicon |

## The rule the whole file exists to enforce

> A dictionary entry is a name plus a meaning. **Two uses share a name only when a value carried from one artefact to the other is still correct.**

That last clause is the operational test, because the project store *does* carry values between artefacts. `owner` on a risk register and `owner` on a design doc would legitimately be different people, so they are two entries.

**Convergence means fewer ambiguous names, which usually means MORE names.** The corpus's most common proposed name is `name` at 676 occurrences, and it is the worst variable in the corpus because it means 676 different things. There is no `name` entry and there must never be one — it resolves to `owner_full_name`, `reviewer_name`, `engagement_name`, `persona_name`, `feature_name` or a per-row slot depending on the line it sits on. Eight separate `*_name` entries is the rule working, not a failure to consolidate.

## Gotchas

- **This directory is the only place a `.json` reaches a user's disk.** `packablePath` in `faion-cli/tools/vfs-pack/pack.go` admits **everything under a `templates/` path segment**, un-extension-gated (F036/AD-024); every other `.json` in the corpus is excluded, and `meta.json` is excluded everywhere as packer input. Proven by test: `faion/templates/vars-dictionary.schema.json` ships, `faion/schemas/vars-dictionary.schema.json` does **not**. Moving this file to a tidier-looking `schemas/` dir makes it invisible on every user's machine — a fresh instance of CR-010.
- **A new root under `skills/faion/` needs a case in `regen-tier-manifest.py`, not only a `meta.json`.** The generator walks seven named roots; a directory absent from that list is never read and inherits a tier silently.
- **`sensitive` currently blocks the project store, and that is the open question here.** Eight of the nine sensitive entries are people, including `owner_full_name` — the field 814 templates carry. `tplcore.py` refuses to store a sensitive value, so the corpus's most common field is the one a project can never remember. §8 of the findings file argues the flag is doing two jobs (must-not-travel, must-not-be-cached) where personal data only needs the first. Not changed here: §5/§5a are ratified and splitting the flag is a contract change.
- Entry count and the `$comment` on each entry are the audit trail — a `$comment` says why a name was split or merged, and several cite the specific template where both names appear **in the same file**. That in-file evidence is the strongest form the test takes; prefer it when adding an entry.
