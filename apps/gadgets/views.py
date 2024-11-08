# Django Imports
from django.utils import timezone

# Third-Party Imports
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.permissions import AllowAny



# Local Imports
from apps.accounts.models import User
from apps.accounts.services import TokenService, validation
from .serializers import AdamSerializer
from .models import Adam
from rest_framework import status


# testing Redis operations 
cache.set('my_key', 'This is the value chote', timeout=10)

class Test(APIView):
    def post(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        print(client_ip)
        return Response({"message": "working", "client_ip": str(client_ip)}, status=200)

        
class Test_01(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        value = cache.get('my_key')
        return Response({"yeee":f"working --> {value}"},status=200)


class AdamView(APIView):
    def get(self, request):
        try:
            data = Adam.objects.all().order_by("-id")
            serializer = AdamSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        serializer = AdamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        try:
            adam = Adam.objects.get(id=id)
            serializer = AdamSerializer(instance=adam, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Adam.DoesNotExist:
            return Response({'detail': 'Adam does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            adam = Adam.objects.get(id=id)
            adam.delete()
            return Response({"detail": "Adam deleted successfully"}, status=status.HTTP_200_OK)
        except Adam.DoesNotExist:
            return Response({'detail': 'Adam does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)