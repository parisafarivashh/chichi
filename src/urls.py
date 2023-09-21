from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.color import ColorView


router = DefaultRouter()
router.register('colors', ColorView, basename='color')


urlpatterns = [
    path('', include(router.urls)),
]

