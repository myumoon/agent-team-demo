"""TaskServiceのユニットテスト"""
import pytest
from unittest.mock import MagicMock

from taskflow.models.task import Task, TaskStatus
from taskflow.services.task_service import TaskService


def make_storage(tasks=None):
    """テスト用のモックストレージを生成する。"""
    storage = MagicMock()
    storage.load.return_value = tasks if tasks is not None else []
    return storage


class TestAddTask:
    def test_returns_created_task(self):
        storage = make_storage()
        service = TaskService(storage)
        task = service.add_task("Buy milk")
        assert task.title == "Buy milk"
        assert task.description == ""
        assert task.status == TaskStatus.PENDING

    def test_with_description(self):
        storage = make_storage()
        service = TaskService(storage)
        task = service.add_task("Buy milk", description="2% fat")
        assert task.description == "2% fat"

    def test_saves_to_storage(self):
        storage = make_storage()
        service = TaskService(storage)
        task = service.add_task("Buy milk")
        storage.save.assert_called_once()
        saved_tasks = storage.save.call_args[0][0]
        assert task in saved_tasks


class TestListTasks:
    def test_returns_all_tasks(self):
        existing = [Task(title="Task A"), Task(title="Task B")]
        storage = make_storage(existing)
        service = TaskService(storage)
        result = service.list_tasks()
        assert result == existing

    def test_returns_empty_list_when_no_tasks(self):
        storage = make_storage([])
        service = TaskService(storage)
        assert service.list_tasks() == []


class TestCompleteTask:
    def test_marks_task_as_completed(self):
        task = Task(title="Do laundry")
        storage = make_storage([task])
        service = TaskService(storage)
        result = service.complete_task(task.id)
        assert result.status == TaskStatus.COMPLETED

    def test_sets_completed_at(self):
        task = Task(title="Do laundry")
        storage = make_storage([task])
        service = TaskService(storage)
        result = service.complete_task(task.id)
        assert result.completed_at is not None

    def test_saves_after_completion(self):
        task = Task(title="Do laundry")
        storage = make_storage([task])
        service = TaskService(storage)
        service.complete_task(task.id)
        storage.save.assert_called_once()

    def test_raises_value_error_for_unknown_id(self):
        storage = make_storage([])
        service = TaskService(storage)
        with pytest.raises(ValueError):
            service.complete_task("nonexistent-id")


class TestDeleteTask:
    def test_removes_task_from_storage(self):
        task = Task(title="Old task")
        storage = make_storage([task])
        service = TaskService(storage)
        service.delete_task(task.id)
        saved_tasks = storage.save.call_args[0][0]
        assert task not in saved_tasks

    def test_saves_after_deletion(self):
        task = Task(title="Old task")
        storage = make_storage([task])
        service = TaskService(storage)
        service.delete_task(task.id)
        storage.save.assert_called_once()

    def test_raises_value_error_for_unknown_id(self):
        storage = make_storage([])
        service = TaskService(storage)
        with pytest.raises(ValueError):
            service.delete_task("nonexistent-id")
