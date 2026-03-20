from cawg_trqp_refimpl.cache import TTLCache


def test_cache_set_get():
    cache = TTLCache()
    cache.set("k", {"x": 1}, ttl_class="medium")
    assert cache.get("k") == {"x": 1}
