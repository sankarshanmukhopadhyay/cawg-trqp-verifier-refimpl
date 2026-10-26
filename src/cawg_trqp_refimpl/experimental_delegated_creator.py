"""Experimental delegated-creator authority evaluation, independent of CAWG normative profiles.

Inputs are validated before evaluation. No actual C2PA parser, signature verifier,
credential issuer, external rights resolver, or trust-registry integration is implied.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from typing import Any

PROFILE_ID = "experimental-delegated-creator/0.1"
COVERAGES = {"unverified", "delegator-covered", "credential-backed"}
ACTIONS = {"create", "transform", "publish"}
MAX_DEPTH = 3
MAX_DURATION_SECONDS = 86400 * 30

class InvalidCase(ValueError):
    pass

def _timestamp(value: str) -> datetime:
    if not isinstance(value, str):
        raise InvalidCase("timestamp_malformed")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidCase("timestamp_malformed") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise InvalidCase("timestamp_without_timezone")
    return parsed.astimezone(timezone.utc)

def _set(value: Any, name: str) -> set[str]:
    if not isinstance(value, list) or not value or any(not isinstance(v, str) or not v.strip() for v in value):
        raise InvalidCase(name + "_malformed")
    if len(value) != len(set(value)):
        raise InvalidCase(name + "_duplicate")
    return set(value)

def _digest(uri: str, document: Any) -> str:
    return hashlib.sha256(json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def evaluate(case: dict[str, Any]) -> dict[str, Any]:
    """Return explicit authorization and coverage; never equate provenance with permission."""
    if not isinstance(case, dict):
        raise InvalidCase("case_malformed")
    for field in ("id", "root_principal", "actor", "action", "resource", "purpose",
                  "signed_at", "evaluated_at", "links", "chain", "generator"):
        if field not in case:
            raise InvalidCase("missing_" + field)
    for field in ("id", "root_principal", "actor", "resource", "purpose"):
        if not isinstance(case[field], str) or not case[field].strip():
            raise InvalidCase(field + "_malformed")
    if case["action"] not in ACTIONS:
        raise InvalidCase("action_unsupported")
    signed = _timestamp(case["signed_at"])
    now = _timestamp(case["evaluated_at"])
    chain = case["chain"]
    if not isinstance(chain, list) or len(chain) > 32:
        raise InvalidCase("chain_malformed")
    links = case["links"]
    if not isinstance(links, list):
        raise InvalidCase("links_malformed")
    for link in links:
        if not isinstance(link, dict) or set(link) != {"uri", "sha256", "content"}:
            raise InvalidCase("link_malformed")
        uri = link["uri"]
        if not isinstance(uri, str) or not uri.startswith("https://"):
            raise InvalidCase("link_uri_invalid")
        if not isinstance(link["sha256"], str) or len(link["sha256"]) != 64:
            raise InvalidCase("link_digest_malformed")
    generator = case["generator"]
    if not isinstance(generator, dict) or set(generator) != {"id", "reject_on_unverified"}:
        raise InvalidCase("generator_malformed")
    if not isinstance(generator["id"], str) or not generator["id"].strip() or not isinstance(generator["reject_on_unverified"], bool):
        raise InvalidCase("generator_malformed")
    result = {"case_id": case["id"], "profile": PROFILE_ID, "coverage": "unverified",
              "evidence_provenance": {"credential": "caller_supplied_simulation", "delegator_signature": "not_verified", "signing_time": "caller_supplied_untrusted", "linked_content": "local_digest_only"},
              "historical_authority": "indeterminate", "current_authority": "indeterminate",
              "authority": "indeterminate", "generator": "rejected", "reason": "no_delegation",
              "evaluated_at": case["evaluated_at"], "evidence_sha256": None}
    def finish(reason: str, authority: str = "denied") -> dict[str, Any]:
        result["reason"], result["authority"] = reason, authority
        result["historical_authority"] = authority
        result["current_authority"] = authority
        result["generator"] = "accepted" if authority == "authorized" or (authority == "indeterminate" and not generator["reject_on_unverified"]) else "rejected"
        return result

    # Invalid/absent external evidence cannot be transformed into an allow.
    for link in links:
        if _digest(link["uri"], link["content"]) != link["sha256"]:
            return finish("linked_evidence_integrity", "indeterminate")
    if not chain:
        return finish("no_delegation", "indeterminate")
    if len(chain) > MAX_DEPTH:
        return finish("chain_depth_exceeded")
    previous = case["root_principal"]
    prev_actions = prev_resources = prev_purposes = None
    prev_start = prev_end = None
    visited = {previous}
    credential_backed = True
    normalized = []
    for i, edge in enumerate(chain):
        required = {"delegator", "delegate", "actions", "resources", "purposes", "not_before", "not_after",
                    "redelegation", "revoked_at", "evidence_uri", "credential_verified"}
        if not isinstance(edge, dict) or set(edge) != required:
            raise InvalidCase("chain_edge_malformed")
        if not isinstance(edge["delegator"], str) or not isinstance(edge["delegate"], str) or not edge["delegate"]:
            raise InvalidCase("chain_parties_malformed")
        actions = _set(edge["actions"], "actions")
        resources = _set(edge["resources"], "resources")
        purposes = _set(edge["purposes"], "purposes")
        start, end = _timestamp(edge["not_before"]), _timestamp(edge["not_after"])
        if start >= end:
            raise InvalidCase("interval_invalid")
        if not isinstance(edge["redelegation"], bool) or not isinstance(edge["credential_verified"], bool):
            raise InvalidCase("edge_flags_malformed")
        if edge["revoked_at"] is not None:
            _timestamp(edge["revoked_at"])
        if edge["evidence_uri"] is not None and not isinstance(edge["evidence_uri"], str):
            raise InvalidCase("evidence_uri_malformed")
        if edge["delegator"] != previous:
            return finish("chain_disconnected")
        if edge["delegate"] in visited:
            return finish("chain_cycle")
        if i and not chain[i - 1]["redelegation"]:
            return finish("redelegation_forbidden")
        if i and (not actions <= prev_actions or not resources <= prev_resources or not purposes <= prev_purposes or start < prev_start or end > prev_end):
            return finish("scope_or_duration_escalation")
        if (end - start).total_seconds() > MAX_DURATION_SECONDS:
            return finish("delegation_duration_exceeded")
        if not (start <= signed < end):
            return finish("not_valid_at_signing")
        revoked = _timestamp(edge["revoked_at"]) if edge["revoked_at"] else None
        if revoked is not None and revoked <= signed:
            return finish("revoked_at_signing")
        # Historical authorization is not rewritten by subsequent expiry/revocation.
        # Current authorization is a separate, explicitly provisional decision.
        if not (start <= now < end) or (revoked is not None and revoked <= now):
            result["current_authority"] = "denied"
        if not edge["evidence_uri"] or not any(link["uri"] == edge["evidence_uri"] for link in links):
            return finish("delegation_evidence_unavailable", "indeterminate")
        credential_backed = credential_backed and edge["credential_verified"]
        normalized.append({"delegator": edge["delegator"], "delegate": edge["delegate"]})
        visited.add(edge["delegate"])
        previous, prev_actions, prev_resources, prev_purposes, prev_start, prev_end = edge["delegate"], actions, resources, purposes, start, end
    result["coverage"] = "credential-backed" if credential_backed else "delegator-covered"
    result["evidence_sha256"] = hashlib.sha256(json.dumps(normalized, sort_keys=True).encode()).hexdigest()
    if previous != case["actor"]:
        return finish("actor_not_delegate")
    if case["action"] not in prev_actions or case["resource"] not in prev_resources or case["purpose"] not in prev_purposes:
        return finish("requested_action_out_of_scope")
    decision = finish("authorized", "authorized")
    decision["current_authority"] = result["current_authority"] if result["current_authority"] == "denied" else "authorized"
    return decision
