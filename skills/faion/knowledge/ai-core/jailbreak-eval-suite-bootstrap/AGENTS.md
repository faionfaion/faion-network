# Jailbreak Eval Suite Bootstrap

## Summary

**One-sentence:** Produces a starter adversarial eval suite (≥50 prompts spanning 10 jailbreak categories) wired into CI with per-category pass-rate thresholds and a JSONL judge contract.

**One-paragraph:** Without an automated jailbreak eval suite any model-change, prompt-edit, or tool-add can silently re-enable previously-fixed attacks. This methodology bootstraps a working suite in one sitting: pick 10 attack categories (DAN, role-play, cipher, base64, suffix, persona-flip, hypothetical, code-context, multi-turn, refusal-bypass), seed each with ≥5 cases from open benchmarks (JailbreakBench, JBDistill, JailBreakV-28K), define a binary judge contract per case (LLM-as-judge + regex backstop), and wire the runner into CI with a per-category pass-rate threshold (≥95% default). Calibrate the judge once against a hand-labelled holdout before trusting it as the merge gate.

**Ефективно для:** customer-support agents, code-assistants with destructive tools, content-moderation pipelines, evaluator harnesses guarding model upgrades.

## Applies If (ALL must hold)

- The agent or model exposes safety-critical behaviour (refusing certain categories of request).
- A target list of disallowed behaviours can be enumerated (≥3 categories).
- A scoring channel exists — either programmatic (regex/parser) or LLM-as-judge with a calibration set.
- CI capacity exists to run ≥50 prompts per merge (typical run: 1-3 min on parallel workers).

## Skip If (ANY kills it)

- No safety contract — model has no refusal categories, so jailbreak has no meaning.
- Pre-MVP prompts churning daily — eval thresholds shift faster than the suite.
- Closed evaluation environment without internet/CI access.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Refusal-category list | Markdown / YAML | safety policy doc |
| Sample disallowed prompts | JSONL | red-team review, JailbreakBench, etc. |
| Judge model endpoint | API URL + creds | secrets manager |
| CI runner with parallel workers | shell + Python ≥3.11 | repo CI config |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[judge-calibration-protocol]]` | Calibrates the LLM-as-judge before it gates merges. |
| `[[ai-failure-mode-taxonomy]]` | Common vocabulary for category names. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: category coverage ≥10, ≥5 cases each, judge contract, calibration, threshold per category, regression alert | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for suite-config.json + JSONL case format + runner output report | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: judge-not-calibrated, cherry-picked categories, single-threshold-everywhere, no-novelty-rotation, no-CI-gate | ~600 |
| `content/04-procedure.xml` | medium | 6-step procedure: enumerate categories → seed cases → write judge contract → calibrate → wire runner → set CI gate | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "are there safety refusal contracts to defend?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Seed cases from public benchmarks | sonnet | Mechanical extraction, dedup, translation. |
| Author per-category judge prompt | opus | Adversarial creativity + edge cases. |
| Run calibration & compute κ | haiku | Numerical, deterministic. |
| Triage failed eval case | opus | Multi-step reasoning over trace. |

## Templates

| File | Purpose |
|---|---|
| `templates/eval-cases.jsonl` | 10-category seed (5 cases each = 50 cases). |
| `templates/judge-prompt.md` | Binary refusal-judge prompt template. |
| `templates/suite-config.yaml` | Per-category thresholds, runner args, output paths. |
| `templates/runner.py` | Reference parallel runner that loads cases, calls model + judge, emits report.json. |
| `templates/_smoke-test.jsonl` | 5-case minimum-viable suite for the smoke loop. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-jailbreak-eval-suite-bootstrap.py` | Validates suite-config.yaml + eval-cases.jsonl conform to the contract (category coverage, judge wiring, thresholds). | Pre-commit on suite-config / cases; CI before runner. |

## Related

- parent skill: `geek/ai/`
- `[[judge-calibration-protocol]]` — required upstream
- `[[indirect-prompt-injection-defense]]` — IPI defense pulls cases from the same suite

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether to bootstrap a suite: skip when the agent has no refusal contract; switch to minimal smoke-only suite when CI budget is tight; full bootstrap when ≥10 categories and a calibrated judge can be supplied.
