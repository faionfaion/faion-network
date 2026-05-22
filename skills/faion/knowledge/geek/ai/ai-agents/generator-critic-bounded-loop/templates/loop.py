# purpose: reference loop with hard cap, delta exit, structured critic
# consumes: prompt + generator function + critic function
# produces: final output + loop trace
# depends-on: templates/critic_schema.py
# token-budget-impact: cheap path 1 generator + 1 critic call; deep path up to 3 of each
"""Reference generator-critic loop with three exit conditions.

Exit priority:
  1. critic.should_continue is False
  2. score delta below EPSILON for >=1 iteration after the first
  3. iteration count reaches MAX_ITERS

Caller supplies generate(prompt, feedback=None) -> str
and critic(output, prompt) -> CriticVerdict.
"""
from typing import Callable

from .critic_schema import CriticVerdict

MAX_ITERS = 3
EPSILON = 0.02


def generator_critic_loop(
    prompt: str,
    generate: Callable[..., str],
    critic: Callable[[str, str], CriticVerdict],
    max_iters: int = MAX_ITERS,
    epsilon: float = EPSILON,
) -> str:
    """Run the bounded loop. Returns the final output."""
    output = generate(prompt)
    prev_score: float | None = None

    for i in range(max_iters):
        verdict = critic(output, prompt)

        # Exit 1: critic veto.
        if not verdict.should_continue:
            return output

        # Exit 2: plateau (only after the first iteration).
        if prev_score is not None and abs(verdict.score - prev_score) < epsilon:
            return output

        # Otherwise, regenerate with feedback.
        output = generate(prompt, feedback=verdict.feedback)
        prev_score = verdict.score

    # Exit 3: hit the hard cap.
    return output
