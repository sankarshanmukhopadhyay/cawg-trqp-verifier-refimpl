"""Tests for HTTP TRQP service endpoints."""

import json
from pathlib import Path
import pytest

try:
    from flask import Flask
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

if HAS_FLASK:
    from cawg_trqp_refimpl.http_service import HTTPTRQPService


@pytest.mark.skipif(not HAS_FLASK, reason="Flask not installed")
class TestHTTPService:
    @pytest.fixture
    def client(self):
        service = HTTPTRQPService(
            policy_path=Path("data/policies.json"),
            revocation_path=Path("data/revocations.json"),
            debug=True,
        )
        service.app.config["TESTING"] = True
        return service.app.test_client()

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json()["status"] == "healthy"

    def test_authorization_endpoint_valid(self, client):
        payload = {"entity_id": "did:web:publisher.example", "authority_id": "did:web:media-registry.example", "action": "publish", "resource": "cawg:news-content", "context": {"jurisdiction": "IN"}}
        response = client.post("/trqp/authorization", data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        assert "authorized" in response.get_json()

    def test_gateway_authorization_endpoint_valid(self, client):
        payload = {"entity_id": "did:web:publisher.example", "authority_id": "did:web:media-registry.example", "action": "publish", "resource": "cawg:news-content", "context": {"jurisdiction": "IN"}}
        response = client.post("/trqp/gateway/authorization", data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        data = response.get_json()
        assert "authorization" in data and "gateway_mediation" in data

    def test_verify_endpoint(self, client):
        payload = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        payload["use_gateway"] = True
        response = client.post("/trqp/verify", data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        data = response.get_json()
        assert data["verification_mode"] == "gateway_mediated"
        assert data["trust_outcome"] in {"trusted", "trusted_cached"}

    def test_audit_bundle_endpoint(self, client):
        payload = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        payload["use_gateway"] = True
        response = client.post("/trqp/audit-bundle", data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        data = response.get_json()
        assert data["bundle_type"] == "cawg-trqp-audit-bundle"
