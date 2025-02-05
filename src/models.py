# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Detection(Base):
    __tablename__ = 'custom_yolo_detections'

    id = Column(Integer, primary_key=True, index=True)
    image_file = Column(String, index=True)
    label = Column(String, index=True)
    bbox_x_min = Column(Float)
    bbox_y_min = Column(Float)
    bbox_width = Column(Float)
    bbox_height = Column(Float)
