#!/usr/bin/env python3
"""baseline-audit.py — score one Hetzner Cloud box against a CIS-derived
security baseline and print only the items that fail.

This exists for output compression, not for API access. `hcloud` already
wraps the API; what it cannot do is correlate the account side (is a
firewall attached, is SSH open to the world, are backups paid for) with the
box side (what sshd actually negotiated, what is listening on 0.0.0.0, what
the kernel knobs are set to) and hand back one verdict. A clean box costs
one line. The full table goes to --report and never to stdout.

It never runs a command on the box. The box-side evidence is text the
caller has already gathered — `sshd -T`, `ss -tulpnH`, `sysctl -a` and one
small JSON of attestations — so the tool works over any transport, is
testable from fixtures, and cannot itself become the thing that breaks a
production host. It is read-only end to end: every request is a GET, and
the fix for a failing item is printed, never applied.

Two deliberate deviations from CIS, both stated in the report:
net.ipv4.ip_forward is audit-only with an expected waiver, because every
WireGuard hub and container host needs 1; and the SSH port is audit-only,
because moving it costs every tool and firewall a special case while the
cloud firewall already drops the scanners. A baseline that cannot be waived
gets ignored wholesale, so waivers are a first-class input — and an expired
waiver still covering a failing item stops the run rather than passing it.

Input:  --spec plus the gathered evidence files
Output: one summary line on stdout; one line per failing item on stderr.

Exit: 0 the baseline is met - 1 at least one item fails - 2 the tool could
      not run - 3 HCLOUD_TOKEN is absent - 4 the credential was rejected
      - 5 refused by a safety guard - 6 the vendor api failed, including a
      rate limit past its reset.
Zero model calls.
"""
from __future__ import annotations

import argparse
import datetime
import ipaddress
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

NAME = "baseline-audit"
API = "https://api.hetzner.cloud/v1"
ENV_VAR = "HCLOUD_TOKEN"
TIMEOUT = 30
PER_PAGE = 50
MAX_WAIT = 120.0
# One bounded pause when a 429 arrives with no usable RateLimit-Reset header.
DEFAULT_BACKOFF = 30.0
BACKUP_SURCHARGE = 0.20
PUBLIC_ADDRS = {"0.0.0.0", "::", "[::]", "*", "0.0.0.0%*"}

# id -> (title, auto-fixable, remediation). `auto` is the class, not a
# promise: this tool applies nothing. Audit-only means the fix is a
# judgement or a config change no gate should make for you.
ITEMS: list[tuple[str, str, bool, str]] = [
    ("ssh-admin-session", "sudo non-root user with a working key session",
     False, "create the user, install the key, and prove "
     "`ssh -o BatchMode=yes -o PasswordAuthentication=no user@host true` "
     "from a SECOND terminal; every other SSH item stays on hold until this "
     "passes"),
    ("sshd-root-login", "PermitRootLogin no", True,
     "set PermitRootLogin no in /etc/ssh/sshd_config.d/50-baseline.conf, "
     "then `sshd -t && systemctl reload ssh`"),
    ("sshd-password-auth", "PasswordAuthentication no", True,
     "set PasswordAuthentication no, then `sshd -t && systemctl reload ssh`"),
    ("sshd-kbdinteractive", "KbdInteractiveAuthentication no", True,
     "set KbdInteractiveAuthentication no; leaving it on re-opens the "
     "password path that PasswordAuthentication no just closed"),
    ("sshd-pubkey", "PubkeyAuthentication yes", True,
     "set PubkeyAuthentication yes"),
    ("sshd-max-auth-tries", "MaxAuthTries at most 3", True,
     "set MaxAuthTries 3"),
    ("sshd-login-grace", "LoginGraceTime at most 30", True,
     "set LoginGraceTime 30"),
    ("sshd-x11", "X11Forwarding no", True, "set X11Forwarding no"),
    ("sshd-empty-passwords", "PermitEmptyPasswords no", True,
     "set PermitEmptyPasswords no"),
    ("sshd-allowlist", "AllowUsers or AllowGroups allowlist", False,
     "audit-only on purpose: one typo in AllowUsers is total lockout. Add it "
     "by hand, keep a second session open, and re-run this audit"),
    ("sshd-port", "SSH port matches the spec", False,
     "audit-only, and the recommendation is to stay on 22: moving the port "
     "costs every tool, firewall rule and runbook a special case, and the "
     "cloud firewall already drops the scanners it was meant to hide from"),
    ("fw-cloud-attached", "cloud firewall exists and is attached", False,
     "converge it with fw-sync.py; a firewall that exists and is applied to "
     "nothing is a rule set with no host behind it"),
    ("fw-default-deny", "no inbound rule outside the declared public ports",
     False, "converge it with fw-sync.py; the spec's public_ports are the "
     "whole allowlist"),
    ("fw-ssh-restricted", "SSH inbound restricted to admin_cidrs", False,
     "converge it with fw-sync.py; SSH open to 0.0.0.0/0 makes every other "
     "SSH item cosmetic"),
    ("net-public-listeners", "no unexpected listener on 0.0.0.0", False,
     "bind the service to 127.0.0.1 or to the private network, or declare "
     "the port in the spec's public_ports if it is genuinely public"),
    ("net-container-publish", "no container publishing to 0.0.0.0", False,
     "audit-only: a container runtime writes its own forward rules and "
     "bypasses the host firewall, so the fix is app config — publish to "
     "127.0.0.1:PORT, not PORT"),
    ("host-firewall-layer2", "host firewall active and default-deny", True,
     "`ufw default deny incoming && ufw enable`, or the nftables equivalent. "
     "Layer 2 only: it is never the perimeter, the cloud firewall is"),
    ("patch-unattended-upgrades", "unattended-upgrades on with security "
     "origins", True,
     "`dpkg-reconfigure -plow unattended-upgrades` and confirm the security "
     "origin pattern in /etc/apt/apt.conf.d/50unattended-upgrades"),
    ("patch-auto-reboot", 'Unattended-Upgrade::Automatic-Reboot "false"',
     True, 'set Automatic-Reboot "false": a box that reboots itself at 06:00 '
     "is an outage you did not schedule"),
    ("ips-sshd-jail", "fail2ban or sshguard sshd jail active", True,
     "install fail2ban, enable the sshd jail, `fail2ban-client status sshd`"),
    ("ips-ignoreip", "jail ignoreip covers every admin CIDR", True,
     "add every admin CIDR to ignoreip before the jail is enabled: a jail "
     "that can ban you is itself a lockout"),
    ("root-password-locked", "root password locked", True,
     "`passwd -l root` and confirm `passwd -S root` shows L"),
    ("time-sync", "time synchronisation active", True,
     "`timedatectl set-ntp true`; every log correlation and every "
     "certificate check downstream depends on it"),
    ("backup-enabled", "Cloud Backups enabled", False,
     "audit-only because it costs money: enable Backups on the server and "
     "accept the surcharge printed above, or state the restore path you "
     "actually have"),
    ("backup-snapshot-age", "newest backup or snapshot within policy age",
     False, "take a snapshot, or fix the schedule; an enabled backup with no "
     "recent image is the worst of both"),
    ("oob-escape", "out-of-band escape verified", False,
     "open the Hetzner Cloud Console for this server and confirm a login "
     "prompt, or verify the rescue system boots. Until this passes, no "
     "auto-fix in this report may be applied"),
]

# item id, sysctl keys, mode, wanted value. Keys under net.ipv6. are optional:
# a kernel with IPv6 disabled has no knob and that is not a finding.
SYSCTL_ITEMS: list[tuple[str, list[str], str, int]] = [
    ("sysctl-tcp-syncookies", ["net.ipv4.tcp_syncookies"], "eq", 1),
    ("sysctl-rp-filter", ["net.ipv4.conf.all.rp_filter",
                          "net.ipv4.conf.default.rp_filter"], "eq", 1),
    ("sysctl-accept-redirects", ["net.ipv4.conf.all.accept_redirects",
                                 "net.ipv4.conf.default.accept_redirects",
                                 "net.ipv6.conf.all.accept_redirects",
                                 "net.ipv6.conf.default.accept_redirects"],
     "eq", 0),
    ("sysctl-send-redirects", ["net.ipv4.conf.all.send_redirects",
                               "net.ipv4.conf.default.send_redirects"],
     "eq", 0),
    ("sysctl-accept-source-route",
     ["net.ipv4.conf.all.accept_source_route",
      "net.ipv4.conf.default.accept_source_route",
      "net.ipv6.conf.all.accept_source_route"], "eq", 0),
    ("sysctl-log-martians", ["net.ipv4.conf.all.log_martians",
                             "net.ipv4.conf.default.log_martians"], "eq", 1),
    ("sysctl-kptr-restrict", ["kernel.kptr_restrict"], "min", 2),
    ("sysctl-dmesg-restrict", ["kernel.dmesg_restrict"], "eq", 1),
    ("sysctl-unprivileged-bpf", ["kernel.unprivileged_bpf_disabled"],
     "min", 1),
    ("sysctl-ptrace-scope", ["kernel.yama.ptrace_scope"], "min", 1),
]
SYSCTL_FIX = ("write the key to /etc/sysctl.d/60-baseline.conf and "
              "`sysctl --system`")

# The kernel items are generated rather than typed twice: the table above is
# the single place a knob's wanted value lives. They are spliced in ahead of
# the host items so the report reads network, kernel, host, account.
_SPLICE = [i for i, row in enumerate(ITEMS)
           if row[0] == "root-password-locked"][0]
ITEMS[_SPLICE:_SPLICE] = [
    (item, f"{keys[0]} {'at least' if mode == 'min' else 'exactly'} {want}",
     True, f"{SYSCTL_FIX} for {', '.join(keys)}")
    for item, keys, mode, want in SYSCTL_ITEMS
] + [("sysctl-ip-forward", "net.ipv4.ip_forward", False,
      "audit-only with an expected waiver: CIS wants 0 and every WireGuard "
      "hub or container host needs 1, so record a waiver with a reason and an "
      "expiry rather than deviating silently")]

SSH_ITEMS = {"sshd-root-login", "sshd-password-auth", "sshd-kbdinteractive",
             "sshd-pubkey", "sshd-max-auth-tries", "sshd-login-grace",
             "sshd-x11", "sshd-empty-passwords", "sshd-allowlist",
             "sshd-port"}

# --- fixtures. No network, no credential, no host contacted. -----------------
OK_SSHD = """port 22
permitrootlogin no
passwordauthentication no
kbdinteractiveauthentication no
pubkeyauthentication yes
maxauthtries 3
logingracetime 30
x11forwarding no
permitemptypasswords no
allowgroups sudo
"""
BAD_SSHD = OK_SSHD.replace("permitrootlogin no", "permitrootlogin yes") \
    .replace("passwordauthentication no", "passwordauthentication yes") \
    .replace("maxauthtries 3", "maxauthtries 6") \
    .replace("allowgroups sudo\n", "")
OK_SS = """tcp   LISTEN 0 4096 0.0.0.0:22   0.0.0.0:* users:(("sshd",pid=1,fd=3))
tcp   LISTEN 0 4096 [::]:443     [::]:*     users:(("nginx",pid=2,fd=6))
tcp   LISTEN 0 4096 127.0.0.1:5432 0.0.0.0:* users:(("postgres",pid=3,fd=7))
"""
BAD_SS = OK_SS + (
    'tcp   LISTEN 0 4096 0.0.0.0:8080 0.0.0.0:* '
    'users:(("docker-proxy",pid=9,fd=4))\n')
OK_SYSCTL = "\n".join(
    [f"{key} = {want}" for _id, keys, _m, want in SYSCTL_ITEMS
     for key in keys] + ["net.ipv4.ip_forward = 0"]) + "\n"
BAD_SYSCTL = OK_SYSCTL.replace("kernel.kptr_restrict = 2",
                               "kernel.kptr_restrict = 0") \
    .replace("net.ipv4.ip_forward = 0", "net.ipv4.ip_forward = 1")
OK_EVIDENCE = {
    "admin_user": {"name": "ops", "sudo": True, "key_session_verified": True},
    "host_firewall": {"tool": "ufw", "active": True,
                      "default_incoming": "deny"},
    "unattended_upgrades": {"enabled": True, "security_origins": True,
                            "automatic_reboot": "false"},
    "intrusion_prevention": {"tool": "fail2ban", "sshd_jail_active": True,
                             "ignoreip": ["127.0.0.1/8", "203.0.113.0/24"]},
    "root_password_locked": True,
    "time_sync": {"active": True, "source": "systemd-timesyncd"},
    "oob_escape": {"verified": True, "method": "hetzner cloud console"},
    "containers": [],
}
BAD_EVIDENCE = json.loads(json.dumps(OK_EVIDENCE))
BAD_EVIDENCE["intrusion_prevention"]["ignoreip"] = ["127.0.0.1/8"]
BAD_EVIDENCE["oob_escape"] = {"verified": False}
OK_SPEC = {
    "host": "box-1", "ssh_port": 22, "admin_cidrs": ["203.0.113.0/24"],
    "public_ports": [443], "firewall": "box-fw", "backup_max_age_days": 2,
}
OK_ACCOUNT = {
    "found": True, "name": "box-1", "id": 42, "backup_window": "22-02",
    "price_monthly": 20.0, "currency": "EUR",
    "newest_image": "2026-08-13T00:00:00+00:00",
    "firewall": {"found": True, "attached": True, "rules": [
        {"direction": "in", "protocol": "tcp", "port": "22",
         "source_ips": ["203.0.113.0/24"]},
        {"direction": "in", "protocol": "tcp", "port": "443",
         "source_ips": ["0.0.0.0/0", "::/0"]},
    ]},
}
BAD_ACCOUNT = json.loads(json.dumps(OK_ACCOUNT))
BAD_ACCOUNT["backup_window"] = None
BAD_ACCOUNT["firewall"]["rules"][0]["source_ips"] = ["0.0.0.0/0"]
TODAY = datetime.date(2026, 8, 14)


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


def parse_sshd(text: str) -> dict[str, list[str]]:
    """`sshd -T` output to {keyword: [value, ...]}. Keywords are lowercase."""
    out: dict[str, list[str]] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        out.setdefault(parts[0].lower(), []).append(
            parts[1].strip() if len(parts) > 1 else "")
    return out


def parse_listeners(text: str) -> list[dict]:
    """`ss -tulpnH` output to listener records. Malformed lines are skipped."""
    out: list[dict] = []
    for line in text.splitlines():
        fields = line.split()
        if len(fields) < 5:
            continue
        local = fields[4]
        if ":" not in local:
            continue
        addr, _sep, port = local.rpartition(":")
        if not port.isdigit():
            continue
        users = " ".join(fields[6:]) if len(fields) > 6 else ""
        out.append({"proto": fields[0], "addr": addr.strip("[]") or "*",
                    "port": int(port), "users": users,
                    "public": addr in PUBLIC_ADDRS or addr.strip("[]") in
                    ("::", "0.0.0.0", "*")})
    return out


def parse_sysctl(text: str) -> dict[str, str]:
    """`sysctl -a` output to {key: value}."""
    out: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, _sep, value = line.partition("=")
        out[key.strip()] = value.strip()
    return out


def as_network(value) -> ipaddress.IPv4Network | ipaddress.IPv6Network | None:
    """A CIDR, or None when the text is not one. Never raises."""
    try:
        return ipaddress.ip_network(str(value).strip(), strict=False)
    except (TypeError, ValueError):
        return None


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


def cidr_covers(outer, inner) -> bool:
    """True when `outer` contains `inner`.

    Containment is decided WITHIN a family and never across one. `subnet_of`
    raises TypeError on a mixed pair, so the families are compared first: a v4
    allowlist does not cover a v6 arrival, and saying so as False rather than
    as a traceback is what keeps a reachability proof a proof."""
    big, small = as_network(outer), as_network(inner)
    if big is None or small is None or big.version != small.version:
        return False
    return small.subnet_of(big)


def port_covers(spec_port: str | None, port: int) -> bool:
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


def resolve_spec(doc: dict, host: str | None) -> dict | str:
    """The effective baseline for one host, or one error string."""
    hosts = doc.get("hosts") or {}
    name = host or doc.get("host")
    if not name and len(hosts) == 1:
        name = next(iter(hosts))
    if not name:
        return "no host: pass --host or set `host` in the spec"
    if hosts and name not in hosts and host:
        return f"the spec has no host named {name}"
    spec = {"host": name, "ssh_port": 22, "admin_cidrs": [],
            "public_ports": [], "firewall": None, "backup_max_age_days": 2}
    for source in (doc, hosts.get(name) or {}):
        for key in list(spec):
            if key != "host" and key in source:
                spec[key] = source[key]
    if not spec["admin_cidrs"]:
        return "spec.admin_cidrs is empty; half this baseline is meaningless"
    for cidr in spec["admin_cidrs"]:
        if as_network(cidr) is None:
            return f"spec.admin_cidrs holds {cidr!r}, which is not a CIDR"
    # Every number is coerced here and nowhere else. A spec that says
    # "http" or null must come back as one error the caller can fix, not as a
    # ValueError halfway through an audit that has already printed findings.
    try:
        spec["public_ports"] = sorted({int(p) for p in spec["public_ports"]})
        spec["ssh_port"] = int(spec["ssh_port"])
        spec["backup_max_age_days"] = int(spec["backup_max_age_days"])
    except (TypeError, ValueError) as exc:
        return f"spec has a non-numeric port, age or host list: {exc}"
    return spec


def load_waivers(doc: dict, extra: object) -> list[dict] | str:
    """Waivers from the spec, replaced by --waivers when given."""
    raw = doc.get("waivers") or []
    if extra is not None:
        raw = extra.get("waivers") if isinstance(extra, dict) else extra
    if not isinstance(raw, list):
        return "waivers must be a JSON list of {item, reason, expires}"
    for entry in raw:
        if not isinstance(entry, dict) or not entry.get("item") \
                or not entry.get("reason") or not entry.get("expires"):
            return f"waiver {entry!r} needs item, reason and expires"
        try:
            datetime.date.fromisoformat(str(entry["expires"]))
        except ValueError:
            return f"waiver {entry['item']}: expires is not a YYYY-MM-DD date"
    return list(raw)


def check_sshd(conf: dict[str, list[str]], spec: dict) -> dict:
    """Every sshd item. Pure. An absent keyword is unmet, never assumed."""
    out: dict[str, tuple[str, str]] = {}
    if not conf:
        return {i: ("unknown", "no sshd evidence supplied")
                for i in sorted(SSH_ITEMS) if i != "sshd-port"} | \
            {"sshd-port": ("unknown", "no sshd evidence supplied")}
    wanted = {"sshd-root-login": ("permitrootlogin", "no"),
              "sshd-password-auth": ("passwordauthentication", "no"),
              "sshd-kbdinteractive": ("kbdinteractiveauthentication", "no"),
              "sshd-pubkey": ("pubkeyauthentication", "yes"),
              "sshd-x11": ("x11forwarding", "no"),
              "sshd-empty-passwords": ("permitemptypasswords", "no")}
    for item, (key, want) in wanted.items():
        got = (conf.get(key) or [""])[0].lower()
        if not got:
            out[item] = ("fail", f"{key} is not in the sshd evidence")
        elif got == want:
            out[item] = ("ok", f"{key} {got}")
        else:
            out[item] = ("fail", f"{key} {got}, baseline wants {want}")
    for item, key, ceiling in (("sshd-max-auth-tries", "maxauthtries", 3),
                               ("sshd-login-grace", "logingracetime", 30)):
        raw = (conf.get(key) or [""])[0]
        if not raw.isdigit():
            out[item] = ("fail", f"{key} is missing or not a number")
        elif int(raw) == 0 or int(raw) > ceiling:
            out[item] = ("fail", f"{key} {raw}, baseline wants at most "
                                 f"{ceiling} and never 0")
        else:
            out[item] = ("ok", f"{key} {raw}")
    allow = (conf.get("allowusers") or []) + (conf.get("allowgroups") or [])
    out["sshd-allowlist"] = ("ok", "allowlist present") if allow else (
        "fail", "no AllowUsers or AllowGroups; audit-only, add it by hand "
                "with a second session open")
    port = (conf.get("port") or ["22"])[0]
    want_port = str(spec["ssh_port"])
    out["sshd-port"] = ("ok", f"port {port}") if port == want_port else (
        "fail", f"port {port}, spec says {want_port}")
    return out


def check_listeners(records: list[dict] | None, spec: dict) -> dict:
    """Public listeners against the spec, plus container publishing."""
    if records is None:
        return {"net-public-listeners": ("unknown", "no listener evidence"),
                "net-container-publish": ("unknown", "no listener evidence")}
    allowed = set(spec["public_ports"]) | {int(spec["ssh_port"])}
    stray = sorted({r["port"] for r in records
                    if r["public"] and r["port"] not in allowed})
    out = {"net-public-listeners": ("ok", "no undeclared public listener")}
    if stray:
        out["net-public-listeners"] = (
            "fail", "undeclared public ports " +
            ",".join(str(p) for p in stray))
    published = sorted({r["port"] for r in records if r["public"] and
                        ("docker-proxy" in r["users"] or
                         "containerd" in r["users"] or "podman" in r["users"])})
    out["net-container-publish"] = ("ok", "no container on 0.0.0.0")
    if published:
        out["net-container-publish"] = (
            "fail", "container runtime publishes " +
            ",".join(str(p) for p in published) +
            " on 0.0.0.0 and writes its own forward rules")
    return out


def check_sysctl(values: dict[str, str] | None, waived_forward: bool) -> dict:
    """The kernel knobs, plus ip_forward as an audit-only expected waiver."""
    if values is None:
        return {item: ("unknown", "no sysctl evidence")
                for item, *_rest in SYSCTL_ITEMS} | \
            {"sysctl-ip-forward": ("unknown", "no sysctl evidence")}
    out: dict[str, tuple[str, str]] = {}
    for item, keys, mode, want in SYSCTL_ITEMS:
        bad: list[str] = []
        for key in keys:
            raw = values.get(key)
            if raw is None:
                if not key.startswith("net.ipv6."):
                    bad.append(f"{key} unset")
                continue
            head = raw.split()[0] if raw.split() else ""
            if not head.lstrip("-").isdigit():
                bad.append(f"{key}={raw}")
            elif (int(head) != want) if mode == "eq" else (int(head) < want):
                bad.append(f"{key}={head} wants {'>=' if mode == 'min' else ''}"
                           f"{want}")
        out[item] = ("fail", "; ".join(bad)) if bad else ("ok", f"= {want}")
    forward = values.get("net.ipv4.ip_forward", "")
    if forward.strip() == "0":
        out["sysctl-ip-forward"] = ("ok", "ip_forward 0")
    elif waived_forward:
        out["sysctl-ip-forward"] = ("ok", "ip_forward 1, waived")
    else:
        out["sysctl-ip-forward"] = (
            "fail", "ip_forward 1 and no waiver: CIS wants 0, a WireGuard hub "
                    "or container host needs 1 — waive it deliberately")
    return out


def check_evidence(ev: dict | None, spec: dict) -> dict:
    """The attestations no single command produces."""
    if ev is None:
        return {i: ("unknown", "no attestation evidence")
                for i in ("ssh-admin-session", "host-firewall-layer2",
                          "patch-unattended-upgrades", "patch-auto-reboot",
                          "ips-sshd-jail", "ips-ignoreip",
                          "root-password-locked", "time-sync", "oob-escape")}
    out: dict[str, tuple[str, str]] = {}
    admin = ev.get("admin_user") or {}
    if admin.get("sudo") and admin.get("key_session_verified") and \
            admin.get("name") not in (None, "", "root"):
        out["ssh-admin-session"] = ("ok", f"{admin['name']} sudo + key")
    else:
        out["ssh-admin-session"] = (
            "fail", "no proven sudo non-root key session; every SSH fix below "
                    "is on hold until there is one")
    hfw = ev.get("host_firewall") or {}
    if hfw.get("active") and str(hfw.get("default_incoming", "")).lower() in \
            ("deny", "drop", "reject"):
        out["host-firewall-layer2"] = ("ok", f"{hfw.get('tool', '?')} deny")
    else:
        out["host-firewall-layer2"] = (
            "fail", "host firewall absent or not default-deny (layer 2 only)")
    uu = ev.get("unattended_upgrades") or {}
    if uu.get("enabled") and uu.get("security_origins"):
        out["patch-unattended-upgrades"] = ("ok", "on with security origins")
    else:
        out["patch-unattended-upgrades"] = (
            "fail", "unattended-upgrades off or without a security origin")
    reboot = str(uu.get("automatic_reboot", "")).strip().lower()
    out["patch-auto-reboot"] = ("ok", 'Automatic-Reboot "false"') if \
        reboot == "false" else (
        "fail", f"Automatic-Reboot {reboot or 'unset'}, baseline wants false")
    ips = ev.get("intrusion_prevention") or {}
    if ips.get("sshd_jail_active"):
        out["ips-sshd-jail"] = ("ok", f"{ips.get('tool', '?')} sshd jail")
    else:
        out["ips-sshd-jail"] = ("fail", "no active sshd jail")
    ignore = [str(c) for c in (ips.get("ignoreip") or [])]
    missing = [c for c in spec["admin_cidrs"]
               if not any(cidr_covers(i, c) for i in ignore)]
    if ips.get("sshd_jail_active") and missing:
        out["ips-ignoreip"] = (
            "fail", "ignoreip does not cover " + ",".join(missing) +
                    " — a jail that can ban you is itself a lockout")
    elif not ips.get("sshd_jail_active"):
        out["ips-ignoreip"] = ("fail", "no jail, so no ignoreip to check")
    else:
        out["ips-ignoreip"] = ("ok", "ignoreip covers every admin CIDR")
    out["root-password-locked"] = ("ok", "locked") if \
        ev.get("root_password_locked") is True else (
        "fail", "root password not proven locked")
    sync = ev.get("time_sync") or {}
    out["time-sync"] = ("ok", str(sync.get("source", "active"))) if \
        sync.get("active") else ("fail", "time synchronisation not active")
    oob = ev.get("oob_escape") or {}
    out["oob-escape"] = ("ok", str(oob.get("method", "verified"))) if \
        oob.get("verified") else (
        "fail", "no verified console or rescue escape; do not harden SSH on a "
                "box you cannot reach another way")
    return out


def check_account(account: dict, spec: dict, today: datetime.date) -> dict:
    """The API side: firewall shape, backups, snapshot age."""
    out: dict[str, tuple[str, str]] = {}
    fw = account.get("firewall") or {}
    if not spec.get("firewall"):
        out["fw-cloud-attached"] = ("fail", "spec names no firewall")
        out["fw-default-deny"] = ("fail", "spec names no firewall")
        out["fw-ssh-restricted"] = ("fail", "spec names no firewall")
        return out | check_backups(account, spec, today)
    if not fw.get("found"):
        detail = f"no firewall named {spec['firewall']} in this project"
    elif not fw.get("attached"):
        detail = f"{spec['firewall']} exists and is not applied to this server"
    else:
        detail = ""
    out["fw-cloud-attached"] = ("ok", f"{spec['firewall']} attached") if \
        not detail else ("fail", detail)
    rules = [r for r in (fw.get("rules") or []) if r.get("direction") == "in"]
    if not fw.get("found"):
        out["fw-default-deny"] = ("fail", "no firewall, so no default deny")
        out["fw-ssh-restricted"] = ("fail", "no firewall, SSH is open to all")
        return out | check_backups(account, spec, today)
    allowed = set(spec["public_ports"]) | {int(spec["ssh_port"])}
    stray = []
    for rule in rules:
        if rule.get("protocol") not in ("tcp", "udp"):
            stray.append(f"{rule.get('protocol')} rule with no port bound")
            continue
        opened = [p for p in allowed if port_covers(rule.get("port"), p)]
        if not opened:
            stray.append(f"{rule.get('protocol')}/{rule.get('port')} is not a "
                         "declared public port")
    out["fw-default-deny"] = ("fail", "; ".join(stray)) if stray else (
        "ok", f"{len(rules)} inbound rules, all declared")
    ssh_port = int(spec["ssh_port"])
    ssh_rules = [r for r in rules if r.get("protocol") == "tcp"
                 and port_covers(r.get("port"), ssh_port)]
    wide = [s for r in ssh_rules for s in (r.get("source_ips") or [])
            if s.strip() in ("0.0.0.0/0", "::/0")]
    uncovered = [s for r in ssh_rules for s in (r.get("source_ips") or [])
                 if s.strip() not in ("0.0.0.0/0", "::/0") and
                 not any(cidr_covers(c, s) for c in spec["admin_cidrs"])]
    if not ssh_rules:
        out["fw-ssh-restricted"] = ("fail", f"no inbound tcp/{ssh_port} rule; "
                                            "SSH is unreachable through this "
                                            "firewall")
    elif wide:
        out["fw-ssh-restricted"] = ("fail", f"tcp/{ssh_port} open to " +
                                    ",".join(sorted(set(wide))))
    elif uncovered:
        out["fw-ssh-restricted"] = (
            "fail", f"tcp/{ssh_port} allows " + ",".join(sorted(set(uncovered)))
            + " which is outside admin_cidrs")
    else:
        out["fw-ssh-restricted"] = ("ok", f"tcp/{ssh_port} from admin_cidrs")
    return out | check_backups(account, spec, today)


def check_backups(account: dict, spec: dict, today: datetime.date) -> dict:
    """Backups and snapshot age. The cost is part of the detail on purpose."""
    # An absent or unparseable price is reported as unknown, never dropped:
    # money the caller cannot see is money the caller does not decide about.
    try:
        raw = account.get("price_monthly")
        price = None if raw is None else float(raw)
    except (TypeError, ValueError):
        price = None
    cost = (f"; monthly price unknown, Backups add "
            f"{int(BACKUP_SURCHARGE * 100)}%") if price is None else (
        f"; +{account.get('currency', '')} "
        f"{price * BACKUP_SURCHARGE:.2f}/mo, {int(BACKUP_SURCHARGE * 100)}% of "
        f"{account.get('currency', '')} {price:.2f}")
    out = {"backup-enabled": ("ok", f"backup window "
                                    f"{account.get('backup_window')}{cost}")}
    if not account.get("backup_window"):
        out["backup-enabled"] = ("fail", f"Cloud Backups off{cost}")
    newest = account.get("newest_image")
    limit = int(spec["backup_max_age_days"])
    if not newest:
        out["backup-snapshot-age"] = (
            "fail", f"no backup or snapshot bound to this server, policy is "
                    f"{limit} days")
        return out
    try:
        made = datetime.datetime.fromisoformat(
            str(newest).replace("Z", "+00:00")).date()
    except ValueError:
        return out | {"backup-snapshot-age": ("fail",
                                              f"unparseable image date "
                                              f"{newest!r}")}
    age = (today - made).days
    out["backup-snapshot-age"] = ("ok", f"newest image {age}d old") if \
        age <= limit else ("fail", f"newest image {age}d old, policy is "
                                   f"{limit}d")
    return out


def audit(spec: dict, sshd: dict, listeners: list[dict] | None,
          sysctl: dict[str, str] | None, evidence: dict | None,
          account: dict, waived: set[str],
          today: datetime.date) -> dict[str, tuple[str, str]]:
    """Every item's status. Pure: no I/O, no exits, no clock of its own."""
    results: dict[str, tuple[str, str]] = {}
    results.update(check_sshd(sshd, spec))
    results.update(check_listeners(listeners, spec))
    results.update(check_sysctl(sysctl, "sysctl-ip-forward" in waived))
    results.update(check_evidence(evidence, spec))
    results.update(check_account(account, spec, today))
    if results.get("host-firewall-layer2", ("", ""))[0] == "ok" and \
            results.get("fw-cloud-attached", ("", ""))[0] != "ok":
        results["host-firewall-layer2"] = (
            "fail", "layer 2 is up and layer 1 is not; a host firewall is "
                    "never the perimeter")
    return results


def verdict(results: dict, waivers: list[dict],
            today: datetime.date) -> dict:
    """Fold waivers into the results and decide the run's outcome. Pure.

    An expired waiver over an item that passes anyway is bookkeeping and one
    finding. An expired waiver over an item that FAILS is a stale exception
    suppressing a live failure, and the run refuses rather than reporting a
    number nobody can trust."""
    known = {item for item, *_r in ITEMS}
    final = dict(results)
    notes: list[str] = []
    refusals: list[str] = []
    for entry in waivers:
        item = str(entry["item"])
        expires = datetime.date.fromisoformat(str(entry["expires"]))
        if item not in known:
            notes.append(f"waiver names unknown item {item}")
            continue
        status = final.get(item, ("unknown", ""))[0]
        if expires < today:
            if status == "ok":
                notes.append(f"waiver {item} expired {expires} and the item "
                             "passes anyway; delete it")
            else:
                refusals.append(
                    f"waiver {item} expired {expires} and the item still "
                    f"fails: {final.get(item, ('', ''))[1]}")
            continue
        if status == "ok":
            notes.append(f"waiver {item} is not needed, the item passes")
        else:
            final[item] = ("waived", f"{final[item][1]} [waived until "
                                     f"{expires}: {entry['reason']}]")
    failed = sorted(i for i, (s, _d) in final.items() if s != "ok"
                    and s != "waived")
    auto = {i for i, _t, is_auto, _f in ITEMS if is_auto}
    oob_ok = final.get("oob-escape", ("", ""))[0] in ("ok", "waived")
    held = sorted(i for i in failed if i in auto) if not oob_ok else []
    return {"results": final, "failed": failed, "notes": notes,
            "refusals": refusals, "held": held, "oob_ok": oob_ok}


def exit_code(out: dict) -> int:
    """The exit status for a completed audit. Pure, so the self-test can
    assert that a stale waiver and a held auto-fix both come back as the
    guard refusal rather than as an ordinary finding."""
    if out["refusals"] or out["held"]:
        return 5
    return 1 if out["failed"] else 0


def report(spec: dict, out: dict) -> str:
    """The full table. Never stdout: a network tool that fills a screen has
    failed its purpose."""
    final = out["results"]
    lines = [f"# {NAME}: {spec['host']}", "",
             "| item | class | status | detail |", "|---|---|---|---|"]
    for item, title, is_auto, _fix in ITEMS:
        status, detail = final.get(item, ("unknown", "not evaluated"))
        lines.append(f"| {item} | {'auto' if is_auto else 'audit-only'} | "
                     f"{status} | {title}: {detail} |")
    lines += ["", "## remediation", ""]
    ssh_blocked = final.get("ssh-admin-session", ("", ""))[0] != "ok"
    for item, _title, is_auto, fix in ITEMS:
        if final.get(item, ("unknown", ""))[0] in ("ok", "waived"):
            continue
        mark = "AUTO"
        if not is_auto:
            mark = "AUDIT-ONLY"
        elif not out["oob_ok"]:
            mark = "HOLD (no verified out-of-band escape)"
        elif ssh_blocked and item in SSH_ITEMS:
            mark = "HOLD (no proven key session)"
        lines.append(f"- [{mark}] {item}: {fix}")
    lines += ["", "## waivers", ""]
    lines += [f"- {n}" for n in out["notes"] + out["refusals"]] or ["- none"]
    return "\n".join(lines) + "\n"


def call(path: str, token: str, sleeper=time.sleep, retried: bool = False):
    """One GET, with a single wait to RateLimit-Reset and never a spin."""
    request = urllib.request.Request(API + path, method="GET")
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/json")
    opener = urllib.request.build_opener(SameHostRedirect)
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
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
            return call(path, token, sleeper, True)
        raise ApiError(6, f"api {exc.code} on {path}")
    except (urllib.error.URLError, OSError) as exc:
        raise ApiError(2, f"cannot reach the api: {exc}")
    except ValueError:
        raise ApiError(6, f"api returned unparseable json on {path}")


def gather(spec: dict, token: str) -> dict:
    """The account side in four GETs. I/O only; the rules live in check_*."""
    name = urllib.parse.quote(str(spec["host"]))
    body = call(f"/servers?name={name}&per_page={PER_PAGE}", token)
    servers = body.get("servers") or []
    if not servers:
        raise ApiError(2, f"no server named {spec['host']} in this project")
    server = servers[0]
    price = None
    currency = ""
    location = ((server.get("datacenter") or {}).get("location") or {}
                ).get("name")
    for entry in ((server.get("server_type") or {}).get("prices") or []):
        if entry.get("location") == location or price is None:
            gross = (entry.get("price_monthly") or {}).get("gross")
            try:
                price = float(gross)
                currency = entry.get("price_monthly", {}).get(
                    "currency", "EUR") or "EUR"
            except (TypeError, ValueError):
                price = None
    account = {"found": True, "name": server.get("name"), "id": server.get("id"),
               "backup_window": server.get("backup_window"),
               "price_monthly": price, "currency": currency,
               "newest_image": None, "firewall": {"found": False}}
    if spec.get("firewall"):
        fwname = urllib.parse.quote(str(spec["firewall"]))
        fwbody = call(f"/firewalls?name={fwname}&per_page={PER_PAGE}", token)
        walls = fwbody.get("firewalls") or []
        if walls:
            applied = walls[0].get("applied_to") or []
            attached = any(
                (a.get("server") or {}).get("id") == server.get("id")
                for a in applied)
            account["firewall"] = {"found": True, "attached": attached,
                                   "rules": walls[0].get("rules") or []}
    stamps: list[str] = []
    for query in (f"/images?type=backup&bound_to={server.get('id')}"
                  f"&sort=created:desc&per_page={PER_PAGE}",
                  f"/images?type=snapshot&sort=created:desc"
                  f"&per_page={PER_PAGE}"):
        for image in (call(query, token).get("images") or []):
            source = (image.get("created_from") or {}).get("id")
            if image.get("type") == "snapshot" and source != server.get("id"):
                continue
            if image.get("created"):
                stamps.append(str(image["created"]))
    account["newest_image"] = max(stamps) if stamps else None
    return account


def self_test() -> list[str]:
    """Prove parsing, every rule family, the waiver logic and the report.
    Makes no network call and needs no credential."""
    failures: list[str] = []
    spec = resolve_spec({"hosts": {"box-1": OK_SPEC}}, None)
    if not isinstance(spec, dict) or spec["host"] != "box-1":
        return [f"the ok spec did not resolve: {spec}"]
    if not isinstance(resolve_spec({"host": "x"}, None), str):
        failures.append("a spec with no admin_cidrs was accepted")

    good = audit(spec, parse_sshd(OK_SSHD), parse_listeners(OK_SS),
                 parse_sysctl(OK_SYSCTL), OK_EVIDENCE, OK_ACCOUNT,
                 set(), TODAY)
    bad = audit(spec, parse_sshd(BAD_SSHD), parse_listeners(BAD_SS),
                parse_sysctl(BAD_SYSCTL), BAD_EVIDENCE, BAD_ACCOUNT,
                set(), TODAY)
    if len(good) != len(ITEMS):
        failures.append(f"audit produced {len(good)} of {len(ITEMS)} items")
    clean = verdict(good, [], TODAY)
    if clean["failed"]:
        failures.append(f"the ok fixture failed: {clean['failed']}")
    dirty = verdict(bad, [], TODAY)
    for expected in ("sshd-root-login", "sshd-password-auth",
                     "sshd-max-auth-tries", "sshd-allowlist",
                     "net-public-listeners", "net-container-publish",
                     "sysctl-kptr-restrict", "sysctl-ip-forward",
                     "ips-ignoreip", "oob-escape", "fw-ssh-restricted",
                     "backup-enabled"):
        if expected not in dirty["failed"]:
            failures.append(f"the bad fixture did not fail {expected}")
    if dirty["oob_ok"] or not dirty["held"]:
        failures.append("an unverified out-of-band escape did not hold the "
                        "auto-fixes")
    if "sshd-root-login" not in dirty["held"]:
        failures.append("a failing auto item was not held")

    forgiven = verdict(audit(spec, parse_sshd(OK_SSHD),
                             parse_listeners(OK_SS), parse_sysctl(BAD_SYSCTL),
                             OK_EVIDENCE, OK_ACCOUNT,
                             {"sysctl-ip-forward"}, TODAY),
                       [{"item": "sysctl-kptr-restrict", "reason": "wg hub",
                         "expires": "2026-12-31"}], TODAY)
    if "sysctl-ip-forward" in forgiven["failed"]:
        failures.append("an expected ip_forward waiver did not apply")
    if "sysctl-kptr-restrict" in forgiven["failed"]:
        failures.append("a live waiver did not suppress its item")
    expired = verdict(bad, [{"item": "sysctl-kptr-restrict", "reason": "old",
                             "expires": "2026-01-01"}], TODAY)
    if not expired["refusals"]:
        failures.append("an expired waiver over a failing item did not refuse")
    stale = verdict(good, [{"item": "sshd-x11", "reason": "old",
                            "expires": "2026-01-01"}], TODAY)
    if stale["refusals"] or not stale["notes"]:
        failures.append("an expired waiver over a passing item was not a note")
    if not isinstance(load_waivers({}, [{"item": "x"}]), str):
        failures.append("a waiver with no reason or expires was accepted")

    listeners = parse_listeners(BAD_SS)
    if len(listeners) != 4 or listeners[2]["public"]:
        failures.append(f"listener parsing is wrong: {listeners}")
    if not cidr_covers("203.0.113.0/24", "203.0.113.7/32"):
        failures.append("a covering CIDR was not recognised")
    if cidr_covers("203.0.113.0/24", "198.51.100.7/32"):
        failures.append("a foreign CIDR was treated as covered")
    if cidr_covers("0.0.0.0/0", "::1/128"):
        failures.append("a v4 supernet was said to cover a v6 address")
    if not port_covers("80-443", 443) or port_covers("80-443", 8080):
        failures.append("port range coverage is wrong")
    # A dual-stack admin list is completely ordinary. Containment must be
    # decided per family and must never raise, and a v4-only allowlist must
    # NOT be read as covering a v6 admin range.
    mixed = resolve_spec(dict(OK_SPEC, admin_cidrs=["203.0.113.0/24",
                                                    "2001:db8:1::/64"]), None)
    if not isinstance(mixed, dict):
        failures.append(f"a dual-stack spec did not resolve: {mixed}")
    else:
        v4_only = json.loads(json.dumps(OK_EVIDENCE))
        v4_only["intrusion_prevention"]["ignoreip"] = ["203.0.113.0/24"]
        status, detail = check_evidence(v4_only, mixed)["ips-ignoreip"]
        if status != "fail" or "2001:db8:1::/64" not in detail:
            failures.append("a v4-only ignoreip was read as covering a v6 "
                            "admin range")
        both = json.loads(json.dumps(OK_EVIDENCE))
        both["intrusion_prevention"]["ignoreip"] = ["203.0.113.0/24",
                                                    "2001:db8::/32"]
        if check_evidence(both, mixed)["ips-ignoreip"][0] != "ok":
            failures.append("an ignoreip covering both families was rejected")

    # An absent field is "I could not determine this", never "it is fine".
    thin = {"found": True, "name": "box-1", "id": 42,
            "firewall": {"found": False}}
    lean = check_account(thin, spec, TODAY)
    if lean["backup-enabled"][0] != "fail" or \
            "price unknown" not in lean["backup-enabled"][1]:
        failures.append("an absent monthly price was not reported as unknown")
    if lean["backup-snapshot-age"][0] != "fail":
        failures.append("an absent image date was not a finding")
    if lean["fw-cloud-attached"][0] != "fail":
        failures.append("an absent firewall was not a finding")
    for broken in ({"host": "h", "admin_cidrs": ["nonsense"]},
                   {"host": "h", "admin_cidrs": ["203.0.113.0/24"],
                    "public_ports": ["http"]},
                   {"host": "h", "admin_cidrs": ["203.0.113.0/24"],
                    "backup_max_age_days": None}):
        if not isinstance(resolve_spec(broken, None), str):
            failures.append(f"a malformed spec was accepted: {broken}")

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
                call("/servers", "fixture-credential", slept.append)
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

    # The exit table, asserted rather than described. A clean run is 0, an
    # ordinary failing item is 1, and both guard refusals are 5.
    if exit_code(clean) != 0:
        failures.append("a clean audit did not map to exit 0")
    plain = verdict(audit(spec, parse_sshd(BAD_SSHD), parse_listeners(OK_SS),
                          parse_sysctl(OK_SYSCTL), OK_EVIDENCE, OK_ACCOUNT,
                          set(), TODAY), [], TODAY)
    if not plain["failed"] or plain["held"] or exit_code(plain) != 1:
        failures.append("a failing audit with a verified escape was not exit 1")
    if exit_code(dirty) != 5:
        failures.append("held auto-fixes did not map to the guard refusal, 5")
    if exit_code(expired) != 5:
        failures.append("an expired waiver over a failing item was not exit 5")

    text = report(spec, dirty)
    if "HOLD (no verified out-of-band escape)" not in text:
        failures.append("the report did not hold the auto-fixes")
    if "20% of" not in text:
        failures.append("the report did not print the backup surcharge")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", help="infra JSON: admin_cidrs, public_ports, "
                                   "ssh_port, firewall, hosts")
    ap.add_argument("--host", help="which host in the spec to audit")
    ap.add_argument("--waivers", help="JSON list of {item, reason, expires}")
    ap.add_argument("--sshd-config", dest="sshd", help="output of `sshd -T`")
    ap.add_argument("--listeners", help="output of `ss -tulpnH`")
    ap.add_argument("--sysctl", help="output of `sysctl -a`")
    ap.add_argument("--evidence", help="JSON of the attestations no single "
                                       "command produces")
    ap.add_argument("--report", help="write the full item table here")
    ap.add_argument("--json", action="store_true",
                    help="emit the summary line as one line of JSON")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit, offline")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=37 failures={len(failures)}")
        return 1 if failures else 0

    if not args.spec:
        print(f"{NAME}: --spec is required", file=sys.stderr)
        return 2
    try:
        doc = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        extra = None if not args.waivers else json.loads(
            Path(args.waivers).read_text(encoding="utf-8"))
        sshd = parse_sshd(Path(args.sshd).read_text(encoding="utf-8")) \
            if args.sshd else {}
        listeners = parse_listeners(
            Path(args.listeners).read_text(encoding="utf-8")) \
            if args.listeners else None
        sysctl = parse_sysctl(Path(args.sysctl).read_text(encoding="utf-8")) \
            if args.sysctl else None
        evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8")) \
            if args.evidence else None
    except (OSError, ValueError) as exc:
        print(f"{NAME}: cannot read an input: {exc}", file=sys.stderr)
        return 2

    spec = resolve_spec(doc, args.host)
    if isinstance(spec, str):
        print(f"{NAME}: {spec}", file=sys.stderr)
        return 2
    waivers = load_waivers(doc, extra)
    if isinstance(waivers, str):
        print(f"{NAME}: {waivers}", file=sys.stderr)
        return 2

    token = os.environ.get(ENV_VAR, "").strip()
    if not token:
        print(f"{NAME}: {ENV_VAR} is not set; the credential is read from the "
              "environment and there is no flag for it. The account-side items "
              "cannot be verified and a half-run baseline is not a baseline",
              file=sys.stderr)
        return 3

    today = datetime.date.today()
    live = {str(w["item"]) for w in waivers
            if datetime.date.fromisoformat(str(w["expires"])) >= today}
    try:
        account = gather(spec, token)
    except ApiError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return exc.code

    results = audit(spec, sshd, listeners, sysctl, evidence, account, live,
                    today)
    out = verdict(results, waivers, today)
    if args.report:
        try:
            Path(args.report).write_text(report(spec, out), encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write the report: {exc}", file=sys.stderr)
            return 2

    for item in out["failed"]:
        print(f"{NAME}: {item}: {out['results'][item][1]}", file=sys.stderr)
    for note in out["notes"]:
        print(f"{NAME}: note: {note}", file=sys.stderr)
    for refusal in out["refusals"]:
        print(f"{NAME}: refused: {refusal}", file=sys.stderr)
    if out["held"]:
        print(f"{NAME}: refused: no verified out-of-band escape, so "
              f"{len(out['held'])} auto-fixes are on hold", file=sys.stderr)

    waived = sum(1 for s, _d in out["results"].values() if s == "waived")
    summary = {"tool": NAME, "host": spec["host"], "checks": len(ITEMS),
               "failed": len(out["failed"]), "waived": waived,
               "held": len(out["held"]),
               "report": args.report or None}
    if args.json:
        print(json.dumps(summary, sort_keys=True))
    else:
        print(f"{NAME}: host={spec['host']} checks={len(ITEMS)} "
              f"failed={len(out['failed'])} waived={waived} "
              f"held={len(out['held'])} -> {args.report or 'no report'}")
    return exit_code(out)


if __name__ == "__main__":
    sys.exit(main())
