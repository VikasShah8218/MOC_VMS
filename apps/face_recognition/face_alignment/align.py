from apps.face_recognition.face_alignment import mtcnn
from PIL import Image
import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn_model = mtcnn.MTCNN(device=device, crop_size=(112, 112))

def add_padding(pil_img, top, right, bottom, left, color=(0,0,0)):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def get_aligned_face(img, rgb_pil_image=None):
    if rgb_pil_image is not None:
        if isinstance(rgb_pil_image, Image.Image):
            img = rgb_pil_image
        else:
            raise ValueError('Provided input is not a valid PIL Image.')
    elif img is not None:
        pass
    else:
        raise ValueError('Either an image path or a PIL image must be provided.')
    
    # find face
    try:
        bboxes, faces = mtcnn_model.align_multi(img, limit=1)
        face = faces[0]
    except Exception as e:
        print('Face detection Failed due to error.')
        print(e)
        face = None

    return face


