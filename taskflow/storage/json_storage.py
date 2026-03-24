import json
from abc import ABC, abstractmethod
from pathlib import Path

from taskflow.models.task import Task


class BaseStorage(ABC):
    """ストレージの抽象基底クラス"""

    @abstractmethod
    def load(self) -> list[Task]:
        """タスクの一覧を読み込む"""
        ...

    @abstractmethod
    def save(self, tasks: list[Task]) -> None:
        """タスクの一覧を保存する"""
        ...


class JsonStorage(BaseStorage):
    """JSONファイルへのタスク読み書きを行うストレージクラス"""

    def __init__(self, file_path: str) -> None:
        """
        コンストラクタ

        Args:
            file_path: JSONファイルのパス
        """
        self.file_path = Path(file_path)

    def load(self) -> list[Task]:
        """JSONファイルからタスク一覧を読み込む。ファイルが存在しない場合は空リストを返す。"""
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return [Task.from_dict(item) for item in data]

    def save(self, tasks: list[Task]) -> None:
        """タスク一覧をJSONファイルに保存する。

        Args:
            tasks: 保存するタスクのリスト
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=2)
