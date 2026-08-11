# lexicon/

Query-side language data for `faion search`. Corpus data, not code: the CLI
compiles these files into a sorted table at pack time and does longest-prefix
lookup at query time. Nothing here is ever shown to a user.

**Why it exists.** The corpus is English — 26,114 Cyrillic word tokens across
23,800 files, 5,806 of them the one boilerplate string `Ефективно для`, and zero
of 2,638 methodology first-headings carry Cyrillic. A Ukrainian query therefore
scores zero everywhere and falls through to the floor-fill, which returns the
alphabetical head of the corpus every time — recall ≈ 4.9%, i.e. chance. A
measured ablation on a 60-entry prototype moved UA recall@20 from 2/11 to 11/11.

## Files

| File | What |
|------|------|
| `ua-en.tsv` | 561 rows, `ua_prefix<TAB>en_terms<TAB>src`, byte-sorted, LF, NFC |
| `ua-stopwords.txt` | 121 Ukrainian function words dropped before scoring |
| `meta.json` | tier gate for the directory — **free**, deliberately |

## Format

`ua_prefix` is ONE lowercase Ukrainian token with its inflectional tail removed.
The runtime matches the longest prefix a query token starts with, so `кеш`
covers кеш / кешу / кешем / кешування for free.

`src` is provenance, re-derived from the corpus by the validator rather than
trusted: `taxonomy` (prefix of a Ukrainian trigger word in
`playbooks/taxonomy.xml`), `domains` (terms attested in
`knowledge/domains.xml`), `tags` (terms attested in `meta.json` tags), `title`
(terms attested in slugs, paths and `AGENTS.md` titles), `observed` (terms
attested only in body prose). `observed` is capped at 20% of the file, which is
what keeps the lexicon mined from the corpus rather than free-associated.

## Commands

```bash
python3 scripts/validate-lexicon.py          # shipped files
python3 scripts/validate-lexicon.py <dir>    # a candidate dir
```

## Gotchas

- **No stemmer.** One was measured and gained exactly zero (15/25 → 15/25):
  there is no Ukrainian index text to stem toward, and longest-prefix lookup
  absorbs inflection anyway. Do not add one, and do not pull a Snowball binding.
- **Tier is free and must stay free.** Any paid tier here means a free user
  cannot search in their own language. The rows leak no paid content — they are
  English words, not slugs.
- **No apostrophes in `ua_prefix`.** The Ukrainian apostrophe has three
  encodings in the wild (U+0027 / U+2019 / U+02BC), so a prefix carrying one of
  them silently misses the other two. Truncate before it: `пам`, not `пам'ят`.
- **One token per prefix.** A hyphenated prefix such as `дизайн-систем` can
  never match, because the runtime looks up single tokens.
- Expansion **BOOSTS** candidates and never filters them — the constitution's
  "every failure direction widens the candidate set" rule applies here too.
- A stopword may not start with any lexicon prefix; it would be dropped before
  the prefix could ever fire. The validator rejects that pair.
