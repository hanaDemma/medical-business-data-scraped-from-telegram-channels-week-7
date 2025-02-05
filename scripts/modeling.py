import torch
import os
import cv2
import pandas as pd
import logging
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle

# Setup logging
logging.basicConfig(filename='../logs/yolo_detection.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def modeling():
    # Define paths
    IMAGE_DIR = '../docs/images/'
    OUTPUT_DIR = '../docs/yolo_output/'

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # List to store all detection results
    all_detections = []

    # Loop through all images in the directory
    for img_file in os.listdir(IMAGE_DIR):
        img_path = os.path.join(IMAGE_DIR, img_file)
        
        if img_file.endswith(('.jpg', '.jpeg', '.png')):
            # Read the image using OpenCV
            img = cv2.imread(img_path)
            height, width, _ = img.shape  # Get image dimensions
            
            # Run YOLO detection
            results = model(img)
            
            # Convert results to pandas DataFrame for easier manipulation
            results_df = results.pandas().xyxy[0]  # Get results in YOLO xyxy format
            
            # Add image metadata to each detection
            results_df['image_file'] = img_file
            results_df['image_width'] = width
            results_df['image_height'] = height
            results_df['aspect_ratio'] = width / height
            
            # Append results to the list
            all_detections.append(results_df)
            
            # Save the detection results to the output folder
            results.save(OUTPUT_DIR)
            
            logging.info(f'Processed {img_file} and saved results to {OUTPUT_DIR}')
            print(f'Detected objects in {img_file}')

    # Concatenate all detection results into a single DataFrame
    if all_detections:
        final_detections_df = pd.concat(all_detections, ignore_index=True)

        # Save the final DataFrame to CSV
        final_detections_df.to_csv(os.path.join(OUTPUT_DIR, 'yolo_detections.csv'), index=False)

        # Preview the DataFrame
        final_detections_df.head()
    else:
        print("No valid detections found.")


def custom_modeling():
    # Define paths
    IMAGE_DIR = '../docs/images/'
    OUTPUT_DIR = '../docs/yolo_output/'

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # List to store all detection results
    all_detections = []

    # Function to display an image with bounding boxes in Jupyter Notebook
    def display_image_with_boxes(img, boxes):
        fig, ax = plt.subplots(1)
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # Display image
        
        # Draw bounding boxes
        for box in boxes:
            x, y, w, h = box
            rect = Rectangle((x, y), w, h, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        
        plt.show()

    # Loop through all images in the directory
    for img_file in os.listdir(IMAGE_DIR):
        img_path = os.path.join(IMAGE_DIR, img_file)
        
        if img_file.endswith(('.jpg', '.jpeg', '.png')):
            # Read the image using OpenCV
            img = cv2.imread(img_path)
            height, width, _ = img.shape  # Get image dimensions
            
            # Select ROIs
            boxes = cv2.selectROIs("Select ROIs", img)
            cv2.destroyWindow("Select ROIs")
            
            if len(boxes) > 0:
                display_image_with_boxes(img, boxes)  # Show image with selected boxes
                
                # Collect labels for each bounding box
                for i, box in enumerate(boxes):
                    x, y, w, h = box
                    label = input(f"Enter label for section {i+1} of {img_file}: ")
                    
                    detection = {
                        'image_file': img_file,
                        'label': label,
                        'bbox_x_min': x,
                        'bbox_y_min': y,
                        'bbox_width': w,
                        'bbox_height': h,
                        'image_width': width,
                        'image_height': height
                    }
                    all_detections.append(detection)
                
                output_image_path = os.path.join(OUTPUT_DIR, img_file)
                for box in boxes:
                    x, y, w, h = box
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.imwrite(output_image_path, img)

    if all_detections:
        final_detections_df = pd.DataFrame(all_detections)

        final_detections_df.to_csv(os.path.join(OUTPUT_DIR, 'custom_labeled_data.csv'), index=False)

        final_detections_df.head()
    else:
        print("No detections made.")

def save_prediction_data():
    # Load your CSV
    csv_path = '../docs/yolo_output/custom_labeled_data.csv'
    df = pd.read_csv(csv_path)

    # Define a path for YOLO annotation files
    yolo_output_dir = '../docs/yolo_annotations/'
    os.makedirs(yolo_output_dir, exist_ok=True)

    # Convert each row to YOLO format
    for _, row in df.iterrows():
        class_id = 0  # Modify if you have multiple classes
        x_center = (row['bbox_x_min'] + row['bbox_width'] / 2) / row['image_width']
        y_center = (row['bbox_y_min'] + row['bbox_height'] / 2) / row['image_height']
        width = row['bbox_width'] / row['image_width']
        height = row['bbox_height'] / row['image_height']

        annotation_filename = os.path.splitext(row['image_file'])[0] + '.txt'
        with open(os.path.join(yolo_output_dir, annotation_filename), 'w') as f:
            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")