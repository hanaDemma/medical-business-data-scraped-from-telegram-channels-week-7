# schemas.py
from pydantic import BaseModel

class DetectionBase(BaseModel):
    image_file: str
    label: str
    bbox_x_min: float
    bbox_y_min: float
    bbox_width: float
    bbox_height: float

class DetectionCreate(DetectionBase):
    pass

class Detection(DetectionBase):
    id: int

    class Config:
        orm_mode = True
