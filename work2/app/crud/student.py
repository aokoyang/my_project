from sqlalchemy.orm import Session
from app.models.student import Student as DBStudent
from app.schemas.student import StudentCreate

def get_student(db: Session, student_id: int):
    return db.query(DBStudent).filter(DBStudent.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBStudent).offset(skip).limit(limit).all()

def create_student(db: Session, student: StudentCreate):
    db_student = DBStudent(name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    student = db.query(DBStudent).filter(DBStudent.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return student