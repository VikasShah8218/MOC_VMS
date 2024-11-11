from apps.face_recognition.scripts.utils import store_feature_in_db, extract_feature, load_pretrained_model
from PIL import Image
import base64
import io

def store_features_in_db(db_path, base64_image, person_name, device, top_k=1, similarity_threshold=0.7):
    model = load_pretrained_model('ir_101', device)
    pil_image = Image.open(io.BytesIO(base64.b64decode(base64_image))).convert('RGB')
    feature = extract_feature(model, pil_image, device=device)
    return store_feature_in_db(db_path, feature, pil_image, person_name, similarity_threshold, top_k)