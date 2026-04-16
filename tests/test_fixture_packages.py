import json
from pathlib import Path

import pytest

from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.gateway import TrustGateway
from cawg_trqp_refimpl.verifier import Verifier


FIXTURE_ROOT = Path('fixtures/profile-bound')


@pytest.mark.parametrize(
    'fixture_name, verifier_factory, profile',
    [
        ('standard-v1', lambda: Verifier(service=MockTRQPService(Path('data/policies.json'), Path('data/revocations.json'))), 'standard'),
        ('high-assurance-v1', lambda: Verifier(service=MockTRQPService(Path('data/policies.json'), Path('data/revocations.json'))), 'high_assurance'),
        (
            'gateway-standard-v1',
            lambda: Verifier(
                service=MockTRQPService(Path('data/policies.json'), Path('data/revocations.json')),
                gateway=TrustGateway(
                    MockTRQPService(Path('data/policies.json'), Path('data/revocations.json')),
                    gateway_id='gateway:interop',
                    route_label='route:gateway-standard',
                ),
            ),
            'standard',
        ),
        (
            'multi-authority-v1',
            lambda: Verifier(
                gateway=TrustGateway(
                    gateway_id='gateway:mesh',
                    authority_routes={
                        'did:web:media-registry.example': {
                            'service': MockTRQPService(Path('data/policies_multi_authority.json'), Path('data/revocations.json')),
                            'route_label': 'route:media-india',
                        },
                        'did:web:coalition-registry.example': {
                            'service': MockTRQPService(Path('data/policies_multi_authority.json'), Path('data/revocations.json')),
                            'route_label': 'route:coalition-eu',
                        },
                    },
                )
            ),
            'standard',
        ),
    ],
)
def test_fixture_package_replays_to_expected_outcome(fixture_name, verifier_factory, profile):
    base = FIXTURE_ROOT / fixture_name
    request = VerificationRequest(**json.loads((base / 'request.json').read_text(encoding='utf-8')))
    expected = json.loads((base / 'expected_result.json').read_text(encoding='utf-8'))
    result = verifier_factory().verify(request, profile=profile).to_dict()

    assert result['trust_outcome'] == expected['trust_outcome']
    assert result['verification_mode'] == expected['verification_mode']
    assert result['policy_evidence']['verification_profile']['id'] == expected['policy_evidence']['verification_profile']['id']


def test_compatibility_matrix_references_existing_artifacts():
    matrix = json.loads(Path('conformance/compatibility-matrix.json').read_text(encoding='utf-8'))
    for control in matrix['controls'].values():
        for evidence in control.get('evidence', []):
            assert Path(evidence).exists(), evidence
