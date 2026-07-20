"""HTTP service exposing TRQP authorization, verification, and audit export patterns."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from flask import Flask, request, jsonify

from .audit import build_audit_bundle
from .gateway import TrustGateway
from .mock_service import MockTRQPService
from .models import AuthorizationResponse, RecognitionResponse, VerificationRequest
from .profile import VerificationProfileError, load_api_profile
from .verifier import Verifier

MAX_REQUEST_BYTES = 64 * 1024


class HTTPTRQPService:
    """Flask-based HTTP wrapper for TRQP policy service and verifier patterns."""

    def __init__(self, policy_path: str | Path, revocation_path: str | None = None, debug: bool = False) -> None:
        self.mock_service = MockTRQPService(policy_path, revocation_path)
        self.gateway = TrustGateway(self.mock_service, gateway_id='gateway:http', route_label='http-pattern')
        self.app = Flask(__name__)
        self.app.config["DEBUG"] = debug
        self.app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_BYTES
        self._register_routes()

    def _register_routes(self) -> None:
        @self.app.errorhandler(413)
        def too_large(_: Exception) -> tuple[Any, int]:
            return jsonify({"error": "request_too_large", "message": f"Request body exceeds {MAX_REQUEST_BYTES} bytes"}), 413

        @self.app.route("/health", methods=["GET"])
        def health() -> tuple[dict[str, Any], int]:
            return jsonify({"status": "healthy", "capabilities": ["authorization", "recognition", "verify", "audit_bundle", "gateway"]}), 200

        @self.app.route("/trqp/authorization", methods=["POST"])
        def authorization() -> tuple[dict[str, Any], int]:
            data, error = self._json_body()
            if error:
                return error
            required = ["entity_id", "authority_id", "action", "resource"]
            missing = [f for f in required if f not in data]
            if missing:
                return jsonify({"error": "invalid_request", "message": f"Missing fields: {', '.join(missing)}"}), 400
            field_error = self._require_strings(data, required)
            if field_error:
                return field_error
            result = self.mock_service.authorization(data["entity_id"], data["authority_id"], data["action"], data["resource"], data.get("context", {}))
            return jsonify(self._serialize_response(result)), 200

        @self.app.route("/trqp/recognition", methods=["POST"])
        def recognition() -> tuple[dict[str, Any], int]:
            data, error = self._json_body()
            if error:
                return error
            required = ["authority_id", "recognized_authority_id"]
            missing = [f for f in required if f not in data]
            if missing:
                return jsonify({"error": "invalid_request", "message": f"Missing fields: {', '.join(missing)}"}), 400
            field_error = self._require_strings(data, required)
            if field_error:
                return field_error
            result = self.mock_service.recognition(data["authority_id"], data["recognized_authority_id"], data.get("context", {}))
            return jsonify(self._serialize_response(result)), 200

        @self.app.route("/trqp/gateway/authorization", methods=["POST"])
        def gateway_authorization() -> tuple[dict[str, Any], int]:
            data, error = self._json_body()
            if error:
                return error
            required = ["entity_id", "authority_id", "action", "resource"]
            missing = [f for f in required if f not in data]
            if missing:
                return jsonify({"error": "invalid_request", "message": f"Missing fields: {', '.join(missing)}"}), 400
            field_error = self._require_strings(data, required)
            if field_error:
                return field_error
            result, mediation = self.gateway.authorization(data["entity_id"], data["authority_id"], data["action"], data["resource"], data.get("context", {}))
            return jsonify({"authorization": result, "gateway_mediation": mediation}), 200

        @self.app.route("/trqp/verify", methods=["POST"])
        def verify() -> tuple[dict[str, Any], int]:
            data, error = self._json_body()
            if error:
                return error
            try:
                req = VerificationRequest(**self._verification_request_fields(data))
                profile = self._resolve_api_profile(data)
            except (TypeError, VerificationProfileError, ValueError) as exc:
                return jsonify({"error": "invalid_request", "message": str(exc)}), 400
            verifier = Verifier(service=self.mock_service, gateway=self.gateway if data.get('use_gateway') else None)
            result = verifier.verify(req, profile=profile)
            self._emit_audit_event("verify", profile, bool(data.get("use_gateway")), result.to_dict())
            return jsonify(result.to_dict()), 200

        @self.app.route("/trqp/audit-bundle", methods=["POST"])
        def audit_bundle() -> tuple[dict[str, Any], int]:
            data, error = self._json_body()
            if error:
                return error
            try:
                req = VerificationRequest(**self._verification_request_fields(data))
                profile = self._resolve_api_profile(data)
            except (TypeError, VerificationProfileError, ValueError) as exc:
                return jsonify({"error": "invalid_request", "message": str(exc)}), 400
            use_gateway = bool(data.get('use_gateway'))
            verifier = Verifier(service=self.mock_service, gateway=self.gateway if use_gateway else None)
            result = verifier.verify(req, profile=profile)
            self._emit_audit_event("audit_bundle", profile, use_gateway, result.to_dict())
            try:
                bundle = build_audit_bundle(req, result, profile=profile, use_gateway=use_gateway)
            except ValueError as exc:
                return jsonify({"error": "invalid_request", "message": str(exc)}), 400
            return jsonify(bundle.to_dict()), 200

    def _json_body(self) -> tuple[dict[str, Any], tuple[Any, int] | None]:
        if not request.is_json:
            return {}, (jsonify({"error": "invalid_request", "message": "Request content type must be application/json"}), 415)
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return {}, (jsonify({"error": "invalid_request", "message": "Request body must be a JSON object"}), 400)
        return data, None

    def _require_strings(self, data: dict[str, Any], fields: list[str]) -> tuple[Any, int] | None:
        invalid = [field for field in fields if not isinstance(data.get(field), str) or not data.get(field)]
        if invalid:
            return jsonify({"error": "invalid_request", "message": f"Fields must be non-empty strings: {', '.join(invalid)}"}), 400
        if "context" in data and not isinstance(data["context"], dict):
            return jsonify({"error": "invalid_request", "message": "context must be a JSON object"}), 400
        return None

    def _resolve_api_profile(self, data: dict[str, Any]) -> Any:
        overlays = data.get("overlays", [])
        if overlays and not isinstance(overlays, list):
            raise ValueError("overlays must be a list of built-in overlay names")
        return load_api_profile(data.get("profile", "standard"), overlays=overlays)

    def _verification_request_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            'asset_id', 'integrity_ok', 'entity_id', 'authority_id', 'issuer_id',
            'action', 'resource', 'context', 'process_evidence'
        }
        fields = {key: value for key, value in data.items() if key in allowed}
        fields.setdefault("issuer_id", None)
        required = {"asset_id", "integrity_ok", "entity_id", "authority_id", "action", "resource"}
        missing = sorted(required - set(fields))
        if missing:
            raise ValueError(f"Missing fields: {', '.join(missing)}")
        string_fields = ["asset_id", "entity_id", "authority_id", "action", "resource"]
        invalid = [field for field in string_fields if not isinstance(fields.get(field), str) or not fields.get(field)]
        if invalid:
            raise ValueError(f"Fields must be non-empty strings: {', '.join(invalid)}")
        if "issuer_id" in fields and fields["issuer_id"] is not None and not isinstance(fields["issuer_id"], str):
            raise ValueError("issuer_id must be a string or null")
        if not isinstance(fields.get("integrity_ok"), bool):
            raise ValueError("integrity_ok must be a boolean")
        if "context" in fields and not isinstance(fields["context"], dict):
            raise ValueError("context must be a JSON object")
        if "process_evidence" in fields and fields["process_evidence"] is not None and not isinstance(fields["process_evidence"], dict):
            raise ValueError("process_evidence must be a JSON object or null")
        return fields

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

    def _emit_audit_event(self, event_type: str, profile: Any, use_gateway: bool, result: dict[str, Any]) -> None:
        event = {
            "event_type": event_type,
            "profile": getattr(profile, "id", str(profile)),
            "use_gateway": use_gateway,
            "verification_mode": result.get("verification_mode"),
            "trust_outcome": result.get("trust_outcome"),
            "policy_freshness": result.get("policy_freshness"),
        }
        self.app.logger.info("cawg_trqp_http_audit %s", json.dumps(event, sort_keys=True))

    def run(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        self.app.run(host=host, port=port)
