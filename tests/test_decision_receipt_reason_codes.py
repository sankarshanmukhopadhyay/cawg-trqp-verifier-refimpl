from cawg_trqp_refimpl.feed_descriptor import FRESHNESS_REASON_CODES


def test_freshness_reason_codes_are_governance_stable():
    assert {"fresh", "stale_but_warned", "stale_rejected", "missing_feed_descriptor", "descriptor_signature_invalid", "descriptor_digest_mismatch", "authority_not_recognized", "route_unattested", "revocation_channel_degraded"}.issubset(FRESHNESS_REASON_CODES)
