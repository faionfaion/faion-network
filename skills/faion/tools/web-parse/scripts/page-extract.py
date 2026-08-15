#!/usr/bin/env python3
"""page-extract.py — cached HTML into readable text plus its structured data.

The whole point is that the model never reads raw HTML. One pass per page emits
the prose and the machine-readable layer (JSON-LD, OpenGraph, microdata)
together, to a JSONL file; stdout stays one line.

The engineering that makes it trustworthy is the nesting fix.
`html.parser.HTMLParser` is a token stream, not a tree, and it does **not**
synthesise the end tags HTML5 implies: feed it `<ul><li>a<li>b</ul><p>x<p>y`
and it fires handle_endtag exactly once, for `ul`. Every unclosed `li` and `p`
then leaves the depth stack permanently wrong, and anything nesting-aware —
microdata scopes above all — silently mis-nests on most real pages. This file
fixes it in-tool with a fixed implied-end-tag table plus the void-element set,
applied before each push, and --self-test proves both the raw failure and the
fix. Pulling in beautifulsoup4 or lxml would have been the alternative; the
pack ships no dependencies, and forty deterministic lines are more auditable
than a parser nobody in the loop has read.

Charset: Content-Type, then a <meta charset> sniff of the first 2 KB, then
UTF-8 with errors="replace". No chardet.

Personal data is not an output. No email, phone or address field is ever
emitted from JSON-LD or microdata, and an email found in prose is redacted to
[email]: this tool reads public pages for what they say, not for who to contact.

Input:  --cache a directory filled by polite-fetch.py
Output: --out JSONL, one object per page; one summary line on stdout

Exit: 0 every page extracted · 1 a page fell under --min-text-len · 2 the tool
      could not run · 3 the cache ledger records a robots.txt skip, so the
      corpus is truncated · 4 a page parsed degraded (undecodable bytes,
      unusable JSON-LD, or a body that is not HTML).
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import codecs
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

NAME = "page-extract"

# Elements that never have an end tag, so they are never pushed.
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

# The implied-end-tag table: starting the key closes any of these that is open,
# repeatedly, before the key is pushed. This is the whole bug fix.
BLOCK_STARTS = {"address", "article", "aside", "blockquote", "details", "div",
                "dl", "fieldset", "figcaption", "figure", "footer", "form",
                "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "main",
                "nav", "ol", "p", "pre", "section", "table", "ul"}
CLOSED_BY = {tag: frozenset({"p"}) for tag in BLOCK_STARTS}
CLOSED_BY.update({
    "li": frozenset({"li", "p"}),
    "dd": frozenset({"dd", "dt", "p"}),
    "dt": frozenset({"dd", "dt", "p"}),
    "td": frozenset({"td", "th", "p"}),
    "th": frozenset({"td", "th", "p"}),
    "tr": frozenset({"tr", "td", "th", "p"}),
    "thead": frozenset({"thead", "tbody", "tfoot", "tr", "td", "th", "p"}),
    "tbody": frozenset({"thead", "tbody", "tfoot", "tr", "td", "th", "p"}),
    "tfoot": frozenset({"thead", "tbody", "tfoot", "tr", "td", "th", "p"}),
    "option": frozenset({"option"}),
    "rt": frozenset({"rt", "rp"}),
    "rp": frozenset({"rt", "rp"}),
})

SKIP = {"script", "style", "noscript", "template", "svg", "iframe", "head",
        "title"}
EMITTABLE = {"p", "li", "blockquote", "pre", "h1", "h2", "h3", "h4", "h5", "h6"}

# Never emitted, at any depth, from any structured block.
PII_KEYS = {"email", "telephone", "phone", "faxnumber", "address",
            "streetaddress", "postalcode", "postofficeboxnumber",
            "contactpoint", "mobile", "whatsapp"}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CT_CHARSET = re.compile(r"charset=([A-Za-z0-9_.:+-]+)", re.I)
META_CHARSET = re.compile(rb"""<meta[^>]*?charset=["']?([A-Za-z0-9_.:+-]+)""", re.I)
HTML_TYPES = ("text/html", "application/xhtml+xml", "text/plain")

# Fixtures for --self-test. MISNESTED is the case that would otherwise ship
# broken: not one of its `li` or `p` elements carries an end tag.
MISNESTED = "<ul><li>a<li>b</ul><p>x<p>y"
MICRODATA = ('<div itemscope itemtype="T"><span itemprop="name">N</span>'
             '<ul><li itemprop="k">a<li itemprop="k">b</ul>'
             '<meta itemprop="email" content="x@y.test"></div>')
JSONLD_OK = ('<script type="application/ld+json">{"@type":"Person",'
             '"name":"A","email":"a@b.test","telephone":"+1"}</script><p>body</p>')
JSONLD_BAD = '<script type="application/ld+json">{oops</script><p>body</p>'
PROSE = '<p>Write to a.person@example.test about it.</p>'


def is_html(content_type: str) -> bool:
    """Whether a cached body is worth parsing as markup.

    An empty Content-Type is treated as maybe-HTML and parsed; anything that
    names a type this tool does not read — a PDF, an image, a zip — is not.
    The subtlety worth a test: an empty string must not be folded into the
    prefix list, because every string starts with the empty string, and the
    guard then admits everything.
    """
    kind = content_type.split(";")[0].strip().lower()
    return not kind or kind.startswith(HTML_TYPES)


def redact(text: str) -> str:
    return EMAIL.sub("[email]", text)


def strip_pii(value):
    """Structured data minus every contact field, at any depth."""
    if isinstance(value, dict):
        return {k: strip_pii(v) for k, v in value.items()
                if k.lower().lstrip("@") not in PII_KEYS}
    if isinstance(value, list):
        return [strip_pii(v) for v in value]
    if isinstance(value, str):
        return redact(value)
    return value


def resolve_charset(content_type: str, head: bytes) -> str:
    """Content-Type, then a <meta charset> sniff of the first 2 KB, then UTF-8."""
    found = CT_CHARSET.search(content_type or "")
    if not found:
        found = META_CHARSET.search(head[:2048])
    name = found.group(1) if found else b"utf-8"
    if isinstance(name, bytes):
        name = name.decode("ascii", errors="replace")
    try:
        codecs.lookup(name)
    except LookupError:
        return "utf-8"
    return name


def decode(body: bytes, content_type: str) -> tuple[str, bool]:
    """(text, degraded). Degraded means bytes were replaced, so the text is lossy."""
    charset = resolve_charset(content_type, body)
    text = body.decode(charset, errors="replace")
    return text, "�" in text


class Doc(HTMLParser):
    """A depth-correct reader: prose blocks, OpenGraph, JSON-LD and microdata
    in one pass. `implied` counts the end tags HTMLParser never fires."""

    def __init__(self, markdown: bool = False):
        super().__init__(convert_charrefs=True)
        self.markdown = markdown
        self.stack: list[dict] = []
        self.blocks: list[tuple[str, str]] = []
        self.items: list[dict] = []
        self.jsonld: list = []
        self.og: dict[str, str] = {}
        self.title = ""
        self.lang = ""
        self.implied = 0
        self.degraded = 0
        self.skip = 0
        self.capture: list[str] | None = None
        self.cur: list[str] = []
        self.cur_tag = "p"

    # -- readable blocks -------------------------------------------------
    def flush(self) -> None:
        text = " ".join("".join(self.cur).split())
        if text:
            self.blocks.append((self.cur_tag, text))
        self.cur = []

    def retag(self) -> None:
        self.cur_tag = next((f["tag"] for f in reversed(self.stack)
                             if f["tag"] in EMITTABLE), "p")

    # -- the fix ---------------------------------------------------------
    def close_implied(self, tag: str) -> None:
        while self.stack and self.stack[-1]["tag"] in CLOSED_BY.get(tag, ()):
            self.pop_frame()
            self.implied += 1

    def pop_frame(self) -> dict:
        frame = self.stack.pop()
        text = " ".join("".join(frame["buf"]).split())
        if self.stack:
            self.stack[-1]["buf"].append(text)
        if frame["tag"] in SKIP:
            self.skip -= 1
            if frame["tag"] == "title" and self.capture is not None:
                self.title = " ".join("".join(self.capture).split())
                self.capture = None
            elif frame["tag"] == "script" and self.capture is not None:
                raw = "".join(self.capture)
                self.capture = None
                try:
                    self.jsonld.append(strip_pii(json.loads(raw)))
                except (json.JSONDecodeError, ValueError):
                    self.degraded += 1
        if frame["tag"] == "a" and self.markdown and frame.get("href"):
            self.cur.append(f"]({frame['href']})")
        if frame["tag"] in EMITTABLE:
            self.flush()
        value = frame["item"] if frame["item"] is not None else text
        if frame["prop"]:
            self.attach(frame["prop"],
                        frame["static"] if frame["static"] is not None else value)
        elif frame["item"] is not None and not self.owner():
            self.items.append(frame["item"])
        self.retag()
        return frame

    def owner(self) -> dict | None:
        return next((f for f in reversed(self.stack) if f["item"] is not None), None)

    def attach(self, prop: str, value) -> None:
        owner = self.owner()
        if owner is None:
            return
        item = owner["item"]
        if prop in item:
            if not isinstance(item[prop], list):
                item[prop] = [item[prop]]
            item[prop].append(value)
        else:
            item[prop] = value

    # -- HTMLParser hooks ------------------------------------------------
    def handle_starttag(self, tag, attrs):
        attr = {}
        for key, val in attrs:
            attr.setdefault(key.lower(), val or "")
        self.close_implied(tag)

        if tag == "html" and attr.get("lang"):
            self.lang = attr["lang"][:16]
        if tag == "meta":
            prop = attr.get("property", "")
            if prop.startswith("og:"):
                self.og.setdefault(prop, redact(attr.get("content", "")))
        if tag == "br" and not self.skip:
            self.cur.append(" ")

        prop = attr.get("itemprop", "").strip()
        static = None
        for source in ("content", "href", "src", "datetime"):
            if source in attr:
                static = attr[source]
                break
        if prop and prop.lower() in PII_KEYS:
            prop = ""

        if tag in VOID:
            if prop:
                self.attach(prop, redact(static or ""))
            return

        if tag in EMITTABLE:
            self.flush()
            self.cur_tag = tag
        if tag == "a" and self.markdown and not self.skip:
            href = attr.get("href", "")
            if href and not href.lower().startswith("mailto:"):
                self.cur.append("[")
            else:
                href = ""
        else:
            href = ""

        item = {"@type": attr["itemtype"]} if "itemscope" in attr else None
        if item is not None and not attr.get("itemtype"):
            item = {}
        self.stack.append({"tag": tag, "buf": [], "prop": prop, "static": static
                           if prop and static is not None else None,
                           "item": item, "href": href})
        if tag in SKIP:
            self.skip += 1
            if tag == "title" or (tag == "script" and
                                  "ld+json" in attr.get("type", "")):
                self.capture = []

    def handle_endtag(self, tag):
        if tag in VOID or not any(f["tag"] == tag for f in self.stack):
            return
        while self.stack:
            if self.pop_frame()["tag"] == tag:
                return
            self.implied += 1

    def handle_data(self, data):
        if self.capture is not None:
            self.capture.append(data)
            return
        if self.skip:
            return
        self.cur.append(data)
        if self.stack:
            self.stack[-1]["buf"].append(data)

    def finish(self) -> None:
        """Close the document. Everything still open is an implied end tag."""
        self.close()
        while self.stack:
            self.pop_frame()
            self.implied += 1
        self.flush()


def render(blocks: list[tuple[str, str]], fmt: str) -> str:
    """Readable prose. Markdown keeps heading level, list and quote shape."""
    out: list[str] = []
    for tag, text in blocks:
        if fmt != "markdown":
            out.append(f"- {text}" if tag == "li" else text)
            continue
        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            out.append("#" * int(tag[1]) + f" {text}")
        elif tag == "li":
            out.append(f"- {text}")
        elif tag == "blockquote":
            out.append(f"> {text}")
        elif tag == "pre":
            out.append(f"```\n{text}\n```")
        else:
            out.append(text)
    return redact("\n\n".join(out))


def extract(html: str, fmt: str) -> dict:
    """One page: prose plus its structured layer. Pure, so --self-test is real."""
    doc = Doc(markdown=(fmt == "markdown"))
    doc.feed(html)
    doc.finish()
    text = render(doc.blocks, fmt)
    return {"title": redact(doc.title), "lang": doc.lang, "text": text,
            "words": len(text.split()), "degraded": doc.degraded,
            "implied_closes": doc.implied,
            "structured": {"jsonld": doc.jsonld, "opengraph": doc.og,
                           "microdata": strip_pii(doc.items)}}


def read_ledger(cache: Path) -> list[dict] | str:
    path = cache / "ledger.jsonl"
    if not path.is_file():
        return f"no ledger at {path} — fill the cache with polite-fetch first"
    entries: list[dict] = []
    try:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                entries.append(json.loads(line))
    except (OSError, json.JSONDecodeError) as exc:
        return f"unreadable ledger: {exc}"
    return sorted(entries, key=lambda e: str(e.get("url", "")))


def self_test() -> list[str]:
    """Fixtures only. The first two checks are the reason this tool exists."""
    failures: list[str] = []

    seen: list[str] = []

    class Raw(HTMLParser):
        def handle_endtag(self, tag):
            seen.append(tag)

    raw = Raw()
    raw.feed(MISNESTED)
    raw.close()
    if seen != ["ul"]:
        failures.append(f"the mis-nesting premise changed: HTMLParser fired {seen}")

    doc = Doc()
    doc.feed(MISNESTED)
    doc.finish()
    if doc.stack:
        failures.append(f"depth stack left {len(doc.stack)} frame(s) open")
    if doc.blocks != [("li", "a"), ("li", "b"), ("p", "x"), ("p", "y")]:
        failures.append(f"implied end tags mis-nested: {doc.blocks}")
    if doc.implied != 4:
        failures.append(f"expected 4 implied closes, got {doc.implied}")

    micro = extract(MICRODATA, "text")["structured"]["microdata"]
    if micro != [{"@type": "T", "name": "N", "k": ["a", "b"]}]:
        failures.append(f"microdata scope wrong: {micro}")

    ok = extract(JSONLD_OK, "text")
    if ok["structured"]["jsonld"] != [{"@type": "Person", "name": "A"}]:
        failures.append(f"JSON-LD not stripped of contact fields: "
                        f"{ok['structured']['jsonld']}")
    if ok["degraded"]:
        failures.append("valid JSON-LD was reported degraded")
    if extract(JSONLD_BAD, "text")["degraded"] != 1:
        failures.append("unusable JSON-LD was not counted as degraded")

    if "@" in extract(PROSE, "text")["text"]:
        failures.append("an email survived into the prose")

    if extract("<h2>T</h2><ul><li>a", "markdown")["text"] != "## T\n\n- a":
        failures.append("markdown rendering lost heading or list shape")
    if resolve_charset("text/html; charset=iso-8859-1", b"") != "iso-8859-1":
        failures.append("Content-Type charset ignored")
    if resolve_charset("", b'<meta charset="cp1251">') != "cp1251":
        failures.append("meta charset sniff failed")
    if resolve_charset("text/html; charset=nonsense-9", b"") != "utf-8":
        failures.append("unknown charset did not fall back to UTF-8")
    if decode(b"\xff\xfe", "text/html")[1] is not True:
        failures.append("undecodable bytes were not reported degraded")
    for kind in ("text/html; charset=utf-8", "TEXT/HTML", "", "text/plain"):
        if not is_html(kind):
            failures.append(f"refused to parse {kind!r}")
    for kind in ("application/pdf", "image/png", "application/zip"):
        if is_html(kind):
            failures.append(f"would have parsed {kind!r} as markup")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", help="cache directory written by polite-fetch")
    ap.add_argument("--out", help="destination JSONL, one object per page")
    ap.add_argument("--format", default="text", choices=["text", "markdown"],
                    help="prose shape in the text field")
    ap.add_argument("--structured", action="store_true",
                    help="include the JSON-LD, OpenGraph and microdata block")
    ap.add_argument("--min-text-len", type=int, default=200,
                    help="characters below which a page counts as a finding")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=22 failures={len(failures)}")
        return 1 if failures else 0

    if not args.cache or not args.out:
        print(f"{NAME}: --cache and --out are both required", file=sys.stderr)
        return 2
    cache = Path(args.cache)
    entries = read_ledger(cache)
    if isinstance(entries, str):
        print(f"{NAME}: {entries}", file=sys.stderr)
        return 2

    findings: list[str] = []
    records: list[str] = []
    pages = short = degraded = 0
    truncated = any(e.get("outcome") == "skipped"
                    and "robots" in str(e.get("reason", "")) for e in entries)

    for entry in entries:
        if entry.get("outcome") not in ("fetched", "cached"):
            continue
        pages += 1
        body_path = cache / "bodies" / f"{entry.get('key', '')}.body"
        content_type = str(entry.get("content_type", ""))
        if not is_html(content_type):
            degraded += 1
            findings.append(f"{entry.get('url')}: {content_type or 'unknown type'} "
                            "is not HTML, skipped")
            continue
        try:
            raw = body_path.read_bytes()
        except OSError as exc:
            degraded += 1
            findings.append(f"{entry.get('url')}: body unreadable: {exc}")
            continue
        html, lossy = decode(raw, content_type)
        page = extract(html, args.format)
        if lossy or page["degraded"]:
            degraded += 1
        record = {"url": entry.get("url", ""), "title": page["title"],
                  "lang": page["lang"], "format": args.format,
                  "words": page["words"], "chars": len(page["text"]),
                  "text": page["text"]}
        if args.structured:
            record["structured"] = page["structured"]
        records.append(json.dumps(record, sort_keys=True, ensure_ascii=False))
        if len(page["text"]) < args.min_text_len:
            short += 1
            findings.append(f"{entry.get('url')}: {len(page['text'])} chars of text, "
                            f"under --min-text-len")

    try:
        Path(args.out).write_text("".join(line + "\n" for line in records),
                                  encoding="utf-8")
    except OSError as exc:
        print(f"{NAME}: cannot write --out: {exc}", file=sys.stderr)
        return 2

    for finding in findings:
        print(f"{NAME}: {finding}", file=sys.stderr)
    print(f"{NAME}: pages={pages} extracted={len(records)} short={short} "
          f"degraded={degraded} -> {args.out}")
    if truncated:
        return 3
    if degraded:
        return 4
    return 1 if short else 0


if __name__ == "__main__":
    sys.exit(main())
