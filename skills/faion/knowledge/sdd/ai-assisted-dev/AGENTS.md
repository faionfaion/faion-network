# AI-Assisted Development

## Summary

**One-sentence:** Produces an AI-assisted dev workflow record — tool-to-task assignment (Claude Code / Cursor / Copilot), structured-prompt template, review checkpoint matrix, and security-critical block-list — that pins the defect-rate-reducing discipline that informal AI adoption skips.

**One-paragraph:** Produces an AI-assisted dev workflow record — tool-to-task assignment (Claude Code / Cursor / Copilot), structured-prompt template, review checkpoint matrix, and security-critical block-list — that pins the defect-rate-reducing discipline that informal AI adoption skips. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software developers wiring Claude Code, Cursor, and Copilot into their daily flow who need a written tool-to-task map and review discipline before AI-generated code starts compounding latent defects.

## Applies If (ALL must hold)

- The team uses at least one AI coding tool (Claude Code, Cursor, Copilot or another) on a repository it owns and can add files to.
- PRs carry labels or a field, and auto-merge can be disabled, so AI-assisted diffs can be marked and reviewed under a checkpoint.
- The repo has identifiable auth, authorization, crypto, payments, PII, secrets-loading, production IaC and migration paths to block-list.
- Defect escapes, reverts and two-week churn can be counted per PR from the code host or a dashboard, split by the label.
- One engineer owns the map and the cadence comparison as `role:handle`.

## Skip If (ANY kills it)

- The team uses no AI coding tool; there is nothing to map.
- The repository is read-only for the team (a vendored or upstream fork) so no context file, ignore file or label can be added.
- PR-level metrics cannot be produced at all (no code host history, no CI), so the cadence comparison cannot run; instrument first.
- A parent organisation policy already fixes the map, block-list and review checkpoints for this repo; record a pointer to it, not a second record.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tools in use | list of Claude Code / Cursor / Copilot / other with the developers using each | team survey / tool licences |
| Repo layout for the block-list | paths of auth, authorization, crypto, payments, PII, secrets loading, production IaC, migrations | repo tree / CODEOWNERS |
| Vendor data-usage terms | URL and date read for each tool | vendor documentation |
| Context and ignore files | `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`, `.cursorignore` or equivalent | repo root |
| Prompt template | `templates/prompt-code.txt` committed into the repo | this methodology |
| PR quality numbers by label | pr_count, defect escape rate, revert rate, two-week churn for ai-assisted and other PRs over the period | code host API / PR quality dashboard |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: tool-to-task map, security-critical block-list, four-block prompt, repo context file, no secrets in prompts, verify introduced dependencies, AI tests must fail when broken, AI diff reviewed like human code, defect rate tracked AI vs human | ~2750 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the workflow record: seven-class tool-to-task map with checkpoints, eight-area block-list with paths and policy, context file per tool, secrets exclusion file, retention checks, four-block prompt template, ai-assisted label with auto-merge off, decision, evidence, cadence outcome comparing defect / revert / churn with tighten-when-worse; valid and invalid records; 8 forbidden patterns | ~5550 |
| `content/03-failure-modes.xml` | essential | 7 modes: AI everywhere no map, confident insecure default, prose prompt, secrets in the prompt, hallucinated package, tests that test nothing, churn nobody measures | ~950 |
| `content/04-procedure.xml` | recommended | 9 steps: write the map, write the block-list, commit context files, exclude secrets and check retention, adopt the four-block prompt, verify introduced dependencies, break the function for generated tests, label and review every AI diff, compare defects at cadence | ~1700 |
| `content/05-examples.xml` | recommended | Complete billing-platform record (map across three tools, eight-area block-list, three context files, .cursorignore, retention checked, August churn comparison and tightened refactor checkpoint) with a note per value, plus the 'Copilot for everything' record and what the validator prints | ~2400 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Parse inputs + check preconditions | haiku | Mechanical schema parse. |
| Author the artefact body | sonnet | Bounded synthesis from typed inputs. |
| Review for compliance + cross-cutting impact | opus | Cross-input judgement when stakes are high. |
| Outcome-review synthesis at cadence | opus | Did the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton of the artefact with all required sections. |
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |
| `templates/gen-tests.sh` | Call Claude Code in `--print` mode to generate pytest test stubs. |
| `templates/prompt-code.txt` | Structured code-generation prompt template (context/task/requirements/output). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-dev.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
