from django.urls import path

from .views import RegisterView, MyTokenObtainPairView


# jwt token django
"""
from rest_framework_simplejwt import views as jwt_views

path('api/token/', jwt_views.TokenObtainPairView.as_view(),name='token_obtain_pair'),
path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
"""


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

