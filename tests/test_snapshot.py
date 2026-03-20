from pathlib import Path
from cawg_trqp_refimpl.snapshot import SnapshotStore


def test_snapshot_lookup():
    store = SnapshotStore(Path("data/snapshot.json"))
    item = store.find_authorization(
        "did:web:publisher.example",
        "did:web:media-registry.example",
        "publish",
        "cawg:news-content",
        {"jurisdiction": "IN"},
    )
    assert item is not None
    assert item["authorized"] is True
