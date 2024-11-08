# Standard Library Imports

# Django Imports
from django_filters.rest_framework import DjangoFilterBackend

# Third-Party Imports
from rest_framework import generics, views, response, status

# Local Imports
from .filters import VisitorFilter
from .models import Visitor
from .serializers import VisitorSerializer, UpdateVisitorSerializer
from apps.accounts.mixins import CustomAuthenticationMixin
from apps.passes.models import VisitorPass

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

class VisitorGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView, CustomAuthenticationMixin):
    lookup_field = "id"
    queryset = Visitor.objects
    serializer_class = UpdateVisitorSerializer

    def check_permissions(self, request):
        self.validate_user_type(request, allowed=['Admin', 'Receptionist'])
        return super().check_permissions(request)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['updated_by'] = self.request.user
        return context

class VisitorBlackListAPIView(views.APIView):
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
        
class VisitorWhitelistAPIView(views.APIView):
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


