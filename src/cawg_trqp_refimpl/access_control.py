from __future__ import annotations


def require_scope(granted_scopes: set[str], required_scope: str) -> None:
    if required_scope not in granted_scopes:
        raise PermissionError(f"missing required scope: {required_scope}")
