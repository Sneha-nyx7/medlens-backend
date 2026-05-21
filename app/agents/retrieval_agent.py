import asyncio


async def query_chromadb(entities: dict, embedding: list):

    await asyncio.sleep(0.3)

    passages = [
        {
            "passage_id": "rad_001",
            "source": "Radiopaedia",
            "passage": (
                "Atelectasis refers to partial collapse "
                "of lung tissue commonly visible as "
                "linear opacity on chest radiograph."
            ),
        },
        {
            "passage_id": "nih_002",
            "source": "NIH",
            "passage": (
                "Pleural effusion appears as fluid "
                "accumulation in pleural space."
            ),
        },
    ]

    return passages