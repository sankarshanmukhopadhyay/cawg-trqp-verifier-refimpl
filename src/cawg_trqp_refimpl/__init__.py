"""CAWG-TRQP verifier reference implementation package."""

__version__ = "0.19.2"

# Install execution-context evidence descriptors before consumers construct a
# Verifier. This preserves the public Verifier API while ensuring long-lived
# verifier instances cannot leak transient evidence across decisions.
from .verifier import Verifier  # noqa: E402
from .decision_scope import install_decision_evidence_isolation  # noqa: E402

install_decision_evidence_isolation(Verifier)
