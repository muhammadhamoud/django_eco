from rest_framework import serializers
from .models import CartItem
# from ecommerce.store.models import ProductPrice, Product


# class CartProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = (
#             "title",
#             "seller",
#             "quantity",
#             "price",
#             "image",
#         )

class CartItemSerializer(serializers.ModelSerializer):
    # product = CartProductSerializer(required=False)
    class Meta:
        model = CartItem
        fields = "__all__"



