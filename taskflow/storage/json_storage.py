"""JSONファイルを使ったタスクの永続化ストレージ"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from taskflow.models.task import Task, TaskStatus


class JsonStorage:
    """タスクをJSONファイルに保存するストレージクラス。

    Attributes:
        file_path: JSONファイルのパス
    """

    def __init__(self, file_path: str) -> None:
        """JsonStorageを初期化する。

        Args:
            file_path: JSONファイルのパス
        """
        self.file_path = file_path

    def load(self) -> list[Task]:
        """JSONファイルからタスク一覧を読み込む。

        Returns:
            タスクのリスト。ファイルが存在しない場合は空リストを返す。
        """
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [self._dict_to_task(item) for item in data]

    def save(self, tasks: list[Task]) -> None:
        """タスク一覧をJSONファイルに保存する。

        Args:
            tasks: 保存するタスクのリスト
        """
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)

        data = [self._task_to_dict(task) for task in tasks]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _task_to_dict(self, task: Task) -> dict:
        """タスクを辞書に変換する。

        Args:
            task: 変換するタスク

        Returns:
            タスクを表す辞書
        """
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        }

    def _dict_to_task(self, data: dict) -> Task:
        """辞書からタスクを生成する。

        Args:
            data: タスクを表す辞書

        Returns:
            Taskオブジェクト
        """
        completed_at: Optional[datetime] = None
        if data.get("completed_at"):
            completed_at = datetime.fromisoformat(data["completed_at"])

        return Task(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=completed_at,
        )
