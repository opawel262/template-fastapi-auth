from enum import Enum
from sqlalchemy import Column, Enum as SqlEnum, Integer, String, DateTime
from datetime import datetime
from app.src.core.database import Base

class TaskStatus(str, Enum):
    COMPLETED = 'Completed'
    IN_PROGRESS = 'In Progress'
    CANCELLED = 'Cancelled'

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=True)
    status = Column(SqlEnum(TaskStatus), nullable=False, default=TaskStatus.IN_PROGRESS) 
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
