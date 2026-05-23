# Slash-Command Surface for PR Review Bots

## Summary

**One-sentence:** Expose review-bot capabilities (`/describe`, `/review`, `/improve`, `/ask`) as PR-comment slash commands so humans steer the bot in-band; auto-trigger describe+review, leave improve opt-in.

**One-paragraph:** Review bots either run on every PR with no human steering (noisy) or live behind a separate dashboard nobody opens (dead). Qodo Merge, CodeRabbit, and Sourcery converged on a third path: the bot listens for PR-comment slash commands, lets humans request `/review`, `/describe`, `/improve`, `/ask` on demand, and runs `/describe` + `/review` automatically on open / push while keeping `/improve` (the noisy suggestion engine) explicitly opt-in. This methodology produces the bot's GitHub Action config that wires `auto_describe`, `auto_review`, `auto_improve`, and the slash-command dispatcher.

**Ефективно для:**

- Multi-author repo, де люди хочуть "second pair of eyes" перед human review.
- High-volume repo (&gt;20 PR/day), де люди тонуть у написанні description.
- Open-source repo, де контриб'ютори не мають інституційного контексту.
- Repo, що вже використовує slash-command-aware bot (Qodo Merge / CodeRabbit / Sourcery).

## Applies If (ALL must hold)

- Repo runs a slash-command-capable PR bot (Qodo Merge / CodeRabbit / Sourcery) OR can install one.
- Team agrees `auto_describe` and `auto_review` should run on every PR open / push.
- Team agrees `auto_improve` should be opt-in (per PR or per repo).
- A `<!-- AUTO-DESCRIBE-START -->` / `<!-- AUTO-DESCRIBE-END -->` block convention is acceptable in PR bodies.

## Skip If (ANY kills it)

- Tiny PRs (&lt;20 LOC average) — `/review` adds more noise than signal.
- "No third-party app" policy without a self-hosted PR-Agent install.
- Single-author repo where author already writes descriptions — auto-describe overwrites them.
- Compliance setup that requires every bot comment to be pre-approved.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bot install | Qodo Merge GitHub app OR self-hosted PR-Agent | platform |
| Workflow file | .github/workflows/qodo-merge.yml | platform |
| LLM key | OPENAI_KEY / ANTHROPIC_KEY in repo secrets | security |
| PR description template | with AUTO-DESCRIBE block | docs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mr-graph-vs-diff-reviewer]] | Reviewer methodology this bot drives. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bot_pick` | sonnet | Qodo Merge vs CodeRabbit vs Sourcery — needs judgement. |
| `workflow_draft` | haiku | Boilerplate YAML. |
| `pr_template_draft` | haiku | Markdown skeleton with AUTO-DESCRIBE markers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/qodo-merge.yml` | Qodo Merge workflow with auto_describe + auto_review on, auto_improve off. |
| `templates/pr-description-block.md` | PR body skeleton with AUTO-DESCRIBE-START/END markers. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-slash-command-surface.py` | Validate produced bot-config artefact against schema. | pre-merge of workflow file |

## Related

- [[mr-graph-vs-diff-reviewer]]
- [[mr-codemod-refactor-agent]]
- [[mr-error-tracker-draft-pr]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (repo size, bot install presence, team review style) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to enable a given auto-trigger — the tree terminates either on the active rule or on `skip-this-methodology`.
