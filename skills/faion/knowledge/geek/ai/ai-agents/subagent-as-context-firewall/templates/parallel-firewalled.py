import asyncio

async def parallel_investigation(questions: list[str]) -> list[SubagentReport]:
    return await asyncio.gather(*[
        investigator.run(q) for q in questions
    ])

# Parent's context grows by SUM(reports) — typically < 5K total even for 5 subagents
