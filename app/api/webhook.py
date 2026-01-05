from fastapi import APIRouter, Request

from app.config.settings import VERIFY_TOKEN
from app.api.wa_parser import extract_incoming_text_messages
from app.services.dedupe import InMemoryDedupe
from app.services.whatsapp import WhatsAppService
from app.agents.sales_agent import SalesAgent

router = APIRouter()

# Singletons (MVP)
dedupe = InMemoryDedupe()
wa = WhatsAppService()
agent = SalesAgent()


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
    # raw body for future signature verification (we'll add in next step)
    try:
        payload = await request.json()
    except Exception:
        print("⚠️ Webhook recibido sin JSON")
        return {"status": "ignored"}

    messages = extract_incoming_text_messages(payload)

    if not messages:
        # Esto incluye statuses, delivered, read, etc.
        print("ℹ️ Evento sin mensaje de texto (status u otro)")
        return {"status": "ignored"}

    processed = 0

    for from_number, text, message_id in messages:
        # dedupe to avoid double replies
        if dedupe.seen(message_id):
            continue

        print(f"📩 Mensaje de {from_number}: {text}")

        reply = agent.handle_message(text)
        await wa.send_text(to=from_number, text=reply)

        processed += 1

    return {"status": "received", "processed": processed}
