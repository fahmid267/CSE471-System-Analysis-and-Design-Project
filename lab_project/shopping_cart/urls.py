from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<int:product_id>', views.add_to_cart, name = "add_to_cart"), 
    path('view_cart', views.view_cart, name = "view_cart"),
    path('update_cart/<int:item_id>', views.update_cart, name = "update_cart"),
    path('purchase_completed/', views.purchase_completed, name='purchase_completed'),
    path('download_invoice/', views.download_invoice, name='download_invoice'),
    path('download_invoice_file/', views.download_invoice_file, name='download_invoice_file')
]