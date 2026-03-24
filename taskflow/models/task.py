"""タスクデータモデル"""
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
    """タスクエンティティ"""
    title: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
