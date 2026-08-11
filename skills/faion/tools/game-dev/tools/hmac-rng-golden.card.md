# hmac-rng-golden

## Purpose
Emit and re-verify golden vectors for an HMAC-SHA256 rejection-sampling RNG, so a deterministic simulation's randomness cannot drift unnoticed.

## Invoke
```
python3 {script} --emit --key {str}|--key-hex {hex} --case {n}:{msg} [--case ...] [--cases-file {path}] [--word-bits 32|64] [--counter-encoding text|be32] [--counter-sep {sep}] --out {golden.json}
python3 {script} --verify {golden.json}
```

## Inputs
- `--emit` / `--verify {file}` — exactly one. Required.
- `--key {str}` or `--key-hex {hex}` — HMAC key. Required for `--emit`.
- `--case {n}:{msg}` — one vector, bound first so a message containing `:` stays intact. Repeatable; required unless `--cases-file`.
- `--cases-file {path}` — file of `{n}:{msg}` lines, `#` comments allowed. Optional.
- `--word-bits 32|64` — `64` takes the first 8 digest bytes then bumps the counter; `32` scans all eight u32 words first. Optional, default `64`.
- `--counter-encoding text|be32` — `text` appends `sep + str(counter)`; `be32` appends `struct.pack(">I", counter)`. Optional, default `text`.
- `--counter-sep {sep}` — separator before the counter in `text` mode. Optional, default `|`.
- `--out {path}` — golden file; `-` writes JSON to stderr. Required for `--emit`.

## Outputs
- Files: `{out}` — `{algorithm, key_hex, word_bits, counter_encoding, counter_sep, cases:[{msg,n,value,blocks}]}`.
- stdout: `hmac-rng-golden: emit cases=N word_bits=B encoding=E -> path` or `hmac-rng-golden: verify path cases=N ok=M mismatch=K`.
- stderr on verify: one line per mismatching case with golden vs recomputed value.
- Exit: `0` emitted / all vectors match · `1` at least one mismatch · `2` bad key, bad case syntax, missing or malformed golden file.

## When NOT to use
- Cryptographic key or nonce generation — this is reproducible game randomness, not a CSPRNG.
- RNGs that are not HMAC-SHA256 rejection sampling, or that fold rejected words instead of discarding them.
- Shuffles and weighted draws — model those as repeated `{n}:{msg}` draws, not one vector.

## Cost
Zero model calls. Milliseconds; one HMAC block per case in the overwhelming majority of draws.
