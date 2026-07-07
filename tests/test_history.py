import json
from pathlib import Path

from history import HistoryManager


def test_history_file_auto_created(tmp_path: Path) -> None:
    history_path = tmp_path / "history.json"
    HistoryManager(str(history_path))
    assert history_path.exists()
    assert json.loads(history_path.read_text(encoding="utf-8")) == []


def test_add_and_load_history(tmp_path: Path) -> None:
    history_path = tmp_path / "history.json"
    manager = HistoryManager(str(history_path))
    manager.add_record("10+5", "15")
    manager.add_record("20/4", "5")

    loaded = manager.load_history()
    assert loaded == ["10+5 = 15", "20/4 = 5"]


def test_clear_history(tmp_path: Path) -> None:
    history_path = tmp_path / "history.json"
    manager = HistoryManager(str(history_path))
    manager.add_record("3*3", "9")
    manager.clear_history()

    assert manager.load_history() == []
    assert json.loads(history_path.read_text(encoding="utf-8")) == []
