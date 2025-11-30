from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    group_id: Optional[int] = None

    class Config:
        from_attributes = True