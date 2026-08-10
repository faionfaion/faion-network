# Visual Automation Tools
**Layer:** 3 — Orchestration · **Verified:** 2026-08-03

The decisive question for every tool below: **can it actually shell out to run a local `faion` CLI binary on the user's machine?** That determines whether a non-technical solopreneur has any visual on-ramp to a Go CLI product at all — none of these tools can embed Go code, so the only paths in are (a) an exec/shell node, or (b) a webhook/HTTP bridge to a locally-running process that itself wraps the binary.

**The honest boundary, assessed:** per the user's landscape doc, a visual automation tool like n8n is needed only when something must fire **without the user present** — a night-time event, a schedule, an external webhook arriving while the machine is unattended. If everything runs with the user present, their own coding-agent's hooks and scheduler (cron, Claude Code hooks, the `loop`/`schedule` skills already in this environment) already cover it — a visual tool adds a second orchestration surface for no benefit. **This assessment holds.** The one qualifier: a visual tool's exec/shell node is only useful for a *solopreneur* on-ramp if it can call `faion` — and as the findings below show, three of four cannot, which means for most solopreneurs "n8n as an on-ramp to faion" is not actually available; the honest recommendation narrows to "n8n, self-hosted, Execute Command re-enabled" as the only same-process path, with everything else requiring either an enterprise plan or a local bridge process that reintroduces the "always running" burden the visual tool was supposed to remove.

---

# n8n
**Layer:** 3 — Orchestration · **Verdict:** 🟡 take the idea, not the tool · **Verified:** 2026-08-03

## What it is
Open-source, node-based visual workflow automation tool; self-hostable or cloud-hosted, with an "Execute Command" node that can run arbitrary shell commands when self-hosted.

## Current state
- Valuation **doubled to $5.2B on a ~$60M SAP strategic investment, announced 2026-05-12** (up from a prior $2.5B valuation); SAP plans to embed n8n's canvas into Joule Studio by Q3 2026. Sources: Bloomberg and Tech.eu, both dated 2026-05-12, checked 2026-08-03.
- Self-hosted deployment is free/open-source (fair-code / Sustainable Use License).
- **Execute Command node is disabled by default since v2.0 for security**; the official docs state verbatim: *"This node isn't available on n8n Cloud."* Confirmed via docs.n8n.io, checked 2026-08-03.
- Re-enabling it self-hosted requires explicit node-allow configuration — but this is a live pain point: **GitHub issue #23439** ("Unable to re-enable Execute Command node in n8n 2.0") shows some self-hosters cannot get it back even after setting the documented config, as of the issue's last activity.

## Mechanics
Execute Command node runs a literal shell command string against the n8n host's shell, with stdin/stdout wired into the workflow's data flow — the closest thing to a general-purpose exec primitive among all four tools evaluated here.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Bloomberg: SAP invests in n8n at $5.2B | https://www.bloomberg.com/news/articles/2026-05-12/sap-invests-in-ai-automation-startup-n8n-at-5-2-billion-value | Valuation, SAP investment terms | 2026-08-03 |
| 2 | Tech.eu: n8n valuation doubles | https://tech.eu/2026/05/12/n8n-s-valuation-doubles-to-5-2bn-following-sap-strategic-investment/ | Same, second source | 2026-08-03 |
| 3 | n8n docs: Execute Command node | https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executecommand | Cloud restriction stated verbatim | 2026-08-03 |
| 4 | GitHub n8n-io/n8n#23439 | https://github.com/n8n-io/n8n/issues/23439 | Re-enable config pain point, self-hosted only | 2026-08-03 |

## What to borrow for faion
Nothing structural to embed — but n8n IS the one tool in this set that offers a real same-process on-ramp: a self-hosted n8n instance with Execute Command re-enabled can literally run `faion search ...` / `faion get-content ...` as a node and route the output into whatever downstream automation (a Telegram post, a scheduled digest, a webhook reply) the user is building. Worth a companion how-to guide/playbook if we ever want to court the "scheduled/unattended automation" segment of solopreneur users.

## What NOT to borrow — and why
n8n Cloud (the easiest on-ramp for a genuinely non-technical user) explicitly blocks this — so the "visual on-ramp for non-technical users" story only works for a self-hosting user, who is by definition not fully non-technical. Don't oversell this as a no-code path; it is a low-code path gated behind self-hosting + a config re-enable that itself has an open bug.

## Mapping to our corpus
`faion-network/skills/faion/knowledge/automation-tooling/` currently covers Playwright/Puppeteer/pnpm/backend-language scaffolds — no n8n-specific methodology exists. If we build the "faion as an n8n node" playbook, it belongs in `automation-tooling` or a new `sdlc-ai` entry adjacent to `faion-cli-agent-adapter-pattern`.

## Open questions / staleness risk
Whether GitHub #23439's re-enable bug has since been fixed was not re-checked against the issue's current (possibly closed) status — verify before publishing a how-to guide that assumes re-enabling works cleanly.

---

# Make (formerly Integromat) / Maia
**Layer:** 3 — Orchestration · **Verdict:** 🔴 skip · **Verified:** 2026-08-03

## What it is
Cloud-only visual automation SaaS; Maia is Make's agentic/AI-agent feature layered on top of the existing scenario-builder.

## Current state
- **Maia: open beta since 2026-02-02** confirmed as **still closed/limited beta for paid plans as of the current help-center wording**, with GA date unannounced ("later in 2026") and a waitlist still required as of the most recent check (help.make.com, checked 2026-08-03).
- Make has **no self-host option** for the core platform, ever (it is a pure SaaS product).
- Make DOES ship an **"On-Premise Agent"** (Java, run via `java -jar agent.jar`), but it is **Enterprise-plan only** and its sole shipped module is the **HTTP Agent app** — described in Make's own docs as "an http agent that allows for a connection with other custom systems that provide an api or a web service." No shell/exec/local-binary-call capability is documented anywhere in this bridge. Source: help.make.com/on-premise-agent, checked 2026-08-03.

## Mechanics
Scenario-based visual builder (modules chained left-to-right); Maia agents sit as an AI-decision layer inside a scenario, priced per-run at roughly 43-50 operations/credits.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Make: Introduction to Maia | https://help.make.com/introduction-to-maia-by-make | Beta status, credit cost, pricing tier gating | 2026-08-03 |
| 2 | Make: On-Premise Agent docs | https://help.make.com/on-premise-agent | Java agent, Enterprise-only, HTTP Agent module only | 2026-08-03 |

## What to borrow for faion
Nothing. No exec path exists at any plan tier reachable by a solopreneur budget.

## What NOT to borrow — and why
**CANNOT shell out directly; the only workaround (Enterprise-only On-Premise Agent → HTTP Agent module → a self-run local HTTP server wrapping `faion`) is not a fit for a solopreneur budget or a non-technical user** — it requires both an Enterprise Make subscription and standing up your own local server process, which reintroduces the "must be running/present" burden the visual tool was meant to remove.

## Mapping to our corpus
No adoption path; do not recommend Make in any faion onboarding material as an automation on-ramp.

## Open questions / staleness risk
Maia's GA date is genuinely unannounced — re-check before any future dossier revision; "later in 2026" could land any time and change the calculus (though the exec-capability gap would remain regardless of Maia's beta/GA status, since that gap is about the platform's SaaS-only architecture, not about Maia specifically).

---

# Dify
**Layer:** 3 — Orchestration · **Verdict:** 🔴 skip · **Verified:** 2026-08-03

## What it is
Open-source LLM app-building platform (workflow builder + agent framework + RAG pipeline), self-hostable, with a "Code" node for inline Python/Node execution.

## Current state
- Latest self-hosted version at last check: **1.14.2 (2026-05-19)**, with image tags observed moving toward **1.16.1** — the prior research pass's "1.15.0 (2026-06-25)" is in the right neighborhood but likely superseded; **re-verify the exact current tag before publishing**, this pass could not pin it precisely (source: GitHub releases, checked 2026-08-03).
- Self-hosting is fully supported; the community edition has "no meaningful feature limitations" versus the cloud tier.

## Mechanics
- Code nodes execute inside **dify-sandbox**, a seccomp-based runc container restricting syscalls via an explicit whitelist. **Confirmed: this blocks all exec/subprocess calls** — 2026 security research (Imperva coverage, Security Boulevard; and GitHub issue #38105) documents the sandbox model in detail, including whitelist bugs that cause ~0.1% nondeterministic Code-node failures. The existence of a syscall whitelist at all is itself confirmation that a working exec path is not exposed — a permissive sandbox wouldn't need one.
- **The sandbox restriction applies identically whether self-hosted or cloud** — it is a property of the Code-node container, not the deployment target. No documented allowlist mechanism exists to mount or permit an arbitrary external binary from inside the sandbox, even for a self-hosting operator with full server access.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Dify GitHub releases | https://github.com/langgenius/dify/releases | Version history (1.14.2, moving to 1.16.1) | 2026-08-03 |
| 2 | Imperva / Security Boulevard coverage of dify-sandbox | (2026 security research, exact URL not retained by fork) | Seccomp/whitelist model confirmed | 2026-08-03 |
| 3 | GitHub langgenius/dify#38105 | github.com/langgenius/dify (issue #38105) | Whitelist bugs causing nondeterministic Code-node failures | 2026-08-03 |

## What to borrow for faion
Nothing — even self-hosting doesn't open a path.

## What NOT to borrow — and why
**CANNOT shell out directly, no workaround even self-hosted** — the seccomp whitelist is baked into the sandbox container regardless of who operates the server. This is the most closed of the four tools evaluated.

## Mapping to our corpus
No adoption path.

## Open questions / staleness risk
Exact current version not pinned this pass (1.14.2 vs 1.16.1 vs the prior pass's 1.15.0) — do not cite a specific version number in customer-facing material without a fresh check. The sandbox-blocks-exec conclusion itself is well-corroborated from multiple independent sources and is low staleness-risk.

---

# Flowise
**Layer:** 3 — Orchestration · **Verdict:** 🟡 take the idea, not the tool (technical users only) · **Verified:** 2026-08-03

## What it is
Self-hostable, Node.js-based visual LangChain-flow builder aimed at developers, not non-technical users (self-admittedly, per the prior research pass).

## Current state
- **Acquired by Workday, announced 2025-08-14**, terms undisclosed (source: Workday newsroom, checked 2026-08-03).
- Self-hostable, Node.js/TypeScript codebase.

## Mechanics
- **Custom Function node**: runs in a restricted VM sandbox. `require('child_process')` fails with "Cannot find module" — only allowlisted built-in/external modules work, controlled via the `TOOL_FUNCTION_EXTERNAL_DEP` env var. **This node CANNOT shell out.**
- **Custom Tool node**: distinct from Custom Function. Documentation and community sources describe it as running "in Flowise's server process, NOT sandboxed" — full JS access, unlike Custom Function's VM isolation. Since Flowise is self-hosted Node.js, a Custom Tool could plausibly `require('child_process')` and shell out to a local `faion` binary. **However, no source was found this pass explicitly confirming `child_process` works inside Custom Tool specifically** (only that it's unsandboxed, in contrast to Custom Function which is explicitly sandboxed and blocks it). **Treat as likely-but-unconfirmed — verify directly in a running Flowise instance before stating it as fact.**

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Workday newsroom: Workday Acquires Flowise | https://newsroom.workday.com/2025-08-14-Workday-Acquires-Flowise,-Bringing-Powerful-AI-Agent-Builder-Capabilities-to-the-Workday-Platform | Acquisition date confirmed, terms undisclosed | 2026-08-03 |
| 2 | Flowise Custom Function / Custom Tool docs + community | (Flowise docs/GitHub, exact URL not retained by fork) | Sandboxing distinction between the two node types | 2026-08-03 |

## What to borrow for faion
If the Custom Tool `child_process` path is confirmed in a follow-up direct test, Flowise becomes a second same-process on-ramp alongside self-hosted n8n — worth testing directly (spin up a local Flowise instance, add a Custom Tool node, attempt `child_process.execSync('faion --version')`) before committing to a recommendation either way.

## What NOT to borrow — and why
Flowise is explicitly dev-facing (LangChain-flow builder), not a non-technical on-ramp regardless of exec capability — its target user already has the technical background to just call the CLI directly, which reduces the value of routing through a visual layer at all for THIS specific persona (non-technical solopreneur).

## Mapping to our corpus
No current adoption; flag as a follow-up verification task (direct hands-on test of Custom Tool + child_process) before any customer-facing claim.

## Open questions / staleness risk
The Custom Tool exec capability is the single least-verified claim across both tool dossiers in this research pass — explicitly unconfirmed, needs a direct test, not just doc reading, before it's asserted as fact anywhere customer-facing.
