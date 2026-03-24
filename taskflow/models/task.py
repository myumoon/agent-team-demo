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
    status: TaskStatus = field(default=TaskStatus.PENDING)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
