#!/usr/bin/env python3
"""Validate a Source Routing Record against the mcp-vs-cli-decision-rule contract.

Enforces the currency framing of the standing charge (r1), the CLI default and
its override reason (r2), the closed justification list (r3), the server cap and
the deferred-loading fallback (r4), first-party-only credentials (r5), the
spec-revision clock (r6) and the registry-is-not-trust rule (r7).

Usage:
  validate-mcp-vs-cli-decision-rule.py <source-routing-record.yaml|.json>
  validate-mcp-vs-cli-decision-rule.py --self-test
  validate-mcp-vs-cli-decision-rule.py --help

Exit codes: 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

ROUTES = {"cli", "mcp", "neither"}
JUSTIFICATIONS = {"stateful-session", "oauth-brokered", "push-subscription", "no-cli-exists"}

BASE_KEYS = ("agent", "server_cap", "definition_footprint_tokens",
             "standing_cost_per_session", "deferred_tool_loading", "sources")

# r6 — the stateless revision that deprecates Sampling, Roots and Logging.
CURRENT_REVISION = "2026-07-28"
# r7 — a listing is not a review.
REGISTRY_TOKENS = ("registry", "listed in the catalogue", "official catalogue")


def _text(v: object) -> str:
    return str(v or "").strip()


def violations(rec: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(rec, dict):
        return ["record root must be a mapping"]

    for key in BASE_KEYS:
        if key not in rec:
            errs.append(f"missing required key: {key}")
    if errs:
        return errs

    # r1 — the charge must be legible as money, not only as a token count.
    if len(_text(rec["standing_cost_per_session"])) < 4:
        errs.append(
            "standing_cost_per_session must express the charge in currency, not only "
            "as a token count (r1-standing-cost-per-request)"
        )

    cap = int(rec["server_cap"])
    if cap < 0:
        errs.append("server_cap must be >= 0 (r4-declare-a-server-cap)")

    # r4 — deferred loading trades a standing charge for a silent-miss risk.
    if rec["deferred_tool_loading"] is True and len(_text(rec.get("deferred_fallback"))) < 20:
        errs.append(
            "deferred_tool_loading is on but no deferred_fallback is recorded; a tool "
            "the agent never fetched fails as a refusal, not as an error "
            "(r4-declare-a-server-cap)"
        )

    sources = rec["sources"]
    if not isinstance(sources, list) or not sources:
        errs.append("sources must be a non-empty list")
        return errs

    mcp_count = 0
    for i, s in enumerate(sources):
        if not isinstance(s, dict):
            errs.append(f"sources[{i}] must be a mapping")
            continue
        label = _text(s.get("name")) or f"sources[{i}]"
        route = _text(s.get("route"))
        if route not in ROUTES:
            errs.append(f"{label}: route must be one of {sorted(ROUTES)}")
            continue
        if not _text(s.get("capability")):
            errs.append(f"{label}: capability is required — what the agent needs from it")
        cli_available = s.get("cli_available")
        if not isinstance(cli_available, bool):
            errs.append(f"{label}: cli_available must be an explicit boolean (r2-cli-is-the-default-route)")

        # r7 — registry listing is never a justification.
        blob = " ".join(
            _text(s.get(k)) for k in ("cli_insufficient_reason", "reason", "credential_scope")
        ).lower()
        if any(tok in blob for tok in REGISTRY_TOKENS):
            errs.append(
                f"{label}: cites registry listing as justification; the registry has been "
                "in preview since 2025-09-08 and reviews nothing (r7-registry-is-not-a-trust-signal)"
            )

        if route == "cli":
            if not _text(s.get("cli_binary")):
                errs.append(f"{label}: a cli route must name its cli_binary (r2-cli-is-the-default-route)")
            continue

        if route == "neither":
            if len(_text(s.get("reason"))) < 12:
                errs.append(f"{label}: a 'neither' route must record why")
            continue

        # route == mcp
        mcp_count += 1
        if cli_available is True and len(_text(s.get("cli_insufficient_reason"))) < 20:
            errs.append(
                f"{label}: a CLI exists but the source routes to MCP with no "
                "cli_insufficient_reason naming what the command cannot do "
                "(r2-cli-is-the-default-route)"
            )
        just = _text(s.get("mcp_justification"))
        if just not in JUSTIFICATIONS:
            errs.append(
                f"{label}: mcp_justification must be one of {sorted(JUSTIFICATIONS)}, got "
                f"{just!r} (r3-closed-list-of-justifications)"
            )
        if s.get("first_party") is not True:
            errs.append(
                f"{label}: an MCP route requires first_party: true; a third-party server "
                "sees every request and response it brokers (r5-first-party-oauth-only)"
            )
        if not _text(s.get("credential_scope")):
            errs.append(f"{label}: an MCP route requires a credential_scope (r5-first-party-oauth-only)")

        # r6 — pin the revision and start the clock when it is old.
        revision = _text(s.get("spec_revision"))
        if not revision:
            errs.append(f"{label}: an MCP route requires spec_revision (r6-pin-and-date-the-spec-revision)")
        else:
            if revision < CURRENT_REVISION and not _text(s.get("migration_deadline")):
                errs.append(
                    f"{label}: spec_revision {revision} predates {CURRENT_REVISION} with no "
                    "migration_deadline; the deprecation clock has no owner "
                    "(r6-pin-and-date-the-spec-revision)"
                )
            if revision >= CURRENT_REVISION and just == "stateful-session":
                errs.append(
                    f"{label}: justifies MCP by stateful-session against the stateless "
                    f"{revision} revision; the state has to live somewhere else "
                    "(r6-pin-and-date-the-spec-revision)"
                )

    # r4 — the cap is a cap.
    if mcp_count > cap:
        errs.append(
            f"{mcp_count} sources route to MCP but server_cap is {cap}; move the "
            "lowest-value one to CLI rather than raising the cap (r4-declare-a-server-cap)"
        )
    footprint = int(rec["definition_footprint_tokens"])
    if mcp_count == 0 and footprint != 0:
        errs.append(
            f"no source routes to MCP but definition_footprint_tokens is {footprint}; "
            "it must be 0 (r1-standing-cost-per-request)"
        )
    if mcp_count > 0 and footprint <= 0:
        errs.append(
            "sources route to MCP but definition_footprint_tokens is unmeasured; measure "
            "the connected set (r1-standing-cost-per-request)"
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


def _ok_mixed() -> dict:
    return {
        "agent": "the repo coding agent, running with shell access",
        "server_cap": 2,
        "definition_footprint_tokens": 21400,
        "standing_cost_per_session": "USD 0.09 per session at our current turn count",
        "deferred_tool_loading": True,
        "deferred_fallback": "re-run discovery once, then report the gap instead of declining silently",
        "sources": [
            {"name": "GitHub", "capability": "issues and PRs", "cli_available": True,
             "cli_binary": "gh", "route": "cli"},
            {"name": "the design tool", "capability": "read a component tree",
             "cli_available": False, "route": "mcp", "mcp_justification": "oauth-brokered",
             "first_party": True, "credential_scope": "read-only on two named files",
             "spec_revision": "2026-07-28"},
            {"name": "the ticketing system", "capability": "watch for status changes",
             "cli_available": True, "route": "mcp",
             "cli_insufficient_reason": "the command answers questions; it cannot receive a push",
             "mcp_justification": "push-subscription", "first_party": True,
             "credential_scope": "one project, issue read plus comment write",
             "spec_revision": "2026-03-26", "migration_deadline": "2027-07-28"},
        ],
    }


def _ok_cli_only() -> dict:
    return {
        "agent": "solo developer's coding agent, shell access enabled",
        "server_cap": 0,
        "definition_footprint_tokens": 0,
        "standing_cost_per_session": "USD 0.00 - no server connected",
        "deferred_tool_loading": False,
        "sources": [
            {"name": "GitHub", "capability": "issues, PRs, releases", "cli_available": True,
             "cli_binary": "gh", "route": "cli"},
            {"name": "the analytics dashboard", "capability": "weekly traffic numbers",
             "cli_available": False, "route": "neither",
             "reason": "no first-party path; a third-party server would hold the credential"},
        ],
    }


def self_test() -> int:
    over_cap = dict(_ok_mixed(), server_cap=1)

    cli_ignored = _ok_mixed()
    cli_ignored["sources"] = list(cli_ignored["sources"])
    cli_ignored["sources"][2] = dict(cli_ignored["sources"][2])
    cli_ignored["sources"][2].pop("cli_insufficient_reason")

    open_just = _ok_mixed()
    open_just["sources"] = list(open_just["sources"])
    open_just["sources"][1] = dict(open_just["sources"][1], mcp_justification="better integration")

    third_party = _ok_mixed()
    third_party["sources"] = list(third_party["sources"])
    third_party["sources"][1] = dict(third_party["sources"][1], first_party=False)

    old_rev = _ok_mixed()
    old_rev["sources"] = list(old_rev["sources"])
    old_rev["sources"][2] = dict(old_rev["sources"][2])
    old_rev["sources"][2].pop("migration_deadline")

    stateful_on_stateless = _ok_mixed()
    stateful_on_stateless["sources"] = list(stateful_on_stateless["sources"])
    stateful_on_stateless["sources"][1] = dict(
        stateful_on_stateless["sources"][1], mcp_justification="stateful-session"
    )

    registry_cited = _ok_mixed()
    registry_cited["sources"] = list(registry_cited["sources"])
    registry_cited["sources"][2] = dict(
        registry_cited["sources"][2],
        cli_insufficient_reason="it is in the official registry so it is the supported path",
    )

    no_fallback = dict(_ok_mixed())
    no_fallback.pop("deferred_fallback")

    cap_zero_with_mcp = dict(_ok_mixed(), server_cap=0)
    stale_footprint = dict(_ok_cli_only(), definition_footprint_tokens=9000)
    no_binary = _ok_cli_only()
    no_binary["sources"] = [dict(no_binary["sources"][0])]
    no_binary["sources"][0].pop("cli_binary")

    cases = [
        ("mixed routing, valid", _ok_mixed(), 0),
        ("cli-only, no server connected", _ok_cli_only(), 0),
        ("more MCP routes than the cap", over_cap, 1),
        ("CLI exists but MCP chosen with no reason", cli_ignored, 1),
        ("justification outside the closed list", open_just, 1),
        ("third-party server given credentials", third_party, 1),
        ("old revision with no migration deadline", old_rev, 1),
        ("stateful justification on a stateless revision", stateful_on_stateless, 1),
        ("registry listing cited as justification", registry_cited, 1),
        ("deferred loading with no fallback", no_fallback, 1),
        ("server_cap 0 with MCP routes", cap_zero_with_mcp, 1),
        ("footprint recorded with no MCP route", stale_footprint, 1),
        ("cli route without a binary", no_binary, 1),
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
