#!/usr/bin/env python3
"""zone-audit.py — audit one Cloudflare zone's security settings against a
policy file and print only the settings that violate it.

This exists for output compression, not for API access. Cloudflare ships an
MCP server; asking it for a zone's posture returns ~40 setting objects of
vendor JSON that the model pays for token by token and then has to compare by
hand. This tool makes the same calls, applies the policy, and returns one
summary line plus one line per violation. A clean zone costs a single line.

The batch `GET /zones/{id}/settings` endpoint was deprecated 2025-04-23 (EOL
2027-03-31), so the sweep fans out over the per-setting endpoint instead: one
GET per policy key, which is also why the policy file is the thing that sets
the request count.

It does NOT change anything. Every request is a GET, and the fix for a
violation is deliberately left to a human: the safe value for `security_level`
on a zone under attack is a judgement no gate should make.

Input:  --zone plus an optional --policy JSON file
Output: one summary line on stdout; one line per violation on stderr.

Exit: 0 policy met - 1 at least one violation - 2 the tool could not run
      - 3 the credential is absent - 4 the credential was rejected
      - 6 the vendor API failed, including a rate limit.
Zero model calls.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

NAME = "zone-audit"
API = "https://api.cloudflare.com/client/v4"
ENV_VAR = "CLOUDFLARE_API_TOKEN"
TIMEOUT = 30

# The built-in policy. A --policy file is merged over this, and a rule of null
# drops that check, so a caller states only their deltas.
DEFAULT_POLICY = {
    "ssl": {"at_least": "full"},
    "min_tls_version": {"at_least": "1.2"},
    "always_use_https": "on",
    "security_level": {"at_least": "medium"},
    "http3": "on",
    "opportunistic_encryption": "on",
}

# Ordered scales, worst first, for the `at_least` rule. A value outside its
# scale is reported rather than silently passed.
RANKS = {
    "ssl": ["off", "flexible", "full", "strict"],
    "min_tls_version": ["1.0", "1.1", "1.2", "1.3"],
    "security_level": ["off", "essentially_off", "low", "medium", "high",
                       "under_attack"],
}

# Per-setting `result` objects as the API returns them. OK satisfies the
# built-in policy; BAD is the zone a caller actually has — SSL left on
# flexible, TLS 1.0 still accepted, HTTPS not forced.
OK_FIXTURE = (
    '[{"id": "ssl", "value": "strict", "editable": true},'
    ' {"id": "min_tls_version", "value": "1.3"},'
    ' {"id": "always_use_https", "value": "on"},'
    ' {"id": "security_level", "value": "high"},'
    ' {"id": "http3", "value": "on"},'
    ' {"id": "opportunistic_encryption", "value": "on"}]'
)
BAD_FIXTURE = (
    '[{"id": "ssl", "value": "flexible"},'
    ' {"id": "min_tls_version", "value": "1.0"},'
    ' {"id": "always_use_https", "value": "off"},'
    ' {"id": "security_level", "value": "high"},'
    ' {"id": "http3", "value": "on"},'
    ' {"id": "opportunistic_encryption", "value": "on"}]'
)


class ApiError(Exception):
    """A failed call, carrying the exit code the caller should return."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


class SameHostRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse a redirect that leaves the API host.

    The request carries a bearer credential in a header and urllib would
    replay that header at whatever host the Location line names."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        here = urllib.parse.urlsplit(req.full_url).hostname
        there = urllib.parse.urlsplit(newurl).hostname
        if here != there:
            return None
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def envelope_errors(body: dict) -> list[str]:
    """The envelope's own error strings, never its result."""
    out = []
    for item in body.get("errors") or []:
        if isinstance(item, dict):
            out.append(f"{item.get('code', '?')}: {item.get('message', '')}")
        else:
            out.append(str(item))
    return out


def settings_map(results: list) -> dict:
    """Per-setting result objects to {setting_id: value}."""
    out: dict = {}
    for item in results:
        if isinstance(item, dict) and item.get("id"):
            out[str(item["id"])] = item.get("value")
    return out


def compare(setting_id: str, value, rule) -> str | None:
    """One violation string, or None when the value satisfies the rule."""
    text = str(value)
    if isinstance(rule, list):
        rule = {"one_of": rule}
    if isinstance(rule, dict):
        if "one_of" in rule:
            allowed = [str(x) for x in rule["one_of"]]
            if text in allowed:
                return None
            return f"{setting_id}: {text}, policy allows {'|'.join(allowed)}"
        if "at_least" in rule:
            scale = RANKS.get(setting_id)
            want = str(rule["at_least"])
            if not scale or text not in scale or want not in scale:
                return (f"{setting_id}: {text}, policy wants at least {want} "
                        "and the value is off the known scale")
            if scale.index(text) >= scale.index(want):
                return None
            return f"{setting_id}: {text}, policy wants at least {want}"
        return f"{setting_id}: policy rule {sorted(rule)} is not understood"
    if text == str(rule):
        return None
    return f"{setting_id}: {text}, policy wants {rule}"


def check(settings: dict, policy: dict, strict: bool = False) -> list[str]:
    """Every violation, one string each. Pure: no I/O, no exits.

    A setting the zone or plan does not expose arrives as None. That is a
    skipped check by default — a Free zone has no say over an Enterprise-only
    toggle — and a violation under --strict, where the caller has decided that
    an unverifiable control is an unmet control."""
    findings: list[str] = []
    for setting_id in sorted(policy):
        rule = policy[setting_id]
        if rule is None:
            continue
        if setting_id not in settings or settings[setting_id] is None:
            if strict:
                findings.append(f"{setting_id}: not exposed by this zone or "
                                "plan, and strict counts that as unmet")
            continue
        problem = compare(setting_id, settings[setting_id], rule)
        if problem:
            findings.append(problem)
    return findings


def checked_ids(policy: dict) -> list[str]:
    """The setting ids the sweep will fetch, in a fixed order."""
    return [k for k in sorted(policy) if policy[k] is not None]


def report(zone: str, policy: dict, settings: dict,
           findings: list[str]) -> str:
    """The written audit: every setting checked, not only the failures."""
    lines = [f"# {NAME}: {zone}", "", "| setting | value | rule | verdict |",
             "|---|---|---|---|"]
    failed = {f.split(":", 1)[0] for f in findings}
    for setting_id in checked_ids(policy):
        value = settings.get(setting_id)
        shown = "not exposed" if value is None else str(value)
        verdict = "VIOLATION" if setting_id in failed else (
            "skipped" if value is None else "ok")
        lines.append(f"| {setting_id} | {shown} | "
                     f"{json.dumps(policy[setting_id])} | {verdict} |")
    lines += ["", f"violations: {len(findings)}", ""]
    lines += [f"- {f}" for f in findings] or ["- none"]
    return "\n".join(lines) + "\n"


def call(path: str, token: str, soft: tuple = ()) -> dict | None:
    """One GET. Returns the parsed envelope, or None for a tolerated status."""
    request = urllib.request.Request(API + path, method="GET")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/json")
    opener = urllib.request.build_opener(SameHostRedirect)
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in soft:
            return None
        if exc.code in (401, 403):
            raise ApiError(4, f"credential rejected ({exc.code}) on {path}")
        raise ApiError(6, f"api {exc.code} on {path}")
    except (urllib.error.URLError, OSError) as exc:
        raise ApiError(2, f"cannot reach the api: {exc}")
    except ValueError:
        raise ApiError(6, f"api returned unparseable json on {path}")
    if not body.get("success"):
        detail = "; ".join(envelope_errors(body))[:160]
        raise ApiError(6, f"api rejected {path}: {detail}")
    return body


def resolve_zone(zone: str, token: str) -> str:
    """The zone id, or an ApiError naming which of the two failures it was."""
    body = call(f"/zones?name={urllib.parse.quote(zone)}", token)
    result = (body or {}).get("result") or []
    if not result:
        raise ApiError(2, f"no zone named {zone} is visible to this token")
    return str(result[0].get("id"))


def sweep(zone_id: str, token: str, ids: list[str]) -> dict:
    """One GET per setting. The batch settings endpoint is deprecated."""
    out: dict = {}
    for setting_id in ids:
        body = call(f"/zones/{zone_id}/settings/{setting_id}", token,
                    soft=(400, 404))
        out[setting_id] = None if body is None else (
            body.get("result") or {}).get("value")
    return out


def load_policy(path: str | None) -> dict:
    """The built-in policy with the file merged over it. Raises ValueError."""
    policy = dict(DEFAULT_POLICY)
    if not path:
        return policy
    override = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(override, dict):
        raise ValueError("a policy file is a JSON object of setting id to rule")
    policy.update(override)
    return policy


def self_test() -> list[str]:
    """Prove parsing, merging and the policy comparison. No network call."""
    failures: list[str] = []
    ok = settings_map(json.loads(OK_FIXTURE))
    bad = settings_map(json.loads(BAD_FIXTURE))

    if len(ok) != 6:
        failures.append(f"OK fixture parsed to {len(ok)} settings, expected 6")
    if check(ok, DEFAULT_POLICY):
        failures.append(f"OK fixture violated the policy: {check(ok, DEFAULT_POLICY)}")
    if len(check(bad, DEFAULT_POLICY)) != 3:
        failures.append(f"BAD fixture gave {check(bad, DEFAULT_POLICY)}, "
                        "expected ssl, min_tls_version, always_use_https")
    if compare("min_tls_version", "1.3", {"at_least": "1.2"}) is not None:
        failures.append("at_least treated a higher value as a violation")
    if compare("ssl", "flexible", {"at_least": "full"}) is None:
        failures.append("at_least passed a value below the floor")
    if compare("ssl", "banana", {"at_least": "full"}) is None:
        failures.append("a value off the scale was passed silently")
    if compare("security_level", "high", ["high", "under_attack"]) is not None:
        failures.append("a list rule rejected a member")

    thin = {k: v for k, v in ok.items() if k != "http3"}
    if check(thin, DEFAULT_POLICY):
        failures.append("an unexposed setting was counted without strict")
    if len(check(thin, DEFAULT_POLICY, strict=True)) != 1:
        failures.append("strict did not count an unexposed setting")

    relaxed = dict(DEFAULT_POLICY)
    relaxed["ssl"] = None
    if len(check(bad, relaxed)) != 2:
        failures.append("a null rule did not drop its check")
    if "ssl" in checked_ids(relaxed):
        failures.append("a null rule was still fetched")

    body = {"success": False, "errors": [{"code": 1049, "message": "no route"}]}
    if envelope_errors(body) != ["1049: no route"]:
        failures.append("envelope errors were not extracted")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zone", help="zone name to audit, e.g. example.com")
    ap.add_argument("--policy", help="JSON policy file merged over the default")
    ap.add_argument("--out", help="write the full audit table here")
    ap.add_argument("--json", action="store_true",
                    help="emit the summary line as one line of JSON")
    ap.add_argument("--strict", action="store_true",
                    help="count a setting the plan does not expose as unmet")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit, offline")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=12 failures={len(failures)}")
        return 1 if failures else 0

    if not args.zone:
        print(f"{NAME}: --zone is required", file=sys.stderr)
        return 2
    try:
        policy = load_policy(args.policy)
    except (OSError, ValueError) as exc:
        print(f"{NAME}: cannot read the policy: {exc}", file=sys.stderr)
        return 2

    token = os.environ.get(ENV_VAR, "").strip()
    if not token:
        print(f"{NAME}: {ENV_VAR} is not set; the credential is read from the "
              "environment and there is no flag for it", file=sys.stderr)
        return 3

    ids = checked_ids(policy)
    try:
        zone_id = resolve_zone(args.zone, token)
        settings = sweep(zone_id, token, ids)
    except ApiError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return exc.code

    findings = check(settings, policy, args.strict)
    if args.out:
        try:
            Path(args.out).write_text(
                report(args.zone, policy, settings, findings), encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write the audit: {exc}", file=sys.stderr)
            return 2

    for finding in findings:
        print(f"{NAME}: {finding}", file=sys.stderr)
    if args.json:
        print(json.dumps({"tool": NAME, "zone": args.zone, "checks": len(ids),
                          "violations": len(findings), "findings": findings},
                         sort_keys=True))
    else:
        print(f"{NAME}: zone={args.zone} checks={len(ids)} "
              f"violations={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
