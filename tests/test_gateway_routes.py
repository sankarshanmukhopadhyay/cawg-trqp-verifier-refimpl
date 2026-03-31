import json
from pathlib import Path

from cawg_trqp_refimpl.gateway import TrustGateway
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.verifier import Verifier


def test_gateway_routes_multi_authority_requests_deterministically():
    routes = {
        "did:web:media-registry.example": {
            "service": MockTRQPService(Path("data/policies_multi_authority.json")),
            "route_label": "route:media-india",
        },
        "did:web:coalition-registry.example": {
            "service": MockTRQPService(Path("data/policies_multi_authority.json")),
            "route_label": "route:coalition-eu",
        },
    }
    gateway = TrustGateway(gateway_id="gateway:mesh", authority_routes=routes)
    verifier = Verifier(gateway=gateway)

    vector = json.loads(Path("examples/interoperability_vector_multi_authority.json").read_text())["vectors"][1]
    vector.pop("name", None)
    request = VerificationRequest(**vector)
    result = verifier.verify(request, profile="standard")

    assert result.trust_outcome == "trusted"
    assert result.gateway_mediation["route_label"] == "route:coalition-eu"
    assert result.gateway_mediation["target_authority_id"] == "did:web:coalition-registry.example"
