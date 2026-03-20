"""HTTP service exposing TRQP authorization and recognition endpoints.

This module provides Flask-based HTTP endpoints for the TRQP protocol,
enabling network-based access to policy queries. It wraps the MockTRQPService
and provides standard HTTP transport, error handling, and response formatting.

References:
- TRQP v2.0 specification: https://trustoverip.github.io/tswg-trust-registry-protocol/
"""

from __future__ import annotations
import json
from typing import Any
from flask import Flask, request, jsonify
from .mock_service import MockTRQPService
from .models import AuthorizationResponse, RecognitionResponse


class HTTPTRQPService:
    """Flask-based HTTP wrapper for TRQP policy service."""

    def __init__(self, policy_path: str, revocation_path: str | None = None, debug: bool = False) -> None:
        """Initialize HTTP service with TRQP policy backend.
        
        Args:
            policy_path: Path to policies.json file
            revocation_path: Optional path to revocations.json file
            debug: Enable Flask debug mode
        """
        self.mock_service = MockTRQPService(policy_path, revocation_path)
        self.app = Flask(__name__)
        self.app.config["DEBUG"] = debug
        self._register_routes()

    def _register_routes(self) -> None:
        """Register HTTP endpoints for TRQP operations."""

        @self.app.route("/health", methods=["GET"])
        def health() -> dict[str, str]:
            """Health check endpoint."""
            return jsonify({"status": "healthy"}), 200

        @self.app.route("/trqp/authorization", methods=["POST"])
        def authorization() -> tuple[dict[str, Any], int]:
            """TRQP authorization endpoint.
            
            Request body:
            {
                "entity_id": "...",
                "authority_id": "...",
                "action": "...",
                "resource": "...",
                "context": {...}
            }
            
            Returns:
                Serialized AuthorizationResponse with HTTP status.
            """
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "invalid_request", "message": "Request body must be JSON"}), 400

                # Validate required fields
                required = ["entity_id", "authority_id", "action", "resource"]
                missing = [f for f in required if f not in data]
                if missing:
                    return (
                        jsonify({"error": "invalid_request", "message": f"Missing fields: {', '.join(missing)}"}),
                        400,
                    )

                result = self.mock_service.authorization(
                    entity_id=data.get("entity_id"),
                    authority_id=data.get("authority_id"),
                    action=data.get("action"),
                    resource=data.get("resource"),
                    context=data.get("context", {}),
                )

                return jsonify(self._serialize_response(result)), 200

            except Exception as e:
                return jsonify({"error": "server_error", "message": str(e)}), 500

        @self.app.route("/trqp/recognition", methods=["POST"])
        def recognition() -> tuple[dict[str, Any], int]:
            """TRQP recognition endpoint.
            
            Request body:
            {
                "authority_id": "...",
                "recognized_authority_id": "...",
                "context": {...}
            }
            
            Returns:
                Serialized RecognitionResponse with HTTP status.
            """
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "invalid_request", "message": "Request body must be JSON"}), 400

                # Validate required fields
                required = ["authority_id", "recognized_authority_id"]
                missing = [f for f in required if f not in data]
                if missing:
                    return (
                        jsonify({"error": "invalid_request", "message": f"Missing fields: {', '.join(missing)}"}),
                        400,
                    )

                result = self.mock_service.recognition(
                    authority_id=data.get("authority_id"),
                    recognized_authority_id=data.get("recognized_authority_id"),
                    context=data.get("context", {}),
                )

                return jsonify(self._serialize_response(result)), 200

            except Exception as e:
                return jsonify({"error": "server_error", "message": str(e)}), 500

    def _serialize_response(self, response: AuthorizationResponse | RecognitionResponse) -> dict[str, Any]:
        """Convert response object to JSON-serializable dict."""
        result = {
            "recognized" if isinstance(response, RecognitionResponse) else "authorized": getattr(
                response, "recognized" if isinstance(response, RecognitionResponse) else "authorized"
            ),
        }

        for field in ["expires", "policy_epoch", "evidence", "reason"]:
            value = getattr(response, field, None)
            if value is not None:
                result[field] = value

        return result

    def run(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        """Start the HTTP service.
        
        Args:
            host: Bind address
            port: Bind port
        """
        self.app.run(host=host, port=port)
