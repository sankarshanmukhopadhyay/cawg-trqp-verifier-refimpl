from datetime import datetime, timezone
from pathlib import Path
import json

from cawg_trqp_refimpl.snapshot import SnapshotStore


def test_snapshot_lookup():
    store = SnapshotStore(Path("data/snapshot.json"), Path("data/trust_anchors.json"))
    item = store.find_authorization(
        "did:web:publisher.example",
        "did:web:media-registry.example",
        "publish",
        "cawg:news-content",
        {"jurisdiction": "IN"},
    )
    assert item is not None
    assert item["authorized"] is True
    assert store.signature_verified is True


def test_snapshot_tamper_detected(tmp_path):
    snapshot = json.loads(Path("data/snapshot.json").read_text(encoding="utf-8"))
    snapshot["authorization"][0]["authorized"] = False
    tampered = tmp_path / "snapshot.json"
    tampered.write_text(json.dumps(snapshot), encoding="utf-8")

    store = SnapshotStore(tampered, Path("data/trust_anchors.json"))
    assert store.is_usable() is False
    assert "invalid_snapshot_signature" in store.validation_errors


def test_snapshot_expiry_enforced():
    store = SnapshotStore(
        Path("data/snapshot.json"),
        Path("data/trust_anchors.json"),
        current_time=datetime(2027, 1, 1, tzinfo=timezone.utc),
    )
    assert store.is_usable() is False
    assert "expired_snapshot" in store.validation_errors
