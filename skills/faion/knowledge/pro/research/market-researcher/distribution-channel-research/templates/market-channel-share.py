"""
market-channel-share.py — aggregate per-competitor traffic mixes into
a market-level channel-share table with confidence bands.

Usage: python market-channel-share.py mix.yaml

mix.yaml shape:
  competitors:
    - name: Acme
      weight: 1.0   # use monthly visits as proxy weight
      mix:
        direct: 0.35
        search_organic: 0.30
        search_paid: 0.10
        social: 0.15
        referral: 0.05
        mail: 0.05
"""
import sys, yaml


def aggregate(rows: list[dict]) -> dict[str, dict]:
    chans = sorted({k for r in rows for k in r["mix"].keys()})
    out = {}
    for c in chans:
        vals = [r["mix"].get(c, 0.0) for r in rows]
        wts = [r.get("weight", 1.0) for r in rows]
        wsum = sum(wts) or 1
        mean = sum(v * w for v, w in zip(vals, wts)) / wsum
        spread = max(vals) - min(vals)
        n_nonzero = sum(1 for v in vals if v > 0)
        if n_nonzero >= 7:
            conf = "HIGH"
        elif n_nonzero >= 4:
            conf = "MED"
        else:
            conf = "LOW"
        out[c] = {
            "share": round(mean, 3),
            "spread": round(spread, 3),
            "n": n_nonzero,
            "conf": conf,
        }
    return out


def render(agg: dict[str, dict]) -> None:
    print("| Channel | Market Share | Spread (max-min) | N competitors | Confidence |")
    print("|---------|-------------|------------------|----------------|------------|")
    for c, r in sorted(agg.items(), key=lambda x: -x[1]["share"]):
        print(
            f"| {c} | {r['share']*100:.1f}% | {r['spread']*100:.1f}pp"
            f" | {r['n']} | {r['conf']} |"
        )


def main(path: str) -> None:
    data = yaml.safe_load(open(path))
    render(aggregate(data["competitors"]))


if __name__ == "__main__":
    main(sys.argv[1])
