#!/usr/bin/env python3
"""hmac-rng-golden.py — golden vectors for HMAC-SHA256 rejection-sampling RNG.

The pattern every deterministic-simulation backend hand-rolls: draw an
unbiased integer in [0, n) from HMAC-SHA256(key, msg || counter), rejecting
words at or above (WORD_SPACE // n) * n instead of folding them, so there is
no modulo bias and every outcome is replayable from stored state.

Four parameters cover the variants observed in the wild:
  --word-bits 64   take the first 8 digest bytes as one big-endian u64,
                   then bump the counter (one word per HMAC block).
  --word-bits 32   scan all eight big-endian u32 words of the digest before
                   bumping the counter.
  --counter-encoding text  message = msg + sep + str(counter)   (sep is --counter-sep)
  --counter-encoding be32  message = msg.encode() + struct.pack(">I", counter)

Modes:
  --emit    compute the vectors for a case list and write a golden JSON file.
  --verify  recompute a golden file from its own declared parameters and
            compare, so a stale or edited file cannot pass as pinned truth.

Input:  see --help
Output: one summary line on stdout; exit 0 ok / 1 mismatch / 2 bad input.
Zero model calls, no third-party imports, fully deterministic.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import hmac
import io
import json
import struct
import sys
import tempfile
from pathlib import Path

NAME = "hmac-rng-golden"
ALGORITHM = "hmac-sha256-rejection"
DIGEST_BYTES = 32


def _block(key: bytes, msg: str, counter: int, encoding: str, sep: str) -> bytes:
    if encoding == "be32":
        payload = msg.encode("utf-8") + struct.pack(">I", counter)
    else:
        payload = (msg + sep + str(counter)).encode("utf-8")
    return hmac.new(key, payload, hashlib.sha256).digest()


def draw(key: bytes, msg: str, n: int, word_bits: int, encoding: str,
         sep: str) -> tuple[int, int]:
    """Return (value, blocks_consumed). Unbiased uniform int in [0, n)."""
    if n < 1:
        raise ValueError("n must be >= 1")
    word_bytes = word_bits // 8
    word_space = 1 << word_bits
    if n > word_space:
        raise ValueError(f"n={n} exceeds the {word_bits}-bit word space")
    limit = (word_space // n) * n
    step = DIGEST_BYTES if word_bits == 64 else word_bytes
    counter = 0
    while True:
        block = _block(key, msg, counter, encoding, sep)
        # word_bits=64 consumes only the first 8 bytes per block (step=32
        # makes the loop body run once); word_bits=32 scans all 8 words.
        for off in range(0, DIGEST_BYTES, step):
            word = int.from_bytes(block[off:off + word_bytes], "big")
            if word < limit:
                return word % n, counter + 1
        counter += 1
        if counter > 10_000:  # unreachable for sane n; guards a bad param set
            raise RuntimeError("rejection loop did not terminate")


def parse_case(spec: str) -> tuple[str, int]:
    """`<n>:<msg>` — n first so a message containing ':' stays intact."""
    head, sep, msg = spec.partition(":")
    if not sep:
        raise ValueError(f"case must be '<n>:<msg>', got {spec!r}")
    try:
        n = int(head)
    except ValueError:
        raise ValueError(f"case n must be an integer, got {head!r}") from None
    return msg, n


def load_key(args) -> bytes:
    if args.key_hex:
        try:
            return bytes.fromhex(args.key_hex)
        except ValueError:
            raise ValueError("--key-hex is not valid hex") from None
    if args.key is not None:
        return args.key.encode("utf-8")
    raise ValueError("one of --key-hex / --key is required")


def cmd_emit(args) -> int:
    try:
        key = load_key(args)
    except ValueError as exc:
        print(f"hmac-rng-golden: {exc}", file=sys.stderr)
        return 2

    specs = list(args.case)
    if args.cases_file:
        p = Path(args.cases_file)
        if not p.is_file():
            print(f"hmac-rng-golden: cases file not found: {p}", file=sys.stderr)
            return 2
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                specs.append(line)
    if not specs:
        print("hmac-rng-golden: no cases (--case / --cases-file)", file=sys.stderr)
        return 2

    cases = []
    try:
        for spec in specs:
            msg, n = parse_case(spec)
            value, blocks = draw(key, msg, n, args.word_bits,
                                 args.counter_encoding, args.counter_sep)
            cases.append({"msg": msg, "n": n, "value": value, "blocks": blocks})
    except (ValueError, RuntimeError) as exc:
        print(f"hmac-rng-golden: {exc}", file=sys.stderr)
        return 2

    doc = {
        "algorithm": ALGORITHM,
        "key_hex": key.hex(),
        "word_bits": args.word_bits,
        "counter_encoding": args.counter_encoding,
        "counter_sep": args.counter_sep,
        "cases": cases,
    }
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if args.out == "-":
        sys.stderr.write(text)
    else:
        Path(args.out).write_text(text, encoding="utf-8")
    print(f"hmac-rng-golden: emit cases={len(cases)} word_bits={args.word_bits} "
          f"encoding={args.counter_encoding} -> {args.out}")
    return 0


def cmd_verify(path_str: str) -> int:
    p = Path(path_str)
    if not p.is_file():
        print(f"hmac-rng-golden: golden file not found: {p}", file=sys.stderr)
        return 2
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        key = bytes.fromhex(doc["key_hex"])
        word_bits = int(doc["word_bits"])
        encoding = doc.get("counter_encoding", "text")
        sep = doc.get("counter_sep", "|")
        cases = doc["cases"]
    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
        print(f"hmac-rng-golden: malformed golden file: {exc}", file=sys.stderr)
        return 2
    if doc.get("algorithm") != ALGORITHM:
        print(f"hmac-rng-golden: unknown algorithm {doc.get('algorithm')!r}",
              file=sys.stderr)
        return 2
    # A `cases` that is not a list of objects is a malformed file, which is
    # exit 2. Without this it reached draw() as a string or an int and died in
    # a TypeError traceback under exit 1 — the code that means "the vectors
    # disagree", so a corrupt golden read as a real drift in the RNG.
    if not isinstance(cases, list) or any(not isinstance(c, dict) for c in cases):
        print("hmac-rng-golden: malformed golden file: 'cases' must be a list "
              "of objects", file=sys.stderr)
        return 2

    mismatch = 0
    for i, c in enumerate(cases):
        try:
            value, _ = draw(key, c["msg"], int(c["n"]), word_bits, encoding, sep)
        except (ValueError, RuntimeError, KeyError, TypeError) as exc:
            print(f"hmac-rng-golden: case {i} unusable: {exc}", file=sys.stderr)
            return 2
        if value != c.get("value"):
            mismatch += 1
            print(f"  case {i} msg={c['msg']!r} n={c['n']}: "
                  f"golden={c.get('value')} recomputed={value}", file=sys.stderr)
    ok = len(cases) - mismatch
    print(f"hmac-rng-golden: verify {p} cases={len(cases)} ok={ok} mismatch={mismatch}")
    return 1 if mismatch else 0


# Known answers, frozen. Each is (word_bits, encoding, sep, msg, n, value,
# blocks) for key 0001020304050607, and each was computed OUTSIDE this file by
# an implementation written from the docstring, then pinned here. They are not
# regenerated by draw(): a golden-vector tool whose test regenerates its own
# goldens proves only that it is self-consistent, which is exactly the failure
# it exists to catch.
KAT_KEY = bytes.fromhex("0001020304050607")
KAT = (
    (64, "text", "|", "seed", 100, 36, 1),
    (64, "be32", "|", "seed", 100, 85, 1),
    (32, "text", "|", "seed", 100, 49, 1),
    (32, "be32", "|", "seed", 100, 66, 1),
    (64, "text", ":", "seed", 100, 8, 1),
    (64, "text", "|", "seed", 1, 0, 1),
)
# Rejection cases. n is one above half the word space, so the acceptance
# window is exactly n and roughly half of all words are out of range. The
# `fold` column is what `word % n` would give without rejection: an
# implementation that folded instead of rejecting would return it, so these
# two vectors are the ones that can tell the difference.
KAT_REJECT = (
    (64, (1 << 63) + 1, "b", 2467050883727023111, 2, 5145611501986162224),
    (32, (1 << 31) + 1, "b", 828977, 1, 1198056037),
)


def _reference(key: bytes, msg: str, n: int, word_bits: int, encoding: str,
               sep: str) -> tuple[int, int]:
    """A second, deliberately naive implementation of the documented scheme,
    used only by --self-test. It shares no code with draw() — the whole point
    of a golden vector is a value two independent implementations agree on."""
    space = 1 << word_bits
    limit = (space // n) * n
    counter = 0
    while counter < 10_000:
        if encoding == "be32":
            payload = msg.encode("utf-8") + struct.pack(">I", counter)
        else:
            payload = (msg + sep + str(counter)).encode("utf-8")
        digest = hmac.new(key, payload, hashlib.sha256).digest()
        if word_bits == 64:
            words = [int.from_bytes(digest[:8], "big")]
        else:
            words = [int.from_bytes(digest[i:i + 4], "big")
                     for i in range(0, DIGEST_BYTES, 4)]
        for word in words:
            if word < limit:
                return word % n, counter + 1
        counter += 1
    raise RuntimeError("reference rejection loop did not terminate")


def run_cli(argv: list[str]) -> int:
    """Call main() with a fixed argv and swallow its output, so --self-test
    proves the exit contract end to end: a tampered golden is exit 1 and a
    malformed one is exit 2, and the difference is what a caller branches on."""
    saved = sys.argv
    sys.argv = [NAME] + argv
    try:
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return main()
    finally:
        sys.argv = saved


def self_test() -> list[str]:
    """Prove the sampler against pinned known answers and prove the CLI's
    verdicts against files written to a temporary directory."""
    failures: list[str] = []

    # 1-6: the four counter/word variants, the separator and the n=1 edge,
    # each against a frozen literal.
    for bits, encoding, sep, msg, n, value, blocks in KAT:
        got = draw(KAT_KEY, msg, n, bits, encoding, sep)
        if got != (value, blocks):
            failures.append(f"KAT word_bits={bits} {encoding} sep={sep!r}: "
                            f"got {got}, want {(value, blocks)}")
        ref = _reference(KAT_KEY, msg, n, bits, encoding, sep)
        if ref != (value, blocks):
            failures.append(f"KAT word_bits={bits} {encoding}: the independent "
                            f"implementation gives {ref}, not {(value, blocks)}")

    # 7-8: rejection sampling actually rejects. Both fixtures have an
    # out-of-range first word, and both differ from what folding would give.
    for bits, n, msg, value, blocks, folded in KAT_REJECT:
        got = draw(KAT_KEY, msg, n, bits, "text", "|")
        if got != (value, blocks):
            failures.append(f"rejection word_bits={bits}: got {got}, "
                            f"want {(value, blocks)}")
        if got[0] == folded % n:
            failures.append(f"rejection word_bits={bits}: returned the folded "
                            "value, so out-of-range words are not rejected")
        first = _block(KAT_KEY, msg, 0, "text", "|")
        head = int.from_bytes(first[:bits // 8], "big")
        if head < (((1 << bits) // n) * n):
            failures.append(f"rejection word_bits={bits}: the fixture's first "
                            "word is in range, so it proves nothing")

    # 9: the same seed reproduces the same sequence, which is the whole
    # promise — a replayed match must land on the same rolls.
    left = [draw(KAT_KEY, f"turn-{i}", 20, 64, "text", "|") for i in range(8)]
    right = [draw(KAT_KEY, f"turn-{i}", 20, 64, "text", "|") for i in range(8)]
    if left != right:
        failures.append("the same seed gave two different sequences")
    if len({v for v, _ in left}) < 2:
        failures.append("the sequence fixture is constant and proves nothing")

    # 10: a different key gives a different sequence.
    other = [draw(b"\xff" * 8, f"turn-{i}", 20, 64, "text", "|") for i in range(8)]
    if other == left:
        failures.append("a different key gave the same sequence")

    # 11: every draw lands inside the requested range.
    if any(not 0 <= draw(KAT_KEY, f"r{i}", 6, 32, "be32", "|")[0] < 6
           for i in range(200)):
        failures.append("a draw landed outside [0, n)")

    # 12: the parameters the caller can get wrong.
    for args, label in (((KAT_KEY, "x", 0, 64, "text", "|"), "n=0"),
                        ((KAT_KEY, "x", (1 << 32) + 1, 32, "text", "|"),
                         "n above the 32-bit word space")):
        try:
            draw(*args)
        except ValueError:
            pass
        else:
            failures.append(f"{label} was accepted")

    # 13: a case spec keeps a ':' inside the message, and a spec without one
    # is refused rather than guessed at.
    if parse_case("5:room:42") != ("room:42", 5):
        failures.append("parse_case lost the colon inside the message")
    for spec in ("nocolon", "x:msg"):
        try:
            parse_case(spec)
        except ValueError:
            continue
        failures.append(f"parse_case accepted {spec!r}")

    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        golden = home / "golden.json"
        emit = ["--emit", "--key-hex", KAT_KEY.hex(), "--case", "100:seed",
                "--case", "6:room-1", "--out", str(golden)]

        # 14: emit then verify is exit 0 both ways, and the file carries the
        # pinned value rather than whatever the run happened to produce.
        if run_cli(emit) != 0:
            failures.append("--emit did not exit 0")
        elif run_cli(["--verify", str(golden)]) != 0:
            failures.append("--verify of a fresh golden did not exit 0")
        doc = json.loads(golden.read_text(encoding="utf-8"))
        if doc["cases"][0]["value"] != 36:
            failures.append(f"emitted value {doc['cases'][0]['value']}, want 36")

        # 15: a tampered value is exit 1 — the drift this tool exists to see.
        doc["cases"][0]["value"] += 1
        tampered = home / "tampered.json"
        tampered.write_text(json.dumps(doc), encoding="utf-8")
        if run_cli(["--verify", str(tampered)]) != 1:
            failures.append("a tampered golden did not exit 1")

        # 16: an edited parameter is drift too. Same vectors, other encoding.
        doc = json.loads(golden.read_text(encoding="utf-8"))
        doc["counter_encoding"] = "be32"
        swapped = home / "swapped.json"
        swapped.write_text(json.dumps(doc), encoding="utf-8")
        if run_cli(["--verify", str(swapped)]) != 1:
            failures.append("a golden with an edited encoding did not exit 1")

        # 17-20: malformed input is exit 2, never exit 1 and never a traceback.
        broken = {
            "cases-not-objects": {"algorithm": ALGORITHM, "key_hex": "00",
                                  "word_bits": 64, "cases": [1, 2]},
            "cases-not-a-list": {"algorithm": ALGORITHM, "key_hex": "00",
                                 "word_bits": 64, "cases": "nope"},
            "wrong-algorithm": {"algorithm": "md5-modulo", "key_hex": "00",
                                "word_bits": 64, "cases": []},
            "unusable-n": {"algorithm": ALGORITHM, "key_hex": "00",
                           "word_bits": 64,
                           "cases": [{"msg": "x", "n": "many", "value": 1}]},
        }
        for label, payload in broken.items():
            path = home / f"{label}.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            code = run_cli(["--verify", str(path)])
            if code != 2:
                failures.append(f"{label} golden: exit {code}, want 2")
        (home / "garbage.json").write_text("{not json", encoding="utf-8")
        for label, argv in (("missing file", ["--verify", str(home / "gone.json")]),
                            ("not JSON", ["--verify", str(home / "garbage.json")]),
                            ("both modes", ["--emit", "--verify", str(golden)]),
                            ("neither mode", ["--key", "k"]),
                            ("no key", ["--emit", "--case", "6:x",
                                        "--out", str(home / "none.json")]),
                            ("no cases", ["--emit", "--key", "k",
                                          "--out", str(home / "none.json")]),
                            ("bad case", ["--emit", "--key", "k", "--case", "six:x",
                                          "--out", str(home / "none.json")])):
            code = run_cli(argv)
            if code != 2:
                failures.append(f"{label}: exit {code}, want 2")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--emit", action="store_true", help="compute and write a golden file")
    ap.add_argument("--verify", metavar="FILE", help="recompute and compare a golden file")
    ap.add_argument("--key-hex", help="HMAC key as hex")
    ap.add_argument("--key", help="HMAC key as a utf-8 string")
    ap.add_argument("--case", action="append", default=[], metavar="N:MSG",
                    help="one case, n first (repeatable)")
    ap.add_argument("--cases-file", help="file of N:MSG lines, # comments allowed")
    ap.add_argument("--word-bits", type=int, choices=(32, 64), default=64)
    ap.add_argument("--counter-encoding", choices=("text", "be32"), default="text")
    ap.add_argument("--counter-sep", default="|",
                    help="separator before the counter in text encoding (default '|')")
    ap.add_argument("--out", default="-", help="golden file path, '-' for stderr")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=20 failures={len(failures)}")
        return 1 if failures else 0

    if args.emit == bool(args.verify):
        print("hmac-rng-golden: pick exactly one of --emit / --verify FILE",
              file=sys.stderr)
        return 2
    return cmd_emit(args) if args.emit else cmd_verify(args.verify)


if __name__ == "__main__":
    sys.exit(main())
