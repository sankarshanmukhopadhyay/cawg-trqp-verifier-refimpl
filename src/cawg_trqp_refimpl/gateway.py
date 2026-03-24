from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .mock_service import MockTRQPService


class TrustGateway:
    """Remote policy mediation component for verifier-side trust orchestration.

    The gateway is intentionally simple in the reference implementation. It sits
    between verifier logic and the underlying TRQP service so deployments can
    centralize policy mediation, auditing, and interoperability routing without
    changing verifier behavior.
    """

    def __init__(self, service: MockTRQPService, gateway_id: str = 'gateway:default', route_label: str = 'default') -> None:
        self.service = service
        self.gateway_id = gateway_id
        self.route_label = route_label

    def authorization(self, entity_id: str, authority_id: str, action: str, resource: str, context: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        response = asdict(self.service.authorization(entity_id, authority_id, action, resource, context))
        mediation = {
            'gateway_id': self.gateway_id,
            'route_label': self.route_label,
            'mode': 'remote_policy_mediation',
            'target_authority_id': authority_id,
            'decision_type': 'authorization',
        }
        return response, mediation

    def recognition(self, authority_id: str, recognized_authority_id: str, context: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        response = asdict(self.service.recognition(authority_id, recognized_authority_id, context))
        mediation = {
            'gateway_id': self.gateway_id,
            'route_label': self.route_label,
            'mode': 'remote_policy_mediation',
            'target_authority_id': authority_id,
            'decision_type': 'recognition',
        }
        return response, mediation
