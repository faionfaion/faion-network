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
import hashlib
import hmac
import json
import struct
import sys
from pathlib import Path

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

    mismatch = 0
    for i, c in enumerate(cases):
        try:
            value, _ = draw(key, c["msg"], int(c["n"]), word_bits, encoding, sep)
        except (ValueError, RuntimeError, KeyError) as exc:
            print(f"hmac-rng-golden: case {i} unusable: {exc}", file=sys.stderr)
            return 2
        if value != c.get("value"):
            mismatch += 1
            print(f"  case {i} msg={c['msg']!r} n={c['n']}: "
                  f"golden={c.get('value')} recomputed={value}", file=sys.stderr)
    ok = len(cases) - mismatch
    print(f"hmac-rng-golden: verify {p} cases={len(cases)} ok={ok} mismatch={mismatch}")
    return 1 if mismatch else 0


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
    args = ap.parse_args()

    if args.emit == bool(args.verify):
        print("hmac-rng-golden: pick exactly one of --emit / --verify FILE",
              file=sys.stderr)
        return 2
    return cmd_emit(args) if args.emit else cmd_verify(args.verify)


if __name__ == "__main__":
    sys.exit(main())
