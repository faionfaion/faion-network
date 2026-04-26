"""
vui-batch-runner.py — batch intent-accuracy runner against Alexa ask-cli simulate.

Usage: python vui-batch-runner.py test-matrix.jsonl
  test-matrix.jsonl: one JSON object per line:
    {"utterance": "...", "expected_intent": "...", "expected_slots": {...}}

Output: per-intent accuracy table to stdout.

Requires:
  - ask-cli installed and configured (npm i -g ask-cli)
  - SKILL_ID env variable set to the Alexa skill ID
  - Python 3.9+
"""
import json
import os
import statistics
import subprocess
import sys


SKILL_ID = os.environ.get("SKILL_ID", "amzn1.ask.skill.REPLACE_ME")
LOCALE = os.environ.get("LOCALE", "en-US")


def simulate(text: str) -> dict:
    out = subprocess.check_output(
        ["ask", "simulate", "-t", text, "-l", LOCALE, "-s", SKILL_ID],
        stderr=subprocess.DEVNULL,
    )
    return json.loads(out)


def extract_intent(result: dict) -> str | None:
    try:
        body = result["result"]["skillExecutionInfo"]["invocationResponse"]["body"]
        return body.get("intent", {}).get("name")
    except (KeyError, TypeError):
        return None


def run(matrix_path: str) -> list:
    rows = []
    with open(matrix_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            case = json.loads(line)
            try:
                result = simulate(case["utterance"])
                got_intent = extract_intent(result)
            except subprocess.CalledProcessError as e:
                got_intent = None
                print(f"WARN simulate failed for: {case['utterance'][:60]}", file=sys.stderr)
            rows.append({
                **case,
                "got_intent": got_intent,
                "ok": got_intent == case["expected_intent"],
            })
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)

    rows = run(sys.argv[1])
    by_intent: dict[str, list[bool]] = {}
    for r in rows:
        by_intent.setdefault(r["expected_intent"], []).append(r["ok"])

    print(f"\n{'Intent':<40} {'Pass':>5} {'Total':>5} {'Accuracy':>9}")
    print("-" * 65)
    for intent, results in sorted(by_intent.items()):
        passed = sum(results)
        total = len(results)
        acc = statistics.mean(results)
        flag = " <-- LOW" if acc < 0.85 else ""
        print(f"{intent:<40} {passed:>5} {total:>5} {acc:>8.1%}{flag}")

    overall = sum(r["ok"] for r in rows) / len(rows) if rows else 0
    print(f"\nOverall: {overall:.1%} ({sum(r['ok'] for r in rows)}/{len(rows)})")
