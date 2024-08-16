from pydantic import BaseModel
from app.src.domain.task.models import TaskStatus
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    body: str
    status: TaskStatus

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    status: Optional[TaskStatus] = None

class Task(TaskCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
