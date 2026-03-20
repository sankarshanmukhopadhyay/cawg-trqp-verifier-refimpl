from __future__ import annotations
import json
from pathlib import Path


class SnapshotStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def find_authorization(self, entity_id: str, authority_id: str, action: str, resource: str, context: dict) -> dict | None:
        for item in self.data.get("authorization", []):
            if (
                item.get("entity_id") == entity_id
                and item.get("authority_id") == authority_id
                and item.get("action") == action
                and item.get("resource") == resource
                and all(context.get(k) == v for k, v in item.get("context", {}).items())
            ):
                return item
        return None

    def find_recognition(self, authority_id: str, recognized_authority_id: str, context: dict) -> dict | None:
        for item in self.data.get("recognition", []):
            if (
                item.get("authority_id") == authority_id
                and item.get("recognized_authority_id") == recognized_authority_id
                and all(context.get(k) == v for k, v in item.get("context", {}).items())
            ):
                return item
        return None
