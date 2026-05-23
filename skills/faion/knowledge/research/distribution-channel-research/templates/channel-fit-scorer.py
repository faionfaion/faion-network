# purpose: Score each channel on fit + cost + speed + measurability
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
# channel_fit_scorer.py — score channels vs fixed weights, emit ranked markdown table
# Input: channels.yaml with channel scores per criterion
# Output: ranked markdown table to stdout
# Usage: python channel_fit_scorer.py channels.yaml
import sys, yaml

WEIGHTS = {
    "audience":    0.25,
    "competitors": 0.15,
    "cost":        0.20,
    "time":        0.15,
    "scale":       0.15,
    "capability":  0.10,
}


def weighted_score(ch: dict) -> float:
    return round(sum(ch["scores"][k] * w for k, w in WEIGHTS.items()), 2)


def main(path: str) -> None:
    data = yaml.safe_load(open(path))
    rows = [(c["name"], c["scores"], weighted_score(c)) for c in data["channels"]]
    rows.sort(key=lambda r: -r[2])

    cols = list(WEIGHTS.keys())
    header = "| Channel | " + " | ".join(cols) + " | Total |"
    sep = "|" + "---|" * (len(cols) + 2)
    print(header)
    print(sep)
    for name, sc, total in rows:
        cells = " | ".join(str(sc.get(k, "-")) for k in cols)
        print(f"| {name} | {cells} | {total} |")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "channels.yaml")
