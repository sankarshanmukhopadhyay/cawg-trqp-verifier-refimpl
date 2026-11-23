from cawg_trqp_refimpl.cache import TTLCache


def test_cache_set_get():
    cache = TTLCache()
    cache.set("k", {"x": 1}, ttl_class="medium")
    assert cache.get("k") == {"x": 1}


def test_cache_evicts_least_recently_used_when_maxsize_reached():
    cache = TTLCache(maxsize=2)
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.get("a") == 1
    cache.set("c", 3)
    assert cache.get("a") == 1
    assert cache.get("b") is None
    assert cache.get("c") == 3


def test_cache_metrics_and_clear():
    cache = TTLCache(maxsize=2)
    assert cache.get("missing") is None
    cache.set("a", 1)
    assert cache.get("a") == 1
    stats = cache.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    cache.clear()
    assert cache.stats()["entries"] == 0


def test_cache_expiry_boundary_is_exclusive(monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("cawg_trqp_refimpl.cache.time.time", lambda: now[0])
    cache = TTLCache()
    cache.set("authority", {"authorized": True}, ttl_class="medium")
    now[0] += 3599
    assert cache.get("authority") == {"authorized": True}
    now[0] += 1
    value, metadata = cache.get_with_metadata("authority")
    assert value is None
    assert metadata == {"cache_hit": False, "expired": True}
