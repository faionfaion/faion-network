# vui_fairness.py — WER-by-demographic evaluator
# Input CSV columns: utterance_id, accent, age_group, ref_text, hyp_text
# Output: tab-separated WER table by group; flags groups with WER > 1.5x overall
# Install: pip install jiwer
import csv
import sys
from collections import defaultdict

try:
    import jiwer
except ImportError:
    sys.exit("Install jiwer: pip install jiwer")

DISPARITY_THRESHOLD = 1.5  # flag subgroup WER > 1.5x overall WER


def evaluate(path: str) -> None:
    by_group: dict = defaultdict(lambda: {"refs": [], "hyps": []})

    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in ("accent", "age_group"):
                g = (key, row[key])
                by_group[g]["refs"].append(row["ref_text"])
                by_group[g]["hyps"].append(row["hyp_text"])

    all_refs = sum((v["refs"] for v in by_group.values()), [])
    all_hyps = sum((v["hyps"] for v in by_group.values()), [])
    overall_wer = jiwer.wer(all_refs, all_hyps)

    header = ("group_type", "group_value", "n", "wer", "flag")
    rows = [header]

    for (gtype, gval), data in sorted(by_group.items()):
        wer = jiwer.wer(data["refs"], data["hyps"])
        flag = "REVIEW" if wer > overall_wer * DISPARITY_THRESHOLD else ""
        rows.append((gtype, gval, len(data["refs"]), f"{wer:.3f}", flag))

    rows.append(("overall", "-", len(all_refs), f"{overall_wer:.3f}", ""))

    for row in rows:
        print("\t".join(map(str, row)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python vui_fairness.py <csv_path>")
    evaluate(sys.argv[1])
