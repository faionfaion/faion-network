# PR Mentoring Session Protocol

## Summary

**One-sentence:** Produces a PR-mentoring session record — junior author, senior reviewer, learning goal, observed gap, follow-up action — so PR reviews with juniors actually become a measurable mentoring loop instead of folklore.

**One-paragraph:** Produces a PR-mentoring session record — junior author, senior reviewer, learning goal, observed gap, follow-up action — so PR reviews with juniors actually become a measurable mentoring loop instead of folklore. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** engineering managers and senior reviewers running a recurring mentoring loop with a junior author who need a written protocol that captures the learning goal + observed gap + follow-up so growth becomes reviewable.

## Applies If (ALL must hold)

- A junior engineer has an open PR and a senior reviewer has (or will post) at least one comment on a specific diff line of it.
- The pair runs a recurring mentoring loop, so a prior session record can be linked and its follow-up PR judged.
- The code host exposes line-level anchors (`#discussion_r`, `#L`, `#note_`) and commit authorship, so the gap and the fix can be attributed.
- The record can be stored where the junior can read it (repo `.product/`, shared doc), and the junior can confirm the text with a comment, reaction or co-authorship.
- One senior owns the record as `role:handle` and an engineering manager exists to escalate to on the third not-demonstrated.

## Skip If (ANY kills it)

- There is no PR from the junior yet, or the review has no line-level comment; run an ordinary review or wait for the next PR.
- The review is between peers of equal seniority with no learning goal; use the normal code-review methodology.
- The organisation keeps mentoring notes private to managers and will not let the junior read or confirm them; the protocol cannot run as a secret dossier.
- The PR is a generated or mechanical change (dependency bump, formatter run) with nothing to learn from.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Junior's open PR | PR URL on GitHub, GitLab or Bitbucket | code host |
| Prior session record | previous record for the same junior with its named follow-up PR, or none | `.product/pr-mentoring-session-protocol/` in the repo |
| Review comment thread | comments labelled per Conventional Comments with line anchors | the PR review |
| Fix commit | commit URL on the junior's branch with the junior as author | the PR |
| Junior's confirmation | comment, reaction or co-authorship URL confirming the gap and decision text | the PR or record |
| Follow-up PR or ticket | URL once it exists, within 14 days or the next two PRs | code host / tracker |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: one observable goal, gap cites diff line, labelled comments + praise, junior restates and writes fix, one PR per session, follow-up is a named next PR, progression linked to prior session, record shared with junior | ~2100 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the session record: one PR with junior and senior, learning_goal as a behaviour, observed_gap did/should, restated_gap, comment_counts per label with praise, deferred_findings, junior-authored fix commit, progression with prior_action_status and streak, follow-up PR within 14 days with escalation at streak 3, junior confirmation, line-anchored evidence; valid and invalid records; 8 forbidden patterns | ~4350 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | ~1200 |
| `content/04-procedure.xml` | recommended | 8 steps: open from the prior record, one observable goal, anchor the gap to a line, labelled comments with praise, junior restates and fixes, park deferred findings, name the follow-up and share with the junior, close on the follow-up PR | ~1500 |
| `content/05-examples.xml` | recommended | Complete session record for a junior's second attempt at a re-runnable migration (gap at line 18, six labelled comments, junior's fix commit, streak 2, follow-up PR landed) with a note per value, plus the same session as a trait review and what the validator prints | ~1850 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pr-mentoring-session-protocol.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
