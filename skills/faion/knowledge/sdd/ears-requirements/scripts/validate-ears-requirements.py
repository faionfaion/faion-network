#!/usr/bin/env python3
"""Lint EARS requirement statements and validate an EARS requirement-set artefact.

Dev-time only. The shipping runtime is Go (faion-cli internal/earslint); this
script and that package load the SAME grammar file, templates/ears-rules.json,
and both MUST reproduce templates/ears-fixtures.tsv exactly.

Usage:
  validate-ears-requirements.py <file.json>     validate a requirement-set artefact
  validate-ears-requirements.py <file.md>       lint requirement lines in Markdown
  validate-ears-requirements.py --self-test     replay every fixture
  validate-ears-requirements.py --help

Options:
  --strict    E-codes fail the run; E010 is promoted to error
  --lenient   accept a bare space before the actor (Kiro-style comma-less input)
  --json      machine-readable output

Exit codes: 0 ok (or warnings only), 1 violations, 2 usage/IO failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULES_PATH = HERE.parent / "templates" / "ears-rules.json"
FIXTURES_PATH = HERE.parent / "templates" / "ears-fixtures.tsv"

PATTERN_ENUM = {
    "ubiquitous",
    "state-driven",
    "event-driven",
    "optional-feature",
    "unwanted-behaviour",
    "complex",
    "n-a",
}

FOLD = {
    "‘": "'", "’": "'",
    "“": '"', "”": '"',
    "–": "-", "—": "-",
    " ": " ", "…": "...",
}


def load_rules() -> dict:
    try:
        return json.loads(RULES_PATH.read_text(encoding="utf-8"))
    except OSError as exc:  # pragma: no cover - environment failure
        raise SystemExit(f"cannot read {RULES_PATH}: {exc}") from exc


RULES = load_rules()
RX = {k: re.compile(v) for k, v in RULES["regex"].items()}
RANK = RULES["clause_order"]["ranks"]


# --------------------------------------------------------------------------
# Stage 1 — normalize
# --------------------------------------------------------------------------
def normalize(line: str) -> str:
    s = line
    for bad, good in FOLD.items():
        s = s.replace(bad, good)
    s = RX["list_marker"].sub("", s)
    s = RX["req_id"].sub("", s)
    return RX["whitespace"].sub(" ", s.strip())


# --------------------------------------------------------------------------
# Stage 2 — head-marker split (LAST match wins)
# --------------------------------------------------------------------------
class Split:
    __slots__ = ("ok", "prefix", "has_then", "system", "modal", "response")

    def __init__(self) -> None:
        self.ok = False
        self.prefix = ""
        self.has_then = False
        self.system = ""
        self.modal = ""
        self.response = ""


def split_line(s: str, lenient: bool = False) -> Split:
    rx = RX["head_lenient"] if lenient else RX["head_strict"]
    matches = list(rx.finditer(s))
    sp = Split()
    if not matches:
        return sp
    m = matches[-1]
    sp.ok = True
    sp.prefix = s[: m.start()].strip().rstrip(",").strip()
    sp.has_then = m.group(1) is not None
    sp.system = m.group(2).strip()
    sp.modal = m.group(3).strip().lower()
    resp = s[m.end():].strip()
    if resp.endswith("."):
        resp = resp[:-1].rstrip()
    sp.response = resp
    return sp


# --------------------------------------------------------------------------
# Stage 3a — clause parsing and classification
# --------------------------------------------------------------------------
def parse_clauses(prefix: str) -> tuple[list[tuple[str, str]], list[str]]:
    clauses: list[tuple[str, str]] = []
    errs: list[str] = []
    if not prefix.strip():
        return clauses, errs
    for seg in prefix.split(","):
        seg = seg.strip()
        if not seg:
            continue
        m = RX["clause_keyword"].match(seg)
        if m is None:
            errs.append("E004")
            continue
        clauses.append((m.group(1).lower(), m.group(2).strip()))
    return clauses, errs


def classify(clauses: list[tuple[str, str]], has_then: bool) -> tuple[str, list[str]]:
    errs: list[str] = []
    last = -1
    for kw, _ in clauses:
        r = RANK[kw]
        if r < last:
            errs.append("E005")
        last = max(last, r)

    counts: dict[str, int] = {}
    for kw, _ in clauses:
        key = "while" if kw == "during" else kw
        counts[key] = counts.get(key, 0) + 1
    for key in ("where", "when", "if"):
        if counts.get(key, 0) > 1:
            errs.append("E007")
    if counts.get("if", 0) > 0 and not has_then:
        errs.append("E006")
    if counts.get("if", 0) == 0 and has_then:
        errs.append("E006")

    if errs:
        return "invalid", errs
    if not clauses:
        return "ubiquitous", errs
    if len(clauses) > 1:
        return "complex", errs
    kw = clauses[0][0]
    return {
        "when": "event-driven",
        "while": "state-driven",
        "during": "state-driven",
        "where": "optional-feature",
        "if": "unwanted-behaviour",
    }[kw], errs


# --------------------------------------------------------------------------
# Stage 3b — lint
# --------------------------------------------------------------------------
SEVERITY = {r["code"]: r["severity"] for r in RULES["rules"]}


def _is_error(code: str) -> bool:
    """Default-mode severity. E010 is a warning until --strict promotes it."""
    return SEVERITY.get(code) == "error"


def _mixed_bool(text: str) -> bool:
    return bool(
        RX["bool_and"].search(text)
        and RX["bool_or"].search(text)
        and "(" not in text
    )


def lint(line: str, lenient: bool = False) -> tuple[str, list[str]]:
    """Return (pattern, sorted unique codes) for one candidate line."""
    s = normalize(line)
    codes: list[str] = []

    n_shall = len(RX["shall"].findall(s))
    if n_shall > 1:
        # E002 short-circuits: a bundled statement must be split before it can
        # be meaningfully classified, and further findings would be noise.
        return "invalid", ["E002"]

    sp = split_line(s, lenient)
    if not sp.ok:
        codes.append("E003")
    if n_shall == 0:
        codes.append("E001")
        if sp.ok and RX["weak_modal"].match(sp.modal):
            codes.append("E008")

    clauses, clause_errs = parse_clauses(sp.prefix) if sp.ok else ([], [])
    codes.extend(clause_errs)
    pattern, class_errs = classify(clauses, sp.has_then)
    codes.extend(class_errs)

    # A condition keyword sitting after the actor is an ordering violation.
    trailing_cond = None
    if sp.ok:
        m = re.search(r"(?i)\b(if|while|where)\b", sp.response)
        if m:
            codes.append("E005")
            trailing_cond = sp.response[m.start():]
            pattern = "invalid"

    # E009 — mixed and/or without parentheses, over every condition region.
    for _, body in clauses:
        if _mixed_bool(body):
            codes.append("E009")
    if trailing_cond and _mixed_bool(trailing_cond):
        codes.append("E009")

    # E010 — sentence terminator.
    if not s.endswith("."):
        codes.append("E010")

    # Line-scope warnings.
    if RX["vague"].search(s):
        codes.append("W103")
    if RX["escape_clause"].search(s):
        codes.append("W104")
    if RX["rate"].search(s):
        codes.append("W108")

    # Clause-scope warnings.
    for kw, body in clauses:
        if kw == "if" and RX["normal_event_in_if"].search(body):
            codes.append("W106")
        if kw == "when" and RX["failure_in_when"].search(body):
            codes.append("W107")
    if len(clauses) > 3:
        codes.append("W110")

    if sp.ok:
        if RX["vague_system"].match(sp.system):
            codes.append("W111")
        resp = sp.response
        if RX["passive_response"].search(resp):
            codes.append("W101")
        if RX["and_or"].search(resp):
            codes.append("W102")
        if RX["pronoun"].search(resp):
            codes.append("W105")
        if len(resp.split()) > 30:
            codes.append("W109")
        if RX["weasel_response"].search(resp):
            codes.append("W112")
        if RX["bare_integer"].search(resp) and not RX["number_with_unit"].search(resp):
            codes.append("W114")

    has_error = any(_is_error(c) for c in codes)
    if pattern == "ubiquitous" and not has_error:
        # I113 is a prompt, not a check: most requirements are not ubiquitous.
        codes.append("I113")
    if has_error:
        pattern = "invalid"

    return pattern, sorted(set(codes))


def severity_of(code: str, strict: bool) -> str:
    if strict and code == "E010":
        return "error"
    return SEVERITY.get(code, "warn")


def message_of(code: str) -> str:
    for r in RULES["rules"]:
        if r["code"] == code:
            return r["message"]
    return "unknown rule"


# --------------------------------------------------------------------------
# Candidate-line extraction from Markdown
# --------------------------------------------------------------------------
RE_ID_LINE = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(?:FR|NFR|AC|REQ)-\d+")
RE_MODAL_LINE = re.compile(
    r"(?i)\bthe\s+[A-Za-z][A-Za-z0-9 _/.-]{1,58}?\s+"
    r"(?:shall|must|will|should|may|can|might|has to|have to|needs to|need to)\b"
)


def extract_candidates(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        if line.startswith("|"):
            # Table rows: only the statement cell is a candidate. A cell that is
            # nothing but an identifier is metadata, not a requirement.
            for cell in (c.strip() for c in line.strip("|").split("|")):
                if RE_MODAL_LINE.search(cell):
                    out.append((i, cell))
            continue
        if RE_ID_LINE.match(line) or RE_MODAL_LINE.search(line):
            out.append((i, line))
    return out


# --------------------------------------------------------------------------
# Artefact validation (content/02-output-contract.xml)
# --------------------------------------------------------------------------
def validate_artefact(doc: dict) -> list[str]:
    errs: list[str] = []
    for key in ("artefact_id", "version", "last_reviewed", "requirements",
                "ears_violations", "owner"):
        if key not in doc:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(doc["version"])):
        errs.append(f"version {doc['version']!r} is not semver")
    if str(doc["owner"]).strip().lower() in ("", "team", "we", "none"):
        errs.append("owner must be a person, not 'team' / 'we' (f6)")
    reqs = doc["requirements"]
    if not isinstance(reqs, list) or not reqs:
        errs.append("requirements must be a non-empty list")
        return errs

    declared = {}
    for v in doc.get("ears_violations") or []:
        if isinstance(v, dict) and v.get("id") and v.get("code"):
            declared.setdefault(v["id"], set()).add(v["code"])

    for i, r in enumerate(reqs):
        if not isinstance(r, dict):
            errs.append(f"requirements[{i}] must be an object")
            continue
        rid = str(r.get("id", ""))
        if not re.fullmatch(r"(FR|NFR)-\d{3}", rid):
            errs.append(f"requirements[{i}] id {rid!r} must match (FR|NFR)-NNN (f1)")
            continue
        if not str(r.get("verification_method", "")).strip():
            errs.append(f"{rid}: verification_method is required (f2)")
        pat = r.get("ears_pattern")
        if pat not in PATTERN_ENUM:
            errs.append(f"{rid}: ears_pattern {pat!r} not in the enum")
            continue
        if pat == "n-a":
            if rid.startswith("FR-"):
                errs.append(f"{rid}: an FR may not opt out of EARS (f3)")
            if len(str(r.get("ears_pattern_na_reason", "")).strip()) < 12:
                errs.append(f"{rid}: ears_pattern: n-a requires ears_pattern_na_reason (f4)")
            continue
        derived, codes = lint(str(r.get("statement", "")))
        if derived != pat:
            errs.append(
                f"{rid}: ears_pattern is {pat!r} but the statement parses as "
                f"{derived!r} — stale artefact, not an override"
            )
        e_codes = {c for c in codes if _is_error(c)}
        if e_codes and rid.startswith("FR-"):
            missing = e_codes - declared.get(rid, set())
            errs.append(
                f"{rid}: statement emits {sorted(e_codes)} in a final artefact (f5)"
                + (f"; not declared in ears_violations: {sorted(missing)}" if missing else "")
            )
    return errs


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------
def read_fixtures() -> list[tuple[str, str, list[str], str]]:
    rows: list[tuple[str, str, list[str], str]] = []
    for raw in FIXTURES_PATH.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 4:
            raise SystemExit(f"fixture row must have 4 tab-separated columns: {raw!r}")
        line, pattern, codes, mode = parts
        wanted = [] if codes.strip() == "-" else [c.strip() for c in codes.split(",")]
        rows.append((line, pattern.strip(), sorted(wanted), mode.strip()))
    return rows


def self_test() -> int:
    failed = 0
    rows = read_fixtures()
    for line, want_pattern, want_codes, mode in rows:
        got_pattern, got_codes = lint(line, lenient=(mode == "lenient"))
        ok = got_pattern == want_pattern and got_codes == want_codes
        if not ok:
            failed += 1
            print(f"[FAIL] {line}")
            print(f"       pattern want={want_pattern} got={got_pattern}")
            print(f"       codes   want={want_codes} got={got_codes}")
        else:
            print(f"[ok  ] {want_pattern:<18} {','.join(want_codes) or '-':<28} {line[:64]}")

    # Every rule in the table must be exercised by at least one fixture.
    exercised = {c for _, _, cs, _ in rows for c in cs}
    declared = {r["code"] for r in RULES["rules"]}
    unexercised = sorted(declared - exercised)
    if unexercised:
        failed += 1
        print(f"[FAIL] rules declared in ears-rules.json but never exercised: {unexercised}")

    # Contract self-tests.
    good = {
        "artefact_id": "t", "version": "1.0.0", "last_reviewed": "2026-08-04",
        "owner": "@solo-founder", "ears_violations": [],
        "requirements": [
            {"id": "FR-001",
             "statement": "When a customer submits the checkout form, the payment service shall create a charge intent.",
             "ears_pattern": "event-driven", "priority": "must",
             "verification_method": "integration test"},
            {"id": "NFR-002",
             "statement": "The payment integration is isolated behind a single adapter module.",
             "ears_pattern": "n-a",
             "ears_pattern_na_reason": "architectural constraint, not a system response",
             "priority": "should", "verification_method": "architecture test"},
        ],
    }
    fr_opt_out = json.loads(json.dumps(good))
    fr_opt_out["requirements"][0] = {
        "id": "FR-002", "statement": "The app should be fast.", "ears_pattern": "n-a",
        "ears_pattern_na_reason": "we could not phrase it", "priority": "must",
        "verification_method": "manual",
    }
    stale = json.loads(json.dumps(good))
    stale["requirements"][0]["ears_pattern"] = "ubiquitous"
    no_reason = json.loads(json.dumps(good))
    del no_reason["requirements"][1]["ears_pattern_na_reason"]
    bad_owner = json.loads(json.dumps(good))
    bad_owner["owner"] = "team"

    cases = [
        ("valid artefact", good, 0),
        ("FR opting out of EARS (f3)", fr_opt_out, 1),
        ("recorded pattern disagrees with the parser", stale, 1),
        ("n-a without a reason (f4)", no_reason, 1),
        ("owner is 'team' (f6)", bad_owner, 1),
    ]
    for name, doc, expect in cases:
        errs = validate_artefact(doc)
        got = 1 if errs else 0
        if got != expect:
            failed += 1
            print(f"[FAIL] {name} -> {errs}")
        else:
            print(f"[ok  ] contract: {name}")

    total = len(rows) + len(cases) + 1
    print(f"\n{total - failed}/{total} self-tests passed")
    return 1 if failed else 0


# --------------------------------------------------------------------------
def main(argv: list[str]) -> int:
    args = [a for a in argv[1:]]
    if not args or "-h" in args or "--help" in args:
        print(__doc__)
        return 2
    strict = "--strict" in args
    lenient = "--lenient" in args
    as_json = "--json" in args
    positional = [a for a in args if not a.startswith("-")]

    if "--self-test" in args:
        return self_test()
    if len(positional) != 1:
        print(__doc__)
        return 2

    path = Path(positional[0])
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return 2

    if path.suffix == ".json":
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"{path}: invalid JSON: {exc}", file=sys.stderr)
            return 2
        errs = validate_artefact(doc)
        if as_json:
            print(json.dumps({"path": str(path), "violations": errs}, indent=2))
        elif errs:
            print(f"FAIL  {path}", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
        else:
            print(f"OK  {path}")
        return 1 if errs else 0

    findings = []
    for lineno, cand in extract_candidates(path.read_text(encoding="utf-8")):
        pattern, codes = lint(cand, lenient=lenient)
        for code in codes:
            findings.append({
                "line": lineno, "code": code, "pattern": pattern,
                "severity": severity_of(code, strict), "message": message_of(code),
                "text": cand,
            })
    if as_json:
        print(json.dumps({"path": str(path), "findings": findings}, indent=2))
    else:
        for f in findings:
            print(f"{path}:{f['line']}:1  {f['severity']}  {f['code']}  {f['message']}")
        if not findings:
            print(f"OK  {path}")
    if strict and any(f["severity"] == "error" for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
