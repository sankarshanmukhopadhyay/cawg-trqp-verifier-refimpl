from __future__ import annotations
import time
from collections import OrderedDict
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
    def __init__(self, maxsize: int = 1024) -> None:
        self.maxsize = maxsize
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()

    @property
    def cache(self) -> OrderedDict[str, CacheEntry]:
        return self._store

    def _purge_expired(self) -> None:
        now = time.time()
        expired_keys = [key for key, entry in self._store.items() if now > entry.expires_at]
        for key in expired_keys:
            self._store.pop(key, None)

    def _evict_if_needed(self) -> None:
        self._purge_expired()
        while len(self._store) > self.maxsize:
            self._store.popitem(last=False)

    def set(self, key: str, value: Any, ttl_class: str = "medium") -> None:
        ttl_seconds = TTL_BY_CLASS.get(ttl_class, TTL_BY_CLASS["medium"])
        self._store.pop(key, None)
        self._store[key] = CacheEntry(value=value, expires_at=time.time() + ttl_seconds)
        self._evict_if_needed()

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        if time.time() > entry.expires_at:
            self._store.pop(key, None)
            return None
        self._store.move_to_end(key)
        return entry.value

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)
