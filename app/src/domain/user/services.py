from sqlalchemy.orm import Session
from . import schemas, models
from typing import Union

def create_user(user: schemas.UserCreate, db: Session):
    from app.src.core.security import get_password_hash

    user.password = get_password_hash(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()
