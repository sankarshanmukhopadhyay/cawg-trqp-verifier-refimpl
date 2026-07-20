import json
from pathlib import Path

from cawg_trqp_refimpl.http_service import HTTPTRQPService


def test_http_verify_reuses_cache_across_requests():
    service = HTTPTRQPService(Path("data/policies.json"), Path("data/revocations.json"))
    client = service.app.test_client()
    payload = json.loads(Path("examples/verification_request.json").read_text())
    first = client.post("/trqp/verify", json=payload)
    second = client.post("/trqp/verify", json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert service.cache.stats()["hits"] >= 1
    assert "Authorization cache hit" in second.get_json()["explanations"]


def test_gateway_and_direct_verifiers_share_l1_cache_without_request_scope_loss():
    service = HTTPTRQPService(Path("data/policies.json"), Path("data/revocations.json"))
    assert service.verifier.cache is service.cache
    assert service.gateway_verifier.cache is service.cache
