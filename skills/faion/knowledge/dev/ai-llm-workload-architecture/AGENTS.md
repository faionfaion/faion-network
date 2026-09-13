# AI LLM Workload Architecture

## Summary

**One-sentence:** Produces an AI/LLM workload architecture spec — eval set, scoring function, pass/fail thresholds, regression gate, owner — that makes LLM-backed features comparable across runs instead of vibes-only.

**One-paragraph:** Produces an AI/LLM workload architecture spec — eval set, scoring function, pass/fail thresholds, regression gate, owner — that makes LLM-backed features comparable across runs instead of vibes-only. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software developers shipping LLM-backed features (RAG, agents, chat) who must wire an eval-driven workload architecture before the next regression silently degrades quality.

## Applies If (ALL must hold)

- The feature calls an LLM on a production path — RAG answerer, agent, summariser or chat — and a change to its prompt text, system prompt, model id, sampling parameters, retrieval configuration or tool schemas can reach users.
- An eval set of at least a few dozen real cases exists or can be assembled from production samples, and it can be stored as a versioned file or hashed dataset export.
- CI can run a job on pull requests and mark it a required check, so the eval suite can block a merge.
- The vendor exposes dated or versioned model snapshots (or a stable mapping from alias to snapshot), so the production model id can be pinned.
- A p95 latency target and a per-request token or cost ceiling exist or can be set from the SLO.

## Skip If (ANY kills it)

- The change touches no LLM call path — no prompt, model id, sampling, retrieval or tool-schema edit — so ordinary code review and tests apply.
- The feature is an offline batch job with no user-facing latency and no regression exposure; a one-off eval report suffices.
- A platform team already runs a shared eval gate that this feature's prompts, model config and tool schemas are registered with; extend that spec rather than writing a second one.
- The output is scored by a downstream deterministic system (a compiler, a schema validator, a test suite) and that system is already the merge gate.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval cases | JSONL or dataset export with input, expected output and case id | product samples / support transcripts |
| Prompt files and few-shot blocks | files under a version-controlled directory | feature repo |
| Scoring code or judge prompt | function, regex, JSON schema, or judge prompt text | feature repo |
| CI system with required checks | pipeline config (GitHub Actions, GitLab CI, Buildkite) | platform / repo settings |
| Vendor model-versioning page | list of dated snapshot ids and deprecation dates | model vendor documentation |
| SLO figures | p95 latency ms; per-request token or cost ceiling | product / finance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: eval set pinned, deterministic scoring, numeric thresholds vs baseline, merge-blocking gate, model id pinned, latency and cost budgets, injection cases, degradation path | ~1750 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the spec: eval_set with git ref or hash and contamination check, scoring with judge pinned at temperature 0 and prompt hash, baseline_run plus numeric per-metric thresholds, merge-blocking gate on watched paths, dated production_model_id, p95 and per-request budgets measured in the run, one injection case per untrusted channel, bounded retry and evaluated fallback; valid and invalid examples | ~4300 |
| `content/03-failure-modes.xml` | essential | 6 subject-specific antipatterns with detector + repair | ~1000 |
| `content/04-procedure.xml` | recommended | 9 steps: pin eval set, deterministic scoring and noise floor, baseline and thresholds, merge-blocking gate, pin model id, budgets in the run, injection cases per channel, degradation path with eval cases, validate and file | ~1850 |
| `content/05-examples.xml` | recommended | Complete support-ticket summariser spec with notes on every non-obvious value, plus the same feature before the spec breaking six rules and what the validator and reviewer say | ~2050 |
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
| `scripts/validate-ai-llm-workload-architecture.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
