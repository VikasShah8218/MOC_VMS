# Django Imports
from django.urls import path

# Local Imports
from . import views
from .views import *


urlpatterns = [
    path('test/',Test.as_view()),
    path('test-01/',Test_01.as_view()),
    path('adam/', AdamView.as_view()),               
    path('adam/<int:id>/', AdamView.as_view()), 
    path('adam-linkedwith/', AdamLinkedwithView.as_view()),             
    path('adam-linkedwith/<int:id>/', AdamLinkedwithView.as_view()), 
]