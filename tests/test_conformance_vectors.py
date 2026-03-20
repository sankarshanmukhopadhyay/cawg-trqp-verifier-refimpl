import json
from pathlib import Path
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.snapshot import SnapshotStore
from cawg_trqp_refimpl.verifier import Verifier


def test_standard_expected_result_shape():
    data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(VerificationRequest(**data), profile="standard").to_dict()
    expected = json.loads(Path("examples/expected/standard_result.json").read_text(encoding="utf-8"))
    for key, value in expected.items():
        assert result[key] == value


def test_edge_expected_result_shape():
    data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
    verifier = Verifier(snapshot=SnapshotStore(Path("data/snapshot.json")))
    result = verifier.verify(VerificationRequest(**data), profile="edge").to_dict()
    expected = json.loads(Path("examples/expected/edge_result.json").read_text(encoding="utf-8"))
    for key, value in expected.items():
        assert result[key] == value
