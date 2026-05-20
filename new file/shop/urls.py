from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("login/", views.ShopLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("api/products/", views.api_products, name="api_products"),
    path("api/orders/", views.api_orders, name="api_orders"),
    path("api/cart/add/", views.api_cart_add, name="api_cart_add"),
    path("api/cart/update/", views.api_cart_update, name="api_cart_update"),
    path("api/cart/remove/", views.api_cart_remove, name="api_cart_remove"),
]
