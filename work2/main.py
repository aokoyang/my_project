from fastapi import FastAPI
from app.api import student, group, student_group
from app.database import Base, engine

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")

app.include_router(student.router, prefix="/students", tags=["students"])
app.include_router(group.router, prefix="/groups", tags=["groups"])
app.include_router(student_group.router, prefix="/student-group", tags=["student-group"])