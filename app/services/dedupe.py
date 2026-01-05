import time
from typing import Dict


class InMemoryDedupe:
    """
    Simple in-memory dedupe for message ids.

    NOTE: Works for single-process MVP. For production / multiple replicas,
    replace with Redis or DB (e.g. SETNX with TTL).
    """

    def __init__(self, ttl_seconds: int = 86400) -> None:
        self.ttl = ttl_seconds
        self._store: Dict[str, float] = {}

    def seen(self, key: str) -> bool:
        now = time.time()

        # cheap cleanup
        expired = [k for k, exp in self._store.items() if exp < now]
        for k in expired:
            self._store.pop(k, None)

        if key in self._store:
            return True

        self._store[key] = now + self.ttl
        return False
