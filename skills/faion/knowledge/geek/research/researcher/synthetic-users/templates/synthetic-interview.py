# synthetic_interview.py — generate synthetic user profiles and simulate responses
# Requires: pip install anthropic

import anthropic

client = anthropic.Anthropic()


def generate_profile(icp: str) -> str:
    """Generate one synthetic user profile for the given ICP description."""
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": (
                f"Create a synthetic user profile for: {icp}. "
                "Include: name, age, role, company size, primary job-to-be-done, "
                "tech comfort (1-5), top 3 frustrations with current solution, "
                "budget authority (yes/no). "
                "Be specific and internally consistent. "
                "Do NOT default to generic UX tropes — make this person distinct."
            )
        }]
    )
    return msg.content[0].text


def simulate_response(profile: str, question: str) -> str:
    """Simulate how the given profile would answer a research question."""
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f"You are this person:\n{profile}\n\n"
                f"Answer this research question as them: {question}\n"
                "Be honest. Express skepticism if you feel it. "
                "Do not manufacture enthusiasm. "
                "If you are neutral or negative, say so."
            )
        }]
    )
    return msg.content[0].text


def adversarial_response(profile: str, product: str) -> str:
    """Generate a skeptical 'why would I NOT buy this?' response to counter positive bias."""
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f"You are this person:\n{profile}\n\n"
                f"As a skeptical user, explain why you would NOT buy {product}. "
                "Be specific about your objections. This is not a role to be supportive."
            )
        }]
    )
    return msg.content[0].text
