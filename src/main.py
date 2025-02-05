from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import psycopg2
import os
import pandas as pd
from fastapi.staticfiles import StaticFiles
import shutil
import cv2 
import pandas as pd


app = FastAPI()

image_dir = os.path.join(os.getcwd(),'..', 'docs', 'images')

# Serve the static files from 'docs/images'
app.mount("/static", StaticFiles(directory=image_dir), name="static")
# Set up Jinja2 template directory
templates = Jinja2Templates(directory="templates")

# PostgreSQL database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="telegram_raw_data",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

# Fetch data from the database
def fetch_detections():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM custom_yolo_detections")
    detections = cursor.fetchall()
    cursor.close()
    conn.close()
    return detections

# HTML Response for displaying detections with CRUD buttons
@app.get("/", response_class=HTMLResponse)
async def read_detections(request: Request):
    detections = fetch_detections()
    return templates.TemplateResponse("index.html", {"request": request, "detections": detections})

# Handle image upload and object detection
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Save uploaded image to the image directory
    image_path = os.path.join(image_dir, file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run object detection model on the uploaded image
    img = cv2.imread(image_path)
    
    # Here, run your YOLO model to get the bounding boxes (e.g., `boxes`) and labels
    boxes = cv2.selectROIs("Select ROIs", img)
    cv2.destroyWindow("Select ROIs")
    
    detections = []
    for i, box in enumerate(boxes):
        x, y, w, h = box
        label = f"label_{i}"  # Replace with actual YOLO detection logic
        detections.append((file.filename, label, x, y, w, h, img.shape[1], img.shape[0]))  # (image_file, label, bbox_x_min, bbox_y_min, bbox_width, bbox_height, image_width, image_height)

    # Save detections to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO custom_yolo_detections (
            image_file, label, bbox_x_min, bbox_y_min, bbox_width, bbox_height, image_width, image_height
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    for detection in detections:
        cursor.execute(insert_query, detection)
    conn.commit()
    cursor.close()
    conn.close()

    return RedirectResponse(url="/", status_code=303)
# Update detection label
@app.post("/update/")
async def update_detection(detection_id: int = Form(...), new_label: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE custom_yolo_detections SET label = %s WHERE id = %s", (new_label, detection_id))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

# Delete a detection entry
@app.post("/delete/")
async def delete_detection(detection_id: int = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM custom_yolo_detections WHERE id = %s", (detection_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

# Create a new detection entry
@app.post("/create/")
async def create_detection(
    image_file: str = Form(...), label: str = Form(...),
    bbox_x_min: int = Form(...), bbox_y_min: int = Form(...),
    bbox_width: int = Form(...), bbox_height: int = Form(...),
    image_width: int = Form(...), image_height: int = Form(...)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO custom_yolo_detections (
            image_file, label, bbox_x_min, bbox_y_min, bbox_width, bbox_height, image_width, image_height
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (image_file, label, bbox_x_min, bbox_y_min, bbox_width, bbox_height, image_width, image_height))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/", status_code=303)
