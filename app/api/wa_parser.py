from typing import Any, Dict, List, Tuple


def extract_incoming_text_messages(payload: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """
    Extract incoming text messages from a Meta WhatsApp webhook payload.

    Returns:
        List of tuples: (from_wa_id, text_body, message_id)

    Notes:
        - Handles multiple entry/changes/messages.
        - Ignores non-text message types (image, audio, button, etc.).
        - If payload contains only statuses or other events, returns [].
    """
    out: List[Tuple[str, str, str]] = []

    entries = payload.get("entry") or []
    for entry in entries:
        changes = entry.get("changes") or []
        for change in changes:
            value = change.get("value") or {}
            messages = value.get("messages") or []

            for msg in messages:
                if msg.get("type") != "text":
                    continue

                frm = msg.get("from")
                text = ((msg.get("text") or {}).get("body") or "").strip()
                msg_id = msg.get("id")

                if frm and text and msg_id:
                    out.append((frm, text, msg_id))

    return out
