## Survey Question Bank

### Pricing Research

**Van Westendorp Price Sensitivity Meter (4 questions — open numeric)**
- "At what price would [product] be so expensive you would not consider buying it?"
- "At what price would [product] be expensive but still worth considering?"
- "At what price would [product] be a good deal?"
- "At what price would you question the quality of [product]?"
Analysis: use vw-pricing.py to compute PMC, PME, OPP, IPP.

**Gabor-Granger (series of closed price tests)**
- "Would you purchase [product] at $[X]/month?" [Yes / No / Maybe]
Run at $9, $19, $29, $49, $99 to build a price-response curve.

### Satisfaction Research

**Overall satisfaction (1-5 Likert)**
"How satisfied are you with [product] overall?"
1 = Very dissatisfied ... 5 = Very satisfied

**NPS (0-10)**
"How likely are you to recommend [product] to a colleague or friend?"
0 = Not at all likely ... 10 = Extremely likely
Note: report with ±5-7 CI band; do not report raw NPS change without significance test.

**Feature satisfaction matrix (1-5 per feature)**
| Feature | Very Dissatisfied | Dissatisfied | Neutral | Satisfied | Very Satisfied |
|---------|:-----------------:|:------------:|:-------:|:---------:|:--------------:|
| [Feature 1] | | | | | |
| [Feature 2] | | | | | |

### Feature Prioritisation

**MaxDiff (requires balanced incomplete block design — use Conjointly or Sawtooth)**
"Of these four features, which is MOST important to you? Which is LEAST important?"
[Feature A] / [Feature B] / [Feature C] / [Feature D]
Note: do not generate MaxDiff task lists manually or with an LLM — balance is required.

**Importance vs. Satisfaction matrix**
"Rate the IMPORTANCE of each feature (1-5) and your SATISFACTION with how we deliver it (1-5)."
High importance + low satisfaction = highest priority gap.

### Behavioural Self-Report

**Usage frequency (multiple choice — past behaviour only)**
"How often do you use [feature/product]?"
- Daily
- Several times a week
- Weekly
- Monthly or less
- Never
- Prefer not to say

**Current solution (multiple choice)**
"What do you currently use to [solve problem]?"
[List known alternatives + "Something else" + "Nothing / I don't do this"]
