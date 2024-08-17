from fastapi import Depends, Request, Cookie, HTTPException, status
from app.src.domain.auth.services import verify_token
from typing import Optional, Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token-openai-cookie")

def get_db(request: Request):
    return request.state.db

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    access_token: Optional[str] = Cookie(None)) -> str:
    """
    Get the current user by using the access token from cookies.
    
    Parameters:
    - access_token: The access token retrieved from cookies.
    - db: The database session.
    
    Returns:
    - A dictionary representing the current user.
    
    Raises:
    - HTTPException: If the access token is invalid or missing.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is required."
        )
    
    # Function to retrieve user from token (pseudo-code)
    payload = verify_token(access_token)
        
    user_id = payload.get('user_id')
    return user_id