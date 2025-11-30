from sqlalchemy.orm import Session
from app.models.group import Group as DBGroup
from app.schemas.group import GroupCreate

def get_group(db: Session, group_id: int):
    return db.query(DBGroup).filter(DBGroup.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBGroup).offset(skip).limit(limit).all()

def create_group(db: Session, group: GroupCreate):
    db_group = DBGroup(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    group = db.query(DBGroup).filter(DBGroup.id == group_id).first()
    if group:
        db.delete(group)
        db.commit()
    return group