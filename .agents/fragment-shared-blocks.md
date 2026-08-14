# Fragment shared blocks — the sourcing rule and the commit rule

Detail displaced out of [`skills/faion/fragments/AGENTS.md`](../skills/faion/fragments/AGENTS.md),
which has a 20-80 line budget. Both rules exist because a measured
pipeline run shipped something worse than an unprompted agent would
have, and both are asserted by a validator rather than left as style
notes.

## The sourcing rule (research roles)

**faion never goes to the internet — the calling agent does.** The corpus
carries the durable half: what to source, what makes a claim
load-bearing, how to tag confidence, what a finished evidence artifact
looks like. URLs, figures and dates are fetched live, because they rot.

So **every research-role fragment includes
`{{include:corpus:research-source-discipline}}`**, and that block keeps
its four anchors:

1. URL plus access date on every claim;
2. the H/M/L confidence definitions;
3. the "no reliable public figure found" path, so an absent number is
   recorded rather than invented;
4. `faion fact add` provenance.

`scripts/validate-recipes.py` asserts both halves: a fragment whose
opening role line names a researcher, analyst, market, competitor or
evidence role and omits the include is a **failure**.

Measured 2026-08-11, one brief, blind judges: the pipeline run produced
**14 competitors and 0 source URLs**; a plain agent that went to the web
produced **31 and 108**, and won on research depth. Before the
`research/` pack, no fragment in the corpus required a URL, an access
date, a confidence tag or a source floor — the prompts asked for less
than an unprompted agent does on its own.

## The commit rule (every role that writes a file)

A deliverable git has never seen does not survive a clone — and
`deploy-gh.sh` rsyncs a working tree, so it ships anyway, from one
machine, once. Two pipeline runs ended with **23 and 9 untracked
deliverables**; both reported success.

So **every fragment whose output contract names a file it writes
includes `{{include:corpus:gate-commit-discipline}}`**: exactly
`git add` and `git commit`, exactly the paths that contract names, never
`git add -A` (which sweeps in whatever else the run left lying around),
never `--no-verify`, never a push, rebase or reset, and a 50-char
`type: short description` title.

Those roles' hard boundaries no longer forbid git outright — a role
cannot be told both to commit its output and never to run git. Seven of
them previously ended with "never run build, deploy, or git write
commands"; that is now "never run build or deploy commands".

The block lives in `gate/` because it is cross-pack and is a gate on
delivery. Like `research-source-discipline` it declares no slots and
carries no role line, so the role rules do not apply to it.

The other half of the mechanism is the stage's `produces` contract,
which the emitted workflow reads back with `git ls-files` and
`git status` — see [`skills/faion/recipes/AGENTS.md`](../skills/faion/recipes/AGENTS.md).
The corpus asks; the artifact verifies.
