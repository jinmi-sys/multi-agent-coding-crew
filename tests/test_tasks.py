"""Tests for task board."""

import pytest
from multi_agent_coding_crew.tasks.task import Task, TaskBoard, TaskStatus, TaskPriority


class TestTask:
    def test_create_task(self):
        t = Task(title="Build API")
        assert t.title == "Build API"
        assert t.status == TaskStatus.PENDING
        assert t.priority == TaskPriority.MEDIUM
        assert len(t.id) == 8

    def test_task_to_dict(self):
        t = Task(title="Test", description="desc")
        d = t.to_dict()
        assert d["title"] == "Test"
        assert d["status"] == "pending"

    def test_unique_ids(self):
        ids = {Task(title=f"Task {i}").id for i in range(100)}
        assert len(ids) == 100


class TestTaskBoard:
    def test_add_task(self):
        board = TaskBoard()
        t = Task(title="Deploy")
        tid = board.add(t)
        assert tid in board.tasks

    def test_update_status(self):
        board = TaskBoard()
        t = Task(title="Code")
        board.add(t)
        board.update_status(t.id, TaskStatus.IN_PROGRESS)
        assert board.tasks[t.id].status == TaskStatus.IN_PROGRESS

    def test_update_sets_completed_at(self):
        board = TaskBoard()
        t = Task(title="Done task")
        board.add(t)
        board.update_status(t.id, TaskStatus.COMPLETED)
        assert board.tasks[t.id].completed_at is not None

    def test_update_missing_raises(self):
        board = TaskBoard()
        with pytest.raises(KeyError):
            board.update_status("nonexistent", TaskStatus.COMPLETED)

    def test_pending_tasks(self):
        board = TaskBoard()
        t1 = Task(title="A")
        t2 = Task(title="B")
        board.add(t1)
        board.add(t2)
        board.update_status(t1.id, TaskStatus.IN_PROGRESS)
        pending = board.pending_tasks()
        assert len(pending) == 1
        assert pending[0].id == t2.id

    def test_summary(self):
        board = TaskBoard()
        board.add(Task(title="A"))
        board.add(Task(title="B"))
        s = board.summary()
        assert s["pending"] == 2
