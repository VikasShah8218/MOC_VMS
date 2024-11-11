from PIL import ImageDraw


def show_bboxes(img, bounding_boxes, facial_landmarks=[]):
    """Draw bounding boxes and facial landmarks.

    Arguments:
        img: an instance of PIL.Image.
        bounding_boxes: a float numpy array of shape [n, 5].
        facial_landmarks: a float numpy array of shape [n, 10].

    Returns:
        an instance of PIL.Image.
    """

    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy)

    for b in bounding_boxes:
        draw.rectangle([
            (b[0], b[1]), (b[2], b[3])
        ], outline='white')

    # PNET model facial_landmarks
    # for p in facial_landmarks:
    #     for i in range(5):
    #         draw.ellipse([
    #             (p[i] - 1.0, p[i + 5] - 1.0),
    #             (p[i] + 1.0, p[i + 5] + 1.0)
    #         ], outline='blue')

    #Mediapipe model facial_landmarks
    for landmarks in facial_landmarks:
        x_coords = landmarks[:len(landmarks)//2]
        y_coords = landmarks[len(landmarks)//2:]
        
        for (x, y) in zip(x_coords, y_coords):
            draw.ellipse([
                (x - 2.0, y - 2.0),
                (x + 2.0, y + 2.0)
            ], outline='blue', fill='blue')

    return img_copy
