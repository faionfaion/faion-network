# Geek / Evaluation

LLM behavioral evaluation playbooks: adversarial inputs, safety evals, refusal rate measurement, and regression suites. Citation scope: all four tiers (`knowledge/free/ + solo/ + pro/ + geek/`).

| Slug | Goal |
|------|------|
| `behavioral-evals-adversarial` | Build an adversarial test harness that measures refusal rate against prompt injections, jailbreaks, boundary inputs, and role-confusion attacks with a pass criterion of ≥95% |

Spec: `../../../../../.aidocs/conventions/playbooks/playbook-spec.md`. Validator: `python3 scripts/validate-tier-playbook.py <path>`.
