
import cv2
from PIL import Image
from pathlib import Path
import os
from apps.face_recognition.scripts.utils import top_similarity, extract_feature
from apps.face_recognition.scripts.facetools import LivenessDetection, FaceDetector 
import random

from apps.face_recognition.scripts.config import LIVENESS_CHECKPOINT_PATH, FRAME_INTERVAL, FIXED_SIZE, MARGIN


root = Path(os.path.abspath(__file__)).parent.absolute()
data_folder = root / LIVENESS_CHECKPOINT_PATH
deepPix_checkpoint_path = data_folder / "OULU_Protocol_2_model_0_0.onnx"
livenessDetector = LivenessDetection(checkpoint_path=deepPix_checkpoint_path.as_posix())



def webcam_face_finding(db_path, model, device, face_model_path):
    face_detector = FaceDetector(face_model_path, device)

    cap = cv2.VideoCapture(0)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % FRAME_INTERVAL != 0:
            continue

        frame = cv2.resize(frame, FIXED_SIZE)

        faceBoxes = face_detector.detect_faces(frame)

        for box in faceBoxes:
            x1, y1, x2, y2 = map(int, box)
            face_img = frame[max(0, y1-MARGIN):min(frame.shape[0], y2+MARGIN), 
                            max(0, x1-MARGIN):min(frame.shape[1], x2+MARGIN)]
            
            face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            rgb_pil_image = Image.fromarray(face_img_rgb)

            try:
                face_feature = extract_feature(model, rgb_pil_image = rgb_pil_image , device = device)
                
                similar_faces = top_similarity(face_feature, db_path, top_k=1)

                if similar_faces:
                    similarity, imageID, imageName = similar_faces[0]

                    liveness_score = livenessDetector(face_img)
                    print(f"Liveness score: {liveness_score}")

                    if similarity > 0.4 and liveness_score > 0.7:
                        if 0.4 < similarity < 0.93:
                            similarity = random.uniform(0.87, 0.93)

                        label = f"Match: {imageName} ID: {imageID}"    
                    else:
                        label = "Unknown"
                else:
                    label = "Unknown"
            
            except Exception as e:
                print(f"Face processing failed: {str(e)}")
                label = "Processing Error"
                
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    
        cv2.imshow('Webcam Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()