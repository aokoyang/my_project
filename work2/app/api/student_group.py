from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/add/{student_id}/to/{group_id}")
def add_student_to_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    student = crud.student_group.add_student_to_group(db, student_id, group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"message": "Student added to group"}

@router.post("/remove/{student_id}")
def remove_student_from_group(student_id: int, db: Session = Depends(get_db)):
    student = crud.student_group.remove_student_from_group(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student removed from group"}

@router.post("/transfer/{student_id}/from/{old_group_id}/to/{new_group_id}")
def transfer_student(student_id: int, new_group_id: int, db: Session = Depends(get_db)):
    student = crud.student_group.transfer_student(db, student_id, new_group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"message": "Student transferred"}