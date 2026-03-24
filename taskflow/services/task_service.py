"""タスク管理のビジネスロジック"""
from datetime import datetime
from typing import Protocol

from taskflow.models.task import Task, TaskStatus


class StorageProtocol(Protocol):
    """ストレージのプロトコル定義"""

    def load(self) -> list[Task]:
        """タスク一覧を読み込む"""
        ...

    def save(self, tasks: list[Task]) -> None:
        """タスク一覧を保存する"""
        ...


class TaskNotFoundError(Exception):
    """タスクが見つからない場合の例外"""

    pass


class TaskService:
    """タスク管理のビジネスロジックを提供するサービスクラス。

    Attributes:
        storage: タスクを永続化するストレージ
    """

    def __init__(self, storage: StorageProtocol) -> None:
        """TaskServiceを初期化する。

        Args:
            storage: タスクを永続化するストレージ
        """
        self.storage = storage

    def add_task(self, title: str, description: str = "") -> Task:
        """新しいタスクを追加する。

        Args:
            title: タスクのタイトル
            description: タスクの説明（省略可）

        Returns:
            作成されたタスク
        """
        tasks = self.storage.load()
        task = Task(title=title, description=description)
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def list_tasks(self) -> list[Task]:
        """全タスクを一覧で返す。

        Returns:
            タスクのリスト
        """
        return self.storage.load()

    def complete_task(self, task_id: str) -> Task:
        """指定IDのタスクを完了状態にする。

        Args:
            task_id: 完了するタスクのID

        Returns:
            更新されたタスク

        Raises:
            TaskNotFoundError: 指定IDのタスクが存在しない場合
        """
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                self.storage.save(tasks)
                return task
        raise TaskNotFoundError(f"タスクが見つかりません: {task_id}")

    def delete_task(self, task_id: str) -> None:
        """指定IDのタスクを削除する。

        Args:
            task_id: 削除するタスクのID

        Raises:
            TaskNotFoundError: 指定IDのタスクが存在しない場合
        """
        tasks = self.storage.load()
        original_count = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]
        if len(tasks) == original_count:
            raise TaskNotFoundError(f"タスクが見つかりません: {task_id}")
        self.storage.save(tasks)
