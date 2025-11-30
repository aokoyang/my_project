from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class Token(BaseModel):
    access_token: str          
    refresh_token: str         
    token_type: str = "bearer" 

class LoginHistoryEntry(BaseModel):
    user_agent: str            
    login_time: datetime       

    class Config:
        from_attributes = True  


class LoginJson(BaseModel):
    email: str      
    password: str   