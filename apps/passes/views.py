# Standard Library Imports
import datetime
from collections import defaultdict

# Third-Party Imports
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

import time
import random
# Django Imports
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

# Local Imports
from .models import VisitorPass
from .serializers import VisitorPassSerializer, VisitorPassOverwriteSerializer
from apps.accounts.mixins import CustomAuthenticationMixin
from apps.accounts.models import User
from apps.accounts.services import TokenService, validation
from apps.visitor.models import Visitor
from apps.visitor.serializers import VisitorSerializer

from apps.passes.serializers import TblVisitorVisitDateSerializer 
from .utilities import generate_pdf_from_html ,generate_qr_base64




class VisitorPassView(viewsets.ViewSet):
    def get_visitor_pass(self, request):
        try:
            visitorPass=VisitorPass.objects.all().order_by("-updated_on")
            if request.GET.get('visitor_first_name') or request.GET.get('visitor_last_name') or request.GET.get('visiting_department'):
                query_params = defaultdict(str)
                if request.GET.get('visitor_first_name'):
                    query_params['visitor__first_name__icontains'] = request.GET.get('visitor_first_name')
                if request.GET.get('visitor_last_name'):
                    query_params['visitor__last_name__icontains'] = request.GET.get('visitor_last_name')
                if request.GET.get('visiting_department'):
                    query_params['visiting_department'] = request.GET.get('visiting_department')
                if request.GET.get('created_on'):
                    created_on = datetime.datetime.strptime(request.GET['created_on'], '%Y-%m-%d')
                    query_params['created_on__gte'] = datetime.datetime.combine(created_on, datetime.time.min)
                    query_params['created_on__lte'] = datetime.datetime.combine(created_on, datetime.time.max)
                visitorPass = visitorPass.filter(**query_params)
            if request.GET.get('limit') and request.GET.get('offset'):
                visitorPass = visitorPass[int(request.GET['offset']): int(request.GET['offset'])+int(request.GET['limit'])]
            serializer=VisitorPassSerializer(visitorPass, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def post_visitor_pass(self, request):
        serializer = VisitorPassSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = TokenService.decode_token(request.headers["Authorization"].split()[1])
                user = User.objects.get(id=data["user_id"])
                visitor = Visitor.objects.get(id=request.data.get("visitor", ""))
                if visitor.is_blacklisted:
                    return Response({"detail":"Visitor is Blacklisted"},status=400)
                elif visitor.is_deleted:
                    return Response({"detail":"Visitor is Deleted"})
               
                serializer.validated_data["created_by_id"] = user.id
                serializer.validated_data["visitor_id"] = visitor.id
                data = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Visitor.DoesNotExist:
                return Response({"detail": "Visitor not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


    def update_visitor_pass(self, request, pk=None):
        try:
            visitorPass = VisitorPass.objects.get(id=pk)
            user = request.user
            serializer = VisitorPassSerializer(instance=visitorPass, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data["updated_by"] = user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except VisitorPass.DoesNotExist:
            return Response({'message': 'VisitorPass does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrive_visitor_pass(self, request, pk=None):
        try:
            visitorPass = VisitorPass.objects.get(id=pk)
            serializer = VisitorPassSerializer(visitorPass)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VisitorPass.DoesNotExist:
                    return Response({"message": "VisitorPass not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def delete_visitor_pass(self, request, pk=None):
        try:
            visitorPass = VisitorPass.objects.get(pass_id=pk)
            visitorPass.delete()
            return Response({"message":"VisitorPass deleted successfully"}, status=200)
        except VisitorPass.DoesNotExist:
            return Response({'message': 'VisitorPass does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CancelPass(APIView):
    def put(self, request,id):
        try:
            pas = VisitorPass.objects.get(id=id)
            pas.is_cancelled = True
            pas.save()
            seriliser = VisitorPassSerializer(pas)
            return Response(seriliser.data,status=200)
        except VisitorPass.DoesNotExist:
            return Response({"error":"pass not found"})

class passDownload(APIView):
    def post(self, request,pk=None):
        try:
            visitor_pass = VisitorPass.objects.get(id=pk)
            serializer = VisitorPassSerializer(visitor_pass)
        except VisitorPass.DoesNotExist:
            return Response({"detail": "Pass Not Found"}, status=500)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
        
        base64 = generate_qr_base64(visitor_pass.pass_number)
        perms = {
            "loged_in_user":f'{request.user.first_name} {request.user.last_name}',
            "barcode":base64,
            "data":serializer.data,
            }
        try:  
            response = HttpResponse(generate_pdf_from_html(perms,"pass"), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Visitor_Pass.pdf"'
        except IOError:
            response = Response({"detail":"File not exist"})
        return response
    

