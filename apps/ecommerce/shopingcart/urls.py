from django.urls import path
from . import views


urlpatterns = [
    path("product/<str:uuid>/add-to-cart/", views.AddToCartView.as_view()),
    # path("cart/", views.CartItemView.as_view()),
    # path("cart/<int:pk>/remove/", views.CartItemView.as_view()),
]
