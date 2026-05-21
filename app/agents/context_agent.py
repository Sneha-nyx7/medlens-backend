import asyncio


async def run_biomedbert(clinical_note: str):

    await asyncio.sleep(0.5)

    embedding = [0.015] * 768

    entities = {
        "age": 65,
        "sex": "Male",
        "symptoms": ["cough", "fever"],
        "clinical_note": clinical_note,
    }

    return embedding, entities
