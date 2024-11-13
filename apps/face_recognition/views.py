from rest_framework.response import Response
from rest_framework.views import APIView
from apps.face_recognition.scripts.utils import store_feature_in_db,extract_feature, load_pretrained_model
from apps.face_recognition.scripts import (
    store_features_in_db,   #sotre in db    Kam Ka Function
    FACE_MODEL_PATH,  # change with req
)
from PIL import Image
import base64
import torch
import io
import numpy as np

from apps.visitor.models import VisitorFaceFeatures
import time
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cpu' if torch.cuda.is_available() else 'cpu'
db_path = "D:/Drive-1/ESSI/MOC_VMS/apps/face_recognition/face_features.db"
model = load_pretrained_model('ir_101', device)

class Test(APIView):
    def post(self, request):
        client = request.META.get('REMOTE_ADDR')
        return Response({"message":"this is working","ip":client})

class CheckFace(APIView):
    def post(self,request):
        try:
            base64_image,name = request.data["image"],request.data["name"]
            image = Image.open(io.BytesIO(base64.b64decode(base64_image))).convert('RGB')
            feature = extract_feature(model, image, None,device)
            output =  store_feature_in_db(feature,similarity_threshold=0.9)
            return Response({"detail":output})
        except Exception as e:
            return Response({"detail":str(e)})

def check_register_face(base64_image,visitor=None):
    try:
        image = Image.open(io.BytesIO(base64.b64decode(base64_image))).convert('RGB')
        feature = extract_feature(model, image, None,device)
        result,visitor =  store_feature_in_db(feature,similarity_threshold=0.9,visitor=visitor)
        if result and visitor:
            return visitor
        else:
            return None
    except Exception as e:
        print("Check_Register_Face Function Error: ",str(e))
        return None
    
def extract_face_feature(base64_image):
    image = Image.open(io.BytesIO(base64.b64decode(base64_image))).convert('RGB')
    return extract_feature(model,image,None,device)

def find_similar_face_in_db(visitor_image=None, similarity_threshold=0.9):
    matching_visitors = []
    if visitor_image:
        visitors_face_features = VisitorFaceFeatures.objects.all()
        if visitors_face_features:
            current_image_feature = np.frombuffer(extract_face_feature(visitor_image).tobytes(), dtype=np.float32)
            
            for visitor_face_feature in visitors_face_features:
                stored_feature = np.frombuffer(visitor_face_feature.feature, dtype=np.float32)
                similarity = np.dot(current_image_feature.flatten(), stored_feature) / (np.linalg.norm(current_image_feature) * np.linalg.norm(stored_feature))
                print(similarity)
                if similarity >= similarity_threshold:
                    print(f"Similar Face Detected with similarity: {visitor_face_feature.visitor.first_name}  {similarity}")
                    matching_visitors.append(visitor_face_feature.visitor)

    return matching_visitors




    
