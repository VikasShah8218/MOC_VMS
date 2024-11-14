from rest_framework.views import APIView
from rest_framework.response import Response
from .utilities import generate_pdf_from_html,list_of_dicts_to_excel
from apps.visitor.serializers import VisitorSerializer,Visitor
from django.http import HttpResponse
from apps.passes.serializers import VisitorPassSerializer,VisitorPass


class Test(APIView):
    def post(self,request):
        return Response({"detail":'Good Working'},status=200)




class VisitorReport(APIView):
    def get(self,request):
        try:
            start_date ,end_date= request.GET["start_date"],request.GET["end_date"]
            try: download = True if (request.GET["download"]).lower() == "true" else False
            except: download = False
            try:
                search_field,search_value = request.GET["field"],request.GET["value"]
                print("*"*100)
                print(search_field)
                print(search_value)
                print("*"*100)

                field_array = ["is_blacklisted","is_key_active","visitor_type","created_by_id"]
                if search_field in field_array:is_field = True
                else:
                    is_field = False
                    return Response({"detail":f"choose write field {field_array}"})
            except:
                is_field = False
        except:
            return Response({"detail":"Provide required fields: start_date end_date and optional field: field value"})
        
        if is_field:
            filter_args = {search_field: search_value}
            try:visitors = Visitor.objects.filter(**filter_args,created_on__gte = start_date,created_on__lt= end_date)
            except:return Response({"detail":"Unprocessable Data"})
        else:
            try:visitors = Visitor.objects.filter(created_on__gte = start_date,created_on__lt= end_date)
            except:return Response({"detail":"Unprocessable Data"})
                
        serializer = VisitorSerializer(visitors,many = True)
        if download:
            perms = {
            "name":request.user.username,
            "type":"visitor Report",
            "start_date":start_date,
            "end_date":end_date,
            }

            try:  
                response = HttpResponse(generate_pdf_from_html(request,serializer.data,perms,"visitor"), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="Visitor_Report.pdf"'
            except IOError:
                response = Response({"detail":"File not exist"})
            return response
        else:
            return Response(serializer.data,status=200)

class PassReport(APIView):
    def get(self,request):
        try:
            start_date,end_date = request.GET["start_date"],request.GET["end_date"]
            try: download = True if (request.GET["download"]).lower() == "true" else False
            except: download = False
        except:return Response({"detail":"Provide required fields: start_date , end_date"})

        try:visitor_pass = VisitorPass.objects.filter(created_on__gte = start_date,created_on__lt= end_date).order_by("-id")
        except:return Response({"detail":"Unprocessable Data"})

        serializer = VisitorPassSerializer(visitor_pass,many = True)
        if download:
            perms = {
            "name":request.user.username,
            "type":"Pass Report",
            "start_date":start_date,
            "end_date":end_date,
            }
            try:  
                response = HttpResponse(generate_pdf_from_html(request,serializer.data,perms,"pass_report"), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="Pass_Report.pdf"'
            except IOError:
                response = Response({"detail":"File not exist"})
            return response
        else:
            return Response(serializer.data,status=200)
      