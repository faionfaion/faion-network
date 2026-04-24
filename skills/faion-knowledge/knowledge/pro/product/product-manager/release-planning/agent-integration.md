# Agent Integration — Release Planning (Product Manager)

> Companion to the solo-tier `product-planning/release-planning` methodology. This file is the **PM-flavored** angle: cross-functional release coordination, executive comms, customer-facing release notes, GTM gating. For the engineer-only variant (deploy mechanics, feature flags, rollback drills) see the devops/cicd skills. Do not duplicate.

## When to use
- A multi-team release crosses engineering, support, sales-enablement, marketing, and legal — the PM brokers the `Ready` gate per function and refuses to ship until each is green.
- The product has paying customers and breaking changes are on the table; release notes, migration guides, and a deprecation timeline are part of the deliverable, not an afterthought.
- The release calendar has just slipped twice in a row. The cure is rarely "work harder"; it is shrinking the release contents and shortening the cycle (e.g. monthly → biweekly → weekly).
- A regulated or contractual release window applies (SLA-bound deploy windows, customer change-control approvals, broker/escrow review). The PM owns the customer-facing artifact, not just the eng artifact.
- Pre-launch GTM coordination where a feature requires sales decks, support macros, pricing-page copy, and analyst briefing — sequencing matters, not just the deploy.
- Release-train cadence reviews: PM owns whether the train left full or empty, and whether features missed because they were under-scoped or because dependencies were not modeled.

## When NOT to use
- Trunk-based / continuous deployment with feature flags at scale. There is no "release plan" — there is feature-flag rollout per cohort. Use a launch plan tied to flag percentages and a kill-switch runbook, not a versioned release plan.
- Pure infrastructure/refactor work with zero customer-visible behavior change. An eng-internal changelog is enough; a PM release plan adds ceremony.
- Solo founder shipping to <50 users daily on a single SaaS. A `git push` + Discord post is the right ceremony; a release plan template signals premature optimization.
- When the "release" is really an A/B experiment. Use `experimentation-design` and pick a metric, not a ship date.
- Hotfixes for live incidents. Use the incident-response runbook; release-planning's deliberation kills time-to-mitigate.

## Where it fails / limitations
- **PM as deploy gate**: PMs who treat release planning as veto power become the bottleneck. The plan is a coordinator, not an approver — eng owns deploy mechanics; the PM owns *external readiness*.
- **Train-the-monster antipattern**: monthly trains accumulate too much scope; one feature slips and the whole train slips, forcing the PM to pull-or-postpone painful tradeoffs at the last minute. Smaller trains with feature flags decouple readiness from ship date.
- **Communication-plan inflation**: PMs over-index on the comms matrix (every audience × every channel × every revision). Most of those rows produce zero customer behavior change. Cut the matrix to channels where you can later prove engagement; delete the rest.
- **Release-notes drift**: notes get drafted on Monday, the deploy slips to Thursday, two more PRs land — and the notes ship inaccurate. Generate notes from merged-PR labels at deploy time; never edit a release notes doc disconnected from git history.
- **Hidden dependencies**: a feature depends on a back-office migration, a data-team backfill, or a vendor contract clause renewing — none of which are in the eng tracker. The plan looks green; reality is red. Force a `cross-team dependencies` section with a named owner per row.
- **Rollback theater**: every plan has "Rollback Plan: revert PR" and nobody has actually drilled it on this codebase. The first real rollback fails and discredits the PM. Drill rollback in staging at least quarterly, with the on-call who would actually execute it.
- **Friday-shipping politics**: the methodology says Mon-Wed; reality is sales pushed for an end-of-quarter ship. The PM caves and Friday-deploys. Document the exception, log the post-mortem proactively if it bites; do not pretend the policy held.
- **Customer-facing changelogs as marketing copy**: an LLM-rewritten changelog reads as press-release fluff and erodes trust. Customers who read changelogs want truth, including known issues; over-polished notes signal hiding.

## Agentic workflow
The PM-flavored release pipeline is four loops, each driven by a different subagent and gated by a human signoff. (1) **Contents-freeze loop** — at T-N days, an agent reads the project tracker, filters tickets where `status=ready-for-release` AND `target-version=vX.Y.Z`, cross-references CI green status, and posts a candidate manifest to the release channel. PM reviews; manifest is frozen. (2) **Readiness-matrix loop** — for each candidate, the agent walks per-function checklists (eng-done, docs-done, support-trained, marketing-asset-ready, legal-cleared, GTM-cohort-defined) and emits a `release-readiness.md` with green/yellow/red per cell, plus the named owner. Yellow/red cells block until reviewed. (3) **Notes-and-comms loop** — at T-1, the agent generates *three* artifacts from the manifest + merged-PR metadata: customer-facing release notes (markdown for the changelog page), an internal eng release summary (links to PRs, ADRs, runbook diffs), and a sales/support enablement brief (one-pager: "what changed, what to say, what to escalate"). PM edits, never auto-publishes. (4) **Post-release retro loop** — T+24h to T+7d, the agent pulls deployment metrics, error-rate deltas, support-ticket spike data, customer-feedback channel mentions, and drafts a retro doc. PM holds a 30-min retro; outputs `decisions.md` entries for the next cycle.

### Recommended subagents
- `faion-mlp-impl-planner-agent` (referenced in this methodology's frontmatter) — owns the contents-freeze loop: reads the tracker, validates `definition-of-done` per ticket, builds the manifest, refuses to include items that fail the DoD lint.
- `faion-sdd-executor-agent` — for any SDD task carrying a `release-blocker` label, the executor reads `release-readiness.md` and refuses to mark the parent feature `done` until every readiness cell for that feature is green or has a documented exception.
- `faion-pm-agent` (sibling under product-manager skill) — generates the readiness matrix and stakeholder-specific comms drafts; cites the source PRD and ticket history for every claim it makes.
- `faion-marketing-manager` / `faion-gtm-strategist` — consumes the manifest to produce launch-day assets (blog post, social copy, analyst brief). Subordinate to PM signoff; never auto-publishes.
- `faion-content-marketer` — drafts the *customer-facing* release notes from PR descriptions and ticket summaries, with explicit instructions to preserve known-issues honestly.
- `password-scrubber-agent` — non-negotiable before any release-readiness doc, manifest, or retro lands in a public repo or customer-facing channel. Release plans frequently embed customer names, internal URLs, vendor-contract details.

### Prompt pattern
Manifest generation (contents-freeze loop):
```
You are a release-planning agent. Read the project tracker via API/CLI for
items where status="ready-for-release" AND fixVersion="vX.Y.Z". Cross-check:
  - CI green for the target branch (last 24h)
  - All linked PRs merged
  - definition-of-done checklist complete (cite the DoD doc path)
  - Migrations have a rollback script committed
For each item, output: ticket_id, title, owner, risk (L/M/H + 1-line rationale),
customer_visible (Y/N), breaking_change (Y/N), feature_flag (name or "none").
Emit a manifest.md table; flag any item that fails any check as `BLOCKED`
with the missing condition. Do not auto-remove blocked items; the PM decides.
```

Readiness-matrix prompt (cross-functional gate):
```
Read manifest.md and the team-roster doc. For each customer_visible=Y item,
build a readiness row with columns:
  function (eng | docs | support | marketing | legal | sales-enablement | infra)
  artifact (specific deliverable, not "ready")
  owner (named person)
  status (green | yellow | red | n/a)
  evidence_link (URL to the doc/PR/ticket proving green; required for green)
Yellow/red rows must include a `blocker` and `expected-resolution-date`.
Output to release-readiness.md. Refuse to mark green without an evidence_link.
```

Customer-facing release notes (anti-fluff discipline):
```
Read manifest.md and the merged-PR descriptions. Draft customer-facing
release notes in this exact structure:
  # vX.Y.Z (YYYY-MM-DD)
  ## Highlights         (1-2 sentences, plain English, no marketing adjectives)
  ## New                (bullet per feature, what + why-it-matters, no codenames)
  ## Improved           (bullet per change, observable user impact)
  ## Fixed              (bullet per fix, link to public issue if any)
  ## Breaking changes   (with migration steps, not just a warning)
  ## Known issues       (be honest; workarounds where possible)
  ## Deprecations       (timeline + replacement)
Hard rules:
  - No "we are excited" / "delighted" / "thrilled" filler.
  - No internal codenames without a one-line gloss.
  - If a section has no content, omit the header (do not write "None").
  - Cite the merge SHA per bullet in a hidden HTML comment for traceability.
Output a draft for human review. Do not publish.
```

Sales/support enablement brief:
```
From manifest.md, draft a one-page brief titled "vX.Y.Z — What changed for
your customer". Sections: "What's new (user-facing)", "What to say if asked",
"What to escalate", "Pricing/packaging changes (Y/N)", "Known limitations".
Audience: a tier-2 support agent or an AE preparing for a renewal call. No
engineering jargon; use customer-visible names only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Build manifest from PR labels (`gh pr list --label release-vX.Y.Z`); auto-generate notes via `gh release create --generate-notes` | https://cli.github.com |
| `glab` | GitLab equivalent for manifest + release-notes generation | https://gitlab.com/gitlab-org/cli |
| `git-cliff` | Conventional-commit → changelog generator; backbone of automated release notes | https://github.com/orhun/git-cliff |
| `release-please` (Google) | Automated release-PR generator from conventional commits; common for monorepos | https://github.com/googleapis/release-please |
| `semantic-release` | Versioning + changelog + publish from commit messages; Node-centric but multi-language | https://semantic-release.gitbook.io |
| `changesets` | Per-PR changeset files for monorepos (npm-heavy); decouples notes from commit messages | https://github.com/changesets/changesets |
| `goreleaser` | Go-binary release packaging + notes; widely used for CLI tools | https://goreleaser.com |
| `linear-cli` | Pull `Ready` issues into the manifest | https://developers.linear.app |
| `jira-cli` | Same for Jira-backed shops; filter by fixVersion | https://github.com/ankitpokhrel/jira-cli |
| `slack-cli` | Post manifest, readiness summary, and retro draft to release channels | https://api.slack.com |
| `notion-cli` | Sync the readiness matrix into the customer-facing roadmap page | https://developers.notion.com |
| `mailmerge` | Send per-customer or per-cohort release emails from a CSV (no marketing tool needed) | `pip install mailmerge` |
| `kubectl` / `argocd` / `flux` CLIs | Drive the actual deploy step from the release manifest (PM observes, eng owns) | platform-specific |
| `openfeature-cli` / `launchdarkly` / `flagsmith` CLIs | Tie release plan items to feature flags; toggle by cohort | provider-specific |
| `pandoc` | Render notes to PDF for board reports / regulated-industry change-records | system package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Releases | SaaS | Yes — REST + `gh` | Default for OSS / dev-tool releases; generates notes from PR labels |
| GitLab Releases | SaaS / Self-hosted | Yes — REST + `glab` | Tight integration with milestones; first-class for regulated orgs |
| LaunchDarkly | SaaS | Yes — REST + SDKs | Feature-flag-driven release; PM defines cohorts, plan tracks % rollout |
| Statsig | SaaS | Yes — REST | Flags + experiments + metric guardrails on release |
| Flagsmith | OSS / SaaS | Yes — REST | Self-hostable flag platform; common in privacy-sensitive shops |
| Unleash | OSS | Yes — REST | OSS feature-flag service; pairs with self-hosted release runners |
| Linear | SaaS | Yes — GraphQL | `Cycle` and `Project` map naturally to release manifest |
| Jira / Jira Service Mgmt | SaaS / DC | Yes — REST | `fixVersion` is the canonical manifest filter; weak for cross-team gating |
| Productboard | SaaS | Yes — REST | Public-facing roadmap + release notes for B2B SaaS |
| Aha! Roadmaps | SaaS | Yes — REST | Built-in release manager + customer portal |
| Headway / Canny / FeedBear | SaaS | Yes — REST | Customer-facing changelog widgets; embed release notes site-wide |
| Beamer | SaaS | Yes — REST | In-app release announcement widget; pairs with notes pipeline |
| Statuspage / Statuspal | SaaS | Yes — REST | Release windows = scheduled maintenance; declarative incident posts on regression |
| Sentry / Rollbar / Bugsnag | SaaS | Yes — REST | Track release-tagged error rates; the post-release retro pulls from here |
| Datadog / Honeycomb / New Relic | SaaS | Yes — REST | Release annotations on dashboards; correlate deploys with metric shifts |
| Argo CD / Spinnaker / Harness | OSS / SaaS | Yes — REST/CRDs | Progressive-delivery; PM plan items become rollout stages |
| PagerDuty / Opsgenie | SaaS | Yes — REST | Auto-create release-watch incident; PM links from the plan |
| Confluence / Notion | SaaS | Yes — REST | Default home for the human-readable plan; readiness matrix as a database |
| Mailchimp / Customer.io / Intercom | SaaS | Yes — REST | Customer release-email orchestration; PM drafts copy, marketing automates send |

## Templates & scripts
The README ships generic plan and notes templates. The PM-specific gap is the *readiness matrix* — green/yellow/red per function with mandatory evidence links. This script lints the matrix to catch the most common failure (a green cell with no evidence URL).

```python
# release_readiness_lint.py — fail CI if any "green" row lacks an evidence link.
# Input:  release-readiness.md (table format with columns: function, artifact,
#         owner, status, evidence_link, blocker)
# Usage:  python release_readiness_lint.py release-readiness.md
# Exit:   0 = clean, 1 = at least one violation (suitable for pre-merge hook).
import re, sys, pathlib

p = pathlib.Path(sys.argv[1])
lines = p.read_text(encoding="utf-8").splitlines()
rows = [ln for ln in lines if ln.startswith("|") and "---" not in ln]
if len(rows) < 2:
    sys.exit("readiness matrix has no rows")

hdr = [c.strip().lower() for c in rows[0].strip("|").split("|")]
need = {"function", "artifact", "owner", "status", "evidence_link"}
missing = need - set(hdr)
if missing:
    sys.exit(f"missing required columns: {missing}")

idx = {c: hdr.index(c) for c in need}
url_re = re.compile(r"https?://\S+")
violations = []
for ln in rows[1:]:
    cells = [c.strip() for c in ln.strip("|").split("|")]
    if len(cells) < len(hdr):
        continue
    status = cells[idx["status"]].lower()
    evidence = cells[idx["evidence_link"]]
    fn = cells[idx["function"]]
    art = cells[idx["artifact"]]
    if status == "green" and not url_re.search(evidence):
        violations.append(f"GREEN without evidence URL: {fn} / {art}")
    if status in ("yellow", "red") and not cells[idx["owner"]]:
        violations.append(f"{status.upper()} without named owner: {fn} / {art}")

if violations:
    print("\n".join(violations))
    sys.exit(1)
print(f"OK: {len(rows) - 1} rows, all green cells have evidence")
```
Wire this into `.pre-commit-config.yaml` so the readiness doc cannot be merged green-without-evidence. Combine with `git-cliff --tag vX.Y.Z` for auto-notes from conventional commits, edited by the PM for tone.

## Best practices
- Write the release notes *before* the readiness matrix is green. If you cannot describe the release to a customer in one paragraph, the scope is wrong; cut, don't pad.
- Force a `customer_visible` boolean on every manifest item. Items with `customer_visible=N` skip the comms loop entirely; this halves PM workload on infra-heavy releases.
- Make `definition-of-done` per item, not per release. A "release-wide DoD" hides items that never met theirs and shipped anyway.
- Track *cycle time* (commit → live for the median feature) per release and review the trend. PMs who only track ship-date hit-rate miss the truth: they are shipping smaller things slower.
- Run a `pre-mortem` two days before ship: "Imagine we are issuing a postmortem next week — what is it about?". Surfaces the dependency you forgot.
- Keep a `release exceptions log` separate from the readiness matrix. Each Friday-deploy, each yellow-shipped-anyway item, each comms-skip is a row. Review quarterly to spot policy decay.
- For B2B SaaS with named accounts, maintain a per-account release-impact view: which features land, which deprecations affect them, which migrations they must run. Drives the AM/CSM brief.
- Tie release retros to the next release's risk register. A regression caused by a missing flag becomes a "must have flag" entry in the next plan's risk row, with the named owner.
- Treat `Known issues` in customer notes as a feature, not a flaw. Customers trust changelogs that admit limits; absence of known-issues for two releases in a row is a smell, not a victory.
- Version the *plan* itself, not just the software. Plan v1 is the freeze-day artifact; plan v2 is the post-retro corrected version. Diff is the learning record.

## AI-agent gotchas
- **Hallucinated PR contents** — the agent invents a feature in the notes that does not exist in any merged PR. Force every notes bullet to cite a merge SHA in an HTML comment; lint that the SHA exists in `git log`.
- **Auto-publishing release notes** — never. The agent emits a draft to a PR or doc; a human merges. One auto-publish of an inaccurate note destroys more trust than a year of well-edited drafts builds.
- **Sycophantic marketing voice** — LLMs default to "thrilled" and "delighted". Add an explicit anti-fluff clause to the prompt and a post-generation lint that rejects drafts containing those tokens.
- **Breaking-change blindness** — agents extracting notes from PR labels miss the *implicit* breaking change (a default value flipped, an undocumented header now required). Require breaking-change rows to be human-asserted, not LLM-derived from PR titles.
- **Migration-script hallucinations** — agents generate confident `ALTER TABLE` examples that drift from the actual migration. Pull migration content from the migration files in the PR, not from the agent's interpretation.
- **Stale manifest** — an agent run at T-3 days that is not re-run at T-1 ships an obsolete manifest. Make the manifest a CI artifact regenerated on every push to the release branch; consume the freshest only.
- **Comms-channel blast radius** — agents posting drafts to a customer-visible Slack channel by mistake (typo in channel ID) is a real failure mode. Restrict the agent's channel allowlist; require an explicit `--channel` arg, not a default.
- **Long-context manifest dumps** — feeding the entire 200-row manifest into every prompt wastes tokens and dilutes attention. Filter to `customer_visible=Y` for notes; filter to `breaking_change=Y` for migration guides. One filter per artifact.
- **Prompt injection via PR descriptions** — a hostile or sloppy contributor pastes content into a PR description that the agent ingests verbatim into release notes. Sanitize ingested text; never let agent-ingested PR text become customer-facing without human review.
- **Privacy bleed in retros** — agents pulling support-ticket data into the post-release retro can inadvertently embed customer PII into a doc that goes wider than expected. Run `password-scrubber-agent` on every retro; redact ticket bodies, keep only counts and categories.
- **Versioning drift** — agent picks `v1.2.3` from a tag that was never pushed; or picks `v1.2.4` while a hotfix already claimed `v1.2.4`. Always read tags from the upstream remote, never from local-only state; lint that the proposed version > all existing remote tags.
- **Cohort-flag mismatch** — a release plan item names feature flag `new-checkout` but the deployed flag is `checkout-v2`. Have the agent diff the manifest's flag-names column against the live flag-platform API; mismatch = hard fail.
- **Calendar-bound assumptions** — "ship Tuesday" baked into prompts ages poorly across timezones, holidays, and frozen weeks (US Thanksgiving, EU August). Encode the deploy window as a date range from a calendar source, not a string in the prompt.

## References
- Marty Cagan — *Inspired* (2nd ed., 2017) and *Empowered* (2020) — PM-as-coordinator chapters covering release readiness and exec comms.
- Lenny Rachitsky — "How to launch" and "Anatomy of a great release" essays (https://www.lennysnewsletter.com).
- Jason Cohen — "Releases are a feature" (A Smart Bear blog, https://longform.asmartbear.com/releases/).
- Dave Farley & Jez Humble — *Continuous Delivery* (2010) — the canonical text on the deploy mechanics that release-planning rides on; read alongside, not instead of.
- Charity Majors — "Test in production, deploy when you want" (https://charity.wtf) — the case for decoupling deploy from release.
- Reforge — *Mastering Product Launches* program — release-vs-launch distinction and GTM cohort design.
- Stripe API changelog and AWS What's New — gold-standard examples of customer-facing release notes; study what they include and what they deliberately omit.
- Sibling methodologies in this skill: `roadmap-design`, `task-creation-parallelization`, `change-control`, `product-launch`, `feature-prioritization`.
- Companion file: `../../../solo/product/product-planning/release-planning/` (solo-tier baseline; this PM file extends it).
