from datetime import datetime
from pathlib import Path

import pytest

from taskflow.models.task import Task, TaskStatus
from taskflow.storage.json_storage import JsonStorage


def make_task(title: str, status: TaskStatus = TaskStatus.PENDING) -> Task:
    """テスト用Taskを生成するヘルパー"""
    return Task(
        title=title,
        description=f"{title}の説明",
        id=f"id-{title}",
        status=status,
        created_at=datetime(2026, 3, 24, 12, 0, 0),
        completed_at=None,
    )


def test_load_returns_empty_list_when_file_not_exists(tmp_path: Path):
    """ファイルが存在しない場合は空リストを返す"""
    storage = JsonStorage(str(tmp_path / "tasks.json"))

    result = storage.load()

    assert result == []


def test_save_and_load_single_task(tmp_path: Path):
    """1つのタスクを保存・読み込みできる"""
    storage = JsonStorage(str(tmp_path / "tasks.json"))
    task = make_task("タスク1")

    storage.save([task])
    loaded = storage.load()

    assert len(loaded) == 1
    assert loaded[0].id == task.id
    assert loaded[0].title == task.title
    assert loaded[0].status == task.status


def test_save_and_load_multiple_tasks(tmp_path: Path):
    """複数のタスクを保存・読み込みできる"""
    storage = JsonStorage(str(tmp_path / "tasks.json"))
    tasks = [make_task("タスク1"), make_task("タスク2"), make_task("タスク3", TaskStatus.COMPLETED)]

    storage.save(tasks)
    loaded = storage.load()

    assert len(loaded) == 3
    assert loaded[0].id == "id-タスク1"
    assert loaded[1].id == "id-タスク2"
    assert loaded[2].id == "id-タスク3"
    assert loaded[2].status == TaskStatus.COMPLETED


def test_save_overwrites_existing_file(tmp_path: Path):
    """保存時に既存ファイルを上書きする"""
    storage = JsonStorage(str(tmp_path / "tasks.json"))
    task1 = make_task("最初のタスク")
    task2 = make_task("上書きタスク")

    storage.save([task1])
    storage.save([task2])
    loaded = storage.load()

    assert len(loaded) == 1
    assert loaded[0].id == task2.id


def test_save_creates_parent_directories(tmp_path: Path):
    """保存時に親ディレクトリが存在しなくても作成される"""
    storage = JsonStorage(str(tmp_path / "nested" / "dir" / "tasks.json"))
    task = make_task("タスク")

    storage.save([task])
    loaded = storage.load()

    assert len(loaded) == 1
    assert loaded[0].title == task.title


def test_roundtrip_preserves_all_fields(tmp_path: Path):
    """保存・読み込みで全フィールドが保持される"""
    storage = JsonStorage(str(tmp_path / "tasks.json"))
    completed_at = datetime(2026, 3, 24, 15, 0, 0)
    task = Task(
        title="完全なタスク",
        description="詳細説明",
        id="full-task-id",
        status=TaskStatus.COMPLETED,
        created_at=datetime(2026, 3, 24, 10, 0, 0),
        completed_at=completed_at,
    )

    storage.save([task])
    loaded = storage.load()

    assert len(loaded) == 1
    t = loaded[0]
    assert t.id == "full-task-id"
    assert t.title == "完全なタスク"
    assert t.description == "詳細説明"
    assert t.status == TaskStatus.COMPLETED
    assert t.created_at == datetime(2026, 3, 24, 10, 0, 0)
    assert t.completed_at == completed_at


def test_save_empty_list(tmp_path: Path):
    """空リストを保存して読み込むと空リストになる"""
    storage = JsonStorage(str(tmp_path / "tasks.json"))

    storage.save([])
    loaded = storage.load()

    assert loaded == []
