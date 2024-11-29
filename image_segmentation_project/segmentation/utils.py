# import requests

# def call_huggingface_segmentation(image_path):
#     """
#     Sends an image to the Hugging Face YOLOv8 segmentation API for processing.
    
#     :param image_path: Path to the image file to be sent.
#     :return: JSON response from the API.
#     """
#     api_url = "https://hf.space/embed/fcakyon/yolov8-segmentation/api/predict/"
    
#     # Open the image file and send it in the request
#     with open(image_path, "rb") as image_file:
#         files = {"file": image_file}
#         response = requests.post(api_url, files=files)
    
#     if response.status_code == 200:
#         return response.json()  # Successfully received the response
#     else:
#         raise Exception(f"API request failed: {response.status_code}, {response.text}")


from .segmentation_model import SegmentationModel

# def call_huggingface_segmentation(image_path):
#     model = SegmentationModel("yolov8m-seg.pt")
#     results = model.predict(image_path)
#     return results


import cv2
import numpy as np
import time

def call_huggingface_segmentation(image_pair):
    model = SegmentationModel("yolov8m-seg.pt")

    # Convert the image to a numpy array
    img = cv2.imread(image_pair.original_image.path)

    # Start the timer
    start_time = time.time()

    # Pass the numpy array to the predict method
    results = model.predict(img)

    # Stop the timer
    end_time = time.time()

    # Calculate the processing time
    processing_time = end_time - start_time

    # Return the results and the processing time
    return results, processing_time