from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Any


TTL_BY_CLASS = {
    "short": 300,
    "medium": 3600,
    "long": 86400,
}


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class TTLCache:
    def __init__(self) -> None:
        self._store: dict[str, CacheEntry] = {}

    @property
    def cache(self) -> dict[str, CacheEntry]:
        return self._store

    def set(self, key: str, value: Any, ttl_class: str = "medium") -> None:
        ttl_seconds = TTL_BY_CLASS.get(ttl_class, TTL_BY_CLASS["medium"])
        self._store[key] = CacheEntry(value=value, expires_at=time.time() + ttl_seconds)

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        if time.time() > entry.expires_at:
            self._store.pop(key, None)
            return None
        return entry.value

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)
