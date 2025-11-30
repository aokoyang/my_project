from pydantic import BaseModel
from typing import List, Optional

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    students: List["Student"] = []

    class Config:
        from_attributes = True
        
from app.schemas.student import Student
Group.update_forward_refs()