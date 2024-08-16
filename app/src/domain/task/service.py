from sqlalchemy.orm import Session
from . import schemas, models
from typing import Union

def create_task(task: schemas.TaskCreate, db: Session):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, limit: Union[None, int] = None, sort_by_date: bool = False):
    return db.query(models.Task).limit(limit=limit).all()
    
def get_task(task_id: int, db: Session):
    return db.query(models.Task).filter(models.Task.id == task_id).first()
    
def delete_task(db_task: models.Task, db: Session) -> bool:
    db.delete(db_task)
    db.commit()
    return True

def partial_update(db_task: models.Task, task: schemas.TaskUpdate, db: Session):
    update_task = task.model_dump(exclude_unset=True)

    for field, value in update_task.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task