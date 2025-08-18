# src/todo/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, UTC
from collections.abc import Iterable
from uuid import UUID, uuid4


@dataclass(slots=True)
class Task:
    id: UUID
    title: str
    done: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def mark_done(self) -> Task:
        return Task(id=self.id, title=self.title, done=True, created_at=self.created_at)


class TaskRepo:
    def add(self, title: str) -> Task:  # pragma: no cover (interface)
        raise NotImplementedError

    def list(self, include_done: bool = True) -> list[Task]:  # pragma: no cover
        raise NotImplementedError

    def complete(self, task_id: UUID) -> Task:  # pragma: no cover
        raise NotImplementedError

    def delete(self, task_id: UUID) -> None:  # pragma: no cover
        raise NotImplementedError

    def bulk_import(self, tasks: Iterable[Task]) -> None:  # pragma: no cover
        raise NotImplementedError
