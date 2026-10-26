"""Non-cryptographic ordering checks for experimental CAWG assertion dependencies.

Proves only acyclic, sequential reference structure, not covered-hash integrity,
C2PA compliance, or cryptographic signature validity.
"""
from collections import deque

class AssertionOrderError(ValueError):
    pass

KIND_ORDER = ("delegation", "delegator_assertion", "delegate_assertion", "manifest_seal")

def validate_order(nodes):
    if not isinstance(nodes, list) or len(nodes) != 4:
        raise AssertionOrderError("four_stages_required")
    if any(not isinstance(n, dict) or set(n) != {"id", "kind", "depends_on"} for n in nodes):
        raise AssertionOrderError("node_malformed")
    by_id = {n["id"]: n for n in nodes if isinstance(n["id"], str) and n["id"]}
    if len(by_id) != 4 or set(n["kind"] for n in nodes) != set(KIND_ORDER):
        raise AssertionOrderError("stages_or_ids_invalid")
    by_kind = {n["kind"]: n for n in nodes}
    ids = {kind: by_kind[kind]["id"] for kind in KIND_ORDER}
    expected = {
        "delegation": set(),
        "delegator_assertion": {ids["delegation"]},
        "delegate_assertion": {ids["delegation"], ids["delegator_assertion"]},
        "manifest_seal": {ids["delegator_assertion"], ids["delegate_assertion"]},
    }
    for n in nodes:
        deps = n["depends_on"]
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps):
            raise AssertionOrderError("dependencies_malformed")
        if set(deps) != expected[n["kind"]] or len(set(deps)) != len(deps):
            raise AssertionOrderError("invalid_dependency_order")
    return {"structure": "valid", "signature_status": "not_verified", "covered_hash_status": "not_verified"}
