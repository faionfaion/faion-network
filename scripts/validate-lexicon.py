#!/usr/bin/env python3
"""F031 W2: validate the UA->EN query lexicon shipped as corpus data.

Checks `skills/faion/lexicon/ua-en.tsv` and `skills/faion/lexicon/ua-stopwords.txt`:

  1. File hygiene       LF endings, no BOM, NFC, `#` comments only in the
                        leading header block.
  2. Row shape          exactly 3 tab-separated columns.
  3. ua_prefix          one lowercase Ukrainian token, no whitespace, no ASCII;
                        no duplicate prefixes.
  4. Byte order         rows sorted by the UTF-8 bytes of ua_prefix.
  5. Corpus attestation every en term occurs at least once in the corpus.
                        A term that occurs nowhere maps the query at nothing.
  6. Provenance         `src` is re-derived from the corpus, not trusted, and
                        must equal the declared value.
  7. Observed cap       rows whose terms are attested only in body prose are
                        capped at 20% of the file.
  8. Stopwords          sorted, deduplicated, disjoint from the lexicon prefixes.

Usage:
    python3 scripts/validate-lexicon.py            # validate the shipped files
    python3 scripts/validate-lexicon.py <dir>      # validate a candidate dir

Exits 0 when every check passes, 1 on the first failing check's report.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXICON_DIR = ROOT / "skills" / "faion" / "lexicon"
CORPUS = ROOT / "skills" / "faion"
TAXONOMY = CORPUS / "playbooks" / "taxonomy.xml"
DOMAINS = CORPUS / "knowledge" / "domains.xml"

OBSERVED_CAP = 0.20
EN_TOKEN = re.compile(r"^[a-z][a-z0-9+#]*(?:[-.][a-z0-9+#]+)*$")
UA_PREFIX = re.compile(r"^[Ѐ-ӿԀ-ԯ]+$")
WORD = re.compile(r"[a-z][a-z0-9+#]*(?:[-.][a-z0-9+#]+)*")
UA_WORD = re.compile(r"[Ѐ-ӿ]+")
TEXT_SUFFIXES = {".md", ".xml", ".json", ".txt", ".py", ".sh", ".tsv"}

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def read_strict(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(f"{path.name}: starts with a UTF-8 BOM")
    if b"\r" in raw:
        fail(f"{path.name}: contains CR - endings must be LF")
    text = raw.decode("utf-8")
    if unicodedata.normalize("NFC", text) != text:
        fail(f"{path.name}: not NFC-normalised")
    return text


def split_header(path: Path, text: str) -> list[tuple[int, str]]:
    """Return [(lineno, line)] of the data rows; header comments must lead."""
    rows = []
    in_header = True
    for n, line in enumerate(text.split("\n"), start=1):
        if line == "":
            continue
        if line.startswith("#"):
            if not in_header:
                fail(f"{path.name}:{n}: comment outside the leading header block")
            continue
        in_header = False
        rows.append((n, line))
    return rows


def source_sets() -> tuple[set[str], set[str], set[str], set[str]]:
    """Mine the four provenance vocabularies straight from the corpus."""
    taxonomy_ua = set(UA_WORD.findall(TAXONOMY.read_text(encoding="utf-8").lower()))
    domains = set(WORD.findall(DOMAINS.read_text(encoding="utf-8").lower()))
    tags: set[str] = set()
    titles: set[str] = set()
    for meta in CORPUS.rglob("meta.json"):
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for tag in data.get("tags", []) or []:
            tags |= set(WORD.findall(str(tag).lower()))
        titles |= set(WORD.findall(str(data.get("slug") or "").lower()))
    for path in CORPUS.rglob("*"):
        titles |= set(WORD.findall(path.name.lower()))
        titles |= set(WORD.findall(path.parent.name.lower()))
    for agents in CORPUS.rglob("AGENTS.md"):
        try:
            first = agents.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0]
        except OSError:
            continue
        if first.startswith("#"):
            titles |= set(WORD.findall(first.lower()))
    return taxonomy_ua, domains, tags | domains, titles | tags | domains


def unattested_in_corpus(needed: set[str]) -> set[str]:
    """Return the terms that occur nowhere in the corpus. Early-exits."""
    remaining = set(needed)
    for path in CORPUS.rglob("*"):
        if not remaining:
            break
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        remaining -= set(WORD.findall(text))
    return remaining


def classify(ua: str, terms: set[str], taxonomy_ua, domains, tags, titles) -> str:
    if any(w.startswith(ua) for w in taxonomy_ua):
        return "taxonomy"
    if terms <= domains:
        return "domains"
    if terms <= tags:
        return "tags"
    if terms <= titles:
        return "title"
    return "observed"


def validate_lexicon(path: Path) -> None:
    text = read_strict(path)
    rows = split_header(path, text)
    if not rows:
        fail(f"{path.name}: no data rows")
        return

    taxonomy_ua, domains, tags, titles = source_sets()

    parsed = []
    seen: dict[str, int] = {}
    for n, line in rows:
        cols = line.split("\t")
        if len(cols) != 3:
            fail(f"{path.name}:{n}: expected 3 tab-separated columns, got {len(cols)}")
            continue
        ua, en, src = cols
        if ua != ua.strip() or not UA_PREFIX.match(ua) or ua != ua.lower():
            hint = ""
            if any(c in ua for c in "'’ʼ"):
                hint = (" - the Ukrainian apostrophe has three encodings in the wild "
                        "(U+0027/U+2019/U+02BC); truncate the prefix before it instead")
            fail(f"{path.name}:{n}: ua_prefix {ua!r} is not one lowercase "
                 f"Ukrainian token{hint}")
            continue
        if ua in seen:
            fail(f"{path.name}:{n}: duplicate ua_prefix {ua!r} (first seen line {seen[ua]})")
            continue
        seen[ua] = n
        terms = en.split(" ")
        if not terms or en != " ".join(terms) or not en:
            fail(f"{path.name}:{n}: en_terms must be single-space separated")
            continue
        bad = [t for t in terms if not EN_TOKEN.match(t)]
        if bad:
            fail(f"{path.name}:{n}: malformed en term(s) {bad}")
            continue
        parsed.append((n, ua, set(terms), src))

    order = [ua for _, ua, _, _ in parsed]
    if order != sorted(order, key=lambda s: s.encode("utf-8")):
        for a, b in zip(order, order[1:]):
            if a.encode("utf-8") > b.encode("utf-8"):
                fail(f"{path.name}: not byte-sorted - {a!r} precedes {b!r}")
                break

    needed: set[str] = set()
    for _, _, terms, _ in parsed:
        needed |= terms
    missing = unattested_in_corpus(needed)
    if missing:
        for n, ua, terms, _ in parsed:
            hit = sorted(terms & missing)
            if hit:
                fail(f"{path.name}:{n}: {ua!r} maps at term(s) absent from the corpus: {hit}")

    observed = 0
    for n, ua, terms, src in parsed:
        derived = classify(ua, terms, taxonomy_ua, domains, tags, titles)
        if derived != src:
            fail(f"{path.name}:{n}: {ua!r} declares src={src!r}, corpus says {derived!r}")
        if derived == "observed":
            observed += 1
    if parsed:
        share = observed / len(parsed)
        if share > OBSERVED_CAP:
            fail(f"{path.name}: observed rows {observed}/{len(parsed)} = "
                 f"{share:.1%} exceeds the {OBSERVED_CAP:.0%} cap")
        print(f"{path.name}: {len(parsed)} entries, observed {observed} ({share:.1%})")

    return {ua for _, ua, _, _ in parsed}


def validate_stopwords(path: Path, prefixes: set[str]) -> None:
    text = read_strict(path)
    rows = split_header(path, text)
    words = []
    for n, line in rows:
        if line != line.strip() or " " in line or "\t" in line:
            fail(f"{path.name}:{n}: {line!r} is not a bare token")
            continue
        if not UA_PREFIX.match(line) or line != line.lower():
            fail(f"{path.name}:{n}: {line!r} is not one lowercase Ukrainian token")
            continue
        words.append((n, line))
    seen: dict[str, int] = {}
    for n, w in words:
        if w in seen:
            fail(f"{path.name}:{n}: duplicate stopword {w!r} (first seen line {seen[w]})")
        seen[w] = n
    order = [w for _, w in words]
    if order != sorted(order, key=lambda s: s.encode("utf-8")):
        fail(f"{path.name}: not byte-sorted")
    for n, w in words:
        clash = [p for p in prefixes if w.startswith(p)]
        if clash:
            fail(f"{path.name}:{n}: stopword {w!r} would be dropped before "
                 f"lexicon prefix(es) {sorted(clash)} could ever fire")
    print(f"{path.name}: {len(words)} stopwords")


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else LEXICON_DIR
    lex = target / "ua-en.tsv"
    stop = target / "ua-stopwords.txt"
    for p in (lex, stop):
        if not p.exists():
            print(f"FAIL: {p} not found", file=sys.stderr)
            return 1
    prefixes = validate_lexicon(lex) or set()
    validate_stopwords(stop, prefixes)
    if errors:
        print(f"FAIL: {len(errors)} problem(s)", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("OK: lexicon valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
