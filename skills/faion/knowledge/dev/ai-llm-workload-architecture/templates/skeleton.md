<!--
purpose: Canonical skeleton for the `ai-llm-workload-architecture` spec — one section per rule in content/01-core-rules.xml.
consumes: Eval cases, prompt files, scoring code, CI config, runtime model config, SLO figures.
produces: A committed spec at .product/ai-llm-workload-architecture/<feature>.md plus its JSON form validated by scripts/validate-ai-llm-workload-architecture.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-ai-llm-workload-architecture.py.
token-budget-impact: ~1200 tokens to fill end-to-end.
-->
---
version: 0.1.0
feature_name: <feature_name>
owner: <owner_handle>
production_model_id: <production_model_id>
baseline_run_url: <baseline_run_url>
---

# Feature

- feature_name: <feature_name>
- owner: <owner_handle>

# Eval set

- path: <evals/feature/cases.jsonl or dataset export>
- ref: <git sha or sha256:...>
- case_count: <n>
- contamination_check_passed: true (job: <ci job that greps prompts for eval inputs>)

# Scoring

- kind: exact-match | regex | json-schema | unit-assertion | llm-judge
- judge.model_id: <dated id, e.g. claude-sonnet-4-5-20250929>
- judge.temperature: 0
- judge.prompt_hash: sha256:<hash of the judge prompt>
- judge.noise_floor: <largest per-metric delta between two runs at the same commit>

# Metrics and thresholds

- baseline_run: <baseline_run_url> at commit <sha>

| Metric | Baseline | Tolerance | Threshold | Direction |
|---|---|---|---|---|
| answer_accuracy | 0.89 | -0.02 | 0.87 | higher-is-better |
| hallucination_rate | 0.03 | +0.01 | 0.04 | lower-is-better |
| injection_resistance | 1.0 | 0.0 | 1.0 | higher-is-better |

# Regression gate

- ci_job: <name of the required check>
- blocks_merge: true
- watched_paths: <prompts dir>, <model config>, <retrieval config>, <tool schemas>
- prompts_in_version_control: true
- prompt_hash_logged_at_startup: true | false

# Production model

- production_model_id: <production_model_id>

# Budgets

- p95_latency_ms: <n>
- per_request.tokens: <n> and/or per_request.cost_usd: <n>
- measured_in_eval_run: true

# Untrusted input channels

| Channel | Kind | Injection case ids |
|---|---|---|
| <retrieval source> | retrieval-source | <inj-...> |
| <tool name> | tool-output | <inj-...> |
| user turn | user-turn | <inj-...> |

# Degradation path

- retry: max_attempts <n, at most 10>; backoff exponential-with-jitter; base_delay_ms <n>; triggers timeout, 429, 5xx
- fallback: secondary-pinned-model <dated id> | cached-answer | explicit-refusal
- fallback eval_case_ids: <deg-...>
- user_message: <what the user sees>

# Evidence

- <baseline_run_url>
- <second run at the same commit for the noise floor>
- <PR that made the eval job a required check>
