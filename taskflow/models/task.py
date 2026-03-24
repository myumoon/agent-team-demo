"""タスクのデータモデル定義"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class TaskStatus(Enum):
    """タスクのステータス"""

    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class Task:
    """タスクを表すデータクラス。

    Attributes:
        title: タスクのタイトル
        description: タスクの説明
        id: タスクの一意識別子（UUID4）
        status: タスクのステータス
        created_at: タスクの作成日時
        completed_at: タスクの完了日時（未完了の場合はNone）
    """

    title: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """辞書からTaskを生成"""
        completed_at = None
        if data.get("completed_at"):
            completed_at = datetime.fromisoformat(data["completed_at"])

        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=completed_at,
        )
