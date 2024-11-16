from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('test/', Test.as_view()),
    path('weekly-visitor-visit/',WeeklyVisitorsVisitDashboard.as_view()),
    path('today-visitor-visit/',TodayTimeVsVisitorGraphDashboard.as_view()),
    path('pass-time-left/',VisitorPassTimeLeft.as_view()),
]