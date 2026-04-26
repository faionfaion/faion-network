#!/usr/bin/env python3
"""
xr-scene-audit.py <manifest.json>
Audits a spatial scene manifest for XAUR accessibility requirements.
Expected manifest schema: {"interactables": [{id, voice_alias, gaze_supported,
  controller_button, description, seated_compatible}, ...]}
Exit code: 0 = all pass, 1 = failures found.
"""
import json
import sys

REQUIRED_FIELDS = [
    "voice_alias",
    "gaze_supported",
    "controller_button",
    "description",
    "seated_compatible",
]

DESCRIPTION_MAX_CHARS = 80

def audit(manifest_path: str) -> list[dict]:
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    failures = []
    for obj in manifest.get("interactables", []):
        obj_id = obj.get("id", "<unknown>")
        missing = [k for k in REQUIRED_FIELDS if not obj.get(k)]
        issues = list(missing)

        # Description length check
        desc = obj.get("description", "")
        if desc and len(desc) > DESCRIPTION_MAX_CHARS:
            issues.append(f"description too long ({len(desc)} > {DESCRIPTION_MAX_CHARS} chars)")

        if issues:
            failures.append({"id": obj_id, "issues": issues})

    return failures

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: xr-scene-audit.py <manifest.json>", file=sys.stderr)
        sys.exit(2)

    failures = audit(sys.argv[1])

    try:
        with open(sys.argv[1]) as f:
            manifest = json.load(f)
        total = len(manifest.get("interactables", []))
    except Exception:
        total = 0

    result = {
        "total": total,
        "failed": len(failures),
        "passed": total - len(failures),
        "details": failures,
    }
    print(json.dumps(result, indent=2))

    if failures:
        print(f"\nFAIL: {len(failures)}/{total} interactable objects have accessibility gaps.", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\nOK: All {total} interactable objects pass XAUR requirements.")
