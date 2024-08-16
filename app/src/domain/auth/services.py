from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.src.core.security import authenticate_user, create_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM
from . import schemas
from app.src.domain.user.models import User
from app.src.core.database import redis_client
from datetime import timedelta, datetime, timezone
from typing import Union, Literal
import jwt
    
async def get_token(data: schemas.Token, db: Session) -> dict:
    user = authenticate_user(db=db, email=data.email, password=data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid credentials'
        )
    
    _verify_user_access(user)
    
    
    access_token = create_token(token_type='access', data={'user_id': str(user.id)}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(token_type='refresh', data={'user_id': str(user.id)}, expires_delta=REFRESH_TOKEN_EXPIRE_DAYS)

    return {'access_token': access_token, 'refresh_token': refresh_token}
    
def get_token_payload(token: str) -> Union[dict]:
    # decode jwt token to payload
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    return payload

def verify_token(token: str) -> Union[dict, None]:
    # check out in  app/src/core/security.py function create_token() to see token payload structure
    payload = get_token_payload(token)
    _validate_jti(jti=payload.get('jti'), user_id=payload.get('user_id'), token_type=payload.get('token_type'))
    
    expiration_timestamp = payload.get('exp')
    
    if expiration_timestamp is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Expiration time not found in token.'
        )
        
    token_type = payload.get('token_type')
    if not token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token type not found in token'
        )
        
    return payload

def _verify_user_access(user: User) -> None:
    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Your account is not verified'
        )

def _validate_jti(jti: str, user_id: str, token_type: Literal['access', 'refresh']) -> None:
    key = f'user:{user_id}:jti:token_type:{token_type}'
    stored_jti = redis_client.get(key)
    
    if stored_jti is None:
        print("Key does not exist in Redis.")
        
    if stored_jti != jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token identifier (jti).",
        )


def _remove_jti(user_id: str, token_type: Literal['access', 'refresh']) -> int:
    """Remove the jti from Redis."""
    key = f'user:{user_id}:jti_token_type:{token_type}'
    result = redis_client.delete(key)
    return result
