from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.color import ColorView
from .views.user import RegisterView, MyTokenObtainPairView

router = DefaultRouter()
router.register('colors', ColorView, basename='color')


# jwt token django
"""
from rest_framework_simplejwt import views as jwt_views

path('api/token/', jwt_views.TokenObtainPairView.as_view(),name='token_obtain_pair'),
path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
"""


urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view(), name='register'),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

