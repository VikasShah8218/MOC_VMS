from .serializers import AdamLinkedwithCreateSerializer ,AdamLinkedwithReadSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AdamSerializer
from apps.accounts.models import User
from django.core.cache import cache
from .models import AdamLinkedwith
from rest_framework import status
from .models import Adam


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
        


class AdamLinkedwithView(APIView):
    def get(self, request):
        try:
            data = AdamLinkedwith.objects.all().order_by("-id")
            serializer = AdamLinkedwithReadSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        adam_id,client_ip = request.data.get("adam"),request.data.get("client_ip")

        if not Adam.objects.filter(id=adam_id).exists():
            return Response({"detail": "Adam does not exist."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if AdamLinkedwith.objects.filter(adam_id=adam_id).exists():
            return Response({"detail": "Adam is Linked With another IP "}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if AdamLinkedwith.objects.filter(client_ip=client_ip).exists():
            return Response({"detail": "Client IP already exists in another record."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer = AdamLinkedwithCreateSerializer(data=request.data)
        if serializer.is_valid():
            adam_obj = serializer.save()
            serializer = AdamLinkedwithReadSerializer(adam_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        try:
            adam_linked = AdamLinkedwith.objects.get(id=id)
            serializer = AdamLinkedwithCreateSerializer(adam_linked, data=request.data)
            serializer.is_valid(raise_exception=True)
            adam_obj = serializer.save()
            serializer = AdamLinkedwithReadSerializer(adam_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AdamLinkedwith.DoesNotExist:
            return Response({'detail': 'AdamLinkedwith does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            adam_linked = AdamLinkedwith.objects.get(id=id)
            adam_linked.delete()
            return Response({"detail": "AdamLinkedwith deleted successfully"}, status=status.HTTP_200_OK)
        except AdamLinkedwith.DoesNotExist:
            return Response({'detail': 'AdamLinkedwith does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class AdamLinkedwithView(APIView):
#     def get(self, request):
#         try:
#             data = AdamLinkedwith.objects.all().order_by("-id")
#             serializer = AdamLinkedwithSerializer(data, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request):
#         # Convert adam ID to integer if it's provided as a string
#         if 'adam' in request.data and isinstance(request.data['adam'], str):
#             try:
#                 request.data['adam'] = int(request.data['adam'])
#             except ValueError:
#                 return Response({"error": "Invalid adam ID format"}, status=status.HTTP_400_BAD_REQUEST)
        
#         serializer = AdamLinkedwithSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

#     def put(self, request, id):
#         try:
#             adam_linked = AdamLinkedwith.objects.get(id=id)
            
#             # Convert adam ID to integer if it's provided as a string
#             if 'adam' in request.data and isinstance(request.data['adam'], str):
#                 try:
#                     request.data['adam'] = int(request.data['adam'])
#                 except ValueError:
#                     return Response({"error": "Invalid adam ID format"}, status=status.HTTP_400_BAD_REQUEST)

#             serializer = AdamLinkedwithSerializer(instance=adam_linked, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except AdamLinkedwith.DoesNotExist:
#             return Response({'detail': 'AdamLinkedwith does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def delete(self, request, id):
#         try:
#             adam_linked = AdamLinkedwith.objects.get(id=id)
#             adam_linked.delete()
#             return Response({"detail": "AdamLinkedwith deleted successfully"}, status=status.HTTP_200_OK)
#         except AdamLinkedwith.DoesNotExist:
#             return Response({'detail': 'AdamLinkedwith does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
