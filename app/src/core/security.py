from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Union, Literal
from datetime import timedelta, timezone, datetime
from app.src.core.utils.exceptions import ObligatoryEnvIsNoneException
from app.src.domain.user.models import User
from app.src.domain.user.services import get_user_by_email
from app.src.domain.auth import schemas
from app.src.core.database import redis_client
import jwt
import os
from uuid import uuid4

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRE_DAYS = timedelta(days=10)
SECRET_KEY = os.environ.get('FASTAPI_SECRET_KEY', None)
if not SECRET_KEY:
    raise ObligatoryEnvIsNoneException('Secret key is not set')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str) -> Union[User, False]:
    # authenticate user by checking if user exists by email and if exists check password
    user = get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_token(token_type: Literal['access', 'refresh'], data: dict = None, expires_delta: timedelta | None = timedelta(days=7)):
    """ Create jwt token """
    
    to_encode = data.copy()
    
    iat = datetime.utcnow()
    exp = iat + expires_delta
    
    jti = str(uuid4())
    
    to_encode.update({
        'token_type': token_type,
        'exp': exp,
        'iat': iat,
        'jti': jti,
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    _store_jti(user_id=to_encode['user_id'], jti=jti, token_type=token_type, expires_in=expires_delta)

    return encoded_jwt

def _store_jti(user_id: str, jti: str, token_type: Literal['access', 'refresh'], expires_in: timedelta):
    """Store the jti in Redis with an expiration time."""
    key = f'user:{user_id}:jti:token_type:{token_type}'
    redis_client.set(key, jti, expires_in)
