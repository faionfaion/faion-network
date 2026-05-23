#!/usr/bin/env python3
"""validate-video-generation-prompt-engineering.py — validate prompt-template.yaml.

Inputs: --file PATH | --self-test | --help
Exit:   0 valid, 1 invalid, 2 usage
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["provider", "sasscl", "provider_overlay", "max_chars", "eval", "brand_locks"]
SASSCL_FIELDS = {"subject_slot", "action_slot", "setting", "style", "camera", "lighting"}
PROVIDER_CAPS = {"runway": 500, "luma": 1500, "veo": 2000, "sora": 4000, "kling": 2500}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    sasscl = obj.get("sasscl", {})
    if isinstance(sasscl, dict):
        missing = SASSCL_FIELDS - set(sasscl.keys())
        if missing:
            errs.append(f"sasscl missing fields {sorted(missing)} (r1-sasscl-formula)")
    if not obj.get("provider_overlay"):
        errs.append("provider_overlay required (r2-provider-quirk-overlay)")
    prov = obj.get("provider")
    cap = PROVIDER_CAPS.get(prov, 4000)
    if obj.get("max_chars", 0) > cap:
        errs.append(f"max_chars exceeds {prov} cap {cap} (r4-max-prompt-length)")
    ev = obj.get("eval", {})
    if isinstance(ev, dict):
        if ev.get("sample_size", 0) < 5:
            errs.append("eval.sample_size must be >=5 (r3-five-gen-eval-gate)")
        if ev.get("promotion_threshold", 0) < 0.8:
            errs.append("eval.promotion_threshold must be >=0.8 (r3-five-gen-eval-gate)")
    locks = set(obj.get("brand_locks", []))
    if not {"style", "camera", "lighting"} <= locks:
        errs.append("brand_locks must include style + camera + lighting (r5-brand-style-locked)")
    return errs


FIXTURE_VALID = """
provider: runway
provider_overlay: "tracking shot"
max_chars: 480
sasscl:
  subject_slot: x
  action_slot: y
  setting: z
  style: a
  camera: b
  lighting: c
eval: {rubric_path: r, sample_size: 5, promotion_threshold: 0.8}
brand_locks: [style, camera, lighting]
"""

FIXTURE_INVALID = """
provider: runway
provider_overlay: ""
max_chars: 5000
sasscl: {subject_slot: x}
eval: {rubric_path: r, sample_size: 1, promotion_threshold: 0.5}
brand_locks: []
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n"); return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n"); return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(prog="validate-video-generation-prompt-engineering", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n"); return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
