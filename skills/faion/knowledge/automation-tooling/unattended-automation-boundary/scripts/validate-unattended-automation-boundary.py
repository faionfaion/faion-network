#!/usr/bin/env python3
"""Validate an Unattended Automation Record against the boundary contract.

Enforces the nobody-present gate and its stop (r1), the fixed escalation order
and its justifications (r2), the dated per-tool exec-capability table (r3), the
always-on host requirement (r4), blast radius and stop switch (r5), the
single-surface rule (r6) and the dated failing trigger (r7).

Usage:
  validate-unattended-automation-boundary.py <record.yaml|.json>
  validate-unattended-automation-boundary.py --self-test
  validate-unattended-automation-boundary.py --help

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

SURFACES = {"none", "agent-hooks", "os-scheduler", "workflow-runtime"}
TRIGGER_KINDS = {"schedule", "webhook", "file-event", "manual"}
AVAILABILITY = {"always-on", "sleeps", "manual-start"}

GATE_KEYS = ("system", "triggers", "failing_trigger", "chosen_surface", "rejected_surfaces")
SURFACE_KEYS = (
    "needs_local_exec", "runtime", "self_hosted", "why_hooks_insufficient",
    "why_scheduler_insufficient", "host", "host_availability",
    "host_cost_per_month", "blast_radius", "stop_switch",
)

# r3 — exec capability, assessed 2026-08-04. True means "can run a local binary",
# and for n8n only when self-hosted.
EXEC_CAPABLE = {
    "n8n": "self-hosted-only",
    "make": False,
    "maia": False,
    "dify": False,
    "flowise": False,
}
EXEC_REASON = {
    "make": "Make/Maia cannot exec; the On-Premise Agent is an HTTP bridge on an enterprise plan",
    "maia": "Make/Maia cannot exec; the On-Premise Agent is an HTTP bridge on an enterprise plan",
    "dify": "Dify cannot exec even self-hosted; its code sandbox seccomp policy blocks exec syscalls",
    "flowise": "Flowise Custom Function runs in a JS VM sandbox without child_process",
}

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def violations(rec: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(rec, dict):
        return ["record root must be a mapping"]

    for key in GATE_KEYS:
        if key not in rec:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    surface = str(rec["chosen_surface"]).strip()
    if surface not in SURFACES:
        errs.append(f"chosen_surface {surface!r} not in {sorted(SURFACES)}")

    # r1 — the trigger inventory is what decides the gate.
    triggers = rec["triggers"]
    if not isinstance(triggers, list) or not triggers:
        errs.append("triggers must be a non-empty inventory (r1-nobody-present-gate)")
        return errs
    unattended = 0
    for i, t in enumerate(triggers):
        if not isinstance(t, dict):
            errs.append(f"triggers[{i}] must be a mapping")
            continue
        if not str(t.get("name") or "").strip():
            errs.append(f"triggers[{i}] needs a name")
        if str(t.get("kind") or "").strip() not in TRIGGER_KINDS:
            errs.append(f"triggers[{i}].kind must be one of {sorted(TRIGGER_KINDS)}")
        if not isinstance(t.get("human_present"), bool):
            errs.append(
                f"triggers[{i}].human_present must be an explicit boolean; it is the "
                "field that decides the gate (r1-nobody-present-gate)"
            )
        elif t["human_present"] is False:
            unattended += 1
        if not str(t.get("when") or "").strip():
            errs.append(f"triggers[{i}] needs a concrete `when`")

    # r7 — a dated failure of the current arrangement.
    failing = str(rec["failing_trigger"]).strip()
    if len(failing) < 30:
        errs.append("failing_trigger must describe a real failure in >=30 chars (r7-name-the-failing-trigger)")
    if not YEAR_RE.search(failing):
        errs.append("failing_trigger must carry a four-digit year (r7-name-the-failing-trigger)")

    # r6 — everything considered goes in rejected_surfaces, never alongside.
    rejected = rec["rejected_surfaces"]
    if not isinstance(rejected, list) or not rejected:
        errs.append(
            "rejected_surfaces must name at least what you were about to install "
            "(r6-one-unattended-surface-per-system)"
        )
    else:
        for i, r in enumerate(rejected):
            if not isinstance(r, dict) or not str(r.get("reason") or "").strip():
                errs.append(f"rejected_surfaces[{i}] needs a surface and a reason (r6-one-unattended-surface-per-system)")

    # r1 — the stop: no unattended trigger means no surface, and the record ends.
    if unattended == 0:
        if surface != "none":
            errs.append(
                "no trigger has human_present: false, so chosen_surface must be 'none' "
                "and nothing is installed (r1-nobody-present-gate)"
            )
        leaked = [k for k in SURFACE_KEYS if k in rec]
        if leaked:
            errs.append(
                "the gate stopped this record; remove surface fields: "
                + ", ".join(sorted(leaked))
                + " (r1-nobody-present-gate)"
            )
        return errs

    if surface == "none":
        leaked = [k for k in SURFACE_KEYS if k in rec]
        if leaked:
            errs.append(
                "chosen_surface is 'none' so the record MUST stop; remove: "
                + ", ".join(sorted(leaked))
                + " (r1-nobody-present-gate)"
            )
        return errs

    # r4 / r5 — operating conditions for any real surface.
    if not str(rec.get("host") or "").strip():
        errs.append("a chosen surface requires a named host (r4-host-must-be-awake)")
    availability = str(rec.get("host_availability") or "").strip()
    if availability not in AVAILABILITY:
        errs.append(f"host_availability must be one of {sorted(AVAILABILITY)} (r4-host-must-be-awake)")
    elif availability != "always-on":
        errs.append(
            f"host_availability is '{availability}'; a host that is not always-on turns a "
            "missed run into silence, not an error (r4-host-must-be-awake)"
        )
    if len(str(rec.get("blast_radius") or "").strip()) < 20:
        errs.append("blast_radius must state what a run may write, publish and spend (r5-blast-radius-and-stop-switch)")
    if len(str(rec.get("stop_switch") or "").strip()) < 12:
        errs.append(
            "stop_switch must be operable by a human who has not read the workflow "
            "(r5-blast-radius-and-stop-switch)"
        )

    # r2 — each step up names what the step below could not express.
    if surface in ("os-scheduler", "workflow-runtime"):
        if len(str(rec.get("why_hooks_insufficient") or "").strip()) < 20:
            errs.append(
                "escalating past agent hooks requires why_hooks_insufficient, naming a "
                "missing capability rather than a convenience (r2-cheapest-surface-first)"
            )
    if surface == "workflow-runtime":
        if len(str(rec.get("why_scheduler_insufficient") or "").strip()) < 20:
            errs.append(
                "escalating past the OS scheduler requires why_scheduler_insufficient "
                "(r2-cheapest-surface-first)"
            )

    # r3 — exec capability is a hard constraint on the last surface.
    needs_exec = rec.get("needs_local_exec")
    if not isinstance(needs_exec, bool):
        errs.append("needs_local_exec must be an explicit boolean (r3-exec-capability-is-a-hard-constraint)")
    if surface == "workflow-runtime":
        runtime = str(rec.get("runtime") or "").strip().lower()
        if not runtime:
            errs.append("chosen_surface 'workflow-runtime' requires a named runtime (r3-exec-capability-is-a-hard-constraint)")
        elif needs_exec is True:
            capability = EXEC_CAPABLE.get(runtime)
            if capability is False:
                errs.append(
                    f"needs_local_exec is true but {runtime} cannot run a local binary: "
                    f"{EXEC_REASON[runtime]} (assessed 2026-08-04) "
                    "(r3-exec-capability-is-a-hard-constraint)"
                )
            elif capability == "self-hosted-only" and rec.get("self_hosted") is not True:
                errs.append(
                    "needs_local_exec is true with n8n, which can exec on self-hosted "
                    "instances only and with the node explicitly re-enabled; set "
                    "self_hosted: true or choose another surface "
                    "(r3-exec-capability-is-a-hard-constraint)"
                )
            elif capability is None:
                errs.append(
                    f"runtime {runtime!r} is not in the dated capability table; verify it can "
                    "exec a local binary and record the check (r3-exec-capability-is-a-hard-constraint)"
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


def _ok_none() -> dict:
    return {
        "system": "weekly content pipeline: research, draft, review, publish",
        "triggers": [
            {"name": "start the week's batch", "kind": "manual", "human_present": True,
             "when": "Monday morning, when I sit down"},
            {"name": "publish after review", "kind": "manual", "human_present": True,
             "when": "after I have read it"},
        ],
        "failing_trigger": "None. Checked three months of runs to 2026-08-04: every one began with me starting it.",
        "chosen_surface": "none",
        "rejected_surfaces": [
            {"surface": "workflow-runtime", "reason": "every trigger has me present; the session already runs it"},
        ],
    }


def _ok_scheduler() -> dict:
    return {
        "system": "nightly ingest of an external partner feed",
        "triggers": [
            {"name": "partner drops the feed", "kind": "webhook", "human_present": False,
             "when": "between 02:00 and 04:00 UTC"},
            {"name": "manual re-run", "kind": "manual", "human_present": True, "when": "next morning"},
        ],
        "failing_trigger": "On 2026-07-19 the partner posted at 03:10 UTC and nothing ingested until 11:00 next day.",
        "chosen_surface": "os-scheduler",
        "needs_local_exec": True,
        "why_hooks_insufficient": "hooks fire inside a session; there is no session at 03:00 and nothing starts one",
        "host": "the reporting VPS",
        "host_availability": "always-on",
        "blast_radius": "writes the staging schema and /var/log/ingest only; holds a read-only feed token",
        "stop_switch": "systemctl disable --now ingest.timer",
        "rejected_surfaces": [
            {"surface": "workflow-runtime", "reason": "a timer already expresses this; it would be a second scheduler"},
        ],
    }


def _ok_n8n() -> dict:
    return dict(
        _ok_scheduler(),
        chosen_surface="workflow-runtime",
        runtime="n8n",
        self_hosted=True,
        why_scheduler_insufficient="the feed must fan out to four downstream systems with per-branch retry and replay",
    )


def self_test() -> int:
    none_with_host = dict(_ok_none(), host="a VPS", host_availability="always-on")
    present_but_surface = dict(_ok_none(), chosen_surface="os-scheduler")

    dify = dict(_ok_n8n(), runtime="dify")
    n8n_cloud = dict(_ok_n8n(), self_hosted=False)
    unknown_runtime = dict(_ok_n8n(), runtime="zapier")

    sleeping = dict(_ok_scheduler(), host_availability="sleeps")
    no_stop = dict(_ok_scheduler())
    no_stop.pop("stop_switch")
    no_escalation = dict(_ok_n8n())
    no_escalation.pop("why_scheduler_insufficient")
    undated = dict(_ok_scheduler(), failing_trigger="The feed was late once and the report went out stale.")
    implicit_presence = dict(_ok_scheduler())
    implicit_presence["triggers"] = [
        {"name": "partner drops the feed", "kind": "webhook", "when": "02:00 UTC"},
    ]

    cases = [
        ("gate stop, nothing installed", _ok_none(), 0),
        ("os-scheduler warranted", _ok_scheduler(), 0),
        ("self-hosted n8n with exec", _ok_n8n(), 0),
        ("none but a host specified", none_with_host, 1),
        ("all triggers attended yet a surface chosen", present_but_surface, 1),
        ("exec required on dify", dify, 1),
        ("exec required on n8n cloud", n8n_cloud, 1),
        ("runtime absent from the capability table", unknown_runtime, 1),
        ("host sleeps", sleeping, 1),
        ("no stop switch", no_stop, 1),
        ("escalation to a runtime unjustified", no_escalation, 1),
        ("failing trigger carries no date", undated, 1),
        ("human_present left implicit", implicit_presence, 1),
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
