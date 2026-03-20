from pathlib import Path
import json
from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.snapshot import SnapshotStore
from cawg_trqp_refimpl.verifier import Verifier


def run():
    authority_id = "did:web:media-registry.example"
    standard_request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), authority_id)
    blocked_request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_blocked.json"), authority_id)

    standard = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    edge = Verifier(snapshot=SnapshotStore(Path("data/snapshot.json")))

    print("=== Standard Profile: Allowed Entity ===")
    print(json.dumps(standard.verify(standard_request, profile="standard").to_dict(), indent=2))

    print("\n=== Edge Profile: Allowed Entity ===")
    print(json.dumps(edge.verify(standard_request, profile="edge").to_dict(), indent=2))

    print("\n=== Standard Profile: Blocked Entity ===")
    print(json.dumps(standard.verify(blocked_request, profile="standard").to_dict(), indent=2))


if __name__ == "__main__":
    run()
