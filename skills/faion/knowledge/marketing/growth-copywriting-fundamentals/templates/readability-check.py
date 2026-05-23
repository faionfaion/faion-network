"""
Copy Readability Checker
Scores copy against targets for email, landing page, and ad copy.

Install: pip install textstat
Usage: python readability-check.py
       (paste your copy at the COPY variable below, or pipe via stdin)
"""

import sys
import textstat


TARGETS = {
    "flesch_reading_ease": (60, 70, "higher is easier; 60-70 = 8th grade"),
    "gunning_fog": (None, 10, "lower is better; target <10"),
    "avg_sentence_length": (None, 20, "lower is better; target <20 words"),
}


def check(copy: str) -> None:
    scores = {
        "flesch_reading_ease": textstat.flesch_reading_ease(copy),
        "gunning_fog": textstat.gunning_fog(copy),
        "avg_sentence_length": textstat.avg_sentence_length(copy),
    }

    print("\n=== Readability Scores ===")
    for metric, value in scores.items():
        low, high, note = TARGETS[metric]
        if high and value > high:
            status = "FAIL"
        elif low and value < low:
            status = "WARN"
        else:
            status = "OK"
        print(f"  {status:4}  {metric}: {value:.1f}  ({note})")

    word_count = len(copy.split())
    print(f"\n  INFO  Word count: {word_count}")

    you_count = copy.lower().count(" you") + copy.lower().count(" your")
    we_count = copy.lower().count(" we ") + copy.lower().count(" our ")
    if we_count > 0:
        ratio = you_count / we_count
        status = "OK" if ratio >= 2 else "WARN"
        print(f"  {status:4}  You/We ratio: {ratio:.1f} (target 2:1)")
    print()


if __name__ == "__main__":
    if not sys.stdin.isatty():
        copy = sys.stdin.read()
    else:
        copy = """
Paste your copy here to test it.
Replace this text with your landing page, email, or ad copy.
Run the script to see readability scores.
"""
    check(copy)
