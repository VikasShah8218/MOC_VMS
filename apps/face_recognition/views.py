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
device = 'cuda' if torch.cuda.is_available() else 'cpu'
db_path = "D:/Drive-1/ESSI/MOC_VMS/apps/face_recognition/face_features.db"

class Test(APIView):
    def post(self, request):
        client = request.META.get('REMOTE_ADDR')
        return Response({"message":"this is working","ip":client})

class CheckFace(APIView):
    def post(self,request):
        base64_image = request.data["image"]
        name = request.data["name"]
        model = load_pretrained_model('ir_101', device)
        image = Image.open(io.BytesIO(base64.b64decode(base64_image))).convert('RGB')
        feature = extract_feature(model, image, None,device)
        output =  store_feature_in_db(db_path,feature, image, name, similarity_threshold=0.7, top_k=1)
        return Response({"detail":output})

