from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Tolen(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

class UserLogin (BaseModel):
    username: str
    password: str
    
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    role_id: int
    
class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role_id: int
    role_name: str
    is_active: bool
    
    class config: 
        from_attributes = True
        
class UserInDB(UserResponse):
    password_hash: str
