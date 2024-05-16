from sqlalchemy.orm import Session

from . import models, schemas

def create_environemnt_record(db: Session, environment_record: schemas.EnvironmentCreate):
    new_record = models.Environment(**environment_record.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def read_environment_by_serial(db: Session, serial: int, start: str, end: str):
    return db.query(models.Environment).filter(
            and_(models.Environment.serial == serial, 
            models.Environment.start >= start,
            mdoels.Environment.end <= end))

def update_environment_record(db: Session, environment_record_id: int, update_info: schemas.EnvironmentBase):
    db.query(models.Environment).update(update_info.dict())
    db.commit()

def delete_environment_record(db: Session, environment_record_id: int):
    db.query(models.Environment).filter(models.Environment.id == environment_record_id)
    db.commit()
