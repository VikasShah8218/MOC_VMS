from django.urls import path
from .views import *


urlpatterns = [
    path('test' , Test.as_view()),
    path('visitor',VisitorReport.as_view()),
    path('pass',PassReport.as_view()),
]