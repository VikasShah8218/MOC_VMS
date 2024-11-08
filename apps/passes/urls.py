from django.urls import path
from .views import *


urlpatterns = [
    path('visitor-pass-info',VisitorPassView.as_view({
            "get":"get_visitor_pass",
            "post":"post_visitor_pass"
        })),
    path('visitor-pass-info/<int:pk>', VisitorPassView.as_view({
        "put":"update_visitor_pass",
        "get":"retrive_visitor_pass",
        "delete":"delete_visitor_pass"
    })),
    path('cancel-pass/<int:id>',CancelPass.as_view()),
    path('pass-download/<int:pk>' , passDownload.as_view() , name='pass_download' ),
]