from django.urls import path, include
from . import views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'carts', views.CartViewSet)
# cart_router = DefaultRouter()
# cart_router.register(r'items', views.CartItemViewSet, basename='cart-items')

# # router.register(r'n_profiles', views.ProfileViewSet)
# # router.register(r'orders', views.OrderViewSet, basename='orders')
# # router.register(r'products', views.ProductsViewSet)
# # router.register(r'categories', views.CategoryViewSet)

# # product_router = DefaultRouter()
# # product_router.register(r'reviews', views.ReviewViewSet, basename='product-reviews')
# # path('products/<uuid:product>/reviews/', include(product_router.urls)),


urlpatterns = [
    # path('', include(router.urls)),
    # path('', include(cart_router.urls)),
    path('cart/', views.CartAPI.as_view(), name='cart'),

]