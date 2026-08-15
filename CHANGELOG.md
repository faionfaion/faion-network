# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- **Tier names are no longer tags.** `pro`, `solo` and `geek` were the #1, #2
  and #4 most frequent tags in the corpus — 568 uses across 564 knowledge
  files — and none of them is a tag. They duplicate the `tier` field, which
  is authoritative, and they duplicate it **inconsistently**: the `pro` tag
  sat on only ~19% of `pro`-tier documents, `solo` on ~22%, `geek` on ~16%,
  and `free` never appeared at all.

  That is not redundancy, it is a facet that lies. Filtering `tag:pro`
  returns a fifth of the pro-tier corpus while reading like a tier filter.
  Four files carried **both** `pro` and `solo` — a document has one tier, so
  those are proof the tags never tracked it.

  Removed under `.aidocs/conventions/meta-json-spec.md` §13.1, which states
  the rule as a prohibition: a tier name is never a tag. Vocabulary 4,411 →
  4,408 distinct, 13,446 → 12,878 uses. The visible effect is that the
  facet's most common values are now topics — `pm`, `marketing`, `infra`,
  `architecture`, `ba`, `rag`, `dev`.

  Mechanically safe, verified rather than assumed: no file's `tags` became
  empty (the schema has no `minItems`, but none was tested), every affected
  file's JSON round-trips byte-identically so the diff carries only the
  removed lines, and neither `tier-manifest.json` nor the L2 `INDEX.xml`
  files carry tags, so no index regeneration was needed.

  **Not touched, deliberately:** the 2,666 tags used exactly once (60% of the
  vocabulary), and the fact that all 455 playbooks carry `tags: []` so a
  playbook facet does not exist at all. Consolidating a controlled vocabulary
  is `feature-071`'s job, and it ships switchable and measured — against a
  measured gain of +5 R@1, it may not ship on by default.

- **Every tool now has a `--self-test`, and backfilling the six that did not
  found two real bugs.** 24 of 24 pass; the count was 18 of 24 before, and
  the six without one were the original three packs — the ones already
  shipping to subscribers, with zero regression tests between them.
  `validate-methodology-scripts.py` treats `--self-test` as a SHOULD and
  never actually checks for it, which is why nothing caught this.

  - **`lever-check.py` announced its own failure and passed anyway.** Two
    ledger rows sharing an id — two research passes concatenated is the
    obvious way in — let one answer cover both. The tool printed
    `levers=2 applied=1 declined=0 unanswered=1 findings=0` and **exited
    0**, because `unanswered` is derived from `len(ledger) - len(answers)`
    while the exit code comes from a separate problem list that stayed
    empty. A quality gate that reports an unanswered lever and returns
    success is worse than no gate. A repeated ledger id is now a finding, so
    the count and the verdict cannot disagree.
  - **`hmac-rng-golden.py` reported a corrupt golden file as RNG drift.** A
    malformed `cases` reached `draw()` as a string or an int, died with a
    `TypeError` traceback, and exited **1** — the code meaning "the vectors
    disagree". A caller branching on the exit code read a hand-edited file
    as genuine non-determinism in its simulation. Now exit 2, the documented
    malformed-input code.

  The `hmac-rng-golden` self-test pins known-answer vectors computed
  **outside** the file and cross-checks them against a second implementation
  written from the docstring — a golden-vector tool whose test regenerates
  its own goldens proves nothing. `django-test-gate` gained two pure
  functions so its verdict logic is testable without spawning a process,
  proven behaviour-identical over 40 stdout×returncode combinations. Every
  new self-test was mutation-tested: unquoting the nginx regex location,
  folding instead of rejecting an out-of-range RNG draw, dropping the
  unsourced-claim gate — each mutation is caught.

- **CR-006 filed: the `sdd/templates` pair, and it is not the duplicate it
  looked like.** Both directories carry `content_id 180a580e913ae900` and
  two of their three content files are byte-identical — but their template
  payloads have nothing in common. `templates` holds the **pre-F-067
  five-file Markdown pattern** across seven subdirectories, i.e. migration
  residue that survived inside a methodology; `templates-planning` holds
  eight real artefacts in the current shape, five of which exist nowhere
  else in the corpus.

  The reference count cuts the other way: `templates` has **62** inbound
  wikilinks, `templates-planning` has **zero**. So the better payload is the
  one nothing points at — though all 62 are a bare `- [[templates]]` bullet
  at the same line of a `## Related` block, which reads as generated
  boilerplate rather than 62 decisions.

  Proposed but not executed: merge the eight artefacts into `templates`,
  drop the legacy subdirectories, retire `templates-planning`. Corpus
  deletion needs the owner's approval and a re-verification pass, per the
  precedent CR-005 set.

- **`scripts/regen-methodology-validators.py` — rebuilds a methodology's
  validator from the JSON Schema in its own output contract.** It landed in
  the wrong commits: the script rode along with the four tool packs and its
  three worked examples with the methodology harvest, because two `git add`
  calls were broader than they should have been. Recording that here rather
  than rewriting history.

  Motivation was a measurement: 966 of 2,578 per-methodology validators
  check only that required keys are present, and 610 of those sit on a
  contract already declaring `enum`, `pattern`, `minItems`, `minLength` and
  bounds the code never enforces. Because validators ship one directory at a
  time via `get-content`, a shared runtime helper is impossible — so the
  constraints are inlined into each generated file.

  **The census inverted the premise.** Over 2,601 slugs: 1,372 would gain
  constraints (1,141 of them a hard declared one), but **761 are refused as
  would-be-weaker and 102 as unprovable** — in roughly 29% of the corpus
  *the code already knows more than the contract*. `infra/terraform-state`
  enforces "rationale must cite an `inputs_used.name`", a cross-field rule
  no JSON Schema expresses. Refusing is the default, and the generator will
  not write a slug whose existing validator rejects the contract's own valid
  example, because then the differential proves nothing.

  A further **318 contracts declare no schema at all**, and 55 spell an enum
  as pipe-separated prose in a `description` while the code enforces it.
  Those are content problems: the right repair is to enrich the contract,
  not the code, and promoting description text to constraints would be
  inventing content. Rollout stays opt-in per slug.

  Worked example, `architecture/trade-off-build-vs-buy`, against the **old
  file's own** deliberately-broken fixture: the old validator caught 2 of
  10 defects, the regenerated one catches 12 — including an ADR id failing
  its pattern, a score above its maximum, a negative cost below its minimum,
  an empty required array, and a version that is not semver.

- **Four more tool packs: `deploy/` (free), `env-topology/` (solo),
  `sdd-sync/` (pro), `hetzner/` (pro).** The tool layer is now **12 packs /
  24 tools**, manifest 3,075 → 3,079, `0` validator findings.

  `hetzner/fw-sync` is the one worth reading. `set_rules` is a destructive
  replace — an empty array wipes every rule — so the tool computes the
  post-apply rule set and **proves** inbound SSH survives from every
  `admin_cidrs` entry plus the caller's own source before it writes;
  failing that proof is a refusal, not a warning. Then it arms a revert and
  requires a *second* invocation to cancel it. No commit, no permanent
  change.

  `sdd-sync` resolved a delivery trap by reading the packer **and** the
  materialiser rather than one of them: `.json` is excluded from the blob
  outright, and while `.xml` is packed, `syncPack` puts only scripts, cards
  and nested helpers on disk. A `profiles/*.xml` would therefore have
  worked in-repo and 404'd on a customer's machine. Vendor profiles are
  embedded in the script with a `--profiles` override instead.

  That correction also overturned a claim this changelog made two entries
  ago: **shared helper modules are not impossible.** The card rule globs
  `scripts/*` non-recursively and the CLI materialises nested
  `scripts/<sub>/*.py` as pack Helpers, so `scripts/lib/` both validates
  and ships. The earlier guidance cost real duplication — the Cloudflare
  pack copied its HTTP helper into three scripts on the strength of it.
  Both `tools/AGENTS.md` and `docs/tool-authoring.md` are corrected.

  Two contract clarifications, both prompted by an author pushing back with
  evidence: a **two-phase apply-then-commit is stronger than `--yes`** and
  satisfies the `mutate` rule in its place, which is why `fw-sync` has no
  `--yes`; and exit `6` means *vendor API error* — a non-2xx, an
  unparseable envelope, a failed async action — while `2` stays for
  genuine unreachability, so a caller can tell "their API is unhappy" from
  "I could not start".

- **Three methodologies harvested from a sibling product, where the
  evidence is measured rather than researched.** `infra/cdn-fronted-static-deploy`,
  `sdlc-ai/risk-scored-fanout-audit`, `dev/build-generator-discipline`.

  The first carries its incident numbers intact — 2026-07-28, 735 bytes
  served against 10,487 at origin, `cf-cache-status: HIT`, `age: 280134`,
  `/sw.js` 7.7 hours stale, 960 `.venv` files shipped by an exclude-list
  rsync — and writes that incident out twice as a *failing artefact*: once
  as the bad example in `02-output-contract.xml`, once as a validator
  fixture. The rule is executable, not narrated. It pairs with the
  `asset-stamp` tool, which implements its first lever; both now link to
  each other.

  Two of the three ship a validator with fixtures (7 and 12); the third
  deliberately declares **no** `<schema>`, because its artefact is a tree of
  files rather than a JSON document, and a mandatory-but-fake validator is
  worse than none.

  One claim from the brief could not be corroborated in the source — that a
  default `urllib` User-Agent draws a 403 from the CDN. It is kept as an
  operational note in its own `<rationale>` rather than stated as a measured
  constant, because everything else in that file is a number that came out
  of a file.

  Not harvested, and why: the source's subject-matter corpus is third-party
  copyrighted certification material and is off-limits in any form,
  including as a test fixture; the audit scripts' risk weights are bound to
  one dataset's field names, so the transferable part is the policy, which
  is now two rules; and a genuinely interesting dependency-surface-freezing
  technique was left out rather than smuggled into a build-discipline file
  where it does not belong.

- **Four new tool packs: `cloudflare/` (solo), `github-ci/` (pro),
  `web-parse/` (solo), `browser/` (free).** Nine tools, all stdlib, all
  carded, all self-tested — 146 self-test checks across the pack, `0`
  validator findings, manifest 3,068 → 3,072.

  The design rule they were built to is **output compression, not API
  access**. A vendor MCP server hands the model raw JSON and the model pays
  for every byte; these make the calls, parse, and print one summary line.
  `zone-audit` fans out over the per-setting endpoints that replaced
  Cloudflare's deprecated batch settings API (EOL 2027-03-31) and returns a
  verdict, not a settings dump.

  Three bugs the authors found by testing rather than by inspection, each
  the kind a card cannot catch:

  - `polite-fetch` asked the **wrong port** for permission.
    `urlsplit().hostname` drops it, so a target on `127.0.0.1:8931` fetched
    robots.txt from port 80, got HTML, parsed zero rules — an accidental
    allow-all — and then fetched a path under an explicit `Disallow`. Keyed
    on `netloc` now, with the port case as a self-test.
  - `polite-fetch`'s `is_html` had `""` in its prefix tuple, and every
    string starts with the empty string, so a PDF was parsed as markup.
  - `png-diff`'s decoder returns a value-or-error union, and three fixtures
    inside `self_test()` fed it straight to `compare()`. A decoder
    regression would have killed **the test that exists to catch it** with a
    traceback instead of printing a failure. The exit contract is now
    exercised end to end through a `run_cli()` helper.

  Four defects in `validate-tools.py` itself, all surfaced by an author
  hitting them honestly:

  - the `credentials.env_var` check ran **per script**, so a pack mixing a
    credentialed tool with a credential-free one failed the innocent
    one. Now per pack.
  - the host allowlist rejected any fixture URL, and the first author to hit
    that wrote `"https://" + "example.com"` to slip past the scan. A rule
    nobody can satisfy honestly teaches obfuscation, so RFC 2606 / 6761
    reserved names are now always permitted and the fixture is written
    plainly.
  - `"*"` in `network.hosts` was decorative — the scan did not treat it as a
    wildcard, so `web-parse`, which by definition contacts hosts it cannot
    know in advance, passed only by accident of using `.invalid` literals.
  - the host regex read the `user` in `user:pw@host` as the hostname.

- **`INDEX.xml` is generated again, and the reason it wasn't was a name
  collision.** `regen-domains-xml.py` skipped any leaf whose path contained
  `templates`, `scripts`, `content` or `__pycache__` — a filter meant for a
  methodology's *structural subdirectories*, matched against the **whole**
  relative path. `skills/faion/knowledge/sdd/templates` is a real
  methodology whose slug is literally `templates`, so the filter swallowed
  it: the generator reported 2,597 methodologies against 2,598 on disk and
  would have dropped a live entry from `sdd/INDEX.xml`. The match now starts
  below `<domain>/<slug>`, because the slug position is a name the author
  chose and only the parts under it are structural.

  This corrects a claim made earlier in this same changelog: the drop was
  **not** a `status` filter. Both `sdd/templates` and `sdd/templates-planning`
  are `status: "draft"` and only one was affected, which is what gave the
  first explanation away.

  With that fixed the generator is a genuine drop-in replacement, verified
  rather than assumed: regenerating the whole corpus removes **zero**
  methodology entries and adds zero, `validate-domains-index.py` and
  `validate-domain-index.py --all` both pass 22/22, and `count=` now matches
  the directory count exactly for every domain — it had drifted (`sdd` said
  101 against 101 on disk only after the fix; the pre-fix generator said
  100). The hand-edit instruction in the root and `scripts/` `AGENTS.md` is
  replaced with the command.

  Left for a content decision, not fixed here: `sdd/templates` and
  `sdd/templates-planning` share the same `content_id` and two of their three
  content files are byte-identical. That is a duplicate pair, and deleting
  corpus content is a change-request with its own evidence, not a side
  effect of a tooling fix.

- **A tool may now hold a third-party credential, and the validator polices
  it.** `tool-pack-meta.schema.json` gains two optional objects: `network`
  (`hosts[]` + `class: read|mutate`) and `credentials` (`env_var`, `vendor`,
  `min_scope`). `card.schema.json` is deliberately untouched — a credential
  is named in `## Inputs` as a plain backticked variable name, which the
  flag scan ignores because it only matches `--` tokens. That avoids
  changing the six pinned card sections and the Go that mirrors them.

  `scripts/validate-tools.py` gains five checks, each proven to fire against
  a negative fixture rather than assumed:

  - importing `urllib`/`http`/`socket`/etc. with no `network` block — a
    credential with nowhere it is forbidden to go;
  - a URL literal naming a host outside `network.hosts`. Subdomains of a
    declared host pass; an undeclared host fails;
  - declaring `credentials` and never reading the named variable;
  - importing `subprocess` in a pack holding a credential — a token in a
    command string is a token in the process table;
  - defining any `--*token*` / `--*secret*` / `--*password*` / `--*api-key*`
    flag. Secrets come from the environment; argv is visible in `ps` and
    lands in shell history and in agent transcripts.

  There is deliberately **no `destroy` class**. `read` issues no non-GET;
  `mutate` is dry-run until `--yes`. An irreversible delete has no way to be
  declared, so it has no way to ship.

  `docs/tool-authoring.md` also now states the design rule these tools exist
  for, which is **output compression, not API access**: an MCP server hands
  the model the vendor's raw JSON and the model pays for every byte, while a
  tool makes the calls and returns only what changes a decision. A network
  tool whose stdout is longer than a screen has failed its purpose however
  correct it is.

- **New tool pack `static-web/` (tier free), first tool `asset-stamp.py`.**
  Harvested from a working generator in a sibling product rather than
  written from research, so the rationale is a measured incident and not a
  hypothesis: on a live Cloudflare-fronted site, hours after a green
  deploy, `GET /assets/js/main.js` returned a **three-day-old 735-byte
  file** with `cf-cache-status: HIT` and `age: 280134`, while the origin
  held the current 10,487-byte file. CI was green throughout, because
  nothing in a normal pipeline looks at what the edge actually serves.

  Assets are served `immutable, max-age=31536000`, so an edge object
  outlives any number of deploys, and purging by API needs credentials a
  build does not have. Page HTML is `cf-cache-status: DYNAMIC` and never
  edge-cached — so the URL the HTML emits is the one lever a build owns.
  Appending the file's own content hash makes a changed asset a URL the
  edge has never seen, while an unchanged asset keeps its URL and stays
  cached: invalidation without giving up caching.

  Only `href="…"` and `src="…"` are rewritten. An asset path inside a
  JavaScript string literal is deliberately left alone — rewriting a value
  the page later compares or keys on turns a cache fix into a data bug.
  A referenced file that does not exist is reported, never silently
  stamped, because that is a link defect a query string would hide.

  Tested end to end, not just self-tested: unstamped page exits 1, stamping
  is idempotent so a second run reports `drifted=0`, changing the asset's
  bytes produces a different hash, and a missing asset surfaces as a
  finding. `--check` is the CI gate form.

  This is also the first pack stamped from `docs/templates/` under
  `docs/tool-authoring.md`, which exercised the checklist end to end:
  validator clean, card 34 of 40 lines, `regen-fragment-index.py --only
  tools` and `regen-tier-manifest.py` (3,067 → 3,068 entries).

- **`deploy-scaffold.py` stopped shipping the maintainer's own server as
  the default target.** `--ssh-addr` defaulted to a real production IP,
  `--ssh-user` to `faion`, `--ssh-host` to `faion-net` and `--ssh-port` to
  a real non-standard port. `game-dev-tools` is tier `solo`, so every
  paying subscriber received that as a runnable default. `--ssh-user` and
  `--ssh-addr` are now **required** — there is no safe default for "which
  machine do I overwrite".

  Two further defects in the same emitted script, both of which made it
  unrunnable or unsafe on any machine but the maintainer's:

  - It called **`fssh`**, a private `~/bin` dispatcher no customer has, for
    both the key-cache step and the whole remote install block. A
    subscriber running the generated `deploy.sh` got `fssh: command not
    found` after the rsync had already overwritten the target. Replaced
    with a plain `ssh` invocation built from the new `--ssh-key` flag,
    overridable by `SSH_KEY` in the environment.
  - The rsync transport passed `StrictHostKeyChecking=no` together with
    `UserKnownHostsFile=/dev/null`, which accepts any host key on every
    run — a shipped man-in-the-middle hole on a channel carrying `sudo
    rsync`. Now `accept-new`, which pins on first contact and fails on a
    change.

  Verified by generating a scaffold and grepping the output: no address,
  no port, no `fssh`, no `StrictHostKeyChecking=no`.

- **Tool authoring is now stamped, not reverse-engineered.** The tool layer
  is about to grow from 3 packs to many, and every new one will be written
  by a subagent that today has to infer the conventions from prose plus a
  read of the existing packs — slow, and it produces drift.

  Added `docs/templates/tool-script.py.template`, `tool-card.md.template`
  and `tool-pack-meta.json.template`. Verified rather than asserted: stamped
  into a scratch pack and run through `validate-tools.py`, they give **0
  findings**, the card lands at **34 lines against the 40-line cap** with
  its guidance comments still in place, and `--self-test` exits 0.

  Added `docs/tool-authoring.md` — a linear 14-step checklist, a
  failure-mode table mapping each mistake to the exact validator message it
  produces, and the `.sh` and network-tool deltas. Added
  `rules/tool-authoring.md` as the trigger stub, mirroring the existing
  `rules/skill-authoring.md` → `docs/skill-authoring.md` pair.

  The templates live in `docs/`, not under `skills/faion/tools/`, because
  `validate-tools.py` iterates every directory beneath `tools/` and would
  fail a template pack, and `regen-fragment-index.py` would index it.

  Three constraints are written down for the first time, all of which will
  bite the packs coming next: the card schema pins **exactly six sections**
  and `faion-cli/internal/tools/card.go` hardcodes the same six headings, so
  a seventh needs a schema and a Go change in lockstep; `meta.json` is
  `additionalProperties:false`, so it cannot carry a `network` or
  `credentials` field yet; and a **shared helper module is impossible**
  because every `.py`/`.sh` in a pack's `scripts/` must have its own card.

- **Corrected three documentation claims that were actively misleading
  authoring agents.** `skills/faion/tools/AGENTS.md` said `vfs-pack` packs
  only `.md` and `.xml`, so `scripts/*.py|sh` "do **not**" ship and F029
  still needed the allowlist widened. F029-T01 landed 2026-08-11:
  `pack.go:631` allowlists `.py`/`.sh` from any `scripts/` path segment,
  2,702 executables already ship, and `faion tools sync` materialises them.
  The stale line was load-bearing — it is the first thing an agent reads
  before designing a tool pack, and it says the pack cannot be delivered.
  Replaced with what the packer actually does, plus the fact that
  `~/.faion/tools/<pack>/` is world-readable and must never hold a
  credential.

  The root `AGENTS.md` claimed all composables are tier `free` since v13.
  Fragments and recipes are; tool packs are not — `game-dev` is `solo` in
  both its `meta.json` and the manifest.

  `scripts/AGENTS.md` listed ten scripts as "superseded, kept for history"
  that no longer exist, and documented eleven live ones nowhere: the three
  index regenerators, `repair-playbook-bridge.py`, `schema_check.py`, the
  fragment/recipe/tool validators, `test-retrieve-2level.py` and
  `update.sh`. It also called `slug-rename-map.json` migrator input when it
  is a runtime dependency, and did not warn that
  `validate-domain-index.py` and `validate-domains-index.py` are two
  different gate validators separated by one letter.

- **Deleted four validators that validate nothing that exists.**
  `validate-methodology-xml.py` targets `methodology.xml` and the corpus
  holds zero of them; `validate-playbook-v2.py` targets `playbook.yaml`,
  likewise zero. Both "pass" by finding no input, which is worse than
  failing. `audit-index-coverage.py` audits the pre-F-067 shape
  (`<tier>/<group>/<skill>/SKILL.md`, `playbook_paths` in the manifest)
  and reports 41 errors and 97 warnings, every one of them phantom.
  `check-review-tools.sh` probes for `codex` and `kiro` CLIs on behalf of
  a review phase no current workflow invokes; it had zero inbound
  references and was not even listed in `scripts/AGENTS.md`.

  None of the four is in `FAST_IDS`, in `f066-validate-all.sh`, or in
  `validator-baseline.txt`, so the pre-commit gate is unchanged.

  One shipped methodology named a deleted instrument:
  `sdlc-ai/verification-rung-placement-rule` used
  `audit-index-coverage.py` as the rung-1 instrument for the
  `tier-gate-coverage` defect, in both its `AGENTS.md` and its
  `rung-placement-record.yaml` template. Repointed to
  `regen-tier-manifest.py --dry-run`, which answers the same question
  ("is any content path ungated, double-gated, or gated to a tier nobody
  owns") against the F-067 source of truth.

- **Deleted six migration one-shots whose migrations are finished.**
  `migrate-f067.py`, `migrate-methodology-to-v2.py`,
  `migrate-playbook-to-v2.py`, `migrate-playbook-yaml-to-xml.py`,
  `apply-domain-merge.py`, `fix-methodology-phase-d.py` — F-059, F-060,
  F-065, F-066 Phase C and F-067 all landed, and nothing outside the
  do-not-run list referenced any of them.

  **`slug-rename-map.json` and `remap-dangling-wikilinks.py` are kept, and
  the do-not-run list was wrong about both.** `scripts/AGENTS.md` filed
  them as migration input; they are live runtime dependencies of
  `repair-playbook-bridge.py`, which binds the JSON path directly and
  `ast.literal_eval`s the `REMAP` dict out of the other. Deleting either
  aborts it on startup. The 234 KB of JSON is not a reason to delete a
  file something reads. Verified after deletion: `--dry-run` still walks
  1,020 chains and 5,493 XML files, and still reports 3 files it would
  change — so that repairer has not converged and is unfinished work, not
  history.

- **Deleted the three index builders that silently emptied the file they
  targeted.** `build-domain-index-v2.py` was documented as broken; the
  audit found `build-methodology-index.py` and `build-methodology-index-c.py`
  share the identical defect and were never written down. All three parse
  YAML frontmatter that F-067 moved into `meta.json`, so all three collect
  zero entries and write `count="0"`.

  `build-methodology-index-c.py` was the worst of the three: writing is its
  default and only behaviour — no `--write`, no `--check`, no `--dry-run`,
  and `--domain` required. `--domain dev` would have replaced the live
  122 KB / 379-entry `dev/INDEX.xml` with 112 bytes, then crashed on an
  unrelated error afterwards. It destroyed first and reported second.
  Nothing referenced any of the three except do-not-run warnings.

  The root `AGENTS.md` gotcha is rewritten accordingly. It now also records
  what the audit turned up about the working generator: `regen-domains-xml.py`
  reads `meta.json` and reproduces the indexes almost exactly (121 insertions
  across 23 files, mostly stale `count=` attributes and summaries that had
  drifted from `meta.json`) — but it filters L2 entries by `status`, so
  `sdd/templates` (`status: "draft"`) drops out of the index while
  `tier-manifest.json` still carries it. Two methodologies are affected. Until
  that is settled it is not a drop-in replacement, and the hand-edit
  instruction stands.

- **The corpus no longer instructs agents to run a validator that cannot
  work.** `sdd-batch-orchestrator` named `validate-methodology-xml.py` as
  its VERIFY step in three content files, while `workflows/AGENTS.md` said
  do not run it — shipped content contradicting itself. That validator
  targets `methodology.xml`, of which the corpus holds **zero** since
  F-067; it reports "no methodology.xml files found" and exits clean, so
  the VERIFY step was passing by finding nothing. Repointed to
  `validate-methodology-v2.py`, the gate `check-validators.sh` actually
  runs.

  `workflows/AGENTS.md` also claimed `validate-workflow-v2.py` "is
  validator 6 of `f066-validate-all.sh`". It is not — validator 6 is
  `validate-methodology-scripts.py`, and workflow-v2 is wired into neither
  runner nor the pre-commit gate. The line now says so, because "a
  validator runs this for you" and "nothing runs this for you" lead to
  different behaviour.

  `docs/methodology-xml-schema.md` gained a SUPERSEDED banner for the same
  reason: it specifies the single-file `methodology.xml` shape F-045
  planned and F-067 abandoned, while `AGENTS.md` still lists it among the
  live corpus specs. An authoring agent reading it builds the wrong thing.

- **Corpus validation no longer needs the corpus to be inside a binary,
  and still never needs a login** (AD-018 step 8).
  `scripts/validate-recipes.py` pinned `FAION_CORPUS_SOURCE=embed` so
  that `faion workflow validate` would resolve `corpus:` fragment
  references without an account — this repo IS the corpus, so making its
  own validation depend on someone's subscription is circular. AD-018
  step 7 deleted the embedded corpus and that escape hatch with it.

  The successor publishes **this working tree**: `vfs-pack --publish`
  over `skills/` into a temp directory, once per run, with
  `FAION_CORPUS_ROOT` pointed at the result. That is strictly better than
  the crutch it replaces. The embed answered out of whatever corpus the
  binary happened to be built from, which could be months old or, on a
  default build, the eight-entry seed tree; the published root is the
  fragments in the checkout being validated, so a fragment edited here is
  validated as edited.

  Resolution order for the corpus, in the same shape the `faion` binary
  already had: `$FAION_CORPUS_ROOT` (a caller who published once for a
  whole CI job) → `$FAION_VFS_PACK` (a prebuilt packer) → `go run` against
  a sibling `../faion-cli` checkout. When none is available the compile
  check is **skipped** with a message naming what to install, exactly as
  it already was for an absent `faion` binary — the corpus is validated
  far more often than the CLI is built — and `--strict` makes the skip
  fatal. The publish is cached for the process and removed at exit: it
  walks ~26k files, and one walk per recipe would turn a full run into
  minutes for no new information.

  Measured: 4/4 recipes pass in 10.9 s, logged out, with the API base
  pointed at a closed port.

- **CR-005 marked executed, with the numbers it actually produced.** Status moves
  `pending-owner-decision` to `executed`; the proposal text is kept verbatim as
  the record of the evidence, behind a banner that says to read it in the past
  tense. The new execution record carries the re-verification result (40 of 40
  survived — every candidate still carried the full generic signature, and every
  named survivor still carried real rules), the measured impact against the
  predicted one, the per-domain `count=` changes, and three places the estimate
  was wrong: the motion references were 4 not 1, the playbook reference was a
  `<gap>` not a `<ref>` (and `<gap>` means *missing*, so it had been wrong all
  along), and the lexicon knock-on nobody predicted. It also records that three
  survivors are themselves partially stamped, which widens the separate
  "20 partially-stamped" cleanup beyond the `dev/` and `frontend/` runs.
  The root `AGENTS.md` corpus counts follow the corpus: 2,638 to 2,598
  methodology dirs, manifest 3,107 to 3,067 entries.

- **Regenerated `skills/tier-manifest.json` after the CR-005 deletion.** 3,107 to
  3,067 entries — `+0 added, -40 removed, ~0 changed`, the whole diff being the
  40 deleted knowledge dirs (knowledge 2,638 to 2,598; playbooks, fragments,
  tools, recipes and lexicon untouched). Version stays 14: the schema did not
  change, only the inventory. `regen-fragment-index.py` reports fragments,
  recipes and tools all up to date — the composable layer shares no path with
  the deleted set, so it is a no-op rather than a skipped step.

- **Deleted the 40 template-stamped methodologies of CR-005.** Each row was
  re-verified before removal: the directory existed, carried the generic
  signature in all five content files plus the stock `## Applies If` lines, and
  — for the 39 with a named survivor — the survivor existed and carried real,
  subject-specific rules. All 40 passed; none was spared. Removed 40 dirs /
  562 files / 1,441,400 bytes. `INDEX.xml` entries were removed by hand (never
  `build-domain-index-v2.py`, which empties the file it targets) and both the
  `count=` attr and the matching `domains.xml` per-domain count re-derived from
  disk: backend 147 to 137, frontend 42 to 21, research 82 to 80, ux 186 to 179.
  One knock-on fix in the lexicon: `frontend/spatial-design-tools` was the only
  place the tag `unity` appeared, so `юніті` no longer qualifies as `src=title`
  and is recorded as `observed`, which is what the corpus now says. Provenance
  is re-derived data, so correcting it is the fix; the validator baseline was
  not widened, and no baseline row referenced a deleted directory.

- **Repointed the references CR-005's deletion would strand.** Ahead of removing
  `ux/motion-and-microinteraction-spec`, its inbound links were moved to the
  surviving sibling `ux/motion-and-micro-interaction-system`: two `[[wikilinks]]`
  (`## Assumes Loaded` row and `## Related` bullet) dropped, since the only
  successor is the referring file itself and a self-link is not a reference; two
  prose routes in `01-core-rules.xml` and `06-decision-tree.xml` that sent the
  caller to the dead slug rewritten to describe the action instead of naming a
  methodology. In the `zero-to-one-product-design-brief-to-dev-handoff-8-weeks`
  playbook the stale `<gap>` — `<gap>` declares a slug the corpus is *missing*,
  and this one existed on disk — became a `<ref>` to the surviving sibling in
  stage 7, whose own task line already reads "spec: states, tokens, motion".
  The four `[[voice-ui-patterns]]` links need no edit: both referring files are
  themselves in the deletion set.

- **Corpus validation no longer requires being logged in.** AD-018 made `cache`
  the CLI's default corpus source, so `validate-recipes.py` — which shells out
  to `faion workflow validate` — began failing all four recipes on
  `auth: not authenticated (jwt)`. Checking this repo offline is the entire
  point of the validator, so it now pins `FAION_CORPUS_SOURCE=embed` for that
  subprocess. Step 7 deletes the embed; the comment there names its successor
  (a `vfs-pack --publish` fixture in a temp root) so nobody "fixes" a future
  failure by logging in.
- **Doc-convention cleanup landed from an abandoned session.** `.claude/` and
  `scripts/lib/` carried repo-style `AGENTS.md`/`CLAUDE.md` pairs the convention
  does not cover — `.claude/` is the installed-skills target, `scripts/lib/` a
  helper module; neither is a directory a reader navigates. Removed, with the
  skill-authoring rule and the adapters envelope brought in line. Also deleted
  `skills/tier-manifest.json.f067-pre-bak`: a 929 KB backup of a generated file,
  and the same path-to-tier sitemap AD-018 spent the day removing from the
  shipped binary. `*.f067-pre-bak` added to `.gitignore`.

- **Doc-convention cleanup landed from an abandoned session.** `.claude/` and
  `scripts/lib/` carried repo-style `AGENTS.md`/`CLAUDE.md` pairs the convention
  does not cover — `.claude/` is the installed-skills target, `scripts/lib/` is
  a helper module, neither is a source directory a reader navigates. Removed,
  with the skill-authoring rule and the adapters envelope brought in line.
  Also deleted `skills/tier-manifest.json.f067-pre-bak`: a 929 KB backup of a
  generated file, and the same path-to-tier sitemap AD-018 spent the day
  removing from the shipped binary. `*.f067-pre-bak` added to `.gitignore`.

- docs: the root `AGENTS.md` said five things that are no longer true, and one that never was. The gotcha "no git hook is installed here" is deleted — the hooks landed, so the entry now says what they gate (title rule, `## [Unreleased]` entry, the 20-80 budget on staged files, 9 whole-corpus validators plus scoped `validate-methodology-v2`) and that the gate is the failure **SET** in `scripts/validator-baseline.txt`, never a count. `f066-validate-all.sh` runs **10** validators, not 7; the tier manifest is **v14**, not v12; the composable layer is **25** fragments over 6 packs (24 before `gate-commit-discipline`). And the layout table pointed playbook leaves at `playbooks/by-goal/<goal>/<slug>/`, which was never a real path: all 492 leaf dirs live at `playbooks/<goal>/<slug>/` and `by-goal/` holds nothing but the L2 `INDEX.xml` files — a reader following the table found no playbook at all. `scripts/AGENTS.md` gains rows for `check-validators.sh`, `install-hooks.sh` and `validator-baseline.txt`, and the same 7 → 10 correction.

- fix: the validator baseline comparison ignores the baseline's own comment header. `--check-all` reported the four `#` lines of `scripts/validator-baseline.txt` as "baseline failures no longer reproduce" — noise, never a false block (a comment can never appear on the current side), but it buried the one line that matters. `compare` now filters comments and blank lines out of both directions.

- docs: `skills/faion/fragments/AGENTS.md` back inside its 20-80 line budget — 100 lines to 79. The sourcing rule and the commit rule were carrying their full rationale and their measurements inline; both move verbatim to [.agents/fragment-shared-blocks.md](.agents/fragment-shared-blocks.md) and leave a four-line summary of what each shared block guarantees and which validator asserts it. Nothing is dropped: the 14-competitors/0-URLs measurement, the four sourcing anchors, the 23-and-9 untracked-deliverables measurement and the `gate/`-not-`research/` placement all survive one link away. It was the only `AGENTS.md` in the repo outside the corpus envelopes breaching the budget, and the new pre-commit hook checks that budget on staged files.

- chore: pre-commit and commit-msg hooks, gated on a failure baseline. The repo rule "every project must have working pre-commit hooks; on failure fix the cause, never `--no-verify`" had nothing behind it here — no hook was installed, and the `## [Unreleased]` rule was enforced by review. `.githooks/` is now tracked and `scripts/install-hooks.sh` points `core.hooksPath` at it; `init.sh`, `scripts/check-validators.sh` and `scripts/f066-validate-all.sh` all call it quietly, so a fresh clone is hooked by whichever is run first. `commit-msg` enforces `type: short description` at 50 characters, no trailing period, no `Co-Authored-By`, no emojis (arrows and dashes are deliberately outside the rejected ranges). `pre-commit` runs three gates: the `## [Unreleased]` entry, checked as a diff of **that section** against the commit's base so editing a released section does not satisfy it; the 20-80 line `AGENTS.md` budget on staged files only, with methodology and playbook envelopes exempt because their shape is the corpus spec and not the docs convention; and the corpus validators. `git commit --amend` is detected from the parent process's arguments, because git exports no flag for it and an amend otherwise diffs against the commit being amended.
  The validator split is the scope decision, and it is one number: `f066-validate-all.sh` takes ~4 minutes, of which ~205 s is validator 3 alone spawning one python per slug across 2,639 slugs. The other nine sweep the whole corpus in ~6 s of CPU between them, so they run in full on every commit while `validate-methodology-v2.py` runs only against the slugs the commit touched; the full sweep is manual (`scripts/check-validators.sh --check-all`). `validate-playbook-v3.py` runs in neither — it fails 455/455 because it demands YAML frontmatter no playbook `AGENTS.md` has ever carried, and a gate that is always red trains people to ignore gates.
  The gate is on the failure **SET**, never on counts: counts wave through a swap, one failure fixed and one introduced. `scripts/check-validators.sh` normalises every validator's `FAIL <path>` lines to `<validator-id>\t<repo-relative-path>` (and contributes an `EXIT:<rc>` row for a validator that fails without printing one, so a silent breakage cannot slip past), and diffs against `scripts/validator-baseline.txt` — 17 known, pre-existing failures: 9 decision-tree, 6 methodology-v2, 2 templates. A line absent from the baseline blocks; a baseline line that no longer reproduces is reported as a fix and never blocks, so repairing content does not also require curating a file to land. Not covered, still manual: nothing checks that a staged `meta.json` was followed by `regen-tier-manifest.py`.

- feat: research-first-build asserts its own deliverables. Ten of the fourteen stages now declare `produces`, so the emitted workflow checks them on disk and in git before marking the stage ok: `research_plan` → `research-plan.md`; the three research stages → their `*-catalog.md` and `*-claims.jsonl`; `evidence` → `evidence-table.md`, `evidence-gaps.md`, `commercial-levers.jsonl`; `concept` → `concept.md`; `lever_gate` → `lever-decisions.md`; `design` → `spec.md`; `plan` → `spec.md` and `plan.md`; all with `committed: true`. `implement` declares `item_commit`, so a dispatched task counts as done only when the commit it claimed resolves, is reachable from HEAD, postdates the baseline the run recorded before stage one, changes at least one path, and is not another item's commit. Why: a 13-stage run dispatched 18 implement executors, **16 of which detected a mis-wired run directory and correctly refused** — "BLOCKED — no code written, no branch, no worktree, no commits" — and the pipeline reported `"implement": {"ok": true, "items": 18}` alongside two clean gates over a game that did not exist. The agents behaved impeccably; only the independent reviewer caught it, and a weaker reviewer would have recorded a clean success with two of eighteen tasks built. The stage now reports landed against dispatched and a shortfall stops the run. Card updated (it also said "thirteen stages" under Cost where the rest of it said fourteen).

- feat: the recipe fixes the catalog filenames. `build-domain-cataloger` took its output filename from the axis it was given — `<axis-slug>-catalog.md`, where the slug was the agent's own contraction of a free-text axis description. A filename the agent chooses is a filename no later stage can assert, so the fragment gains a `slug` slot and writes `<outdir>/<slug>-catalog.md` and `<outdir>/<slug>-claims.jsonl`; `research-first-build` passes `axis-one` and `axis-three` for its two cataloger stages. `research-market-analyst` already wrote fixed names (`market-catalog.md`, `market-claims.jsonl`) and is untouched. The `evidence` stage still globs `*-claims.jsonl` and the concept synthesizer still reads every `*-catalog.md`, so the merge behaviour is unchanged.

- feat: the concept stage writes a concept document. `build-concept-synthesizer` gains an `outdir` slot and writes `<outdir>/concept.md` — the verdict it already returns, rendered as a document the repository keeps: title, core paragraph, the catalog entries it rests on, the scored comparison, the runner-up and why it lost, and a table of every lever id with its disposition, adding nothing not already in the structured output. Its boundary changes from "No file writes" and the `concept` stage's capability from read-only to write. Why: a run shipped **no `docs/concept.md`** — one of four artifacts its own brief made a hard precondition for everything downstream. All three blind judges caught it independently and the pipeline never noticed, because the concept existed only as structured output in the run directory, outside the repo, and vanished with it. The stage's `produces` contract now names the file, so a run that skips it stops there.

- feat: file-writing fragments commit what they write. New shared block `gate/gate-commit-discipline.md`, included by the nine roles whose output contract names a file — `research-desk-brief`, `research-market-analyst`, `research-evidence-table`, `build-domain-cataloger`, `build-solution-designer`, `build-asset-director`, `sdd-planner`, `sdd-task-executor`, `sdd-fix-applier`. It authorises exactly `git add` and `git commit` for exactly the paths the role's own contract names: explicit paths (never `git add -A`, which sweeps in whatever else the run left lying around), a 50-char `type: short description` title, no `--no-verify`, no amend, no push/rebase/reset, and a clean tree for the paths touched. Seven of those roles previously ended their hard boundary with "never run build, deploy, or git write commands" — amended to "never run build or deploy commands", because a role cannot be told both to commit its output and never to run git. Why: two runs of the research-first pipeline ended with **23 untracked deliverables (10 under `docs/`, 6 under `frontend/`) and 9** respectively, and both reported success — `deploy-gh.sh` rsyncs a working tree, so "ready to deploy" was being satisfied by files git had never seen and no clone would ever have. The block lives in `gate/` because it is cross-pack and is a gate on delivery; like `research-source-discipline` it declares no slots and carries no role line, so the role rules do not apply to it. `fragments/INDEX.xml` regenerated (25 fragments).

- feat: a recipe stage declares what it must produce. `docs/schemas/recipe.schema.json` gains an optional `produces` on the stage object — `files` (paths that may embed `{{var:NAME}}` and nothing else), `committed` (those paths must be tracked by git and unmodified), `item_commit` (fan-out only: every dispatched item must leave one sha in `<run>/<stage>/<index>.commit`). `validate-recipes.py` gains `check_stage_produces`, mirroring the compiler's refusals so a recipe is rejected on a machine with no `faion` binary — which is the machine a corpus author is usually on: an empty contract, a repeated path, a `..` segment, a `{{stage:}}`/`{{run:}}`/`{{item:}}` reference in a produced path, `committed` with no files, and `committed` or `item_commit` on a read-only stage. Why the restriction to `{{var:}}`: a path resolved from an earlier stage's *result* is an assertion the run could argue with, and the assertion is the whole point. Purely additive — the four shipped recipes validate unchanged.

- feat: commercial-significance tag on evidence claims (P3.4). `source-table.py` gains two per-claim fields — `commercial` (bool, default `false`) and `lever` (required when `commercial` is true, the ACTION the claim implies in the product's own terms) — a `Commercial lever` column on the table, a `--levers` ledger of the tagged claims with stable ids `C1..Cn`, and two new failure conditions: a commercial claim with no lever, and a commercial claim marked `"load_bearing": false` (a claim that moves what the product earns is load-bearing by definition). A non-bool `commercial` is malformed input, exit 2. The tag is assigned by the **evidence stage**, not the researchers: a lever is a lever because of what the other axes say it costs, and the merged claim set exists only here — plus one stage owns completeness, so an untagged lever has an address. `research-evidence-table` gains the tagging step under a one-way ratchet (it may add a tag a researcher left off, never clear one a researcher set — it already holds the power to demote `load_bearing`, and this stops that power reaching the money tag), emits `commercial-levers.jsonl`, and treats a zero-entry ledger as a finding rather than a clean run. Why: measured across three runs of the research-first pipeline, blind judges scored it 23 and 25 on product/earning potential against 27 for a bare agent with no corpus — the only axis it lost. The mechanism was named independently by two judges: it found the commercially decisive levers, sourced them, and shipped without them, silently. Nothing forced use.
- feat: concept answers every tagged lever (P3.4). `build-concept-synthesizer` gains a `levers` slot and a fifth method step: every id in the commercial-lever ledger gets an entry in the verdict, `applied` with `lands_in` (the mechanism, surface or part of the design that carries it, specific enough that the designer can build it and a reader can check it is there) or `declined` with a reason classified as exactly one of `dark-pattern`, `envelope`, `evidence`, `economics`, `dependency`. **Deferral is a decline** and takes the same classified reason: "out of scope for the first slice" names WHEN, not WHY. There is deliberately no class for "later" — if none of the five applies, the honest answer is that the lever should be applied, which is the exact escape hatch the measured runs used (two of the shipped catalog's ranked revenue entries deferred out of slice 1, no reason recorded). A `dark-pattern` decline is a GOOD decline: one line, passes clean, and the prompt says revenue potential never outranks it and asks for no second reason to bolster it. The schema adds a required `commercial_findings` array whose items require all six fields — an applied lever writes `decline_class: "not-declined"`, a declined one writes `lands_in: "none"` — because optional fields are what models omit. The recipe's `concept` stage is handed the ledger the evidence stage wrote.
- feat: lever-check counts applied vs declined (P3.4). New tool in the free `research/` pack: `lever-check.py` reads the commercial-lever ledger and the concept verdict and writes a decisions report — the counts line, a row per ledger id, then every decline printed in full with its class and its reason. The split is the whole design. **Completeness is arithmetic and fails**: a ledger id with no entry, an entry with no disposition, an applied lever that names nowhere it lands, a decline with no reason or a `decline_class` outside the five (including `not-declined`, which is how a deferral tries to pass), a lever answered twice, or an answer to an id the ledger does not carry — exit 1, each finding on stderr. **Reason quality is a judgement and only reports**: the tool never reads a reason for merit. Blocking on merit is gamed inside one round because the cheapest way through is to reword; reporting alone is ignored because nothing consumes it. So the block sits on the one condition that cannot be argued with — a commercially significant finding the concept never answered at all — and the judgement is printed where the reviewer and the human read it. A `dark-pattern` decline therefore passes exactly like any other: the tool has no opinion on which class is used, only that one is.
- feat: research-first-build gates the lever ledger (P3.4). A fourteenth stage, `lever_gate`, sits between `concept` and `design` — deliberately before the designer, so the spec is derived from a verdict that has already answered every commercially significant finding rather than patched after it. It follows the existing gate pattern exactly: `corpus:gate-runner` as the stage body and again as the gate verifier, `corpus:gate-fixer` as the fixer, `max_rounds: 2`, `subject` = `{{stage:concept.file}}` (a gate's subject must be an EARLIER stage, which is why this is a stage of its own and not a gate block on `concept`), and one validation command — `python3 $(faion tools path lever-check) --ledger {docs_dir}/commercial-levers.jsonl --concept {file} --report {docs_dir}/lever-decisions.md`. The stage body produces the count on the first pass; the gate loop repairs an unanswered lever on the second. Honest note on what "fails" means in this machinery: `writeClaudeGate` breaks on `verdict.clean` and logs "rounds exhausted" otherwise — a gate block never aborts the run. So this fails the STAGE, records the unclean verdict in the run result, and spends a fixer round forcing the missing disposition into the verdict before the design reads it. That is the part that changes behaviour; the reasons themselves are printed, not adjudicated. Verified by compiling the recipe: the emitted artifact carries `lever_gate`, `lever_gate.gate.verifier` and `lever_gate.gate.fixer`, and `{{stage:concept.file}}` resolves to `${RUN}/concept.result.json`.
- docs: CR-005 lists 40 deletion candidates, nothing deleted (P2.2). `.aidocs/improvements/CR-005-generic-methodology-deletion-candidates.md` is evidence for a decision the owner makes; no file it names has been touched. Measured, not estimated: the bulk-generation stamp is detectable by exact signature, and the signatures nest perfectly — **120** methodologies carry a generic `02-output-contract.xml` and `06-decision-tree.xml`, and **100** of those carry it in every file including the routing `AGENTS.md` (same 5 rule ids, same 4 antipattern ids, same 4 step names, same 3 stock `## Applies If` lines). The other 20 are contiguous runs in `dev/` and `frontend/` with real rules under a generic contract, and are not proposed for deletion. Of the 100, **60 were rewritten** under the entries above and **40 are proposed for deletion as redundant** — the subject already exists elsewhere in a copy that has real rules. **35 of the 40 have a same-slug twin in another domain and the twin is the real one**: `backend/api-authentication` is the template, `dev/api-authentication` cites OWASP API Security Top 10 and requires a named revocation path. The reference impact is the decision-relevant part and it is small for a structural reason: wikilinks and `<ref slug=…>` resolve by **slug, not path**, and the manifest carries both twins under the same `slug` and the same `content_id`, so deleting `backend/api-rest-design` while `dev/api-rest-design` survives leaves all 24 inbound `[[api-rest-design]]` links resolving unchanged. Across all 40: 242 inbound wikilinks and 66 slug refs, of which **3 would dangle** — two of them from files that are themselves on the list, leaving **1 wikilink edit and 1 playbook ref edit** for the entire deletion. Impact if accepted: 40 dirs, 562 files, 1.37 MB, 40 manifest entries (3,107 → 3,067), 40 `INDEX.xml` entries to remove by hand, corpus 2,638 → 2,598, and zero unique subjects lost for 35 of the 40. The CR also flags the wider pattern it only partly addresses: **133 slugs exist in more than one domain, covering 270 dirs (10.2% of the corpus)**, and the ~235 duplicated dirs outside this set have not been compared pair-by-pair.

- chore: manifest picks up the 60 rewritten versions (P2.2). `regen-tier-manifest.py` run after the rewrite: **+0 added, -0 removed, ~60 changed**, which is exactly the set whose `meta.json` moved 1.1.0 → 1.2.0 and `last_reviewed` 2026-05-23 → 2026-08-13. Header unchanged at v14 / 3,107 entries — no methodology was added or deleted by this task, and none was retiered. The `~60 changed` figure is the check that the rewrite touched what it claimed to and nothing else.

- fix: decision trees route on the rewritten rules (P2.2). Rewriting `01-core-rules.xml` for 60 methodologies changed every rule id in them, and `06-decision-tree.xml` addresses rules by id through `<conclusion ref=…>`. That silently broke **37 of the 60** against rule B5.5 of `validate-methodology-decision-tree.py` — every leaf `ref=` must name a rule id present in `01-core-rules.xml` — a regression introduced by the rewrite itself and caught only because three of the authoring workers reported it unprompted. Repairing it by remapping ids would have been the wrong fix: the trees were the same generic artefact as the rules, the identical `q-prereqs-ok → q-trigger-fits → q-evidence-available → q-named-owner` ladder appearing verbatim across 120 methodologies and routing on nothing about the subject. All 60 were rewritten instead, to route on signals a practitioner could genuinely be unsure about before running anything: consumer language spread and whether client and server share one build graph (api-contract-pattern-selection); which observability layer is unbuilt and what is wrong with it (api-monitoring); native shell present and the WebKit feature gaps (both PWA files); whether an alert self-resolves inside its window (alert-to-fix-incident-loop); the divergence ratio between top-down and bottom-up estimates (tam-sam-som); whether the claim class is performance or opinion, which exits focus-groups immediately (focus-groups-ux-research); and whether the study is already fielded, which routes diary-study-basics out to diary-study-execution and back. Several trees now encode the sibling boundaries agreed during the rule rewrite — competitor-analysis and competitive-intelligence route to each other on the snapshot-versus-delta question, and design-system-governance routes to breaking-change-deprecation-policy rather than restating its timelines. A structural gotcha worth recording for the next author: the validator's `_depth` counts the `decision-tree` element and each `branch` as well as each `question`, against a hard cap of 5, so only two question levels fit as nesting; coverage has to come from breadth (3-4 parallel root branches) rather than depth. Every leaf now resolves — validator 4 fails on exactly the 9 pre-existing dirs it failed on before, all for `missing content/06-decision-tree.xml`, and the full `f066-validate-all.sh` report is **byte-identical** to the pre-change capture.

- fix: real rule sets for 18 UX methodologies (P2.2). Two established-method clusters and one design-system-operations cluster. The research methods had real published structure to draw on and produced the strongest rules in the whole task: a cognitive walkthrough scores severity by whether a step blocks, never by frequency, because an inspection with no users cannot emit a frequency-weighted severity or a "% of users affected" number at all; diary entries must record event time and entry time separately, because Stone et al. (BMJ 2002) instrumented paper diaries and found ~90% reported compliance against ~11% actual, so backfilled entries are excluded from any temporal pattern; entry triggers must be declared interval-, signal- or event-contingent, since event triggers are blind to non-events and interval entries summarise the day away; focus groups may make no task-performance claim at all — success rate, time and findability route out to usability testing, tree testing or analytics, because a group measures socially-acceptable opinion; and tree testing reports success and directness separately, because high success with low directness is label ambiguity and reads as a pass if the two are merged. On the design-system side: a colour change that crosses a WCAG 1.4.3/1.4.11 threshold is a MAJOR, not a PATCH tweak; a changelog rollback plan is a version pin, because npm publish immutability means reverting the PR is not a consumer-side rollback; governance references the deprecation policy by URL and version and is forbidden from inlining its timelines, which is the rule that keeps the two from collapsing into each other; and `prefers-reduced-motion` must **replace** rather than shorten a transform — a compressed slide raises angular velocity and is a stronger vestibular stimulus, not a weaker one — paired with a rule to keep completion events firing (0.01ms, never `animation: none`, or `transitionend` handlers strand modals). `ux/audience-segmentation` was written as the definitive version of a subject whose `research/` twin is on the deletion list, and requires a segment to be an executable query over real record-store fields with a ≤5% unassignable residue: a partition you cannot assign a live user to is a persona, not a segment. `mobile-ux-basics` records the target-size floor per platform rather than picking one number, because WCAG 2.2 SC 2.5.8 AA (24x24 CSS px), SC 2.5.5 AAA (44x44), Apple HIG (44x44 pt) and Material (48x48 dp) genuinely differ and the strictest applicable one wins. `meta.json` 1.1.0 → 1.2.0, `last_reviewed` → 2026-08-13; decision trees rewritten.

- fix: real rule sets for 18 research methodologies (P2.2). The largest generic cluster and the one most at risk of being rewritten into a second layer of mush, because six of the eighteen are near-neighbours by name. They were written by three workers each told to report `CANNOT-SALVAGE: <slug> — duplicate of <other>` rather than produce two similar rule sets; none fired, and each pair came back with an explicit boundary instead. `competitive-intelligence-market-research` owns period-over-period deltas (`cycle` + before/after + `observed_at`), `competitor-analysis-market-research` owns the point-in-time matrix and positioning map, and each one's skip rule now routes to the other by name — no baseline yet means run competitor-analysis first; a change-over-time question means run competitive-intelligence. `market-analysis` (static structural read: boundary test, MECE demand-side segments, regulatory instrument vs application date), `trend-analysis-market-research` (falsifiability core: rate of change, per-trend `valid_until`, a disconfirming signal named at authoring time and not rewritable at review) and `product-development-trends-market-research` (practitioner metrics with denominators, cumulative counters banned because stars and all-time downloads are monotonic and structurally cannot emit a decline signal) came back with zero rule-id overlap. The rules that carry real content: TAM/SAM/SOM computed both top-down and bottom-up with the divergence ratio recorded, a gap over 2x blocking sign-off until the differing term is named; triangulation requires methods that are actually independent, so one recruited panel surveyed and interviewed is **one** method and three dashboards over one events table is **one** method; churn compounded not multiplied, since 5%/month is ~46% annual rather than 60% and the linear shortcut misstates the LTV that the whole ranking gate divides by; channel payback in months gates the score rather than raw CAC, because a cheap low-margin channel past 12 months is cash-negative inside runway; collection stops at the login wall, sourced to Van Buren (2021) and hiQ v. LinkedIn, because the defensible line is the authentication gate and not the word "scraping"; and all four JTBD forces must be quoted rather than inferred, since an unsurfaced anxiety recorded as zero turns an interview gap into a finding. `meta.json` 1.1.0 → 1.2.0, `last_reviewed` → 2026-08-13; decision trees rewritten.

- fix: real rule sets for 10 dev methodologies (P2.2). The AI-assisted-development and on-call cluster: `ai-over-reliance-self-audit`, `ai-pairing-decision-tree`, `ai-prompt-as-commit-artifact`, `ai-prompt-patterns-test-ideation`, `alert-to-fix-incident-loop`, `hidden-tech-debt-trace`, `hot-path-baseline-template`, `library-evaluation-rubric`, `ls-gumroad-pricing-flip`, `migration-impact-mapping`. Seven rules each, all replacing the generic template. The ones that carry a number or a mechanism a practitioner would otherwise have to look up: a prompt trailer block must be the commit message's **final** paragraph, because git's trailer parser only scans the last paragraph and one stray trailing line makes `%(trailers:key=…)` return empty — so the audit reports zero AI commits and looks clean; page on symptom or burn rate with the multiwindow multi-burn-rate thresholds (14.4x/1h and 6x/6h page, 1x/3d tickets) and never on a cause metric; the perceived-versus-measured speedup rule cites METR 2025, where developers forecast ~24% faster, believed ~20% faster afterwards, and measured **19% slower** — self-report diverges in sign, which is the whole reason the audit needs a timed assistant-off baseline; supervision budget must cover the expected diff, because defect discovery falls off above roughly 200-400 LOC per sitting, so a large agent diff is nominally reviewed and empirically unread; performance baselines must guard coordinated omission (a closed-loop generator stops sending during a stall and records one slow sample instead of thousands — k6 `constant-arrival-rate`, `wrk2 -R` or Gatling); bundle deltas must be measured on a real import, since tree-shaking needs an ESM entry plus `"sideEffects": false` and a CJS-only package links whole however narrowly you import it; a bare `Mock()` answers to any attribute or signature, so a renamed production method keeps passing `assert_called_once_with` against a phantom; and a migration must declare its point of no return, because rollback expires silently at the contract phase or the first destructive backfill. `dev/ls-gumroad-pricing-flip` was explicitly flagged as a likely delete and was judged salvageable on vendor-specific evidence: editing a variant price on LemonSqueezy or Gumroad applies to new checkouts only, existing subscriptions bill on at their creation price unless migrated, so the default outcome of a price rise is a flat MRR curve the operator misreads as failed elasticity. `meta.json` 1.1.0 → 1.2.0, `last_reviewed` → 2026-08-13; decision trees rewritten.

- fix: real rule sets for 7 backend and comms methodologies (P2.2). Same defect as the frontend batch — `backend/api-contract-pattern-selection`, `api-monitoring`, `nodejs-service-layer-architecture`, `nodejs-service-layer-implementation` and `comms/freelancer-inbound-reply-template`, `freelancer-scope-change-script-library`, `freelancer-weekly-report-template` carried the topic-free 5-rule template. Replaced with 7 rules each about the subject. The backend four now pin things that are checkable in a repo: a tRPC verdict is valid only when client and server share one TypeScript build **and** deploy together, because the contract is an inferred `AppRouter` type and an independently released client gets zero compile-time signal for a renamed field; a Prometheus `route` label must be the path template, not the raw path, or cardinality grows with traffic instead of with API surface; the service layer owns the transaction boundary, since repository-owned implicit transactions partially commit and external calls inside one trip Prisma's 5s interactive timeout; and an Express error handler must declare four parameters, because Express selects error middleware by function arity and a three-argument handler is silently never invoked. The comms three were the batch where the escape hatch was most likely to fire and did not: a first-touch reply must not carry a number before scope is known (every later discovery then reads as a price increase against the anchor), a scope-change option set must include a swap that holds the date (the MESO pattern makes fixed capacity visible without the freelancer having to refuse), and client-owned work belongs in the report's `asks` section rather than `next` (listed as freelancer work it ages invisibly and the slip is attributed to the freelancer). `06-decision-tree.xml` rewritten in all 7 — see the decision-tree entry below for why. `meta.json` 1.1.0 → 1.2.0, `last_reviewed` → 2026-08-13.

- fix: real rationales for 15 BA rule sets (P2.2). Every `<rationale>` in these 15 `content/01-core-rules.xml` files was a string substitution — the body was literally the `source` attribute followed by `— applies to <Methodology Title>.`, so `ba/discovery-to-delivery-handover-protocol` justified all 8 of its rules with 8 restatements of their own source names. The statements were never the problem: they carry real thresholds (nine named handover artefacts, a 90-minute synchronous walkthrough, a 30-day hot-line, client-stakeholder introduction within 5 business days), which is why this is a repair and not a rewrite. **120 rationale bodies** replaced with mechanism explanations across `definition-of-ready-checklist`, `demo-recap-email-template`, `discovery-to-delivery-handover-protocol`, `ecommerce-checkout-ba-pack`, `facilitation-anti-patterns`, `freelance-proposal-template`, `glossary-management-as-code`, `hipaa-baa-vendor-checklist`, `inbound-intake-qualification`, `interview-recording-redaction-pipeline`, `kpi-drift-alarm-template`, `live-ticket-drafting-shared-screen-pattern`, `nda-msa-obligation-extractor`, `process-mining-tool-shortlist` and `requirement-quality-scorecard`. The change is surgical and machine-checked: `git diff -U0` reports **0 changed `<statement>` lines** across all 15 files, and the `source=` attribute sets diff identical old-vs-new — only rationale bodies and the one `<text version=>` line per file moved. Accuracy was bounded deliberately on the two regulated subjects. `hipaa-baa-vendor-checklist` now states what HIPAA actually does and does not require: audit rights are **not** required (the mechanism given is instead the covered entity's duty to act on a known pattern of material breach, which is unmeetable without a discovery mechanism), encryption is **addressable** rather than required (the lever is the "unsecured PHI" trigger for breach notification), 60 days is the vendor's regulatory ceiling with the 72-hour narrowing described as contractual, and subcontractor-list disclosure is attributed to the GDPR processor regime rather than to HIPAA. `interview-recording-redaction-pipeline` asserts no statutory deadline number at all — the internal-inside-external relationship is stated qualitatively, which holds regardless of regime. No percentages, study results or CFR citations were invented anywhere. `meta.json` untouched; the rule ids did not move, so all 15 decision trees still resolve. Validators 3 and 4 pass 15/15. One pre-existing defect left in place for a separate pass, since fixing it would have modified a statement: `process-mining-tool-shortlist` rule `weighted-criteria` lists `conformance check` twice.

- fix: real rule sets for 7 frontend methodologies (P2.2). `frontend/pwa-core`, `pwa-advanced`, `shadcn-ui`, `tailwind-patterns`, `ui-lib-basics`, `ui-lib-patterns` and `w3c-design-tokens-standard-ui-design` shipped a `content/01-core-rules.xml` carrying the same five topic-free rules as 99 other methodologies — `anchor-evidence-required`, `owner-and-last-touched`, `template-version-pinned`, `human-checkpoint-before-binding-action`, `skip-when-prerequisites-missing` — with the methodology name interpolated into the summary and nowhere else. Each is replaced by 7 rules about the actual subject, every rationale naming a mechanism rather than asserting importance: Service Worker scope tied to the script's path and the `controllerchange` update prompt (auto-`skipWaiting` under a loaded page serves `ChunkLoadError` from precached chunks the new build deleted); VAPID key stability under RFC 8292 and subscription pruning on 410 Gone under RFC 8030 (retried dead endpoints keep the reported delivery rate plausible while real reach collapses); Radix primitive version pinning, because the accessible keyboard semantics live in the dependency and an unpinned bump changes them with zero diff in the repo; `twMerge` resolving conflicts against its own static class-group map rather than `tailwind.config`, so custom scales need `extendTailwindMerge`; rest-props and ref forwarding, where a prop allowlist silently drops `type="submit"` and the button renders correctly but stops submitting; `inert` plus scrollbar-gutter compensation for modal backgrounds, since an overlay is paint only; and DTCG draft pinning, because `$value` for color and dimension moved from string to object between drafts and both parse as valid JSON, so the failure lands deep in the platform build. `pwa-core`'s pre-existing `content/01-rules.xml` and `02-patterns.xml` held genuine domain material and were harvested rather than replaced — both files are untouched and now referenced from `see-also`. `meta.json` `version` 1.1.0 → 1.2.0 and `last_reviewed` 2026-05-23 → 2026-08-13 on all 7. Validator 3 passes 7/7.

- fix: the playbook→methodology bridge resolves again (P2.6). `repair-playbook-bridge.py` applied over **205 files** — 112 leaf `AGENTS.md` and 93 `content/01-playbook.xml`. Markdown path references go from **0 of 1,375 resolving to 1,362 of 1,362**: 356 remapped through `slug-rename-map.json`, 1,001 by unique slug, 2 by a domain segment of the old path, 3 through the ratified rename table, **13 dropped**. XML slug references go from 5,470 of 5,634 to **5,492 of 5,492**: 22 remapped (`technical-debt` → `technical-debt-management` ×9, `cohort-basics` → `cohort-implementation` ×8, `trunk-based-development` → `trunk-based-dev-principles` ×4, `deploy-blue-green-canary` → `release-strategy-canary-blue-green-feature-flag` ×1), **142 dropped** across 97 distinct slugs. Both carriers are now at **100%**, every destination checked on disk before it was written, and a rerun is a byte-identical no-op. The `(tier: …)` annotation on each `**Backed by methodology**` bullet is re-read from the target's `meta.json` rather than carried over from the old path's tier segment, so the tier stated beside a reference is the tier the manifest will enforce on it. What was dropped, and why: role and container names that were never methodologies and have no successor (`market-researcher` 13, `software-developer`, `researcher`, `claude-code`, `automation-tooling`, `sdd`, `business-analyst`); slugs for methodologies that were planned and never written, which is the bulk of the XML residue and the same content gap the leaves already record under `## Known gaps` (`user-interviews-methods` 6, `behavioral-evals-adversarial` 5, `requirements-management` 5, `llm-as-judge-harness` 4, 90 more at 1-3 each); and one ambiguity kept ambiguous — `solo/dev/software-developer/technical-debt` (7 references) has two equally plausible successors, `product/technical-debt-management` and `pm/technical-debt-management`, and nothing in the old path chooses between them, so it drops. Note the asymmetry that made that call: the same slug **remaps** in the XML carrier, because a bare `slug=` reference is domain-free and a duplicated slug is not ambiguous for it, while a path reference must name one domain and would be asserting a destination the evidence does not support. 45 `<methodologies>` elements are left empty by the drops, joining the 97 empty ones already in the tree. All 453 playbook XML files still parse.

- feat: `scripts/repair-playbook-bridge.py` — the decision table for the stale methodology references in playbook leaves, applied by script rather than by hand (P2.6). Measured over the 456 leaf envelopes and their 453 `content/01-playbook.xml`: **1,375 path references** across the two Markdown carriers (`**Methodologies in chain:**` and `**Backed by methodology**`, in 112 leaves) and **5,634 bare-slug `<ref slug=…>`** in the XML. The two carriers are **not** the same defect, which is why the script decides them separately. A Markdown reference names a *path* — `solo/dev/software-architect/architecture-decision-records` — and F-067 moved every methodology to `<domain>/<slug>`, so **1,375 of 1,375 resolve to nothing**; an XML reference names a *bare slug*, which is path-independent and survived the move intact, so 5,470 of 5,634 already resolve and the residue is slugs with no methodology anywhere rather than layout drift. Same two actions as `remap-dangling-wikilinks.py` — remap when a successor exists and is verified on disk, drop when none exists or more than one target is plausible, never invent — with four ordered sources of evidence. **A**, `slug-rename-map.json`, the F-067 migration's own per-path decision table: authoritative, and the only source that can split a slug living in two domains, because it alone knows which old path became which new one (`dev/software-architect/architecture-decision-records` → `architecture/…` while `sdd/sdd/architecture-decision-records` → `sdd/…`, 21 references that a basename rule would have had to drop). **B**, the slug is unique in the corpus. **C**, the slug is duplicated but a segment of the old path is a current domain that holds it. **D**, the ratified rename table inside `remap-dangling-wikilinks.py`, re-checked through B and C so a ratified rename onto a duplicated slug still has to disambiguate. Dropping removes the whole bullet; a `**Backed by methodology**` heading left with nothing under it goes too, with the blank line above it, while an emptied `**Methodologies in chain:**` block gets the placeholder 34 leaves already carry. An emptied `<methodologies>` element is left in place: 97 stages already ship one, so an empty element is the shape in use and removing it would be a schema change rather than a fix. `--dry-run` prints the class histogram, `--report` adds the per-target drop table.

- fix: the 11 playbook goal indexes point at playbooks that exist (P2.3). Regenerated by `regen-playbook-index.py`: **455 of 455 `path=` attributes were wrong** and are now right, every one resolving to a directory whose name is the entry's own slug. The old values named the retired `skills/faion/playbooks/<tier>/<group>/<slug>` layout — `by-goal/operate-ritual/INDEX.xml` sent a router to `playbooks/solo/solo-ops-finance/affiliate-referral-check-and-payout` when the playbook has been at `playbooks/operate-ritual/affiliate-referral-check-and-payout` since F-067 — so **every** L2 lookup in the layer resolved to nothing while all 11 counts matched the tree exactly and hid it. This is now urgent rather than cosmetic: P0.3 landed CLI-side and `taxonomy.xml` plus these 11 files entered the candidate manifest (3,192 → 3,204 candidates), so they are a live retrieval surface an agent is handed, not dormant files. One slug drift fixed with them — `discover-validate` listed `solo-idea-to-validated-mvp` for a directory named `idea-to-validated-mvp` — and 114 summaries reflowed off the leaf `meta.json` at a 200-character word-boundary clip. Counts unchanged at 25 / 33 / 77 / 154 / 32 / 15 / 23 / 33 / 39 / 12 / 12. **`audit-comply` stays in the taxonomy**: the audit that opened this task reported it as a category with zero leaves and a decision-tree step to nowhere, but it has **12** on disk (`soc2-gdpr-audit-prep`, `fintech-hipaa-compliance-audit-prep`, five accessibility-audit playbooks and five more) and its 12 index entries all resolve — the audit's own per-goal figures sum to 443, not 455, which is exactly those 12. Nothing to remove, and step 11 of the decision tree stands.

- feat: `scripts/regen-playbook-index.py` — the generator for the playbook layer's 11 L2 goal indexes (P2.3). Knowledge routes `domains.xml` → `<domain>/INDEX.xml` and the composable layer got `regen-fragment-index.py`; playbooks had no generator at all, which is why `by-goal/<goal>/INDEX.xml` could carry **455 entries whose `path=` named a directory that does not exist** while every count matched reality — a hand-kept list drifts destination-first, since only the count is ever spot-checked. Every entry is derived from the leaf's own `meta.json` (slug, tier, complexity, summary) plus where the leaf actually sits on disk, and the goal set plus each index's `<description>` come from `taxonomy.xml`, so L1 and L2 cannot disagree about which categories exist. Two aborts rather than a half-correct index: a taxonomy category with no leaves under it, and a directory under `playbooks/` holding leaves with no category above it — the second is what a repeat of the deleted tier subtree would look like, and it now fails the run instead of sitting there unroutable. Modelled on `regen-fragment-index.py` and `regen-tier-manifest.py`, which read `meta.json` — deliberately **not** on `scripts/build-domain-index-v2.py`, which reads YAML frontmatter no envelope carries and empties the `INDEX.xml` it targets. Summaries are clipped to 200 characters on a word boundary, because an L2 index is read whole before any leaf is opened and a runaway summary is charged to every lookup, not just its own. `generated=` is bumped only when the body changes, so a rerun over an unchanged tree is a byte-identical no-op; `--dry-run` reports and writes nothing, `--check` exits 1 on drift, `--only <goal>` regenerates one index.

- chore: `tier-manifest.json` drops its dead playbook map (P2.3, v13 → **v14**). `tiers.<tier>.playbook_root` and `tiers.<tier>.playbook_paths` — 4 roots and 50 paths naming the `playbooks/<tier>/<group>/<slug>` layout deleted in the commit before this one — are gone, and `regen-tier-manifest.py` now strips them rather than copying the previous `tiers` block through verbatim, so they cannot come back on the next run. Nothing read them: `grep` over `faion-cli` finds neither key in any `.go` file, and `faion-net-be` touches exactly one field of a tier block (`preview_percentage`, in `preview_for`) while `required_tier_for_path` resolves meta.json-first against `entries`. `entries` is byte-for-byte unchanged at **3,107** — +0 added, -0 removed, ~0 changed — because the deleted subtree carried no `meta.json` and so was never in the manifest to begin with. The `knowledge_root` / `knowledge_paths` pair is the same shape of dead field and is left alone on purpose: it belongs to the knowledge layer, is 66% stale by an earlier audit's count, and removing it is a knowledge-layer decision, not a side effect of a playbook fix.

- chore: the dead tier-playbook subtree leaves the repo (P2.3). `skills/faion/playbooks/{free,solo,pro,geek}/<group>/<slug>/playbook.md` — **120 playbook bodies** plus 107 envelope files, 227 files in a `group/slug` scheme the corpus abandoned at F-067 — deleted, along with `scripts/validate-tier-playbook.py`, whose entire corpus was that subtree. Checked before deleting, four ways. **The CLI never packs it**: `faion-cli` classifies a playbook path as `playbooks/<domain>/<slug>/` (`internal/content/kind.go`) and reads tier from each leaf's own `meta.json`; no Go file outside tests names a tier directory. **The manifest never gates it**: all 455 playbook entries in `skills/tier-manifest.json` sit under the 11 goal dirs and not one under a tier dir, because the subtree carries no `meta.json` at all — so those 120 files were ungated content, reachable by nobody. **The backend never reads it**: `faion-net-be/apps/cli/tier_gating.py` resolves tier meta.json-first and touches exactly one field of `tiers.<t>` (`preview_percentage`); the `playbook_root` / `playbook_paths` arrays pointing into the subtree are read by no code in either repo. And **it duplicates nothing**: zero of its 120 slugs collide with the 455 goal-dir slugs, so this was a parallel disconnected corpus, not a second copy — which is also why deleting it removes no content that any surface could serve. `SKILL.md`'s Playbooks section, which still described tier directories as the gating boundary, now describes the layout that exists; `.aidocs/conventions/playbooks/` is marked retired in place rather than deleted, since it is the record of how those files were authored.

- chore: the **2,448** `.bak` migration sidecars leave the repo (P2.5). `methodology-v1.xml.bak` (1,514), `playbook.yaml.bak` (455), `body.md.bak` (455), `AGENTS.md.v1.bak` (20) and four v1 content files, all written by `migrate-methodology-to-v2.py`, `migrate-playbook-to-v2.py` and `migrate-playbook-yaml-to-xml.py` as rollback scratch and then never removed. They cost zero blob bytes — the CLI's `packablePath` ships `.md`/`.xml` anywhere, `.py`/`.sh` under `scripts/` and `.tsv`/`.txt` under `lexicon/`, so a `.bak` was never packable — but they carry repo weight and have now misled two separate audits into counting them as corpus content. Checked before deleting. Nothing reads them: the only `.bak` hits outside the files themselves are the three migration scripts *writing* them, `tests/test_snapshot.sh` moving a fixture aside, and prose in two corpus methodologies about backing up dotfiles; `skills/tier-manifest.json` has zero `.bak` paths and the 22 `INDEX.xml` files list none. And every one has a live successor: 2,444 by direct name, and the four `content/0X-*.xml.v1.bak` in `research/audience-segmentation` only look orphaned because the v2 rename changed the filenames — that directory carries the full canonical `01-core-rules` through `06-decision-tree` set. `*.bak` added to `.gitignore` so the next migration run does not put them back. Validators 1-10 byte-identical, and `regen-tier-manifest.py --dry-run` reports no entry change.

- fix: the stale wikilinks are gone from the corpus (P2.1). `remap-dangling-wikilinks.py` applied over 301 leaf `AGENTS.md` files: **232 links remapped**, **291 dropped** (234 `## Related` bullets, 57 `## Assumes Loaded` rows, nothing left half-edited mid-line), and **57 `## Assumes Loaded` sections removed** because dropping their only row left a header with no table under it — the section is optional in `validate-methodology-v2.py`, so no section beats an empty one. Dangling links fall from **544 to 21**, and all 21 remaining are the two deliberate non-references: `[[Related]]` in the "covered by a more specific methodology in `[[Related]]`" Skip-If line of 20 infra leaves, and the `[[bin]]` of a Cargo manifest quoted in one `rust-error-handling` table cell. Nothing outside `skills/faion/knowledge/**/AGENTS.md` was touched: the 22 `INDEX.xml` files and `domains.xml` carry **zero** `slug=`/`path=` attributes pointing at a missing methodology, the `meta.json` hits are `tags` keywords and `domain` names rather than references, and the `recipes/`, `fragments/`, `tools/` and `workflows/` matches are all the literal string `AGENTS.md`. Validators 1-10 byte-identical to the pre-change report; the failing sets of validators 3, 4 and 5 are the same six, nine and two directories as before. One reference class is knowingly left alone: the `**Backed by methodology**` lines in the 511 playbook `AGENTS.md` files still name pre-F-067 paths — 3,087 of their 4,016 refs are old paths whose basename resolves and 339 resolve to nothing at all. That is a separate defect an order of magnitude larger than this one, and fixing only the slice that happens to overlap these slugs would leave the file class inconsistent for no gain.

- feat: `scripts/remap-dangling-wikilinks.py` — the decision table for the stale `[[wikilinks]]` in leaf methodology `AGENTS.md` files, applied by script rather than by hand (P2.1). Measured over the 2,638 leaves: **8,938** wikilinks, of which **544 dangle** across **131 distinct slugs**. Every one is drift off the pre-F-067 role taxonomy, not missing knowledge, and they come in four shapes. Old paths (`solo/dev/software-architect/quality-attributes`) whose basename still resolves — remapped automatically, no table entry needed, 130 links. Title-slug drift, where the link carries the H1 and the directory carries something else: `sdd-document-templates` is `sdd/templates` (62 links, the single largest group), `docker-compose-devops` is `infra/docker-compose`, `docker-compose-infrastructure` is `infra/docker-compose-infra` — each confirmed by reading the target's H1, not by string distance. Slug variants — a dropped qualifier (`requirements-traceability-full-lifecycle`), a doubled underscore (`linear-issue-tracking__pm-agile`), a leaked domain annotation (`ai-assisted-specification-writing (sdd)`). And role or knowledge-base container names — `project-manager`, `growth-marketer`, `gtm-strategist`, `pm-traditional`, `software-developer`, `llm-integration` — which were never methodologies and have no successor to point at. Those are dropped, as is anything where more than one plausible target exists: `code-review-checklist` (42 links) could mean any of `code-review`, `ai-code-review-checklist`, `audit-grade-code-review-checklist` or `compliance-aware-code-review-checklist`, and a link resolving to the wrong methodology is worse than no link. 26 explicit remap entries, each justified in the source; everything else is dropped. Two targets are deliberately left alone: `[[Related]]` is prose pointing at the file's own section, and `[[bin]]` is Cargo-manifest syntax quoted inside a table cell.

- fix: type defects in the composable-layer validators and generator. Three real crash paths, all of which turn a diagnosable input into a traceback. `regen-fragment-index.py` called `.group(1)` on a possibly-`None` `re.search` for the `count=` attribute — an `INDEX.xml` that is not a generated index now raises `Abort` and exits 2 with the reason, instead of an `AttributeError`. `validate-recipes.py`, `validate-tools.py` and `validate-fragments.py` built `sorted()` over a `set[str | None]` from `Element.get()` on five index-agreement checks; a single attribute-less `<pack>`, `<tool>`, `<fragment>` or `<recipe>` element raised `TypeError` mid-run, so the one malformed entry the check exists to catch was the one input that killed it. Coerced with `or ""`, matching the `slugs` list beside them, so the empty name is reported as an index/disk mismatch. And the `schema_check` import in all three validators is now loaded through `importlib.util` from an absolute path derived from `__file__`, rather than through a `sys.path` mutation plus a bare `from schema_check import`: the old form leans on `sys.path[0]` being the script's own directory (true only when the file is the invoked script) and is unresolvable to any static checker that does not replay the mutation. All three run clean from an unrelated cwd; `ruff check` clean; validators 1-10 byte-identical to the pre-change report.

- feat: the composable layer ships at tier **free** (P1.5). All four recipes (`sdd-feature`, `audit-and-fix` solo; `research-first-build`, `article-pipeline` pro), all five paid fragment packs (`gate`, `research`, `sdd` solo; `build`, `article` pro) and `tools/research` move to free — 10 manifest entries retiered, none added or removed. Tier histogram free 136 → **146**, solo 864 → **858**, pro 1413 → **1409**, geek 694 unchanged, total 3,107. Manifest v12 → **v13**; the whole `Prior notes, verbatim:` chain is preserved. The argument is F031's, made about the UA→EN lexicon: a paid lexicon would mean free users cannot search in their own language. This layer is the same shape of thing — the mechanism that makes an agent's output correct — and gating a mechanism does not sell tiers, it makes free-tier output worse and burns trust before conversion. What a tier buys is the **content** a pipeline consumes: 2,638 methodologies and 455 playbooks stay gated exactly as they were. Two consequences forced the scope rather than taste. `validate-recipes.py` enforces tier monotonicity, so a free recipe cannot compose a paid fragment — moving the recipe layer moves every fragment pack it composes, which is all of them. And `validate-fragments.py` enforces the tool direction, so `tools/research` had to follow `research-evidence-table`, which names `source-table`: a free fragment naming a solo tool is an instruction its reader cannot run. `tools/game-dev` stays **solo** — no fragment names it, and scaffolding a systemd unit and an nginx vhost is content, not mechanism. Tier prose corrected everywhere it was asserted: the three pack `AGENTS.md` tables and their gotchas, `SKILL.md`'s recipe row, and the five `meta.json` summaries that justified a tier in words. Validators 8/9/10 green: 4/4 recipes, 24 fragments, 5 tools, 0 findings.

- fix: the quality gate stops calling its subject an article (P1.4). `corpus:gate-runner` and `corpus:gate-fixer` read `{{slot:subject}}` where they read `{{slot:article}}`, and their prose is rewritten to match: the subject is whatever the pipeline gates — one file, a directory, a repository — and the commands under `Inputs:` decide what "valid" means. Both hard boundaries were article-shaped and are now true of what the fragments actually do: the runner is a verdict and writes nothing at all, the fixer edits only the files the findings name and only inside the subject path. This is the measured centrepiece of the one pipeline arm that scored 30/30 in the blind five-arm run, and three of the four recipes that compose it are code pipelines that had to pass a directory in a slot called `article`. Every binding updated: `sdd-feature` (bootstrap, fix), `audit-and-fix` (checks, fix), `research-first-build` (bootstrap, fix) rename the key; `article-pipeline`'s `review` stage fills both `article` (its own editor prompt) and `subject` (the gate) from the same var, which is the shape `recipes/AGENTS.md` now documents in place of the deleted historical-reasons note. Nothing else in the corpus referenced the old key, and no non-test Go file in `faion-cli` names it — the CLI's `slot:article` hits are all synthetic fixtures under `internal/workflow/testdata/` and `*_test.go`, which carry their own fragment bodies. `validate-recipes.py` 4/4 with 0 findings, `validate-fragments.py` 24 fragments with 0 findings; the three L2 indexes are byte-identical, since no fragment was added or renamed.

- fix: `validate-fragments.py` checks name uniqueness over the whole prefix, not just `*.md`. The CLI derives a corpus name from the basename minus its last extension (`internal/frag/corpus.go`), flat over everything `vfs-pack` ships under `faion/fragments/` — `.md` **and** `.xml`. Checking only fragment bodies would have let a per-pack `INDEX.xml` land beside the library one and make `corpus:INDEX` ambiguous, which is exactly the trap the new index creates for the next author. Demonstrated on both shapes: a duplicated fragment basename across two packs and a second `INDEX.xml` inside a pack each produce their finding.

- docs: the three pack `AGENTS.md` files point at what now enforces them. `fragments/`, `tools/` and `recipes/` each gain their `INDEX.xml` in the layout with the never-hand-edit note, a `## Validation` section naming the validator and linking its schemas, and the rules the validators made precise: the `Inputs:` and hard-boundary rules bind **role** fragments only (a shared include block or an emitted block is exempt — the distinction was implicit in the tree and nowhere in the prose), and a recipe stage fills exactly the slots its fragments declare, no more. The fragment `## Packs` table also gains the `search/` row it had been missing since the pack shipped — five packs listed where six exist is exactly the drift an index is supposed to end. All three stay inside the 20-80 line budget (80 / 47 / 47).

- fix: `deploy-scaffold.card.md` documents the eight flags it was hiding — `--test-labels`, `--workers`, `--rate`, `--burst`, `--ssh-host`, `--ssh-user`, `--ssh-addr`, `--ssh-port`. The card-first rule says an agent must be able to run the tool having read the card and nothing else, and these were reachable only by opening `deploy-scaffold.py`, which the rule forbids: the worker count, the nginx rate limit and the entire deploy target were undocumented capabilities. Three grouped lines, so the card lands at 38 of its 40 permitted. This is the only finding `validate-tools.py` produced across all five shipped tools; nothing else in the pack layer was broken.

- chore: `f066-validate-all.sh` runs 10 validators, not 8 — `validate-fragments` as step 9 and `validate-tools` as step 10, so the composable layer is checked by the same command that checks the corpus rather than by remembering to run two more scripts.

- feat: `validate-recipes.py` gains schema, tier and slot checks. `meta.json` and `recipe.json` are now validated against `docs/schemas/recipe-meta.schema.json` and `docs/schemas/recipe.schema.json`, and the card's shape check moves to `card.schema.json` so the six-section rule has one definition instead of two. Three new checks. **Tier monotonicity**: every fragment a recipe composes must be gated at or below the recipe's own tier — a solo recipe whose stages are pro fragments is a pipeline a solo user can pick and cannot run, and the failure would surface mid-run rather than at the pick; the rule was already written in `recipes/AGENTS.md` and had no enforcement. **Slot coverage**: a stage must fill every `{{slot:NAME}}` its prompt, verifier and fixer fragments declare — counting slots pulled in through `{{include:}}`, since the composer expands first and substitutes after — and must not fill a slot no fragment it composes reads, which is the silent half: a stale slot key is invisible at compile time and simply never reaches a prompt. **Index agreement**: `recipes/INDEX.xml` must list exactly the recipes on disk, with a matching `count` and alphabetical order. Demonstrated red before green on a mutated copy of `sdd-feature`: twelve findings covering all five new checks plus the CLI's own refusal, and 4/4 clean on the shipped recipes.

- feat: `scripts/validate-fragments.py` and `scripts/validate-tools.py` — validators 9 and 10. Tools had **zero** validation until now, which is why `deploy-scaffold.card.md` could drift eight flags away from its script and nothing noticed. `validate-fragments.py` checks pack `meta.json` against its schema and `group` against the directory, flat name uniqueness across the whole tree (`corpus:` names are path-independent, so two packs shipping one basename make every reference ambiguous), `{{include:}}` resolution and `corpus:`-only includes with no self-cycle, `<name>.schema.md` pairing and JSON validity, the 80-line body cap, and — for **role** fragments only, identified by an opening `You are a|an|the <role>.` — a stated hard boundary plus slots gathered under a trailing `Inputs:` heading with none above it. Shared include blocks and emitted blocks are exempt by design: `research-source-discipline` declares no slots on purpose and `search-refine` is text the CLI prints to a user. It also enforces the direction of tier the library gotcha already named — a fragment naming a tool must be gated at or **above** that tool's pack, since a free fragment naming a solo tool is an instruction its reader cannot follow. `validate-tools.py` checks pack `meta.json`, card↔script pairing both ways, card shape through `card.schema.json`, that `## Invoke` writes `{script}` and carries no literal `scripts/` path, that every exit status the script can return is explained under `## Outputs` (Python exits read from `return <int>` inside `def main` plus literal `sys.exit(<int>)` — scoping to `main` matters, because `deploy-scaffold.py` has a `return 301` inside a heredoc of nginx config and it is not an exit status), that the script has a shebang and imports only the standard library, and that **every long option the script's parser defines appears in `## Inputs`**, with anything the card mentions and the script does not define failing in the other direction. Both are wired into `f066-validate-all.sh` as steps 9 and 10. `scripts/schema_check.py` supports them: a dependency-free checker for exactly the JSON Schema keywords `docs/schemas/` uses, which **refuses any schema using a keyword it does not know** rather than silently under-enforcing, and which was cross-checked against the `jsonschema` package on every shipped file and on ten deliberate mutations — identical verdicts throughout. Demonstrated red before green: nine findings from a mutated fragment pack, eight from a mutated tool pack.

- feat: JSON Schemas for the fragment / recipe / tool layer under `docs/schemas/` (P1.3). The knowledge layer has `methodology-xml-schema.md` and seven validators; this layer's rules lived as prose inside three `AGENTS.md` files, which is a bar nobody checks. Five schemas: `fragment-pack-meta`, `tool-pack-meta` and `recipe-meta` (the directory-gating `meta.json`, `additionalProperties: false` so a typo'd key is a finding rather than a silently ignored one, slug patterns that keep a pack slug from colliding with a fragment or tool name, `summary` given a `minLength` because it is copied verbatim into `INDEX.xml` and is the only thing an agent reads before picking); `recipe` (the F027 `recipe.json`, mirroring the typed model in `faion-cli internal/workflow/recipe.go` — `recipe: 1`, the closed five-value `pattern` set, the closed `{read, write, net}` capability model, `retry` 0-3, `max_rounds` 1-3, `max_concurrent` 1-16, `fanout.over` pinned to the `stage:<id>.file#<path>` form since there is no fan-out over a var, and a `corpus:` -only fragment reference pattern); and `card` (the parsed form of a recipe or tool card — six sections as an ordered `prefixItems` tuple, `lines` capped at 40, `invoke` and `inputs` non-empty). The card schema describes the parsed object rather than the Markdown because the card is Markdown and pretending otherwise would have meant a schema nothing could run. The CLI's own `faion workflow validate` stays the authority on cross-stage references; these encode the checks that must hold with no binary present. Verified against all 13 shipped `meta.json` / `recipe.json` files: zero findings.

- feat: `SKILL.md` routes to the composable layer — a third branch beside knowledge and playbooks. The umbrella an agent reads first contained **zero** mentions of fragments, recipes or tools, so the layer with the only measured quality advantage in the product was reachable only by an agent that already knew the directory existed. New routing row for the task-shaped need — "build a research-first product", "run this SDD feature", "write and translate an article", "audit and fix this tree" — pointing at `recipes/INDEX.xml` → `<name>.card.md`, with `fragments/INDEX.xml` and `tools/INDEX.xml` as the supporting indexes, plus the line that decides between the branches: a methodology tells you what good looks like, a recipe is the thing that runs. A short `## Recipes, fragments and tools` section names the four recipes with their tiers and stage counts, states card-first for both recipes and tools, and records that fragment tier ≤ recipe tier so picking a readable recipe never yields an unreadable stage. Frontmatter `description` gains clause (h) for the same trigger, because a branch the router never auto-invokes on is a branch that does not exist.

- feat: L2 indexes for the composable layer — `skills/faion/fragments/INDEX.xml` (6 packs, 24 fragments), `skills/faion/recipes/INDEX.xml` (4 recipes, 6 / 13 / 6 / 4 stages) and `skills/faion/tools/INDEX.xml` (3 packs, 5 tools), generated by `regen-fragment-index.py` in the same shape as `knowledge/<domain>/INDEX.xml`: root `<index domain count version generated>`, a `<description>` stating the retrieval step, then entries alphabetical by slug carrying `slug` + `tier` + `path` + `<summary>`. Each carries the one extra thing its kind needs to be routed from without opening a leaf: a fragment pack lists every `corpus:<name>` beneath it and the paired `corpus:<name>.schema` where one exists, a recipe carries its stage count and its card path, a tool pack lists each tool with its card and its script. ~400 KB of fragments, recipes and tools was the only part of the corpus with a measured quality advantage and the only part with no way in.

- feat: `scripts/regen-fragment-index.py` — the generator for the composable layer's L2 indexes (P1.1). Knowledge routes `domains.xml` → `<domain>/INDEX.xml` and playbooks route `taxonomy.xml` → `by-goal/<goal>/INDEX.xml`; `fragments/`, `recipes/` and `tools/` had no index of any kind, so the only way to reach `research-first-build` was to already know the directory existed. Every entry is derived from the pack's own `meta.json` (slug, tier, group, summary) plus what is on disk (fragment basenames and their paired `.schema.md`, card and script paths, `recipe.json` stage counts), so an index cannot drift from the tree the way a hand-kept list does. Modelled on `regen-tier-manifest.py`, which reads `meta.json` — deliberately **not** on `scripts/build-domain-index-v2.py`, which reads YAML frontmatter no envelope carries and empties the `INDEX.xml` it targets. `generated=` is bumped only when the body actually changes, so a rerun over an unchanged tree is a byte-identical no-op instead of a one-line date diff. `--dry-run` reports and writes nothing, `--check` exits 1 on drift, `--only <domain>` regenerates one index.

- feat: make the unpackable `## Templates` rows deliverable (P0.4 step 4) — 3,949 rows named a file `vfs-pack` never puts in the blob (`.json` 1,765, `.py` outside `scripts/` 617, `.yaml` 560, `.sh` 170, `.txt` outside `lexicon/` 142, and 60 other extensions), so no CLI surface could fetch any of them. Triaged mechanically: **3,514 real artifacts inlined** as fenced code blocks under a new `## Template Contents` section at the *end* of each of 2,030 envelopes — the `AGENTS.md` itself ships, so the body becomes deliverable at the cost of bytes rather than a new blob entry — and **435 scaffolding rows dropped**, taking 271 files with them (164 files stayed because `content/*.xml` or `scripts/` in the same methodology still names them). The `## Templates` table keeps every surviving row as the index and gains one line telling the reader the body is inlined below and the path must not be fetched, because a row that still invites a failing `get-content` has not been fixed. Fence language tags are derived per extension, with double-suffixes (`golden-set.jsonl.tmpl`) resolving through the inner extension, and fence length grows past any backtick run in the body. The five-key faion header is stripped from the inlined copy: it is authoring metadata already present in the table, and it has no business being pasted into a real `pyproject.toml`. Classifier: an unfinished marker in *value* position, a self-description as an unwritten skeleton, echo placeholders whose value repeats the key, a sub-200-byte body carrying a placeholder, zero non-comment lines, or placeholder saturation at or above 0.5/line. Measured on a **blind hold-out of 20** stratified across ten extensions: **18/20 = 90%**, both errors false-*keeps*; across all 43 hand-labeled files there were **zero false deletes**, which is the error direction that matters, since a false keep costs bytes and a false delete destroys work. Two rules were tried and rejected on evidence: a byte-size threshold (it condemned a complete Prettier config and two real worked trajectories for being short) and an empty-shell scalar ratio (it introduced a false delete without catching its target). Shipping `.md`/`.xml` surface 70.45 MB → 74.23 MB, **+3.78 MB**, against the ~18.9 MB of headroom; methodology envelopes 11.07 MB → 14.85 MB, median growth +1.5 KB, p90 +4.2 KB, worst case 4 KB → 23 KB. That worst case is the real cost of this trade and is worth recording: routing reads the envelope, so a handful of template-dense methodologies now cost materially more to route into, and the inlined section is deliberately placed last so the routing content keeps the top of the file. Tier manifest unchanged at 3,107 entries (directory-gated, no `meta.json` touched); validators 1-8 identical to the pre-change baseline, including the 6 / 9 / 2 pre-existing failures in validators 3 / 4 / 5, which this change neither caused nor fixed.

- fix: retire the `TBD-template-header` placeholder, 183 → 0 (P0.4 step 3) — every one of these templates was scaffolded and then left with its `purpose:` line reading the literal placeholder, so the one field meant to say what the file is said nothing for as long as the file has existed. Split mechanically on whether the file carries a real reusable artifact (`docs/skill-authoring.md` line 47): **9 deleted** as scaffolding, each condemned by an unfinished marker in *value* position (`"todo": "fill per 04-procedure.xml"`, `<instruction>TODO</instruction>`) — the file saying of itself that it was never written — with their `## Templates` rows removed alongside; **174 kept and their headers filled**, 155 from the Purpose cell the methodology had already written for that file in its own `## Templates` table, 17 from the file's own leading docstring or banner comment (`rrf.py` → "Reciprocal Rank Fusion (RRF) implementation"), 2 from the filename where the file offers nothing else. Size alone was explicitly rejected as the test: a first pass condemned `dev/javascript/templates/prettierrc.json` (a complete 8-key Prettier config) and `agent-trajectory-eval-method/templates/golden-trajectory.jsonl` (two real worked trajectories) purely for being short, so density formats need the marker test, not a byte threshold. Placeholder *density* likewise never condemns a large file on its own — a fill-in record is supposed to have slots. Tier manifest unaffected (3,107 entries, directory-gated, no `meta.json` touched).

- fix: file the 30 mis-filed template rows under `## Templates` (P0.4 step 2) — 15 methodologies (of the 23 written in the compact single-manifest style) listed their `templates/*` files inside a `## Content` table alongside the content and the validator script. Every tool that reads templates keys on the `## Templates` heading, so a template filed under `## Content` is a template nothing checks: `validate-methodology-templates.py` skipped all 30, and six of them (`graph-design-record{,-no-graph}.yaml`, `schema-pair-record{,-two-call}.yaml`, `closed-set-validation-contract{,-mixed}.yaml`) turned out to carry no canonical five-key header at all — they were shipped unchecked for as long as they have existed. Rows moved into a real `## Templates` table placed before `## Related`, purposes carried over verbatim, and the six headers written from each file's own contract. The `scripts/*` rows in those same tables were deliberately left where they are: those name files that exist and that `vfs-pack` ships, so nothing is being promised that cannot be delivered, and the canonical three-column `## Scripts` table has a `When to call` column this format supplies no honest answer for. Validator 5 stays at 2,637/2,639 — the two failures are the pre-existing `sdd/{ui-ux-design,user-flows}-template` ones, untouched here.

- fix: drop methodology table rows naming a file that does not exist (P0.4 step 1) — 223 rows across 211 `AGENTS.md` envelopes: **193 `## Scripts` rows** promising a `scripts/validate-<slug>.py` that was never written (the `scripts/` directory is empty in every one of the 191 methodologies affected), and **30 `## Content (load on demand)` rows** promising a `content/*.xml` that was never authored (15 × `04-procedure.xml`, 14 × `05-examples.xml`, 1 × `03-failure-modes.xml`, over 27 methodologies). 180 `## Scripts` headings were removed outright because the dead row was the table's only row; no `## Content` table was emptied, so every methodology still declares a body. Deletion was driven by a script that resolves each row's first cell against the filesystem — the disk is the arbiter, not a hand-kept list. A promise the tool cannot keep is worse than no promise: `faion get-content` on any of these paths returned nothing, and the agent that asked learned the manifest lies. `validate-methodology-scripts.py` stays 2,639/2,639 because its B4.1 rule keys on a `<schema>` in `02-output-contract.xml`, and none of the 193 declared one — the rows were unvalidated fiction, which is why they survived this long.

- feat: ship the search refine fragment at tier **free** (`skills/faion/fragments/search/search-refine.md`, `corpus:search-refine`). faion-cli's F030 removed the ranking model from `faion search`; when the CLI's own `<coverage>` verdict is below `strong` it emits a second-pass instruction, and that instruction is prose that teaches — i.e. content, so it lives here and travels in the blob like every other piece of corpus text. It is resolved through `frag` + `Compose` with the slots the search fills (`query`, `level`, `matched`, `unmatched`, `next`, `pass`, `max_pass`), and the CLI falls back to a terse built-in whenever it cannot resolve, so a seed build still works. **Tier free deliberately**: a gated refine block would mean a free user cannot use the search loop at all, which would make the cheapest tier the worst-behaved one — the loop is how a lexical search recovers from a thin first result, and charging for it would be charging for the recovery from our own limitation. Tier manifest 3,106 → 3,107 entries (+1 added / -0 removed / ~0 changed); version stays v12, so the `Prior notes, verbatim:` chain is preserved byte-for-byte.

- chore: register the research fragment pack in the tier manifest (3,105 → 3,106 entries, +1 added / -0 removed / ~0 changed) — one entry gating `skills/faion/fragments/research/` at tier **solo**, under the directory-coverage rule already applied to every fragment library. Version stays v12, so `build_notes()` returns the existing `notes` untouched and the whole `Prior notes, verbatim:` chain is preserved byte-for-byte.

- feat: `research-first-build` researches against live sources — 11 → 13 stages. A new `research_plan` stage (`corpus:research-desk-brief`) writes the angles, queries and stop rules the three research stages then follow; `research_two` swaps `build-domain-cataloger` for `corpus:research-market-analyst`, so the market axis runs under the competitor breadth floor and the mandatory debunk pass instead of the generic cataloger; and a new `evidence` stage (`corpus:research-evidence-table`) sits between the research and the concept pick, because a concept chosen from unsourced claims is a guess with a rationale attached. `build-domain-cataloger` was upgraded rather than left behind: it includes the discipline block, is told to use its own web tools and to follow the plan when one is given, its Evidence field now demands a URL, an access date and a confidence tag (and "no reliable public source found" where there is none, instead of a plausible attribution), and it emits `<axis>-claims.jsonl` alongside its catalog so all three axes feed the same gate. Every fragment reference verified resolving through `faion frag get corpus:<name>` against a CLI embedded with the real corpus — the four new ones list at tier `solo` and compose with the discipline block expanded inline — and `validate-recipes.py --strict` reports 4/4 recipes, 0 fragment findings, with `faion workflow validate` accepting the 13-stage recipe.

- feat: `validate-recipes.py` gains the research-sourcing gate — validator 8 now also reads the fragment library, because a prose bar nobody checks decays into a bar nobody meets. A fragment is a **research role** when its opening role line names one (`You are a|an|the <role>.`, matched on the role noun alone, so "You are the concept synthesizer. You read the research catalogs" is not one and an SDD intake *analyzer* is not an *analyst*) or when it lives under `fragments/research/`; such a fragment must contain `{{include:corpus:research-source-discipline}}`. The block itself is probed for its four anchors — URL plus access date, the H/M/L definitions, the no-reliable-figure path, the `faion fact add` provenance line — against its whitespace-collapsed text, since a fragment hard-wrapped at ~68 columns does not stop stating a requirement because the requirement fell across a line break. The check runs library-wide even when named recipe dirs are given: a research fragment that drops the block breaks every recipe composing it, including the ones not on the command line. Demonstrated red before green twice — stripping the include from `research-market-analyst` produced exactly its finding, and replacing "no reliable public figure found" in the discipline block produced exactly the anchor finding — then 4/4 recipes and 0 fragment findings once restored.

- feat: research fragment pack at `skills/faion/fragments/research/` (tier **solo**) — four fragments that make the corpus *demand* the fetch instead of standing in for it. `research-source-discipline` is the shared block the others pull in with `{{include:}}` and declares no slots on purpose: load-bearing means "removing it changes a decision, a ranking or a number", every load-bearing claim carries a URL **and the date you accessed it**, H is a primary source fetched now / M a secondary that discloses its method / L inference or an estimator that hides one, a figure prints its date and says so when the freshest available is over a year old, an unfindable number is written "no reliable public figure found" plus the searches run rather than as a plausible one, anything used from training and not re-verified is labelled "recalled from training, not re-verified" and tagged L, conflicting sources are resolved by naming the authoritative one (a filing or registry entry over an estimator with an undisclosed method) and printing the rejected figure, and findings are recorded with `faion fact add --source --quote` so a later run can re-check rather than trust. `research-market-analyst` adds competitor breadth floors (≥25 whole-market, ≥12 named niche, never fewer than the brief asks), per-competitor sourcing, and a mandatory **Contested figures** debunk pass; `research-evidence-table` is the output contract and runs the `source-table` tool, whose invocation it reads from `faion tools card source-table` rather than guessing a path; `research-desk-brief` turns a question into 4-8 angles of *different source kinds* with real queries and a stop rule. Every one names the agent's own web tools explicitly and forbids answering from the corpus or from memory. Measured motivation (2026-08-11, one brief, blind judges): the pipeline run produced **14 competitors and 0 source URLs**, a plain agent that went to the web produced **31 and 108** and won on research depth — and before this pack no fragment in the corpus required a URL, an access date, a confidence tag or a source floor, so the research prompts asked for less than an unprompted agent does by default. Tier is solo to match the `tools/research` pack the evidence fragment invokes: a free fragment naming a solo tool would be uninvokable. `fragments/AGENTS.md` documents the library (all five packs) at the library level, not per pack — corpus fragment names are the flat file basename, so five per-pack `AGENTS.md` files would make `corpus:AGENTS` ambiguous.

- fix: tool cards write `{script}` in `## Invoke` (CR-005) — all five F029 cards wrote `python3 scripts/foo.py …` / `sh scripts/venv-bootstrap.sh …`, a path correct only inside this repo, while the CLI's `Card.ResolveInvoke` substitutes the materialised absolute path into a `{script}` placeholder. Every card was therefore resolving through the fallback branch, which rewrites any token whose basename matches the script's filename — a shim that cannot tell the script from an argument that happens to share its name, and that silently does nothing when a card renames the script. The placeholder is the contract; the fallback is compatibility for packs outside this repo. Six lines changed across five files, every other section byte-identical; `tools/AGENTS.md` now states the rule so the next pack author never reads the resolver to find it. Verified against the CLI built with the real corpus: `faion tools card <name>` reports the resolved absolute path for all five (python-web at tier free, game-dev and research at geek) with every argument placeholder preserved and no literal `scripts/` token left. Recorded as `.aidocs/crs/done/CR-005-tool-card-invoke-placeholder.md`.

- chore: register the recipe library and the gate pack in the tier manifest (v11 → v12, 3,099 → 3,105 entries, +6 added / -0 removed / ~0 changed) — `regen-tier-manifest.py` gained a sixth walk over `skills/faion/recipes/<name>/meta.json`, one entry gating each `recipe.json` and its card under the same directory-coverage rule `vfs-pack` applies to knowledge, playbooks, fragment libraries, tool packs and the lexicon. The six new entries are the four recipes plus the `fragments/gate` (solo) and `fragments/build` (pro) packs. Prior `notes` preserved verbatim behind the existing `Prior notes, verbatim:` prefix chain.

- feat: `scripts/validate-recipes.py` — the gate that keeps a recipe and its card in agreement, wired into `f066-validate-all.sh` as validator 8. Fails on: a card missing one of the six ordered sections or over the 40-line cap; a `{{var:}}` (or a declared var) absent from the card's `## Inputs`, because a card the agent cannot invoke from is not a contract; a fragment reference that resolves to no file under `skills/faion/fragments/` — and a non-`corpus:` reference at all, since a shipped recipe composing a user-space fragment resolves on the author's machine and nowhere else; and any recipe `faion workflow validate` refuses (required vars are supplied as placeholders so a var-resolution failure is never mistaken for a structural one). The binary is located via `$FAION_BIN`, then `../faion-cli/bin/faion`, then PATH; absent, the compile check is skipped with a notice, and `--strict` makes absence fatal. Demonstrated red before green: a fixture with a missing `## Cost`, an undocumented var, `corpus:no-such-fragment` and a forward stage reference produced exactly four findings and exit 1; the four shipped recipes pass 4/4 clean under `--strict`.

- feat: workflow recipe library at `skills/faion/recipes/` — four F027 recipes an agent picks between from cards, so the CLI never has to guess a pipeline shape it has no model to guess with. `sdd-feature` (solo, 6 stages: intake → plan → bootstrap gate → per-task fan-out over isolated worktrees → review → gated fix), `research-first-build` (pro, 11 stages: three parameterised research catalogs → quantified concept pick → design → plan → fan-out → assets → bootstrap gate → review → gated fix, distilled from the real g5 pipeline), `article-pipeline` (pro, 6 stages: outline → per-section fan-out → assemble → gated editorial pass → translate → language review) and `audit-and-fix` (solo, 4 stages, no fan-out — the smallest, deliberately: bootstrap → machine checks → cited review → gated fix). Four different stage shapes on purpose: the catalog teaches by contrast. Each dir is `meta.json` + `recipe.json` + an F029-shaped card (six ordered sections, ≤40 lines) documenting every `{{var:}}` the recipe declares. Rules recorded in `recipes/AGENTS.md`: card-first, `corpus:` references only, fragment tier ≤ recipe tier, a `bootstrap` stage wherever the pipeline runs tests, and service identity and paths always as vars so two runs cannot collide on a name, a port or a state dir. Verified with the CLI built against the real corpus: all 23 fragment references resolve via `faion frag get`, and `faion workflow validate` accepts all four (6 / 11 / 6 / 4 stages). Gotcha recorded: `vfs-pack` ships `.md`/`.xml` only, so the cards ship in the CLI blob but `recipe.json` does not — the same delivery gap F029 has with `scripts/*.py`.

- feat: research-first build fragment pack at `skills/faion/fragments/build/` (tier **pro**) — four role fragments generalised from the g5 research-first pipeline with the game specifics removed: `build-domain-cataloger` (one parameterised research axis in, one named catalog out, entries carrying dated and verifiable evidence, uncertain attributions marked rather than invented), `build-concept-synthesizer` plus its paired schema (candidates combined ACROSS catalogs, scored on envelope fit / evidence / build cost / value, winner recorded with its runner-up and what was sacrificed — a pick with no stated sacrifice is not a pick), `build-solution-designer` (concept → EARS spec for the first buildable slice, and it must name the identities the build parameterises: service name, ports, hostnames, state dirs — the g3/g4 lesson where two pipelines emitted the same service name and would have clobbered each other), and `build-asset-director` (non-code assets, reuse before create, self-contained and dependency-free).

- feat: `corpus:sdd-planner.schema` — the planner's output contract as a paired schema (`feature_id` plus a non-empty `tasks` array of `{id, title, summary, feature_folder, depends_on}`). Without it the planner returns prose and nothing downstream can fan out: the recipe grammar ranges only over an earlier stage's JSON array, so a per-task implementation fan-out needs the plan to *be* an array. Generalised from the shape the g5 pipeline proved in anger.

- feat: verification-gate fragment pack at `skills/faion/fragments/gate/` (tier **solo**) — `gate-runner`, `gate-runner.schema` and `gate-fixer` move out of the pro-tier article library, because a gate is plumbing every gated pipeline needs and the solo-tier recipes (`sdd-feature`, `audit-and-fix`) could not have resolved a pro fragment. Corpus names are path-independent, so `corpus:gate-runner` still resolves for the article pipeline; only the tier gating changes. New `gate-bootstrap` joins them: it makes the project's toolchain exist and proves the gate commands run before any stage depends on them — the g3/g4 lesson, where pipelines burned fix rounds on a missing venv, turned into a stage instead of an assumption. Its hard boundary is environment artifacts only: it never edits source, and a project that declares no dependencies is a finding, not an invitation to invent a bootstrap.

- fix: validate-lexicon.py return annotation — validate_lexicon returns the prefix set that validate_stopwords consumes, not None.
- chore: register the lexicon in the tier manifest (v10 → v11, 3,098 → 3,099 entries, +1 added / -0 removed / ~0 changed) — `regen-tier-manifest.py` gained a fifth walk over `skills/faion/lexicon/meta.json`, alongside knowledge, playbooks, fragment libraries and tool packs, so one entry gates `ua-en.tsv` and `ua-stopwords.txt` under the same directory-coverage rule `vfs-pack` applies. Prior `notes` preserved verbatim behind the existing `Prior notes, verbatim:` prefix chain.

- feat: `scripts/validate-lexicon.py` — the gate that keeps the lexicon mined rather than invented, wired into `f066-validate-all.sh` as validator 7. Eight checks: LF/no-BOM/NFC hygiene with `#` comments confined to the leading header block; exactly three tab-separated columns; `ua_prefix` one lowercase Ukrainian token with no duplicates (a prefix carrying an apostrophe gets a targeted hint — U+0027/U+2019/U+02BC all occur in the wild, so a prefix must be truncated before it); byte-wise sort order; **every `en` term attested at least once in the corpus**, because a term that occurs nowhere maps the query at nothing; `src` **re-derived from the corpus and compared to the declared value** rather than trusted; the 20% `observed` cap; and stopwords sorted, deduplicated and disjoint from the lexicon prefixes — a stopword starting with a lexicon prefix would be dropped before that prefix could ever fire. Demonstrated red before green: injected rows reproduced all seven shape and provenance failures plus the cap failure at 47.6%, then the shipped files pass clean.

- feat: UA→EN query lexicon as corpus data at `skills/faion/lexicon/` (tier **free**, deliberately — a paid-tier lexicon would mean free users cannot search in their own language, and the rows leak no paid content since they are English words, not slugs). `ua-en.tsv` carries 561 rows of `ua_prefix<TAB>en_terms<TAB>src`, byte-sorted, LF, NFC; `ua-stopwords.txt` carries 121 Ukrainian function words the runtime drops before scoring. Measured motivation: the corpus is English — 26,114 Cyrillic word tokens across 23,800 files, 5,806 of them the single boilerplate string `Ефективно для`, and zero of 2,638 methodology first-headings carry Cyrillic — so a Ukrainian query scores zero everywhere and falls through to the floor-fill, returning the alphabetical head of the corpus every time at recall ≈ 4.9%, i.e. chance. `ua_prefix` is one lowercase Ukrainian token with its inflectional tail removed and the runtime does longest-prefix matching, so `кеш` covers кеш/кешу/кешем/кешування for free; **no stemmer** — one was measured and gained exactly zero, because there is no Ukrainian index text to stem toward. Provenance is mined, not asserted: 25 rows `taxonomy` (prefix of a Ukrainian trigger word in `playbooks/taxonomy.xml`), 38 `domains`, 306 `tags`, 101 `title`, and 91 `observed` (16.2%, under the 20% cap). Verified against the real corpus with ten representative Ukrainian queries: all ten now reach a plausible slug — including `dev/web-scraping-resilience` for the retry/backoff query, one of the genuine targets the current prefilter never shortlists — where nine of the ten produce no signal at all without the lexicon.

- feat: index and tier-gate the tool packs — `skills/faion/tools/AGENTS.md` states the **card-first rule** (an agent must be able to run a tool having read only its `tools/<name>.card.md`; never open the script to work out arguments, never re-implement a tool that has a card), fixes the card's section order (`Purpose · Invoke · Inputs · Outputs · When NOT to use · Cost`, ≤40 lines) and the script contract (stdlib/POSIX only, deterministic, one summary line to stdout, `0` success / `1` the checked thing is wrong / `2` the tool could not run, never calls a model). `regen-tier-manifest.py` now also walks `skills/faion/tools/<pack>/meta.json` — one entry gates the pack's `scripts/` and cards, the directory-coverage rule already used for fragment libraries — and its `notes` handling was made lossless: `build_notes()` prepends the new version's note and keeps the previous one verbatim, returning `notes` unchanged when the manifest is already at the target version, so repeated regenerations neither stack prefixes nor drop history. Manifest v9 → v10, 3,095 → 3,098 entries (+3, no removals, no changes). Gotcha recorded: `vfs-pack` packs only `.md`/`.xml`, so cards ship in the CLI blob but `scripts/*.py|sh` do not — materialising a pack needs the packer allowlist widened or a separate delivery path.

- feat: `skills/faion/tools/research/` tool pack (tier **solo**) — `source-table.py` reads a claims JSONL (`{claim, url, date, confidence, load_bearing}`), writes a markdown evidence table plus a gaps report keyed by input line number, and **exits 1 when any load-bearing claim carries no source**. `load_bearing` defaults to true, so colour and context must be marked down explicitly rather than sourcing being opted into; a malformed `url`, a non-`YYYY-MM-DD` date and a missing confidence are reported without failing the run, and `--require-date` promotes an undated load-bearing claim to a failure. Encodes the measured loss where a control arm beat our pipeline mainly on sourced research — 108 URLs against 0.

- feat: `skills/faion/tools/game-dev/` tool pack (tier **solo**). `hmac-rng-golden.py` emits and re-verifies golden vectors for HMAC-SHA256 rejection-sampling randomness — the primitive six sibling backends each hand-rolled — parameterised over the four variants actually observed: `--word-bits 64` (first 8 digest bytes, then bump the counter) vs `32` (scan all eight u32 words first), and `--counter-encoding text` (`msg + sep + str(counter)`, `--counter-sep` covering both `|` and `|c`) vs `be32` (`struct.pack(">I", counter)`). Cross-checked against four independent implementations byte-for-byte over 8 bounds × 3 messages; `--verify` recomputes a golden file from its own declared parameters, so an edited or stale file cannot pass as pinned truth (exit 1 on mismatch). `deploy-scaffold.py` emits the systemd unit + nginx vhost + `deploy.sh` trio, deriving **every** collidable identity from `--name` — unit, unix user/group, `/var/lib/<name>`, nginx `limit_req` zone — after two sibling pipelines emitted the same service name and shared a state dir and a rate-limit zone; the identity line it prints is what a second pipeline diffs against, and `--check-local` exits 3 when the identity is already taken. Regex `location`s are always emitted quoted: unquoted, nginx reads `{8}` as a block open and `nginx -t` dies with `unknown directive "8}$"` (both branches verified against the real `nginx -t`).

- feat: first tool pack in the corpus — `skills/faion/tools/python-web/` (tier **free**), the shape every later pack follows: `meta.json` gating the pack dir, `scripts/<name>.py|sh`, and `tools/<name>.card.md` as the contract an agent reads *instead of* the script. `venv-bootstrap.sh` (POSIX sh) creates the `.venv`, installs `requirements.txt` and proves the imports, idempotent via a requirements checksum stamp inside the venv rather than a timestamp — the lesson from pipelines that ran `manage.py test` with no venv and spent fix-rounds on a phantom ImportError. `django-test-gate.py` runs a suite through the project's own venv (probing `<project>/.venv` then `<project>/../.venv`, the backend/+repo-root layout) and prints one line `{"ok":bool,"ran":N,"failures":[...]}`; exit 0 green / 1 red / 2 the suite never ran, which separates a red suite from a broken harness instead of reporting both as failure. Both stdlib/POSIX only, deterministic, zero model calls.

- feat: quota-gate platform adapter contract — the skill no longer implicitly assumes the NERO statusline: `SKILL.md`'s source-resolution section now documents the adapter contract (order unchanged: `$CLAUDE_SESSION_STATE` → `/tmp/claude-session-state.json` → `~/.claude/session-state.json`) with the JSON shape third-party writers must produce (`rate_limits.five_hour/seven_day.used_percentage`, mtime kept fresh) and UNKNOWN (rc=2) stated explicitly as the answer when no source exists — callers must gate conservatively, the gate never guesses GO. `scripts/quota_gate.py` `--source <path>` is now a hard override of env + both default paths: a missing/unreadable `--source` returns UNKNOWN instead of silently falling back to another file. Verified against GO/HOLD/bad-shape/missing/stale fixtures; still dependency-free.
- feat: SDD role fragment library at `skills/faion/fragments/sdd/` — six role fragments distilled from the sdd-batch-orchestrator workflow's role contracts (`corpus:sdd-intake-analyzer`, `sdd-planner`, `sdd-task-executor`, `sdd-wave-coordinator`, `sdd-code-reviewer`, `sdd-fix-applier`) plus paired verdict schemas `sdd-wave-coordinator.schema.md` (CLEAR/HOLD/ABORT with citation-bearing findings) and `sdd-code-reviewer.schema.md` (PASS/FAIL-WITH-NITS/FAIL with blocker citations), following the article library's conventions: `.md`-only packing, corpus name = path base minus extension, `{{slot:...}}` pointers placed last (static-first for provider caches), per-role hard boundary. Tier decision: **solo**, deliberately below the article library's pro — SDD is the solo-tier product core (`knowledge/solo/sdd/`) and no meta/manifest convention forces otherwise. Manifest regenerated (3,094 → 3,095 entries, notes preserved). Workflows `AGENTS.md` Related section points to the library.
- chore: remove track-wakeup.sh from plugin hooks — workspace-specific statusline tooling, not a product hook; lives in ~/.claude/hooks/ where its settings.json invoker already points. Dropped the stale f067 manifest backup file.
- feat: article pipeline fragment library (F027 T06) — first corpus fragment library at `skills/faion/fragments/article/` (tier pro, spec Q1 default — owner had not objected by execution time): eight role fragments distilled from `workflows/article-pipeline.js`, universal parts only (`corpus:article-outliner`, `article-section-writer`, `article-assembler`, `article-editor-reviewer`, `article-translator`, `article-language-reviewer`, plus generic `gate-runner` + `gate-fixer`), with paired wire schemas `article-outliner.schema.md` / `gate-runner.schema.md` (`.md` because vfs-pack packs only `.md`; corpus names are the path base minus extension, so they resolve as `corpus:<name>.schema` per the F027 pairing convention). Every role fragment carries the content-only hard boundary; slots are pointers placed last (static-first for provider caches). Tier registration: `regen-tier-manifest.py` now also walks `skills/faion/fragments/<library>/meta.json` — one entry gates the whole library dir, mirroring vfs-pack's directory-coverage rule; manifest regenerated to v9 (3,094 entries). Gotcha: never put `AGENTS.md`/`CLAUDE.md` (any non-fragment `.md`) under `skills/faion/fragments/` — every `.md` there packs as an addressable corpus fragment.
- feat: add runnable article-pipeline workflow (workflows/article-pipeline.js, invoked by name via the Workflow tool) — universal longform production: outline (schema-constrained) → parallel section writers → assemble with tail-artifact check → editor review → gate loop (capped fixes) → per-language translate/review/gates as barrier-free pipeline chains; hard content-only boundary (never code, only supplied gate commands run). Replaces the seven faion-article-* agent definitions — universal parts live in the script, faion.net specifics moved to faion-net-fe with the skill.
- chore: move faion-net-content skill out of the corpus to faion-net-fe/.claude/skills/ — product-specific editorial machinery does not belong in the product-neutral methodology repo.
- chore: sync tier-manifest with the landed corpus batch (3,093 entries: 15 new methodologies registered, two-pass tier geek → pro).
- chore: move the 46 BMAD v6.10.0 skill dirs out of `skills/` to `~/workspace/tools/bmad/` — they were untracked (installer-placed, never committed) but loaded ~1.8k tokens of descriptions into every session because `~/.claude` symlinks here. Re-running the BMAD installer with the `claude-code` target puts them back; check `git status skills/` after any BMAD install.
- chore: drop 2 stray agent-worktree artifacts tracked under .clone/.
- chore: mark 73 methodology validate-*.py scripts executable.
- fix: apply arXiv:2604.23178 (TMLR 2026) judge-bias findings — judge-calibration-protocol gains r7 (sub-floor κ = pairwise triage only, never a gate; best debiased config measured κ=0.549), llm-judge-rubric-evidence-first gains r6 (style bias 0.10-0.76 dominates, up to 19x position bias) plus per-family verbosity signs.
- fix: correct ai-agents/two-pass-reason-then-extract causal rationale (1.1.0 → 1.2.0, geek → pro) — the accuracy loss sits in the format INSTRUCTION in the prompt, not the decoder's grammar mask (arXiv:2604.03616, 2026-04-04); adds two antipatterns and the required-field-omission clarification. content_id 3a4830f4d2828248 → c0abba28b1cfdd21.
- feat: add product/working-backwards-prfaq methodology (solo) — Produces a PRFAQ Record — a one-page past-tense launch press release plus separate customer and internal FAQ banks — run as five phases that end in a proceed/revise/kill judgement, never a score, before any spec is written. The concept_type switch re-points the success measure and the internal FAQ's antagonist so one instrument serves commercial, internal, open-source, nonprofit, service, creative and physical concepts.
- feat: add automation-tooling/unattended-automation-boundary methodology (solo) — Produces an Unattended Automation Record deciding whether an automation runtime is warranted at all — usually it is not — and, when it is, the cheapest surface that can express the trigger: agent hooks, then the OS scheduler, then a self-hosted workflow runtime. Carries the dated per-tool exec-capability table that eliminates most visual tools outright when a local binary must run.
- feat: add ai-core/closed-set-output-validation methodology (solo) — groundedness as set membership (grounding_rate = |E n C| / |E|) when the output space is enumerable; count-don't-log rule, mixed-output scoping, MiniCheck CC BY-NC licence bar.
- feat: add ai-core/retrieval-cost-per-answer-audit methodology (solo) — Produces a Retrieval Cost Ledger over ten real queries — index tokens, candidate tokens, delivered-body tokens, correctness — yielding median tokens per lookup and the overhead ratio that decides whether to compress, restructure or leave the retrieval structure alone.
- feat: add ai-agents/context-graph-engineering methodology (pro) — Produces a Graph Design Record that first proves a graph is warranted at all (M:N, cross-links, cycles or temporal validity), then constrains edge construction, traversal budget and integrity checks — so the graph never costs more than the retrieval it replaces.
- feat: add ai-agents/hierarchical-index-compression methodology (pro) — Produces an Index Budget Record bounding a tiered retrieval hierarchy: a per-level read ceiling, fan-out that provably reaches the corpus, entries capped to a discriminator rather than a restated summary, and a numeric shard trigger.
- feat: add ai-agents/on-disk-checkpoint-ledger methodology (solo) — Produces a Checkpoint Ledger Spec giving a bash/cron agent orchestrator durable resume, per-unit append-only history and truncate-and-requeue rollback — state directory, marker files and flock, no framework and no database.
- feat: add ai-agents/schema-semantic-constraint-gap methodology (pro) — constrained decoding guarantees shape only; wire schema vs validation schema split, checker + counter per dropped keyword, per-transport drop sets, and the citations x structured-outputs 400 fork.
- feat: add sdlc-ai/gate-fail-closed-rule methodology (free) — Produces a Gate Failure Contract enforcing one rule — a gate that cannot evaluate must not report pass — by naming the five non-evaluating modes (parse, refusal, truncation, transport, empty), emitting a synthetic blocking finding instead of raising, and proving it with fault injection.
- feat: add sdlc-ai/context-file-cost-budget methodology (solo) — Produces a Context Budget Record over an existing AGENTS.md/CLAUDE.md: every line classified instruction/overview/preference, a line ceiling enforced, overviews relocated or cut, and a five-run median cost measurement before any improvement is claimed. Encodes the measured finding that human-written context files buy ~4pp task success for ~19% more inference spend while LLM-generated ones measurably hurt.
- feat: add sdlc-ai/mcp-vs-cli-decision-rule methodology (solo) — Produces a Source Routing Record routing each live source an agent needs to CLI, MCP or neither. Default is CLI: a binary the agent shells out to has no standing cost, while MCP tool definitions are re-sent on every request before any work. MCP is reserved for a closed list of things a one-shot command cannot do, under a declared server cap, first-party OAuth only, with the 2026-07-28 stateless revision and its Sampling/Roots/Logging deprecations pinned.
- feat: add sdlc-ai/verification-rung-placement-rule methodology (solo) — Produces a Rung Placement Record routing every check to the cheapest instrument that can detect its defect — rung 1 static lint at zero tokens, rung 2 mechanically-scored trigger evals, rung 3 a budgeted pairwise judge, rung H a person reading — and rejects any placement that cannot justify itself against the rung below.
- feat: add sdd/constitution-md methodology (free) — Produces constitution.md — at most 20 standing rules that pass the durable/cross-cutting/contestable/checkable test, each with a one-sentence why written before the rule, stable R-NN ids, a compliance statement and a semver footer — small enough to load into every phase, and explicitly delegating domain facts to project-spec/ instead of absorbing them.
- feat: add sdd/ears-requirements methodology (free) — Constrains the statement sentence of every requirement to one of the five EARS patterns (Mavin, RE'09) with a derived clause order Where < While < When < If/Then, ships the grammar as machine-readable data plus fixtures, and routes everything that is not a system response to a condition somewhere else instead of dressing it in 'shall'.
- feat: add sdd/spec-delta-format methodology (solo) — Defines the one-file spec delta: a baseline named by reference and git ref, four operation verbs (RENAMED, REMOVED, CHANGED, ADDED) applied in exactly that order, a mandatory scenario-loss check on every removal and change, a bounded Out of Scope section, and archiving only after the merged project-spec/ verifies.
- docs: land SDD state — feature-049-spec-deltas-bdd-cli (in-progress) and the ai-sdlc-landscape-2026 research set.
- feat: add .codex-plugin manifest for the Codex packaging of faion.
- feat: add quota-gate skill — GO/HOLD/UNKNOWN rate-limit gate with a source-freshness guard.
- feat: add faion-net-content skill — editorial pipeline for the faion.net content surface (audience-first, subagent-driven, multilingual).
- chore: add scripts AGENTS/CLAUDE docs and build-methodology-index-c.py.
- feat: add hooks AGENTS/CLAUDE docs and track-wakeup.sh hook.
- feat: add 7 article-pipeline agent definitions (outliner, writer, reviewer-en, translation-reviewer, translator, glossary-extractor, qg-fixer).
- docs: slim root AGENTS.md to the 20-80 line budget; deep reference moves to .agents/ (INDEX, adapters, docs-convention, linting).
- feat: wire project-spec into sdd workflows — sdd-batch-orchestrator v2.3.0 (PLAN declares expected `project-spec/` impact or `no spec impact`, EXECUTE lands the delta in the same commit set, REVIEW treats spec/code mismatch as a blocker, the coordinator mechanically checks every merged feature touched `project-spec/` or declared no-impact in `readiness.md`, DELIVER gated by a batch-level rebuild test) and idea-to-prod v1.2.0 (Phase 3 bootstraps `.aidocs/project-spec/` from prfaq + brainstorm + decisions before per-feature planning; feature specs become deltas against it).
- feat: sdd-batch-orchestrator v2.2.0 - three-role split. The orchestrator is the main thread and gets its own contract (`templates/orchestrator-approach.md`) - it is the one role with no dispatchable prompt file. The coordinator is a new independent subagent gating every wave boundary with CLEAR/HOLD/ABORT: it checks that the merge landed, that the merge point is green (first run of the verify matrix over the combination), that the next wave's file-overlap admission still holds against the mutated tree, and that no feature leaked outside its declared surface - and it may never fix, merge or re-dispatch. Executors are unchanged. Phase count stays at twelve per the 2026-05-02 decision; prompts 13-14 front the coordinator and the ledger auditor because prompt files are capabilities, not phases.
- feat: sdd-batch-orchestrator reflection - append-only action ledger at `.aidocs/<project>/memory/action-ledger.md`, written by the coordinator at wave boundaries and at batch close, audited by `prompts/14-ledger-auditor.md` before the next batch's INTAKE. Entries require cited evidence (sha, path, or failing command) and qualify only on recurrence, a spent fix-loop iteration, or a coordinator catch - the last class meaning the phase that should have caught it is under-specified, so its remediation is a diff to a versioned prompt file. The auditor may write only `status` plus an appended `resolved:` citation. Both halves ship together: writing without auditing is the diary failure the empty `memory/` folders already record.
- fix: idea-to-prod taught a retired SDD document set (the spec/design/test-plan/implementation-plan quartet) - Phase 3 now writes spec.md + plan.md (## Design + ## Execution Plan) + conditional user-flows.md / ui-ux-design.md + TASK_*.md + readiness.md, and names the retired files as rejectable output. Same fix in sdd-batch-orchestrator 04-parallelism, 07-verify-review-fix-loop and templates/prompt-skeleton.md.
- fix: idea-to-prod no longer mandates an LLM-generated AGENTS.md in every directory it creates - the CLAUDE.md one-liner stays mandatory, AGENTS.md becomes a capped human-confirmed stub, never auto-generated prose (Gloaguen et al., arXiv Feb 2026: generated context files measured net-negative).
- feat: idea-to-prod v1.1.0 - Phase 2.5 concept gate (PRFAQ verdict proceed|revise|kill; kill is a successful stop), constitution.md + prfaq.md in the .product/ layout, cheapest-instrument-first Phase 6 validation with a rung-3 cap, index-reads-are-dispatch-costs rule, dispatch marker written before dispatch, consistent-but-wrong failure mode, desk-research verification rule.
- feat: sdd-batch-orchestrator v2.1.0 - EXECUTE entry gate on unresolved clarification markers, blockers must cite spec.md or a constitution rule id, one-shot convergence re-derivation after the first REVIEW PASS, freeform-body + validated-last-line output contract, foreign artifact name map.
- feat: poll-agents v2.1.0 - ACTIVE.txt mandatory and written before dispatch, closed-set check on done= slugs, stale in-flight sweep to dead-letter, uncached-dispatch fan-out sizing rule.
- feat: improver v2.2.0 - run existing validators before dispatching investigation subagents, ERR entries record rung: and check:, rung-inflation anti-patterns (heuristics flag, exact rules block).
- feat: brainstorm v2.1.0 - four-field shape emitted as a terminal pass, externally-grounded personas carry per-claim source + confidence, orchestrator range-checks the consensus count.
- feat: media-ops v2.1.0 - visual-automation platforms (n8n, Make, Dify, Flowise) rejected as schedulers or publishers; media-manager remains the only unattended trigger surface.
- feat: project-spec-structure v1.1.0 — canonical location fixed at `.aidocs/project-spec/` (repo root, committed; ONE spec per product for multi-repo), current-revision-only rule (no `old/` copies, no in-tree changelog — history lives in git + `features/done/`), `constitution.md` declares deviations only, agent-home canonical storage named an antipattern. Same fix in `.agents/sdd-lifecycle.md`.
- chore: sdd registration catch-up — register 7 shipped-but-unlisted sdd methodologies in tier-manifest (cr-bug-tracking, plan-md-structure, project-spec-structure, quality-gates, readiness-checklist, ui-ux-design-template, user-flows-template) and the same plus `templates` in sdd/INDEX.xml (count 90→98); sync stale manifest versions for sdd-workflow-overview and sdd-promotion-gate-checklist; commit previously-untracked `.agents/sdd-lifecycle.md`. Entries for still-uncommitted methodology dirs stay out until their dirs land.
- feat: add ai-agents/orchestrator-token-protocol methodology (free) — a fan-out pays for retrieval once: the orchestrator searches and passes hash-IDs, subagents hydrate via `get-content --sink`, every spawned process sets `FAION_SUBAGENT=1` (shared no-transcript cache bucket), and `faion tokens report` brackets the dispatch so the CLI's own cost is attributed. Anchored on the 2026-08-09 A/B run: 22 searches, 8,669,708 cache-write tokens, ~$55, against a reported −3.4% agent-visible saving.
- feat: add quality-gates methodology (stack-to-gate matrix for backend / frontend / user-facing / pure-data; two-layer enforcement readiness.md + CI; framework-neutral tool recommendations).
- feat: add user-flows-template methodology (per-feature user-flows.md; actor + preconditions + happy + negative paths per flow; pos+neg required; 1:1 mapping to Playwright specs).
- feat: add ui-ux-design-template methodology (Nielsen 5 + Norman 2 per-feature audit; required for UI work, skipped for backend; ui-ux-design.md.tmpl).
- docs: drop test-plan.md references from SDD methodologies (replace with user-flows.md / plan.md across design-docs-patterns, sdd-batch-orchestrator phases 02/07/10, 01-overview).
- docs: update sdd-for-solos playbook to new lifecycle (merge Step 4+5 into single plan.md step, drop test-plan, add conditional user-flows.md / ui-ux-design.md, add Step 6 readiness, add CR/BUG section); bump to v2.0.0.
- docs: update sdd-promotion-gate-checklist to gate both backlog→todo and in-progress→done (new 07-done-gate.xml delegates to readiness-checklist); bump to v1.2.0.
- docs: update sdd-workflow-overview to new lifecycle (spec → plan → tasks → readiness → done; CR/BUG side-streams; project-spec/ as central artefact); bump to v1.1.0.
- docs: update top-level AGENTS.md SDD doc types (drop test-plan.md, merge design+implementation-plan into plan.md, add project-spec/ + user-flows.md + ui-ux-design.md + readiness.md + CR/BUG side streams).
- feat: add plan-md-structure methodology (merge design.md + implementation-plan.md into one plan.md with two H2 sections; skip rule for trivial features; F021/F022/F002 drift rationale).
- feat: add cr-bug-tracking methodology (CR and BUG side-streams; global per-repo numbering with separate counters; commit prefixes cr(CR0NN)/fix(BUG0NN); BUG-driven business-rules.md updates).
- feat: add readiness-checklist methodology (10-item readiness.md gating in-progress → done; conditional quality gates; surface-coupling review).
- feat: add project-spec-structure methodology (folder shape, rebuild test as acceptance gate, per-feature delta update, location declared in constitution.md).
- F-068 T05: clean 4 dead `knowledge_paths` entries in tier-manifest.json `tiers` block (python-developer/javascript-developer roles, post-T01 remap).
- F-068 T01: remap 19 role-as-domain methodologies (python-developer/javascript-developer → dev/frontend/backend).
- F-068 T02: resolve sdd/templates-planning decision-tree stub (downgraded to draft).
- F-068 T03: remove F-067 transitional frontmatter fallback (7 files).
- F-067: corpus restructure to domain-first layout (2625 methodologies + 444 playbooks).
- F-067: migration tooling (`scripts/migrate-f067.py`, `scripts/regen-tier-manifest.py`, `scripts/regen-domains-xml.py`, `scripts/slug-rename-map.json`), runtime `meta.json` schema (`skills/meta-schema.json`), validator + retriever updates with meta.json + frontmatter fallback.
- F-066 Phase D: tier-manifest re-sync to v7 — 2625 entries regenerated from current AGENTS.md frontmatter.
- F-066 Phase C: corpus validator repair (B1 envelope, decision-tree depth, template headers, scripts) — 436 files normalized to v3 spec.
- F-066 refactor: harvest +135 files (batch 0).
- F-066 refactor: harvest +55 files (batch 5).
- F-066 refactor: harvest +165 files (batch 4).
- F-066 refactor: harvest +192 files (batch 3).
- F-066 refactor: harvest +173 files (batch 2).
- F-066 refactor: harvest +156 files (batch 1).
- F-066 refactor: harvest +171 files (batch 0).
- F-066 refactor: harvest +28 files (batch 5).
- F-066 refactor: harvest +158 files (batch 4).
- F-066 refactor: harvest +192 files (batch 3).
- F-066 refactor: harvest +168 files (batch 2).
- F-066 refactor: harvest +157 files (batch 1).
- F-066 refactor: harvest +149 files (batch 0).
- F-066 refactor: harvest +132 files (batch 4).
- F-066 refactor: harvest +172 files (batch 3).
- F-066 refactor: harvest +167 files (batch 2).
- F-066 refactor: harvest +156 files (batch 1).
- F-066 refactor: harvest +150 files (batch 0).
- F-066 refactor: harvest +86 files (batch 4).
- F-066 refactor: harvest +160 files (batch 3).
- F-066 refactor: harvest +186 files (batch 2).
- F-066 refactor: harvest +182 files (batch 1).
- F-066 refactor: harvest +159 files (batch 0).
- F-066 refactor: harvest +66 files (batch 4).
- F-066 refactor: harvest +159 files (batch 3).
- F-066 refactor: harvest +165 files (batch 2).
- F-066 refactor: harvest +161 files (batch 1).
- F-066 refactor: harvest +145 files (batch 0).
- F-066 refactor: harvest +136 files (batch 3).
- F-066 refactor: harvest +115 files (batch 2).
- F-066 refactor: harvest +145 files (batch 1).
- F-066 refactor: harvest +138 files (batch 0).
- F-066 refactor: harvest +81 files (batch 1).
- F-066 refactor: harvest +68 files (batch 0).
- F-066 refactor: harvest +7 files (batch 0).
- F-066 refactor: harvest +140 files (batch 6).
- F-066 refactor: harvest +137 files (batch 5).
- F-066 refactor: harvest +180 files (batch 4).
- F-066 refactor: harvest +212 files (batch 3).
- F-066 refactor: harvest +188 files (batch 2).
- F-066 refactor: harvest +179 files (batch 1).
- F-066 refactor: harvest +158 files (batch 0).
- F-066 refactor: harvest +138 files (batch 5).
- F-066 refactor: harvest +174 files (batch 4).
- F-066 refactor: harvest +169 files (batch 3).
- F-066 refactor: harvest +157 files (batch 2).
- F-066 refactor: harvest +244 files (batch 1).
- F-066 refactor: harvest +184 files (batch 0).
- F-066 refactor: harvest +161 files (batch 6).
- F-066 refactor: harvest +190 files (batch 5).
- F-066 refactor: harvest +163 files (batch 4).
- F-066 refactor: harvest +150 files (batch 3).
- F-066 refactor: harvest +128 files (batch 2).
- F-066 refactor: harvest +137 files (batch 1).
- F-066 refactor: harvest +251 files (batch 0).
- F-066 refactor: harvest +22 files (batch 7).
- F-066 refactor: harvest +165 files (batch 6).
- F-066 refactor: harvest +164 files (batch 5).
- F-066 refactor: harvest +159 files (batch 4).
- F-066 refactor: harvest +155 files (batch 3).
- F-066 refactor: harvest +148 files (batch 2).
- F-066 refactor: harvest +140 files (batch 1).
- F-066 refactor: harvest +140 files (batch 0).
- F-066 refactor: harvest +76 files (batch 6).
- F-066 refactor: harvest +169 files (batch 5).
- F-066 refactor: harvest +163 files (batch 4).
- F-066 refactor: harvest +186 files (batch 3).
- F-066 refactor: harvest +175 files (batch 2).
- F-066 refactor: harvest +174 files (batch 1).
- F-066 refactor: harvest +152 files (batch 0).
- F-066 refactor: harvest +89 files (batch 6).
- F-066 refactor: harvest +215 files (batch 5).
- F-066 refactor: harvest +177 files (batch 4).
- F-066 refactor: harvest +162 files (batch 3).
- F-066 refactor: harvest +152 files (batch 2).
- F-066 refactor: harvest +137 files (batch 1).
- F-066 refactor: harvest +156 files (batch 0).
- F-066 refactor: harvest +84 files (batch 6).
- F-066 refactor: harvest +170 files (batch 5).
- F-066 refactor: harvest +160 files (batch 4).
- F-066 refactor: harvest +168 files (batch 3).
- F-066 refactor: harvest +152 files (batch 2).
- F-066 refactor: harvest +154 files (batch 1).
- F-066 refactor: harvest +201 files (batch 0).
- F-066 refactor: harvest +177 files (batch 5).
- F-066 refactor: harvest +163 files (batch 4).
- F-066 refactor: harvest +180 files (batch 3).
- F-066 refactor: harvest +165 files (batch 2).
- F-066 refactor: harvest +263 files (batch 1).
- F-066 refactor: harvest +160 files (batch 0).
- F-066 refactor: harvest +122 files (batch 6).
- F-066 refactor: harvest +159 files (batch 5).
- F-066 refactor: harvest +163 files (batch 4).
- F-066 refactor: harvest +160 files (batch 3).
- F-066 refactor: harvest +155 files (batch 2).
- F-066 refactor: harvest +150 files (batch 1).
- F-066 refactor: harvest +152 files (batch 0).
- F-066 refactor: harvest +150 files (batch 6).
- F-066 refactor: harvest +166 files (batch 5).
- F-066 refactor: harvest +124 files (batch 4).
- F-066 refactor: harvest +153 files (batch 3).
- F-066 refactor: harvest +151 files (batch 2).
- F-066 refactor: harvest +157 files (batch 1).
- F-066 refactor: harvest +189 files (batch 0).
- F-066 refactor: harvest +127 files (batch 4).
- F-066 refactor: harvest +101 files (batch 3).
- F-066 refactor: harvest +152 files (batch 2).
- F-066 refactor: harvest +151 files (batch 1).
- F-066 refactor: harvest +152 files (batch 0).
- F-066 refactor: harvest +98 files (batch 6).
- F-066 refactor: harvest +167 files (batch 5).
- F-066 refactor: harvest +145 files (batch 4).
- F-066 refactor: harvest +126 files (batch 3).
- F-066 refactor: harvest +186 files (batch 2).
- F-066 refactor: harvest +176 files (batch 1).
- F-066 refactor: harvest +158 files (batch 0).
- F-066 refactor: harvest +78 files (batch 6).
- F-066 refactor: harvest +177 files (batch 5).
- F-066 refactor: harvest +114 files (batch 4).
- F-066 refactor: harvest +145 files (batch 3).
- F-066 refactor: harvest +167 files (batch 2).
- F-066 refactor: harvest +132 files (batch 1).
- F-066 refactor: harvest +109 files (batch 0).
- F-066 refactor: harvest +107 files (batch 5).
- F-066 refactor: harvest +213 files (batch 4).
- F-066 refactor: harvest +217 files (batch 3).
- F-066 refactor: harvest +160 files (batch 2).
- F-066 refactor: harvest +153 files (batch 1).
- F-066 refactor: harvest +163 files (batch 0).
- F-066 refactor: harvest +22 files (batch 6).
- F-066 refactor: harvest +175 files (batch 5).
- F-066 refactor: harvest +205 files (batch 4).
- F-066 refactor: harvest +170 files (batch 3).
- F-066 refactor: harvest +160 files (batch 2).
- F-066 refactor: harvest +166 files (batch 1).
- F-066 refactor: harvest +167 files (batch 0).
- F-066 refactor: harvest +68 files (batch 5).
- F-066 refactor: harvest +199 files (batch 4).
- F-066 refactor: harvest +228 files (batch 3).
- F-066 refactor: harvest +167 files (batch 2).
- F-066 refactor: harvest +163 files (batch 1).
- F-066 refactor: harvest +84 files (batch 0).
- F-066 refactor: harvest +10 files (batch 1).
- F-066 refactor: harvest +189 files (batch 0).
- F-066 refactor: safe-harvest +627 files (skipping active chunk-00).
- F-066 refactor: safe-harvest +275 files (skipping active chunk-00).
- F-066 refactor: harvest +59 files (batch 1).
- F-066 refactor: harvest +177 files (batch 0).
- F-066 refactor: harvest +35 files (batch 4).
- F-066 refactor: harvest +159 files (batch 3).
- F-066 refactor: harvest +175 files (batch 2).
- F-066 refactor: harvest +223 files (batch 1).
- F-066 refactor: harvest +264 files (batch 0).
- F-066 refactor: harvest +13 files (batch 0).
- F-066 refactor: harvest +8 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +42 files (batch 1).
- F-066 refactor: harvest +86 files (batch 0).
- F-066 refactor: harvest +9 files (batch 0).
- F-066 refactor: harvest +8 files (batch 0).
- F-066 refactor: harvest +8 files (batch 0).
- F-066 refactor: harvest +18 files (batch 0).
- F-066 refactor: harvest +10 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +25 files (batch 0).
- F-066 refactor: harvest +7 files (batch 0).
- F-066 refactor: harvest +60 files (batch 1).
- F-066 refactor: harvest +174 files (batch 0).
- F-066 refactor: harvest +8 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +9 files (batch 0).
- F-066 refactor: harvest +7 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +7 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +8 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +8 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +17 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +93 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +43 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +154 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +71 files (batch 1).
- F-066 refactor: harvest +221 files (batch 0).
- F-066 refactor: harvest +25 files (batch 0).
- F-066 refactor: harvest +24 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +129 files (batch 1).
- F-066 refactor: harvest +146 files (batch 0).
- F-066 refactor: harvest +143 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +83 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +52 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 wave-4 stragglers harvest.
- F-066 wave-4 stragglers harvest.
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +155 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +13 files (batch 0).
- F-066 refactor: harvest +43 files (batch 0).
- F-066 refactor: harvest +185 files (batch 0).
- F-066 wave-4 chunk-07 v1.bak sidecars from refactor.
- F-066 refactor: harvest +1 files (batch 0).
- F-066 refactor: harvest +13 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +17 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +23 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +20 files (batch 1).
- F-066 refactor: harvest +23 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +11 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +7 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +1 files (batch 2).
- F-066 refactor: harvest +165 files (batch 1).
- F-066 refactor: harvest +56 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +6 files (batch 0).
- F-066 refactor: harvest +7 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +4 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +3 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 refactor: harvest +22 files (batch 0).
- F-066 refactor: harvest +13 files (batch 0).
- F-066 refactor: harvest +19 files (batch 0).
- F-066 refactor: harvest +5 files (batch 0).
- F-066 refactor: harvest +7 files (batch 0).
- F-066 refactor: harvest +12 files (batch 0).
- F-066 refactor: harvest +13 files (batch 0).
- F-066 refactor: harvest +38 files (batch 0).
- F-066 refactor: harvest +16 files (batch 0).
- F-066 refactor: harvest +19 files (batch 0).
- F-066 refactor: harvest +1 files (batch 0).
- F-066 phase C autofixer: fix-methodology-phase-d.py applied to all active dirs (xml escape, content_id, stub rules, template headers).
- F-066 refactor: harvest +41 files (batch 0).
- F-066 refactor: harvest +14 files (batch 0).
- F-066 refactor: harvest +16 files (batch 0).
- F-066 refactor: harvest +18 files (batch 0).
- F-066 phase D: update faion/CLAUDE.md for v5.0 (20 canonical domains, 11 goal categories, 2-level retrieval).
- F-066 refactor: harvest +19 files (batch 0).
- F-066 refactor: harvest +11 files (batch 0).
- F-066 phase D: update faion SKILL.md description + routing for v3 layout + 2-level retrieval.
- F-066 refactor: harvest +17 files (batch 0).
- F-066 refactor: harvest +46 files (batch 0).
- F-066 refactor: harvest +12 files (batch 0).
- F-066 refactor: harvest +17 files (batch 0).
- F-066 phase D: validate-domain-index.py + f066-validate-all.sh (corpus-wide runner).
- F-066 refactor: harvest +2 files (batch 0).
- F-066 phase D: extend validate-methodology-v2.py with B1 keys (complexity, produces, est_tokens, tags) for status=active.
- F-066 refactor: harvest +18 files (batch 0).
- F-066 refactor: harvest +70 files (batch 0).
- F-066 phase D: relax decision-tree validator (accept sibling-branch shape).
- F-066 phase D scaffold: validate-methodology-decision-tree.py + validate-methodology-templates.py + validate-methodology-scripts.py.
- F-066 phase A: enrich domains.xml with decision-tree + disambiguation + typical-asks (v1.1).
- F-066 refactor: harvest +296 files (batch 5).
- F-066 refactor: harvest +279 files (batch 4).
- F-066 refactor: harvest +185 files (batch 3).
- F-066 refactor: harvest +236 files (batch 2).
- F-066 refactor: harvest +259 files (batch 1).
- F-066 refactor: harvest +287 files (batch 0).
- F-065 phase 6: retriever reads L1 (domains.xml + taxonomy.xml) before L2 INDEX.xml before leaf files. Saves ~80% retrieval context.
- F-065 phase 5: L2 goal indexes (11 categories, 455 playbooks).
- F-065 phase 5: canonical playbook taxonomy + validator.
- F-065 phase 2: assemble L1 domains.xml (20 domains) + validator.
- F-065 phase 2: L2 INDEX.xml for ml-engineering/backend/frontend/ba (606 methodologies).
- F-065 phase 2: L2 INDEX.xml for comms/hr/claude-code/security (51 methodologies).
- F-065 phase 2: L2 INDEX.xml for dev/pm/infra/marketing (1267 methodologies).
- F-065 phase 4: playbook goal classification chunk 1 (91 dirs).
- F-065 phase 4: playbook goal classification chunk 2 (91 dirs).
- F-065 phase 4: playbook goal classification chunk 3 (91 dirs).
- F-065 phase 4: playbook goal classification chunk 4 (91 dirs).
- F-065 phase 4: playbook goal classification chunk 5 (91 dirs + 47 gap-fill).
- F-065 phase 2: L2 INDEX.xml for sdd/ai-agents/ux/sdlc-ai (400 methodologies).
- F-065 phase 2: L2 INDEX.xml for research/ai-core/product/architecture (303 methodologies).
- F-065 phase 3: playbook YAML→XML batch 5 (55 dirs).
- F-065 phase 3: playbook YAML→XML batch 4 (100 dirs).
- F-065 phase 3: playbook YAML→XML batch 3 (100 dirs).
- F-065 phase 3: playbook YAML→XML batch 2 (100 dirs).
- F-065 phase 3: playbook YAML→XML batch 1 (100 dirs).
- F-065 phase 1: domain merge batch 18 (7 files).
- F-065 phase 1: domain merge batch 17 (100 files).
- F-065 phase 1: domain merge batch 16 (100 files).
- F-065 phase 1: domain merge batch 15 (100 files).
- F-065 phase 1: domain merge batch 14 (100 files).
- F-065 phase 1: domain merge batch 13 (100 files).
- F-065 phase 1: domain merge batch 12 (100 files).
- F-065 phase 1: domain merge batch 11 (100 files).
- F-065 phase 1: domain merge batch 10 (100 files).
- F-065 phase 1: domain merge batch 9 (100 files).
- F-065 phase 1: domain merge batch 8 (100 files).
- F-065 phase 1: domain merge batch 7 (100 files).
- F-065 phase 1: domain merge batch 6 (100 files).
- F-065 phase 1: domain merge batch 5 (100 files).
- F-065 phase 1: domain merge batch 4 (100 files).
- F-065 phase 1: domain merge batch 3 (100 files).
- F-065 phase 1: domain merge batch 2 (100 files).
- F-065 phase 1: domain merge batch 1 (100 files).
- tier-manifest sync: include all v2 methodologies + gap entries.
- F-064 final wave: playbook batch 6 (+20 files).
- F-064 final wave: playbook batch 5 (+100 files).
- F-064 final wave: playbook batch 4 (+100 files).
- F-064 final wave: playbook batch 3 (+100 files).
- F-064 final wave: playbook batch 2 (+100 files).
- F-064 final wave: playbook batch 1 (+100 files).
- F-064 final wave: playbook batch 0 (+100 files).
- F-063 final wave: harvest batch 2 (+28 files).
- F-063 final wave: harvest batch 1 (+100 files).
- F-063 final wave: harvest batch 0 (+100 files).
- F-063+F-064 harvest +312.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +2.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +2.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +49.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +2.
- F-063+F-064 harvest +41.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +2.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +40.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +1.
- F-063+F-064 harvest +2.
- F-063+F-064 harvest +44.
- F-063+F-064 harvest +36.
- F-063+F-064 harvest +40.
- F-063+F-064 harvest +8.
- F-063 harvest +395.
- F-063 harvest +316.
- F-063 harvest +2.
- F-063 harvest +2.
- F-063 harvest +320.
- F-063 harvest +1.
- F-063 harvest +1.
- F-063 harvest +2.
- F-063 harvest +2.
- F-063 harvest +2.
- F-063 harvest +2.
- F-063 harvest +1.
- F-063 harvest +3.
- F-063 harvest +1.
- F-063 harvest +1.
- F-063 harvest +2.
- F-063 harvest +4.
- F-063 harvest +4.
- F-063 harvest +3.
- F-063 harvest +1.
- F-063 harvest +3.
- F-063 harvest +3.
- F-063 harvest +5.
- F-063 harvest +4.
- F-063 harvest +6.
- F-063 harvest +4.
- F-063 harvest +1.
- F-063 harvest +5.
- F-063 harvest +5.
- F-063 harvest +2.
- F-063 harvest +7.
- F-063 harvest +5.
- F-063 harvest +8.
- F-063 harvest +322.
- F-063 harvest +8.
- F-063 harvest +5.
- F-063 harvest +6.
- F-063 harvest +5.
- F-063 harvest +7.
- F-063 harvest +4.
- F-063 harvest +7.
- F-063 harvest +6.
- F-063 harvest +8.
- F-063 harvest +6.
- F-063 harvest +8.
- F-063 harvest +3.
- F-063 harvest +8.
- F-063 harvest +9.
- F-063 harvest +5.
- F-063 harvest +30.
- F-063 harvest +299.
- F-063 harvest +330.
- F-063 harvest +0.
- F-063 harvest +5.
- F-063 harvest +15.
- F-063 Added: chunk-01 P2 harvest (79 entries).
- F-063 harvest +11.
- F-063 harvest +5.
- F-063 harvest +5.
- F-063 harvest +5.
- F-063 harvest +9.
- F-063 harvest +322.
- F-063 harvest +14.
- F-063 Added: chunk-00 P2 harvest (79 entries).
- F-063 harvest +8.
- F-063 harvest +5.
- F-063 harvest +4.
- F-063 harvest +7.
- F-063 harvest +321.
- F-063 harvest +5.
- F-063 harvest +7.
- F-063 harvest +7.
- F-063 harvest +11.
- F-063 harvest +5.
- F-063 harvest +8.
- F-063 Added: harvest +6 writer dirs.
- F-063 Added: harvest +6 writer dirs.
- F-063 Added: harvest +8 writer dirs.
- F-063 Added: harvest +4 writer dirs.
- F-063 Added: harvest +12 writer dirs.
- F-063 Added: 27 incremental writer-output dirs (mid-flight harvest).
- F-063 Added: 52+ P1 gap methodologies from Wave 3 writers (uncommitted batch harvest).
- F-062 Added: bulk migration of all 1638 v1 methodology.xml → v2 multi-file dirs (94% in initial sweep + 98 force-fix for skill-level conflicts + 5 XML id repairs).
- F-063 Added: P0 gap methodologies (5): agency-case-study-template, ai-code-review-checklist, ai-generated-layout-review-checklist, async-standup-template, debt-scoring-rubric.
- F-059 Changed: validate-methodology-v2.py accepts any 01-*.xml as core (not just 01-core-rules.xml).
- F-059 Added: methodology template v2 (multi-file dir AGENTS.md + content/*.xml).
- F-059 Added: scripts/validate-methodology-v2.py + scripts/migrate-methodology-to-v2.py.
- F-059 Added: canonical exemplar at solo/research/researcher/jobs-to-be-done/ (JTBD).
- F-060 Added: playbook template v2 (playbook.yaml manifest + body.md).
- F-060 Added: scripts/validate-playbook-v2.py + scripts/migrate-playbook-to-v2.py.
- F-060 Added: canonical exemplar at solo/product-planning/idea-to-validated-mvp/.
- F-061 Added: workflow template v2 schema (envelope ≤80 lines + content_id + success_criteria).
- F-061 Added: scripts/validate-workflow-v2.py.
- F-061 Changed: 6 workflows normalized (brainstorm, idea-to-prod, improver, media-ops, poll-agents, sdd-batch-orchestrator).
- sdd-batch-orchestrator: add Pre-flight branch check section to 04-parallelism.xml (F-056; rule landed after F-050 T09 detached-HEAD incident).
- chore(skills): feature-044 closeout — bump tier-manifest to v6, refresh `geek/ai/ai-agents/CLAUDE.md` count (26 → 84, with 53-new + 31-legacy split documented), and extend `skills/CLAUDE.md` geek tree with `sdlc-ai (52)`. tier-manifest.json's geek `knowledge_paths` already lists `faion/knowledge/geek/sdlc-ai`; no schema change required (044-T06).
- feat(workflows): add idea-to-prod — autonomous one-prompt build workflow
- chore(skills): index 234 methodologies in 6 geek-tier index files (closes audit gap)
- chore(skills): index 330 methodologies in 12 pro-tier SKILL.md files (closes audit gap)
- chore(skills): index 139 methodologies in 7 free/solo SKILL.md files (closes audit gap)
- chore(skills): add SKILL.md + CLAUDE.md for 21 geek-tier KBs (closes audit gap)
- chore(skills): add SKILL.md + CLAUDE.md for 21 solo-tier KBs (closes audit gap)
- chore(skills): add SKILL.md + CLAUDE.md for 6 pro-tier KBs (code-quality, software-architect, software-developer, product-operations, product-planning, ui-designer)
- chore(skills): sync tier-manifest.json with filesystem (50 paths) — closes audit gap
- feat(scripts): add audit-index-coverage.py — verifies tier-manifest, workflow catalog, tier-AGENTS.md, per-KB SKILL.md, and structural floor. Five checks, JSON output, --strict exit codes for CI gating. Recognizes both KB shapes (router with SKILL.md, flat with AGENTS.md).
- feat: add Codex compatibility layer while preserving Claude Code packaging. Added `.codex-plugin/plugin.json`, top-level and workflow platform adapters for Claude Code vs Codex, and neutral workflow primitives for user-choice, subagent dispatch, quota state, memory, and worktree isolation. Updated Faion indexes and README so Claude reads Claude adapters and Codex reads Codex adapters; Claude-only frontmatter, hooks, and retrieval remain available for Claude Code.
- feat: `sdd-batch-orchestrator/decisions.xml` — closes the last workflow-spec gap. Seven architectural decisions: 12-phase shape (vs collapsed 9-phase), versioned prompt files (vs inline orchestrator improvisation), worktree-isolated parallel waves (vs shared working tree), `flock`-serialized merge into the default branch (vs optimistic concurrent merges), hard-capped REVIEW→FIX loop (vs unbounded retry), focused before/after visual delivery (vs PR description text), per-surface playbook adaptation (vs one-size-fits-all). `xmllint --noout` clean. catalog.json updated: `sdd-batch-orchestrator.has_decisions: true`.
- feat: workflow-spec compliance + catalog. Authored `content/*.xml` (semantic XML, closed-glossary tags) + `decisions.xml` for the 4 migrated workflows: brainstorm (5 content + decisions), improver (5 + decisions), media-ops (7 + decisions), poll-agents (5 + decisions). All XMLs `xmllint --noout` clean. Each AGENTS.md trimmed to ≤80 lines (51 / 51 / 64 / 49). Added `skills/faion/workflows/catalog.json` (v1) — machine-readable index mapping each workflow slug to status, version, summary, trigger keywords, phase ids, content file count, decisions presence, AGENTS.md line count, and workflow-specific notes (consent gate, hard rules, reference impls). 5 workflows total: brainstorm, improver, media-ops, poll-agents, sdd-batch-orchestrator. workflows/AGENTS.md updated to point routing decisions at catalog.json.
- refactor: collapse all applied skills under `faion` umbrella as workflows. Moved `brainstorm/`, `improver/`, `media-ops/`, `poll-agents/` into `skills/faion/workflows/<slug>/`. Top-level `skills/` now contains a single applied skill: `faion` (plus NERO-specific). Each migrated workflow has new workflow-spec front-matter (status, audience, owner, last_verified, version, applies_to) + required H2 sections (Summary, Why, When To Use, When NOT To Use). `brainstorm` got Phase 0 CONSENT GATE: if the orchestrator triggers brainstorm but the user did not explicitly request it, MUST ask via AskUserQuestion before launching agents. faion SKILL.md got rich auto-routing description listing all 7 trigger surfaces (knowledge, playbooks, brainstorm, SDD, improver, media-ops, poll-agents). Internal `/faion:<sub>` invocations replaced with bare `/faion` (umbrella routes by context). README + workflows/AGENTS.md + faion/CLAUDE.md indexes refreshed.
- chore: delete `feature-executor` and `sdd-execution` applied skills. `feature-executor` declared a non-existent multi-agent architecture (4 agents that were never built); `sdd-execution`'s 17 sub-methodologies duplicate `knowledge/solo/sdd/sdd/`. Single source of truth now: `knowledge/solo/sdd/` for theory + `workflows/sdd-batch-orchestrator/` for execution. References across 134 files redirected to `/faion`. tier-manifest v3 → v4 (single applied skill: `faion`).
- refactor: plugin rename to `faion` + drop `faion-` prefix from applied skills. Plugin manifest `name: faion-network` → `faion` (v1.1.0). Renamed skill folders: `faion-brainstorm` → `brainstorm`, `faion-feature-executor` → `feature-executor`, `faion-improver` → `improver`, `faion-sdd-execution` → `sdd-execution`, `faion-media-ops` → `media-ops`, `faion-poll-agents` → `poll-agents`. SKILL.md frontmatter `name:` fields updated; bulk reference rewrites across 199 files (skills/, agents/, hooks/, knowledge XML, docs, README). Invocation now `/faion:<skill>` (or unprefixed when no conflict). `media-ops` SKILL.md normalized (lowercase `skill.md` → `SKILL.md`, frontmatter added). Frozen `.aidocs/done/` and `.aidocs/feature-04*` left as-is for historical accuracy.
- chore: remove `hooks/auto-update.sh` — plugins use `/plugin update faion`, the bespoke fetch hook is obsolete. Removed from `hooks/hooks.json` and deleted the script.
- feat: package faion-network as Claude Code plugin — added `.claude-plugin/plugin.json` manifest (name: faion-network, v1.0.0), `hooks/hooks.json` wiring existing scripts to UserPromptSubmit + SessionStart events via `${CLAUDE_PLUGIN_ROOT}`, README plugin install section. Direct clone (`~/.claude` symlink) install path preserved.
- chore: feature-048 lifecycle in-progress → done
- feat: feature-048 COMPLETE — all 4 waves shipped (free 30 + solo 30 + pro 30 + geek 30 = 120 playbooks); 100% validator pass; cross-tier slug uniqueness enforced; all groups have AGENTS.md/CLAUDE.md; orphan worktree commits restored (3 geek + 5 pro + 4 solo + 1 free)
- feat: feature-048 wave 4 closeout — Geek tier complete (30/30); group AGENTS.md/CLAUDE.md added for mcp-protocol; orphan worktree commits restored for llm-as-judge-harness, when-to-fine-tune-vs-prompt, retrieval-evaluation-ragas
- add: tier-playbook geek/fine-tuning/lora-basics-dataset-prep
- add: tier-playbook geek/ai-product-positioning/trust-ux-citations
- add: tier-playbook geek/ai-consultancy-ops/ai-audit-checklist
- add: tier-playbook geek/ai-agents/agent-debugging-observability
- add: tier-playbook geek/cost-optimization/prompt-caching-strategy
- add: tier-playbook geek/multimodal/ocr-pipeline-vision-llm
- add: tier-playbook geek/mcp-protocol/mcp-claude-code-integration
- add: tier-playbook geek/evaluation/behavioral-evals-adversarial
- add: tier-playbook geek/claude-code-skills/claude-code-subagents-slash
- add: tier-playbook geek/rag-pipelines/rag-reranking
- add: tier-playbook geek/ai-consultancy-ops/ai-proposal-template
- add: tier-playbook geek/llm-integration/function-calling-tool-use
- add: tier-playbook geek/context-engineering/long-context-strategies
- add: tier-playbook geek/llm-integration/structured-output-json-schema
- add: tier-playbook geek/llm-integration/llm-fallback-chains
- add: tier-playbook geek/ai-agents/agent-memory-architecture
- add: tier-playbook geek/ai-safety/pii-redaction-pipeline
- add: tier-playbook geek/cost-optimization/model-routing-cheap-vs-strong
- add: tier-playbook geek/ml-ops/model-monitoring-drift
- add: tier-playbook geek/context-engineering/prompt-caching-anthropic
- add: tier-playbook geek/prompt-engineering/semantic-xml-prompts-anthropic
- add: tier-playbook geek/ai-agents/multi-agent-orchestration
- add: tier-playbook geek/claude-code-skills/claude-code-skill-authoring
- add: tier-playbook geek/mcp-protocol/mcp-server-build
- add: tier-playbook geek/rag-pipelines/rag-chunking-benchmark
- add: tier-playbook geek/ai-agents/react-loop-production
- add: tier-playbook geek/rag-pipelines/rag-hybrid-search-bm25-vector
- docs: feature-048 wave 4 dispatch rules
- feat: feature-048 wave 3 closeout — Pro tier complete (30/30 pass validator); group AGENTS.md/CLAUDE.md added for team-management, hr-ops, business-analysis; 5 orphan worktree commits restored (caching-strategy, scoping-workshop, hiring-funnel, terraform-iac, onboarding-30-60-90)
- add: tier-playbook pro/market-research/positioning-workshop
- add: tier-playbook pro/client-engagement/discovery-call-structure
- add: tier-playbook pro/devops-cicd/deploy-blue-green-canary
- add: tier-playbook pro/backend-systems/db-scaling-read-replicas
- add: tier-playbook pro/client-engagement/weekly-status-report
- add: tier-playbook pro/business-analysis/stakeholder-elicitation
- add: tier-playbook pro/market-research/competitor-analysis
- add: tier-playbook pro/ux-research/user-interviews-at-scale
- add: tier-playbook pro/delivery-ops/sprint-planning-agency
- add: tier-playbook pro/paid-acquisition/meta-ads-b2c
- add: tier-playbook pro/growth-marketing/aarrr-funnel
- add: tier-playbook pro/infra-engineering/aws-gcp-basics
- add: tier-playbook pro/client-engagement/statement-of-work
- add: tier-playbook pro/product-management/prd-template
- add: tier-playbook pro/paid-acquisition/ltv-cac-attribution
- add: tier-playbook pro/client-engagement/scope-creep-management
- add: tier-playbook pro/delivery-ops/capacity-planning
- add: tier-playbook pro/team-management/first-hire-developer
- add: tier-playbook pro/devops-cicd/production-cicd-pipeline
- add: tier-playbook pro/paid-acquisition/google-ads-first-campaign
- docs: feature-048 wave 3 dispatch rules
- add: tier-playbook solo/product-ops/solo-metrics-tracking
- add: tier-playbook solo/seo-essentials/on-page-seo
- add: tier-playbook solo/product-planning/weekly-review-solo
- add: tier-playbook solo/solo-ops-finance/runway-calc
- add: tier-playbook solo/automation/pre-commit-hooks
- add: tier-playbook solo/product-planning/weekly-review-solo
- add: tier-playbook solo/sdd-workflow/spec-to-code-pipeline
- add: tier-playbook solo/comms-stakeholder/client-email-templates
- add: tier-playbook solo/sdd-workflow/scope-cutting
- add: tier-playbook solo/product-ops/rice-ice-prioritization
- add: tier-playbook solo/ui-design/design-tokens-minimal
- add: tier-playbook solo/product-ops/backlog-hygiene
- add: tier-playbook solo/content-marketing/content-calendar
- add: tier-playbook solo/automation/env-management-secrets
- add: tier-playbook solo/launch-operations/churn-intervention
- add: tier-playbook solo/launch-operations/payment-flow
- add: tier-playbook solo/automation/github-actions-cicd
- add: tier-playbook solo/frontend-launch/landing-page-from-zero
- add: tier-playbook solo/seo-essentials/technical-seo-audit
- add: tier-playbook solo/api-design/api-key-auth
- add: tier-playbook solo/content-marketing/newsletter-setup
- add: tier-playbook solo/sdd-workflow/sdd-for-solos
- add: tier-playbook solo/launch-operations/pricing-experiments
- add: tier-playbook solo/sdd-workflow/writing-first-spec
- add: tier-playbook solo/server-craft/vps-first-deploy
- add: tier-playbook solo/launch-operations/customer-onboarding-email
- add: tier-playbook solo/product-planning/roadmap-for-one-person
- docs: feature-048 wave 2 dispatch rules
- feat: feature-048 wave 1 closeout — Free tier complete (30/30 playbooks pass validator); group AGENTS.md/CLAUDE.md added for tech-setup, dev-fundamentals, business-discovery, cost-free-stack; validator hardened (DS3 ignores H2 inside fenced code-blocks; DS10 placeholder regex no longer false-positives on "address bar" / "snack bar" / etc.); --self-test still 5/5 pass

- add: tier-playbook free/dev-fundamentals/code-style-and-prettier
- add: tier-playbook free/marketing-fundamentals/positioning-basics
- add: tier-playbook free/cost-free-stack/free-email-with-cloudflare
- add: tier-playbook free/dev-fundamentals/write-good-readme
- add: tier-playbook free/dev-fundamentals/testing-intro-python
- add: tier-playbook free/mvp-essentials/mvp-launch-checklist
- add: tier-playbook free/cost-free-stack/free-auth-supabase
- add: tier-playbook free/marketing-fundamentals/landing-page-essentials
- add: tier-playbook free/tech-setup/git-branching-basics
- add: tier-playbook free/business-discovery/is-this-a-real-problem
- add: tier-playbook free/business-discovery/niche-selection-framework
- add: tier-playbook free/dev-fundamentals/python-package-manager
- add: tier-playbook free/dev-fundamentals/dotenv-secrets-management
- add: tier-playbook free/hosting-infra/cloudflare-dns-free-ssl
- add: tier-playbook free/tech-setup/vscode-first-project-setup
- add: tier-playbook free/cost-free-stack/free-analytics-posthog
- add: tier-playbook free/marketing-fundamentals/first-10-customers
- add: tier-playbook free/hosting-infra/deploy-to-vercel-free
- add: tier-playbook free/mvp-essentials/ugly-first-version
- add: tier-playbook free/ops-basics/wise-account-for-solos
- add: tier-playbook free/business-discovery/idea-validation-landing-page
- add: tier-playbook free/mvp-essentials/mvp-scope-cutting
- add: tier-playbook free/dev-fundamentals/javascript-first-project
- add: tier-playbook free/hosting-infra/deploy-static-site-github-pages
- add: tier-playbook free/tech-setup/ssh-key-setup-github
- add: tier-playbook free/tech-setup/git-daily-workflow
- add: tier-playbook free/business-discovery/mom-test-customer-interview
- add: tier-playbook free/hosting-infra/buy-domain-namecheap-cloudflare
- add: tier-playbook free/dev-fundamentals/python-first-project
- add: tier-playbook free/tech-setup/github-account-and-first-repo
- docs: feature-048 wave 1 dispatch rules
- feat: feature-048 phases 1-3 — tier-playbook foundation: convention spec at `.aidocs/conventions/playbooks/` (CLAUDE.md, AGENTS.md ≤80 lines, full playbook-spec.md with 8 anti-patterns + inline template + 8-item authoring checklist) + cross-link from `.aidocs/conventions/workflows/AGENTS.md`; `skills/faion/SKILL.md` Playbooks section + `skills/faion/CLAUDE.md` playbooks tree + `skills/CLAUDE.md` index row; `skills/tier-manifest.json` extended with `playbook_root` + `playbook_paths` per tier (49 group paths); validator `scripts/validate-tier-playbook.py` with --self-test (5 cases pass: valid playbook, slug regex, missing front-matter, broken section order, foo/bar placeholder) covering DS1-DS10; scaffold `skills/faion/playbooks/{free,solo,pro,geek}/` with per-tier AGENTS.md (≤80 lines) listing groups from priority-120.md; author-prompt template at `.aidocs/conventions/playbooks/author-prompt.md` for orchestrator dispatch to faion-sdd-executor-agent. Phases 4-7 (120-playbook authoring waves) ready to dispatch.
- docs: add `.aidocs/in-progress/feature-048-tier-playbooks/` — SDD feature scaffold for new `tier-playbook` entity (standalone, tier-gated how-to guides parallel to `knowledge/`); README.md + spec.md (8 acceptance criteria, 5 functional requirements F1-F5, tier-inheritance citation rule) + design.md (folder shape `skills/faion/playbooks/<tier>/<group>/<slug>/`, 8 fixed H2 sections, front-matter schema, validator script spec, faion/SKILL.md amendments, boundary vs workflow-bound playbook) + implementation-plan.md (7 phases: 3 setup + 4 authoring waves, pool-based dispatch, ~648k token estimate) + test-plan.md (10 drift sentinels DS1-DS10, validator self-test, wave + feature acceptance, rollback criteria); catalog/ contains all-400-ideas.md (400 candidates, 100 per tier) + priority-120.md (top 30 per tier ranked, persona-coded, effort-sized); brainstorm provenance: 4 parallel multi-persona research agents (4 personas per tier) producing 400 ranked candidates synthesized into per-tier 30-item priority queues
- docs: add `.aidocs/conventions/workflows/` — authoritative spec for workflow + playbook entity types (workflow-spec.md, playbook-spec.md, AGENTS.md); locks in workflow-spec (folder shape, phase quad-block schema, tool allowlist, idempotency classes, output-contract grammar, three-axis SemVer, drift sentinels, decisions log, optional cross-cutting methodology refs, anti-patterns, inline template) and playbook-spec (Diátaxis how-to, front-matter schema, surface choices table, mandatory `## Methodologies` table linking to `skills/faion/knowledge/`, MAY/MAY-NOT override lists, worked-example requirement, drift sentinels, anti-patterns, inline template); synthesized from 6-agent diverge + 2-reviewer converge via /faion-brainstorm
- add: github-repo-bootstrap methodology (new)
- add: cloudflare-pages-github methodology (new)
- add: cloudflare-domain-dns methodology (new)
- docs: add Autonomous-Agent Sufficiency section to methodology-xml-schema (formalizes feature-048 requirements)
- add: llm-classifier-design methodology (new)
- improve: prototyping — methodology rewritten for autonomous agent application
- improve: competitive-analysis — methodology rewritten for autonomous agent application
- improve: key-trends-summary — methodology rewritten for autonomous agent application
- improve: release-planning — methodology rewritten for autonomous agent application
- improve: mlp-planning — methodology rewritten for autonomous agent application
- improve: minimum-product-frameworks — methodology rewritten for autonomous agent application
- improve: outcome-based-roadmaps-advanced — methodology rewritten for autonomous agent application
- improve: reporting-dashboards — methodology rewritten for autonomous agent application
- improve: zero-click-search-adaptation — methodology rewritten for autonomous agent application
- improve: topical-authority — methodology rewritten for autonomous agent application
- improve: seo — methodology rewritten for autonomous agent application
- improve: go-error-handling-patterns — methodology rewritten for autonomous agent application
- feat: add `skills/faion/workflows/sdd-batch-orchestrator/` — faion-network adaptation of the batch orchestrator proposal (12 phases, prompt-file convention, worktree+flock parallelism, verify-review-fix loop with surface-specific verifiers, focused recapture, tg-send/SDD delivery, quota gating); 10 semantic-XML content files + 4 templates; introduces `skills/faion/workflows/` as the home for end-to-end orchestration patterns
- docs: add `.aidocs/proposal/sdd-batch-orchestrator/` — abstract description of the SDD batch orchestrator pattern (12 phases, prompt-file convention, wave parallelism, verify-review-fix loop, focused recapture); semantic-XML content + reusable templates (prompt skeleton, playbook skeleton, dispatch message, focused-screenshot.py)
- Improve methodology: trade-off-quality-attributes (sufficient for autonomous agents)
- Improve methodology: database-selection (sufficient for autonomous agents)
- Improve methodology: data-modeling (sufficient for autonomous agents)
- Improve methodology: creational-patterns (sufficient for autonomous agents)
- Improve methodology: continuous-delivery (sufficient for autonomous agents)
- Improve methodology: best-practices-2026 (sufficient for autonomous agents)
- Improve methodology: api-gateway-patterns (sufficient for autonomous agents)
- Improve methodology: spatial-computing-overview (sufficient for autonomous agents)
- Improve methodology: methodologies-index (sufficient for autonomous agents)
- Improve methodology: methodologies-detail (sufficient for autonomous agents)
- Improve methodology: methodologies-summary (sufficient for autonomous agents)
- Improve methodology: seven-performance-domains (sufficient for autonomous agents)
- Improve methodology: google-display-ads (sufficient for autonomous agents)
- Improve methodology: gcp-arch-patterns (sufficient for autonomous agents)
- Improve methodology: aws-networking (sufficient for autonomous agents)
- Improve methodology: aws-architecture-services (sufficient for autonomous agents)
- Improve methodology: finops-framework (sufficient for autonomous agents)
- Improve methodology: container-orchestration (sufficient for autonomous agents)
- Improve methodology: cloud-architecture (sufficient for autonomous agents)
- Improve methodology: stakeholder-analysis (sufficient for autonomous agents)
- Improve methodology: modern-ba-framework (sufficient for autonomous agents)
- Improve methodology: ba-strategic-partnership (sufficient for autonomous agents)
- Improve methodology: business-analyst/ba-trends-summary (sufficient for autonomous agents)
- Improve methodology: figma-vs-adobe-strategy-2026 (sufficient for autonomous agents)
- Improve methodology: ai-spatial-computing (sufficient for autonomous agents)
- Improve methodology: llm-observability-stack (sufficient for autonomous agents)
- chore: improve ai-governance-compliance methodology with concrete checklist + commands (agent-coverage)
- chore: improve langchain-rag-pipeline methodology with concrete checklist + commands (agent-coverage)
- chore: improve ai-agent-patterns methodology with concrete checklist + commands (agent-coverage)
- chore: improve nodejs-express-fastify methodology with concrete checklist + commands (agent-coverage)
- chore: improve methodologies methodology with concrete checklist + commands (agent-coverage)
- chore: improve files-reference methodology with concrete checklist + commands (agent-coverage)
- chore: improve django-decision-tree methodology with concrete checklist + commands (agent-coverage)
- chore: fill remaining catalog descriptions (452 entries: 1 domain + 451 methodologies); catalog.py update now handles mixed domain/method JSON inputs
- chore: rebuild catalog after sdlc-ai migration; catalog.py now handles flat-group structure (sdlc-ai); methodology.xml replaces README.md (feature-047)
- chore: migrate tracker-ai-triage-classify-route, tracker-github-copilot-workspace, tracker-gitlab-duo-developer-flow to methodology.xml (feature-047 batch A16)
- chore: migrate uv-lockfile-floor to methodology.xml (feature-047 batch A18)
- chore: migrate test-consumer-contract-from-spec, test-golden-master-legacy-rewrite, test-mutation-feedback-loop to methodology.xml (feature-047 batch A14)
- chore: migrate tracker-jira-rovo-mcp-agents, tracker-linear-agent-as-assignee, ts-strict-isolated to methodology.xml (feature-047 batch A17)
- chore: migrate task-plan-mode-locked-execution, task-spec-kit-three-step, task-worktree-runtime-isolation to methodology.xml (feature-047 batch A13)
- chore: migrate test-property-based-llm-invariants, test-self-healing-locators-audited, test-tdd-red-green-split-agents to methodology.xml (feature-047 batch A15)
- chore: migrate pyproject-single-source, sec-codeql-autofix-on-pr, sec-secrets-defense-in-depth to methodology.xml (feature-047 batch A11)
- chore: migrate mr-codemod-refactor-agent, mr-error-tracker-draft-pr, mr-graph-vs-diff-reviewer to methodology.xml (feature-047 batch A9)
- chore: migrate mr-renovate-ai-handoff, mr-slash-command-surface, pnpm-catalogs to methodology.xml (feature-047 batch A10)
- chore: migrate sec-trivy-pinned-supply-chain-scan, task-agent-drafts-spec-before-coding, task-agent-fixable-triage-gate to methodology.xml (feature-047 batch A12)
- chore: migrate lint-autofix-vs-flag-decision-rule, lint-megalinter-polyglot, lint-precommit-floor to methodology.xml (feature-047 batch A7)
- chore: migrate lint-ruff-and-biome-as-default, lint-shellcheck-hadolint-iac-floor, lint-staged-only-not-whole-tree to methodology.xml (feature-047 batch A8)
- chore: migrate lang-php-phpstan9-psalm-taint, lang-ruby-sorbet-strict-floor, lang-swift-harmonize-arch-tests to methodology.xml (feature-047 batch A6)
- chore: migrate lang-csharp-roslyn-analyzer-errors, lang-go-tygo-frontend-contract, lang-jvm-jreleaser-tag-release to methodology.xml (feature-047 batch A5)
- chore: migrate inc-runbook-as-markdown-tagged-steps, inc-tool-tier-approval-gate, kb-agents-md-context-pyramid to methodology.xml (feature-047 batch A3)
- chore: migrate gov-sonarqube-ai-code-gate, inc-postmortem-auto-draft-no-publish, inc-read-only-investigation-default to methodology.xml (feature-047 batch A2)
- chore: migrate kb-codebase-rag-symbol-chunked, kb-symbol-index-fresh-tags, kb-versioned-agent-memory-files to methodology.xml (feature-047 batch A4)
- chore: migrate gov-approval-token-signed-jwt, gov-conventional-commits-enforced, gov-license-compliance-scan to methodology.xml (feature-047 batch A1)
- chore: migrate nginx-reverse-proxy, ssl-tls-management, server-init-bootstrap to methodology.xml (feature-045 batch FU)
- chore: migrate secrets-management, shell-productivity, ssh-hardening to methodology.xml (feature-045 batch FV)
- chore: migrate product-discovery, product-launch, release-planning to methodology.xml (feature-045 batch FT)
- chore: migrate continuous-discovery, feature-prioritization-moscow, feature-prioritization-rice to methodology.xml (feature-045 batch FS)
- chore: migrate 3/3 solo/ux/ux-ui-designer methodologies → methodology.xml (mobile-ux, prototyping, recognition-over-recall; feature-045 batch FR)
- chore: migrate success-metrics-definition, use-case-mapping, user-interviews to methodology.xml (feature-045 batch FH 3/3)
- chore: migrate reflexion-learning, sdd-workflow-overview, task-creation-parallelization to methodology.xml (feature-045 batch FM 3/3)
- chore: migrate writing-specifications, yaml-frontmatter, use-case-mapping to methodology.xml (feature-045 batch FO)
- chore: migrate 3/3 solo/sdd methodologies → methodology.xml (key-trends-summary, living-documentation, mistake-memory; feature-045 batch FO)
- chore: migrate ops-financial-planning, ops-pricing-strategy, tailwind-design-tokens to methodology.xml (feature-045 batch FQ)
- chore: migrate product-launch, roadmap-design, feature-prioritization-rice to methodology.xml (feature-045 batch FD 3/3)
- chore: migrate 3/3 solo/product/product-manager methodologies → methodology.xml (mvp-scoping, outcome-based-roadmaps-advanced, product-discovery; feature-045 batch FC)
- chore: migrate seo-techniques, topical-authority, clickup-setup to methodology.xml (feature-045 batch FA 3/3)
- chore: migrate growth-seo-link-building, seo, seo-basics to methodology.xml (feature-045 batch EZ)
- chore: migrate swap-memory-management, systemd-user-services, tmux-power-user to methodology.xml (feature-045 batch ES 3/3)
- chore: migrate 3/3 solo/sdd methodologies → methodology.xml (api-first-development, architecture-decision-records, backlog-grooming-roadmapping; feature-045 batch FI)
- chore: migrate go-concurrency-patterns, unattended-upgrades, wireguard-vpn to methodology.xml format (FEATURE-045 batch ET 3/3)
- chore: migrate 3/3 solo/marketing methodologies → methodology.xml (ops-automation-workflow, ops-dashboard-setup, ops-customer-support; feature-045 batch EX)
- migrate: 3/3 solo/dev/software-developer methodologies → methodology.xml (api-versioning, browser-automation, api-graphql; feature-045 batch EK)
- chore: migrate graphql-api, graphql-api-design, internationalization to methodology.xml (FEATURE-045 batch EW sonnet retry)
- chore: migrate agent-dev-tuning, bash-aliases to methodology.xml format (FEATURE-045 batch EH 2/3)
- chore: migrate direnv-mise-versions to methodology.xml (FEATURE-045 batch EJ 3/3)
- chore: migrate deploy-scripts to methodology.xml (FEATURE-045 batch EJ 2/3)
- chore: migrate cron-automation to methodology.xml (FEATURE-045 batch EJ 1/3)
- chore: migrate logging-patterns, message-queues, monorepo-turborepo to methodology.xml format (FEATURE-045 batch ER 3/3)
- chore: migrate rest-api-design, docker-compose (cicd), docker-compose (infra) to methodology.xml (FEATURE-045 batch EU)
- chore: migrate graphql-api, graphql-api-design, internationalization to methodology.xml format (FEATURE-045 batch EA 3/3)
- migrate: 3/3 solo/dev/software-developer Go methodologies → methodology.xml (go-error-handling-patterns, go-project-structure, go-standard-layout; feature-045 batch DZ)
- migrate: 3/3 solo/dev/software-developer methodologies → methodology.xml (python-async-patterns, rate-limiting, react-component-architecture; feature-045 batch EF)
- chore: migrate openapi-specification, performance-testing, pwa-development to methodology.xml format (FEATURE-045 batch EE 3/3)
- chore: migrate caching-strategy, contract-first-development, database-design to methodology.xml format (FEATURE-045 batch EP 3/3, sonnet retry)
- migrate: 3/3 solo/infra/server-craft methodologies → methodology.xml (kernel-tuning, monitoring-logging, multi-project-hosting; feature-045 batch EN)
- migrate: api-openapi-spec, docker-compose-patterns, dotfiles-management → methodology.xml (feature-045 batch EL)
- migrate: 3/3 solo/dev/software-architect methodologies → methodology.xml (modular-monolith, monolith-architecture, patterns-overview; feature-045 batch EI)
- migrate: performance-architecture to methodology.xml (feature-045 batch ED)
- migrate: quality-attributes to methodology.xml (feature-045 batch ED)
- migrate: security-architecture to methodology.xml (feature-045 batch ED)
- migrate: 3/3 solo/dev methodologies → methodology.xml (xp-extreme-programming, accessibility, css-in-js-advanced; feature-045 batch DR)
- migrate: 3/3 solo/dev/software-developer API methodologies → methodology.xml (api-graphql, api-openapi-spec, api-rate-limiting; feature-045 batch DT)
- migrate: 3/3 python-developer/software-architect methodologies → methodology.xml (django-celery, django-services, architecture-decision-records; feature-045 batch DV)
- migrate: 3/3 solo/dev/software-developer methodologies → methodology.xml (design-tokens, django-celery, django-services; feature-045 batch DL)
- migrate: 3/3 solo/dev/software-developer methodologies → methodology.xml (nextjs-app-router, nodejs-service-layer, nosql-patterns; feature-045 batch EC)
- migrate: 3/3 paths to methodology.xml (ui-lib-patterns, nextjs-app-router, nodejs-service-layer-architecture; feature-045 batch DJ)
- migrate: 3/3 frontend-developer methodologies → methodology.xml (shadcn-ui, shadcn-ui-architecture, storybook-setup; feature-045 batch DF)
- migrate: 3/3 batch DA methodologies → methodology.xml (trunk-based-dev-patterns, trunk-based-dev-principles, framework-decomposition-patterns; feature-045 batch DA)
- migrate: 3/3 pro/research/market-researcher methodologies → methodology.xml (competitive-intelligence-methods, competitor-analysis, ui-lib-basics; feature-045 batch DI)
- migrate: 3/3 solo/dev/software-architect methodologies → methodology.xml (behavioral-patterns, c4-model, caching-architecture; feature-045 batch DM)
- migrate: 3/3 automation-tooling methodologies → methodology.xml (cd-basics, cd-pipelines, continuous-delivery; feature-045 batch CW)
