"""
spatial-spec-linter.py — validate a JSON spatial UX spec against field-zone rules.

Usage: python spatial-spec-linter.py spec.json
Exit code: 0 = clean, 1 = violations found

Expected JSON format:
{
  "elements": [
    {
      "id": "primary-menu",
      "field": "near",
      "distance_m": 0.8,
      "interactive": true,
      "text": false,
      "font_pt": null
    }
  ]
}
"""
import json
import sys

NEAR_MIN, NEAR_MAX = 0.30, 1.00
MID_MIN,  MID_MAX  = 1.00, 3.00
FAR_MIN            = 3.00

FAR_TEXT_MIN_PT = 60
MID_TEXT_MIN_PT = 36


def lint(spec: dict) -> list:
    issues = []
    for el in spec.get("elements", []):
        eid = el.get("id", "?")
        d = el.get("distance_m")
        field = el.get("field")

        if d is None or field is None:
            issues.append(f"{eid}: missing distance_m or field")
            continue

        # Distance vs field consistency
        if field == "near" and not (NEAR_MIN <= d <= NEAR_MAX):
            issues.append(f"{eid}: near field expects {NEAR_MIN}-{NEAR_MAX}m, got {d}m")
        elif field == "mid" and not (MID_MIN < d <= MID_MAX):
            issues.append(f"{eid}: mid field expects {MID_MIN}-{MID_MAX}m, got {d}m")
        elif field == "far" and d < FAR_MIN:
            issues.append(f"{eid}: far field expects >{FAR_MIN}m, got {d}m")

        # Interactive in far field is unreachable
        if el.get("interactive") and field == "far":
            issues.append(f"{eid}: interactive element in far field (unreachable by hand-ray)")

        # Text legibility by distance
        if el.get("text"):
            font_pt = el.get("font_pt", 0)
            if d > FAR_MIN and font_pt < FAR_TEXT_MIN_PT:
                issues.append(f"{eid}: text at {d}m needs >={FAR_TEXT_MIN_PT}pt, got {font_pt}pt")
            elif MID_MIN < d <= FAR_MIN and font_pt < MID_TEXT_MIN_PT:
                issues.append(f"{eid}: text at {d}m needs >={MID_TEXT_MIN_PT}pt, got {font_pt}pt")

        # Critical content too close (inside 0.3m causes discomfort)
        if d < NEAR_MIN:
            issues.append(f"{eid}: content at {d}m is inside minimum comfortable distance (0.3m)")

    return issues


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)

    spec = json.load(open(sys.argv[1]))
    issues = lint(spec)
    for issue in issues:
        print(issue)
    sys.exit(1 if issues else 0)
