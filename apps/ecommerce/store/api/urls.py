from django.urls import path, include
from . import views
# from . import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r"categories", views.CategoryAdmin, basename='category')
# router.register(r"product-lists", views.ListProductView)
# router.register(r"product-search", viewsets.ProductSearchView)

app_name = "store"

urlpatterns = [
    path("api/", include(router.urls)),

    path("category/", views.CategoryList.as_view(), name='categories'),
    path("category/<str:id>/", views.CategoryAPIView.as_view(), name='category_view'),
    path('category/<str:id>/', views.CategoryAdmin.as_view(), name='category'),

    path("product/", views.ProductList.as_view(), name='products'),
    path("product/create", views.ProductCreateView.as_view(), name='create-product'),
    path("product/<str:id>/", views.ProductAdmin.as_view(), name='product'),
    path("product/<str:id>/create-price/", views.ProductPriceCreateView.as_view(), name='update-product-price'),

    path('product/<str:id>/reviews/create', views.ProductReviewCreateView.as_view(), name='create_product_review'),
    # path('product/<str:pk>/reviews/', views.ProductReviewListView.as_view(), name='product_reviews'),

    path("product/<str:id>/add-to-cart/", views.AddToCartView.as_view()),
    path('orders/<str:id>/', views.OrderDetailView.as_view(), name='order-detail'),

    path("product/<str:id>/reservation/", views.ReservationView.as_view(), name='reservation'),

    # path("product/category/", views.ProductListByCategory.as_view(), name='product-category'),

    # path("api/product-list/", views.ListProductAPIView.as_view()),
    # # path("serpy/product/", views.SerpyListProductAPIView.as_view()),
    # path("api/list-product/user/", views.ListUserProductAPIView.as_view()),
    # path("api/create/product/", views.CreateProductAPIView.as_view()),
    # path("api/product/<int:pk>/delete/", views.DestroyProductAPIView.as_view()),
    # path("api/product/<str:uuid>/", views.ProductDetailView.as_view()),
    # path("api/products/views/", views.ProductViewsAPIView.as_view()),
    
    # # Try requests lib and microservices here. #
    # path("micro/", views.ListMicroServiceView.as_view()),
    # path("micro/create/", views.MicroServiceCreateView.as_view()),
    # path("get/", views.GETRequests.as_view()),
    # path("post/", views.POSTRequests.as_view()),
]

# urlpatterns += [
#     path('search/', include('haystack.urls')),
# ]