from django.urls import path, include
from . import views
from .customer_handler.customer_request import *


urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('order-update/', order_update, name="order-update"),
    path('order-validation/', order_validation, name="order-validation"),
    path('<slug:selected_category>/', views.store, name="category"),
]