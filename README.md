# Image Segmentation Web App

Final year project (CS619) for the BS Computer Science degree at Virtual University of Pakistan.

A Django web application where registered users upload an image and get it segmented by a pre-trained YOLOv8 segmentation model (`yolov8m-seg`) from Hugging Face. Original and segmented images are kept in a per-user history.

## Features
- User registration and login
- Image upload (JPG, JPEG, PNG, WebP; max 10 MB)
- Object segmentation with `yolov8m-seg` (image size 640, confidence 0.25, IoU 0.45)
- Per-user history and gallery; view, download and delete images

## Tech stack
Python, Django, SQLite, YOLOv8 (Hugging Face / Ultralytics)

## Setup
```bash
git clone https://github.com/tayyab-balti/FYP.git
cd FYP
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Then open http://127.0.0.1:8000/

## Project structure
- `image_segmentation_project/`: Django project settings and URLs
- `registration/`: user registration and login
- `segmentation/`: upload, segmentation, models, forms and templates

## Notes
Built with development settings (`DEBUG = True`, SQLite). Not production-ready.
