from ultralytics import YOLO
import logging

class FaceDetector:
    def __init__(self, model_path, device):
        logging.getLogger().setLevel(logging.WARNING)
        
        self.model = YOLO(model_path).to(device)

    def detect_faces(self, frame, margin=2, conf_threshold=0.5):
        results = self.model.predict(frame, verbose=False)[0] 
        filtered_boxes = results.boxes[results.boxes.cls == 0]  
        filtered_boxes = filtered_boxes[filtered_boxes.conf >= conf_threshold]

        boxes_with_margin = []
        for box in filtered_boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            boxes_with_margin.append((x1 - margin, y1 - margin, x2 + margin, y2 + margin))

        return boxes_with_margin
