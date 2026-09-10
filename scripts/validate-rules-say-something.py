#!/usr/bin/env python3
"""CR-011 §0 — a methodology's rules must be about its subject, and the gate must be able to tell.

`validate-methodology-v2.py` enforces exactly one thing about rules: at least
one `<rule testable="true">` exists. All 16,000+ rules in the corpus declare
`testable="true"`, so the attribute is a constant and the check is satisfied
by any document with one rule of any quality. That is how 61 pro- and
geek-tier documents shipped with rule sets shared verbatim with dozens of
unrelated documents and not one sentence about the thing they are named for.

This validator is the classifier that found them, turned into a gate:

* A rule statement that appears verbatim (normalised) in **10 or more distinct
  slugs** is cross-document FILLER — it cannot be about any one subject.
* A statement under 40 characters is a STUB.
* A statement that only restates the envelope's Applies If / Skip If (the
  `preconditions` / `must be skipped` / `action=skip` family) and is shared
  by 3+ slugs is a universal SKIP-GATE.
* Everything else is SUBJECT-BEARING.

A methodology FAILS when it has **zero** subject-bearing rules. That is the
one verdict a corpus-wide frequency count can make without reading the
document: a rule set that is entirely filler says nothing about anything.
Corpus state at the commit that introduced this gate: 0 failures of 2,514
methodologies with rules, down from 61 before CR-011's rewrite.

Deliberately NOT gated here: the share of filler in a document that has at
least one real rule (167 documents are >= 40% filler today). Gating a ratio
turns a content problem into a threshold argument; gating zero does not.

    --all      corpus sweep, `FAIL <dir>` per failing slug (what check-validators.sh runs)
    <dir>      one slug, against the corpus-wide frequency table
    --report   the corpus-wide split, no exit code
"""
from __future__ import annotations

import argparse
import collections
import glob
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE = os.path.join(REPO_ROOT, "skills", "faion", "knowledge")

RULE = re.compile(r"<rule\b[^>]*\bid=\"([^\"]+)\"[^>]*>(.*?)</rule>", re.S)
STATEMENT = re.compile(r"<statement[^>]*>(.*?)</statement>", re.S)
SKIP_WORDS = re.compile(
    r"(applies if|skip if|must be skipped|action=skip|MUST NOT run|preconditions)", re.I)

FILLER_SLUGS = 10   # a statement shared by this many slugs is about none of them
STUB_CHARS = 40
STAMP_LIST = os.path.join(REPO_ROOT, "scripts", "rules-stamp-list.txt")


def stamp_keys() -> set[str]:
    """The stamp as it was measured BEFORE the rewrite, committed.

    A live frequency table alone loses its teeth the moment the stamp is
    removed: the first version of this gate PASSED the exact google-analytics
    rules file it was written to catch, because after CR-011 those statements
    were shared by fewer than 10 slugs. Conformance to the current corpus is not
    correctness. The list below was measured at 16aa79dd8 and is read as data;
    a statement on it is filler no matter how many slugs carry it today.
    """
    try:
        lines = open(STAMP_LIST, encoding="utf-8").read().splitlines()
    except OSError:
        return set()
    return {l.split("\t", 1)[1].strip() for l in lines if l and not l.startswith("#") and "\t" in l}


def _flat(s: str) -> str:
    for ent, ch in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&apos;", "'"), ("&quot;", '"')):
        s = s.replace(ent, ch)
    return " ".join(s.split())


def _key(s: str) -> str:
    """Lowercase letters only, so two stamp rules differing by the slug they
    name or a number collapse onto one key."""
    return " ".join(re.sub(r"[^a-z ]+", " ", _flat(s).lower()).split())


def rules_of(slug_dir: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for path in sorted(glob.glob(os.path.join(slug_dir, "content", "*.xml"))):
        raw = open(path, encoding="utf-8", errors="replace").read()
        for rid, body in RULE.findall(raw):
            st = STATEMENT.search(body)
            out.append((rid, _flat(st.group(1) if st else body)))
    return out


def corpus_rules() -> dict[str, list[tuple[str, str]]]:
    docs: dict[str, list[tuple[str, str]]] = {}
    for ag in sorted(glob.glob(os.path.join(KNOWLEDGE, "*", "*", "AGENTS.md"))):
        d = os.path.dirname(ag)
        rules = rules_of(d)
        if rules:
            docs[d] = rules
    return docs


def frequency(docs: dict[str, list[tuple[str, str]]]) -> dict[str, set[str]]:
    table: dict[str, set[str]] = collections.defaultdict(set)
    for d, rules in docs.items():
        for _rid, text in rules:
            table[_key(text)].add(d)
    return table


def classify(text: str, slug_name: str, table: dict[str, set[str]], stamps: set[str] = frozenset()) -> str:
    key = _key(text)
    shared = len(table.get(key, ()))
    if len(text) < STUB_CHARS:
        return "stub"
    if shared >= FILLER_SLUGS or key in stamps:
        return "filler"
    if SKIP_WORDS.search(text) and (slug_name.replace("-", " ") in text.lower() or shared >= 3):
        return "skip-gate"
    return "subject"


def verdict(slug_dir: str, rules, table, stamps) -> tuple[int, collections.Counter]:
    kinds = collections.Counter(classify(t, os.path.basename(slug_dir), table, stamps) for _r, t in rules)
    return kinds["subject"], kinds


def rel(p: str) -> str:
    return os.path.relpath(p, REPO_ROOT)


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("target", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    docs = corpus_rules()
    table = frequency(docs)
    stamps = stamp_keys()

    if args.report:
        total = collections.Counter()
        zero = 0
        for d, rules in docs.items():
            subject, kinds = verdict(d, rules, table, stamps)
            total.update(kinds)
            zero += subject == 0
        n = sum(total.values())
        print(f"methodologies with rules: {len(docs)}   rules: {n}")
        for k, c in total.most_common():
            print(f"  {k:10} {c:6}  ({c / n * 100:.1f}%)")
        print(f"zero subject-bearing rules: {zero}")
        return 0

    if args.all:
        targets = list(docs)
    elif args.target:
        targets = [os.path.abspath(args.target)]
    else:
        ap.error("provide a slug dir, --all, or --report")

    fail = 0
    for d in targets:
        rules = docs.get(d) or rules_of(d)
        if not rules:
            continue  # v2 owns "no rules at all"
        subject, kinds = verdict(d, rules, table, stamps)
        if subject == 0:
            fail += 1
            print(f"FAIL {rel(d)}")
            print(f"  - {len(rules)} rule(s), none about the subject: "
                  f"{kinds['filler']} shared verbatim by {FILLER_SLUGS}+ slugs, "
                  f"{kinds['skip-gate']} restate Applies If / Skip If, {kinds['stub']} under {STUB_CHARS} chars")
        elif not args.all:
            print(f"PASS {rel(d)}  ({subject} subject-bearing of {len(rules)})")
    if args.all:
        print(f"\nsummary: {len(targets) - fail} pass / {fail} fail / {len(targets)} total")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
