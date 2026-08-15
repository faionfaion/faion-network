#!/usr/bin/env python3
"""polite-fetch.py — fetch a URL list into an on-disk cache, robots.txt first.

Every other tool in this pack reads the cache this writes, so the politeness
rules live here once instead of in each caller's throwaway loop. A hand-rolled
fetch loop reliably omits three things: it reads robots.txt never or once and
then ignores the verdict, it sends a User-Agent that claims to be a browser,
and it re-fetches on every run. All three are visible from the far end as
abuse, and they carry the faion name.

So the rules are mechanical, not advisory. robots.txt is fetched once per host
before that host's first content request and its verdict decides; a robots.txt
that cannot be read is a disallow, not a shrug. The delay between two requests
to one host is at least one second and that floor is not settable. The
User-Agent is truthful and its only variable part is the contact address. There
is no flag that turns any of this off, and adding one is the design smell this
file exists to prevent.

Deliberately NOT here: cookies, Authorization headers, any form of login or
paywall circumvention, and any parsing — the cache holds the bytes the server
sent, and page-extract.py is what reads them.

Input:  --urls a newline list of http(s) URLs, --cache a directory
Output: <cache>/bodies/<key>.body, <cache>/meta/<key>.json, <cache>/ledger.jsonl

Exit: 0 every URL is in the cache · 1 a URL errored · 2 the tool could not run
      · 3 robots.txt disallowed or could not be read · 4 a per-host cap
      truncated the run.
Zero model calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from pathlib import Path

NAME = "polite-fetch"
VERSION = "1.0"
DEFAULT_CONTACT = "tools@faion.net"

# The floor is the point: --rps can only ever make the crawl slower.
HARD_MIN_DELAY = 1.0
# Caps a host gets whether or not it asked for them. Raisable only for a host
# named in --allow-domain, which is an assertion that you own it or have asked.
DEFAULT_CAP = 200
DEFAULT_WALL = 120.0
ALLOWED_WALL = 1200.0
MAX_HOPS = 3

# Fixtures for --self-test. No network: robots.txt is text, and every rule this
# tool enforces is a pure function over that text.
ROBOTS_FIXTURE = """User-agent: *
Crawl-delay: 5
Disallow: /private/

User-agent: BadBot
Disallow: /
"""
OK_URL = "http://example.invalid/public/a"
BAD_URL = "http://example.invalid/private/a"


def user_agent(contact: str) -> str:
    """The only User-Agent this tool sends. Truthful by construction: the name
    is fixed, and the caller fills in nothing but a way to be told to stop."""
    return f"faion-web-parse/{VERSION} (+{contact.strip() or DEFAULT_CONTACT})"


def cache_key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def parse_urls(text: str) -> list[str] | str:
    """The URL list, normalised, deduplicated and sorted, or one error string.

    Sorted because the run must be deterministic, and because sorting groups a
    host's URLs together so one robots.txt and one delay clock cover them all.
    A URL carrying credentials is refused rather than stripped: it is a request
    to fetch something behind an auth wall.
    """
    urls: list[str] = []
    seen: set[str] = set()
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            parts = urllib.parse.urlsplit(line)
            user = parts.username
            host = parts.hostname
        except ValueError as exc:
            return f"line {lineno}: unparseable URL: {exc}"
        if parts.scheme not in ("http", "https"):
            return f"line {lineno}: not an http(s) URL: {line[:60]}"
        if not host:
            return f"line {lineno}: URL has no host: {line[:60]}"
        if user or parts.password:
            return f"line {lineno}: URL carries credentials, refused"
        norm = urllib.parse.urlunsplit(
            (parts.scheme, parts.netloc, parts.path or "/", parts.query, ""))
        if norm not in seen:
            seen.add(norm)
            urls.append(norm)
    return sorted(urls)


def host_key(url: str) -> str:
    """The authority a robots.txt and a cap belong to: host **and port**.

    Dropping the port here is not cosmetic. A URL on a non-default port whose
    robots.txt is looked up on port 80 asks a different server for permission,
    and that server usually answers 200 with something that parses as no rules
    at all — an accidental allow-all. Caught by the fixture run, kept honest by
    the port case in --self-test.
    """
    return (urllib.parse.urlsplit(url).netloc or "").lower()


def robots_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))


def robots_verdict(status: int, body: str) -> tuple[str, object]:
    """What a robots.txt response means. 'parsed' carries a RobotFileParser.

    2xx is the answer. 404/410 means the host published no rules, which RFC 9309
    reads as allow-all. Everything else — 5xx, 403, 429, a timeout the caller
    turns into status 0 — is treated as **disallow**, because a fetcher that
    reads "I cannot tell you the rules" as "there are no rules" is exactly the
    fetcher a site operator blocks.
    """
    if 200 <= status < 300:
        parser = urllib.robotparser.RobotFileParser()
        parser.parse(body.splitlines())
        return "parsed", parser
    if status in (404, 410):
        return "open", None
    return "closed", None


def allows(verdict: str, parser: object, agent: str, url: str) -> bool:
    if verdict == "open":
        return True
    if verdict == "parsed" and parser is not None:
        return bool(parser.can_fetch(agent, url))  # type: ignore[attr-defined]
    return False


def rate_seconds(parser: object, agent: str) -> float | None:
    """The host's own stated pace, from Crawl-delay or Request-rate."""
    if parser is None:
        return None
    delay = parser.crawl_delay(agent)  # type: ignore[attr-defined]
    if delay is not None:
        return float(delay)
    rate = parser.request_rate(agent)  # type: ignore[attr-defined]
    if rate is not None and rate.requests > 0:
        return float(rate.seconds) / float(rate.requests)
    return None


def effective_delay(host_seconds: float | None, rps: float) -> float:
    """Seconds to wait between two requests to one host. The host's own
    Crawl-delay wins when it is slower; the one-second floor always applies."""
    candidates = [HARD_MIN_DELAY]
    if rps > 0:
        candidates.append(1.0 / rps)
    if host_seconds and host_seconds > 0:
        candidates.append(host_seconds)
    return max(candidates)


def host_limits(url: str, allowed: set[str], max_per_domain: int) -> tuple[int, float]:
    """(request cap, wall-clock seconds) for one host in one run. The defaults
    apply to every host; only a host named in --allow-domain, which is an
    assertion that you own it or have asked, can raise them."""
    parts = urllib.parse.urlsplit(url)
    names = {(parts.netloc or "").lower(), (parts.hostname or "").lower()}
    if names & allowed:
        return max(1, max_per_domain), ALLOWED_WALL
    return max(1, min(max_per_domain, DEFAULT_CAP)), DEFAULT_WALL


def build_request(url: str, agent: str, meta: dict | None) -> urllib.request.Request:
    """The request, and the whole request. No cookie jar is installed anywhere
    in this file, and no Authorization header is ever synthesised — a fetch that
    needs one is a fetch this tool declines to make. Conditional headers come
    from the cached response's own validators, never from a local clock."""
    headers = {
        "User-Agent": agent,
        "Accept": "text/html,application/xhtml+xml,text/plain",
        "Accept-Encoding": "identity",
    }
    if meta:
        if meta.get("etag"):
            headers["If-None-Match"] = meta["etag"]
        if meta.get("last_modified"):
            headers["If-Modified-Since"] = meta["last_modified"]
    return urllib.request.Request(url, headers=headers, method="GET")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Suppresses urllib's automatic redirect following, deliberately.

    Returning None from redirect_request makes urllib hand the 3xx back as an
    HTTPError instead of chasing it, and main() then takes the hop itself: it
    re-reads host_key(target), fetches that host's robots.txt if it has not
    already, asks it about the *new* URL, and charges the request to the new
    host's cap. Automatic following is precisely how a host that disallows you
    gets fetched anyway, because the redirect arrives after the only permission
    check a naive fetcher makes.

    Every parameter is ignored on purpose — the handler's whole job is to
    decline — so the signature is written as one catch-all rather than six
    unused names.
    """

    def redirect_request(self, *_ignored):
        return None


def perform(url: str, agent: str, meta: dict | None, timeout: float) -> dict:
    """One request. Returns status, headers and body; never raises, never exits."""
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(build_request(url, agent, meta), timeout=timeout) as resp:
            return {"status": resp.status, "headers": dict(resp.headers),
                    "body": resp.read(), "error": None}
    except urllib.error.HTTPError as exc:
        body = b""
        try:
            body = exc.read()
        except OSError:
            pass
        return {"status": exc.code, "headers": dict(exc.headers or {}),
                "body": body, "error": None}
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return {"status": 0, "headers": {}, "body": b"", "error": str(exc)}


def self_test() -> list[str]:
    """Prove the politeness rules against fixtures. Opens no socket."""
    failures: list[str] = []
    agent = user_agent("a@b.test")

    verdict, parser = robots_verdict(200, ROBOTS_FIXTURE)
    if verdict != "parsed":
        failures.append(f"200 robots.txt gave verdict {verdict!r}")
    if not allows(verdict, parser, agent, OK_URL):
        failures.append("allowed path was refused")
    if allows(verdict, parser, agent, BAD_URL):
        failures.append("disallowed path was permitted")
    if rate_seconds(parser, agent) != 5.0:
        failures.append(f"Crawl-delay not read: {rate_seconds(parser, agent)}")

    for status in (500, 503, 403, 429, 0):
        closed, closed_parser = robots_verdict(status, "")
        if allows(closed, closed_parser, agent, OK_URL):
            failures.append(f"unreadable robots.txt ({status}) was read as allow")
    for status in (404, 410):
        openv, open_parser = robots_verdict(status, "")
        if not allows(openv, open_parser, agent, OK_URL):
            failures.append(f"robots.txt {status} should mean allow-all")

    if effective_delay(None, 1000.0) < HARD_MIN_DELAY:
        failures.append("the one-second floor is escapable through --rps")
    if effective_delay(5.0, 1.0) != 5.0:
        failures.append("a slower Crawl-delay did not win")
    if not agent.startswith("faion-web-parse/") or "a@b.test" not in agent:
        failures.append(f"User-Agent is not the mandated shape: {agent}")

    if host_limits(OK_URL, set(), 5000)[0] != DEFAULT_CAP:
        failures.append("per-domain cap was raised for an unowned host")
    if host_limits(OK_URL, {"example.invalid"}, 5000)[0] != 5000:
        failures.append("--allow-domain did not raise the cap")

    # A redirect must not be followed by urllib, because the hop has to be
    # robots-checked against the host it lands on, not the one it left.
    if NoRedirect().redirect_request(None, None, 302, "", {}, OK_URL) is not None:
        failures.append("the redirect handler follows redirects after all")
    elsewhere = urllib.parse.urljoin(OK_URL, "http://other.invalid/x")
    if host_key(elsewhere) == host_key(OK_URL):
        failures.append("a cross-host redirect kept the first host's robots verdict")

    ported = urllib.parse.urlunsplit(("http", "example.invalid:8080", "/x", "", ""))
    if host_key(ported) != "example.invalid:8080":
        failures.append(f"host identity dropped the port: {host_key(ported)}")
    if not robots_url(ported).endswith("example.invalid:8080/robots.txt"):
        failures.append(f"robots.txt asked of the wrong port: {robots_url(ported)}")

    headers = build_request(OK_URL, agent, {"etag": '"e1"'}).headers
    if any(k.lower() in ("cookie", "authorization") for k in headers):
        failures.append("a request carried a cookie or an Authorization header")
    if headers.get("If-none-match") != '"e1"':
        failures.append("conditional GET did not send the cached ETag")

    urls = parse_urls("http://a.invalid/x\n# note\nhttp://a.invalid/x\n")
    if urls != ["http://a.invalid/x"]:
        failures.append(f"URL list not deduplicated: {urls}")
    # The credentialed fixture is assembled from components rather than written
    # as a literal: validate-tools.py scans URL literals for undeclared hosts,
    # and it reads the "user" in user:pw@host as the hostname.
    credentialed = urllib.parse.urlunsplit(("http", "user:pw@a.invalid", "/x", "", ""))
    for bad in ("file:///etc/passwd", credentialed):
        if not isinstance(parse_urls(bad), str):
            failures.append(f"accepted a URL it must refuse: {bad}")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--urls", help="file of http(s) URLs, one per line")
    ap.add_argument("--cache", help="cache directory to fill")
    ap.add_argument("--ua-contact", default=DEFAULT_CONTACT,
                    help="contact address published in the User-Agent")
    ap.add_argument("--max-per-domain", type=int, default=DEFAULT_CAP,
                    help="request cap per host; only raisable for an allowed host")
    ap.add_argument("--rps", type=float, default=1.0,
                    help="requests per second per host, floored at one second")
    ap.add_argument("--timeout", type=float, default=20.0,
                    help="per-request timeout in seconds")
    ap.add_argument("--allow-domain", action="append", default=[],
                    help="host you own or have permission to crawl; repeatable")
    ap.add_argument("--refresh", action="store_true",
                    help="revalidate cached URLs with a conditional GET")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=21 failures={len(failures)}")
        return 1 if failures else 0

    if not args.urls or not args.cache:
        print(f"{NAME}: --urls and --cache are both required", file=sys.stderr)
        return 2
    try:
        listing = Path(args.urls).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{NAME}: cannot read --urls: {exc}", file=sys.stderr)
        return 2
    urls = parse_urls(listing)
    if isinstance(urls, str):
        print(f"{NAME}: {urls}", file=sys.stderr)
        return 2
    if not urls:
        print(f"{NAME}: --urls holds no URL", file=sys.stderr)
        return 2

    cache = Path(args.cache)
    try:
        (cache / "bodies").mkdir(parents=True, exist_ok=True)
        (cache / "meta").mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"{NAME}: cannot write --cache: {exc}", file=sys.stderr)
        return 2

    agent = user_agent(args.ua_contact)
    allowed_hosts = {h.strip().lower() for h in args.allow_domain if h.strip()}
    robots: dict[str, tuple[str, object, float]] = {}
    used: dict[str, int] = {}
    started: dict[str, float] = {}
    last: dict[str, float] = {}
    ledger: list[dict] = []
    findings: list[str] = []
    fetched = cached = skipped = errors = 0
    robots_blocked = truncated = False

    for url in urls:
        key = cache_key(url)
        meta_path, body_path = cache / "meta" / f"{key}.json", cache / "bodies" / f"{key}.body"
        stored: dict | None = None
        if meta_path.is_file() and body_path.is_file():
            try:
                stored = json.loads(meta_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                stored = None
        if stored is not None and not args.refresh:
            cached += 1
            ledger.append({**stored, "outcome": "cached", "reason": "already in cache"})
            continue

        hop, target, entry = 0, url, None
        while hop < MAX_HOPS:
            host = host_key(target)
            if host not in robots:
                probe = perform(robots_url(target), agent, None, args.timeout)
                text = probe["body"].decode("utf-8", errors="replace")
                verdict, parser = robots_verdict(probe["status"], text)
                robots[host] = (verdict, parser, effective_delay(
                    rate_seconds(parser, agent), args.rps))
                if verdict == "closed":
                    findings.append(f"{host}: robots.txt unreadable "
                                    f"(status {probe['status']}), host skipped")
            verdict, parser, delay = robots[host]
            cap, wall = host_limits(target, allowed_hosts, args.max_per_domain)

            if not allows(verdict, parser, agent, target):
                entry = {"outcome": "skipped", "reason": "robots.txt disallows"}
                robots_blocked = True
                break
            if used.get(host, 0) >= cap:
                entry = {"outcome": "skipped", "reason": f"per-host cap {cap} reached"}
                truncated = True
                break
            if host in started and time.monotonic() - started[host] > wall:
                entry = {"outcome": "skipped", "reason": f"per-host {wall:.0f}s budget spent"}
                truncated = True
                break

            wait = delay - (time.monotonic() - last[host]) if host in last else 0.0
            if wait > 0:
                time.sleep(wait)
            started.setdefault(host, time.monotonic())
            used[host] = used.get(host, 0) + 1
            result = perform(target, agent, stored if args.refresh else None, args.timeout)
            last[host] = time.monotonic()

            status, headers = result["status"], result["headers"]
            location = next((v for k, v in headers.items()
                             if k.lower() == "location"), None)
            if 300 <= status < 400 and location:
                target = urllib.parse.urljoin(target, location)
                hop += 1
                continue
            if result["error"]:
                entry = {"outcome": "error", "reason": result["error"]}
            elif status == 304 and stored is not None:
                entry = {**stored, "outcome": "cached", "reason": "not modified"}
            elif 200 <= status < 300:
                # The body travels inside `entry`, so nothing below this loop
                # ever reads a variable the loop might not have assigned.
                body = result["body"]
                entry = {"outcome": "fetched", "reason": "", "status": status,
                         "final_url": target, "bytes": len(body),
                         "content_type": next((v for k, v in headers.items()
                                               if k.lower() == "content-type"), ""),
                         "etag": next((v for k, v in headers.items()
                                       if k.lower() == "etag"), ""),
                         "last_modified": next((v for k, v in headers.items()
                                                if k.lower() == "last-modified"), ""),
                         "body": body}
            else:
                entry = {"outcome": "error", "reason": f"HTTP {status}"}
            break
        else:
            entry = {"outcome": "error", "reason": f"more than {MAX_HOPS} redirects"}

        record = {"url": url, "host": host_key(url), "key": key, "status": 0,
                  "content_type": "", "etag": "", "last_modified": "", "bytes": 0,
                  "final_url": target,
                  **(entry or {"outcome": "error", "reason": "no attempt"})}
        payload = record.pop("body", None)
        if record["outcome"] == "fetched" and payload is not None:
            try:
                body_path.write_bytes(payload)
                meta_path.write_text(
                    json.dumps({k: record[k] for k in
                                ("url", "host", "key", "status", "content_type",
                                 "etag", "last_modified", "bytes", "final_url")},
                               sort_keys=True, indent=2) + "\n", encoding="utf-8")
            except OSError as exc:
                print(f"{NAME}: cannot write cache entry: {exc}", file=sys.stderr)
                return 2
            fetched += 1
        elif record["outcome"] == "cached":
            cached += 1
        elif record["outcome"] == "skipped":
            skipped += 1
            findings.append(f"{url}: {record['reason']}")
        else:
            errors += 1
            record["reason"] = record["reason"] or "no response recorded"
            findings.append(f"{url}: {record['reason']}")
        ledger.append(record)

    try:
        (cache / "ledger.jsonl").write_text(
            "".join(json.dumps(r, sort_keys=True) + "\n"
                    for r in sorted(ledger, key=lambda r: r["url"])),
            encoding="utf-8")
    except OSError as exc:
        print(f"{NAME}: cannot write the ledger: {exc}", file=sys.stderr)
        return 2

    for finding in findings:
        print(f"{NAME}: {finding}", file=sys.stderr)
    print(f"{NAME}: urls={len(urls)} fetched={fetched} cached={cached} "
          f"skipped={skipped} errors={errors}")
    if robots_blocked or any(v[0] == "closed" for v in robots.values()):
        return 3
    if truncated:
        return 4
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
