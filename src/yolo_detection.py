import torch
import os
import cv2
import requests 

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

IMAGE_DIR = '../docs/images/'
OUTPUT_DIR = '../docs/yolo_output/'

for img_file in os.listdir(IMAGE_DIR):
    img_path = os.path.join(IMAGE_DIR, img_file)
    
    if img_file.endswith(('.jpg', '.jpeg', '.png')):
        img = cv2.imread(img_path)
        
        results = model(img)
        
        results_df = results.pandas().xyxy[0]  
        for index, row in results_df.iterrows():
            detection_data = {
                "image_file": img_file,
                "label": str(row['label']),  
                "bbox_x_min": float(row['xmin']),
                "bbox_y_min": float(row['ymin']),
                "bbox_width": float(row['xmax']) - float(row['xmin']),
                "bbox_height": float(row['ymax']) - float(row['ymin']),
            }
            
            response = requests.post("http://127.0.0.1:8000/detections/", json=detection_data)
            print(response.json())  