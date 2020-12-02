from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('order-update/', views.order_update, name="order-update"),
    path('order-validation/', views.order_validation, name="order-validation"),
    path('product-category/', views.get_product_category, name="product-category"),
]