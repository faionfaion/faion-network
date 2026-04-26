#!/usr/bin/env python3
"""slip_baseline.py — baseline schedule-slip regressor (GBR, GroupKFold).

Input:  CSV with feature columns + 'slip_days' target + 'project_id' group column.
Output: trained pipeline saved to model_out (joblib), MAE per fold printed.

Beat this baseline with feature engineering before claiming ML adds value.
Promote via MLflow registry, not by overwriting slip.joblib in place.
"""
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
