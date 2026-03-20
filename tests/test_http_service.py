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
    """Tests for HTTP TRQP service."""

    @pytest.fixture
    def client(self):
        """Create Flask test client."""
        service = HTTPTRQPService(
            policy_path=Path("data/policies.json"),
            revocation_path=Path("data/revocations.json"),
            debug=True
        )
        service.app.config["TESTING"] = True
        return service.app.test_client()

    def test_health_check(self, client):
        """Health endpoint should return healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json()["status"] == "healthy"

    def test_authorization_endpoint_valid(self, client):
        """Authorization endpoint should accept valid request."""
        payload = {
            "entity_id": "did:web:example.com",
            "authority_id": "did:web:authority.example",
            "action": "verify",
            "resource": "manifest",
            "context": {}
        }
        response = client.post(
            "/trqp/authorization",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "authorized" in data

    def test_authorization_endpoint_missing_fields(self, client):
        """Authorization endpoint should reject missing required fields."""
        payload = {
            "entity_id": "did:web:example.com",
            # Missing authority_id, action, resource
        }
        response = client.post(
            "/trqp/authorization",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_recognition_endpoint_valid(self, client):
        """Recognition endpoint should accept valid request."""
        payload = {
            "authority_id": "did:web:authority.example",
            "recognized_authority_id": "did:web:other.example",
            "context": {}
        }
        response = client.post(
            "/trqp/recognition",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "recognized" in data

    def test_recognition_endpoint_missing_fields(self, client):
        """Recognition endpoint should reject missing required fields."""
        payload = {
            "authority_id": "did:web:authority.example",
            # Missing recognized_authority_id
        }
        response = client.post(
            "/trqp/recognition",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 400

    def test_authorization_invalid_json(self, client):
        """Endpoint should reject invalid JSON."""
        response = client.post(
            "/trqp/authorization",
            data="not json",
            content_type="application/json"
        )
        # Flask will return 400 for parse error
        assert response.status_code in [400, 500]
