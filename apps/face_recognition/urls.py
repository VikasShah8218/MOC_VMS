from django.urls import path
from .views import *

urlpatterns = [
    path('test/', Test.as_view()),
    path('check-face-test/', CheckFace.as_view()),
]