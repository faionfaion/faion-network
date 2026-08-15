#!/usr/bin/env python3
"""png-diff.py — compare two PNGs on two gates at once and return a verdict.

A visual regression gate has to be arithmetic, not judgement. A model asked
"do these screenshots look the same" answers differently on two runs, and a
single changed-pixel ratio is easy to tune until it says yes to everything.
So this decides on two gates that must both pass:

  * changed-pixel ratio — catches drift spread across the frame;
  * largest 4-connected cluster of changed pixels — catches a button that
    moved 6px, which is a tiny fraction of a 1440x900 frame and therefore
    invisible to any ratio a real page can pass.

A pixel counts as changed when the largest per-channel delta exceeds
--rgb-tolerance. The default 8 absorbs anti-aliasing and JPEG-free
re-rasterisation without absorbing a moved element, whose edge pixels differ
by far more.

PNG is decoded here with zlib and struct: 8-bit truecolour, RGB or RGBA, all
five scanline filters. 16-bit, palette and interlaced files are refused with
exit 2 rather than guessed at — a codec that guesses produces a green gate
over pixels it never read. The mask is re-encoded through the same code, and
--self-test round-trips it.

The images can come from anywhere: a Playwright run, a CI artefact, a
designer's export. This tool never opens a socket and never launches a
browser.

Input:  --a baseline PNG, --b candidate PNG
Output: one verdict line on stdout; optional mask PNG and JSON report.

Exit: 0 within tolerance · 1 a gate was exceeded · 2 the tool could not run
      (unreadable file, dimension mismatch, unsupported PNG form).
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import struct
import sys
import tempfile
import zlib
from pathlib import Path

NAME = "png-diff"
SIGNATURE = b"\x89PNG\r\n\x1a\n"
MASK_CHANGED = (255, 255, 255)
MASK_IGNORED = (64, 64, 64)
MASK_SAME = (0, 0, 0)


def paeth(left: int, up: int, upleft: int) -> int:
    """The PNG predictor. Ties go to left, then up — the order is normative."""
    estimate = left + up - upleft
    da, db, dc = abs(estimate - left), abs(estimate - up), abs(estimate - upleft)
    if da <= db and da <= dc:
        return left
    if db <= dc:
        return up
    return upleft


def unfilter(raw: bytes, width: int, height: int, bpp: int) -> bytearray | str:
    """Undo the per-scanline filters and widen to RGBA, or one error string."""
    stride = width * bpp
    if len(raw) != (stride + 1) * height:
        return "inflated data does not match the header dimensions"
    out = bytearray(width * height * 4)
    prior = bytearray(stride)
    pos = 0
    for y in range(height):
        ftype = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        if ftype == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif ftype == 2:
            line = bytearray((a + b) & 0xFF for a, b in zip(line, prior))
        elif ftype == 3:
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((left + prior[i]) >> 1)) & 0xFF
        elif ftype == 4:
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                upleft = prior[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + paeth(left, prior[i], upleft)) & 0xFF
        elif ftype != 0:
            return f"row {y}: unknown scanline filter {ftype}"
        base = y * width * 4
        if bpp == 4:
            out[base:base + stride] = line
        else:
            for x in range(width):
                src = x * 3
                dst = base + x * 4
                out[dst:dst + 3] = line[src:src + 3]
                out[dst + 3] = 255
        prior = line
    return out


def decode_png(blob: bytes) -> tuple[int, int, bytearray] | str:
    """(width, height, RGBA bytes) or one error string. No third-party codec:
    zlib inflates the IDAT stream and struct reads the chunk headers."""
    if not blob.startswith(SIGNATURE):
        return "not a PNG file (signature mismatch)"
    pos = len(SIGNATURE)
    header = None
    idat: list[bytes] = []
    while pos + 8 <= len(blob):
        (length,) = struct.unpack(">I", blob[pos:pos + 4])
        ctype = blob[pos + 4:pos + 8]
        body = blob[pos + 8:pos + 8 + length]
        if len(body) != length:
            return "truncated chunk"
        pos += 12 + length
        if ctype == b"IHDR":
            if length != 13:
                return "malformed IHDR"
            header = struct.unpack(">IIBBBBB", body)
        elif ctype == b"IDAT":
            idat.append(body)
        elif ctype == b"IEND":
            break
    if header is None:
        return "no IHDR chunk"
    width, height, depth, colour, compression, method, interlace = header
    if depth != 8:
        return f"bit depth {depth} is unsupported; 8-bit only"
    if colour not in (2, 6):
        return (f"colour type {colour} is unsupported; truecolour RGB (2) or "
                "RGBA (6) only")
    if interlace != 0:
        return "interlaced PNG is unsupported"
    if compression != 0 or method != 0:
        return "unsupported compression or filter method"
    if width == 0 or height == 0:
        return "zero-sized image"
    if not idat:
        return "no IDAT chunk"
    try:
        raw = zlib.decompress(b"".join(idat))
    except zlib.error as exc:
        return f"IDAT will not inflate: {exc}"
    pixels = unfilter(raw, width, height, 3 if colour == 2 else 4)
    if isinstance(pixels, str):
        return pixels
    return width, height, pixels


def chunk(ctype: bytes, body: bytes) -> bytes:
    crc = zlib.crc32(ctype + body) & 0xFFFFFFFF
    return struct.pack(">I", len(body)) + ctype + body + struct.pack(">I", crc)


def encode_png(width: int, height: int, data: bytes, bpp: int,
               ftype: int = 0) -> bytes:
    """Encode 8-bit RGB (bpp 3) or RGBA (bpp 4). `ftype` picks one scanline
    filter for every row; the writer only ever uses 0, but --self-test walks
    0-4 so the decoder's filter arms are exercised rather than assumed."""
    stride = width * bpp
    raw = bytearray()
    prior = bytearray(stride)
    for y in range(height):
        line = bytearray(data[y * stride:(y + 1) * stride])
        encoded = bytearray(stride)
        for i in range(stride):
            left = line[i - bpp] if i >= bpp else 0
            upleft = prior[i - bpp] if i >= bpp else 0
            if ftype == 0:
                encoded[i] = line[i]
            elif ftype == 1:
                encoded[i] = (line[i] - left) & 0xFF
            elif ftype == 2:
                encoded[i] = (line[i] - prior[i]) & 0xFF
            elif ftype == 3:
                encoded[i] = (line[i] - ((left + prior[i]) >> 1)) & 0xFF
            else:
                encoded[i] = (line[i] - paeth(left, prior[i], upleft)) & 0xFF
        raw += bytes([ftype]) + encoded
        prior = line
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6 if bpp == 4 else 2,
                       0, 0, 0)
    return (SIGNATURE + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def parse_rect(spec: str) -> tuple[int, int, int, int] | str:
    """`x,y,w,h`, or one error string."""
    parts = spec.split(",")
    if len(parts) != 4:
        return f"--ignore takes x,y,w,h; got {spec!r}"
    values = []
    for part in parts:
        part = part.strip()
        if not part.isdigit():
            return f"--ignore takes non-negative integers; got {spec!r}"
        values.append(int(part))
    if values[2] == 0 or values[3] == 0:
        return f"--ignore rect has zero area: {spec!r}"
    return values[0], values[1], values[2], values[3]


def largest_cluster(mask: bytearray, width: int,
                    height: int) -> tuple[int, tuple[int, int, int, int]]:
    """Area and bounding box of the largest 4-connected run of changed pixels.
    This is the gate a ratio cannot express: a moved element is a small share
    of the frame and a large single blob."""
    best = 0
    box = (0, 0, 0, 0)
    seen = bytearray(len(mask))
    for start in range(len(mask)):
        if not mask[start] or seen[start]:
            continue
        stack = [start]
        seen[start] = 1
        area = 0
        x0 = x1 = start % width
        y0 = y1 = start // width
        while stack:
            index = stack.pop()
            area += 1
            x, y = index % width, index // width
            x0, x1 = min(x0, x), max(x1, x)
            y0, y1 = min(y0, y), max(y1, y)
            if x > 0 and mask[index - 1] and not seen[index - 1]:
                seen[index - 1] = 1
                stack.append(index - 1)
            if x + 1 < width and mask[index + 1] and not seen[index + 1]:
                seen[index + 1] = 1
                stack.append(index + 1)
            if y > 0 and mask[index - width] and not seen[index - width]:
                seen[index - width] = 1
                stack.append(index - width)
            if y + 1 < height and mask[index + width] and not seen[index + width]:
                seen[index + width] = 1
                stack.append(index + width)
        if area > best:
            best = area
            box = (x0, y0, x1 - x0 + 1, y1 - y0 + 1)
    return best, box


def compare(a: tuple[int, int, bytearray], b: tuple[int, int, bytearray],
            tolerance: int, ignores: list[tuple[int, int, int, int]]) -> dict | str:
    """The whole measurement, pure: no I/O, no exits. Returns the counters or
    one error string when the two images are not comparable at all."""
    width, height, apx = a
    bwidth, bheight, bpx = b
    if (width, height) != (bwidth, bheight):
        return (f"dimension mismatch: {width}x{height} against "
                f"{bwidth}x{bheight}")
    total = width * height
    ignored = bytearray(total)
    for x, y, w, h in ignores:
        for row in range(max(0, y), min(height, y + h)):
            lo = max(0, x)
            hi = min(width, x + w)
            if hi > lo:
                base = row * width
                ignored[base + lo:base + hi] = b"\x01" * (hi - lo)
    considered = total - sum(ignored)

    mask = bytearray(total)
    stride = width * 4
    changed = 0
    for y in range(height):
        off = y * stride
        arow = apx[off:off + stride]
        brow = bpx[off:off + stride]
        if arow == brow:
            continue  # the common case, and the reason this is fast enough
        base = y * width
        for x in range(width):
            if ignored[base + x]:
                continue
            i = x * 4
            delta = max(abs(arow[i] - brow[i]), abs(arow[i + 1] - brow[i + 1]),
                        abs(arow[i + 2] - brow[i + 2]),
                        abs(arow[i + 3] - brow[i + 3]))
            if delta > tolerance:
                mask[base + x] = 1
                changed += 1
    cluster, box = largest_cluster(mask, width, height)
    return {
        "width": width, "height": height, "changed": changed,
        "considered": considered, "ignored": total - considered,
        "ratio": (changed / considered) if considered else 0.0,
        "max_cluster": cluster, "cluster_box": list(box), "mask": mask,
    }


def verdict(result: dict, max_ratio: float, max_cluster: int) -> str:
    """Both gates must pass. Either one alone is a gate you can tune past."""
    if result["ratio"] > max_ratio:
        return "fail"
    if result["max_cluster"] > max_cluster:
        return "fail"
    return "pass"


def fmt_ratio(value: float) -> str:
    text = f"{value:.6f}".rstrip("0").rstrip(".")
    return text or "0"


def mask_png(result: dict, ignores: list[tuple[int, int, int, int]]) -> bytes:
    """White where changed, grey where ignored, black elsewhere — so a reader
    can see what the gate excluded, not only what it flagged."""
    width, height = result["width"], result["height"]
    ignored = bytearray(width * height)
    for x, y, w, h in ignores:
        for row in range(max(0, y), min(height, y + h)):
            lo, hi = max(0, x), min(width, x + w)
            if hi > lo:
                base = row * width
                ignored[base + lo:base + hi] = b"\x01" * (hi - lo)
    pixels = bytearray(width * height * 3)
    for index in range(width * height):
        if result["mask"][index]:
            colour = MASK_CHANGED
        elif ignored[index]:
            colour = MASK_IGNORED
        else:
            colour = MASK_SAME
        pixels[index * 3:index * 3 + 3] = bytes(colour)
    return encode_png(width, height, bytes(pixels), 3)


def run_cli(argv: list[str]) -> int:
    """Call main() with a fixed argv and swallow its output. --self-test uses
    this to prove the exit contract end to end: every decode error must reach
    the caller as exit 2, not as a traceback and not as a verdict."""
    saved = sys.argv
    sys.argv = [NAME] + argv
    try:
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return main()
    finally:
        sys.argv = saved


def solid(width: int, height: int, colour: tuple[int, int, int]) -> bytearray:
    return bytearray(bytes(colour) * width * height)


def block(pixels: bytearray, width: int, x: int, y: int, w: int, h: int,
          colour: tuple[int, int, int]) -> None:
    for row in range(y, y + h):
        start = (row * width + x) * 3
        pixels[start:start + w * 3] = bytes(colour) * w


def self_test() -> list[str]:
    """Round-trip the codec and prove both gates. A hand-rolled PNG codec with
    no test is a liability, so every fixture here is encoded, decoded back and
    measured rather than asserted about on paper."""
    failures: list[str] = []

    # 1-5: every scanline filter survives encode -> decode.
    source = solid(9, 7, (10, 20, 30))
    block(source, 9, 2, 1, 4, 3, (200, 100, 50))
    for ftype in range(5):
        decoded = decode_png(encode_png(9, 7, bytes(source), 3, ftype))
        if isinstance(decoded, str):
            failures.append(f"filter {ftype}: {decoded}")
            continue
        expected = bytearray()
        for index in range(9 * 7):
            expected += source[index * 3:index * 3 + 3] + b"\xff"
        if (decoded[0], decoded[1], decoded[2]) != (9, 7, expected):
            failures.append(f"filter {ftype}: round-trip changed the pixels")

    # 6: RGBA round-trips too.
    rgba = bytearray(bytes((1, 2, 3, 4)) * 12)
    decoded = decode_png(encode_png(4, 3, bytes(rgba), 4))
    if isinstance(decoded, str) or decoded[2] != rgba:
        failures.append("RGBA round-trip failed")

    base = solid(200, 200, (255, 255, 255))
    block(base, 200, 20, 20, 21, 21, (0, 0, 0))
    baseline = decode_png(encode_png(200, 200, bytes(base), 3))
    if isinstance(baseline, str):
        return failures + [f"baseline fixture will not decode: {baseline}"]

    # 7: identical images pass.
    same = compare(baseline, baseline, 8, [])
    if isinstance(same, str) or same["changed"] != 0:
        failures.append(f"identical images reported a change: {same}")
    elif verdict(same, 0.001, 400) != "pass":
        failures.append("identical images did not pass")

    # 8-9: an anti-aliasing-scale delta on every pixel passes, and the same
    # delta under a tighter tolerance does not — the knob is real.
    shifted = bytearray(max(0, v - 5) for v in base)
    nudged = decode_png(encode_png(200, 200, bytes(shifted), 3))
    if isinstance(nudged, str):
        return failures + [f"nudged fixture will not decode: {nudged}"]
    aa = compare(baseline, nudged, 8, [])
    if isinstance(aa, str) or aa["changed"] != 0:
        failures.append("a delta of 5 was counted as changed at tolerance 8")
    elif verdict(aa, 0.001, 400) != "pass":
        failures.append("an anti-aliasing-scale delta did not pass")
    tight = compare(baseline, nudged, 4, [])
    if isinstance(tight, str) or tight["changed"] == 0:
        failures.append("a delta of 5 was ignored at tolerance 4")

    # 10-12: a moved block passes the ratio gate and fails the cluster gate.
    # This is the case that justifies the second gate.
    moved = solid(200, 200, (255, 255, 255))
    block(moved, 200, 60, 60, 21, 21, (0, 0, 0))
    candidate = decode_png(encode_png(200, 200, bytes(moved), 3))
    if isinstance(candidate, str):
        return failures + [f"moved-block fixture will not decode: {candidate}"]
    shift = compare(baseline, candidate, 8, [])
    if isinstance(shift, str):
        failures.append(f"moved-block fixture: {shift}")
    else:
        if shift["ratio"] > 0.05:
            failures.append(f"moved block ratio {shift['ratio']} is not under "
                            "the 0.05 gate, so it proves nothing")
        if shift["max_cluster"] <= 400:
            failures.append(f"moved block cluster {shift['max_cluster']} did "
                            "not exceed the 400 gate")
        if verdict(shift, 0.05, 400) != "fail":
            failures.append("a moved block passed both gates")

        # 13: an --ignore rect covering both positions suppresses it.
        masked = compare(baseline, candidate, 8, [(0, 0, 200, 200)])
        if isinstance(masked, str) or masked["changed"] != 0:
            failures.append("an --ignore rect over the whole frame still "
                            "reported changes")

        # 14: the mask re-encodes and decodes back to the same flags.
        painted = decode_png(mask_png(shift, []))
        if isinstance(painted, str):
            failures.append(f"mask will not decode: {painted}")
        else:
            white = sum(1 for i in range(200 * 200)
                        if painted[2][i * 4] == 255 and painted[2][i * 4 + 1] == 255
                        and painted[2][i * 4 + 2] == 255)
            if white != shift["changed"]:
                failures.append(f"mask marks {white} pixels, diff found "
                                f"{shift['changed']}")

    # 15: a dimension mismatch is refused, not resized.
    small = decode_png(encode_png(10, 10, bytes(solid(10, 10, (0, 0, 0))), 3))
    if isinstance(small, str):
        return failures + [f"small fixture will not decode: {small}"]
    if not isinstance(compare(baseline, small, 8, []), str):
        failures.append("a dimension mismatch was not refused")

    # 16-18: the forms this codec will not guess at.
    for depth, colour, interlace, label in ((16, 2, 0, "16-bit"),
                                            (8, 3, 0, "palette"),
                                            (8, 2, 1, "interlaced")):
        ihdr = struct.pack(">IIBBBBB", 4, 4, depth, colour, 0, 0, interlace)
        blob = (SIGNATURE + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", zlib.compress(b"\x00" * 64))
                + chunk(b"IEND", b""))
        if not isinstance(decode_png(blob), str):
            failures.append(f"{label} PNG was accepted")

    # 19-20: a non-PNG and a truncated PNG are refused.
    if not isinstance(decode_png(b"GIF89a"), str):
        failures.append("a non-PNG was accepted")
    whole = encode_png(200, 200, bytes(base), 3)
    if not isinstance(decode_png(whole[:len(whole) // 2]), str):
        failures.append("a truncated PNG was accepted")

    # 21-25: the exit contract, end to end. Every decode error must reach the
    # caller as exit 2 — the union decode_png returns is checked exactly once,
    # in main, and this is what proves it.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "a.png").write_bytes(whole)
        (root / "b.png").write_bytes(encode_png(200, 200, bytes(moved), 3))
        (root / "small.png").write_bytes(
            encode_png(10, 10, bytes(solid(10, 10, (0, 0, 0))), 3))
        (root / "truncated.png").write_bytes(whole[:len(whole) // 2])
        cases = [
            (["--a", f"{root}/a.png", "--b", f"{root}/a.png"], 0, "identical"),
            (["--a", f"{root}/a.png", "--b", f"{root}/b.png",
              "--max-ratio", "0.05"], 1, "moved block over the cluster gate"),
            (["--a", f"{root}/a.png", "--b", f"{root}/truncated.png"], 2,
             "truncated PNG"),
            (["--a", f"{root}/a.png", "--b", f"{root}/small.png"], 2,
             "dimension mismatch"),
            (["--a", f"{root}/a.png", "--b", f"{root}/missing.png"], 2,
             "unreadable file"),
        ]
        for argv, want, label in cases:
            got = run_cli(argv)
            if got != want:
                failures.append(f"{label}: exit {got}, want {want}")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", dest="before", help="baseline PNG")
    ap.add_argument("--b", dest="after", help="candidate PNG")
    ap.add_argument("--mask", help="write a diff mask PNG here")
    ap.add_argument("--report", help="write a JSON report here")
    ap.add_argument("--max-ratio", type=float, default=0.001,
                    help="largest changed-pixel share that still passes")
    ap.add_argument("--max-cluster", type=int, default=400,
                    help="largest 4-connected changed cluster that still passes")
    ap.add_argument("--rgb-tolerance", type=int, default=8,
                    help="per-channel delta below which a pixel is unchanged")
    ap.add_argument("--ignore", action="append", default=[], metavar="X,Y,W,H",
                    help="rectangle excluded from the comparison (repeatable)")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=25 failures={len(failures)}")
        return 1 if failures else 0

    if not args.before or not args.after:
        print(f"{NAME}: --a and --b are both required", file=sys.stderr)
        return 2
    if args.rgb_tolerance < 0 or args.max_cluster < 0 or args.max_ratio < 0:
        print(f"{NAME}: tolerances must be non-negative", file=sys.stderr)
        return 2

    ignores: list[tuple[int, int, int, int]] = []
    for spec in args.ignore:
        rect = parse_rect(spec)
        if isinstance(rect, str):
            print(f"{NAME}: {rect}", file=sys.stderr)
            return 2
        ignores.append(rect)

    images = []
    for label, path in (("--a", args.before), ("--b", args.after)):
        try:
            blob = Path(path).read_bytes()
        except OSError as exc:
            print(f"{NAME}: cannot read {label}: {exc}", file=sys.stderr)
            return 2
        image = decode_png(blob)
        if isinstance(image, str):
            print(f"{NAME}: {label} {path}: {image}", file=sys.stderr)
            return 2
        images.append((image, hashlib.sha256(blob).hexdigest()[:16]))

    result = compare(images[0][0], images[1][0], args.rgb_tolerance, ignores)
    if isinstance(result, str):
        print(f"{NAME}: {result}", file=sys.stderr)
        return 2
    outcome = verdict(result, args.max_ratio, args.max_cluster)

    if args.mask:
        try:
            Path(args.mask).write_bytes(mask_png(result, ignores))
        except OSError as exc:
            print(f"{NAME}: cannot write --mask: {exc}", file=sys.stderr)
            return 2
    if args.report:
        payload = {k: v for k, v in result.items() if k != "mask"}
        payload.update({
            "a": args.before, "b": args.after,
            "a_sha256": images[0][1], "b_sha256": images[1][1],
            "gates": {"max_ratio": args.max_ratio,
                      "max_cluster": args.max_cluster,
                      "rgb_tolerance": args.rgb_tolerance},
            "ignore": [list(r) for r in ignores],
            "verdict": outcome,
        })
        try:
            Path(args.report).write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write --report: {exc}", file=sys.stderr)
            return 2

    if outcome == "fail":
        if result["ratio"] > args.max_ratio:
            print(f"{NAME}: ratio {fmt_ratio(result['ratio'])} exceeds "
                  f"--max-ratio {args.max_ratio}", file=sys.stderr)
        if result["max_cluster"] > args.max_cluster:
            print(f"{NAME}: cluster {result['max_cluster']}px at "
                  f"{result['cluster_box']} exceeds --max-cluster "
                  f"{args.max_cluster}", file=sys.stderr)
    print(f"{NAME}: changed={result['changed']} "
          f"ratio={fmt_ratio(result['ratio'])} "
          f"max_cluster={result['max_cluster']} verdict={outcome}")
    return 1 if outcome == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
