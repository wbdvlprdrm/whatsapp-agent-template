import hmac
import hashlib
from fastapi import Request

from app.config.settings import META_APP_SECRET, APP_ENV


def verify_meta_signature(request: Request, raw_body: bytes) -> bool:
    """
    Verifies X-Hub-Signature-256 from Meta.

    In development (APP_ENV != "production"), you can skip enforcing it.
    In production, you should require META_APP_SECRET and a valid signature.
    """
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature or not signature.startswith("sha256="):
        return False

    if not META_APP_SECRET:
        return False

    given = signature.split("=", 1)[1].strip()
    secret = META_APP_SECRET.encode("utf-8")
    computed = hmac.new(secret, msg=raw_body, digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, given)
