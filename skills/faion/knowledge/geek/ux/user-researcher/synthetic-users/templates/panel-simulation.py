"""Run multi-persona synthetic interview panel via Claude API.

Input:  PERSONAS list + QUESTIONS list (edit below)
Output: printed Q&A pairs per persona
Note:   Use temperature 0.7-0.9 for realistic variation between personas.
        Always follow with real-user validation (min 3 sessions) before decisions.
"""
import anthropic

client = anthropic.Anthropic()

PERSONAS = [
    {"name": "Maya", "role": "Marketing manager", "tech": "medium", "pain": "manual CSV exports"},
    {"name": "Tom", "role": "Sales rep", "tech": "low", "pain": "too many apps to switch between"},
]

QUESTIONS = [
    "What is your first reaction to this product description?",
    "What would stop you from adopting this tool?",
    "What feature would make you pay for this immediately?",
]


def simulate_interview(persona: dict, questions: list[str]) -> list[dict]:
    system = (
        f"You are {persona['name']}, {persona['role']}. "
        f"Tech comfort: {persona['tech']}. Main pain: {persona['pain']}. "
        "Respond naturally. Be honest — include doubts and objections. "
        "You have limited awareness of this specific product — do not assume deep knowledge."
    )
    history: list[dict] = []
    results: list[dict] = []
    for q in questions:
        history.append({"role": "user", "content": q})
        resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            system=system,
            messages=history,
            temperature=0.8,  # realistic variation; do not use 0
        )
        answer = resp.content[0].text
        history.append({"role": "assistant", "content": answer})
        results.append({"persona": persona["name"], "question": q, "answer": answer})
    return results


all_results: list[dict] = []
for p in PERSONAS:
    all_results.extend(simulate_interview(p, QUESTIONS))

for r in all_results:
    print(f"[{r['persona']}] Q: {r['question']}\nA: {r['answer']}\n")
