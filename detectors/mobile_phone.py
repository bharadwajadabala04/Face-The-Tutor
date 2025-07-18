# detectors/mobile_phone.py

from ultralytics import YOLO
import cv2
import torch
from config import YOLO_MODEL_PATH

model = YOLO(YOLO_MODEL_PATH)  # e.g. "yolov8n.pt" or your custom model path

def is_phone_present(frame):
    results = model(frame, verbose=False)
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls].lower()
            if "phone" in label or "cell" in label:
                return True
    return False
