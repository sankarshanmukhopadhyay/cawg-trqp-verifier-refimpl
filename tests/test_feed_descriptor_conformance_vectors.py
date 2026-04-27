import copy
import json
from pathlib import Path

from cawg_trqp_refimpl.feed_descriptor import validate_feed_descriptor

TRUST = json.loads(Path("data/trust_anchors.json").read_text())
BODY = Path("data/policies.json").read_text()


def _policy_descriptor():
    return json.loads(Path("examples/feed_descriptors/policy-feed.signed.json").read_text())


def test_unknown_authority_is_negative_conformance_vector():
    descriptor = copy.deepcopy(_policy_descriptor())
    report = validate_feed_descriptor(descriptor, BODY, trust_anchors=TRUST, expected_authorities={"did:web:another-registry.example"})
    assert report.reason_code == "authority_not_recognized"


def test_unattested_gateway_route_is_negative_conformance_vector():
    descriptor = copy.deepcopy(_policy_descriptor())
    descriptor["route"]["attested"] = False
    report = validate_feed_descriptor(descriptor, BODY, trust_anchors=TRUST, expected_authorities={"did:web:media-registry.example"}, route_required=True)
    assert report.reason_code in {"descriptor_signature_invalid", "route_unattested"}
