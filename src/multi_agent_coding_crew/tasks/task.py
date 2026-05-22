"""Task definition and tracking."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
import time
import uuid


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    title: str
    description: str = ""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_agent: Optional[str] = None
    dependencies: list[str] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "assigned_agent": self.assigned_agent,
            "dependencies": self.dependencies,
            "artifacts": self.artifacts,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "error": self.error,
        }


class TaskBoard:
    """Kanban-style task board for tracking crew work."""

    def __init__(self):
        self.tasks: dict[str, Task] = {}

    def add(self, task: Task) -> str:
        self.tasks[task.id] = task
        return task.id

    def update_status(self, task_id: str, status: TaskStatus) -> None:
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")
        self.tasks[task_id].status = status
        if status == TaskStatus.COMPLETED:
            self.tasks[task_id].completed_at = time.time()

    def get_by_status(self, status: TaskStatus) -> list[Task]:
        return [t for t in self.tasks.values() if t.status == status]

    def pending_tasks(self) -> list[Task]:
        return self.get_by_status(TaskStatus.PENDING)

    def summary(self) -> dict[str, int]:
        counts = {}
        for task in self.tasks.values():
            counts[task.status.value] = counts.get(task.status.value, 0) + 1
        return counts
