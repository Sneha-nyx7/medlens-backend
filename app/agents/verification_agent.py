import asyncio


async def verify_and_triage(
    report: dict,
    passages: list,
    pathologies: dict,
):

    await asyncio.sleep(0.3)

    if pathologies.get("Pneumothorax", 0) > 0.5:
        triage = "STAT"

    elif (
        pathologies.get("Atelectasis", 0) > 0.5
        or pathologies.get("Pneumonia", 0) > 0.5
    ):
        triage = "URGENT"

    else:
        triage = "ROUTINE"

    justification = (
        f"Triage classified as {triage} "
        f"based on detected pathology scores."
    )

    return triage, justification