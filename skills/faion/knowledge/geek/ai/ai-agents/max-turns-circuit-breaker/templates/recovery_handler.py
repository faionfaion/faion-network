"""Recovery handler for MaxTurnsExceeded.

Pattern: cap the main agent's max_turns aggressively; on overflow, hand the
partial trajectory to a small/cheap model that produces a one-sentence summary
of what was tried so the user gets a graceful reply instead of a 500.
"""
from agents import Agent, Runner
from agents.exceptions import MaxTurnsExceeded
from agents.models import ModelSettings


# Cheap model — this only ever runs for one turn, summarizing a trace.
recovery_agent = Agent(
    name="Recovery",
    model="gpt-4.1-mini",
    instructions=(
        "You receive a partial agent trajectory (tool calls + observations). "
        "Return one sentence describing what was attempted and what blocked progress. "
        "Do not invent a final answer — only summarize."
    ),
    model_settings=ModelSettings(temperature=0.0),
)


async def run_with_recovery(agent: Agent, user_msg: str, max_turns: int = 8) -> str:
    """Run agent with explicit cap; convert timeout to graceful summary."""
    try:
        res = await Runner.run(agent, user_msg, max_turns=max_turns)
        return res.final_output
    except MaxTurnsExceeded as e:
        # Preserve trace id (e.run_data) for ops, return graceful reply.
        recap = await Runner.run(
            recovery_agent,
            e.run_data.to_input_list(),
            max_turns=1,
        )
        return f"I got stuck after {max_turns} turns. {recap.final_output}"
