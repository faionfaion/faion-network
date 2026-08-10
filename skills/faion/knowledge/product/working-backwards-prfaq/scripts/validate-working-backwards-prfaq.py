#!/usr/bin/env python3
"""Validate a PRFAQ Record against the working-backwards-prfaq contract.

Enforces the five-phase early stop (r1, r7), the past-tense press release
(r2), the implementation-noun ban in the headline (r3), the two separate FAQ
banks (r4, r5) and the concept_type / success_measure coupling (r6).

Usage:
  validate-working-backwards-prfaq.py <prfaq-record.yaml|.json>
  validate-working-backwards-prfaq.py --self-test
  validate-working-backwards-prfaq.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

CONCEPT_TYPES = {
    "commercial", "internal", "oss", "nonprofit", "service", "creative", "physical",
}
VERDICTS = {"proceed", "revise", "kill"}

BASE_KEYS = (
    "concept", "concept_type", "customer", "problem", "problem_evidence",
    "verdict", "verdict_rationale",
)

# Which record key belongs to which phase, for the early-stop check (r7).
PHASE_KEYS = {
    2: ("press_release",),
    3: ("customer_faq",),
    4: ("internal_faq", "must_be_true", "cheapest_disproof"),
    5: ("success_measure",),
}

# r7 — a judgement, never a number, under any field name.
BANNED_KEY_TOKENS = ("score", "rating", "confidence", "points", "weighted", "total")

# r2 — forward-looking verb forms in a launch announcement.
FUTURE_PATTERNS = (
    r"\bwill\b", r"\bwon't\b", r"\bplans? to\b", r"\baims? to\b",
    r"\bis going to\b", r"\bare going to\b", r"\bshall\b",
    r"\broadmap\b", r"\bcoming soon\b", r"\bin the future\b", r"\bsoon\b",
)

# r3 — implementation nouns banned from headline and subhead.
IMPL_NOUNS = (
    "ai-powered", "ai ", "llm", "platform", "engine", "framework", "api",
    "blockchain", "algorithm", "microservice", "saas", "machine learning",
)

# r6 — the antagonist each concept_type implies, as tokens the measure must name.
ANTAGONIST_TOKENS = {
    "commercial": ("pay", "price", "paid", "revenue", "purchas"),
    "internal": ("fund", "budget", "headcount", "sponsor"),
    "oss": ("maintain", "contributor", "maintainer"),
    "nonprofit": ("funder", "grant", "beneficiar", "donor"),
    "service": ("bill", "rate", "hour", "retainer"),
    "creative": ("audience", "reader", "listener", "viewer", "buyer"),
    "physical": ("unit", "margin", "return", "cogs"),
}

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
PRESS_TEXT_FIELDS = ("headline", "subhead", "body", "customer_quote")


def _walk_keys(node: object):
    if isinstance(node, dict):
        for k, v in node.items():
            yield str(k)
            yield from _walk_keys(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk_keys(v)


def _faq_ok(errs: list[str], rec: dict, key: str, rule: str) -> list[dict]:
    items = rec.get(key)
    if not isinstance(items, list) or len(items) < 5:
        n = len(items) if isinstance(items, list) else 0
        errs.append(f"{key} needs >=5 question/answer items, got {n} ({rule})")
        return []
    good = []
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not item.get("q") or not item.get("a"):
            errs.append(f"{key}[{i}] must be a mapping with non-empty q and a ({rule})")
        else:
            good.append(item)
    return good


def violations(rec: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(rec, dict):
        return ["record root must be a mapping"]

    for key in BASE_KEYS:
        if key not in rec or not str(rec.get(key) or "").strip():
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    # r7 — no numeric score under any name, anywhere in the record.
    for k in _walk_keys(rec):
        low = k.lower()
        if any(tok in low for tok in BANNED_KEY_TOKENS):
            errs.append(
                f"key {k!r} emits a number where a judgement is required; "
                "remove it (r7-judgement-not-score)"
            )

    ctype = str(rec["concept_type"]).strip()
    if ctype not in CONCEPT_TYPES:
        errs.append(f"concept_type {ctype!r} not in {sorted(CONCEPT_TYPES)} (r6-concept-type-switch)")
    verdict = str(rec["verdict"]).strip()
    if verdict not in VERDICTS:
        errs.append(f"verdict {verdict!r} not in {sorted(VERDICTS)} (r7-judgement-not-score)")

    # r1 — a customer specific enough to point at, and dated evidence.
    if len(str(rec["customer"]).strip()) < 12:
        errs.append("customer must be specific enough to point at a person (r1-named-customer-dated-problem)")
    evidence = str(rec["problem_evidence"]).strip()
    if len(evidence) < 40:
        errs.append("problem_evidence must be >=40 chars of observation (r1-named-customer-dated-problem)")
    if not YEAR_RE.search(evidence):
        errs.append("problem_evidence must state when it was observed (four-digit year) (r1-named-customer-dated-problem)")
    if len(str(rec["verdict_rationale"]).strip()) < 40:
        errs.append("verdict_rationale must be >=40 chars of prose (r7-judgement-not-score)")

    # r7 — the early stop. A kill completes the record at its phase.
    if verdict == "kill":
        phase = rec.get("killed_at_phase")
        if phase not in (1, 2, 3, 4, 5):
            errs.append("verdict 'kill' requires killed_at_phase in 1..5 (r7-judgement-not-score)")
            return errs
        leaked = [
            k for p, keys in PHASE_KEYS.items() if p > int(phase)
            for k in keys if k in rec
        ]
        if leaked:
            errs.append(
                f"killed at phase {phase} so the record MUST stop there; remove: "
                + ", ".join(sorted(leaked))
                + " (r7-judgement-not-score)"
            )
        return errs

    if verdict == "revise":
        target = rec.get("revise_target_phase")
        if target not in (1, 2, 3, 4):
            errs.append(
                "verdict 'revise' requires revise_target_phase in 1..4; "
                "a revise pointing at phase 5 is a kill in disguise (r7-judgement-not-score)"
            )

    # Phases 2-5 are all required once the verdict is not a kill.
    for keys in PHASE_KEYS.values():
        for k in keys:
            if k not in rec:
                errs.append(f"missing required key for a non-kill verdict: {k}")
    if errs:
        return errs

    # r2 / r3 — the press release.
    pr = rec["press_release"]
    if not isinstance(pr, dict):
        errs.append("press_release must be a mapping (r2-launched-past-tense)")
    else:
        for f in ("headline", "subhead", "body", "customer_quote", "available_from"):
            if not str(pr.get(f) or "").strip():
                errs.append(f"press_release.{f} is required (r2-launched-past-tense)")
        for f in PRESS_TEXT_FIELDS:
            text = str(pr.get(f) or "").lower()
            for pat in FUTURE_PATTERNS:
                if re.search(pat, text):
                    errs.append(
                        f"press_release.{f} uses forward-looking language matching {pat!r}; "
                        "the announcement is written as already shipped (r2-launched-past-tense)"
                    )
                    break
        head = (str(pr.get("headline") or "") + " " + str(pr.get("subhead") or "")).lower()
        for noun in IMPL_NOUNS:
            if noun in head:
                errs.append(
                    f"headline/subhead names the implementation ({noun.strip()!r}); "
                    "say what the customer can now do (r3-solution-vocabulary-banned-from-the-headline)"
                )
                break

    # r4 / r5 — two separate banks.
    cust = _faq_ok(errs, rec, "customer_faq", "r4-customer-faq-is-objections")
    intl = _faq_ok(errs, rec, "internal_faq", "r5-internal-faq-must-hurt")
    joined = " ".join(str(i.get("q", "")).lower() for i in cust)
    if cust and not any(t in joined for t in ("cost", "price", "pay", "charge")):
        errs.append("customer_faq must include what it costs them (r4-customer-faq-is-objections)")
    if cust and not any(t in joined for t in ("instead of", "why not", "already use", "today")):
        errs.append("customer_faq must name the incumbent they use today (r4-customer-faq-is-objections)")
    shared = {str(i.get("q", "")).strip().lower() for i in cust} & {
        str(i.get("q", "")).strip().lower() for i in intl
    }
    if shared:
        errs.append(
            "customer_faq and internal_faq share a question verbatim; they are separate "
            "banks with different audiences (r5-internal-faq-must-hurt)"
        )

    # r5 — kill-assumptions and their falsification.
    mbt = rec["must_be_true"]
    if not isinstance(mbt, list) or not mbt:
        errs.append("must_be_true must list >=1 kill-assumption (r5-internal-faq-must-hurt)")
    else:
        for i, a in enumerate(mbt):
            if not isinstance(a, dict) or not a.get("assumption"):
                errs.append(f"must_be_true[{i}] needs an assumption (r5-internal-faq-must-hurt)")
                continue
            status = str(a.get("status") or "").strip()
            if status not in ("confirmed", "untested"):
                errs.append(f"must_be_true[{i}].status must be confirmed|untested (r5-internal-faq-must-hurt)")
            if verdict == "proceed" and status != "confirmed" and not str(a.get("disproof") or "").strip():
                errs.append(
                    f"must_be_true[{i}] is untested with no disproof but the verdict is proceed; "
                    "the build would be the test (r7-judgement-not-score)"
                )
    if len(str(rec["cheapest_disproof"]).strip()) < 12:
        errs.append("cheapest_disproof must name an act performable this week (r5-internal-faq-must-hurt)")

    # r6 — the success measure must name the antagonist the concept_type implies.
    measure = str(rec["success_measure"]).strip().lower()
    if len(measure) < 12:
        errs.append("success_measure must be >=12 chars (r6-concept-type-switch)")
    tokens = ANTAGONIST_TOKENS.get(ctype, ())
    if tokens and not any(t in measure for t in tokens):
        errs.append(
            f"concept_type '{ctype}' means the party who can kill this is named by one of "
            f"{list(tokens)}; success_measure names none of them (r6-concept-type-switch)"
        )

    return errs


def load(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        if yaml is None:
            print("PyYAML required for YAML records; install pyyaml or pass JSON", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(raw)
    return json.loads(raw)


def _ok_full() -> dict:
    return {
        "concept": "one-command month-end close for solo bookkeepers",
        "concept_type": "commercial",
        "customer": "solo bookkeepers with 8-20 recurring clients",
        "problem": "closing a client month means reconciling three exports by hand",
        "problem_evidence": "Observed in five calls during March 2026; four had built a spreadsheet macro for it.",
        "press_release": {
            "headline": "Solo bookkeepers now close a client month in one afternoon",
            "subhead": "Three hand-matched exports became one review pass.",
            "body": "As of today they import once, review the exceptions, and sign off.",
            "customer_quote": "I stopped turning clients away in the first week of the month.",
            "available_from": "2026-09-01",
        },
        "customer_faq": [
            {"q": "What does it cost me?", "a": "29 EUR/month per seat."},
            {"q": "Why not keep the bank-feed tool I use today?", "a": "It solves one export of three."},
            {"q": "What happens to my data if I leave?", "a": "Full CSV export on demand."},
            {"q": "Do my clients have to do anything?", "a": "No."},
            {"q": "What if a match is wrong?", "a": "Every match is reversible before sign-off."},
        ],
        "internal_faq": [
            {"q": "Why has nobody built this?", "a": "Two have, both priced per-client."},
            {"q": "Honest reason they would not switch?", "a": "They trust their own spreadsheet."},
            {"q": "What when a bank changes its export format?", "a": "We eat it; ongoing cost."},
            {"q": "Who loses if this works?", "a": "Nobody internally, so nobody checks us."},
            {"q": "What kills this in six months?", "a": "Under one in five trials closing a real month."},
        ],
        "must_be_true": [
            {
                "assumption": "a bookkeeper will hand a stranger's tool their client bank exports",
                "status": "untested",
                "disproof": "offer ten a free manual close and count who sends exports",
            },
        ],
        "cheapest_disproof": "offer ten bookkeepers a free manual close and count who sends exports",
        "success_measure": "ten bookkeepers pay the 29 EUR price with no discount offered",
        "verdict": "proceed",
        "verdict_rationale": (
            "Customer nameable, problem dated and already paid for badly, and the one "
            "untested kill-assumption has a week-long disproof rather than a build."
        ),
    }


def _ok_kill() -> dict:
    return {
        "concept": "an AI assistant that summarises your team's Slack every morning",
        "concept_type": "commercial",
        "customer": "nobody nameable after three attempts",
        "problem": "people feel they miss things in Slack",
        "problem_evidence": "Two exchanges on 2026-08-04; no workaround, no competitor paid for, no dated thread.",
        "verdict": "kill",
        "killed_at_phase": 1,
        "verdict_rationale": (
            "No nameable customer and no dated observation, so every later phase would "
            "have been written against a placeholder. Killed at the cost of one phase."
        ),
    }


def self_test() -> int:
    kill_leak = dict(_ok_kill(), success_measure="ten people pay for it")

    scored = _ok_full()
    scored["confidence_score"] = 7.5

    future = _ok_full()
    future["press_release"] = dict(future["press_release"], body="This will streamline the close.")

    thin_faq = _ok_full()
    thin_faq["internal_faq"] = thin_faq["internal_faq"][:3]

    wrong_measure = dict(_ok_full(), success_measure="the team feels much happier about closes")

    untested = _ok_full()
    untested["must_be_true"] = [{"assumption": "they will hand over exports", "status": "untested", "disproof": ""}]

    undated = dict(_ok_full(), problem_evidence="Observed in five calls; four had built a spreadsheet macro for it.")

    impl_headline = _ok_full()
    impl_headline["press_release"] = dict(
        impl_headline["press_release"], headline="An AI-powered reconciliation engine for bookkeepers"
    )

    cases = [
        ("full valid proceed record", _ok_full(), 0),
        ("kill at phase 1", _ok_kill(), 0),
        ("kill with later phase leaked", kill_leak, 1),
        ("numeric score field present", scored, 1),
        ("press release in future tense", future, 1),
        ("internal FAQ under five questions", thin_faq, 1),
        ("commercial measure names no payer", wrong_measure, 1),
        ("proceed on untested assumption with no disproof", untested, 1),
        ("problem_evidence carries no date", undated, 1),
        ("headline names the implementation", impl_headline, 1),
    ]
    failed = 0
    for name, doc, expect in cases:
        errs = violations(doc)
        got = 1 if errs else 0
        if got != expect:
            failed += 1
        status = "ok " if got == expect else "FAIL"
        print(f"[{status}] {name}" + (f" -> {errs[0]}" if errs else ""))
    print(f"\n{len(cases) - failed}/{len(cases)} self-tests passed")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[1] == "--self-test":
        return self_test()
    path = Path(argv[1])
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    errs = violations(load(path))
    if not errs:
        print(f"OK  {path}")
        return 0
    print(f"FAIL  {path}", file=sys.stderr)
    for e in errs:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
