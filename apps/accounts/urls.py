from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('test/', Test.as_view()),
    path('login/', LoginUser.as_view()),    
    path('logout/', LogoutView.as_view()),
    path('create-admin/', RegisterAdmin.as_view({'post': 'create'})),
    path('create-users/', CreateUserByAdmin.as_view({'post': 'create'})),
    path('get-all-user/',GetAllUsersByAdmin.as_view({'get': 'list'})),
    path('update-user/<int:id>/', UpdateUserDetailsByAdmin.as_view()),
    path('reset-password-by-user/', ResetPasswordByUser.as_view()),
    path('reset-password-by-admin/<int:id>/', ResetPasswordByAdmin.as_view()),
]