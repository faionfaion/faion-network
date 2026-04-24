# Agent Integration — Learning Speed as Competitive Moat (Product Manager)

> Companion to the product-operations variant of this methodology. The product-operations file at `../../../solo/product/product-operations/learning-speed-competitive-moat/agent-integration.md` covers the org-wide signal pipeline, `beliefs.yaml`, and the daily/weekly synthesizer loop. **Do not duplicate.** This file focuses on the **PM-as-learner** angle: the personal and squad-level practices, metrics, and rituals that compress *time-to-belief-change* for a single PM owning a product area, plus the PM-specific failure modes the org-wide pipeline cannot fix.

## When to use
- A PM owns a product area against ≥1 well-funded competitor and the differentiation thesis depends on shipping the right thing next, not the most things.
- A PM is preparing for a quarterly business review and needs to defend "what we changed our minds about" with evidence, not vibes.
- A PM is setting personal OKRs / level-expectations and `learning velocity` (not feature throughput) is the contested promotion criterion.
- A PM has just inherited a roadmap built on stale assumptions and needs a 30-day belief-audit before committing to next quarter.
- A PM-led squad is post-PMF and the bottleneck has moved from `does anyone want this?` to `which of 8 plausible bets do we make first?`.
- An exec asks "what would change our roadmap?" — the PM with a kill-criterion list per roadmap item answers in 30 seconds; the PM without spends a week.

## When NOT to use
- Pre-PMF founder/PM. The bottleneck is *one* working hypothesis, not learning velocity across many. Build the thing, talk to 5 users, ship.
- Highly regulated domains (medical devices, defense, certain fintech) where weekly belief updates contradict regulatory commitment cycles. Use slower, audited cadences.
- A PM whose squad has not shipped in 8+ weeks. Belief-update rituals on top of a broken delivery system worsen morale; fix delivery first.
- A PM in a "feature-factory" org where roadmap is set top-down by sales. Personal learning velocity will not move the moat; the moat lives at exec level. Use the framework upward, not at squad level.
- Solo discovery sprints (1-week deep dive into one segment). Single-thread focus beats meta-process; defer.

## Where it fails / limitations
- **Performance theater:** PMs publish a flashy "weekly insights" newsletter, count it as learning velocity, and never change a roadmap line. Learning is measured by *decisions reversed or accelerated*, not by document volume.
- **Hero PM trap:** the most-learning PM in an org is often the bottleneck, because all signals route through them. Personal learning velocity ≠ org learning velocity; the PM must explicitly *delegate* belief ownership to the squad.
- **Confirmation engine:** PMs usually classify their own evidence. Without a peer or red-teamer, every event becomes "evidence for the belief I already had". The methodology is silent on this; PMs must build the social loop.
- **Ritual stacking:** Monday discovery, Tuesday roadmap, Wednesday competitor, Thursday OKRs, Friday retro — soon the PM is in rituals 4 days a week and never makes a decision. Cap rituals at ≤2 hours/week of synchronous time.
- **Calibration debt:** PMs rarely grade their own past predictions, so personal confidence drifts. Without quarterly self-calibration, the "fast-learning PM" is just a fast-talking PM.
- **Cross-PM drift:** in a multi-PM product, each PM's belief registry diverges; a customer hears three different stories. The PM-Lead must enforce a shared belief schema even if individual beliefs differ.
- **Output-trained orgs:** if `# of features shipped` is the PM's review metric, no amount of learning ritual changes incentives. The methodology requires the manager and skip-level to also be on `learning velocity` as a metric, otherwise it dies.
- **Discovery-debt accumulation:** PMs who delegate signal collection to agents stop talking to users; their "fast learning" decays into "fast theorizing on stale data" within ~6 weeks. Force a human-touched discovery floor (≥3 user conversations/week).

## Agentic workflow
The PM-flavored loop is *belief-per-bet*, not *belief-per-org*. For each roadmap bet (typically 4–8 in flight), the PM maintains a one-page `bet.md` with: hypothesis, kill criteria, leading indicator, owner, check-back date, and the two strongest opposing signals seen so far. A daily collector agent (Haiku) scoped to that bet's segment scrapes the relevant analytics slice, support tags, and one external corpus (competitor changelog, subreddit, niche newsletter). A `bet-reviewer` agent (Sonnet) runs at squad weekly, scores each bet against its kill criteria, and outputs `keep | accelerate | kill | reframe` with citations. The PM owns two judgment moments only: (1) accept/reject the reviewer's recommendations on Friday, (2) communicate belief changes upward via the monthly exec brief. Everything else is mechanical and delegated. The PM's promotion narrative is the audit log of `bet.md` changes; "I killed bet X on date Y because of evidence Z" is unambiguous senior-PM evidence.

### Recommended subagents
- `faion-pm-agent` (referenced in this skill's frontmatter; see `agents/pm/`) — owns `bet.md` files in `.aidocs/product/bets/`, refuses to mark a bet `keep` without ≥3 cited supporting events from the last 30 days. Sole writer of the per-bet status field.
- `faion-research-agent` (sibling skill) — runs targeted competitor / segment refreshes that the PM agent's collector cannot script (paywalled reports, expert interviews, niche communities). PM consumes; research agent produces.
- `faion-business-analyst` (sibling) — extracts hypotheses from raw user interviews into structured `event` records that feed the bet's evidence stream. PM-Lead arbitrates conflicts before they hit `bet.md`.
- `faion-brainstorm` — used in the *Friday reframe* path: when `bet-reviewer` outputs `reframe`, brainstorm diverges on alternative framings before the PM converges. Prevents premature kill of bets that just need re-shaping.
- `signal-classifier` (from product-operations variant) — reused as-is; the PM's per-bet collector pipes events into the org-wide classifier rather than re-implementing classification.
- `decision-logger` (from product-operations variant) — reused; every PM bet decision (`keep|accelerate|kill|reframe`) is a row in the decision log with a prediction and a check-back date.
- `password-scrubber-agent` — non-negotiable before any `bet.md` ships to a public artifact (board pre-read, fundraising deck); bets often cite individual customer names, deal sizes, and internal pricing experiments.

### Prompt pattern
Per-bet weekly review (Sonnet, structured output):
```
<role>bet-reviewer</role>
<bet>{{ bet_md }}</bet>
<kill_criteria>{{ bet.kill_criteria }}</kill_criteria>
<events_last_30d>{{ events_for_this_bet_jsonl }}</events_last_30d>
<rules>
  Output one of: keep | accelerate | kill | reframe.
  - keep: >=3 cited events_for in last 30d AND no kill_criterion tripped.
  - accelerate: >=3 events_for AND a leading indicator above target.
  - kill: any kill_criterion tripped OR <2 events_for in last 30d.
  - reframe: >=2 events_against from a coherent alternative hypothesis.
  Cite event_ids per claim. Refuse to recommend without citations.
</rules>
<output_schema>
  {recommendation, rationale, cited_events:[event_id], confidence,
   proposed_kill_criterion_update, check_back_date}
</output_schema>
```

PM personal calibration (quarterly, Opus):
```
<role>pm-calibration</role>
<decision_log>{{ decisions_last_quarter_yaml }}</decision_log>
<deliverable>For each decision: predicted vs actual, calibration score
(0..1), specific lesson. Aggregate: which decision types I am over/under
confident on. Recommend 3 prompt-rubric updates for bet-reviewer for next
quarter.</deliverable>
<constraint>No qualitative praise. Every claim cites a decision_id.
If under 10 decisions logged, output "insufficient sample" — do not
fabricate trend.</constraint>
```

Squad belief broadcast (Haiku, terse):
```
<role>belief-broadcast</role>
<changed_beliefs>{{ diff_of_bets_yaml }}</changed_beliefs>
<audience>squad-engineers</audience>
<format>3 bullets max. Lead with what we now believe (not what we
debated). Link the bet.md and the decision_id. No exec hedging.</format>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Version `bet.md` files; PR-review belief changes; `gh pr view` as the audit trail | https://cli.github.com |
| `lookerctl` / `looker-sdk` | Pull leading-indicator queries per bet on a fixed schedule | https://cloud.google.com/looker |
| `posthog` CLI | Per-bet cohort exports without writing dashboards | https://posthog.com/docs/api |
| `gong-cli` (community) / Gong API | Pull deal-stage transcript snippets per bet's ICP | https://app.gong.io/api |
| `dovetail-cli` (community) / Dovetail API | Pull tagged interview clips into bet evidence | https://developers.dovetailapp.com |
| `notion-cli` / Notion API | Render `bet.md` into the exec-shareable bet board | https://developers.notion.com |
| `linear-cli` / Linear GraphQL | Tie experiments and discovery tasks to bet IDs; close the loop | https://developers.linear.app |
| `dbt` | Per-bet metric models so leading indicators are versioned, not ad-hoc | https://docs.getdbt.com |
| `yq` / `jq` | Diff `bet.md` frontmatter between commits to flag belief drift | https://github.com/mikefarah/yq |
| `pre-commit` + custom hook | Block PRs on `bet.md` without `kill_criteria`, `check_back_date`, `decision_owner` | https://pre-commit.com |
| `claude` (Anthropic SDK) | Bet-reviewer, broadcast, calibration agents | https://docs.anthropic.com |
| `mailmerge` | Send the per-stakeholder bet update from a CSV (no marketing tool) | `pip install mailmerge` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Yes — REST API | Bet-as-objective; integrates roadmap and feedback inboxes |
| Aha! Roadmaps | SaaS | Yes — API | Strong "outcome → initiative → epic" hierarchy; fits PM bets cleanly |
| Roadmunk / airfocus | SaaS | Partial API | Lightweight bet boards for solo PMs |
| Reforge Artifacts | SaaS | No API | Reference templates for PM bet frameworks; copy patterns, do not integrate |
| Maze | SaaS | Yes — API | Continuous discovery experiments scoped per bet |
| Sprig | SaaS | Yes — API | In-product surveys triggered by bet's leading-indicator cohort |
| UserTesting / UserInterviews | SaaS | Yes — API | Recruit per-bet ICP for fast qualitative signal |
| Statsig / Eppo / GrowthBook | SaaS / OSS | Yes — REST | Per-bet experiment results into the reviewer prompt |
| Dovetail | SaaS | Yes — API | Tagged interview corpus per bet |
| Glean | SaaS | Yes — API | Cross-tool semantic search; finds prior internal discussions of a hypothesis |
| Pendo / Heap / Mixpanel | SaaS | Yes — API | Per-bet behavioural cohorts |
| Gainsight PX | SaaS | Yes — API | CS-driven signals for B2B PMs |
| Lattice / 15Five | SaaS | Yes — API | PM personal-OKR alignment with `learning velocity` metric |
| Quantive (Gtmhub) | SaaS | Yes — API | OKR layer that can host `learning velocity` as a first-class objective |
| Plane / OpenProject | OSS | Yes — REST | Self-hosted bet board + decision log |
| Otter.ai / Fireflies | SaaS | Yes — API | Auto-transcribe user calls; PM-flavored review extracts hypothesis-supporting clips |

## Templates & scripts
The product-operations variant ships `belief_update.py` for the org-wide loop — reuse it, do not duplicate. The PM-flavored gap is a *learning-velocity scorecard* the PM can attach to a quarterly review and to OKRs.

```python
# pm_learning_velocity.py — score a PM's learning velocity from their decision log.
# Inputs:
#   decisions.yaml  (list of {id, ts, bet_id, decision, prediction, check_back_date, outcome})
# Usage: python pm_learning_velocity.py decisions.yaml [--quarter 2026Q2]
import sys, yaml, datetime, argparse, statistics

ap = argparse.ArgumentParser()
ap.add_argument("path")
ap.add_argument("--quarter", default=None)
args = ap.parse_args()

decisions = yaml.safe_load(open(args.path)) or []
if args.quarter:
    decisions = [d for d in decisions if d.get("quarter") == args.quarter]
if not decisions:
    sys.exit("no decisions in scope")

n = len(decisions)
reversed30 = sum(1 for d in decisions
                 if d.get("reversed_within_days") and d["reversed_within_days"] <= 30)
graded = [d for d in decisions if d.get("outcome") in ("hit", "miss")]
hit_rate = sum(1 for d in graded if d["outcome"] == "hit") / len(graded) if graded else None
kills = sum(1 for d in decisions if d["decision"] == "kill")
reframes = sum(1 for d in decisions if d["decision"] == "reframe")
mean_time_to_check = statistics.mean(
    [(datetime.date.fromisoformat(d["check_back_date"])
      - datetime.date.fromisoformat(d["ts"][:10])).days
     for d in decisions if d.get("check_back_date")]
) if decisions else 0

print(f"Decisions logged       : {n}")
print(f"Kill / reframe ratio   : {(kills+reframes)/n:.0%}  (target >=30%)")
print(f"Reversed within 30 days: {reversed30/n:.0%}      (target <=15%)")
print(f"Mean time to check-back: {mean_time_to_check:.0f} days  (target <=21)")
if hit_rate is not None:
    print(f"Prediction hit rate    : {hit_rate:.0%}  (target 0.55-0.75 — outside = miscalibrated)")
else:
    print("Prediction hit rate    : insufficient graded sample")
```
A high `Decisions logged` with a near-zero `Kill / reframe ratio` is the signature of a PM who is documenting busywork, not learning. Hit rates above ~75% mean the PM is only logging easy bets; below ~55% means they are guessing.

## Best practices
- One `bet.md` per roadmap bet, in `.aidocs/product/bets/`. Treat it as code: PR-reviewed, diff-able, audit-logged. Slack threads do not count.
- Every bet has a written **kill criterion** before any work starts. "We will stop if X by Y" — measurable, time-bound, ideally a single number. No kill criterion ⇒ not a bet, just a project.
- Tie `learning velocity` to OKRs explicitly: e.g. "≥30% of bets killed/reframed per quarter, prediction hit rate in the 55–75% band". Without an OKR, no incentive, no behavior change.
- Cap rituals at 2 synchronous hours/week (45-min Friday review + 30-min Monday digest read + 15-min daily skim). Anything more crowds out user research.
- Maintain a `discovery floor` per PM: ≥3 user conversations/week, transcripts in Dovetail/Gong with bet tags. Without it, the agent loop runs on stale truth.
- The PM-Lead enforces a shared `bet.md` schema across PMs, but does not normalize bets themselves. Diversity of bets, uniformity of evidence schema.
- Pair-review belief changes: every "kill" or "reframe" requires a peer PM or EM signoff. Self-classification is the #1 source of confirmation bias.
- Quarterly **personal calibration** is non-optional. Run `pm_learning_velocity.py` on your own decisions. If you cannot, you have not been logging.
- Distinguish *evidence-driven* belief changes from *taste-driven* product calls; both are legitimate, but conflating them rots the audit log. Tag each decision.
- Promote with the audit trail. "I killed bet X based on evidence Y on date Z" beats any narrative essay in a senior-PM packet.
- Run an annual **anti-moat audit**: which competitors have a faster learning loop than us, why, and what would it cost to match? Reframe roadmap accordingly.
- Read the org-wide `beliefs.yaml` weekly even if you do not own it. Cross-bet collisions (PM-A's bet rests on a belief PM-B's evidence is killing) are caught only by reading across.

## AI-agent gotchas
- **Bet inflation**: agents propose new bets on every signal cluster, so the PM ends up with 30 bets nobody can maintain. Hard cap (e.g. 8 bets in flight per PM) enforced in the bet-reviewer prompt.
- **Citation laundering**: an LLM cites the same Slack thread three times under three event_ids. Dedupe by `(channel, message_ts)` before counting "independent" supports.
- **Premature kill on weekend lulls**: agent runs Monday, sees zero events_for from the weekend, recommends `kill`. Always evaluate over a rolling 30-day window, not the last sprint.
- **Reframe loops**: a bet that gets reframed every week is not learning, it is drifting. Lint: `reframes_in_last_quarter <= 1` per bet, otherwise flag for human strategy review.
- **Decision-log fabrication for promo**: an LLM asked to "summarize my year for promo" will invent decisions you never made. Use the log to verify the narrative; never let the agent author it.
- **Stale collector outputs leaking into bets**: a competitor scrape returns a 2024 page; the agent dates it `today`. Always preserve `source_published_at` and reject events older than the bet's check-back window.
- **PM tone homogenization**: agents draft all bet updates in the same voice across all PMs in the org; execs notice. Per-PM tone fingerprint or human-author the upward broadcasts.
- **Single-LLM monoculture**: using one model family for collector + classifier + reviewer creates correlated errors. At least the *reviewer* should be a different model class than the classifier (Opus vs Haiku is not enough; consider an alternative provider for the reviewer's red-team pass).
- **Privacy in user transcripts**: PM bets often cite named customers; do not let the bet-reviewer ingest raw PII into a shared belief registry. Strip PII at the classifier stage.
- **Auto-broadcasting kill decisions**: an agent posts "we killed feature X" before sales, support, and partnership were notified. Force a 24-hour human-review delay on `kill` broadcasts; not on `keep` or `accelerate`.
- **Calibration as ritual instead of feedback**: agent emits a calibration scorecard, PM glances and ignores. Tie the scorecard to OKR review; otherwise it has no behavioral effect.
- **Rubric drift**: if quarterly calibration suggests prompt-rubric updates and the PM rewrites the bet-reviewer prompt every quarter, comparability across quarters is lost. Version the rubric; A/B-shadow new rubrics for one quarter before switching.
- **Discovery atrophy via agentification**: tracking "events ingested" rises while "user conversations had" falls. Force the dashboard to display both side-by-side; alert if conversations drop.

## References
- Reforge — *Mastering Product Management* and *Product Strategy* programs; "speed of learning as a moat" essay (https://www.reforge.com/blog/learning-velocity)
- Marty Cagan — *Inspired* (2nd ed., 2017), *Empowered* (2020), *Transformed* (2024) — PM as continuous-discovery learner
- Teresa Torres — *Continuous Discovery Habits* (book + producttalk.org); opportunity-solution tree per bet
- Lenny Rachitsky — "How great PMs run experiments" and "Belief audits" essays (https://www.lennysnewsletter.com)
- John Cutler — *The Beautiful Mess* — repeated posts on bet-thinking and PM learning systems (https://cutlefish.substack.com)
- Annie Duke — *Thinking in Bets*, *How to Decide* — decision logs, prediction calibration
- Melissa Perri — *Escaping the Build Trap* — outcome vs output, belief-change as PM artifact
- Itamar Gilad — *Evidence-Guided* — confidence meter for product bets (https://itamargilad.com)
- Shreyas Doshi — "High-quality decisions vs high-velocity decisions" thread series on X/Twitter
- Mind the Product / ProductTank archives — PM learning-velocity case studies
- Sibling methodologies in this skill: `continuous-discovery-habits`, `experimentation-at-scale`, `competitive-positioning`, `feedback-management`, `release-planning`
- Companion file: `../../../solo/product/product-operations/learning-speed-competitive-moat/agent-integration.md` (org-wide signal pipeline + `beliefs.yaml`)
