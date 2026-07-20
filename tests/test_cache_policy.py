import json
from pathlib import Path
from jsonschema import Draft202012Validator


def test_cache_policy_schema_accepts_governed_policy():
    schema = json.loads(Path("schemas/cache-policy.schema.json").read_text())
    policy = {
        "mode": "cache_first",
        "maximum_ttl_seconds": 3600,
        "negative_ttl_seconds": 60,
        "stale_while_revalidate_seconds": 30,
        "require_policy_epoch": True,
        "invalidate_on_revocation_delta": True,
        "live_on_risk_tiers": ["high", "critical"],
        "failure_behavior": "indeterminate"
    }
    Draft202012Validator(schema).validate(policy)
