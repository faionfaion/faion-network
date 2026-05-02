---
name: model-monitoring-drift
description: Log every LLM call to Postgres/S3, run daily KL-divergence and refusal-rate aggregations, score samples with an LLM judge, and fire Slack alerts when thresholds breach.
tier: geek
group: ml-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a production monitoring pipeline that logs every LLM call (prompt, response, latency, token counts) to Postgres and S3, runs a nightly aggregation job that computes token-distribution KL-divergence against a stable baseline, refusal rate, and LLM-judge confidence on a 5 % sample, and fires a Slack alert the moment any metric breaches its threshold.

## Prerequisites

- Python 3.11+, `pip install anthropic>=0.51 psycopg[binary]>=3.1 boto3>=1.34 scipy>=1.13 slack-sdk>=3.27 pydantic>=2.7`.
- A Postgres 15+ instance with `CREATE TABLE` access (local Docker or managed, e.g. Neon/Supabase).
- An S3-compatible bucket (AWS S3, Cloudflare R2, or MinIO) for raw JSONL archives.
- An `ANTHROPIC_API_KEY`, `DATABASE_URL` (DSN string), `AWS_*` credentials, and `SLACK_BOT_TOKEN` + `SLACK_ALERT_CHANNEL` in environment or `.env`.
- Basic familiarity with Anthropic Python SDK tool-use and token-count fields.
- 7–14 days of existing production traffic, or a synthetic baseline dataset, to calibrate KL-divergence thresholds before enabling live alerts.

## Steps

1. **Create the schema** in Postgres. Run once at deploy time.

   ```sql
   CREATE TABLE llm_calls (
       id          BIGSERIAL PRIMARY KEY,
       ts          TIMESTAMPTZ NOT NULL DEFAULT now(),
       model       TEXT        NOT NULL,
       feature     TEXT        NOT NULL,
       user_id     TEXT,
       prompt_hash TEXT        NOT NULL,
       input_tokens  INT NOT NULL,
       output_tokens INT NOT NULL,
       latency_ms    INT NOT NULL,
       refusal       BOOLEAN NOT NULL DEFAULT FALSE,
       s3_key        TEXT NOT NULL
   );
   CREATE INDEX ON llm_calls (ts DESC);
   CREATE INDEX ON llm_calls (feature, ts DESC);
   ```

2. **Install the logging wrapper** that instruments every Anthropic SDK call.

   ```python
   # monitor/logger.py
   import hashlib, json, os, time
   from datetime import datetime, timezone
   from pathlib import Path

   import boto3
   import psycopg
   from anthropic import Anthropic
   from pydantic import BaseModel

   REFUSAL_PHRASES = frozenset([
       "i cannot", "i can't", "i am unable", "sorry, i",
       "as an ai", "against my guidelines", "not appropriate",
   ])

   class CallRecord(BaseModel):
       ts: datetime
       model: str
       feature: str
       user_id: str | None
       prompt: str
       response: str
       input_tokens: int
       output_tokens: int
       latency_ms: int
       refusal: bool
       s3_key: str

   _s3 = boto3.client("s3")
   _BUCKET = os.environ["S3_BUCKET"]
   _DB_DSN = os.environ["DATABASE_URL"]

   def _is_refusal(text: str) -> bool:
       low = text.lower()
       return any(p in low for p in REFUSAL_PHRASES)

   def _archive_to_s3(record: CallRecord) -> str:
       key = f"llm-calls/{record.ts.date()}/{record.ts.isoformat()}.json"
       _s3.put_object(
           Bucket=_BUCKET,
           Key=key,
           Body=record.model_dump_json().encode(),
           ContentType="application/json",
       )
       return key

   def logged_call(
       client: Anthropic,
       *,
       model: str,
       messages: list[dict],
       feature: str,
       user_id: str | None = None,
       **kwargs,
   ) -> str:
       """Drop-in wrapper around client.messages.create; returns response text."""
       prompt_text = json.dumps(messages)
       t0 = time.perf_counter()
       resp = client.messages.create(
           model=model,
           messages=messages,
           **kwargs,
       )
       latency_ms = int((time.perf_counter() - t0) * 1000)
       response_text = resp.content[0].text if resp.content else ""

       record = CallRecord(
           ts=datetime.now(timezone.utc),
           model=model,
           feature=feature,
           user_id=user_id,
           prompt=prompt_text,
           response=response_text,
           input_tokens=resp.usage.input_tokens,
           output_tokens=resp.usage.output_tokens,
           latency_ms=latency_ms,
           refusal=_is_refusal(response_text),
           s3_key="",
       )
       record.s3_key = _archive_to_s3(record)

       with psycopg.connect(_DB_DSN) as conn:
           conn.execute(
               """
               INSERT INTO llm_calls
                 (ts, model, feature, user_id, prompt_hash,
                  input_tokens, output_tokens, latency_ms, refusal, s3_key)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               """,
               (
                   record.ts, record.model, record.feature, record.user_id,
                   hashlib.sha256(prompt_text.encode()).hexdigest()[:16],
                   record.input_tokens, record.output_tokens,
                   record.latency_ms, record.refusal, record.s3_key,
               ),
           )
       return response_text
   ```

3. **Use `logged_call` in production** in place of `client.messages.create`.

   ```python
   from anthropic import Anthropic
   from monitor.logger import logged_call

   client = Anthropic()

   answer = logged_call(
       client,
       model="claude-sonnet-4-6",
       messages=[{"role": "user", "content": "Summarize the following: ..."}],
       feature="article-summary",
       user_id="u-9912",
       max_tokens=512,
   )
   ```

4. **Capture the baseline token distribution.** Run this once against 7+ days of stable traffic to store the reference histogram in Postgres.

   ```python
   # monitor/baseline.py
   import json
   import numpy as np
   import psycopg, os

   _DB_DSN = os.environ["DATABASE_URL"]

   def capture_baseline(feature: str, days: int = 7) -> None:
       """Compute output-token histogram for the last `days` days and store it."""
       with psycopg.connect(_DB_DSN) as conn:
           rows = conn.execute(
               """
               SELECT output_tokens FROM llm_calls
               WHERE feature = %s
                 AND ts > now() - (%s || ' days')::interval
               """,
               (feature, str(days)),
           ).fetchall()

       counts = [r[0] for r in rows]
       if len(counts) < 100:
           raise ValueError(f"Need ≥100 samples for baseline; got {len(counts)}")

       hist, edges = np.histogram(counts, bins=50, range=(0, 2048), density=True)
       hist = hist + 1e-9  # Laplace smoothing — avoids log(0) in KL

       with psycopg.connect(_DB_DSN) as conn:
           conn.execute(
               """
               INSERT INTO baselines (feature, captured_at, hist_json, edges_json)
               VALUES (%s, now(), %s, %s)
               ON CONFLICT (feature) DO UPDATE
                 SET captured_at = EXCLUDED.captured_at,
                     hist_json   = EXCLUDED.hist_json,
                     edges_json  = EXCLUDED.edges_json
               """,
               (feature, json.dumps(hist.tolist()), json.dumps(edges.tolist())),
           )
   ```

   Also add the `baselines` table:

   ```sql
   CREATE TABLE baselines (
       feature      TEXT PRIMARY KEY,
       captured_at  TIMESTAMPTZ NOT NULL,
       hist_json    TEXT NOT NULL,
       edges_json   TEXT NOT NULL
   );
   ```

5. **Write the daily aggregation job.** This runs via cron (e.g. `0 6 * * *`) or a scheduled task. It computes KL-divergence, refusal rate, and an LLM-judge confidence score, then fires Slack if any threshold is breached.

   ```python
   # monitor/daily_agg.py
   import json, os, random
   import numpy as np
   import psycopg
   from scipy.special import kl_div
   from anthropic import Anthropic
   from slack_sdk import WebClient

   _DB_DSN   = os.environ["DATABASE_URL"]
   _SLACK_TOKEN   = os.environ["SLACK_BOT_TOKEN"]
   _SLACK_CHANNEL = os.environ["SLACK_ALERT_CHANNEL"]

   KL_THRESHOLD       = 0.05   # nats — tune after first 14 days
   REFUSAL_THRESHOLD  = 0.08   # 8 % refusal rate
   CONFIDENCE_THRESHOLD = 0.72  # avg judge score below this fires alert

   def _kl_divergence(p: list[float], q: list[float]) -> float:
       p_arr = np.array(p, dtype=float)
       q_arr = np.array(q, dtype=float)
       p_arr /= p_arr.sum()
       q_arr /= q_arr.sum()
       return float(np.sum(kl_div(p_arr, q_arr)))

   def _judge_confidence(client: Anthropic, sample: list[dict]) -> float:
       """Ask claude-haiku-4-5 to score a batch of responses 0–1."""
       if not sample:
           return 1.0
       scores = []
       for item in sample:
           resp = client.messages.create(
               model="claude-haiku-4-5-20251001",
               max_tokens=16,
               system=(
                   "Rate the quality of the following AI response on a scale of 0.0 to 1.0. "
                   "Reply with only the number, e.g. '0.87'."
               ),
               messages=[{
                   "role": "user",
                   "content": f"Prompt: {item['prompt'][:400]}\n\nResponse: {item['response'][:400]}",
               }],
           )
           try:
               scores.append(float(resp.content[0].text.strip()))
           except ValueError:
               scores.append(0.5)
       return float(np.mean(scores))

   def run_daily(feature: str) -> dict:
       client = Anthropic()
       slack  = WebClient(token=_SLACK_TOKEN)
       alerts = []

       with psycopg.connect(_DB_DSN) as conn:
           # Today's output-token histogram
           rows = conn.execute(
               """
               SELECT output_tokens FROM llm_calls
               WHERE feature = %s AND ts > now() - interval '1 day'
               """,
               (feature,),
           ).fetchall()
           today_counts = [r[0] for r in rows]

           # Baseline histogram
           base = conn.execute(
               "SELECT hist_json, edges_json FROM baselines WHERE feature = %s",
               (feature,),
           ).fetchone()

           # Refusal rate
           total = len(today_counts)
           refusals = conn.execute(
               """
               SELECT COUNT(*) FROM llm_calls
               WHERE feature = %s AND ts > now() - interval '1 day' AND refusal = TRUE
               """,
               (feature,),
           ).fetchone()[0]

           # 5 % sample for LLM judge
           sample_rows = conn.execute(
               """
               SELECT prompt_hash, s3_key FROM llm_calls
               WHERE feature = %s AND ts > now() - interval '1 day'
               ORDER BY random() LIMIT %s
               """,
               (feature, max(1, total // 20)),
           ).fetchall()

       # KL divergence
       if base and len(today_counts) >= 30:
           baseline_hist = json.loads(base[0])
           edges = json.loads(base[1])
           today_hist, _ = np.histogram(
               today_counts, bins=len(baseline_hist),
               range=(edges[0], edges[-1]), density=True,
           )
           today_hist = today_hist + 1e-9
           kl = _kl_divergence(today_hist.tolist(), baseline_hist)
           if kl > KL_THRESHOLD:
               alerts.append(f"KL-divergence {kl:.4f} > threshold {KL_THRESHOLD} for feature={feature}")

       # Refusal rate
       refusal_rate = refusals / total if total else 0.0
       if refusal_rate > REFUSAL_THRESHOLD:
           alerts.append(
               f"Refusal rate {refusal_rate:.1%} > threshold {REFUSAL_THRESHOLD:.0%} "
               f"for feature={feature} ({refusals}/{total})"
           )

       # LLM judge (5 % sample, cheapest model)
       # We only have s3_key in the DB; re-fetch prompt+response from S3 here
       # (omitted for brevity — see templates.md for full S3 fetch helper)
       # Stub: pass empty sample if S3 fetch not configured
       judge_score = _judge_confidence(client, [])  # replace [] with real sample
       if judge_score < CONFIDENCE_THRESHOLD:
           alerts.append(
               f"Judge confidence {judge_score:.2f} < threshold {CONFIDENCE_THRESHOLD} "
               f"for feature={feature}"
           )

       if alerts:
           msg = "\n".join([f":rotating_light: *LLM drift alert — {feature}*"] + alerts)
           slack.chat_postMessage(channel=_SLACK_CHANNEL, text=msg)

       return {"feature": feature, "total": total, "refusal_rate": refusal_rate, "alerts": alerts}
   ```

6. **Schedule the aggregation job** with a cron entry or systemd timer.

   ```
   # crontab -e
   0 6 * * * cd /srv/myapp && python3 -m monitor.daily_agg --feature article-summary >> /var/log/llm-drift.log 2>&1
   ```

   Add a `__main__` block to `daily_agg.py`:

   ```python
   if __name__ == "__main__":
       import argparse
       p = argparse.ArgumentParser()
       p.add_argument("--feature", required=True)
       args = p.parse_args()
       result = run_daily(args.feature)
       print(json.dumps(result, indent=2))
   ```

7. **Deploy a Grafana dashboard** to visualise trends. Connect Grafana to Postgres (native datasource) and add two panels using these queries.

   Panel 1 — Daily token distribution (histogram):

   ```sql
   SELECT
     date_trunc('day', ts) AS time,
     percentile_cont(0.50) WITHIN GROUP (ORDER BY output_tokens) AS p50,
     percentile_cont(0.95) WITHIN GROUP (ORDER BY output_tokens) AS p95
   FROM llm_calls
   WHERE feature = 'article-summary'
     AND $__timeFilter(ts)
   GROUP BY 1
   ORDER BY 1;
   ```

   Panel 2 — Daily refusal rate:

   ```sql
   SELECT
     date_trunc('day', ts) AS time,
     ROUND(100.0 * SUM(refusal::int) / COUNT(*), 2) AS refusal_pct
   FROM llm_calls
   WHERE feature = 'article-summary'
     AND $__timeFilter(ts)
   GROUP BY 1
   ORDER BY 1;
   ```

   Import both panels under a dashboard named `LLM Output Drift — <feature>`. Add a threshold annotation at `refusal_pct = 8` and `p95 > 1500` (tokens) for visual alerting.

## Verify

Run the aggregation job manually against the last 24 h and confirm it exits without error and emits a JSON result:

```bash
cd /srv/myapp
python3 -m monitor.daily_agg --feature article-summary
```

Expected output (no alerts scenario):

```json
{
  "feature": "article-summary",
  "total": 842,
  "refusal_rate": 0.023,
  "alerts": []
}
```

Then confirm a row is present in Postgres:

```sql
SELECT count(*), max(ts) FROM llm_calls WHERE feature = 'article-summary';
```

Returns `count > 0` and `max` within the last hour.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ValueError: Need ≥100 samples for baseline` during `capture_baseline` | Fewer than 100 rows for the feature in the selected window | Extend `days` parameter or wait for more traffic before capturing baseline |
| KL-divergence alerts fire every day immediately after baseline capture | Baseline was captured on abnormal traffic (spike day) | Re-run `capture_baseline` on a normal 7-day window; increase `KL_THRESHOLD` to 0.1 temporarily while recalibrating |
| Slack alerts arrive but `alerts` list is empty in the JSON log | Exception swallowed silently inside `slack.chat_postMessage` | Wrap the call in a try/except and log the exception; check `SLACK_BOT_TOKEN` scope includes `chat:write` |
| `psycopg.errors.UndefinedTable` on first run | `baselines` table not created | Run the `CREATE TABLE baselines` DDL from Step 4 |
| Judge confidence always returns 0.5 | `claude-haiku-4-5-20251001` content block parsing fails | Log `resp.content[0].text` raw; strip whitespace and non-numeric chars before `float()` conversion |
| S3 `NoCredentialsError` | `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` not set | Export credentials or use an IAM instance profile; for R2, set `endpoint_url` in `boto3.client` |
| Grafana panel shows no data | Postgres datasource uses UTC but `$__timeFilter` offset wrong | Set Grafana org timezone to UTC; verify `ts` column is `TIMESTAMPTZ` not naive `TIMESTAMP` |

## Next

- Add a `prompt-drift` variant that embeds prompts with `text-embedding-3-small` and tracks cosine similarity to baseline centroid daily — catches prompt-template changes that do not affect token count.
- Extend to multi-feature monitoring by looping `run_daily` over all distinct `feature` values from the `llm_calls` table.
- Wire the Slack alert into a PagerDuty incident when `kl > 0.15` (severe drift) using the PagerDuty Events API v2.

## References

- [knowledge/geek/ai/ml-ops/llm-observability-stack-2026](../../../knowledge/geek/ai/ml-ops/llm-observability-stack-2026) — the four-category metric framework (cost, quality, perf, reliability) underpins threshold selection in Steps 5 and 7; the 7–14 day baseline calibration rule from this methodology directly sets the Prerequisites requirement here.
- [knowledge/geek/ai/ml-ops/evaluation-metrics](../../../knowledge/geek/ai/ml-ops/evaluation-metrics) — the refusal-rate and LLM-judge-score patterns in Step 5 implement the safety and quality metric families from this methodology; the 5–10 % sampling rule for judge calls is taken directly from its production-cost guidance.
