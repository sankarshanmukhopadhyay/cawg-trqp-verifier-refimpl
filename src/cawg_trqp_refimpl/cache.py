from __future__ import annotations

import time
from collections import OrderedDict
from dataclasses import dataclass
from threading import RLock
from typing import Any, Protocol


TTL_BY_CLASS = {
    "short": 300,
    "medium": 3600,
    "long": 86400,
}


class DecisionCache(Protocol):
    """Minimal cache contract used by the verifier.

    Implementations may be in-process or distributed, but must preserve
    deterministic keys and bounded expiry semantics.
    """

    def set(self, key: str, value: Any, ttl_class: str = "medium") -> None: ...
    def get(self, key: str) -> Any | None: ...
    def invalidate(self, key: str) -> None: ...


@dataclass
class CacheEntry:
    value: Any
    cached_at: float
    expires_at: float
    ttl_class: str


class NoOpDecisionCache:
    """Explicit cache-disabled adapter for live-only deployments and tests."""

    def set(self, key: str, value: Any, ttl_class: str = "medium") -> None:
        return None

    def get(self, key: str) -> Any | None:
        return None

    def invalidate(self, key: str) -> None:
        return None


class TTLCache:
    """Thread-safe bounded LRU cache with simple operational metrics.

    This is an L1 reference adapter. Production deployments may replace it
    with a shared L2 implementation that satisfies :class:`DecisionCache`.
    """

    def __init__(self, maxsize: int = 1024) -> None:
        if maxsize < 1:
            raise ValueError("maxsize must be at least 1")
        self.maxsize = maxsize
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = RLock()
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0

    @property
    def cache(self) -> OrderedDict[str, CacheEntry]:
        return self._store

    def _purge_expired_locked(self) -> None:
        now = time.time()
        expired_keys = [key for key, entry in self._store.items() if now > entry.expires_at]
        for key in expired_keys:
            self._store.pop(key, None)
            self._expirations += 1

    def _evict_if_needed_locked(self) -> None:
        self._purge_expired_locked()
        while len(self._store) > self.maxsize:
            self._store.popitem(last=False)
            self._evictions += 1

    def set(self, key: str, value: Any, ttl_class: str = "medium") -> None:
        ttl_seconds = TTL_BY_CLASS.get(ttl_class, TTL_BY_CLASS["medium"])
        now = time.time()
        with self._lock:
            self._store.pop(key, None)
            self._store[key] = CacheEntry(
                value=value,
                cached_at=now,
                expires_at=now + ttl_seconds,
                ttl_class=ttl_class,
            )
            self._evict_if_needed_locked()

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None
            if time.time() > entry.expires_at:
                self._store.pop(key, None)
                self._expirations += 1
                self._misses += 1
                return None
            self._store.move_to_end(key)
            self._hits += 1
            return entry.value

    def invalidate(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def stats(self) -> dict[str, int | float]:
        with self._lock:
            self._purge_expired_locked()
            requests = self._hits + self._misses
            return {
                "entries": len(self._store),
                "maxsize": self.maxsize,
                "hits": self._hits,
                "misses": self._misses,
                "evictions": self._evictions,
                "expirations": self._expirations,
                "hit_ratio": (self._hits / requests) if requests else 0.0,
            }
