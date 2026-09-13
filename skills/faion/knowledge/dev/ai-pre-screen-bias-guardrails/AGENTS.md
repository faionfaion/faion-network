# AI Pre-Screen Bias Guardrails

## Summary

**One-sentence:** Produces a guardrail spec for AI-assisted hiring pre-screens and take-home reviews: protected-class blinding, scoring rubric, calibration sample, and human-of-record sign-off — so the bias surface from LLM-graded candidates stays auditable.

**One-paragraph:** Produces a guardrail spec for AI-assisted hiring pre-screens and take-home reviews: protected-class blinding, scoring rubric, calibration sample, and human-of-record sign-off — so the bias surface from LLM-graded candidates stays auditable. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** engineering managers and hiring teams using LLMs to pre-screen CVs or grade take-homes who need a written guardrail their legal + DEI partners can audit before any candidate sees the system.

## Applies If (ALL must hold)

- A model scores, ranks, summarises or filters candidate submissions (CVs, cover letters, take-homes) before a human sees them.
- The job requirements for the role are written down, so every rubric criterion can map to one.
- A real applicant pool from a previous cycle is available for calibration, with consent as the candidates' jurisdictions require.
- Self-identification data is collected in an HR system held apart from the scoring pipeline, so per-stage selection rates can be computed.
- Legal can name which automated-employment-decision law applies to the candidates' jurisdictions, and a hiring manager is willing to be the human of record.

## Skip If (ANY kills it)

- No automated step touches candidate material before a human reads it; ordinary structured-interview practice applies.
- The model is used only after a human decision, for example to draft feedback to candidates already advanced, and never influences advance or reject.
- A vendor tool already carries a current, independent bias audit, a candidate notice and a per-stage adverse-impact report for this role, and the employer's own pipeline adds no scoring; attach the vendor's artefacts instead of writing a second spec.
- The role is internal-only mobility with no external candidates and no jurisdiction where an AEDT law applies, and counsel has confirmed in writing that none applies.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Job requirements for the role | written list, one line per requirement | hiring manager / job description |
| Redaction fixture set | sample CVs and take-homes containing each of the ten attribute classes | recruiting / DEI |
| Previous-cycle applicant pool | submissions with consent for calibration use | applicant tracking system |
| Self-identification data | HRIS table keyed by candidate, held apart from scoring | HR information system |
| Legal determination | which AEDT law applies per candidate jurisdiction, or a signed none-applies memo | employment counsel |
| Vendor or employer bias audit | independent audit summary with date and auditor | vendor / audit firm |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: protected attributes stripped, rubric versioned first, no proxy criteria, real-pool calibration, four-fifths monitoring, human of record, notice and bias audit, per-candidate audit log | ~2100 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the spec: redaction with all ten stripped attribute classes and unit test, hashed rubric with low / mid / high anchors, proxy review with zero terms, real-pool calibration with two reviewers and pre-set threshold, per-stage four-fifths table forcing on_hold under 0.8, human of record with no auto-reject, applicable law with notice and bias audit, seven-field audit log at 12+ months, pinned tuple; valid and invalid examples | ~5700 |
| `content/03-failure-modes.xml` | essential | 6 subject-specific antipatterns with detector + repair | ~1150 |
| `content/04-procedure.xml` | recommended | 9 steps: redaction, rubric and hash, proxy review, real-pool calibration, human of record, applicable law with notice and audit, per-stage adverse impact, audit log and pinned tuple, validate and file | ~2000 |
| `content/05-examples.xml` | recommended | Complete backend take-home grader spec with notes on every non-obvious value, plus the same pipeline as first built breaking seven rules and what the validator and legal reviewer say | ~2850 |
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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-pre-screen-bias-guardrails.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
