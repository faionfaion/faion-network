"""
Normalize interview JSON exports to standard records for LLM clustering input.
Input: one or more JSON file paths (as CLI args).
Output: JSON array of normalized records printed to stdout.
"""
import json
import pathlib
import sys


def normalize_interviews(paths: list[str]) -> list[dict]:
    records = []
    for p in paths:
        raw = json.loads(pathlib.Path(p).read_text())
        for segment in raw.get("segments", [raw]):
            records.append({
                "user_id": segment.get("user_id", "anon"),
                "quote": segment.get("transcript", ""),
                "tags": segment.get("tags", []),
                "session_date": segment.get("date", ""),
            })
    return records


if __name__ == "__main__":
    result = normalize_interviews(sys.argv[1:])
    print(json.dumps(result, indent=2, ensure_ascii=False))
