import cv2
import os
import shutil
from pathlib import Path
from apps.face_recognition.scripts.facetools import FaceValidationSystem, FaceDetector, LivenessDetection
from apps.face_recognition.scripts.utils import extract_feature, store_feature_in_db, top_similarity, delete_from_db
from apps.face_recognition.scripts.config import LIVENESS_CHECKPOINT_PATH, MIN_FACE_HEIGHT, MIN_FACE_WIDTH, SIMILARITY_THRESHOLD, LIVENESS_THRESHOLD, ROI_PADDING, EAR_THRESHOLD, FRAME_INTERVAL

# Initialize Liveness Detection
root = Path(os.path.abspath(__file__)).parent.absolute()
data_folder = root / LIVENESS_CHECKPOINT_PATH
deepPix_checkpoint_path = data_folder / "OULU_Protocol_2_model_0_0.onnx"
livenessDetector = LivenessDetection(checkpoint_path=deepPix_checkpoint_path.as_posix())

def store_features_in_db_with_name(db_path, image_path, person_name, feature, similarity_threshold=SIMILARITY_THRESHOLD, top_k=1):
    return store_feature_in_db(db_path, feature, image_path, person_name, similarity_threshold, top_k)

def recognize_face(db_path, feature, top_k=1, similarity_threshold=SIMILARITY_THRESHOLD):
    try:
        similar_faces = top_similarity(feature, db_path, top_k)
        if similar_faces:
            similarity, imageID, imageName = similar_faces[0]
            
            if similarity > similarity_threshold:
                return similarity, imageID, imageName
            
        return None, None, None
    except Exception as e:
        return None, None, None

def process_face(frame, x1, y1, x2, y2, width, height):
    if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
        return None
    roi_frame = frame[y1:y2, x1:x2]
    if roi_frame.size == 0 or roi_frame.shape[0] < MIN_FACE_HEIGHT or roi_frame.shape[1] < MIN_FACE_WIDTH:
        return None
    return roi_frame

def save_and_extract_feature(roi_frame, model, device):
    captured_face_path = "face.jpg"
    cv2.imwrite(captured_face_path, roi_frame)
    
    if os.path.exists(captured_face_path):
        feature = extract_feature(model, image_path=captured_face_path, device=device)
        return feature, captured_face_path
    return None, None

def webcam_RegAndFind(db_path, model, device, face_model_path):
    cap = cv2.VideoCapture(0)
    detector = FaceValidationSystem(face_model_path, device, ear_threshold=EAR_THRESHOLD, roi_padding=ROI_PADDING)
    face_detector = FaceDetector(face_model_path, device)
    os.makedirs("RegisteredFace", exist_ok=True)
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        frame_count += 1
        if frame_count % FRAME_INTERVAL != 0:
            continue

        frame_count = 0
        face_boxes = face_detector.detect_faces(frame)
        status, avg_ear = detector.check_face(frame)
        height, width, _ = frame.shape

        recognized_faces = []
        for (x1, y1, x2, y2) in face_boxes:
            roi_frame = process_face(frame, x1, y1, x2, y2, width, height)
            if roi_frame is None:
                continue
            
            try:
                feature, captured_face_path = save_and_extract_feature(roi_frame, model, device)
                if feature is not None:
                    liveness_score = livenessDetector(roi_frame)
                    if liveness_score < LIVENESS_THRESHOLD:
                        print("Face does not appear to be live. Please use a live face.")
                        continue

                    similarity, person_id, person_name = recognize_face(db_path, feature)
                    
                    recognized_faces.append((person_id, person_name))
                    
                    if person_name:
                        cv2.putText(frame, f'Name: {person_name} ID: {person_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, 'Unknown', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0) if person_name else (0, 0, 255), 2)
                else:
                    print("Feature extraction failed.")
            except Exception as e:
                print(f"Error processing face: {e}")
        
        # Display status
        cv2.putText(frame, f'Status: {"OK" if status == "OK" else "Not OK"}', (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if status == "OK" else (0, 0, 255), 2)
        cv2.imshow('Face Registration System', frame)
        
        key = cv2.waitKey(5) & 0xFF

        # Delete face on 'd' key press
        if key == ord('d'):
            if recognized_faces:
                print("Matching IDs for deletion:")
                for person_id, person_name in recognized_faces:
                    print(f"ID: {person_id}, Name: {person_name}")
                
                delete_id = input("Enter the ID to delete: ")
                delete_from_db(db_path, delete_id)

                print(f"Data with ID {delete_id} has been deleted from the database.")

        # Save face and register on 'c' key press
        if key == ord('c') and status == "OK":
            person_name = input("Enter the name of the person: ")
            if feature is not None:
                success, face_id = store_features_in_db_with_name(db_path, captured_face_path, person_name, feature)
                if success:
                    shutil.copy(captured_face_path, f"RegisteredFace/{face_id}_{os.path.basename(captured_face_path)}")
                    print(f"Feature stored successfully with ID {face_id}")
                else:
                    print(f"Feature already exists with ID {face_id}" if face_id else "Failed to store the feature.")

        # Quit on 'q' key press
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
