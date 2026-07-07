"""Data storage layer for calculator history."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List


class HistoryManager:
    """Manages persistent calculation history in a JSON file."""

    def __init__(self, file_path: str = "history.json") -> None:
        self.file_path = Path(file_path)
        self._ensure_history_file()

    def _ensure_history_file(self) -> None:
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")
            return

        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8") or "[]")
            if not isinstance(data, list):
                self.file_path.write_text("[]", encoding="utf-8")
        except (json.JSONDecodeError, OSError):
            self.file_path.write_text("[]", encoding="utf-8")

    def load_history(self) -> List[str]:
        try:
            raw = self.file_path.read_text(encoding="utf-8")
            data = json.loads(raw or "[]")
            if not isinstance(data, list):
                return []

            entries: List[str] = []
            for item in data:
                if isinstance(item, dict):
                    expression = str(item.get("expression", "")).strip()
                    result = str(item.get("result", "")).strip()
                    if expression and result:
                        entries.append(f"{expression} = {result}")
                elif isinstance(item, str):
                    entries.append(item)
            return entries
        except (json.JSONDecodeError, OSError):
            return []

    def add_record(self, expression: str, result: str) -> None:
        payload = {
            "expression": expression,
            "result": result,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

        data = self._read_raw_history()
        data.append(payload)
        self._write_raw_history(data)

    def clear_history(self) -> None:
        self._write_raw_history([])

    def _read_raw_history(self) -> list[dict]:
        try:
            raw = self.file_path.read_text(encoding="utf-8")
            data = json.loads(raw or "[]")
            if isinstance(data, list):
                sanitized: list[dict] = []
                for item in data:
                    if isinstance(item, dict):
                        sanitized.append(item)
                return sanitized
            return []
        except (json.JSONDecodeError, OSError):
            return []

    def _write_raw_history(self, data: list[dict]) -> None:
        self.file_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
