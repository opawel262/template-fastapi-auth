from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
class UserCreate(UserUpdate):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
    
    
class UserRetrieve(UserUpdate):
    id: UUID
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True
    