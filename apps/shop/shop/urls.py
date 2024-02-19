from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("shop/", views.product_list, name="product_list"),
    path(
        "shop/<slug:category_slug>/",
        views.product_list,
        name="product_list_by_category",
    ),
    path("shop/<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
]