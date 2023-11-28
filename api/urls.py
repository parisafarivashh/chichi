from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .controllers.categories import CategoryView, CategoryDetailView
from .controllers.products import ProductView, ProductDetailView


router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryView.as_view(), name='create_list_category'),
    path(
        'categories/<slug:slug>/',
        CategoryDetailView.as_view(),
        name='detail_category'
    ),
    path('products/', ProductView.as_view(), name='create_list_product'),
    path(
        'products/<int:id>/',
        ProductDetailView.as_view(),
        name='detail_product',
    ),
]

