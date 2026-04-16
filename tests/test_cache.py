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
