"""タスク管理サービス"""
from datetime import datetime

from taskflow.models.task import Task, TaskStatus
from taskflow.storage.base import BaseStorage


class TaskService:
    """タスク管理サービス"""

    def __init__(self, storage: BaseStorage) -> None:
        """StorageをDIで受け取る。

        Args:
            storage: タスクの永続化を担うストレージ実装
        """
        self._storage = storage

    def add_task(self, title: str, description: str = "") -> Task:
        """タスクを追加して返す。

        Args:
            title: タスクのタイトル
            description: タスクの説明（省略可）

        Returns:
            作成されたタスク
        """
        tasks = self._storage.load()
        task = Task(title=title, description=description)
        tasks.append(task)
        self._storage.save(tasks)
        return task

    def list_tasks(self) -> list[Task]:
        """全タスクを返す。

        Returns:
            タスクのリスト
        """
        return self._storage.load()

    def complete_task(self, task_id: str) -> Task:
        """タスクを完了にして返す。

        Args:
            task_id: 完了にするタスクのID

        Returns:
            更新されたタスク

        Raises:
            ValueError: 指定されたIDのタスクが存在しない場合
        """
        tasks = self._storage.load()
        for task in tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                self._storage.save(tasks)
                return task
        raise ValueError(f"Task with id '{task_id}' not found")

    def delete_task(self, task_id: str) -> None:
        """タスクを削除する。

        Args:
            task_id: 削除するタスクのID

        Raises:
            ValueError: 指定されたIDのタスクが存在しない場合
        """
        tasks = self._storage.load()
        for i, task in enumerate(tasks):
            if task.id == task_id:
                tasks.pop(i)
                self._storage.save(tasks)
                return
        raise ValueError(f"Task with id '{task_id}' not found")
