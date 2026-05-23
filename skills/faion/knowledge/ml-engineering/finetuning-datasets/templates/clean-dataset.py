"""
Dataset cleaning pipeline: deduplication, filtering, and train/val split.
Input:  raw JSON file (list of {"instruction", "output"} or similar)
Output: train.json and val.json files
"""
import json
import random
import sys


def clean_dataset(
    raw_data: list,
    min_output_len: int = 10,
    max_output_len: int = 4096,
) -> list:
    cleaned = []
    seen: set = set()
    for item in raw_data:
        key = (item.get("instruction", ""), item.get("output", ""))
        if key in seen:
            continue
        seen.add(key)
        output = item.get("output", "").strip()
        if not output:
            continue
        if len(output) < min_output_len or len(output) > max_output_len:
            continue
        cleaned.append(item)
    return cleaned


def split_dataset(data: list, val_ratio: float = 0.1, seed: int = 42):
    random.seed(seed)
    shuffled = data[:]
    random.shuffle(shuffled)
    split = int(len(shuffled) * val_ratio)
    return shuffled[split:], shuffled[:split]  # train, val


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "raw_data.json"
    with open(input_path) as f:
        raw = json.load(f)

    cleaned = clean_dataset(raw)
    print(f"Cleaned: {len(raw)} -> {len(cleaned)} examples")

    train, val = split_dataset(cleaned, val_ratio=0.1)
    with open("train.json", "w") as f:
        json.dump(train, f, indent=2)
    with open("val.json", "w") as f:
        json.dump(val, f, indent=2)
    print(f"Train: {len(train)}, Val: {len(val)}")
