# crud.py
from sqlalchemy.orm import Session
from models import Detection
from schemas import DetectionCreate

def create_detection(db: Session, detection: DetectionCreate):
    db_detection = Detection(**detection.dict())
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection

def get_detections(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Detection).offset(skip).limit(limit).all()
