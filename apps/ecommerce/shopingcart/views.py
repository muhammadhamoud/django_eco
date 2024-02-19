from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Product, ProductPrice
from .models import CartItem
from .serializers import CartItemSerializer

# Create your views here.

class AddToCartView(APIView):

    def post(self, request, uuid):
        product = Product.objects.get(uuid=uuid)
        productprice = ProductPrice.objects.get(product)
        print(productprice)

        # try:
        #     product = Product.objects.get(uuid=uuid)
        # except ProductPrice.DoesNotExist:
        #     return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        shopping_cart, created = CartItem.objects.get_or_create(user=request.user)
        shopping_cart.items.add(productprice)
        serializer = CartItemSerializer(shopping_cart)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)