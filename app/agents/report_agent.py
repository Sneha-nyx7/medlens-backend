import asyncio


async def generate_llm_report(
    pathologies: dict,
    entities: dict,
    passages: list,
):

    await asyncio.sleep(1)

    report = {
        "impression": (
            "Findings suggest left lower lobe atelectasis "
            "with mild pleural effusion."
        ),
        "findings": (
            "Linear opacity noted in left lower lung zone. "
            "Mild pleural fluid accumulation observed."
        ),
        "recommendations": (
            "Recommend clinical correlation and "
            "follow-up chest radiograph."
        ),
    }

    citations = [
        {
            "marker": "[1]",
            "passage_id": "rad_001",
        },
        {
            "marker": "[2]",
            "passage_id": "nih_002",
        },
    ]

    return report, citations