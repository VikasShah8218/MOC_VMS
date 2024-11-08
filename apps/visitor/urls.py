from django.urls import path
from .views import *
from .access import *

urlpatterns = [
    path('visitor-info', VisitorListCreateAPIView.as_view()),
    path('visitor-info/<int:id>', VisitorGetUpdateDestroyAPIView.as_view()),
    path('blacklist/<int:id>', VisitorBlackListAPIView.as_view()),
    path('whitelist/<int:id>', VisitorWhitelistAPIView.as_view()),
    path('access-gate', Access.as_view()),
]
