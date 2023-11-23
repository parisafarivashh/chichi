from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Category
from .views.category import CategoryView, CategoryDetailView
from .views.color import ColorView

router = DefaultRouter()
router.register('colors', ColorView, basename='color')


urlpatterns = [
    path('', include(router.urls)),

    path('categories/', CategoryView.as_view(), name='Create_list_category'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='detail_category')
]

