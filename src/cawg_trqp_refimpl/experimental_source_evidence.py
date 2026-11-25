"""Opt-in, offline authentication of experimental source claims.

Reuse the repository's signed feed descriptor contract. The body below is a
local experiment, not a CAWG/TRQP receipt or recognized industry profile.
Source policy and observation clock must be supplied by the relying party,
separately from evidence packages. No network access or legal determination.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime

from .feed_descriptor import validate_feed_descriptor

PROFILE = "experimental-taskforce-source-claim/0.1"
MAX_BYTES = 65536
STATES = {
    "subject-key-binding": {"active", "revoked", "suspended", "unknown"},
    "authority-to-delegate": {"active", "denied", "revoked", "unknown"},
    "delegation-status": {"active", "revoked", "suspended", "unknown"},
    "consent-record": {"attested", "disputed", "unknown"},
}
CLAIM_FIELDS = {
    "subject-key-binding": {"subject_ref", "key_sha256"},
    "authority-to-delegate": {"statement_sha256", "delegator_key_sha256",
                              "delegate_key_sha256"},
    "delegation-status": {"statement_sha256", "delegator_key_sha256",
                           "delegate_key_sha256"},
    "consent-record": {"subject_ref", "record_sha256"},
}


@dataclass(frozen=True)
class PinnedEvidenceSource:
    """Local relying-party configuration, never inferred from a receipt."""

    kind: str
    authority_id: str
    key_id: str
    public_key_pem: str
    max_age_seconds: int


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate_json_key")
        result[key] = value
    return result


def _invalid_constant(_):
    raise ValueError("nonfinite_json_value")


def _decode(raw):
    if not isinstance(raw, bytes) or not 0 < len(raw) <= MAX_BYTES:
        raise ValueError("evidence_size_invalid")
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                      parse_constant=_invalid_constant)
    if not isinstance(data, dict):
        raise ValueError("evidence_object_required")
    return data


def _timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp_invalid")
    time = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if time.utcoffset() is None:
        raise ValueError("timestamp_unzoned")
    return time


def outcome(status, reason, state="not_checked"):
    return {"status": status, "reason": reason, "state": state}


def assess_signed_claim(package, source, *, kind, expected_claim, observed_at):
    """Authenticate one exact claim against a separately pinned source.

    A result of authenticated_source_claim means the configured key signed a
    fresh descriptor covering the matching body bytes. Its state is the
    source's statement, not independent governance or historical proof.
    """
    if package is None:
        return outcome("missing", "source_package_missing")
    if not isinstance(source, PinnedEvidenceSource) or source.kind != kind:
        return outcome("unrecognized", "source_policy_missing_or_wrong_kind")
    if (kind not in STATES or not all(
            isinstance(v, str) and v.strip()
            for v in (source.authority_id, source.key_id, source.public_key_pem))
            or type(source.max_age_seconds) is not int or source.max_age_seconds <= 0):
        return outcome("invalid", "source_policy_invalid")
    if not isinstance(observed_at, datetime) or observed_at.utcoffset() is None:
        return outcome("indeterminate", "source_clock_unavailable")
    try:
        if not isinstance(package, (tuple, list)) or len(package) != 2:
            return outcome("invalid", "source_package_malformed")
        descriptor_bytes, body_bytes = package
        descriptor, body = _decode(descriptor_bytes), _decode(body_bytes)
        if (set(body) != {"profile", "kind", "claim", "state"}
                or body["profile"] != PROFILE or body["kind"] != kind
                or not isinstance(body["state"], str) or body["state"] not in STATES[kind]
                or not isinstance(body["claim"], dict)
                or set(body["claim"]) != CLAIM_FIELDS[kind]
                or not all(isinstance(v, str) and v.strip()
                           for v in body["claim"].values())):
            return outcome("invalid", "claim_shape_invalid")
        if set(descriptor) != {"descriptor_type", "descriptor_version", "descriptor_id",
                               "issued_at", "valid_until", "authority", "feed",
                               "freshness", "route", "descriptor_signature"}:
            return outcome("invalid", "descriptor_shape_invalid")
        if (descriptor["descriptor_type"] != "cawg-trqp-feed-descriptor"
                or descriptor["descriptor_version"] != "1.0.0"
                or not isinstance(descriptor["descriptor_id"], str)
                or not descriptor["descriptor_id"]):
            return outcome("invalid", "descriptor_profile_invalid")
        authority, feed = descriptor["authority"], descriptor["feed"]
        freshness, sig, route = (descriptor["freshness"], descriptor["descriptor_signature"],
                                 descriptor["route"])
        if not all(isinstance(x, dict) for x in (authority, feed, freshness, sig, route)):
            return outcome("invalid", "descriptor_shape_invalid")
        if (authority.get("authority_id") != source.authority_id
                or authority.get("key_id") != source.key_id
                or sig.get("key_id") != source.key_id):
            return outcome("unrecognized", "source_binding_mismatch")
        scope = authority.get("scope")
        if (not isinstance(scope, list) or not all(isinstance(x, str) for x in scope)
                or "experimental-taskforce:" + kind not in scope):
            return outcome("unrecognized", "source_scope_mismatch")
        expected_feed = "revocation_feed" if kind == "delegation-status" else "policy_feed"
        if (feed.get("feed_type") != expected_feed
                or feed.get("digest_alg") != "sha-256"
                or not isinstance(feed.get("source"), str) or not feed["source"]):
            return outcome("invalid", "feed_contract_invalid")
        max_age = freshness.get("max_age_seconds")
        if type(max_age) is not int or max_age <= 0 or freshness.get("enforcement") != "fail":
            return outcome("invalid", "freshness_contract_invalid")
        issued, expiry = _timestamp(descriptor["issued_at"]), _timestamp(descriptor["valid_until"])
        if issued >= expiry:
            return outcome("invalid", "source_interval_invalid")
        report = validate_feed_descriptor(
            descriptor, body_bytes,
            trust_anchors={"keys": [{"key_id": source.key_id,
                                    "public_key_pem": source.public_key_pem}]},
            expected_authorities={source.authority_id}, now=observed_at,
        )
        if not report.signature_ok:
            return outcome("invalid", "source_signature_invalid")
        if not report.integrity_ok:
            return outcome("invalid", "source_body_digest_mismatch")
        if not report.authority_ok:
            return outcome("unrecognized", "source_authority_mismatch")
        if (issued > observed_at or observed_at >= expiry
                or (observed_at - issued).total_seconds() > min(max_age, source.max_age_seconds)):
            return outcome("stale", "source_observation_outside_freshness")
        if body["claim"] != expected_claim:
            return outcome("mismatch", "source_claim_does_not_match_operation")
        return outcome("authenticated_source_claim", "pinned_source_claim_matches",
                       body["state"])
    except (ValueError, TypeError, KeyError, OverflowError, RecursionError):
        return outcome("invalid", "source_evidence_malformed")
