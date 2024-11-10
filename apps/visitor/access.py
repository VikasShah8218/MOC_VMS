from apps.gadgets.models import AdamLinkedwith
from rest_framework.response import Response
from apps.passes.models import VisitorPass
from rest_framework.views import APIView
from apps.gadgets.adam import activate
from django.utils import timezone


class Access(APIView):
    def post(self,request):
        try:
            adam_data,visitor_pass = AdamLinkedwith.objects.get(client_ip=request.META.get('REMOTE_ADDR')), VisitorPass.objects.get(pass_number = request.data["pass_number"])
            print(visitor_pass.valid_until>=timezone.now() ,(not visitor_pass.is_cancelled), (not visitor_pass.visitor.is_blacklisted), (not visitor_pass.visitor.is_deleted))
            if (visitor_pass.valid_until>=timezone.now()) and (not visitor_pass.is_cancelled) and (not visitor_pass.visitor.is_blacklisted) and ( not visitor_pass.visitor.is_deleted):
                return Response({"detail":"Gate Opened"},status=200) if(activate(adam_data.adam.ip,adam_data.adam.actuation_port)) else Response({"detail":"Something went wrong Adam device"},status=500)
            else:return Response({"detail":"Access Denied"},status=403)
        except Exception as e:return Response({"detail":str(e)},status=500)
