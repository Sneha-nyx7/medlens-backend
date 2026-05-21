import asyncio


async def run_vision_and_gradcam(image_bytes: bytes):

    await asyncio.sleep(1)

    pathologies = {
        "Atelectasis": 0.88,
        "Effusion": 0.72,
        "Pneumonia": 0.31,
        "Edema": 0.12,
    }

    heatmap_base64 = (
        "data:image/png;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"
        "CAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwAD"
        "hgGAWjR9awAAAABJRU5ErkJggg=="
    )

    return pathologies, heatmap_base64