import copy
import pytest
from cawg_trqp_refimpl.experimental_assertion_order import validate_order, AssertionOrderError

def graph():
    return [
        {"id":"delegation","kind":"delegation","depends_on":[]},
        {"id":"delegator","kind":"delegator_assertion","depends_on":["delegation"]},
        {"id":"delegate","kind":"delegate_assertion","depends_on":["delegation","delegator"]},
        {"id":"seal","kind":"manifest_seal","depends_on":["delegator","delegate"]},
    ]
def test_valid_structure_does_not_claim_crypto():
    r=validate_order(graph())
    assert r["structure"]=="valid"
    assert r["signature_status"]=="not_verified"
    assert r["covered_hash_status"]=="not_verified"
@pytest.mark.parametrize("mutation",[
    lambda n: n[0]["depends_on"].append("seal"),
    lambda n: n[1]["depends_on"].clear(),
    lambda n: n[2]["depends_on"].append("seal"),
    lambda n: n[3]["depends_on"].clear(),
    lambda n: n[3].update(id="delegate"),
])
def test_rejects_cycles_missing_coverage_late_dependencies(mutation):
    n=graph()
    mutation(n)
    with pytest.raises(AssertionOrderError):
        validate_order(n)
