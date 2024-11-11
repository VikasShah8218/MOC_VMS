from facetools import FaceValidationSystem
import cv2

if __name__ == "__main__":
    face_model_path = "C:/Users/essi-01/OneDrive/Desktop/New folder/AdaFace/wrap-up-frs/backend/model/final_faceDet_model.pt"

    cap = cv2.VideoCapture(0)
    
    detector = FaceValidationSystem(face_model_path, ear_threshold=0.25, roi_padding=50)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        status = detector.check_face(frame)
        
        height, width, _ = frame.shape

        square_size = min(width, height) - 2 * detector.roi_padding
        roi_x = (width - square_size) // 2  
        roi_y = (height - square_size) // 2 
        if status == "OK":
            roi_color = (0, 255, 0) 
        else:
            roi_color = (0, 0, 255)  

        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + square_size, roi_y + square_size), roi_color, 2)
   
        cv2.putText(frame, f'Status: {status}', (30, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, roi_color, 2)
        cv2.imshow('Face Validation System', frame)

    
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
