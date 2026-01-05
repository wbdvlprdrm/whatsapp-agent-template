import httpx

from app.config.settings import WHATSAPP_TOKEN, WHATSAPP_PHONE_ID, WHATSAPP_API_BASE


class WhatsAppService:
    """
    Minimal WhatsApp Cloud API client for sending messages.
    """

    def __init__(self) -> None:
        if not WHATSAPP_API_BASE:
            raise RuntimeError("Missing WHATSAPP_API_BASE in settings")

        if not WHATSAPP_PHONE_ID:
            raise RuntimeError("Missing WHATSAPP_PHONE_ID in settings")

        if not WHATSAPP_TOKEN:
            raise RuntimeError("Missing WHATSAPP_TOKEN in settings")

        self.base_url = WHATSAPP_API_BASE.rstrip("/")
        self.phone_id = WHATSAPP_PHONE_ID
        self.token = WHATSAPP_TOKEN

    async def send_text(self, to: str, text: str) -> dict:
        """
        Sends a WhatsApp text message.

        Args:
            to: WhatsApp user phone in international format (wa_id), e.g. '5037xxxxxxx'
            text: message body
        Returns:
            Meta API JSON response
        Raises:
            httpx.HTTPStatusError on non-2xx
        """
        url = f"{self.base_url}/{self.phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text},
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()
