# purpose: Pre-existing template carried into the llm-powered-conversational-ai methodology
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml for produces=spec
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

"""
Minimal Anthropic SDK multi-turn conversation prototype.
Replace SYSTEM template variables before use.
Usage: python conversation-loop.py
Requires: pip install anthropic
"""
import anthropic

client = anthropic.Anthropic()

# Replace these before use
PERSONA_NAME = "Aria"
PRODUCT_NAME = "Acme Support"
ALLOWED_TOPICS = "account management, billing, product features"
FORBIDDEN_TOPICS = "competitor products, legal advice, medical advice"

SYSTEM = f"""You are {PERSONA_NAME}, an assistant for {PRODUCT_NAME}.
You help users with: {ALLOWED_TOPICS}.
You must not discuss: {FORBIDDEN_TOPICS}.
If the user asks about something outside your scope, say:
"I can help with {ALLOWED_TOPICS}. Is there something in that area I can assist with?"
Keep responses under 150 words. Be conversational, not formal.
If the user is angry or distressed, acknowledge their feelings and offer to connect them with a human agent."""


def chat(history: list, user_msg: str) -> str:
    history.append({"role": "user", "content": user_msg})
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        system=SYSTEM,
        messages=history,
    )
    assistant_msg = response.content[0].text
    history.append({"role": "assistant", "content": assistant_msg})
    return assistant_msg


def main():
    history = []
    print(f"[{PERSONA_NAME}] Hi! I'm {PERSONA_NAME}. How can I help you today?")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print(f"[{PERSONA_NAME}] Goodbye!")
            break
        reply = chat(history, user_input)
        print(f"[{PERSONA_NAME}] {reply}")


if __name__ == "__main__":
    main()
