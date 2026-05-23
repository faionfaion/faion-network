#!/usr/bin/env python3
"""validate-rag-feature-acceptance-contract.py — validate acceptance-contract.yaml.

Inputs:
    --file PATH    YAML file to validate
    --self-test    Run against built-in fixture
    --help         Show this message

Exit codes:
    0  valid
    1  invalid (violations printed to stderr)
    2  usage error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SIG_RE = re.compile(r".+@.+ \d{4}-\d{2}-\d{2} .+")
FORBIDDEN_METRIC_NAMES = {"bleu", "rouge", "rouge_l", "meteor"}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a YAML object"]
    for k in ("feature", "version", "intents", "signatures", "recontract_triggers"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must match semver X.Y.Z")
    intents = obj.get("intents", {})
    if not isinstance(intents, dict) or len(intents) < 2:
        errs.append("intents must be an object with >= 2 entries (r1-per-intent-decomposition)")
    else:
        for name, intent in intents.items():
            if not isinstance(intent, dict):
                errs.append(f"intents.{name} must be object"); continue
            for k in ("pm_outcome", "acceptable_failure", "sme_rubric", "offline", "online"):
                if k not in intent:
                    errs.append(f"intents.{name}.{k} missing")
            offline = intent.get("offline", {})
            online = intent.get("online", {})
            if isinstance(offline, dict):
                for m in offline:
                    if m.lower() in FORBIDDEN_METRIC_NAMES:
                        errs.append(f"intents.{name}.offline.{m}: vanity metric forbidden as primary gate (fm-01)")
            if isinstance(offline, dict) and isinstance(online, dict):
                if not online:
                    errs.append(f"intents.{name}: offline-only contract forbidden (r3-offline-paired-with-online)")
            rubric = intent.get("sme_rubric", {})
            if isinstance(rubric, dict):
                for k in ("pass", "fail"):
                    if k not in rubric:
                        errs.append(f"intents.{name}.sme_rubric.{k} missing")
    sigs = obj.get("signatures", {})
    if not isinstance(sigs, dict):
        errs.append("signatures must be object")
    else:
        for role in ("pm", "sme", "ml_engineer"):
            v = sigs.get(role)
            if not v:
                errs.append(f"signatures.{role} missing (r2-three-signatures)")
            elif not SIG_RE.match(str(v)):
                errs.append(f"signatures.{role} must be 'email YYYY-MM-DD version'")
    triggers = obj.get("recontract_triggers", [])
    if not isinstance(triggers, list) or len(triggers) < 2:
        errs.append("recontract_triggers must be a list of >= 2 entries (r5-recontract-trigger)")
    return errs


FIXTURE_VALID = """
feature: example-rag
version: 1.0.0
intents:
  policy-lookup:
    pm_outcome: "Resolve policy questions without escalation"
    acceptable_failure: "Refusal acceptable; hallucination not"
    sme_rubric: {pass: "Cites correct section verbatim", fail: "No citation or wrong"}
    offline:
      faithfulness: {threshold: ">= 0.90", baseline: "junior 0.92"}
      context-precision: {threshold: ">= 0.80", baseline: "prod 0.75"}
    online:
      thumbs-down-rate: {threshold: "<= 5%", baseline: "today 9%"}
  troubleshooting:
    pm_outcome: "Walk user through fix"
    acceptable_failure: "Safe-wrong ok; destructive not"
    sme_rubric: {pass: "Correct order; no destructive first", fail: "Destructive without backup"}
    offline:
      answer-relevance: {threshold: ">= 0.80", baseline: "prompt 0.71"}
      destructive-step-detector: {threshold: "== 0", baseline: "hard zero"}
    online:
      follow-up-rephrase-rate: {threshold: "<= 20%", baseline: "today 31%"}
signatures:
  pm: "alice@example.com 2026-05-22 v1.0"
  sme: "ravi@example.com 2026-05-22 v1.0"
  ml_engineer: "jonas@example.com 2026-05-22 v1.0"
recontract_triggers:
  - "intent distribution chi2 p < 0.01"
  - "embedding model upgrade"
"""

FIXTURE_INVALID = """
feature: bad
version: 1
intents:
  only-one:
    pm_outcome: short
    acceptable_failure: short
    sme_rubric: {pass: x, fail: y}
    offline:
      bleu: {threshold: ">= 0.4", baseline: "vibes"}
    online: {}
signatures:
  pm: "team-lead"
recontract_triggers: []
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required for --self-test\n")
        return 2
    valid = yaml.safe_load(FIXTURE_VALID)
    invalid = yaml.safe_load(FIXTURE_INVALID)
    errs_v = validate(valid)
    if errs_v:
        sys.stderr.write("valid fixture rejected:\n" + "\n".join(errs_v) + "\n")
        return 1
    errs_i = validate(invalid)
    if not errs_i:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write(f"self-test OK ({len(errs_i)} violations on invalid fixture)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required for YAML input")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-rag-feature-acceptance-contract",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="YAML or JSON file to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixture")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
