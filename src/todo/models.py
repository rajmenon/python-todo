
import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from uuid import uuid4


class Status(Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    BLOCKED = "blocked"


class TodoItem:
    _status: Status

    def __init__(self, title: str, status: Status = Status.INCOMPLETE) -> None:
        self.title = title
        self._status = status
        self.id = str(uuid4())
        self.created_at = datetime.now()
        # record the updated time correctly
        self.updated_at = datetime.now()

    def mark_complete(self) -> bool:
        if self._status == Status.COMPLETE:
            return False
        self._status = Status.COMPLETE
        self.updated_at = datetime.now()
        return True

    def __repr__(self) -> str:
        return f"TodoItem(title={self.title}, status={self._status})"

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "title": self.title,
            "status": self._status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "TodoItem":
        # title
        title = data.get("title", "") or ""

        # status (be forgiving for missing or invalid values)
        status_raw = data.get("status")
        try:
            status = Status(status_raw) if status_raw else Status.INCOMPLETE
        except Exception:
            status = Status.INCOMPLETE

        item = cls(title=title, status=status)
        item.id = data.get("id", item.id)

        # parse created_at safely
        created_raw = data.get("created_at")
        if created_raw:
            try:
                item.created_at = datetime.fromisoformat(created_raw)
            except Exception:
                item.created_at = datetime.now()
        else:
            item.created_at = datetime.now()

        # parse updated_at safely; fall back to created_at
        updated_raw = data.get("updated_at")
        if updated_raw:
            try:
                item.updated_at = datetime.fromisoformat(updated_raw)
            except Exception:
                item.updated_at = item.created_at
        else:
            item.updated_at = item.created_at

        return item

    @property
    def datemodified(self) -> str:
        """Return a simple string for last-modified time for display."""
        return self.updated_at.isoformat()

    @property
    def done(self) -> bool:
        return self._status == Status.COMPLETE


class TodoList:
    items: dict[str, TodoItem]

    def __init__(self, path: Path | None = None) -> None:
        # default storage path: project root/todos.json
        if path is None:
            project_root = Path(__file__).resolve().parents[2]
            path = project_root / "todos.json"
        self.path: Path = path
        self.items = {}
        self._load()

    def add_item(self, item: TodoItem) -> None:
        self.items[item.id] = item
        self._save()

    def remove_item(self, item: TodoItem) -> None:
        self.items.pop(item.id, None)
        self._save()

    def delete(self, item_id: str) -> None:
        """Delete an item by id or raise KeyError if not found."""
        if item_id in self.items:
            self.items.pop(item_id)
            self._save()
        else:
            raise KeyError(item_id)

    def mark_complete(self, item_id: str) -> bool:
        """Mark an item complete by id. Returns True if changed, False if already complete.

        Raises KeyError if not found.
        """
        item = self.items.get(item_id)
        if item is None:
            raise KeyError(item_id)
        changed = item.mark_complete()
        if changed:
            self._save()
        return changed

    def get_items(self) -> list[TodoItem]:
        return list(self.items.values())

    def _save(self) -> None:
        data = [i.to_dict() for i in self.get_items()]
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(data, indent=2), encoding="utf8")
        except Exception:
            # best-effort: ignore write errors for now
            pass

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            raw = self.path.read_text(encoding="utf8")
            data = json.loads(raw)
            for item_data in data:
                try:
                    item = TodoItem.from_dict(item_data)
                    self.items[item.id] = item
                except Exception:
                    continue
        except Exception:
            # ignore malformed file
            return