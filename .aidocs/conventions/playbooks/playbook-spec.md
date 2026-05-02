---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
applies_to: skills/faion/playbooks/<tier>/<group>/<slug>/playbook.md
---

> **For:** tier-playbook authors (LLM agent or human). **Prereqs:** read `AGENTS.md` first; for the sibling entity see `../workflows/playbook-spec.md`. **You will:** create or audit a `playbook.md` under `skills/faion/playbooks/<tier>/<group>/<slug>/`.

**TL;DR**

- A tier playbook is a Markdown how-to that solves one self-contained user task at a specific pricing tier.
- Lives at `skills/faion/playbooks/<tier>/<group>/<slug>/playbook.md`. One folder per playbook (kebab-case slug, unique cross-tier).
- Every active playbook MUST cite ≥1 methodology from `skills/faion/knowledge/<tier>/...` whose tier ≤ the playbook's tier.
- 8 fixed front-matter keys + 7 fixed H2 sections in fixed order.
- Validator: `python3 scripts/validate-tier-playbook.py <path>`. Pre-commit + CI both run it.

---

## 1. Definition + boundary

A **tier playbook** is a per-task, per-tier adaptation of one or more knowledge methodologies. It records the concrete steps a human or agent follows to accomplish one specific goal.

**Boundary statement (load-bearing):**

> Tier playbooks adapt knowledge to a task at a tier. Workflow playbooks adapt a workflow to a surface. Same word, different axis.

If your draft adapts execution along a delivery surface (frontend, backend, storybook), author a workflow playbook (`../workflows/playbook-spec.md`). If it adapts along a topic + audience tier, author it here.

A tier playbook MUST NOT contain:

- Phase orchestration (that belongs in a workflow).
- Surface-specific deploy mechanics (that belongs in a workflow playbook).
- Pure theory or rationale (that belongs in a methodology under `knowledge/`).

## 2. Diátaxis position: how-to

Tier playbooks are *how-tos* in the Diátaxis sense: goal-oriented, assume reasonable competence at the playbook's tier, deliver a recipe. Section titles use action-leading verbs. Reference and explanation belong in `knowledge/`, not here.

## 3. Where playbooks live

```
skills/faion/playbooks/<tier>/<group>/<slug>/
├── playbook.md           REQUIRED  the canonical body
├── checklist.md          OPTIONAL  printable step-by-step checklist
├── templates.md          OPTIONAL  copy-paste artifacts (configs, snippets)
├── examples.md           OPTIONAL  worked example with real names
└── references.md         OPTIONAL  separate citation file (otherwise inline in playbook.md)
```

### Naming

- Slug regex: `^[a-z][a-z0-9-]{2,40}$`. Kebab-case.
- Slugs are **globally unique across all tiers**. `vps-first-deploy` cannot exist in both `solo/` and `pro/`.
- The slug folder name MUST equal the `name` key in front-matter.

### Tiers

| Tier | Folder | Audience |
|------|--------|----------|
| free | `playbooks/free/` | beginner / explorer; no payment |
| solo | `playbooks/solo/` | solopreneur ($19/mo) |
| pro | `playbooks/pro/` | small agency / studio ($35/mo) |
| geek | `playbooks/geek/` | AI-builder / power user ($99/mo) |

Tiers are directories; gating is enforced by `skills/tier-manifest.json` and the validator.

### Groups

Each tier holds topic groups (`tech-setup/`, `business-discovery/`, `mvp-essentials/`, etc.). Group slug regex matches playbook slug regex. Group folders carry an `AGENTS.md` (≤80 lines) listing playbooks.

## 4. Front-matter required keys

```yaml
---
name: <slug>                                  # equals folder name
description: <one-line, ≤200 chars, action-leading>
tier: free | solo | pro | geek
group: <kebab-case group slug>
status: draft | active | deprecated
owner: <handle>
last_verified: YYYY-MM-DD
version: <semver>                             # 1.0.0 on first publish
---
```

Mismatch between `name` and folder, or `tier` and parent dir, fails validator. `last_verified` >180 days old triggers a warn-on-commit / block-on-PR-merge.

## 5. Required H2 sections (in order)

```
1. ## Goal
2. ## Prerequisites
3. ## Steps
4. ## Verify
5. ## Troubleshooting
6. ## Next
7. ## References
```

A playbook with sections out of order or missing one fails the validator.

### Section content rules

- `## Goal` — one paragraph: *"after this playbook you will have <X>"*. No theory, no philosophy.
- `## Prerequisites` — bullet list: assumed knowledge, accounts, tools installed, prior playbooks (linked).
- `## Steps` — numbered list. Each step starts with an action verb. Real commands, real URLs, real values. **No `foo`/`bar`/`example.com` placeholders.** Code blocks runnable as-is or with named variables.
- `## Verify` — concrete check: a `curl` command, a browser URL, a file existence check, a log line. The reader should be able to run one thing and know whether the playbook worked.
- `## Troubleshooting` — table or bullet list. Each entry: **Symptom → Cause → Fix**. ≥1 entry required for `status: active`.
- `## Next` — 1–3 verb-led pointers. Other tier playbooks (linked), follow-up methodologies, or higher-tier upgrades.
- `## References` — citation table (see §6).

## 6. Citation rule (`## References`)

Required minimum: ≥1 citation for `status: active` playbooks.

Schema (Markdown table OR bullet list — both accepted):

```markdown
- [knowledge/<tier>/<group>/<skill>/<methodology>](../../../knowledge/<tier>/<group>/<skill>/<methodology>) — <playbook-specific rationale, ≥10 chars>
```

OR

```markdown
| Methodology | Why for this playbook |
|-------------|-----------------------|
| `knowledge/<tier>/<group>/<skill>/<methodology>` | <playbook-specific rationale> |
```

### Validation

The validator enforces:

1. **Path resolves.** The methodology folder exists under `skills/faion/knowledge/`.
2. **Tier ≤ playbook tier.** Citation tier (parsed from path) is ≤ playbook tier (from front-matter). Tier order: `free=0 < solo=1 < pro=2 < geek=3`. A `free` playbook MUST NOT cite a `solo`/`pro`/`geek` methodology.
3. **Rationale present + specific.** The `—` (em-dash) segment is non-empty, ≥10 chars, and not in the generic-phrase blocklist (`"explains"`, `"covers"`, `"introduces"` without specificity). Generic rationale fails review.
4. **Cross-playbook references** (optional) follow the same `tier ≤` rule.

## 7. Drift sentinels

Run on every commit during authoring (the validator covers DS1–DS10):

| ID | Sentinel | Pass criterion |
|----|----------|----------------|
| DS1 | All citation paths resolve | Every `## References` path exists under `skills/faion/knowledge/` |
| DS2 | Tier ≤ rule | Every citation tier ≤ playbook tier |
| DS3 | 7-section structure | All 7 H2 sections present + ordered |
| DS4 | Front-matter complete | 8 required keys + valid values |
| DS5 | Slug shape | Regex match |
| DS6 | No duplicate slugs cross-tier | Globally unique |
| DS7 | AGENTS.md ≤80 lines | Per group + tier + root |
| DS8 | last_verified ≤180 days | Warn-only on commit; block on PR-merge if older |
| DS9 | Citation rationale specific | ≥10 chars, not in generic-phrase blocklist |
| DS10 | No `foo`/`bar`/`example.com` placeholders | grep returns 0 in Steps |

## 8. Anti-patterns (will fail review)

1. **Generic citation rationale.** `"explains REST"`, `"covers Cloudflare basics"`. Rewrite as: what does *this* methodology contribute to *this* playbook's steps?
2. **Tier exceeds.** Free playbook cites a solo/pro/geek methodology. Either move the playbook up, or find a free methodology that covers the underlying theory.
3. **`foo`/`bar`/`example.com` in Steps.** Use real names: `mydomain.com`, `myapp`, `2024-q1-launch`. If a real value would leak secrets, use a clearly-marked placeholder (`<your-domain>`) and document it in Prerequisites.
4. **Theory paragraphs in Steps.** "Cloudflare DNS works by…" — that's methodology content, link it instead.
5. **Out-of-order sections.** `## Steps` before `## Prerequisites` is a hard fail.
6. **Missing Troubleshooting.** Every active playbook has known pitfalls; if you genuinely can't think of any, the playbook is too shallow to ship.
7. **Steps without action verbs.** `"Cloudflare config"` → `"Add an A record pointing your domain at the server IP"`.
8. **Verify section that says only "it should work".** Specify the exact check: `curl https://mydomain.com` returns 200, browser shows green padlock, `systemctl status caddy` shows `active (running)`.
9. **References to methodologies that haven't been written yet.** The validator catches this; do not paper over with `(forthcoming)` notes.
10. **Cross-tier slug collision.** Two playbooks with the same slug in different tiers. Pre-check with `find skills/faion/playbooks -name playbook.md` before reserving a slug.
11. **Surface-specific content.** Deploy script paths, frontend-only build commands, backend-only DB schemas. That's a workflow playbook, not a tier playbook.
12. **Overlong body.** `playbook.md` >5k tokens. Split into a parent + companion `examples.md`/`templates.md`.

## 9. Inline minimal template

```markdown
---
name: buy-domain-namecheap
description: Buy a domain on Namecheap and point it at Cloudflare DNS.
tier: free
group: tech-setup
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will own a registered domain and have it managed by Cloudflare DNS, ready for any web service to point at.

## Prerequisites

- A Namecheap account (free signup).
- A Cloudflare account (free signup; see `cloudflare-account-bootstrap`).
- A budget of $8–15/year for the domain itself.

## Steps

1. Sign in at https://www.namecheap.com.
2. Search the domain you want in the search bar.
3. Pick the cheapest available `.com` (or `.net`/`.io` if you accept the surcharge).
4. Add to cart, skip every upsell, check out.
5. In the order confirmation, click "Manage" on the new domain.
6. Under "Nameservers", choose "Custom DNS" and enter the two Cloudflare nameservers from your Cloudflare dashboard (e.g., `dana.ns.cloudflare.com`, `bob.ns.cloudflare.com`).
7. Wait 5–60 minutes for propagation.

## Verify

```
dig +short NS mydomain.com
```

Returns the two Cloudflare nameservers. If it still returns `dns1.registrar-servers.com`, propagation is incomplete — wait longer.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `dig` still shows Namecheap nameservers after 1h | NS change not saved | Re-open Namecheap → Domain List → Manage → Nameservers; verify Custom DNS values |
| Cloudflare shows "pending" for ≥24h | Wrong nameservers | Copy nameservers from Cloudflare dashboard exactly (case-insensitive but spelling matters) |
| Domain costs $40+ | Premium domain | Pick a different name; premiums are not worth it for a side project |

## Next

- `cloudflare-dns-zones` — set up A / CNAME records for your services.
- `https-everywhere-cloudflare` — enable Full (Strict) SSL.

## References

- [knowledge/free/dev/devtools-developer/dns-fundamentals](../../../knowledge/free/dev/devtools-developer/dns-fundamentals) — explains why nameservers must propagate before any DNS query resolves; this playbook waits on exactly that propagation.
- [knowledge/free/dev/devtools-developer/domain-registration-cost](../../../knowledge/free/dev/devtools-developer/domain-registration-cost) — pricing tiers for `.com`/`.net`/`.io`; backs the "skip premium" Step 3.
```

## 10. Authoring checklist (8-item)

Before commit:

- [ ] Slug matches folder name and front-matter `name`.
- [ ] All 8 front-matter keys filled with valid values.
- [ ] All 7 H2 sections present in fixed order.
- [ ] ≥1 methodology citation; tier ≤ playbook tier; rationale playbook-specific.
- [ ] Steps use real commands/URLs/values (no `foo`/`bar`/`example.com`).
- [ ] Verify section runnable as one observable check.
- [ ] Troubleshooting has ≥1 named pitfall.
- [ ] `python3 scripts/validate-tier-playbook.py <path>` exits 0.
