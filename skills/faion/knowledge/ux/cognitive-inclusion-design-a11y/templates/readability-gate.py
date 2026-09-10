#!/usr/bin/env python3
# purpose: Stdlib readability scorer.
# consumes: see content/02-output-contract.xml inputs for cognitive-inclusion-design
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-600 tokens when loaded as context

"""Procedure step 1 (score-language) as a CI gate for English copy.

Usage:
    readability-gate.py copy.txt [--jargon terms.txt] [--owner @handle]
                        [--locale-override "<reason>"] [--out report.json]

Passes when Flesch Reading Ease >= 60 AND Flesch-Kincaid Grade <= 8 (the stricter
reading of rule plain-language-target). Exit 1 = STOP and rewrite (decision-gate).
A locale override records the reason in the report; it never silences a failure.
Syllable counting is a heuristic; expect +-1 grade on very short or very technical text.
"""
import argparse
import datetime
import json
import re
import sys

FLESCH_MIN, GRADE_MAX = 60.0, 8.0
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
SENT_RE = re.compile(r"[.!?]+(?:\s|$)")


def syllables(word: str) -> int:
    w = word.lower().strip("'-")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)  # silent endings
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]+", w)))


def score(text: str) -> dict:
    words = WORD_RE.findall(text)
    sentences = max(1, len(SENT_RE.findall(text)) or 1)
    n_words = max(1, len(words))
    syl = sum(syllables(w) for w in words)
    wps, spw = n_words / sentences, syl / n_words
    return {
        "words": n_words,
        "sentences": sentences,
        "flesch": round(206.835 - 1.015 * wps - 84.6 * spw, 1),
        "grade": round(0.39 * wps + 11.8 * spw - 15.59, 1),
    }


def undefined_jargon(text: str, terms: list[str]) -> list[str]:
    """A term counts as defined when its first use is followed by '(', ' means ' or ', that is,'."""
    flagged = []
    for term in terms:
        m = re.search(rf"\b{re.escape(term)}\b", text, re.I)
        if m and not re.match(r"\s*(\(|means\b|, that is,|, i\.e\.)", text[m.end():m.end() + 12], re.I):
            flagged.append(term)
    return flagged


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("copy", help="plain-text file of user-facing copy; blank line separates spans")
    ap.add_argument("--jargon", help="file with one jargon term per line that must be defined inline")
    ap.add_argument("--owner", default="<@designer>")
    ap.add_argument("--locale-override", default="", help="documented reason a locale uses a different target")
    ap.add_argument("--out", default="readability-report.json")
    args = ap.parse_args()

    text = open(args.copy, encoding="utf-8").read()
    terms = [t.strip() for t in open(args.jargon, encoding="utf-8")] if args.jargon else []
    total = score(text)
    spans = [s.strip() for s in re.split(r"\n\s*\n", text) if s.strip()]
    below = [{"span": s[:80], **score(s)} for s in spans
             if score(s)["flesch"] < FLESCH_MIN or score(s)["grade"] > GRADE_MAX]
    jargon = undefined_jargon(text, [t for t in terms if t])

    lang_ok = total["flesch"] >= FLESCH_MIN and total["grade"] <= GRADE_MAX
    findings = [
        {"rule": "plain-language-target", "verdict": "pass" if lang_ok else "fail",
         "detail": f"flesch {total['flesch']} (min {FLESCH_MIN}), grade {total['grade']} (max {GRADE_MAX}); "
                   f"{len(below)} of {len(spans)} spans below target",
         "spans_below_target": below,
         "locale_override": args.locale_override or None},
        {"rule": "plain-language-target/jargon", "verdict": "pass" if not jargon else "fail",
         "detail": "undefined jargon: " + (", ".join(jargon) or "none")},
    ]
    report = {
        "artefact_id": f"cog-{datetime.date.today():%Y-%m-%d}-language",
        "version": "1.1.0",
        "last_reviewed": datetime.date.today().isoformat(),
        "owner": args.owner,
        "scope": {"component": args.copy, "reading_level": {"flesch": total["flesch"], "grade": total["grade"]},
                  "language": "en", "target": {"flesch_min": FLESCH_MIN, "grade_max": GRADE_MAX}},
        "findings": findings,
        "summary": "Language report only; nav, error-flow, critical-action and timeout audits are separate steps.",
        "verdict": "pass" if all(f["verdict"] == "pass" for f in findings) else "fail",
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"{report['verdict'].upper()}: flesch={total['flesch']} grade={total['grade']} "
          f"spans_below={len(below)} jargon={len(jargon)} -> {args.out}")
    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
