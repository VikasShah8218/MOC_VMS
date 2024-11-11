import cv2
import os
from pathlib import Path
import shutil
from apps.face_recognition.scripts.facetools import FaceValidationSystem, FaceDetector, LivenessDetection
from apps.face_recognition.scripts.utils import extract_feature, store_feature_in_db, top_similarity
from apps.face_recognition.scripts.config import LIVENESS_THRESHOLD, LIVENESS_CHECKPOINT_PATH, EAR_THRESHOLD, ROI_PADDING, SIMILARITY_THRESHOLD

root = Path(os.path.abspath(__file__)).parent.absolute()
data_folder = root / LIVENESS_CHECKPOINT_PATH
deepPix_checkpoint_path = data_folder / "OULU_Protocol_2_model_0_0.onnx"

def store_features_in_db_with_name(db_path, image_path, person_name, feature, similarity_threshold=0.43, top_k=1):
    return store_feature_in_db(db_path, feature, image_path, person_name, similarity_threshold, top_k)

def recognize_face(db_path, feature, top_k=1, similarity_threshold=SIMILARITY_THRESHOLD):
    try:
        similar_faces, stored_imageID = top_similarity(feature, db_path, top_k)
        if similar_faces:
            best_similarity, image_name = similar_faces[0]
            if best_similarity > similarity_threshold:
                return best_similarity, stored_imageID, image_name
        return None, None, None
    except Exception as e:
        return None, None, None

# Face registration with recognition and liveness detection
def webcam_face_registration(db_path, model, device, face_model_path):
    cap = cv2.VideoCapture(0)
    detector = FaceValidationSystem(face_model_path, device, EAR_THRESHOLD, ROI_PADDING)
    face_detector = FaceDetector(face_model_path, device)
    livenessDetector = LivenessDetection(checkpoint_path=deepPix_checkpoint_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        status, avg_ear = detector.check_face(frame)
        height, width, _ = frame.shape
        square_size = min(width, height) - 2 * detector.roi_padding
        roi_x = (width - square_size) // 2
        roi_y = (height - square_size) // 2

        # Set ROI color based on the current status
        roi_color = (0, 255, 0) if status == "OK" else (0, 0, 255)
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + square_size, roi_y + square_size), roi_color, 2)
        cv2.putText(frame, f'Status: {status}', (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, roi_color, 2)
        
        if status == "OK":
            face_bboxes = face_detector.detect_faces(frame)
            for bbox in face_bboxes:
                x1, y1, x2, y2 = bbox[:4]
                face_region = frame[y1:y2, x1:x2]
                liveness_score = livenessDetector(face_region)

                if liveness_score < LIVENESS_THRESHOLD:
                    cv2.putText(frame, "Not Live!", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Live Face Detected", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    captured_face_path = "captured_face.jpg"
                    cv2.imwrite(captured_face_path, face_region)
                    try:
                        feature = extract_feature(model, image_path=captured_face_path, device=device)

                        similarity, person_id, person_name = recognize_face(db_path, feature)

                        if person_name:
                            cv2.putText(frame, f'Recognized: {person_name}', (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, "Press 'c' to register", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    except:
                        pass
                    
        cv2.imshow('Face Registration System', frame)


        if cv2.waitKey(5) & 0xFF == ord('c'):
            if status == "OK" and liveness_score >= LIVENESS_THRESHOLD:
                person_name = input("Enter the name of the person: ")
                success = store_features_in_db_with_name(db_path, captured_face_path, person_name, feature)
                if success:
                    print("Face saved successfully.")
                    shutil.copy(captured_face_path, f"RegisteredFace/{person_id}_{os.path.basename(captured_face_path)}")
                else:
                    print("Face already exists in the database.")

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
