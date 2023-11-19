from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .controllers.categories import CategoryView, CategoryDetailView


router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryView.as_view(), name='Create_list_category'),
    path(
        'categories/<slug:slug>/',
        CategoryDetailView.as_view(),
        name='detail_category'
    ),
]

