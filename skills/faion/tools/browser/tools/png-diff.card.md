# png-diff

## Purpose
Compares two PNGs and returns a pass/fail verdict on two gates that must both hold: the
changed-pixel ratio, which catches drift spread across the frame, and the largest 4-connected
cluster of changed pixels, which catches a small structural shift a ratio hides. Use it as the
visual-regression gate in CI or a pre-commit hook — it is pure arithmetic, so it decides the same
way every run, unlike a model asked whether two screenshots look the same. The images may come
from anywhere: a Playwright run, a CI artefact, a designer's export.

## Invoke
```
python3 {script} --a {before.png} --b {after.png} [--mask {diff.png}] [--report {diff.json}] [--max-ratio {0.001}] [--max-cluster {400}] [--rgb-tolerance {8}] [--ignore {x,y,w,h}] [--self-test]
```

## Inputs
- `--a {file}` — baseline PNG, 8-bit RGB or RGBA. Required unless self-testing.
- `--b {file}` — candidate PNG, same dimensions as `--a`. Required unless self-testing.
- `--mask {file}` — write a diff mask PNG: white where changed, grey where ignored, black elsewhere. Optional.
- `--report {file}` — write a JSON report: counters, gates, verdict, and the sha256 prefix of each input. Optional.
- `--max-ratio {float}` — largest changed-pixel share that still passes, measured over the pixels considered. Optional, default `0.001`.
- `--max-cluster {int}` — largest 4-connected changed cluster, in pixels, that still passes. Optional, default `400`.
- `--rgb-tolerance {int}` — a pixel counts as changed when its largest per-channel delta exceeds this; alpha is compared too, opaque for an RGB input. Optional, default `8`, which absorbs anti-aliasing but not a moved element.
- `--ignore {x,y,w,h}` — rectangle excluded from the comparison, for a clock or a carousel. Repeatable, optional.
- `--self-test` — run the built-in fixtures and exit. Optional.

## Outputs
- Files: `{mask}` — the diff mask; `{report}` — the JSON verdict. Neither is written unless asked for.
- stdout: `png-diff: changed=N ratio=0.0004 max_cluster=112 verdict=pass`
- stderr: which gate was exceeded, and the bounding box of the offending cluster.
- Exit: `0` both gates held · `1` a gate was exceeded · `2` the tool could not run — a file it cannot read, dimensions that differ, or a PNG form it will not guess at (16-bit, palette, interlaced, truncated).

## When NOT to use
- Taking the screenshots. It compares bytes it is handed; `playwright-scaffold` writes the harness that produces them deterministically.
- Non-PNG or 16-bit, palette and interlaced PNG input. These exit rather than being converted: a codec that guesses produces a green gate over pixels it never read.
- Judging whether a change is *good*. It measures difference, never intent — an approved redesign fails this gate, and re-seeding the baseline is the correct answer, not a wider tolerance.

## Cost
Zero model calls. Zero network calls. Pure-Python per-byte PNG filtering: a 1440x900 frame is a few seconds per pair, and identical scanlines short-circuit, so an unchanged page is the fast case.
