---
name: llm-as-judge-harness
description: Build a 100-example golden set, judge outputs with claude-opus-4-7 on 3 axes, and block CI when mean score < 4.0 or any axis < 3.5.
tier: geek
group: evaluation
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a reproducible eval harness: a `golden_set.jsonl` file with 100 scored examples, a Python judge script that calls `claude-opus-4-7` to score each output on three axes (correctness, groundedness, coherence) from 1 to 5, and a GitHub Actions workflow that runs on every pull request and fails when the mean score drops below 4.0 or any axis mean drops below 3.5.

## Prerequisites

- Python 3.11+ with `anthropic>=1.30.0` and `pydantic>=2.7` installed (`pip install anthropic pydantic`).
- An Anthropic API key in the environment as `ANTHROPIC_API_KEY`.
- A GitHub repository with Actions enabled.
- An existing pipeline or agent whose outputs you want to evaluate (returns plain text or JSON strings).
- Basic familiarity with JSONL format and GitHub Actions YAML.

## Steps

1. Create the golden-set schema. Add `eval/golden_set.jsonl` to your repo. Each line is a JSON object:

   ```json
   {"id": "qs-001", "input": "Summarise the EU AI Act Article 6 in two sentences.", "expected_themes": ["high-risk systems", "classification"], "context": "Article 6 defines high-risk AI systems..."}
   ```

   Required keys: `id` (unique string), `input` (the prompt sent to your pipeline), `expected_themes` (list of strings the answer must cover), `context` (optional ground-truth passage for groundedness scoring).

2. Populate `golden_set.jsonl` with 100 examples. Spread them across your real query distribution — aim for at least 5 distinct task types (summarisation, extraction, Q&A, generation, classification). Keep each `context` field under 800 tokens. Commit the file to the repo.

3. Create `eval/run_pipeline.py`. This module wraps your pipeline and returns a string response for each input:

   ```python
   # eval/run_pipeline.py
   import anthropic

   _client = anthropic.Anthropic()

   def run(input_text: str) -> str:
       """Call your pipeline. Replace the body with your real impl."""
       msg = _client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=512,
           messages=[{"role": "user", "content": input_text}],
       )
       return msg.content[0].text
   ```

4. Create `eval/judge.py` — the scoring harness. It reads `golden_set.jsonl`, calls your pipeline, then calls `claude-opus-4-7` to judge each output:

   ```python
   # eval/judge.py
   from __future__ import annotations

   import json
   import os
   import sys
   from pathlib import Path

   import anthropic
   from pydantic import BaseModel, Field

   JUDGE_MODEL = "claude-opus-4-7"
   GOLDEN_SET = Path(__file__).parent / "golden_set.jsonl"
   PASS_MEAN = 4.0
   PASS_AXIS = 3.5


   class AxisScores(BaseModel):
       correctness: float = Field(..., ge=1, le=5)
       groundedness: float = Field(..., ge=1, le=5)
       coherence: float = Field(..., ge=1, le=5)
       reasoning: str


   JUDGE_PROMPT = """\
   You are an impartial evaluator. Score the assistant response on three axes from 1 (very poor) to 5 (excellent).

   <task_input>{input}</task_input>
   <expected_themes>{themes}</expected_themes>
   <ground_truth_context>{context}</ground_truth_context>
   <assistant_response>{response}</assistant_response>

   Axes:
   - correctness: Does the response address all expected_themes accurately?
   - groundedness: Is every factual claim supported by or consistent with the ground_truth_context?
   - coherence: Is the response well-structured, clear, and free of contradiction?

   Reply with ONLY valid JSON matching this schema:
   {{"correctness": <1-5>, "groundedness": <1-5>, "coherence": <1-5>, "reasoning": "<one sentence>"}}
   """

   def judge_one(client: anthropic.Anthropic, example: dict, response: str) -> AxisScores:
       prompt = JUDGE_PROMPT.format(
           input=example["input"],
           themes=", ".join(example.get("expected_themes", [])),
           context=example.get("context", ""),
           response=response,
       )
       msg = client.messages.create(
           model=JUDGE_MODEL,
           max_tokens=256,
           messages=[{"role": "user", "content": prompt}],
       )
       raw = msg.content[0].text.strip()
       return AxisScores.model_validate_json(raw)


   def main() -> None:
       from eval.run_pipeline import run as pipeline_run

       client = anthropic.Anthropic()
       examples = [json.loads(l) for l in GOLDEN_SET.read_text().splitlines() if l.strip()]

       results: list[dict] = []
       for ex in examples:
           response = pipeline_run(ex["input"])
           scores = judge_one(client, ex, response)
           results.append({"id": ex["id"], **scores.model_dump()})
           sys.stderr.write(f"  {ex['id']} C={scores.correctness} G={scores.groundedness} Co={scores.coherence}\n")

       # Aggregate
       axes = ["correctness", "groundedness", "coherence"]
       means = {ax: sum(r[ax] for r in results) / len(results) for ax in axes}
       overall = sum(means.values()) / len(axes)

       report = {"overall_mean": round(overall, 3), "axis_means": {k: round(v, 3) for k, v in means.items()}, "n": len(results)}
       print(json.dumps(report, indent=2))

       # CI gate
       failed = overall < PASS_MEAN or any(v < PASS_AXIS for v in means.values())
       if failed:
           sys.stderr.write(
               f"FAIL: overall={overall:.2f} (need >={PASS_MEAN}), axes={means}\n"
           )
           sys.exit(1)
       sys.stderr.write(f"PASS: overall={overall:.2f}, axes={means}\n")


   if __name__ == "__main__":
       main()
   ```

5. Test locally against a 5-example subset before committing the full golden set:

   ```bash
   head -5 eval/golden_set.jsonl > /tmp/subset.jsonl
   cp /tmp/subset.jsonl eval/golden_set.jsonl
   python -m eval.judge
   cp eval/golden_set.jsonl.bak eval/golden_set.jsonl   # restore
   ```

6. Create `.github/workflows/eval.yml` to run the harness on every pull request:

   ```yaml
   name: eval-regression

   on:
     pull_request:
       branches: [main]
     workflow_dispatch:

   jobs:
     judge:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4

         - uses: actions/setup-python@v5
           with:
             python-version: "3.11"

         - name: Install deps
           run: pip install anthropic>=1.30.0 pydantic>=2.7

         - name: Run eval harness
           env:
             ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
           run: python -m eval.judge

         - name: Upload score report
           if: always()
           uses: actions/upload-artifact@v4
           with:
             name: eval-scores-${{ github.sha }}
             path: eval-report.json
             if-no-files-found: ignore
   ```

   Add `ANTHROPIC_API_KEY` to your repo's Actions secrets (Settings → Secrets and variables → Actions → New repository secret).

7. Optionally write `eval-report.json` from `judge.py` for the artifact upload. Replace the `print(json.dumps(...))` line in `main()` with:

   ```python
   Path("eval-report.json").write_text(json.dumps(report, indent=2))
   print(json.dumps(report, indent=2))
   ```

8. Commit and push to a feature branch, then open a pull request. Watch the `eval-regression` check run in the PR checks list.

## Verify

Run the harness locally against the full 100-example set:

```bash
ANTHROPIC_API_KEY=<your-key> python -m eval.judge
```

Expected output (stdout):

```json
{
  "overall_mean": 4.23,
  "axis_means": {
    "correctness": 4.31,
    "groundedness": 4.18,
    "coherence": 4.21
  },
  "n": 100
}
```

Exit code 0 means pass. If any axis mean is below 3.5 or overall mean below 4.0, exit code is 1 and stderr prints `FAIL: ...`.

In GitHub Actions, the `judge` job shows green when the harness passes and red (blocking merge) when it fails.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `pydantic.ValidationError` on judge output | `claude-opus-4-7` returned prose instead of JSON | Add `"Reply with ONLY valid JSON"` to the judge prompt and set `max_tokens=256` to prevent over-generation; retry |
| `anthropic.RateLimitError` mid-run | 100 sequential API calls hit rate limits | Add `time.sleep(0.3)` between calls or batch with `client.beta.messages.batches.create` |
| `FAIL` on a known-good pipeline | Judge rubric too strict or `expected_themes` too broad | Calibrate by running 10 examples manually, compare your human scores to judge scores, adjust the `JUDGE_PROMPT` rubric wording |
| GitHub Actions secret not found | `ANTHROPIC_API_KEY` missing from repo secrets | Add it under Settings → Secrets → Actions; confirm env var name matches the workflow YAML |
| Golden set drifts from production queries | Set was built once and never updated | Re-sample 20% of examples from recent production logs each quarter and re-score the replaced rows |
| Non-deterministic scores across runs | LLM judges have temperature variance | Pin `temperature=0` in `judge_one`'s `client.messages.create` call |

## Next

- Add `trajectory-eval-otel` instrumentation to export per-step latency and token counts alongside judge scores — gives a cost/quality Pareto view per PR.
- Extend the golden set to 500 examples with adversarial edge cases (ambiguous inputs, retrieval misses, conflicting context) to catch regressions that slip through the balanced 100-example set.
- Promote to a nightly scheduled run (change `on: pull_request` to `on: schedule: - cron: '0 2 * * *'`) and alert on consecutive-night score drops.

## References

- [knowledge/geek/ai/ai-agents/llm-judge-rubric-evidence-first](../../../knowledge/geek/ai/ai-agents/llm-judge-rubric-evidence-first) — provides the evidence-first rubric design that the judge prompt in Step 4 follows: score only what is directly observable in the response, state the criterion before assigning the number.
- [knowledge/geek/ai/ml-ops/evaluation-framework](../../../knowledge/geek/ai/ml-ops/evaluation-framework) — defines the golden-set construction lifecycle (stratified sampling, coverage targets, refresh cadence) that Steps 2 and 8 implement.
- [knowledge/geek/ai/ml-ops/evaluation-benchmarks](../../../knowledge/geek/ai/ml-ops/evaluation-benchmarks) — specifies the pass/fail threshold conventions (mean ≥ 4.0, no axis < 3.5) used as CI gates in Steps 4 and 6.
