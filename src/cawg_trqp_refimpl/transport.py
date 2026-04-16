from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class TransportConstraintError(Exception):
    """Raised when runtime feed transport does not satisfy profile requirements."""


@dataclass(frozen=True)
class FeedTransportMetadata:
    mode: str
    integrity: str
    available: bool = True
    channel: str = "full"

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "integrity": self.integrity,
            "available": self.available,
            "channel": self.channel,
        }


def evaluate_transport_constraints(required: dict[str, Any], actual: FeedTransportMetadata) -> list[str]:
    failures: list[str] = []
    required_mode = required.get("mode")
    compatible_modes = {
        'local': {'local'},
        'http': {'http', 'gateway'},
        'gateway': {'gateway'},
    }
    if required_mode and actual.mode not in compatible_modes.get(required_mode, {required_mode}):
        failures.append(f"transport mode {actual.mode!r} does not satisfy required mode {required_mode!r}")

    integrity_rank = {"none": 0, "tls": 1, "signed": 2}
    required_integrity = required.get("integrity", "none")
    actual_rank = integrity_rank.get(actual.integrity, -1)
    required_rank = integrity_rank.get(required_integrity, 0)
    if actual_rank < required_rank:
        failures.append(
            f"transport integrity {actual.integrity!r} is below required level {required_integrity!r}"
        )

    availability_requirement = required.get("availability_requirement", "best_effort")
    if availability_requirement == "required" and not actual.available:
        failures.append("required transport feed is unavailable")

    return failures
