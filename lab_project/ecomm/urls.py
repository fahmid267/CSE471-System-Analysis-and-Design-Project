from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    # path('product_category/<str:category>/', views.product_from_cat, name = "product_from_cat"),
    path('reviews/<int:product_id>/', views.reviews, name = "reviews"),
    path('products/type/<str:type>/<str:category>/', views.products_by_type, name='products_by_type'),
    path('products/<str:type>/<str:category>/<str:name>/', views.products_by_type, name='products_by_type_with_name')
]