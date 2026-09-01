"""Execution-context isolation for transient verifier evidence.

Verifier instances intentionally retain reusable service/cache adapters, but decision
receipts must never retain transient evidence from another request.  The descriptor
below stores the existing ``last_*`` evidence attributes in ContextVars, preserving
the verifier's internal API while isolating concurrent threads/tasks.
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import Any


class ContextEvidence:
    """Data descriptor providing per-execution-context evidence for each verifier."""

    def __init__(self, name: str) -> None:
        self._state: ContextVar[dict[int, dict[str, Any]]] = ContextVar(
            f"cawg_trqp_{name}", default={}
        )

    def __get__(self, instance: object, owner: type | None = None) -> dict[str, Any] | "ContextEvidence":
        if instance is None:
            return self
        return self._state.get().get(id(instance), {})

    def __set__(self, instance: object, value: dict[str, Any]) -> None:
        state = dict(self._state.get())
        state[id(instance)] = value
        self._state.set(state)


def install_decision_evidence_isolation(verifier_cls: type) -> None:
    """Install context-local evidence descriptors and reset them for every decision."""
    evidence_names = (
        "last_transport_metadata",
        "last_revocation_status",
        "last_feed_descriptor_evidence",
        "last_cache_evidence",
    )
    if getattr(verifier_cls, "_decision_evidence_isolated", False):
        return

    for name in evidence_names:
        setattr(verifier_cls, name, ContextEvidence(name))

    original_verify = verifier_cls.verify

    def isolated_verify(self: Any, *args: Any, **kwargs: Any) -> Any:
        # Reset before *every* decision. Context-local descriptors make this safe
        # for concurrent requests sharing the same long-lived Verifier instance.
        for name in evidence_names:
            setattr(self, name, {})
        return original_verify(self, *args, **kwargs)

    isolated_verify.__name__ = original_verify.__name__
    isolated_verify.__doc__ = original_verify.__doc__
    verifier_cls.verify = isolated_verify
    verifier_cls._decision_evidence_isolated = True
