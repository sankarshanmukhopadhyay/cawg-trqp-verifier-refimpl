from concurrent.futures import ThreadPoolExecutor

from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.verifier import Verifier


def _request(asset_id: str) -> VerificationRequest:
    return VerificationRequest(
        asset_id=asset_id,
        integrity_ok=True,
        entity_id="entity:test",
        authority_id="authority:test",
        issuer_id=None,
        action="read",
        resource="resource:test",
        context={},
    )


def test_sequential_decision_resets_transient_evidence():
    verifier = Verifier()
    verifier.last_feed_descriptor_evidence = {"policy": {"reason_code": "stale-from-a"}}
    verifier.last_cache_evidence = {"authorization": {"cache_hit": True}}

    result = verifier.verify(_request("asset:b"))

    assert result.policy_evidence["feed_descriptors"] == {}
    assert verifier.last_cache_evidence == {}
    assert "stale-from-a" not in str(result.to_dict())


def test_shared_verifier_has_context_local_evidence():
    verifier = Verifier()

    def worker(marker: str) -> str:
        verifier.last_feed_descriptor_evidence = {"marker": {"value": marker}}
        return verifier.last_feed_descriptor_evidence["marker"]["value"]

    with ThreadPoolExecutor(max_workers=4) as pool:
        observed = list(pool.map(worker, ["a", "b", "c", "d"]))

    assert observed == ["a", "b", "c", "d"]
    # Worker evidence is not imported into the caller's execution context.
    assert verifier.last_feed_descriptor_evidence == {}
