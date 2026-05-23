"""
metrics-parser.py — compute tree test metrics from a Treejack CSV export.

Usage: python metrics-parser.py treejack-tasks-export.csv metrics.csv

Columns expected from Treejack "Tasks" export:
  task_id, success (values: "Direct success", "Indirect success", "Direct fail",
  "Indirect fail", "Given up"), first_click_correct (boolean), time_taken_s

Note: Maze and UXtweak use different column names — build adapter per provider.
"""
import pandas as pd, sys


def compute_metrics(input_csv: str, output_csv: str) -> None:
    df = pd.read_csv(input_csv)
    out = []

    for task_id, g in df.groupby("task_id"):
        n = len(g)
        success_values = {"Direct success", "Indirect success"}
        direct_success_values = {"Direct success"}

        success = g["success"].isin(success_values).sum()
        direct = g["success"].isin(direct_success_values).sum()
        first_click_correct = g["first_click_correct"].sum()

        out.append({
            "task": task_id,
            "n": n,
            "success_rate": round(success / n, 3),
            "directness": round(direct / n, 3),
            "first_click_correct_rate": round(first_click_correct / n, 3),
            "median_time_s": round(g["time_taken_s"].median(), 1),
            "abandoned_pct": round(
                (g["success"] == "Given up").sum() / n, 3
            ),
        })

    result = pd.DataFrame(out).sort_values("success_rate")
    result.to_csv(output_csv, index=False)

    # Print summary
    print(f"\nTree Test Metrics ({n} participants, {len(out)} tasks)")
    print(f"Overall success rate: {result['success_rate'].mean():.1%}")
    print(f"Overall directness: {result['directness'].mean():.1%}")
    print("\nWorst 3 tasks:")
    print(result.head(3)[["task", "success_rate", "directness", "first_click_correct_rate"]].to_string(index=False))
    print(f"\nFull results: {output_csv}")


if __name__ == "__main__":
    compute_metrics(sys.argv[1], sys.argv[2])
