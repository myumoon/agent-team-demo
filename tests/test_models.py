from datetime import datetime

import pytest

from taskflow.models.task import Task, TaskStatus


def test_task_creation_defaults():
    """Task生成時のデフォルト値を確認する"""
    task = Task(title="テストタスク")

    assert task.title == "テストタスク"
    assert task.description == ""
    assert task.id is not None
    assert len(task.id) > 0
    assert task.status == TaskStatus.PENDING
    assert isinstance(task.created_at, datetime)
    assert task.completed_at is None


def test_task_creation_with_all_fields():
    """全フィールドを指定してTaskを生成できる"""
    now = datetime.now()
    task = Task(
        title="完了タスク",
        description="詳細説明",
        id="custom-id",
        status=TaskStatus.COMPLETED,
        created_at=now,
        completed_at=now,
    )

    assert task.title == "完了タスク"
    assert task.description == "詳細説明"
    assert task.id == "custom-id"
    assert task.status == TaskStatus.COMPLETED
    assert task.created_at == now
    assert task.completed_at == now


def test_task_to_dict():
    """to_dictが正しく辞書形式に変換できる"""
    now = datetime(2026, 3, 24, 12, 0, 0)
    task = Task(
        title="タスク",
        description="説明",
        id="test-id",
        status=TaskStatus.PENDING,
        created_at=now,
        completed_at=None,
    )

    result = task.to_dict()

    assert result["id"] == "test-id"
    assert result["title"] == "タスク"
    assert result["description"] == "説明"
    assert result["status"] == "pending"
    assert result["created_at"] == now.isoformat()
    assert result["completed_at"] is None


def test_task_to_dict_with_completed_at():
    """completed_atがある場合のto_dictを確認する"""
    now = datetime(2026, 3, 24, 12, 0, 0)
    task = Task(
        title="完了タスク",
        id="test-id",
        status=TaskStatus.COMPLETED,
        created_at=now,
        completed_at=now,
    )

    result = task.to_dict()

    assert result["status"] == "completed"
    assert result["completed_at"] == now.isoformat()


def test_task_from_dict():
    """from_dictが辞書からTaskを正しく生成できる"""
    now = datetime(2026, 3, 24, 12, 0, 0)
    data = {
        "id": "test-id",
        "title": "タスク",
        "description": "説明",
        "status": "pending",
        "created_at": now.isoformat(),
        "completed_at": None,
    }

    task = Task.from_dict(data)

    assert task.id == "test-id"
    assert task.title == "タスク"
    assert task.description == "説明"
    assert task.status == TaskStatus.PENDING
    assert task.created_at == now
    assert task.completed_at is None


def test_task_roundtrip():
    """to_dict -> from_dictで同一Taskが復元できる"""
    original = Task(
        title="往復テスト",
        description="往復テスト説明",
        id="roundtrip-id",
        status=TaskStatus.COMPLETED,
        created_at=datetime(2026, 3, 24, 10, 0, 0),
        completed_at=datetime(2026, 3, 24, 11, 0, 0),
    )

    restored = Task.from_dict(original.to_dict())

    assert restored.id == original.id
    assert restored.title == original.title
    assert restored.description == original.description
    assert restored.status == original.status
    assert restored.created_at == original.created_at
    assert restored.completed_at == original.completed_at


def test_task_status_values():
    """TaskStatusの値が正しい"""
    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus.COMPLETED.value == "completed"


def test_task_status_from_string():
    """文字列からTaskStatusに変換できる"""
    assert TaskStatus("pending") == TaskStatus.PENDING
    assert TaskStatus("completed") == TaskStatus.COMPLETED
