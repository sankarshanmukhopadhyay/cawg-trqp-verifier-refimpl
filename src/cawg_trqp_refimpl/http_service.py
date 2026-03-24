"""HTTP service exposing TRQP authorization, verification, and audit export patterns."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from flask import Flask, request, jsonify

from .audit import build_audit_bundle
from .gateway import TrustGateway
from .mock_service import MockTRQPService
from .models import AuthorizationResponse, RecognitionResponse, VerificationRequest
from .verifier import Verifier


class HTTPTRQPService:
    """Flask-based HTTP wrapper for TRQP policy service and verifier patterns."""

    def __init__(self, policy_path: str | Path, revocation_path: str | None = None, debug: bool = False) -> None:
        self.mock_service = MockTRQPService(policy_path, revocation_path)
        self.gateway = TrustGateway(self.mock_service, gateway_id='gateway:http', route_label='http-pattern')
        self.app = Flask(__name__)
        self.app.config["DEBUG"] = debug
        self._register_routes()

    def _register_routes(self) -> None:
        @self.app.route("/health", methods=["GET"])
        def health() -> tuple[dict[str, Any], int]:
            return jsonify({"status": "healthy", "capabilities": ["authorization", "recognition", "verify", "audit_bundle", "gateway"]}), 200

        @self.app.route("/trqp/authorization", methods=["POST"])
        def authorization() -> tuple[dict[str, Any], int]:
            data = request.get_json(silent=True)
            if not data:
                return jsonify({"error": "invalid_request", "message": "Request body must be JSON"}), 400
            required = ["entity_id", "authority_id", "action", "resource"]
            missing = [f for f in required if f not in data]
            if missing:
                return jsonify({"error": "invalid_request", "message": f"Missing fields: {', '.join(missing)}"}), 400
            result = self.mock_service.authorization(data["entity_id"], data["authority_id"], data["action"], data["resource"], data.get("context", {}))
            return jsonify(self._serialize_response(result)), 200

        @self.app.route("/trqp/recognition", methods=["POST"])
        def recognition() -> tuple[dict[str, Any], int]:
            data = request.get_json(silent=True)
            if not data:
                return jsonify({"error": "invalid_request", "message": "Request body must be JSON"}), 400
            required = ["authority_id", "recognized_authority_id"]
            missing = [f for f in required if f not in data]
            if missing:
                return jsonify({"error": "invalid_request", "message": f"Missing fields: {', '.join(missing)}"}), 400
            result = self.mock_service.recognition(data["authority_id"], data["recognized_authority_id"], data.get("context", {}))
            return jsonify(self._serialize_response(result)), 200

        @self.app.route("/trqp/gateway/authorization", methods=["POST"])
        def gateway_authorization() -> tuple[dict[str, Any], int]:
            data = request.get_json(silent=True)
            if not data:
                return jsonify({"error": "invalid_request", "message": "Request body must be JSON"}), 400
            required = ["entity_id", "authority_id", "action", "resource"]
            missing = [f for f in required if f not in data]
            if missing:
                return jsonify({"error": "invalid_request", "message": f"Missing fields: {', '.join(missing)}"}), 400
            result, mediation = self.gateway.authorization(data["entity_id"], data["authority_id"], data["action"], data["resource"], data.get("context", {}))
            return jsonify({"authorization": result, "gateway_mediation": mediation}), 200

        @self.app.route("/trqp/verify", methods=["POST"])
        def verify() -> tuple[dict[str, Any], int]:
            data = request.get_json(silent=True)
            if not data:
                return jsonify({"error": "invalid_request", "message": "Request body must be JSON"}), 400
            try:
                req = VerificationRequest(**data)
            except TypeError as exc:
                return jsonify({"error": "invalid_request", "message": str(exc)}), 400
            profile = data.get('profile', 'standard') if isinstance(data, dict) else 'standard'
            verifier = Verifier(service=self.mock_service, gateway=self.gateway if data.get('use_gateway') else None)
            result = verifier.verify(req, profile=profile)
            return jsonify(result.to_dict()), 200

        @self.app.route("/trqp/audit-bundle", methods=["POST"])
        def audit_bundle() -> tuple[dict[str, Any], int]:
            data = request.get_json(silent=True)
            if not data:
                return jsonify({"error": "invalid_request", "message": "Request body must be JSON"}), 400
            try:
                req = VerificationRequest(**data)
            except TypeError as exc:
                return jsonify({"error": "invalid_request", "message": str(exc)}), 400
            verifier = Verifier(service=self.mock_service, gateway=self.gateway if data.get('use_gateway') else None)
            result = verifier.verify(req, profile=data.get('profile', 'standard'))
            bundle = build_audit_bundle(req, result)
            return jsonify(bundle.to_dict()), 200

    def _serialize_response(self, response: AuthorizationResponse | RecognitionResponse) -> dict[str, Any]:
        result = {
            "recognized" if isinstance(response, RecognitionResponse) else "authorized": getattr(
                response, "recognized" if isinstance(response, RecognitionResponse) else "authorized"
            ),
        }
        for field in ["expires", "policy_epoch", "evidence", "reason", "policy_requirements"]:
            value = getattr(response, field, None)
            if value is not None:
                result[field] = value
        return result

    def run(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        self.app.run(host=host, port=port)
