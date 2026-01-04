from fastapi import APIRouter, Request
from app.config.settings import VERIFY_TOKEN

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Verification failed"}


@router.post("/webhook")
async def receive_message(request: Request):
    try:
        payload = await request.json()
    except Exception:
        print("⚠️ Webhook recibido sin JSON")
        return {"status": "ignored"}

    entry = payload.get("entry", [])
    if not entry:
        print("⚠️ Payload sin entry")
        return {"status": "ignored"}

    changes = entry[0].get("changes", [])
    if not changes:
        print("⚠️ Entry sin changes")
        return {"status": "ignored"}

    value = changes[0].get("value", {})

    messages = value.get("messages")
    if not messages:
        # Esto incluye statuses, delivered, read, etc.
        print("ℹ️ Evento sin mensaje (status u otro)")
        return {"status": "ignored"}

    message = messages[0]
    from_number = message.get("from")

    text = message.get("text", {}).get("body")
    if not text:
        print(f"⚠️ Mensaje sin texto desde {from_number}")
        return {"status": "ignored"}

    print(f"📩 Mensaje de {from_number}: {text}")

    # 👉 Aquí luego llamaremos al sales_agent
    return {"status": "received"}
