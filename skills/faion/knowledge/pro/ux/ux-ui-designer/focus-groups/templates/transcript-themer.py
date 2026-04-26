"""
transcript-themer.py — TF-IDF + k-means theme extraction from focus group transcript JSON.

Usage: python transcript-themer.py transcript.json [--k 5]
  transcript.json: [{"speaker": "P1", "text": "...", "ts": "00:12:34"}]

Output: theme clusters with top utterances and speaker distribution to stdout.

Requires: pip install scikit-learn
Note: Output is a starting point for human analysis — verify all themes manually.
      LLM-based synthesis collapses minority views; check the raw cluster items.
"""
import argparse
import json
import sys
from collections import Counter

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
except ImportError:
    print("Missing dependency: pip install scikit-learn", file=sys.stderr)
    sys.exit(2)


def extract_themes(utterances: list, k: int = 5) -> dict:
    # Filter very short utterances (likely filler)
    texts = [u for u in utterances if len(u["text"].split()) > 6]

    if len(texts) < k:
        print(f"WARN: only {len(texts)} utterances after filtering — reduce k or check transcript", file=sys.stderr)
        k = max(2, len(texts) // 2)

    raw_texts = [u["text"] for u in texts]
    vectorizer = TfidfVectorizer(stop_words="english", max_features=2000)
    X = vectorizer.fit_transform(raw_texts)

    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)

    clusters: dict[int, list] = {i: [] for i in range(k)}
    for label, utt in zip(km.labels_, texts):
        clusters[label].append(utt)

    return clusters


def report(clusters: dict) -> None:
    for theme_id, items in sorted(clusters.items()):
        speakers = Counter(u["speaker"] for u in items)
        print(f"\n--- Theme {theme_id + 1} ({len(items)} utterances, speakers: {dict(speakers)}) ---")
        for item in items[:4]:
            ts = item.get("ts", "")
            print(f"  [{ts}] {item['speaker']}: {item['text'][:120]}")
        if len(items) > 4:
            print(f"  ... ({len(items) - 4} more)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", help="Path to transcript JSON")
    parser.add_argument("--k", type=int, default=5, help="Number of theme clusters (default 5)")
    args = parser.parse_args()

    utterances = json.load(open(args.transcript))
    clusters = extract_themes(utterances, k=args.k)
    report(clusters)

    print("\nIMPORTANT: Review all clusters manually. Check for minority views not represented in top-4 quotes.")
