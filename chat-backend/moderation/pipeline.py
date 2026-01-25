import httpx
from .auto_moderator import auto_moderate
from .risk import update_user_risk

ML_URL = "http://127.0.0.1:8001/predict"

async def moderate_message(data):
    async with httpx.AsyncClient() as client:
        resp = await client.post(ML_URL, json={"text": data["message"]})
    
    result = resp.json()
    toxicity = result["toxicity"]
    scores = result["scores"]

    decision = auto_moderate(toxicity, scores)

    # update user risk
    await update_user_risk(data["user"], toxicity)

    return {
        "user": data["user"],
        "message": data["message"],
        "toxicity": toxicity,
        "scores": scores,
        "status": decision["status"],
        "moderated_text": decision["text"],
        "reason": decision["reason"]

    }
