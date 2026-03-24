"""ストレージ基底クラス"""
from abc import ABC, abstractmethod
from taskflow.models.task import Task


class BaseStorage(ABC):
    """ストレージの抽象基底クラス"""

    @abstractmethod
    def load(self) -> list[Task]:
        """タスク一覧を読み込む"""
        ...

    @abstractmethod
    def save(self, tasks: list[Task]) -> None:
        """タスク一覧を保存する"""
        ...
