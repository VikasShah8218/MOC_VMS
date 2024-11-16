# Standard Library Imports

# Django Imports
from django_filters.rest_framework import DjangoFilterBackend

# Third-Party Imports

from rest_framework import generics, response, status
from rest_framework.views import APIView
# Local Imports
from .filters import VisitorFilter
from .models import Visitor,VisitorFaceFeatures
from .serializers import VisitorSerializer, UpdateVisitorSerializer
from apps.accounts.mixins import CustomAuthenticationMixin
from apps.passes.models import VisitorPass
from rest_framework.response import Response
from apps.face_recognition.views import check_register_face,extract_face_feature,find_similar_face_in_db


class VisitorListCreateAPIView(generics.ListCreateAPIView, CustomAuthenticationMixin):
    serializer_class = VisitorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VisitorFilter

    def check_permissions(self, request):
        self.validate_user_type(request, allowed=['Admin', 'Receptionist'])
        return super().check_permissions(request)

    def get_queryset(self):
        return Visitor.objects.order_by('-updated_on')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['created_by'] = self.request.user
        return context

    def visitor_exists(self,gov_id_no):
        if gov_id_no:
            visitor = Visitor.objects.filter(gov_id_no=gov_id_no).first()
            if visitor:
                return VisitorSerializer(visitor).data  
        return None 

    def find_visitor_by_face(self, visitor_image,visitor=None):
        return check_register_face(base64_image=visitor_image,visitor=visitor )

    def create(self, request, *args, **kwargs):
        visitor_image = request.data.get('image')
        gov_id_no = request.data.get('gov_id_no')
        serialised_visitor = self.visitor_exists(gov_id_no)
        if serialised_visitor:
            serialised_visitor["detail"] = 'Visitor already exists'
            return Response(serialised_visitor, status=status.HTTP_409_CONFLICT)
        if visitor_image:
            feature = extract_face_feature(visitor_image).tobytes()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            visitor_instance = serializer.save()
            VisitorFaceFeatures.objects.create(visitor=visitor_instance, feature=feature)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else: return Response({"detail":"image is required"},status = 400) # field is required

class VisitorGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView, CustomAuthenticationMixin):
    lookup_field = "id"
    queryset = Visitor.objects
    serializer_class = UpdateVisitorSerializer

    def check_permissions(self, request):
        self.validate_user_type(request, allowed=['Admin', 'Receptionist','Guard'])
        return super().check_permissions(request)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['updated_by'] = self.request.user
        return context

class VisitorBlackListAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return response.Response({"detail": "No id was provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            visitor = Visitor.objects.get(id=kwargs['id'])
            visitor.is_blacklisted = True
            visitor.updated_by = request.user
            try:visitor.other = request.data["other"] 
            except Exception as e:print(e)
            visitor.save(update_fields=['is_blacklisted', 'updated_by','other'])
            passes = VisitorPass.objects.filter(visitor=visitor, is_cancelled=False)
            if passes is None : pass
            else: passes.update(is_cancelled=True)
            return response.Response(status=status.HTTP_200_OK)
        except Visitor.DoesNotExist:
            return response.Response({'detail': 'Visitor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class VisitorWhitelistAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return response.Response({"message": "No id was provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            visitor = Visitor.objects.get(id=kwargs['id'])
            visitor.is_blacklisted = False
            visitor.updated_by = request.user
            try:visitor.other = request.data["other"] 
            except Exception as e:print(e)
            visitor.save(update_fields=['is_blacklisted', 'updated_by','other'])
            return response.Response(status=status.HTTP_200_OK)
        except Visitor.DoesNotExist:
            return response.Response({'message': 'Visitor does not exist'}, status=status.HTTP_404_NOT_FOUND)

class DeletedVisitors(APIView):
    def get(self,request):
        visitors = Visitor.objects.filter(is_deleted = True)
        return Response(VisitorSerializer(visitors,many=True).data,status=200) if visitors else Response({"detail":"Visitors not Found"},status=404)

class FindVisitorByFace(APIView):
    def post(self, request):
        visitor_image = request.data.get('image')
        if not visitor_image:
            return Response({"detail": "Image is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        matching_visitors = find_similar_face_in_db(visitor_image,similarity_threshold=0.47)
        
        # Serialize the list of matching visitors
        serializer = VisitorSerializer(matching_visitors, many=True)
        
        # Manually construct paginated response structure
        response_data = {
            "count": len(matching_visitors),
            "next": None,  # No pagination in this case
            "previous": None,
            "results": serializer.data
        }
        
        # Return the structured data
        return Response(response_data, status=status.HTTP_200_OK)
