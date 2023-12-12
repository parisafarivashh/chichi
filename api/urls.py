from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .controllers.categories import CategoryView, CategoryDetailView
from .controllers.products import ProductView, ProductDetailView
from .controllers.vote import VoteView


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
    path('products/<int:product_id>/votes', VoteView.as_view()),
    path('products/<int:product_id>/votes/<int:id>', VoteView.as_view()),
]

