import cv2
import mediapipe as mp
import math
from apps.face_recognition.scripts.facetools import FaceDetector

class FaceValidationSystem:
    def __init__(self, face_model_path, device, ear_threshold=0.15, roi_padding=50):
        self.ear_threshold = ear_threshold
        self.roi_padding = roi_padding
        self.mp_face_mesh = mp.solutions.face_mesh
        
        self.face_detector = FaceDetector(face_model_path, device)  
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.9,
            min_tracking_confidence=0.9
        )

    def euclidean_distance(self, pt1, pt2):
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def calculate_ear(self, landmarks, eye_points):
        A = self.euclidean_distance(landmarks[eye_points[1]], landmarks[eye_points[5]])
        B = self.euclidean_distance(landmarks[eye_points[2]], landmarks[eye_points[4]])
        C = self.euclidean_distance(landmarks[eye_points[0]], landmarks[eye_points[3]])
        ear = (A + B) / (2.0 * C)
        return ear

    def check_face(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        
        face_bboxes = self.face_detector.detect_faces(frame, conf_threshold=0.7)
        if not face_bboxes:
            return "No face detected", None
        if len(face_bboxes) > 1:
            return "Please remove the rest", None
        
        x1, y1, x2, y2 = face_bboxes[0]
        w, h = x2 - x1, y2 - y1
        
        square_size = min(width, height) - 2 * self.roi_padding
        roi_x = (width - square_size) // 2  
        roi_y = (height - square_size) // 2 

        if x1 < roi_x or y1 < roi_y or x2 > roi_x + square_size or y2 > roi_y + square_size:
            return "Move your face to the center of the box", None
        
        if w < square_size * 0.4 or h < square_size * 0.4:
            return "Come closer to the camera", None
        if w > square_size * 0.9 or h > square_size * 0.9:
            return "Move back slightly", None

        mesh_result = self.face_mesh.process(rgb_frame)

        if not mesh_result.multi_face_landmarks:
            return "Face not detected", None
        
        landmarks = [(int(pt.x * width), int(pt.y * height)) for pt in mesh_result.multi_face_landmarks[0].landmark]
        left_ear = self.calculate_ear(landmarks, self.LEFT_EYE)
        right_ear = self.calculate_ear(landmarks, self.RIGHT_EYE)
        avg_ear = (left_ear + right_ear) / 2.0
        
        if avg_ear < self.ear_threshold:
            return "Keep your eyes open ", avg_ear

        return "OK", avg_ear