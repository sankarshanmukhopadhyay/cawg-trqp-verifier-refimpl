from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .mock_service import MockTRQPService
from .transport import FeedTransportMetadata


class TrustGateway:
    """Remote policy mediation component for verifier-side trust orchestration.

    The gateway supports deterministic route selection and exports route/feed
    evidence so mediated authorization can be replayed and audited.
    """

    def __init__(
        self,
        service: MockTRQPService | None = None,
        gateway_id: str = 'gateway:default',
        route_label: str = 'default',
        authority_routes: dict[str, dict[str, Any]] | None = None,
        transport_integrity: str = 'signed',
    ) -> None:
        self.service = service
        self.gateway_id = gateway_id
        self.route_label = route_label
        self.authority_routes = authority_routes or {}
        self.transport_metadata = FeedTransportMetadata(
            mode='gateway',
            integrity=transport_integrity,
            available=service is not None or bool(authority_routes),
            channel='mediated',
        )

    def _resolve_route(self, authority_id: str) -> tuple[MockTRQPService, str]:
        route = self.authority_routes.get(authority_id)
        if route is not None:
            return route['service'], route.get('route_label', authority_id)
        if self.service is None:
            raise ValueError(f'No policy route configured for authority {authority_id}')
        return self.service, self.route_label

    def _mediation(self, service: MockTRQPService, route_label: str, authority_id: str, decision_type: str) -> dict[str, Any]:
        feed = service.feed_descriptor_evidence().get('policy', {})
        return {
            'gateway_id': self.gateway_id,
            'route_label': route_label,
            'mode': 'remote_policy_mediation',
            'target_authority_id': authority_id,
            'decision_type': decision_type,
            'route_attested': bool(feed.get('route_attested', False)),
            'feed_descriptor': feed,
        }

    def authorization(self, entity_id: str, authority_id: str, action: str, resource: str, context: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        service, route_label = self._resolve_route(authority_id)
        response = asdict(service.authorization(entity_id, authority_id, action, resource, context))
        return response, self._mediation(service, route_label, authority_id, 'authorization')

    def recognition(self, authority_id: str, recognized_authority_id: str, context: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        service, route_label = self._resolve_route(authority_id)
        response = asdict(service.recognition(authority_id, recognized_authority_id, context))
        return response, self._mediation(service, route_label, authority_id, 'recognition')
