import torch
import cv2
import numpy as np
from ultralytics import YOLO

# class SegmentationModel:
#     def __init__(self, model_name):
#         self.model = YOLO(model_name)

#     def predict(self, image_path):
#         # Load image
#         img = cv2.imread(image_path)

#         # Get image size
#         img_height, img_width = img.shape[:2]

#         # Convert image to RGB
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#         # Make predictions
#         results = self.model.predict(img, return_outputs=True)

#         # Draw bounding boxes and masks
#         for result in results:
#             for pred in result:
#                 # Get bounding box coordinates
#                 x, y, x2, y2 = pred['box']

#                 # Get class ID and confidence
#                 class_id = pred['class']
#                 confidence = pred['confidence']

#                 # Get mask
#                 mask = pred['mask']

#                 # Draw bounding box
#                 cv2.rectangle(img, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), 2)

#                 # Draw mask
#                 img[mask == 1] = (0, 255, 0)

#         # Convert image back to BGR
#         img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#         # Save image
#         cv2.imwrite('output.jpg', img)

#         return results
    

class SegmentationModel:
    def __init__(self, model_name):
        self.model = YOLO(model_name)

    def predict(self, img):
        # Convert the numpy array to a PIL image
        from PIL import Image
        img = Image.fromarray(img)

        # Save the PIL image to a temporary file
        temp_image_path = 'temp_image.jpg'
        img.save(temp_image_path)

        # Pass the file path to the predict method of the YOLO model
        results = self.model.predict(temp_image_path, return_outputs=True)

        # Remove the temporary image file
        import os
        os.remove(temp_image_path)

        return results