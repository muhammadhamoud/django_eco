from django.urls import path, include
from .views import *

app_name = "store"

urlpatterns = [
    path("shop/", ProductListView.as_view(), name="product_list"),
    path("shop/<slug:category_slug>/", ProductListByCategoryView.as_view(), name="product_list_by_category"),
    path("shop/<int:pk>/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),

]