# All 400 Playbook Ideas (Catalog)

Full output of 4-tier multi-persona brainstorm. 100 ideas per tier × 4 tiers = 400 candidates. Top 30 per tier marked TIER-1 (implementation queue, see `priority-120.md`); remaining 70 per tier are TIER-2 (deferred to future feature).

Format columns: # | Slug | Title | Problem | Solution outline | Impact | Effort | Persona | Group

Persona keys are tier-specific — see each tier section header.

---

## Free Tier (100)

**Audience:** aspiring solopreneurs, complete beginners, returning developers, side-hustlers.
**Citation scope:** `knowledge/free/` only.
**Personas:** A=first-time founder, B=returning developer, C=marketer-turned-builder, D=side-hustler.

### TIER-1 (Top 30, implementation queue)

| # | Slug | Title | Problem | Solution outline | Impact | Effort | Persona | Group |
|---|------|-------|---------|------------------|--------|--------|---------|-------|
| 1 | github-account-and-first-repo | Create your first GitHub repository | Beginners have no place to store or share code | Sign up → verify email → create repo → add README → first commit | H | S | A,B,C,D | tech-setup |
| 2 | ssh-key-setup-github | Connect your machine to GitHub with SSH | Password prompts block every push; HTTPS breaks on 2FA | Generate ed25519 → copy public key → add to GitHub → test `ssh -T git@github.com` | H | S | A,B,D | tech-setup |
| 3 | git-daily-workflow | The 5-command git workflow for daily coding | Beginners commit rarely, lose work, fear branches | `status → add → commit → pull → push` loop; meaningful messages; when to branch | H | S | A,B,C,D | tech-setup |
| 4 | vscode-first-project-setup | Set up VS Code for your first project | Blank editor overwhelming; wrong extensions slow you down | Install VS Code → must-have extensions → open folder → integrated terminal | H | S | A,C,D | tech-setup |
| 5 | buy-domain-namecheap-cloudflare | Buy a domain and point it to Cloudflare | Beginners overpay on registrars, skip DNS best practices | Search domain on Namecheap → purchase → change nameservers to Cloudflare → verify propagation | H | S | A,B,C,D | hosting-infra |
| 6 | deploy-static-site-github-pages | Publish your first website free on GitHub Pages | Built something but can't show it | Enable Pages → push HTML → custom domain optional → live in 60 seconds | H | S | A,C,D | hosting-infra |
| 7 | deploy-to-vercel-free | Ship a frontend project to Vercel in 5 minutes | Developers build locally but never deploy | Connect repo → auto-detect framework → env vars → preview URL on every push | H | S | B,C,D | hosting-infra |
| 8 | cloudflare-dns-free-ssl | Point your domain and get free SSL on Cloudflare | "HTTPS is complicated and expensive" misconception | Add domain → A/CNAME records → SSL/TLS flexible → verify green lock | H | S | A,B,C,D | hosting-infra |
| 9 | python-first-project | Write and run your first Python script | "I've read tutorials but never shipped anything real" | Install Python → venv → CLI tool (word counter / URL checker) → run | H | S | A,B,D | dev-fundamentals |
| 10 | javascript-first-project | Build your first JavaScript project that runs in a browser | JS learners get stuck in tutorials | Plain HTML → `<script>` → fetch public API → display data → no build tool | H | S | A,C,D | dev-fundamentals |
| 11 | dotenv-secrets-management | Keep secrets out of your code with .env files | Beginners hardcode API keys, leak on GitHub | python-dotenv → `.env` file → `.gitignore` → load in code → checklist | H | S | A,B,D | dev-fundamentals |
| 12 | mom-test-customer-interview | Run a Mom Test customer interview | Founders get false validation from polite feedback | 5 neutral questions → past behavior not opinions → record insights → iterate | H | M | A,B,C | business-discovery |
| 13 | idea-validation-landing-page | Validate your idea with a landing page before building | Building for weeks before knowing if anyone cares | 1-page HTML → headline → email signup → share 3 places → measure | H | M | A,C,D | business-discovery |
| 14 | niche-selection-framework | Pick a niche you can actually win in | Too-broad ideas never get traction | Audience × problem × WTP matrix → 3 filters: access, credibility, monetizability | H | M | A,B,C,D | business-discovery |
| 15 | mvp-scope-cutting | Cut your MVP to the smallest shippable thing | Feature creep kills solo projects before launch | Full feature list → "delete it" test → keep only core loop → define done | H | S | A,B,C,D | mvp-essentials |
| 16 | ugly-first-version | Ship an ugly first version on purpose | Perfectionism prevents launch | Define "good enough to learn" → ship with known flaws → 3 real users → iterate | H | S | A,B,C,D | mvp-essentials |
| 17 | mvp-launch-checklist | Pre-launch checklist for your MVP | Forgetting critical steps (404 page, analytics, contact email) | 20-item checklist: error pages, analytics, contact, mobile test, share on 3 channels | H | S | A,B,C,D | mvp-essentials |
| 18 | python-package-manager | Manage Python dependencies without chaos | Global pip breaks projects; version conflicts | pip + venv → requirements.txt → optional uv → pin versions | H | S | B,D | dev-fundamentals |
| 19 | first-10-customers | How to find your first 10 customers manually | No audience, no product, no idea where to start | Warm network DM → community post → cold email; track in spreadsheet | H | M | A,C,D | marketing-fundamentals |
| 20 | landing-page-essentials | Write a landing page that converts | "My landing page gets visits but zero signups" | Hero formula → 3 benefits → 1 CTA → social proof → above-the-fold | H | M | A,B,C,D | marketing-fundamentals |
| 21 | git-branching-basics | Use branches so you never break working code | Beginners commit directly to main, break things | `git checkout -b` → work → PR → merge → delete; keep main green | H | S | A,B,D | tech-setup |
| 22 | free-analytics-posthog | Add free product analytics with PostHog | "I have users but no idea what they do" | PostHog free → JS snippet → page views + custom events → session replay | H | S | B,C,D | cost-free-stack |
| 23 | free-auth-supabase | Add user login to your app for free | Auth from scratch takes weeks; paid services cost money | Supabase free → email auth → JS client → protected route → magic link | H | M | B,D | cost-free-stack |
| 24 | positioning-basics | Position your product so strangers understand it in 5s | Founders describe features, not benefits | Geoffrey Moore template → "For [who] who [problem], [product] is a [category] that [benefit]" | H | M | A,B,C,D | marketing-fundamentals |
| 25 | write-good-readme | Write a README that gets your repo noticed | Repos with no README get ignored | What it does → who it's for → quick start → screenshot → contributing | H | S | A,B,C | dev-fundamentals |
| 26 | testing-intro-python | Write your first automated test in Python | "I test by running it manually every time" | pytest install → first test file → assert basics → pytest-watch → CI teaser | H | S | B,D | dev-fundamentals |
| 27 | is-this-a-real-problem | Validate that a problem is real before building | Founders solve problems that only they have | Search volume + community complaints + paid competitors → score sheet | H | M | A,B,C,D | business-discovery |
| 28 | wise-account-for-solos | Open a Wise account to get paid internationally | Solos don't know how to receive money from foreign clients | Wise personal → USD/EUR virtual IBANs → share with client → local currency | H | S | A,D | ops-basics |
| 29 | free-email-with-cloudflare | Get a professional email address for free | Using personal Gmail looks unprofessional | Cloudflare Email Routing → forward `hello@yourdomain.com` → reply from Gmail | H | S | A,C,D | cost-free-stack |
| 30 | code-style-and-prettier | Auto-format code so it always looks professional | Inconsistent code style slows reviews and embarrasses beginners | Prettier → `.prettierrc` → format-on-save → pre-commit hook | H | S | A,B,D | dev-fundamentals |

### TIER-2 (Remaining 70, catalog only)

| # | Slug | Title | Group | Impact | Effort |
|---|------|-------|-------|--------|--------|
| 31 | terminal-basics-for-beginners | Terminal survival guide for absolute beginners | tech-setup | H | S |
| 32 | pr-review-workflow | Submit and review a pull request step by step | tech-setup | H | M |
| 33 | git-undo-mistakes | Fix common git mistakes without losing work | tech-setup | H | M |
| 34 | gitignore-setup | Create a .gitignore that actually works | tech-setup | H | S |
| 35 | github-profile-readme | Build a GitHub profile that impresses employers | tech-setup | M | S |
| 36 | github-actions-basic-ci | Run your tests automatically on every push | tech-setup | H | M |
| 37 | deploy-to-netlify-free | Deploy a Jamstack site to Netlify for free | hosting-infra | M | S |
| 38 | basic-nginx-config | Serve your app with nginx on a free VPS | hosting-infra | M | M |
| 39 | oracle-free-vps-setup | Get a forever-free VPS from Oracle Cloud | hosting-infra | M | M |
| 40 | letsencrypt-certbot | Add HTTPS to any server with Let's Encrypt | hosting-infra | H | S |
| 41 | cloudflare-pages-deploy | Deploy frontend to Cloudflare Pages for free | hosting-infra | M | S |
| 42 | subdomain-routing-cloudflare | Set up subdomains for different projects | hosting-infra | M | S |
| 43 | free-database-supabase | Get a free hosted Postgres database | hosting-infra | H | M |
| 44 | python-debugging-basics | Debug Python code without print statements | dev-fundamentals | H | M |
| 45 | javascript-debugging-browser | Debug JS in the browser DevTools | dev-fundamentals | H | M |
| 46 | package-json-explained | Understand package.json before you touch it | dev-fundamentals | M | S |
| 47 | virtual-environments-python | Isolate Python projects with virtual environments | dev-fundamentals | H | S |
| 48 | fetch-api-javascript | Call a public API from JavaScript | dev-fundamentals | H | M |
| 49 | python-http-requests | Call APIs from Python with requests library | dev-fundamentals | H | S |
| 50 | code-review-for-solo-devs | Review your own code like a second developer | dev-fundamentals | M | S |
| 51 | basic-html-css-landing | Build a landing page with raw HTML and CSS | dev-fundamentals | H | M |
| 52 | python-cli-argparse | Build a useful CLI tool with argparse | dev-fundamentals | M | S |
| 53 | find-solo-business-idea | Generate 10 business ideas you could actually build | business-discovery | H | M |
| 54 | market-size-basics | Estimate if a market is big enough to matter | business-discovery | M | M |
| 55 | competitor-research-free | Analyze competitors with free tools only | business-discovery | H | M |
| 56 | willingness-to-pay-test | Test if people will pay before you build | business-discovery | H | M |
| 57 | problem-statement-writing | Write a 1-sentence problem statement | business-discovery | M | S |
| 58 | basic-market-research-reddit | Use Reddit to validate ideas for free | business-discovery | H | S |
| 59 | customer-persona-simple | Build a 1-page customer persona without surveys | business-discovery | M | S |
| 60 | early-adopter-definition | Define who your early adopter actually is | business-discovery | H | S |
| 61 | soft-launch-strategy | Do a soft launch to 10 people before going public | mvp-essentials | H | M |
| 62 | mvp-definition-framework | Define what counts as your MVP | mvp-essentials | H | S |
| 63 | feedback-collection-typeform | Collect product feedback for free with Typeform | mvp-essentials | M | S |
| 64 | error-page-setup | Add proper 404 and 500 error pages | mvp-essentials | M | S |
| 65 | mobile-responsive-basics | Make your MVP work on mobile | mvp-essentials | H | M |
| 66 | free-email-marketing-mailchimp | Send your first email campaign for free | marketing-fundamentals | H | M |
| 67 | twitter-x-starter-for-builders | Use Twitter/X to build in public as a beginner | marketing-fundamentals | M | M |
| 68 | producthunt-prep-launch | Prepare a Product Hunt launch on the free tier | marketing-fundamentals | M | M |
| 69 | seo-basics-for-mvps | Get your first Google traffic with basic SEO | marketing-fundamentals | M | M |
| 70 | social-proof-from-nothing | Add social proof when you have zero users | marketing-fundamentals | M | S |
| 71 | cold-email-first-outreach | Write a cold email that gets replies | marketing-fundamentals | H | M |
| 72 | free-transactional-email | Send transactional emails free with Resend | cost-free-stack | M | M |
| 73 | free-file-storage-cloudflare-r2 | Store files for free with Cloudflare R2 | cost-free-stack | M | M |
| 74 | free-form-handling | Accept form submissions without a backend | cost-free-stack | M | S |
| 75 | free-monitoring-uptime-kuma | Monitor your site uptime for free | cost-free-stack | M | M |
| 76 | free-search-algolia | Add fast search to your site for free | cost-free-stack | M | M |
| 77 | free-cdn-for-images | Serve images fast without paying for CDN | cost-free-stack | M | S |
| 78 | invoicing-first-client | Send your first invoice and get paid | ops-basics | H | S |
| 79 | freelance-contract-basics | Protect yourself with a simple freelance contract | ops-basics | H | M |
| 80 | mercury-bank-for-founders | Open a Mercury bank account for US-based clients | ops-basics | M | M |
| 81 | gdpr-basics-for-mvps | Add a privacy policy and cookie notice cheaply | ops-basics | M | M |
| 82 | stripe-first-payment | Accept your first payment with Stripe | ops-basics | H | M |
| 83 | project-folder-structure | Organize your project files from day one | dev-fundamentals | M | S |
| 84 | environment-variables-explained | Understand environment variables completely | dev-fundamentals | M | S |
| 85 | json-for-beginners | Read and write JSON without confusion | dev-fundamentals | M | S |
| 86 | http-basics-for-builders | Understand HTTP so APIs make sense | dev-fundamentals | H | M |
| 87 | python-virtual-env-uv | Speed up Python setup with uv | dev-fundamentals | M | S |
| 88 | javascript-modules-esm | Use ES modules without confusion | dev-fundamentals | M | M |
| 89 | css-flexbox-cheatsheet | Master flexbox in one playbook | dev-fundamentals | M | S |
| 90 | markdown-for-developers | Write markdown that renders everywhere | dev-fundamentals | M | S |
| 91 | problem-worth-solving-filter | Apply a 5-question filter to any startup idea | business-discovery | H | S |
| 92 | google-trends-for-ideas | Use Google Trends to validate idea timing | business-discovery | M | S |
| 93 | productboard-free-alternative | Track feature requests without paying for tools | mvp-essentials | M | S |
| 94 | launch-on-reddit | Launch your project on Reddit and get real feedback | marketing-fundamentals | M | M |
| 95 | build-in-public-twitter | Document your build in public from day 1 | marketing-fundamentals | M | M |
| 96 | waitlist-page-in-one-hour | Build and launch a waitlist page in one hour | mvp-essentials | H | S |
| 97 | hacker-news-show-hn | Post a Show HN and survive it | marketing-fundamentals | M | M |
| 98 | one-page-business-plan | Write a 1-page business plan in 30 minutes | business-discovery | M | S |
| 99 | tax-basics-for-freelancers | Understand taxes before your first invoice | ops-basics | M | M |
| 100 | yearly-free-tier-audit | Audit your free-tier services before they expire | ops-basics | M | S |

---

## Solo Tier (100)

**Audience:** indie hackers, freelancers, niche product founders, content creators monetizing.
**Citation scope:** `knowledge/free/ + solo/`.
**Personas:** A=indie hacker, B=freelancer, C=niche product founder, D=content creator.

### TIER-1 (Top 30)

See `priority-120.md` § Wave 2.

### TIER-2 (Remaining 70)

| # | Slug | Title | Group | Impact | Effort |
|---|------|-------|-------|--------|--------|
| 31 | design-md-writing | Writing design.md: Architecture Decisions Before You Code | sdd-workflow | H | S |
| 32 | impl-plan-breakdown | Implementation Plan: Task Breakdown for One Developer | sdd-workflow | M | S |
| 33 | test-plan-solo | Test Plan for Solos: What to Test When You're the QA | sdd-workflow | M | S |
| 34 | sdd-scope-guard | SDD Scope Guard: Detect Scope Creep in Your Own Specs | sdd-workflow | M | S |
| 35 | sdd-backlog-lifecycle | SDD Backlog Lifecycle: backlog → todo → in-progress → done | sdd-workflow | M | S |
| 36 | sdd-feature-review | SDD Feature Review: Closing a Feature Without Regret | sdd-workflow | M | S |
| 37 | sdd-constitution-setup | SDD Constitution: Setting Your Tech Standards Once | sdd-workflow | L | S |
| 38 | sdd-planning-rhythm | SDD Planning Rhythm: Weekly + Monthly Cadence Solo | sdd-workflow | M | S |
| 39 | tailwind-essentials | Tailwind Essentials for Shipping: Not a Design Course | frontend-launch | H | S |
| 40 | og-images | OG Images: Social Preview That Drives Clicks | frontend-launch | M | S |
| 41 | performance-budget | Performance Budget: Ship Fast Pages Without a Build Team | frontend-launch | M | M |
| 42 | accessibility-quick-wins | Accessibility Quick Wins: WCAG Basics That Protect and Convert | frontend-launch | M | S |
| 43 | design-system-minimal | Minimal Design System: Component Library for One Dev | frontend-launch | M | M |
| 44 | dark-mode-toggle | Dark Mode Toggle: Ship It Right Without Flicker | frontend-launch | L | S |
| 45 | mobile-first-layout | Mobile-First Layout: Landing Pages That Convert on Phone | frontend-launch | M | S |
| 46 | cookie-consent | Cookie Consent: GDPR-Compliant Without Killing UX | frontend-launch | M | S |
| 47 | error-design | Error States: Design 404, 500, and Empty States Properly | frontend-launch | M | S |
| 48 | pagination-api | Pagination: Cursor vs Offset for Small APIs | api-design | M | S |
| 49 | api-error-responses | API Error Responses: Consistent Format Clients Can Handle | api-design | M | S |
| 50 | rate-limiting-basics | Rate Limiting Basics: Protect Your API Without Complexity | api-design | M | S |
| 51 | openapi-spec | OpenAPI Spec: One-File Contract for Your API | api-design | M | M |
| 52 | webhook-design | Webhook Design: Outbound Events Stripe-Style | api-design | M | M |
| 53 | versioning-api | API Versioning: When and How to Break Compatibility | api-design | L | S |
| 54 | auth-session-vs-jwt | Session vs JWT: Choose Once, Commit | api-design | M | S |
| 55 | cors-config | CORS Config: Unblock Your Frontend Without Opening Everything | api-design | M | S |
| 56 | systemd-unit | systemd Unit: Keep Your Process Running After Reboot | server-craft | H | S |
| 57 | basic-backup | Basic Backup: Automate DB + Files Before You Need It | server-craft | H | S |
| 58 | fail2ban-setup | fail2ban Setup: Block Bots Before They Exhaust Your Server | server-craft | M | S |
| 59 | log-management | Log Management: Find Errors Without Drowning in Output | server-craft | M | S |
| 60 | postgres-first-setup | Postgres First Setup: VPS Database That Won't Bite You | server-craft | M | M |
| 61 | docker-solo | Docker for Solos: One Container, One Product, Ship It | server-craft | M | M |
| 62 | server-hardening | Server Hardening Checklist: 10 Steps Before Going Public | server-craft | M | S |
| 63 | uptime-monitoring | Uptime Monitoring: Know Before Your Users Do | server-craft | M | S |
| 64 | deploy-script | Deploy Script: Push-to-Deploy Without a Platform Fee | automation | H | S |
| 65 | github-actions-testing | GitHub Actions: Run Tests on Every PR | automation | M | S |
| 66 | release-tagging | Release Tagging: Versioning and Changelogs That Ship | automation | L | S |
| 67 | dependency-updates | Dependency Updates: Dependabot Without the Noise | automation | L | S |
| 68 | staging-environment | Staging Environment: Test Before Production | automation | M | M |
| 69 | okrs-solo-style | OKRs Solo-Style: Quarterly Goals for One Founder | product-planning | M | S |
| 70 | what-to-build-next | What to Build Next: Decision Framework for Solos | product-planning | H | S |
| 71 | feature-flags-solo | Feature Flags for Solos: Ship Hidden Until Ready | product-planning | M | M |
| 72 | user-research-solo | User Research Solo: 5 Interviews Beat 500 Analytics | product-planning | M | S |
| 73 | cancelling-features | Cancelling Features: When to Kill What You Shipped | product-ops | M | S |
| 74 | churn-calc | Churn Calculation: MRR Math Every Solo SaaS Needs | product-ops | M | S |
| 75 | product-ops-monthly | Monthly Product Ops: What to Review When You're Alone | product-ops | M | S |
| 76 | free-trial-design | Free Trial Design: Length, Gates, and Conversion Logic | product-ops | M | S |
| 77 | button-form-basics | Buttons and Forms: The 20% That Drives 80% of UX | ui-design | H | S |
| 78 | typography-system | Typography System: Readable Hierarchy Without a Designer | ui-design | M | S |
| 79 | color-system | Color System: Brand Palette That Works Across UI | ui-design | M | S |
| 80 | visual-hierarchy | Visual Hierarchy: Make Users Read What Matters | ui-design | M | S |
| 81 | form-validation-ux | Form Validation UX: Errors That Don't Frustrate | ui-design | M | S |
| 82 | spacing-system | Spacing System: Consistent Rhythm Without a Designer | ui-design | L | S |
| 83 | dark-mode-design | Dark Mode Design: Tokens and Contrast Done Right | ui-design | L | M |
| 84 | evergreen-content | Evergreen Content: Articles That Compound for Years | content-marketing | H | M |
| 85 | repurposing-content | Repurposing Content: One Idea, Five Formats, Zero Extra Work | content-marketing | M | S |
| 86 | first-100-subs | First 100 Subscribers: Manual Tactics That Actually Work | content-marketing | H | S |
| 87 | launch-post-anatomy | Launch Post Anatomy: HN/PH Post That Gets Traction | content-marketing | H | S |
| 88 | email-automation-drip | Email Drip Automation: Welcome Sequence Without an Agency | content-marketing | M | M |
| 89 | social-proof-collection | Social Proof Collection: Testimonials Without Begging | content-marketing | M | S |
| 90 | sitemap-setup | Sitemap Setup: Submit Once, Index Properly | seo-essentials | M | S |
| 91 | search-console-setup | Search Console Setup: Know What Google Sees | seo-essentials | H | S |
| 92 | internal-linking | Internal Linking: Distribute Authority Across Your Site | seo-essentials | M | S |
| 93 | schema-markup-basics | Schema Markup Basics: Rich Results Without a Plugin | seo-essentials | M | S |
| 94 | core-web-vitals | Core Web Vitals: Fix LCP and CLS Without a Build Team | seo-essentials | M | M |
| 95 | feedback-handling | Feedback Handling: Separate Signal from Noise | comms-stakeholder | M | S |
| 96 | mom-test-advanced | Mom Test Advanced: Validate Willingness to Pay | comms-stakeholder | H | S |
| 97 | refund-policy-writing | Refund Policy Writing: Clear Terms That Reduce Disputes | comms-stakeholder | M | S |
| 98 | customer-support-templates | Customer Support Templates: Handle Edge Cases in One Reply | comms-stakeholder | M | S |
| 99 | invoicing-system | Invoicing System: Solo Billing Without an Accountant | solo-ops-finance | M | S |
| 100 | taxes-indie | Taxes for Indie Founders: What to Track From Day One | solo-ops-finance | M | S |

---

## Pro Tier (100)

**Audience:** agency owners, senior contractors, growing team leads, growth marketers.
**Citation scope:** `knowledge/free/ + solo/ + pro/`.
**Personas:** A=agency owner, B=senior contractor, C=growing team lead, D=growth marketer / PPC manager.

### TIER-1 (Top 30)

See `priority-120.md` § Wave 3.

### TIER-2 (Remaining 70)

| # | Slug | Title | Group | Persona |
|---|------|-------|-------|---------|
| 31 | kickoff-process | Client Kickoff: Agenda, Assets, Alignment | client-engagement | A |
| 32 | contract-template | Agency Contract Template: MSA + SOW + NDA | client-engagement | B |
| 33 | terminating-client | How to Fire a Client (and Keep Your Reputation) | client-engagement | B |
| 34 | change-order-workflow | Change Order Workflow: Request to Approval | client-engagement | A |
| 35 | retainer-model | Selling and Running a Monthly Retainer | client-engagement | A |
| 36 | client-health-score | Client Health Score: Churn Signals + Escalation | client-engagement | A |
| 37 | retrospectives-agency | Retrospectives That Actually Change Something | delivery-ops | A |
| 38 | utilization-tracking | Utilization Tracking: Hours to Profit Margin | delivery-ops | A |
| 39 | time-tracking-culture | Time Tracking Without Killing Morale | delivery-ops | C |
| 40 | project-margin-analysis | Project Margin Analysis: Budget vs Actuals | delivery-ops | A |
| 41 | agile-vs-waterfall-choice | Agile vs Waterfall: Decision Framework for Client Work | delivery-ops | A |
| 42 | handoff-documentation | Project Handoff: Docs, Runbooks, Knowledge Transfer | delivery-ops | A |
| 43 | resource-allocation-matrix | Resource Allocation Matrix: Who Does What | delivery-ops | A |
| 44 | first-hire-designer | Hiring Your First Designer: Portfolio to Offer | team-management | C |
| 45 | first-hire-pm | Hiring Your First PM: Scorecard + Trial Project | team-management | C |
| 46 | performance-review-cycle | Performance Review Cycle: Template + Conversation | team-management | C |
| 47 | firing-with-dignity | Letting Someone Go: Legal, Humane, Clean | team-management | C |
| 48 | employer-brand-basics | Employer Brand on $0: Careers Page + Social | team-management | C |
| 49 | remote-team-rituals | Remote Team Rituals: Async-First Culture | team-management | C |
| 50 | compensation-bands | Compensation Bands: Set, Communicate, Update | team-management | C |
| 51 | requirements-gathering | Requirements Gathering: Workshops to Backlog | business-analysis | B |
| 52 | bpmn-basics | BPMN Process Mapping: Notation to Deliverable | business-analysis | B |
| 53 | data-modeling-basics | Data Modeling Basics: ERD + Naming Conventions | business-analysis | B |
| 54 | gap-analysis | Gap Analysis: Current State → Future State | business-analysis | B |
| 55 | ba-artifact-templates | BA Artifact Pack: BRD, FRD, Use Cases, RACI | business-analysis | B |
| 56 | use-case-writing | Use Case Writing: Actor, Flow, Edge Cases | business-analysis | B |
| 57 | prioritization-frameworks | Prioritization: RICE, MoSCoW, Kano at Team Scale | product-management | A |
| 58 | roadmap-for-teams | Roadmap for Teams: Now/Next/Later vs Gantt | product-management | A |
| 59 | customer-feedback-aggregation | Customer Feedback System: Collect → Triage → Act | product-management | A |
| 60 | beta-program | Beta Program: Recruit, Run, Close the Loop | product-management | A |
| 61 | feature-flag-strategy | Feature Flags: Ship Dark, Rollout Safely | product-management | A |
| 62 | k8s-intro | Kubernetes Intro: Pods, Services, Deployments | devops-cicd | A |
| 63 | secret-rotation | Secret Rotation: Vault, Env Parity, Audit Trail | devops-cicd | A |
| 64 | env-parity | Environment Parity: Dev → Staging → Prod | devops-cicd | A |
| 65 | incident-response-runbook | Incident Response Runbook: Detect → Resolve → Post-mortem | devops-cicd | A |
| 66 | monitoring-stack | Monitoring Stack: Prometheus + Grafana + Alerting | infra-engineering | A |
| 67 | log-aggregation | Log Aggregation: ELK/Loki for Production Teams | infra-engineering | A |
| 68 | alert-hygiene | Alert Hygiene: Cut Noise, Keep Signal | infra-engineering | A |
| 69 | multi-region-setup | Multi-Region Setup: Latency, Failover, Cost | infra-engineering | A |
| 70 | runbook-discipline | Runbook Discipline: Write, Test, Rotate | infra-engineering | A |
| 71 | cost-optimization-cloud | Cloud Cost Optimization: Right-size, Reserve, Prune | infra-engineering | A |
| 72 | queue-systems | Queue Systems: Celery, SQS, RabbitMQ Decision | backend-systems | A |
| 73 | async-tasks | Async Task Architecture: Workers, Retries, DLQ | backend-systems | A |
| 74 | graphql-vs-rest-at-scale | GraphQL vs REST at Scale: When to Switch | backend-systems | A |
| 75 | microservices-vs-monolith | Microservices vs Monolith: Decision Rubric | backend-systems | A |
| 76 | api-versioning-strategy | API Versioning: Semver, Headers, Deprecation | backend-systems | B |
| 77 | usability-testing | Usability Testing: Script, Sessions, Findings | ux-research | A |
| 78 | jtbd-framework | Jobs-to-Be-Done: Interview to Opportunity Map | ux-research | B |
| 79 | personas-creation | Persona Creation: Research-Backed, Not Fictional | ux-research | A |
| 80 | user-journey-mapping | User Journey Maps: Touchpoints to Friction Points | ux-research | A |
| 81 | ab-test-design | A/B Test Design: Hypothesis, Sample Size, Significance | ux-research | D |
| 82 | accessibility-audit-wcag | Accessibility Audit: WCAG 2.2 AA for Teams | ux-research | A |
| 83 | growth-experiments | Growth Experiment Framework: Backlog to Results | growth-marketing | D |
| 84 | referral-program | Referral Program: Mechanics, Incentives, Tracking | growth-marketing | D |
| 85 | viral-loops | Viral Loop Design: Identify, Instrument, Amplify | growth-marketing | D |
| 86 | retention-loops | Retention Loops: Habit Formation + Re-engagement | growth-marketing | D |
| 87 | cohort-analysis | Cohort Analysis: Build, Read, Act | growth-marketing | D |
| 88 | email-growth-playbook | Email Growth Playbook: List, Segment, Automate | growth-marketing | D |
| 89 | audience-research-paid | Audience Research for Paid: ICP → Targeting Map | paid-acquisition | D |
| 90 | retargeting-strategy | Retargeting Strategy: Funnels, Windows, Exclusions | paid-acquisition | D |
| 91 | creative-testing-framework | Creative Testing: Variables, Cadence, Kill Rules | paid-acquisition | D |
| 92 | social-calendar-agency | Social Calendar for Agencies: Plan, Batch, Publish | smm-cro | A |
| 93 | community-building | Community Building: Discord/Slack Flywheel | smm-cro | D |
| 94 | landing-page-testing | Landing Page Testing: Design → Hypothesis → Variant | smm-cro | D |
| 95 | funnel-cro | Full-Funnel CRO: Top to Bottom Optimization | smm-cro | D |
| 96 | tam-sam-som | TAM/SAM/SOM: Size Your Market for Investors + Strategy | market-research | B |
| 97 | pricing-research | Pricing Research: Surveys, Van Westendorp, Competitors | market-research | B |
| 98 | market-segmentation | Market Segmentation: Criteria, Clusters, Personas | market-research | B |
| 99 | ats-setup | ATS Setup: Tool Choice, Pipeline Config, Templates | hr-ops | C |
| 100 | offboarding-process | Offboarding: Knowledge Capture, Access, Alumni | hr-ops | C |

---

## Geek Tier (100)

**Audience:** AI agent engineers, RAG builders, AI consultants/agency leads, indie AI product founders.
**Citation scope:** ALL tiers.
**Personas:** A=AI agent engineer, B=RAG builder, C=AI consultant, D=indie AI product founder.

### TIER-1 (Top 30)

See `priority-120.md` § Wave 4.

### TIER-2 (Remaining 70)

| # | Slug | Title | Group | Persona |
|---|------|-------|-------|---------|
| 31 | embedding-model-choice | Embedding Model Comparison: OpenAI vs Cohere vs open-source | rag-pipelines | B |
| 32 | query-rewriting-hyde | Query Rewriting with HyDE: Hypothetical Document Embeddings | rag-pipelines | B |
| 33 | multi-hop-retrieval | Multi-Hop Retrieval: Iterative RAG for Complex Questions | rag-pipelines | B |
| 34 | vector-db-choice-matrix | Vector DB Choice Matrix: Pinecone vs Weaviate vs Qdrant vs pgvector | rag-pipelines | B |
| 35 | metadata-filtering-rag | Metadata Filtering in RAG: Structured + Semantic Combined | rag-pipelines | B |
| 36 | ingestion-pipeline-design | Document Ingestion Pipeline: Parse → Chunk → Embed → Index | rag-pipelines | B |
| 37 | streaming-sse-implementation | Streaming with SSE: Real-Time Token Display + Backpressure | llm-integration | D |
| 38 | batch-inference-anthropic | Batch Inference with Anthropic Message Batches API | llm-integration | D |
| 39 | rate-limit-handling | Rate Limit Handling: Exponential Backoff + Token Bucket | llm-integration | A |
| 40 | cost-tracking-dashboard | LLM Cost Tracking: Token Accounting, Budget Alerts | llm-integration | D |
| 41 | model-selection-claude-gpt-gemini | Model Selection Guide: Claude vs GPT-4o vs Gemini | llm-integration | C |
| 42 | provider-abstraction-layer | Provider Abstraction Layer: LiteLLM + Adapter Pattern | llm-integration | A |
| 43 | system-prompt-design | System Prompt Design: Persona, Format, Constraints | prompt-engineering | A |
| 44 | few-shot-vs-zero-shot | Few-Shot vs Zero-Shot: When Examples Help and When They Hurt | prompt-engineering | B |
| 45 | prompt-versioning-gitops | Prompt Versioning with GitOps: Prompt-as-Code | prompt-engineering | A |
| 46 | prompt-testing-framework | Prompt Testing Framework: Unit Tests for Prompts with pytest | prompt-engineering | A |
| 47 | prompt-injection-defense | Prompt Injection Defense: Detection Patterns + Sanitization | prompt-engineering | C |
| 48 | chain-of-thought-structured | Structured Chain-of-Thought: Scratchpad + Verification | prompt-engineering | A |
| 49 | context-window-mgmt | Context Window Management: Trim, Summarize, Archive | context-engineering | A |
| 50 | context-summarization | Conversation Summarization: Rolling + Retrieval-Augmented | context-engineering | A |
| 51 | context-retrieval-pipeline | Context Retrieval Pipeline: Semantic Search over History | context-engineering | B |
| 52 | kv-cache-optimization | KV-Cache Optimization: Prefix Structure for Maximum Reuse | context-engineering | D |
| 53 | tool-use-design-patterns | Tool Use Design: Schema First, Validation, Safe Side Effects | ai-agents | A |
| 54 | plan-execute-pattern | Plan-Execute Agent: Two-Phase Reasoning for Complex Tasks | ai-agents | A |
| 55 | agent-supervision-human-in-loop | Agent Supervision: Human-in-the-Loop Gates | ai-agents | C |
| 56 | deterministic-agent-testing | Deterministic Agent Testing: Replay, Snapshot, Mock Tools | ai-agents | A |
| 57 | agent-state-machine-design | Agent as State Machine: Explicit States, Transitions, Halt | ai-agents | A |
| 58 | parallel-tool-calls | Parallel Tool Calls: Fan-Out + Result Aggregation | ai-agents | A |
| 59 | mcp-server-testing | MCP Server Testing: Unit + Integration with Mock Clients | mcp-protocol | A |
| 60 | mcp-best-practices | MCP Best Practices: Naming, Descriptions, Error Codes | mcp-protocol | A |
| 61 | mcp-client-integration | MCP Client Integration: Connecting Claude to Your MCP Server | mcp-protocol | A |
| 62 | mcp-auth-security | MCP Auth + Security: OAuth, API Keys, Input Sanitization | mcp-protocol | C |
| 63 | claude-code-hooks-design | Claude Code Hooks: Pre/Post Tool Hooks for Safety + Logging | claude-code-skills | A |
| 64 | agents-md-convention | AGENTS.md Convention: Multi-Agent Knowledge Layer Design | claude-code-skills | A |
| 65 | skill-testing-strategy | Skill Testing Strategy: How to Verify Claude Code Skills Work | claude-code-skills | A |
| 66 | skill-packaging-distribution | Skill Packaging + Distribution: Ship as Installable Add-Ons | claude-code-skills | D |
| 67 | memory-files-pattern | Memory Files Pattern: Persistent Context Across Sessions | claude-code-skills | A |
| 68 | eval-harness-setup | Eval Harness Setup: pytest + LangSmith + CI Integration | evaluation | A |
| 69 | golden-dataset-creation | Golden Dataset Creation: Annotation Guidelines + Quality | evaluation | B |
| 70 | ab-test-agents | A/B Testing Agents: Traffic Split, Metrics, Significance | evaluation | D |
| 71 | regression-testing-prompts | Regression Testing Prompts: Catch Regressions Every Deploy | evaluation | A |
| 72 | harm-classification-pipeline | Harm Classification Pipeline: Moderation Layer Before LLM | ai-safety | C |
| 73 | output-filtering | Output Filtering: Post-LLM Validation + Fallback Responses | ai-safety | C |
| 74 | refusal-patterns | Refusal Pattern Design: Graceful Declines | ai-safety | D |
| 75 | content-moderation-openai-api | Content Moderation with OpenAI Moderation API + Custom Rules | ai-safety | C |
| 76 | audit-log-design | Audit Log Design for AI Systems: What to Log, Retention, GDPR | ai-safety | C |
| 77 | model-versioning-mlflow | Model Versioning with MLflow: Registry, Staging, Production | ml-ops | A |
| 78 | experiment-tracking-wandb | Experiment Tracking with W&B: Sweeps, Artifacts, Model Cards | ml-ops | B |
| 79 | deployment-strategies-blue-green | ML Deployment: Blue-Green, Canary, Shadow Mode | ml-ops | A |
| 80 | retraining-pipeline-design | Retraining Pipeline: Trigger Logic, Data Freshness, Rollback | ml-ops | A |
| 81 | feature-store-basics | Feature Store Basics: What They Solve and When You Need One | ml-ops | C |
| 82 | eval-after-fine-tune | Evaluating Fine-Tuned Models: Before/After Benchmarks | fine-tuning | B |
| 83 | distillation-basics | Model Distillation: Teacher-Student Setup for Cost Reduction | fine-tuning | D |
| 84 | deployment-fine-tuned-model | Deploying Fine-Tuned Models: Inference Servers, Quantization | fine-tuning | A |
| 85 | image-to-text-pipeline | Image-to-Text Pipeline: Claude Vision + Structured Extraction | multimodal | B |
| 86 | audio-transcription-whisper | Audio Transcription with Whisper: Chunking, Diarization | multimodal | D |
| 87 | tts-pipeline-production | TTS Pipeline: ElevenLabs / OpenAI TTS + Caching + Cost | multimodal | D |
| 88 | video-understanding-frames | Video Understanding: Frame Extraction + Vision LLM Analysis | multimodal | B |
| 89 | text-to-image-prompt-engineering | Text-to-Image Prompt Engineering: SD / DALL-E 3 Patterns | multimodal | D |
| 90 | output-length-budgets | Output Length Budgets: max_tokens Strategy + Streaming Cutoff | cost-optimization | D |
| 91 | embedding-cost-ops | Embedding Cost Ops: Batch, Caching, Model Swap | cost-optimization | B |
| 92 | vector-storage-cost | Vector Storage Cost: Compression, Quantization, Tiered | cost-optimization | B |
| 93 | batch-processing-patterns | Batch Processing Patterns: Async Queue + Priority Lanes | cost-optimization | D |
| 94 | pricing-ai-features | Pricing AI Features: Usage-Based vs Seat, Margin Math | ai-product-positioning | D |
| 95 | ai-native-vs-enhanced | AI-Native vs AI-Enhanced: Positioning Framework | ai-product-positioning | D |
| 96 | latency-ux-patterns | Latency UX: Skeletons, Streaming, Optimistic UI | ai-product-positioning | D |
| 97 | error-ux-patterns-ai | Error UX for AI: Graceful Failures, Retry Suggestions | ai-product-positioning | D |
| 98 | roi-estimation-framework | ROI Estimation Framework: Quantify AI Value for Sign-Off | ai-consultancy-ops | C |
| 99 | ai-poc-delivery-playbook | AI POC Delivery: Scope, Build, Demo, Handoff in 4 Weeks | ai-consultancy-ops | C |
| 100 | governance-nist-ai-rmf | AI Governance with NIST AI RMF: Map, Measure, Manage | ai-consultancy-ops | C |

---

## Sample methodology citations

For TIER-1 selections; full citation map produced during phase 4-7 authoring.

### Free tier (sample 10)

| # | Slug | Cites |
|---|------|-------|
| 3 | git-daily-workflow | `knowledge/free/dev/devtools-developer/git-commit-discipline` |
| 9 | python-first-project | `knowledge/free/dev/python-developer/project-structure-basics` |
| 11 | dotenv-secrets-management | `knowledge/free/dev/code-quality/secrets-management` |
| 12 | mom-test-customer-interview | `knowledge/free/marketing/marketing-manager/customer-discovery-interviews` |
| 14 | niche-selection-framework | `knowledge/free/marketing/marketing-manager/niche-targeting-strategy` |
| 20 | landing-page-essentials | `knowledge/free/marketing/marketing-manager/landing-page-copywriting` |
| 24 | positioning-basics | `knowledge/free/marketing/marketing-manager/product-positioning-framework` |
| 25 | write-good-readme | `knowledge/free/dev/code-quality/readme-writing-standards` |
| 26 | testing-intro-python | `knowledge/free/dev/testing-developer/pytest-fundamentals` |
| 30 | code-style-and-prettier | `knowledge/free/dev/code-quality/automated-formatting-standards` |

### Solo tier (sample 10)

| # | Slug | Cites (free + solo) |
|---|------|---------------------|
| 1 | stripe-integration-basics | `free/dev/backend-developer`, `solo/dev/api-developer`, `solo/product/product-operations` |
| 2 | landing-page-from-zero | `free/marketing/marketing-manager`, `solo/dev/frontend-developer`, `solo/ux/ui-designer`, `solo/marketing/seo-manager` |
| 3 | vps-first-deploy | `free/dev/devtools-developer`, `solo/infra/server-craft`, `solo/dev/automation-tooling` |
| 5 | writing-first-spec | `free/dev/software-developer`, `solo/sdd/sdd`, `solo/sdd/sdd-planning`, `solo/product/product-planning` |
| 4 | rest-api-in-one-day | `free/dev/backend-developer`, `solo/dev/api-developer`, `solo/sdd/sdd` |
| 10 | roadmap-for-one-person | `solo/product/product-planning`, `solo/sdd/sdd-planning`, `solo/product/product-operations` |
| 11 | newsletter-setup | `free/marketing/marketing-manager`, `solo/marketing/content-marketer`, `solo/comms/communicator` |
| 16 | technical-seo-audit | `solo/marketing/seo-manager`, `solo/marketing/content-marketer`, `solo/product/product-planning` |
| 20 | client-email-templates | `solo/comms/communicator`, `solo/product/product-operations` |
| 25 | runway-calc | `solo/product/product-planning`, `solo/product/product-operations` |

### Pro tier (sample 10)

| # | Slug | Cites (free + solo + pro) |
|---|------|---------------------------|
| 1 | statement-of-work | `pro/ba/ba-core`, `pro/ba/business-analyst`, `pro/comms/hr-recruiter` |
| 2 | production-cicd-pipeline | `pro/infra/cicd-engineer`, `pro/infra/devops-engineer`, `solo/dev/automation-tooling` |
| 3 | first-hire-developer | `pro/comms/hr-recruiter`, `pro/pm/project-manager`, `solo/comms/communicator` |
| 4 | google-ads-first-campaign | `pro/marketing/ppc-manager`, `pro/marketing/growth-marketer`, `pro/research/market-researcher` |
| 12 | terraform-iac | `pro/infra/infrastructure-engineer`, `pro/infra/devops-engineer`, `pro/infra/cicd-engineer` |
| 17 | stakeholder-elicitation | `pro/ba/business-analyst`, `pro/ba/ba-core`, `pro/ux/ux-researcher` |
| 10 | prd-template | `pro/product/product-manager`, `pro/ba/business-analyst`, `pro/ux/ux-researcher` |
| 15 | aarrr-funnel | `pro/marketing/growth-marketer`, `pro/marketing/conversion-optimizer`, `pro/research/researcher` |
| 13 | caching-strategy | `pro/dev/backend-systems`, `pro/dev/backend-enterprise`, `pro/infra/infrastructure-engineer` |
| 25 | hiring-funnel | `pro/comms/hr-recruiter`, `pro/pm/project-manager`, `pro/ba/business-analyst` |

### Geek tier (sample 10)

| # | Slug | Cites (all tiers) |
|---|------|-------------------|
| 1 | rag-hybrid-search-bm25-vector | `geek/ai/rag-engineer`, `geek/ai/llm-integration` |
| 2 | react-loop-production | `geek/ai/ai-agents`, `geek/ai/llm-integration` |
| 3 | structured-output-json-schema | `geek/ai/llm-integration`, `geek/ai/claude-code` |
| 5 | claude-code-skill-authoring | `geek/ai/claude-code`, `geek/ai/llm-integration` |
| 7 | prompt-caching-anthropic | `geek/ai/llm-integration`, `geek/ai/ai-agents` |
| 9 | mcp-server-build | `geek/ai/claude-code`, `geek/ai/ai-agents` |
| 12 | semantic-xml-prompts-anthropic | `geek/ai/llm-integration`, `geek/ai/claude-code` |
| 13 | retrieval-evaluation-ragas | `geek/ai/rag-engineer`, `geek/ai/ml-ops` |
| 22 | ai-proposal-template | `geek/ai/ai-agents`, `pro/marketing/gtm-strategist`, `pro/research/market-researcher` |
| 30 | ai-audit-checklist | `geek/ai/ml-ops`, `pro/ux/accessibility-specialist`, `pro/research/researcher` |

---

## Summary

| Tier | TIER-1 | TIER-2 | Total | Citation scope |
|------|--------|--------|-------|----------------|
| Free | 30 | 70 | 100 | `knowledge/free/` only |
| Solo | 30 | 70 | 100 | `free + solo` |
| Pro | 30 | 70 | 100 | `free + solo + pro` |
| Geek | 30 | 70 | 100 | all four |
| **TOTAL** | **120** | **280** | **400** | — |

TIER-1 (120) authored under feature-048. TIER-2 (280) backlog for future feature.
