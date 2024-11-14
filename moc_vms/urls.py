from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

jwt_token_url_patterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/' , include(('apps.accounts.urls'))),
    path('visitor/' , include(('apps.visitor.urls'))),
    path('gadgets/' , include(('apps.gadgets.urls'))),
    path('passes/' , include(('apps.passes.urls'))),
    path('face_recognition/' , include(('apps.face_recognition.urls'))),
    path('reports/' , include(('apps.reports.urls'))),
    

]+jwt_token_url_patterns
