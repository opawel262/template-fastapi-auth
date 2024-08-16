from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from app.src.domain.task import schemas, service, models
from app.src.domain.user.models import User
from app.src.core.dependencies import get_db, get_current_user
from typing import Union

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks'],
)

@router.post('/', response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return service.create_task(task=task, db=db)

@router.get('/', response_model=Page[schemas.Task])
def get_tasks(limit: Union[None, int] = None, db: Session = Depends(get_db)):
    return paginate(service.get_tasks(db, limit=limit))

@router.get('/{task_id}',status_code=status.HTTP_200_OK, response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = service.get_task(task_id=task_id, db=db)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task does not exist')
    return db_task

@router.delete('/{task_id}', response_model=bool, status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    db_task = service.get_task(task_id=task_id, db=db)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task does not exist')
    return service.delete_task(db_task=db_task, db=db)

@router.patch('/{task_id}', response_model=schemas.TaskUpdate, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = service.get_task(task_id=task_id, db=db)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task does not exist')
    updated_task = service.partial_update(db_task=db_task, task=task, db=db)
    return updated_task
