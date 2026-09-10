#!/usr/bin/env python3
# purpose: Stdlib helper to scan a scene JSON for reach-zone + occlusion violations.
# consumes: see content/02-output-contract.xml inputs for spatial-accessibility
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-600 tokens when loaded as context

"""Audit an XR scene export against the five spatial-accessibility rules.

Usage:
    xr-scene-audit.py scene.json [--owner @handle] [--out spatial-accessibility-record.json]

Scene JSON (metres, origin at the user's floor point, +y up, +z forward; zones use x/z distance):
{
  "experience": "workshop-vr", "platforms": ["Quest"], "session_pose": ["seated", "standing"],
  "panels": [{"id": "hud", "critical": true, "height_mode": "calibrated",
              "position": {"x": 0, "y": 1.2, "z": 0.5}, "occludes": ["<panel-id>"],
              "seated_position": {"x": 0, "y": 0.9, "z": 0.5}}],
  "events": [{"id": "alarm", "critical": true, "audio": {"spatial": true, "direction_matches_visual": true}}],
  "interactions": [{"id": "reach-shelf", "pose": "standing", "seated_alternate": "<interaction-id>"}]
}
Exit 1 on any failing rule (procedure step 2 decision-gate: fixed Y positions STOP the audit).
"""
import argparse
import datetime
import json
import math
import sys

ZONES = (("near", 0.3, 0.6), ("mid", 0.6, 1.2), ("far", 1.2, math.inf))  # rule reach-zones-pinned
# Comfortable hand-reach height bands for the 1.4-2.0 m user range (rule height-variability).
REACH_Y = {"seated": (0.5, 1.3), "standing": (0.8, 1.8)}


def zone(pos: dict) -> str:
    """Horizontal distance from the user's vertical axis; height is judged separately by REACH_Y."""
    d = math.hypot(pos["x"], pos["z"])
    return next((name for name, lo, hi in ZONES if lo <= d < hi), "too-close")


def reachable(pos: dict, pose: str) -> bool:
    lo, hi = REACH_Y[pose]
    return zone(pos) in ("near", "mid") and lo <= pos["y"] <= hi


def audit(scene: dict) -> list[dict]:
    poses = scene.get("session_pose", ["seated", "standing"])
    panels = scene.get("panels", [])
    critical = {p["id"] for p in panels if p.get("critical")}
    bad = {r: [] for r in ("reach-zones-pinned", "height-variability", "occlusion-budget",
                           "spatial-audio-directional", "seated-alternate-required")}

    for p in panels:
        if p.get("height_mode", "fixed") != "calibrated":          # forbidden pattern f1
            bad["height-variability"].append(f"{p['id']} has fixed Y (height_mode={p.get('height_mode', 'fixed')})")
        if p.get("critical"):
            for pose in poses:
                pos = p.get(f"{pose}_position") or p["position"]
                if not reachable(pos, pose):
                    bad["reach-zones-pinned"].append(f"{p['id']} not reachable {pose}: zone={zone(pos)}, y={pos['y']}")

    occluding = [(p["id"], t) for p in panels if p.get("critical") for t in p.get("occludes", []) if t in critical]
    if len(occluding) > 1:                                          # forbidden pattern f2
        bad["occlusion-budget"].append("critical-on-critical occlusions: " + ", ".join(f"{a}->{b}" for a, b in occluding))

    for e in scene.get("events", []):
        audio = e.get("audio", {})
        if e.get("critical") and not (audio.get("spatial") and audio.get("direction_matches_visual")):
            bad["spatial-audio-directional"].append(f"{e['id']} audio is mono or direction mismatched")  # f4

    for i in scene.get("interactions", []):
        if i.get("pose") == "standing" and not i.get("seated_alternate"):
            bad["seated-alternate-required"].append(f"{i['id']} is standing-only")                # f3

    return [{"rule": rule, "verdict": "fail" if issues else "pass", "detail": issues} for rule, issues in bad.items()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("--owner", default="<@xr-designer>")
    ap.add_argument("--out", default="spatial-accessibility-record.json")
    args = ap.parse_args()
    scene = json.load(open(args.scene, encoding="utf-8"))
    findings = audit(scene)
    failed = [f["rule"] for f in findings if f["verdict"] == "fail"]
    record = {
        "artefact_id": f"spa-{datetime.date.today():%Y-%m-%d}-{scene.get('experience', 'scene')}",
        "version": "1.1.0",
        "last_reviewed": datetime.date.today().isoformat(),
        "owner": args.owner,
        "scope": {"experience": scene.get("experience", "<experience>"),
                  "platforms": scene.get("platforms", ["<platform>"]),
                  "session_pose": scene.get("session_pose", ["seated", "standing"]),
                  "zone_map": {p["id"]: zone(p["position"]) for p in scene.get("panels", [])}},
        "findings": findings,
        "summary": ("all five spatial rules pass" if not failed else "failing: " + ", ".join(failed)),
        "verdict": "pass" if not failed else "fail",
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(f"{record['verdict'].upper()}: {record['summary']} -> {args.out}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
