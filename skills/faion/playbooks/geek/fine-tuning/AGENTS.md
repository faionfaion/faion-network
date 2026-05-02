# Geek / Fine-Tuning

LLM fine-tuning playbooks: dataset prep, LoRA adapters, RLHF/DPO, eval and deployment. Citation scope: all four tiers (`knowledge/free/ + solo/ + pro/ + geek/`).

| Slug | Goal |
|------|------|
| `lora-basics-dataset-prep` | Prepare 200-2000 JSONL training examples, train a LoRA adapter on Llama 3.1 8B via axolotl or TRL (rank=16, alpha=32), and evaluate on a held-out 10% split for under $30 on Modal/RunPod |

Spec: `../../../../../.aidocs/conventions/playbooks/playbook-spec.md`. Validator: `python3 scripts/validate-tier-playbook.py <path>`.
