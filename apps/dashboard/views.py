from rest_framework.response import Response
from rest_framework.views import APIView
# Standard Library Imports

# Django Imports
from django.shortcuts import render
from django.utils import timezone

# Third-Party Imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

# Local Imports
from apps.accounts.models import User
from apps.accounts.services import TokenService, validation
from datetime import timedelta,datetime
from apps.passes.models import VisitorPass
from apps.passes.serializers import VisitorPassSerializer
from datetime import date
from django.core.cache import cache


time_out = 10


class Test(APIView):
    def post(self, request):
        return Response({"detail":"Working, Client IP : "+request.META.get('REMOTE_ADDR')})


class WeeklyVisitorsVisitDashboard(APIView):
    def get(self,request):
        data = {}
        cash_data = cache.get('Weekly_visitors_visit')
        if cash_data != None:
            return Response(cash_data)
        try:
            for i in range(1,8):
                start_date = str(date.today() - timedelta(days=i))+" 00:00:00"
                end_date = str(date.today() - timedelta(days=i))+" 23:59:59"
                filtered = len(VisitorPass.objects.filter(created_on__gte = start_date,created_on__lt = end_date))  
                data[str(date.today() - timedelta(days=i))] = filtered  
            cache.set('Weekly_visitors_visit',data,timeout=time_out)
            return Response(data)
        except:
            return Response({"error":"internal server error"},status=500)      
        
class TodayTimeVsVisitorGraphDashboard(APIView):
    def get(self,request):
        cash_data = cache.get('TodayTimeVsVisitorGraphDashboard')
        if cash_data != None:
            return Response(cash_data)
        try:
            today = datetime.now().date()
            start_time = datetime.combine(today, datetime.min.time()) + timedelta(hours=9)
            end_time = datetime.combine(today, datetime.min.time()) + timedelta(hours=18)
            current_time = start_time
            time_dict = {}
            data = {}
            while current_time <= end_time:
                key = current_time.strftime('%Y-%m-%d %H:%M:%S')
                next_time = current_time + timedelta(minutes=30)
                value = next_time.strftime('%Y-%m-%d %H:%M:%S')
                time_dict[key] = value
                current_time += timedelta(minutes=30)
            for start,end in time_dict.items():
                filtered = len(VisitorPass.objects.filter(created_on__gte = start,created_on__lt = end))
                data[start] =filtered
            cache.set('TodayTimeVsVisitorGraphDashboard',data,timeout=time_out)
            return Response(data)
        except:
            return Response({"error":"internal server Error"},status=500)
        
        
class VisitorPassTimeLeft(APIView):
    def get(self,request):
        cash_data = cache.get('VisitorPassTimeLeft')
        if cash_data != None:
            return Response(cash_data)
        try:
            start_date = str(date.today())+" 00:00:00"
            end_date = str(date.today())+" 23:59:59"
            filtered = VisitorPass.objects.filter(created_on__gte = start_date,created_on__lt = end_date,is_cancelled = False).order_by("-created_on")
            send_data = []
            for i in filtered:
                data= {}
                data["visitor_name"] = i.visitor.first_name
                data["visitor_image"] = i.visitor.image
                data["valid_upto"] = i.valid_until
                data["pass_created_at"] = i.created_on
                data["phone"] = i.visitor.phone
                data["gov_id_type"] = i.visitor.gov_id_type
                data["gov_id_no"] = i.visitor.gov_id_no
                data["phone"] = i.visitor.phone
                data["id"] = i.visitor.id
                send_data.append(data)
            cache.set('VisitorPassTimeLeft',send_data,timeout=time_out)
            return Response(send_data)
        except Exception as e :
            return Response({"error":"internal server Error"},status=500)