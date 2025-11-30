from sqlalchemy.orm import Session
from app.models.student import Student as DBStudent
from app.models.group import Group as DBGroup

def add_student_to_group(db: Session, student_id: int, group_id: int):
    student = db.query(DBStudent).filter(DBStudent.id == student_id).first()
    group = db.query(DBGroup).filter(DBGroup.id == group_id).first()
    if student and group:
        student.group_id = group_id
        db.commit()
        db.refresh(student)
    return student

def remove_student_from_group(db: Session, student_id: int):
    student = db.query(DBStudent).filter(DBStudent.id == student_id).first()
    if student:
        student.group_id = None
        db.commit()
        db.refresh(student)
    return student

def transfer_student(db: Session, student_id: int, new_group_id: int):
    student = db.query(DBStudent).filter(DBStudent.id == student_id).first()
    new_group = db.query(DBGroup).filter(DBGroup.id == new_group_id).first()
    if student and new_group:
        student.group_id = new_group_id
        db.commit()
        db.refresh(student)
    return student

def get_students_in_group(db: Session, group_id: int):
    return db.query(DBStudent).filter(DBStudent.group_id == group_id).all()