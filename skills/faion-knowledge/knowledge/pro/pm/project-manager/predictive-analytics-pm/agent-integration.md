# Agent Integration — Predictive Analytics in PM

## When to use
- Programs with ≥12 months of clean historical project data (issues, time logs, budget actuals, vendor invoices) and recurring project shapes (e.g., 50+ comparable initiatives).
- Construction, engineering, manufacturing, infrastructure, large-scale software programs where schedule slip, cost overrun, and resource contention are repeat offenders.
- Portfolio offices needing early-warning signals for PMO interventions and trend dashboards for executives.
- Vendor / commodity-heavy programs where price volatility (steel, semiconductors, energy, cloud spend) drives budget risk.
- AI-augmented PMOs running EVM + ML side-by-side with human decision-makers.
- Pairing with `earned-value-management/` (input features), `risk-management/` (model output → register), `cost-estimation/`, `schedule-development/`, `pm-tool-selection/`, `geek/ai/ml-engineer`, `geek/ai/ml-ops`.

## When NOT to use
- Small portfolio (<10 projects) — sample size is too small for ML; use heuristics + EVM.
- Brand-new project type with no historical analogues — no training data; rely on reference-class forecasting (Flyvbjerg) instead.
- Highly creative / one-off work (research, novel product) where past patterns do not generalize.
- Privacy-sensitive contexts (HR data, classified projects) where data plumbing dominates ML cost.
- Organisations without basic data hygiene (no consistent statuses, missing actuals, freeform fields) — fix data first; ML cannot.
- When the goal is to "look modern" — predictive analytics adds value only if a decision changes from the model output. If the PMO will not act, do not build it.

## Where it fails / limitations
- Garbage-in/garbage-out dominates. Most PM trackers have inconsistent labels, undated status changes, and missing actuals — no model survives that.
- Concept drift: organisational change, new domains, new tooling all break models trained on prior projects within 6–18 months.
- Predictions become self-fulfilling or self-defeating: if the PMO acts on "delay predicted", the prediction may never realize, making model evaluation hard.
- Black-box models lose stakeholder trust fast in PM contexts. Explainability (SHAP, LIME, partial dependence) is mandatory for governance.
- Model bias replicates historical inequities — projects from disfavored business units may be systematically labeled "high-risk".
- Material price models (steel, copper, semis) inherit macro-volatility; Bayesian / interval forecasts beat point predictions.
- Resource optimization models often produce mathematically optimal but politically infeasible allocations.
- Many vendor "AI PM" features are LLM auto-summarizers, not predictive analytics — verify before integrating.

## Agentic workflow
Treat the analytics layer as a separate ML pipeline (`analytics/` repo) feeding the PM tool through alerts and dashboards, not as a Slackbot. A subagent owns the data contract (issue → feature row), trains and refreshes models, monitors drift, and writes predictions to a "predictions/" datastore that the PM tool ingests via webhook. Humans always retain decision authority — the model produces probability + explanation, never auto-actions. Pair with an MLOps loop (`geek/ai/ml-ops`) for retrain cadence and data-quality gates.

### Recommended subagents
- `faion-sdd-executor-agent` — owns the build/retrain cycle as SDD tasks: TASK_data_contract, TASK_feature_engineering, TASK_baseline_model, TASK_evaluation, TASK_deployment, TASK_monitoring.
- A custom `data-contract-agent` (model: sonnet per README "Analyze and assess"): inspects PM tool exports, defines stable feature columns, flags inconsistent statuses or missing fields.
- A custom `feature-engineering-agent` (model: sonnet): proposes engineered features (planned vs. actual ratios, queue ages, owner change counts, comment cadence) with rationale.
- A custom `model-training-agent` (model: sonnet): wraps scikit-learn / XGBoost / LightGBM / Prophet pipelines; outputs trained model + metrics + SHAP explanations.
- A custom `drift-monitor-agent` (model: haiku): runs nightly to compare incoming feature distributions vs. training set; raises alerts when KS / PSI exceeds threshold.
- A custom `prediction-explainer-agent` (model: opus per README "Strategic decision"): turns SHAP outputs into stakeholder-readable explanations for risk-register entries.
- `password-scrubber-agent` — scrubs exports before any third-party model call; Jira/Linear data leaks vendor names, prices, customer info.

### Prompt pattern
LLMs do not train models — they orchestrate. Use them for data-contract design, feature ideation, and explanation, not numeric prediction.

```
You are the data-contract agent. Inputs:
1. Sample of 5,000 issue rows from the source PM tool (CSV).
2. Project metadata (type, sponsor, budget, dates).

Emit STRICT YAML:
features:
  - name: <snake_case>
    type: numeric|categorical|boolean|datetime
    source_field: <jira_field_id>
    nullable: true|false
    notes: "..."
target:
  name: schedule_slip_days|budget_overrun_pct|risk_materialized|...
  type: regression|classification
  rationale: "..."
exclusions: [ ... fields with PII/credentials ... ]
data_quality_rules:
  - "status not in {Open, In Progress, Done, Closed} → flag"
  - "actual_start > actual_end → drop row"
```

Explanation prompt: `Given SHAP values for prediction id=X (top 5 features by |contribution|), produce a 3-sentence English explanation suitable for a risk-register entry. Cite feature name, direction, and magnitude. Do not editorialize beyond data.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `python` + `pandas` / `polars` | Feature engineering, ETL of PM data | `pip install pandas polars` |
| `scikit-learn` / `xgboost` / `lightgbm` | Tabular ML for slip / overrun / risk classification | `pip install scikit-learn xgboost lightgbm` |
| `prophet` / `sktime` / `darts` | Time-series forecasting for budget runs and material prices | `pip install prophet sktime darts` |
| `shap` / `lime` | Model explanation; required for governance | `pip install shap lime` |
| `evidently` / `nannyml` / `whylogs` | Drift and data-quality monitoring | `pip install evidently nannyml whylogs` |
| `mlflow` / `wandb` / `dvc` | Experiment tracking and model registry | `pip install mlflow wandb dvc` |
| `dbt` | SQL transformations of PM warehouse data into feature tables | https://docs.getdbt.com |
| `airbyte` / `fivetran` | Source connectors for Jira, Asana, ClickUp, Salesforce, NetSuite, Workday | https://airbyte.com / https://fivetran.com |
| `duckdb` | Local OLAP on exported CSVs without a warehouse | `pip install duckdb` |
| `feast` | Feature store for online + offline parity | https://feast.dev |
| `great-expectations` | Data-quality assertions in CI | https://greatexpectations.io |
| `prefect` / `dagster` / `airflow` | Orchestrate the ETL → train → score → publish pipeline | https://prefect.io / https://dagster.io / https://airflow.apache.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Atlassian Intelligence (Jira) | SaaS | Limited API | LLM-summarization features; minimal predictive ML at present. |
| ClickUp AI / Asana Intelligence / Monday AI | SaaS | Limited API | Mostly auto-summary and field generation; predictive features shallow. |
| Microsoft Project Cortex / Viva Insights | SaaS | Graph API | Resource and meeting analytics; useful for capacity inputs. |
| Power BI + Project for the Web | SaaS | REST | Cheapest enterprise-grade visualization on Microsoft estate. |
| Tableau / Looker / Sigma | SaaS | REST / SDK | Common dashboarding for PM analytics; pair with warehouse. |
| Snowflake / BigQuery / Databricks / Redshift | SaaS | SQL + SDK | Warehouse for unified PM data; required at scale. |
| dbt Cloud | SaaS | API | Transformation layer between sources and ML. |
| Procore + Procore Analytics | SaaS | REST | Construction-specific PM with built-in analytics. |
| Autodesk Construction Cloud (BIM 360) | SaaS | REST | Construction analytics + risk insights. |
| Oracle Primavera + Risk Analysis | SaaS / on-prem | REST | Heavy predictive scheduling for capital projects (Monte Carlo). |
| Deltek Cobra / Acumen | SaaS | REST | EVM + risk analytics for govt / aerospace contracts. |
| nPlan / ALICE Technologies | SaaS | REST | ML-driven schedule risk and AI scheduling for construction. |
| KEEL Solutions / Disperse / OpenSpace | SaaS | REST | Construction site progress capture feeding analytics. |
| AlphaSense / Bloomberg Terminal / S&P Capital IQ | SaaS | REST | Material price and macro forecasting feeds. |
| Hugging Face / Anthropic / OpenAI / Vertex AI / Azure ML | SaaS | REST | LLM/ML hosts; route via privacy DPA + zero-retention only. |

## Templates & scripts
The README is short and conceptual. Inline below: a minimal scikit-learn pipeline that predicts schedule slip from a feature CSV.

```python
#!/usr/bin/env python3
"""slip_baseline.py — baseline schedule-slip regressor."""
from __future__ import annotations
import sys
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def main(features_csv: str, model_out: str = "slip.joblib") -> int:
    df = pd.read_csv(features_csv)
    y = df.pop("slip_days")
    groups = df.pop("project_id")
    cat = [c for c in df.columns if df[c].dtype == "object"]
    num = [c for c in df.columns if c not in cat]
    pre = ColumnTransformer(
        [("num", StandardScaler(), num),
         ("cat", OneHotEncoder(handle_unknown="ignore"), cat)]
    )
    pipe = Pipeline([("pre", pre), ("gbr", GradientBoostingRegressor(random_state=0))])
    cv = GroupKFold(n_splits=5)
    scores: list[float] = []
    for tr, te in cv.split(df, y, groups):
        pipe.fit(df.iloc[tr], y.iloc[tr])
        scores.append(mean_absolute_error(y.iloc[te], pipe.predict(df.iloc[te])))
    print(f"MAE per fold: {scores}")
    print(f"MAE mean: {sum(scores) / len(scores):.2f} days")
    pipe.fit(df, y)
    joblib.dump(pipe, model_out)
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Use as the baseline — beat it with feature engineering and model selection before claiming success. Promote via MLflow registry, not by overwriting `slip.joblib` in place.

## Best practices
- Start with one decision: the model only matters if a PMO action changes when its output flips. Define the trigger (e.g., predicted slip > 14d → escalate to steering) before training.
- Reference-class forecasting (Flyvbjerg) as a baseline: simple comparable-project averages often beat ML on small portfolios. Beat the baseline before going complex.
- Predict intervals, not points: schedule slip "8 days ± 14 (P80)" guides better decisions than "8 days".
- Group splits in cross-validation by project or program — random splits leak future into past.
- Calibrate probabilities (Platt / isotonic) before publishing — uncalibrated risk scores produce false alarms.
- Explainability is non-optional in PM. Ship SHAP values with every prediction; a black-box risk-register entry will be ignored.
- Drift-monitor in production: KS / PSI on input distributions, calibration drift on outputs, monthly retrains as default.
- Keep humans in the loop for any escalation. Auto-action is reserved for low-stakes nudges (assignee reminders), never for budget or schedule changes.
- Version the data, not just the model. Use DVC or warehouse snapshots; "model says X" is meaningless without "trained on snapshot Y".
- Document model cards (intended use, training data, metrics, limitations) per Mitchell et al. — required by AI Act for high-risk systems.
- Cap PII / financial data scope to what the model needs; tokenize or hash identifiers.
- Pair with `risk-management/`: model outputs are inputs to the register, not replacements.

## AI-agent gotchas
- LLMs are not numeric forecasters. Do not let an LLM "predict" budget overruns from prose — train a model. LLMs draft, explain, and orchestrate.
- Confabulated metrics: agents will invent MAE / R² / AUC values without running code; force the metrics to come from sklearn output captured by the agent's tool, not the LLM.
- Data leakage: agents conflate target and feature when columns share names (e.g., `final_cost` vs. `forecast_cost`). Force a leakage audit step.
- Sample-size collapse: small samples + many features → overfitting. Force a feature-count cap (e.g., features ≤ N/10).
- Survivorship bias: closed-only datasets exclude killed projects. Re-include them or label outcomes accordingly.
- Bias replication: protected-class data (region, business-unit reputation) leaks into "high-risk" labels. Run fairness checks; remove proxies.
- Shipping a model without monitoring is silent failure — agents declare "deployed" and walk away. Force a monitoring task into the SDD chain.
- Privacy: PM data often includes salary, vendor pricing, customer names. Never send raw rows to a third-party LLM; tokenize or run on-prem.
- Drift-detection thresholds hallucinated: agents pick "reasonable" KS thresholds that fire constantly or never. Calibrate against a validation period.
- Long-context drift: LLMs lose the schema after ~3,000 lines of CSV. Always operate on the data contract YAML, not raw rows.
- Decision-rights confusion: agents schedule "auto re-baseline on slip prediction"; PM decisions belong to humans. Prediction → recommendation → human approval → action.
- Cost runaway: hyperparameter search via cloud GPUs without a budget cap. Cap with explicit budget guardrails per training run.
- Human-in-the-loop checkpoints (mandatory): training-data contract approval, model promotion to prod, threshold changes, deprecation/retraining, any auto-action policy.

## References
- Hyndman & Athanasopoulos "Forecasting: Principles and Practice" — https://otexts.com/fpp3/
- Flyvbjerg "Reference Class Forecasting" — https://en.wikipedia.org/wiki/Reference_class_forecasting
- Mitchell et al. "Model Cards for Model Reporting" — https://arxiv.org/abs/1810.03993
- Lundberg & Lee "A Unified Approach to Interpreting Model Predictions" (SHAP) — https://arxiv.org/abs/1705.07874
- Sculley et al. "Hidden Technical Debt in Machine Learning Systems" — https://research.google/pubs/pub43146/
- PMI "AI in Project Management" reports — https://www.pmi.org/learning/thought-leadership/ai-impact
- ISO/IEC 5338 + ISO/IEC 42001 — AI lifecycle and AI management system standards.
- Sibling methodologies: `earned-value-management/`, `risk-management/`, `cost-estimation/`, `schedule-development/`, `pm-tool-selection/`, `geek/ai/ml-engineer`, `geek/ai/ml-ops`.
