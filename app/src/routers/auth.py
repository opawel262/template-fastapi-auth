from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from app.src.domain.auth import schemas
from app.src.domain.auth.services import get_tokens, get_access_token_by_refresh_token
from app.src.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.src.core.dependencies import get_db
from typing import Union, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@router.post('/token', response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
async def authenticate_user(data: schemas.CreateToken, response: Response, db: Session = Depends(get_db)):
    tokens = await get_tokens(data=data, db=db)
    response.set_cookie(key='access_token', value=tokens.get('access_token'), httponly=True, max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES.total_seconds()))
    response.set_cookie(key='refresh_token', value=tokens.get('refresh_token'), httponly=True, max_age=int(REFRESH_TOKEN_EXPIRE_DAYS.total_seconds()))
    return tokens
@router.post('/refresh-token', response_model=schemas.AccessToken, status_code=status.HTTP_201_CREATED)
async def refresh_token(response: Response, refresh_token: Optional[str] = Cookie(None)):
    access_token = await get_access_token_by_refresh_token(refresh_token)
    response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES.total_seconds()))
    return {'access_token': access_token}