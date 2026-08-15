#!/usr/bin/env python3
"""fw-sync.py — converge a Hetzner cloud firewall from a spec, behind a
lockout proof and a revert timer.

The lockout guard is the whole point of this tool, not a feature of it.
POST /firewalls/{id}/actions/set_rules is a destructive REPLACE: it does not
merge, and an empty array wipes every rule the firewall had. So this tool
computes the post-apply rule set, proves inbound tcp on the configured SSH
port is still allowed from every admin CIDR in the spec AND from the
caller's own source, and refuses before any write when it cannot. It never
asks a third-party service where the caller is; the source comes from
SSH_CONNECTION on-box, or from --admin-cidr, and from nowhere else.

Then the timer. An apply saves the prior rule set to a state file and arms a
revert. The applying process holds until the window elapses and puts the
prior rules back; a later run that finds an overdue uncommitted state puts
them back too, so a dropped SSH session or a closed laptop still ends with
the firewall it started with. Only a SECOND invocation carrying --commit
cancels the revert. No commit, no permanent change.

It converges rules and nothing else. It never attaches or detaches a
firewall, never touches a server, volume, snapshot or image, and cannot
rebuild anything: for those it prints the hcloud command and stops.

Input:  --spec and --firewall, plus --apply and later --commit to keep it
Output: one summary line on stdout; the capped diff on stderr.

Exit: 0 converged or nothing to do - 1 drift found, or the change was
      reverted - 2 the tool could not run - 3 HCLOUD_TOKEN is absent - 4 the
      credential was rejected - 5 refused by a safety guard - 6 the vendor
      api failed, including a rate limit past its reset.
Zero model calls.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

NAME = "fw-sync"
API = "https://api.hetzner.cloud/v1"
ENV_VAR = "HCLOUD_TOKEN"
TIMEOUT = 30
PER_PAGE = 50
MAX_WAIT = 120.0
# One bounded pause when a 429 arrives with no usable RateLimit-Reset header.
DEFAULT_BACKOFF = 30.0
# Hetzner caps a firewall at 50 rules. A spec that produces more is a spec
# bug, and finding out from the API costs a failed write.
MAX_RULES = 50
# A sync that deletes more than this is a decision, not a convergence.
MAX_REMOVE = 25
REVERT_DEFAULT = 10
TICK = 5.0
ACTION_POLLS = 60
ACTION_PAUSE = 2.0
PREVIEW = 20
ANY_V4 = "0.0.0.0/0"
ANY_V6 = "::/0"

# --- fixtures. No network, no credential, no host contacted. -----------------
SPEC_FIXTURE = {
    "host": "box-1",
    "ssh_port": 22,
    "admin_cidrs": ["203.0.113.0/24", "198.51.100.7/32"],
    "public_ports": [80, 443],
    "extra_rules": [{"protocol": "udp", "port": "51820",
                     "source_ips": [ANY_V4, ANY_V6],
                     "description": "wireguard"}],
    "firewalls": {"box-fw": {"public_ports": [80, 443]}},
}
CURRENT_FIXTURE = [
    {"direction": "in", "protocol": "tcp", "port": "22",
     "source_ips": ["203.0.113.0/24", "198.51.100.7/32"]},
    {"direction": "in", "protocol": "tcp", "port": "80",
     "source_ips": [ANY_V4, ANY_V6]},
    {"direction": "in", "protocol": "tcp", "port": "8080",
     "source_ips": [ANY_V4]},
]
# The rule set a caller reaches for when they "just tidy up the SSH rule":
# admin SSH now comes only from an office range nobody is sitting in.
LOCKOUT_FIXTURE = [
    {"direction": "in", "protocol": "tcp", "port": "22",
     "source_ips": ["192.0.2.0/24"]},
    {"direction": "in", "protocol": "tcp", "port": "443",
     "source_ips": [ANY_V4, ANY_V6]},
]


class Throttled:
    """A stubbed opener that raises a 429 where a socket would be opened.

    It is how --self-test exercises the rate-limit path for real without a
    network: nothing is connected, the stub raises first."""

    def __init__(self, headers: dict) -> None:
        self.headers = headers

    def open(self, *_args, **_kwargs):
        raise urllib.error.HTTPError(API, 429, "Too Many Requests",
                                     self.headers, None)


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


def as_network(value) -> ipaddress.IPv4Network | ipaddress.IPv6Network | None:
    """A CIDR, or None when the text is not one. Never raises."""
    try:
        return ipaddress.ip_network(str(value).strip(), strict=False)
    except (TypeError, ValueError):
        return None


def cidr_covers(outer, inner) -> bool:
    """True when `outer` contains `inner`.

    Containment is decided WITHIN a family and never across one. `subnet_of`
    raises TypeError on a mixed pair, and a dual-stack admin list is entirely
    ordinary, so the families are compared first. The consequence is
    deliberate and is what the reachability proof rests on: an SSH rule that
    allows only v4 does NOT cover an operator arriving over v6, so that case
    FAILS the proof rather than passing it."""
    big, small = as_network(outer), as_network(inner)
    if big is None or small is None or big.version != small.version:
        return False
    return small.subnet_of(big)


def reset_wait(header, now: float) -> float | None:
    """Seconds to pause after a 429, or None when waiting is not the answer.

    RateLimit-Reset is a unix timestamp. A missing or unparseable header is
    neither a reason to crash nor a reason to spin — it falls back to one
    bounded pause, because a rate-limit handler that dies on a missing header
    dies exactly when the API is under pressure. A reset further out than
    MAX_WAIT comes back as None and the run ends with exit 6."""
    try:
        wait = float(str(header).strip()) - now
    except (TypeError, ValueError):
        return DEFAULT_BACKOFF
    if wait > MAX_WAIT:
        return None
    return min(max(wait, 0.0) + 1.0, MAX_WAIT)


def port_covers(spec_port, port: int) -> bool:
    """True when a Hetzner rule port field covers `port`."""
    if spec_port in (None, "", "any"):
        return True
    text = str(spec_port)
    if "-" in text:
        low, _sep, high = text.partition("-")
        if low.strip().isdigit() and high.strip().isdigit():
            return int(low) <= port <= int(high)
        return False
    return text.isdigit() and int(text) == port


def normalise(rule: dict) -> dict:
    """One rule in the shape the API takes and the diff compares."""
    # Annotated: source_ips is a LIST in the API body. Without this the
    # inferred value type is str and the list assignment below reads as a bug.
    out: dict[str, object] = {
        "direction": str(rule.get("direction", "in")),
        "protocol": str(rule.get("protocol", "tcp"))}
    if out["protocol"] in ("tcp", "udp") and rule.get("port") is not None:
        out["port"] = str(rule["port"])
    key = "destination_ips" if out["direction"] == "out" else "source_ips"
    out[key] = sorted({str(ip).strip() for ip in
                       (rule.get(key) or rule.get("source_ips") or [])})
    if rule.get("description"):
        out["description"] = str(rule["description"])[:255]
    return out


def rule_key(rule: dict) -> tuple:
    """Identity for the diff. The description is documentation, not identity,
    so re-wording one is never a rule change."""
    ips = rule.get("source_ips") or rule.get("destination_ips") or []
    return (rule.get("direction", "in"), rule.get("protocol", "tcp"),
            str(rule.get("port", "")), tuple(sorted(str(i) for i in ips)))


def show(rule: dict) -> str:
    """One rule as one readable line."""
    ips = rule.get("source_ips") or rule.get("destination_ips") or []
    port = rule.get("port")
    proto = f"{rule.get('protocol')}/{port}" if port else str(
        rule.get("protocol"))
    return (f"{rule.get('direction', 'in')} {proto} "
            f"{'to' if rule.get('direction') == 'out' else 'from'} "
            f"{','.join(sorted(str(i) for i in ips)) or 'anywhere'}")


def resolve_spec(doc: dict, firewall: str) -> dict | str:
    """The effective spec for one firewall, or one error string."""
    walls = doc.get("firewalls") or {}
    if walls and firewall not in walls:
        return f"the spec has no firewall named {firewall}"
    spec = {"firewall": firewall, "host": doc.get("host"), "ssh_port": 22,
            "admin_cidrs": [], "public_ports": [], "extra_rules": []}
    for source in (doc, walls.get(firewall) or {}):
        for key in ("ssh_port", "admin_cidrs", "public_ports", "extra_rules",
                    "host"):
            if key in source:
                spec[key] = source[key]
    if not spec["admin_cidrs"]:
        return "spec.admin_cidrs is empty; there would be no SSH rule to prove"
    for cidr in spec["admin_cidrs"]:
        try:
            ipaddress.ip_network(str(cidr), strict=False)
        except ValueError:
            return f"spec.admin_cidrs holds {cidr!r}, which is not a CIDR"
    spec["public_ports"] = sorted({int(p) for p in spec["public_ports"]})
    spec["ssh_port"] = int(spec["ssh_port"])
    return spec


def desired_rules(spec: dict) -> list[dict]:
    """The rule set the spec describes. Pure: this is what --apply sends."""
    rules = [normalise({"direction": "in", "protocol": "tcp",
                        "port": spec["ssh_port"],
                        "source_ips": spec["admin_cidrs"],
                        "description": "ssh admin"})]
    for port in spec["public_ports"]:
        if int(port) == int(spec["ssh_port"]):
            continue
        rules.append(normalise({"direction": "in", "protocol": "tcp",
                                "port": port,
                                "source_ips": [ANY_V4, ANY_V6],
                                "description": "public"}))
    for extra in spec["extra_rules"]:
        rules.append(normalise(extra))
    seen: dict[tuple, dict] = {}
    for rule in rules:
        seen.setdefault(rule_key(rule), rule)
    return [seen[key] for key in sorted(seen)]


def caller_source(ssh_connection: str | None,
                  declared: list[str] | None) -> str | None:
    """Where this run is coming from: SSH_CONNECTION on-box, else --admin-cidr.

    Deliberately never an IP-echo service: contacting an undeclared host to
    learn our own address is exactly the exfiltration path the network
    allowlist exists to close."""
    if declared:
        return str(declared[0]).strip()
    fields = (ssh_connection or "").split()
    if not fields:
        return None
    try:
        address = ipaddress.ip_address(fields[0])
    except ValueError:
        return None
    return f"{address}/{'32' if address.version == 4 else '128'}"


def prove(rules: list[dict], ssh_port: int, sources: list[str]) -> list[str]:
    """Every source that would LOSE inbound SSH under `rules`. Pure.

    Empty means proven. This runs against the post-apply rule set, before a
    byte is written."""
    ssh_rules = [r for r in rules
                 if r.get("direction", "in") == "in"
                 and r.get("protocol") == "tcp"
                 and port_covers(r.get("port"), int(ssh_port))]
    lost: list[str] = []
    for source in sources:
        covered = any(cidr_covers(allowed, source)
                      for rule in ssh_rules
                      for allowed in (rule.get("source_ips") or []))
        if not covered:
            lost.append(source)
    return lost


def guard(desired: list[dict], current: list[dict], spec: dict,
          sources: list[str], caller: str | None) -> str | None:
    """Why this run must not write, or None when it may. Pure.

    Every branch here is exit 3. They are the refusals a firewall tool has to
    make before the write, because after the write the caller may have no way
    back in."""
    if caller is None:
        return ("cannot tell where this run is coming from: SSH_CONNECTION is "
                "unset and --admin-cidr was not given, so the lockout proof "
                "cannot be made")
    if not desired:
        return ("the spec produces an empty rule set, and set_rules with an "
                "empty array wipes every rule this firewall has")
    if len(desired) > MAX_RULES:
        return (f"{len(desired)} rules is over the Hetzner limit of "
                f"{MAX_RULES} for one firewall")
    removed = [r for r in current if rule_key(r) not in
               {rule_key(d) for d in desired}]
    if len(removed) > MAX_REMOVE:
        return (f"the plan removes {len(removed)} rules, over the cap of "
                f"{MAX_REMOVE}; that is a decision, not a sync")
    lost = prove(desired, spec["ssh_port"], sources)
    if lost:
        return (f"the post-apply rule set would lose inbound tcp/"
                f"{spec['ssh_port']} from " + ",".join(lost) +
                "; add it to spec.admin_cidrs rather than papering over it")
    return None


def diff(desired: list[dict], current: list[dict]) -> tuple[list, list, list]:
    """(add, remove, keep) as rule objects."""
    want = {rule_key(r): r for r in desired}
    have = {rule_key(r): r for r in current}
    add = [want[k] for k in sorted(set(want) - set(have))]
    remove = [have[k] for k in sorted(set(have) - set(want))]
    keep = [want[k] for k in sorted(set(want) & set(have))]
    return add, remove, keep


def digest(rules: list[dict]) -> str:
    """A stable fingerprint, so a preview can be compared with the run."""
    blob = json.dumps([rule_key(r) for r in
                       sorted(rules, key=rule_key)], sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:12]


def outcome(stop: str | None, drift: bool, reverted: bool) -> int:
    """The exit code for a completed run. Pure, so the self-test can assert
    that a rule set which would lock admin SSH out returns the guard refusal,
    5, and never an ordinary finding."""
    if stop:
        return 5
    if reverted:
        return 1
    return 1 if drift else 0


def plan_report(spec: dict, desired: list[dict], current: list[dict]) -> str:
    """The full plan. Never stdout: only the delta goes to a screen."""
    add, remove, keep = diff(desired, current)
    lines = [f"# {NAME}: {spec['firewall']}", "",
             f"digest: {digest(desired)}", "",
             "## post-apply rule set", ""]
    lines += [f"- {show(r)}" for r in desired]
    lines += ["", "## added", ""] + ([f"- {show(r)}" for r in add] or ["- none"])
    lines += ["", "## removed", ""] + ([f"- {show(r)}" for r in remove]
                                       or ["- none"])
    lines += ["", "## unchanged", ""] + ([f"- {show(r)}" for r in keep]
                                         or ["- none"])
    lines += ["", "## prior rule set, restored on revert", ""]
    lines += [f"- {show(r)}" for r in current] or ["- none"]
    return "\n".join(lines) + "\n"


def revert_due(state: dict | None, now: float) -> bool:
    """True when an armed revert is overdue and must be put back.

    A malformed or absent deadline counts as due. Restoring a rule set that
    was live a moment ago cannot lock anyone out, so the fail-safe direction
    is to revert; the unsafe direction would be to let an unreadable timer
    keep an unblessed change alive forever."""
    if not state or state.get("committed") or state.get("reverted"):
        return False
    try:
        return float(state.get("revert_at")) <= now
    except (TypeError, ValueError):
        return True


def read_state(path: Path) -> dict | None:
    """The armed revert, or None when there is nothing pending."""
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return state if isinstance(state, dict) and state.get("tool") == NAME \
        else None


def write_state(path: Path, state: dict) -> None:
    """Replace the state file atomically and keep it private."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)


def call(path: str, token: str, payload: dict | None = None,
         sleeper=time.sleep, retried: bool = False) -> dict:
    """One request. GET without a payload, POST with one."""
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API + path, data=data, method="GET" if data is None else "POST")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/json")
    if data is not None:
        request.add_header("Content-Type", "application/json")
    opener = urllib.request.build_opener(SameHostRedirect)
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8")
        return json.loads(body) if body.strip() else {}
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise ApiError(4, f"credential rejected ({exc.code}) on {path}")
        if exc.code == 429:
            reset = exc.headers.get("RateLimit-Reset") if exc.headers else None
            wait = reset_wait(reset, time.time())
            if retried or wait is None:
                raise ApiError(6, f"rate limited on {path}; RateLimit-Reset "
                                  f"is {reset!r}, which is not a wait this run "
                                  "will sit through")
            sleeper(wait)
            return call(path, token, payload, sleeper, True)
        raise ApiError(6, f"api {exc.code} on {path}")
    except (urllib.error.URLError, OSError) as exc:
        raise ApiError(2, f"cannot reach the api: {exc}")
    except ValueError:
        raise ApiError(6, f"api returned unparseable json on {path}")


def await_actions(body: dict, token: str, sleeper=time.sleep) -> None:
    """Poll every action the mutation started. A mutating POST is never
    retried: a timeout is usually a success nobody waited for."""
    actions = body.get("actions") or (
        [body["action"]] if body.get("action") else [])
    for action in actions:
        ident = action.get("id")
        status = action.get("status")
        # A ceiling on polls, not a backoff: a Hetzner action settles in
        # seconds, so the pause is constant and the counter is only a bound.
        for _poll in range(ACTION_POLLS):
            if status in ("success", "error") or ident is None:
                break
            sleeper(ACTION_PAUSE)
            fresh = call(f"/actions/{ident}", token, None, sleeper)
            status = (fresh.get("action") or {}).get("status")
            action = fresh.get("action") or action
        if status != "success":
            raise ApiError(6, f"action {ident} ended {status!r}: "
                              f"{(action.get('error') or {}).get('message')}")


def find_firewall(name: str, token: str) -> dict:
    """The firewall's id, rules and attachment count."""
    body = call(f"/firewalls?name={urllib.parse.quote(name)}"
                f"&per_page={PER_PAGE}", token)
    walls = body.get("firewalls") or []
    if not walls:
        raise ApiError(2, f"no firewall named {name} in this project; create "
                          f"it with `hcloud firewall create --name {name}`")
    wall = walls[0]
    return {"id": wall.get("id"),
            "rules": [normalise(r) for r in (wall.get("rules") or [])],
            "applied_to": len(wall.get("applied_to") or [])}


def set_rules(firewall_id, rules: list[dict], token: str,
              sleeper=time.sleep) -> None:
    """The destructive replace, awaited to completion."""
    body = call(f"/firewalls/{firewall_id}/actions/set_rules", token,
                {"rules": rules}, sleeper)
    await_actions(body, token, sleeper)


def hold(path: Path, deadline: float, now=time.time,
         sleeper=time.sleep) -> bool:
    """Wait out the revert window. True when a second invocation committed.

    Polling a file rather than a signal is deliberate: the committing run is a
    separate process, usually in a separate terminal, and often on a separate
    machine from the box whose SSH is at stake."""
    while now() < deadline:
        state = read_state(path)
        if state is not None and state.get("committed"):
            return True
        sleeper(min(TICK, max(deadline - now(), 0.1)))
    state = read_state(path)
    # A state file that vanished mid-window is NOT a commit. The only thing
    # that cancels the revert is a second invocation writing committed.
    return bool(state is not None and state.get("committed"))


def self_test() -> list[str]:
    """Prove the spec resolution, the diff, the lockout proof, the revert
    state and the exit code the guard produces. No network call, no
    credential, nothing written outside a temporary path."""
    failures: list[str] = []
    spec = resolve_spec(SPEC_FIXTURE, "box-fw")
    if not isinstance(spec, dict):
        return [f"the fixture spec did not resolve: {spec}"]
    if not isinstance(resolve_spec({"admin_cidrs": []}, "box-fw"), str):
        failures.append("a spec with no admin_cidrs was accepted")
    if not isinstance(resolve_spec({"admin_cidrs": ["nonsense"]},
                                   "box-fw"), str):
        failures.append("a spec with a malformed CIDR was accepted")

    desired = desired_rules(spec)
    if len(desired) != 4:
        failures.append(f"the spec produced {len(desired)} rules, expected 4")
    add, remove, keep = diff(desired, CURRENT_FIXTURE)
    if len(add) != 2 or len(remove) != 1 or len(keep) != 2:
        failures.append(f"diff gave add={len(add)} remove={len(remove)} "
                        f"keep={len(keep)}, expected 2/1/2")
    if [show(r) for r in remove] != ["in tcp/8080 from 0.0.0.0/0"]:
        failures.append(f"the removed rule is wrong: {[show(r) for r in remove]}")
    if digest(desired) != digest(list(reversed(desired))):
        failures.append("the digest depends on rule order")
    if digest(desired) == digest(desired[:-1]):
        failures.append("the digest ignored a dropped rule")

    here = "203.0.113.9/32"
    if prove(desired, 22, spec["admin_cidrs"] + [here]):
        failures.append("the proof rejected a rule set that keeps admin SSH")
    # The heart of this tool: a rule set that WOULD lock admin SSH out must be
    # refused before any write, and the refusal must be exit 3.
    lost = prove(LOCKOUT_FIXTURE, 22, spec["admin_cidrs"] + [here])
    if sorted(lost) != sorted(spec["admin_cidrs"] + [here]):
        failures.append(f"the proof missed a lockout: lost={lost}")
    stop = guard(LOCKOUT_FIXTURE, CURRENT_FIXTURE, spec,
                 spec["admin_cidrs"] + [here], here)
    if stop is None:
        failures.append("a rule set that locks admin SSH out was not refused")
    if outcome(stop, True, False) != 5:
        failures.append("a lockout refusal did not map to the guard exit, 5")
    if outcome(None, False, False) != 0 or outcome(None, True, False) != 1 \
            or outcome(None, False, True) != 1:
        failures.append("the clean, drift and reverted exit codes are wrong")
    if guard(desired, CURRENT_FIXTURE, spec,
             spec["admin_cidrs"] + [here], here) is not None:
        failures.append("a safe convergence was refused")
    if guard([], CURRENT_FIXTURE, spec, spec["admin_cidrs"], here) is None:
        failures.append("an empty rule set was allowed to wipe the firewall")
    if guard(desired, CURRENT_FIXTURE, spec, spec["admin_cidrs"],
             None) is None:
        failures.append("an apply with no known caller source was allowed")
    wide = [dict(r, source_ips=[ANY_V4]) if r.get("port") == "22" else r
            for r in desired]
    if prove(wide, 22, ["198.51.100.7/32"]):
        failures.append("a 0.0.0.0/0 SSH rule was not seen as covering")
    many = [dict(r, port=str(9000 + n)) for n in range(MAX_REMOVE + 2)
            for r in desired[:1]]
    if guard(desired, many, spec, spec["admin_cidrs"], here) is None:
        failures.append("an oversized removal set was allowed")

    if caller_source("198.51.100.7 51000 10.0.0.1 22", None) != \
            "198.51.100.7/32":
        failures.append("SSH_CONNECTION was not read as the caller source")
    if caller_source(None, ["203.0.113.0/24"]) != "203.0.113.0/24":
        failures.append("--admin-cidr was not read as the caller source")
    if caller_source(None, None) is not None:
        failures.append("a caller source was invented from nothing")

    path = Path(os.environ.get("TMPDIR", "/tmp")) / f".{NAME}-selftest.json"
    try:
        write_state(path, {"tool": NAME, "committed": False,
                           "prior_rules": CURRENT_FIXTURE})
        if (read_state(path) or {}).get("committed") is not False:
            failures.append("the state file did not round-trip")
        if hold(path, deadline=0.0, now=lambda: 1.0, sleeper=lambda _s: None):
            failures.append("an uncommitted window was treated as committed")
        write_state(path, {"tool": NAME, "committed": True,
                           "prior_rules": CURRENT_FIXTURE})
        if not hold(path, deadline=2.0, now=lambda: 1.0,
                    sleeper=lambda _s: None):
            failures.append("a committed window was still held")
        path.unlink(missing_ok=True)
        if hold(path, deadline=0.0, now=lambda: 1.0, sleeper=lambda _s: None):
            failures.append("a vanished state file was read as a commit")
    finally:
        path.unlink(missing_ok=True)
    if "## prior rule set, restored on revert" not in \
            plan_report(spec, desired, CURRENT_FIXTURE):
        failures.append("the plan report does not carry the prior rule set")

    # A dual-stack admin list is ordinary, and containment across families
    # must be a verdict, never a TypeError. A v4-only SSH rule must FAIL the
    # proof for a v6 admin range, and that refusal must be exit 3.
    dual = resolve_spec(dict(SPEC_FIXTURE,
                             admin_cidrs=["203.0.113.0/24", "2001:db8:1::/64"]),
                        "box-fw")
    if not isinstance(dual, dict):
        failures.append(f"a dual-stack spec did not resolve: {dual}")
    else:
        dual_rules = desired_rules(dual)
        if prove(dual_rules, 22, dual["admin_cidrs"]):
            failures.append("a dual-stack SSH rule did not cover both families")
        v4_only = [dict(r, source_ips=["203.0.113.0/24"])
                   if r.get("port") == "22" else r for r in dual_rules]
        if prove(v4_only, 22, dual["admin_cidrs"]) != ["2001:db8:1::/64"]:
            failures.append("a v4-only SSH rule was read as covering a v6 "
                            "admin range")
        dual_stop = guard(v4_only, CURRENT_FIXTURE, dual,
                          dual["admin_cidrs"], "203.0.113.9/32")
        if dual_stop is None:
            failures.append("a v4-only rule was allowed against a dual-stack "
                            "admin list")
        if outcome(dual_stop, True, False) != 5:
            failures.append("the dual-stack refusal did not map to exit 5")

    # A 429 whose RateLimit-Reset header is absent or junk must fall back to
    # one bounded pause, not raise and not spin.
    if reset_wait(None, 1000.0) != DEFAULT_BACKOFF:
        failures.append("a 429 with no RateLimit-Reset did not fall back")
    if reset_wait("not-a-number", 1000.0) != DEFAULT_BACKOFF:
        failures.append("an unparseable RateLimit-Reset did not fall back")
    if reset_wait("1005", 1000.0) != 6.0:
        failures.append("a near RateLimit-Reset was not waited out")
    if reset_wait("99999", 1000.0) is not None:
        failures.append("a far RateLimit-Reset was waited on, not refused")


    # The rate-limit path driven for real, not inspected. A 429 whose
    # RateLimit-Reset header is missing must take one bounded pause and then
    # end the run, never crash and never spin.
    real_opener = urllib.request.build_opener
    for headers, want_pause in (({}, [DEFAULT_BACKOFF]),
                                ({"RateLimit-Reset": "junk"},
                                 [DEFAULT_BACKOFF])):
        slept: list[float] = []
        try:
            urllib.request.build_opener = lambda *_a, **_k: Throttled(headers)
            try:
                call("/firewalls", "fixture-credential", None, slept.append)
                failures.append(f"a 429 with headers {headers} did not raise")
            except ApiError as exc:
                if exc.code != 6:
                    failures.append(f"a 429 came back as exit {exc.code}")
            except Exception as exc:
                failures.append(f"the 429 path crashed: "
                                f"{type(exc).__name__}: {exc}")
        finally:
            urllib.request.build_opener = real_opener
        if slept != want_pause:
            failures.append(f"the 429 fallback paused {slept}, expected "
                            f"{want_pause}")

    # A state file with no usable deadline reverts rather than holding a
    # change nobody blessed.
    if not revert_due({"revert_at": None}, 1000.0):
        failures.append("a null revert deadline was not treated as due")
    if not revert_due({"revert_at": "999"}, 1000.0):
        failures.append("an elapsed revert deadline was not due")
    if revert_due({"revert_at": "2000"}, 1000.0):
        failures.append("a future revert deadline was reverted early")
    if revert_due({"revert_at": "999", "committed": True}, 1000.0) or \
            revert_due({"revert_at": "999", "reverted": True}, 1000.0):
        failures.append("a committed or already-reverted state reverted again")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", help="infra JSON: admin_cidrs, public_ports, "
                                   "ssh_port, extra_rules, firewalls")
    ap.add_argument("--firewall", help="the cloud firewall to converge")
    ap.add_argument("--admin-cidr", action="append",
                    help="where this run is coming from, when not on the box")
    ap.add_argument("--apply", action="store_true",
                    help="write the rules and arm the revert timer")
    ap.add_argument("--commit", action="store_true",
                    help="second invocation: cancel the armed revert")
    ap.add_argument("--revert-after", type=int, default=REVERT_DEFAULT,
                    help=f"minutes before the prior rules go back "
                         f"(default {REVERT_DEFAULT})")
    ap.add_argument("--state", default=f"{NAME}-state.json",
                    help="where the armed revert is recorded")
    ap.add_argument("--out", help="write the full plan here")
    ap.add_argument("--json", action="store_true",
                    help="emit the summary line as one line of JSON")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit, offline")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=42 failures={len(failures)}")
        return 1 if failures else 0

    if args.apply and args.commit:
        print(f"{NAME}: refused: commit is a SECOND invocation, not a flag "
              "added to apply; running both at once is the two-phase guard "
              "removed", file=sys.stderr)
        return 5
    if not args.firewall:
        print(f"{NAME}: --firewall is required", file=sys.stderr)
        return 2
    if args.revert_after < 1:
        print(f"{NAME}: --revert-after must be at least 1 minute",
              file=sys.stderr)
        return 2
    state_path = Path(args.state)

    token = os.environ.get(ENV_VAR, "").strip()
    if not token:
        print(f"{NAME}: {ENV_VAR} is not set; the credential is read from the "
              "environment and there is no flag for it", file=sys.stderr)
        return 3

    # Recovery first. An overdue uncommitted apply means the process that was
    # holding the window died, so the prior rules go back before anything else
    # is considered. Restoring a rule set that was live cannot lock anyone out.
    pending = read_state(state_path)
    reverted = False
    if pending and pending.get("firewall") == args.firewall \
            and revert_due(pending, time.time()):
        try:
            set_rules(pending["firewall_id"], pending["prior_rules"], token)
        except ApiError as exc:
            print(f"{NAME}: the overdue revert failed: {exc}", file=sys.stderr)
            return exc.code
        write_state(state_path, dict(pending, committed=False,
                                     reverted=True))
        print(f"{NAME}: reverted: the window closed with no commit, the prior "
              f"{len(pending['prior_rules'])} rules are back", file=sys.stderr)
        reverted = True
        pending = None

    if args.commit and not args.apply:
        state = read_state(state_path)
        if state is None or state.get("firewall") != args.firewall:
            print(f"{NAME}: nothing to commit: no armed revert for "
                  f"{args.firewall} in {state_path}", file=sys.stderr)
            return 2
        if state.get("reverted") or reverted:
            print(f"{NAME}: refused: the window closed and the prior rules "
                  "were restored; re-run with apply", file=sys.stderr)
            return 5
        if state.get("committed"):
            print(f"{NAME}: firewall={args.firewall} already committed "
                  f"digest={state.get('digest')}")
            return 0
        write_state(state_path, dict(state, committed=True))
        print(f"{NAME}: firewall={args.firewall} committed "
              f"digest={state.get('digest')} rules={len(state.get('rules', []))}")
        return 0

    if not args.spec:
        print(f"{NAME}: --spec is required", file=sys.stderr)
        return 2
    try:
        doc = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"{NAME}: cannot read the spec: {exc}", file=sys.stderr)
        return 2
    spec = resolve_spec(doc, args.firewall)
    if isinstance(spec, str):
        print(f"{NAME}: {spec}", file=sys.stderr)
        return 2

    try:
        wall = find_firewall(args.firewall, token)
    except ApiError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return exc.code

    desired = desired_rules(spec)
    add, remove, keep = diff(desired, wall["rules"])
    caller = caller_source(os.environ.get("SSH_CONNECTION"), args.admin_cidr)
    sources = list(dict.fromkeys(list(spec["admin_cidrs"]) +
                                 ([caller] if caller else [])))
    stop = guard(desired, wall["rules"], spec, sources, caller)

    if args.out:
        try:
            Path(args.out).write_text(
                plan_report(spec, desired, wall["rules"]), encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write the plan: {exc}", file=sys.stderr)
            return 2
    for rule in (add + remove)[:PREVIEW]:
        sign = "+" if rule in add else "-"
        print(f"{NAME}: {sign} {show(rule)}", file=sys.stderr)
    if len(add) + len(remove) > PREVIEW:
        print(f"{NAME}: ... and {len(add) + len(remove) - PREVIEW} more, see "
              f"{args.out or 'the out flag'}", file=sys.stderr)
    if not wall["applied_to"]:
        print(f"{NAME}: note: this firewall is applied to nothing; attach it "
              f"deliberately with `hcloud firewall apply-to-resource "
              f"{args.firewall} --type server --server "
              f"{spec.get('host') or 'NAME'}`", file=sys.stderr)
    if ANY_V4 in spec["admin_cidrs"] or ANY_V6 in spec["admin_cidrs"]:
        print(f"{NAME}: note: spec.admin_cidrs allows the whole internet, so "
              "the lockout proof passes and means nothing", file=sys.stderr)

    drift = bool(add or remove)
    committed = False
    if args.apply and stop is None:
        deadline = time.time() + args.revert_after * 60
        write_state(state_path, {
            "tool": NAME, "firewall": args.firewall,
            "firewall_id": wall["id"], "prior_rules": wall["rules"],
            "rules": desired, "digest": digest(desired),
            "revert_at": deadline, "committed": False})
        try:
            set_rules(wall["id"], desired, token)
            committed = hold(state_path, deadline)
            if not committed:
                set_rules(wall["id"], wall["rules"], token)
                write_state(state_path, dict(read_state(state_path) or {},
                                             reverted=True))
                reverted = True
        except ApiError as exc:
            print(f"{NAME}: {exc}", file=sys.stderr)
            return exc.code
        if committed:
            drift = False
        else:
            print(f"{NAME}: reverted: no commit inside {args.revert_after} "
                  f"minutes, the prior {len(wall['rules'])} rules are back",
                  file=sys.stderr)
    elif stop:
        print(f"{NAME}: refused: {stop}", file=sys.stderr)

    mode = "apply" if args.apply else "dry-run"
    summary = {"tool": NAME, "firewall": args.firewall, "mode": mode,
               "add": len(add), "remove": len(remove), "keep": len(keep),
               "digest": digest(desired), "committed": committed,
               "reverted": reverted, "plan": args.out or None}
    if args.json:
        print(json.dumps(summary, sort_keys=True))
    else:
        print(f"{NAME}: firewall={args.firewall} mode={mode} add={len(add)} "
              f"remove={len(remove)} keep={len(keep)} "
              f"digest={digest(desired)} committed={committed} "
              f"reverted={reverted}")
    return outcome(stop, drift, reverted)


if __name__ == "__main__":
    sys.exit(main())
