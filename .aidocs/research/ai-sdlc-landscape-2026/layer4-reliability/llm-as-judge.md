# LLM-as-Judge
**Layer:** 4 — Reliability · **Verdict:** 🟡 take the idea, not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

A judge is a *measuring instrument with a systematic bias you have not characterised*. Used to rank two candidates against each other it is decent. Used to produce an absolute score you gate on, it is a random number with a confidence interval you invented. Take it for rung 3 of the ladder — a handful of scenarios, pairwise, calibrated against your own labels, never fail-open. Do not take it for anything a regex could have caught.

## What it is

Prompting a model to score or compare outputs, in place of a human rater. Three shapes, in increasing order of trustworthiness:

- **Single-output scoring** ("rate this 1–5 for X") — cheapest, least reliable, most seductive. Absolute scores from an uncalibrated judge are not comparable across time, model versions, or prompt edits.
- **Pairwise comparison** ("A or B, which better satisfies X?") — substantially more reliable, because the judge only has to detect a *difference*, not locate a point on a scale it invented. This is the shape the literature supports.
- **Reference-based grading** ("does this output entail the reference answer?") — most reliable, but requires a reference, at which point you should ask whether a deterministic check would do.

## Current state

The 2026 evidence base is bigger than "judges have biases" and materially different from the received wisdom.

**arXiv:2604.23178 — "Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines", Sadman Kabir Soumik, Transactions on Machine Learning Research (2026).** 5 judge models, 3 benchmarks, 4 bias categories, a released 375-pair controlled dataset.

| Finding | Number |
|---|---|
| **Style bias is the dominant failure mode** — judges prefer markdown-formatted responses over equivalent plain prose | magnitude **0.10–0.76** |
| **Position bias is small** — order of presentation | **≤ 0.04** |
| Verbosity/length preference **diverges by model family** | Gemini Pro / Flash / Llama favour longer: **+0.24 to +0.44**; **Claude prefers concise: −0.12**; GPT-4o neutral: **−0.04** |
| Truncation control: all judges correctly identify the complete response | accuracy **0.88–1.00** |
| Best cost/quality configuration | Gemini 2.5 Flash + "Combined Budget" debiasing: **71.0% agreement, κ = 0.549, ~$0.001 per evaluation — ~15× cheaper than the best frontier setup** |
| Debiasing strategies surviving Holm–Bonferroni correction | Claude S8 **+11.5 pp**, Flash S8 **+7.5 pp**, Claude S5 **+7.3 pp** |

**This partially refutes the prior pass's framing.** The prior pass named position bias, self-preference, and verbosity bias as the headline failure modes. Per this paper, **position bias is nearly negligible (≤0.04) while style bias — which the prior pass did not name — is up to 19× larger.** The practical instruction that follows is different too: normalise *formatting* before judging (strip markdown, equalise structure), which is not what "randomise position" tells you to do.

Two model-specific consequences for us:

- **Claude judges prefer concise output (−0.12).** Our house style is terse. A Claude judge grading Faion output has a bias that *aligns* with our style — which is comfortable and therefore dangerous: it will over-reward brevity even when brevity lost information.
- **A ~71% ceiling on human agreement with κ ≈ 0.55** is "moderate" agreement on the Landis–Koch scale. That is the *best tested configuration after debiasing*. Any pipeline treating a judge score as ground truth is treating a coin that lands right 7 times in 10 as a ruler.

**On the "synthetic relevance labels preserve only relative ranking, Kendall τ 0.72–0.91" claim:** I could not source it to arXiv:2604.23178, which is the bias-mitigation paper described above and does not report those figures. The claim is consistent with the IR literature on LLM-generated relevance judgments (the UMBRELA / LLMJudge line of work), where system-level rank correlation is high while absolute nDCG is inflated. **Treat the τ range as plausible but currently unsourced — do not cite it until re-verified.** The underlying principle stands on other grounds and is the more important half anyway: *use a judge to order things, not to score them.*

**Tooling.** Judge functionality is a feature of every harness, not a product: Promptfoo `llm-rubric` / `g-eval` / `factuality` / `answer-relevance` / `context-faithfulness` (MIT, opt-in per assertion, requires a `provider:`); DeepEval G-Eval and friends (OSS, Python); Braintrust autoevals; LangSmith evaluators. Nobody sells a judge; they sell the dashboard around it. Pricing is therefore the harness pricing in `eval-harnesses.md` plus the judge model's own token cost.

## Mechanics

### Judge cost model

```
judge_cost_per_case = (input_tokens_prompt + input_tokens_rubric
                     + input_tokens_candidate(s) + output_tokens) × model_rate
```

For pairwise you pay for both candidates. For our search output — a rubric of ~500 tokens plus two ~600-token result sets plus ~200 tokens of verdict — one comparison is ~2k tokens. At Sonnet-class rates that is fractions of a cent per case; at Opus-class rates, ~10×. **The token cost is not the constraint. The constraint is that every judge call is a call you must not blindly trust, and trust is bought with human labelling time.**

### Calibration protocol (this is the non-optional part)

1. Hand-label **N ≥ 50** cases yourself, pairwise, blind to which system produced which output.
2. Run the judge on the same N.
3. Compute agreement:

```
Raw agreement   p_o = (# cases judge and human agree) / N

Cohen's kappa   κ = (p_o − p_e) / (1 − p_e)
   where p_e = Σ_c  P_human(c) · P_judge(c)     (chance agreement, over categories c)

Interpretation (Landis & Koch): κ < 0.20 poor · 0.21–0.40 fair
   0.41–0.60 moderate · 0.61–0.80 substantial · > 0.80 almost perfect
```

4. If κ < 0.6, **the judge is not usable as a gate.** It may still be usable as a triage sort. The paper's best configuration reaches κ = 0.549 — i.e. even a well-debiased judge lands in "moderate", below the gate threshold. Plan accordingly.
5. Re-run calibration whenever the judge model version, the rubric, or the thing being judged changes shape. Judge drift is silent.

For rank correlation between a judge ordering and a human ordering (the "relative ranking is preserved" property):

```
Kendall τ-b = (C − D) / sqrt( (n₀ − n₁)(n₀ − n₂) )
  C  = concordant pairs,  D = discordant pairs
  n₀ = n(n−1)/2
  n₁ = Σ_i t_i(t_i−1)/2   over tie-groups t in ranking 1
  n₂ = Σ_j u_j(u_j−1)/2   over tie-groups u in ranking 2
```

τ-b, not τ-a: our rankings have ties (equal scores), and τ-a will lie to you about them.

### Bias controls, ordered by the 2026 evidence

| Control | Addresses | Evidence-weighted priority |
|---|---|---|
| **Normalise formatting of both candidates before judging** (strip markdown, equalise headings/bullets/emphasis) | style bias (0.10–0.76) | **Highest** — the largest measured bias, and the cheapest to remove |
| Length-match or explicitly instruct "do not reward length" | verbosity (+0.44 to −0.12, model-dependent) | High — and *sign-aware*: with a Claude judge, guard against over-penalising length |
| Swap A/B and require agreement across both orders | position (≤0.04) | Low value per the paper, but nearly free — keep it, stop leading with it |
| Never let a model judge its own family's output | self-preference | Keep as hygiene; magnitude not quantified in this paper |
| Force a rubric with explicit, enumerated criteria and a required justification per criterion | rubric drift, hand-waving | High |
| Report the *distribution* of scores, never a single mean | over-reading a noisy instrument | High |

### Our existing judge, and its bug

`~/workspace/projects/faion-net/faion-net-fe/scripts/llm-judge.py` grades MDX prose against YAML rubrics (`rubrics/uk-quality.yaml` and siblings). Its interface is good: `--rubric`, `--chunk-words`, `--model`, `--lang`, `--json`, `--max-high` (exit 1 if high-severity findings exceed a threshold). Chunked, rubric-driven, severity-tiered — this is the right shape.

**The bug, at `llm-judge.py:175`:**

```python
def parse_findings(reply: str) -> list[dict]:
    reply = reply.strip()
    reply = re.sub(r"^```(?:json)?\s*", "", reply)
    reply = re.sub(r"\s*```$", "", reply)
    if not reply.startswith("["):
        idx = reply.find("[")
        if idx >= 0:
            reply = reply[idx:]
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        return []          # ← FAIL-OPEN
```

A malformed judge reply returns **zero findings**, which flows into `--max-high` and reports **pass**. Every failure mode of the judge — a refusal, a truncation at `max_tokens`, an API error surfacing as prose, a rate-limit message, a model that decided to explain itself first — is silently converted into "this article is clean". The gate is loudest exactly when it has nothing to say and silent exactly when it has broken.

This matters beyond the FE repo because it is the pattern we would copy. **A quality gate must fail closed.** The fix is three lines: return a sentinel, raise, or emit a synthetic high-severity finding `{"severity":"high","rule":"judge-parse-failure", …}` so the existing `--max-high 0` path trips. The last option is best because it needs no caller changes.

Related note: this is also a live instance of the format-tax question from `structured-output.md`. The judge is asked for JSON in the prompt and the reply is regex-scrubbed for fences — i.e. it is a *soft* format instruction with no constrained decoding. Adding `output_config.format` here would eliminate the `JSONDecodeError` path entirely. But the fail-open must be fixed regardless: a schema-valid empty array is still an empty array.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines (arXiv:2604.23178, TMLR 2026) | https://arxiv.org/abs/2604.23178 | Style bias 0.10–0.76 vs position ≤0.04; per-family verbosity signs incl. Claude −0.12; 71.0% agreement / κ=0.549 at ~$0.001/eval with Gemini 2.5 Flash; Holm–Bonferroni-surviving debiasing gains; 375-pair dataset released | 2026-08-03 |
| 2 | Promptfoo — Configuration reference | https://www.promptfoo.dev/docs/configuration/reference/ | Model-graded assertion types (`llm-rubric`, `g-eval`, `factuality`, `answer-relevance`, `context-faithfulness`), `provider:` / `threshold:` / `weight:` / `metric:` on assertions | 2026-08-03 |
| 3 | Confident AI pricing | https://www.confident-ai.com/pricing | Cost of the dashboard around a judge: Free / $200 / $2,000 / Enterprise | 2026-08-03 |
| 4 | Braintrust pricing | https://www.braintrust.dev/pricing | Scores billed as a unit: 10k/mo free then $2.50/1k; Pro 50k then $1.50/1k — the only vendor that prices *judging* explicitly | 2026-08-03 |
| 5 | `faion-net-fe/scripts/llm-judge.py` (local) | — | Our own rubric-driven chunked judge; `--max-high` gate; **fail-open at line 175** | 2026-08-03 |
| 6 | `faion-net-fe/scripts/check-structural.py` (local) | — | The counter-example: deterministic step-0 gate, docstring states it runs "BEFORE any LLM review, so the model never burns an iteration on a mechanically-detectable defect" | 2026-08-03 |

## What to borrow for faion

1. **Fix the fail-open, and make "fail closed" a house rule.** `llm-judge.py:175` should emit a synthetic high-severity `judge-parse-failure` finding rather than `[]`. Then write it down as a rule: *a gate that cannot evaluate must not report pass.* This is the single most valuable line in this dossier and it costs three lines of Python.
2. **Use judges pairwise, not absolutely.** For search-quality work the question is "is prompt B's ranking better than prompt A's for this query", not "rate this ranking 1–5". Pairwise is what the evidence supports and it is what a champion/challenger prompt change actually needs.
3. **Normalise formatting before judging — first, not last.** Style bias is the largest measured effect (up to 0.76) and is removable with a `strings.ReplaceAll`-grade transform. Everyone's checklist leads with position swapping, which the 2026 data says is worth ≤0.04.
4. **Calibrate against 50 hand-labelled pairs before trusting any judge number**, and record κ next to every judge-derived metric we ever report. A metric without its κ is a decoration.
5. **Borrow the severity-tiered rubric shape from `rubrics/uk-quality.yaml`** for any agent-behaviour rubric we write: enumerated criteria, per-finding severity, `--max-high 0` as the gate. It is a good design; it just needs to fail closed.
6. **Consider a cheap judge, not a frontier one.** The paper's best cost/quality point is a *mid-tier* model with debiasing at ~$0.001/eval, ~15× cheaper than the best frontier setup. If we ever judge at volume, the frontier model is not the answer.
7. **Judge model ≠ system model.** Whatever transport the user runs (`claude`/`codex`/`gemini`/HTTP), the judge should be pinned and versioned independently, and must not be the same family as the system under test.

## What NOT to borrow — and why

- **Do not gate any release on an absolute judge score.** κ ≈ 0.55 at best. An absolute threshold on a moderate-agreement instrument is a coin flip wearing a number.
- **Do not put a judge anywhere near the CLI runtime.** No runtime Python, no runtime judge calls, no per-user grading. Judges are a dev-time instrument for *our* decisions about *our* prompts.
- **Do not use a judge for anything a deterministic check covers.** If the failure is "the ID does not exist", "the score is 1.4", "the required section is missing", "the tier is above the user's" — that is rung 1, costs zero, and is exactly right every time. Handing it to a judge makes it slower, costlier, and less accurate. This is the most common expensive mistake in the whole layer.
- **Do not adopt `g-eval` as a default.** It is a chain-of-thought scoring scheme; it produces plausible-sounding absolute scores, which is precisely the output shape we just said not to gate on.
- **Do not report a mean judge score.** Report the distribution and the disagreement rate. A mean hides that the instrument disagrees with you on 3 cases in 10.
- **Do not let a judge grade `why` strings.** Our `why` field is a ≤240-char UX affordance. Grading it costs tokens to measure something no user complains about.
- **Do not reuse `llm-judge.py` for agent evals.** It is a prose grader for MDX with editorial rubrics. Different artefact, different failure taxonomy. Borrow the shape, write a new one.

## Mapping to our corpus

| Slug | Domain | Action |
|---|---|---|
| `judge-calibration-protocol` | ai-core | **Primary target.** Insert the κ formula, the Landis–Koch bands, the N≥50 protocol, and the κ<0.6 "not a gate" rule |
| `model-eval-control-bands` | ai-core | Add: no absolute-score gates; bands must be defined on pairwise win-rate, not on judge score |
| `ai-feature-eval-set-design` | ai-core | Add the pairwise-over-absolute principle at design time |
| `quality-gates-confidence` | sdd | **Add the fail-closed rule.** This is where "a gate that cannot evaluate must not pass" belongs |
| `lint-autofix-vs-flag-decision-rule` | sdlc-ai | Sibling decision rule; cross-link — same family of judgement about what to block on |
| `eval-in-prod-sampling-policy` | ai-core | Judges as an offline sampler over prod traffic, never inline |
| `thumbs-down-to-eval-pipeline` | ai-core | Human signal as the calibration ground truth for the judge |
| `verbatim-to-eval-row-recipe` | ai-core | How a user complaint becomes a labelled pair |
| `prompt-engineering-evaluation` | ml-engineering | Champion/challenger pairwise judging for prompt edits |
| `evaluation-metrics`, `evaluation-framework`, `model-evaluation` | ml-engineering | Three overlapping leaves — add κ / τ-b formulas to whichever survives dedupe |

Gaps — no leaf covers: **(a) style bias as the dominant judge bias with its 2026 magnitudes; (b) the fail-open/fail-closed rule for LLM-backed gates.** Both are new leaves, and (b) is the one with a live bug behind it.

## Open questions / staleness risk

- **Unsourced:** the Kendall τ 0.72–0.91 figure for synthetic relevance labels. Attributed in the prior pass to arXiv:2604.23178, which does not contain it. Likely from the UMBRELA/LLMJudge IR line. **Do not cite until re-verified.**
- **Not quantified in the paper we do have:** self-preference bias magnitude. The "don't let a model judge its own family" rule is hygiene, not measured hygiene. Worth finding a number before we lean on it.
- The per-family verbosity signs (Claude −0.12, Gemini +0.24…+0.44) are **model-version-specific** and will not survive a generation change. Re-measure on the judge we actually pin.
- **High staleness on the 71% / κ=0.549 ceiling.** This is a 2026 measurement on 2026 judges. If judge agreement improves materially, the κ<0.6 "not a gate" rule loosens — that is a real possibility within a year and would change the ladder's rung-3 economics.
- We have **zero hand-labelled pairs**. Every κ threshold in this file is a rule about a number we have never computed.
- Open: should the fail-closed fix go in as a bug (BUG in `.product/bugs/todo/`) against faion-net-fe now, given it silently passes articles today? It is a live correctness hole in a shipped pipeline, not a research finding. Recommend yes.
