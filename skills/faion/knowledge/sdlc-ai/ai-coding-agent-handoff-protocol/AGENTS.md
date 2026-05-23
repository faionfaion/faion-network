# AI Coding Agent Handoff Protocol

## Summary

**One-sentence:** Spec → AI-agent task → human review discipline that stops vibe-coded breakage by enforcing a written hand-off contract, a bounded change scope, and a mandatory diff-review gate before merge.

**One-paragraph:** Spec → AI-agent task → human review discipline that stops vibe-coded breakage by enforcing a written hand-off contract, a bounded change scope, and a mandatory diff-review gate before merge. The methodology pins the artefact: a TASK.md envelope listing brief, allowed file paths, forbidden changes, acceptance criteria, and the review checklist the human applies post-run.

**Ефективно для:**

- Solo founders delegating coding tasks to AI agents under time pressure.
- Pipelines where agents produce diffs that humans must approve.
- Reviewers who need a structured artefact instead of free-form prompts.
- Audit surface: every agent run has a hand-off + review record.

## Applies If (ALL must hold)

- An AI coding agent is delegated work in this repo.
- Changes touch ≥1 file that humans care about (production code).
- There is a review gate before merge.

## Skip If (ANY kills it)

- Throwaway scratchpad / one-off scripts.
- Agent runs read-only / analytical tasks (no diff produced).
- No human reviewer available at all — find one before delegating.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task brief | markdown | User |
| Repo state | git | Local clone |
| Review checklist | markdown | Convention |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdlc-ai/ai-convention-anchoring` | Provides the convention layer the agent must honour. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ai-coding-agent-handoff-protocol` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-ai-coding-agent-handoff-protocol` | haiku | Schema check + threshold checks; deterministic. |
| `review-ai-coding-agent-handoff-protocol` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-coding-agent-handoff-protocol.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ai-coding-agent-handoff-protocol.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-coding-agent-handoff-protocol.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[agents-md-per-module-bootstrap]]
- [[ai-convention-anchoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
