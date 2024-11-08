# Django Imports
from django.urls import path

# Local Imports
from . import views
from .views import *


urlpatterns = [
    path('test/',Test.as_view()),
    path('test-01/',Test_01.as_view()),
    # path('register-adam/',ResgisterAdam.as_view()),
    # path('register-reader/',ResgisterReader.as_view()),
    # path('update-reader/<int:id>',UpdateReader.as_view()),
    # path('get-adam/',GetAdam.as_view()),
    # path('update-adam/<int:id>',UpdateAdam.as_view()),
    # path('delete-reader/<int:id>',DeleteReader.as_view()),
    # path('map-reader-guard/<int:id>',MapReader.as_view()),
    # path('map-reader-guard/',MapReader.as_view()),
    path('adam/', AdamView.as_view()),               
    path('adam/<int:id>/', AdamView.as_view()), 
]