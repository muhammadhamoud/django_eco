from django.shortcuts import render
from django.utils import timezone
import logging
import json
import requests

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework import filters
from rest_framework import viewsets
from django_filters import NumberFilter

from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from core.ecommerce_permissions import IsAdminOrStaffPermission, IsOwnerAuthenticated
from core.decorators import time_calculator
from .serializers import *
from store.models import Category, Order

class CategoryList(ListAPIView):
    # Show the list of Categories
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("name",)
    ordering_fields = ("created",)
    filter_fields = ("created",)

    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        queryset = Category.objects.all()
        self.time()
        return queryset

class CategoryAPIView(RetrieveAPIView):
    # Show one category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)
    
class CategoryAdmin(RetrieveUpdateDestroyAPIView):
    # Manage Get, Put, Post, Update and Batch Categories
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]

class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name='prices__price', lookup_expr='gte')
    max_price = NumberFilter(field_name='prices__price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = []

class ProductList(ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    # filterset_class = ProductFilter
    search_fields = ("name",)
    ordering_fields = ("created",)
    search_fields = ("name", "category__name",)
    filter_fields = ("name", "category__name",) 

    # queryset = Product.objects.all()

    @time_calculator
    def time(self):
        return 0
    
    def get_queryset(self):
        # user = self.request.user
        queryset = Product.objects.filter(is_active=True, is_deleted=False)

        # Filter by category__name if it's provided in the request
        category_name = self.request.query_params.get("category__name")

        if category_name:
            queryset = queryset.filter(category__name=category_name)

        return queryset


    # Cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response(serializer.data)

class ProductAdmin(RetrieveUpdateDestroyAPIView):
    # Manage Get, Put, Post, Update and Batch
    serializer_class = ProductSerializer
    # queryset = Product.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        product = get_object_or_404(Product, id=id, is_active=True, is_deleted=False)
        
        # try:
        #     product = Product.objects.get(id=id, is_active=True, is_deleted=False)
        # except Product.DoesNotExist:
        #     return Response({"detail": "Product not found or not active"}, status=status.HTTP_404_NOT_FOUND)

        # product = Product.objects.get(id=id)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not ProductViews.objects.filter(product=product, ip_address=ip).exists():
            ProductViews.objects.create(product=product, ip_address=ip)
            product.views += 1
            product.save()
        
        serializer = ProductSerializer(product, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        
        # Use the custom permission to check if the user is an admin or staff
        if not IsAdminOrStaffPermission().has_permission(request,self):
            raise PermissionDenied("Only admin users can update products.")

        # Extract the fields you want to update from the request data
        # Exclude fields you don't want to update (e.g., images and prices)
        data = {
            'name': request.data.get('name', product.name),
            'description': request.data.get('description', product.description),
            'category': request.data.get('category', product.category_id),
            'label': request.data.get('label', product.label_id),
            'stock': request.data.get('stock', product.stock),
            # Add more fields as needed
        }

        # Update the product with the modified data
        serializer = ProductSerializer(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)

        if not IsAdminOrStaffPermission().has_permission(request,self):
            raise PermissionDenied("Only admin users can delete products.")
        
        # Save the product with 'is_deleted' set to True
        product.is_deleted = True
        product.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        # Batch update products
        product_uuids = request.data.get("uuids", [])
        new_category = request.data.get("category", None)

        if not IsAdminOrStaffPermission().has_permission(request,self):
            raise PermissionDenied("Only admin users can batch update products.")

        if not product_uuids or new_category is None:
            return Response(
                {"detail": "Please provide 'uuids' and 'category' for batch update."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update products with matching UUIDs to the new category
        updated_count = Product.objects.filter(
            Q(uuid__in=product_uuids) & ~Q(category=new_category)
        ).update(category=new_category)

        return Response(
            {"detail": f"Batch update completed. {updated_count} products updated."},
            status=status.HTTP_200_OK,
        )


class ProductCreateView(CreateAPIView):
    permission_classes = [IsAdminOrStaffPermission]
    serializer_class = ProductDetailSerializer

    def perform_create(self, serializer):
        # Create the product, but don't save it to the database yet
        product = serializer.save()

        # Create a default product price for the newly created product
        currency = Currency.objects.get(code="USD")  # Replace with the desired currency
        default_price = ProductPrice(product=product, currency=currency, price=999.00)  # Set your default price here

        # Now save the product and default price together
        product.save()
        default_price.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class ProductCreateView(CreateAPIView):
#     permission_classes = [IsAdminOrStaffPermission]
#     serializer_class = ProductDetailSerializer

#     def create(self, request, *args, **kwargs):

#         # if not request.user.is_admin or not request.user.is_staff:
#         #     raise PermissionDenied("Only admin users can update products.")
        
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         # push_notifications(user, request.data["title"], "you have add a new product")
#         # if user.profile.phone_number:
#         #     send_message(user.profile.phone_number, "Congratulations, you Created New Product")
#         # logger.info(
#         #     "product ( "
#         #     + str(serializer.data.get("title"))
#         #     + " ) created"
#         #     + " by ( "
#         #     + str(user.username)
#         #     + " )"
#         # )
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductViewsAPIView(ListAPIView):
    permission_classes = [IsOwnerAuthenticated]
    serializer_class = ProductViewsSerializer
    queryset = ProductViews.objects.all()

class ProductPurchaseCountAPIView(ListAPIView):
    permission_classes = [IsOwnerAuthenticated]
    serializer_class = ProductPurchaseCountSerializer
    queryset =  ProductPurchaseCount.objects.all()

class UpdateProductPriceView(UpdateAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    # lookup_field = 'id'  # Set the lookup field to 'id'

    def update(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.id, is_active=True, is_deleted=False)
        print(product)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        currency_code = request.data.get('currency')  # Get the currency code from the request body
        if currency_code:
            serializer.validated_data['currency'] = currency_code  # Set the currency code in the serializer data
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductPriceCreateView(CreateAPIView):
    permission_classes = [IsAdminOrStaffPermission]
    serializer_class = ProductPriceSerializer

    def create(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        # Create a new dictionary with the updated data
        data = {
            'product': product.id,
            'currency': request.data.get('currency'),
            'coupon': request.data.get('coupon'),
            'price': request.data.get('price'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Provide a list of available currencies to the serializer
        context['available_currencies'] = Currency.objects.all()
        return context

class ProductReviewCreateView(CreateAPIView):
    serializer_class = ProductReviewSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.filter(id=self.id)
        return ProductReview.objects.filter(queryset)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     # Automatically set the user based on the authenticated user
    #     serializer.save(user=self.request.user)


class ProductReviewListView(ListAPIView):
    serializer_class = ProductReviewSerializer

    # def get_queryset(self):
    #     queryset = Product.objects.filter(id=self.id)
    #     return ProductReview.objects.filter(product_id=product_id)

class AddToCartView(APIView):
    def post(self, request, id):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the start_date and end_date from request parameters or data
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Check if start_date and end_date are present in the request
        if start_date is None or end_date is None:
            return Response({"error": "start_date or end_date is missing in the request."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Filter ProductPrice objects based on the date
        productprice = ProductPrice.objects.filter(
            product=product,
            start_date__lte=start_date,
            end_date__gte=end_date
        ).first()

        if productprice is None:
            return Response({"error": "Product price not available for the current date"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the user's shopping cart
        shopping_cart, created = CartItem.objects.get_or_create(
            user=request.user,
            item=productprice,
            ordered=False
            )

        print(shopping_cart)
        # Add the selected productprice to the shopping cart
        # shopping_cart.add_to_cart(productprice)

        order_queryset = Order.objects.filter(user=request.user, ordered=False)

        if not order_queryset.exists():
            order = Order.objects.create(user=request.user, ordered_date=timezone.now())
            order.items.add(shopping_cart)
            print("New order is created and item was added to your cart.")

        else:
            order = order_queryset[0]
            if order.items.filter(item_id=shopping_cart.id).exists():
                 shopping_cart.quantity += 1
                 shopping_cart.save()
            else:
                 order.items.add(shopping_cart)
                 print("This item quantity was updated.")



        # if order_queryset.exists():
        #     order = order_queryset[0]
        #     # check if the order item is in the order
        #     if order.items.filter(item_id=item.id).exists():
        #         order_item.quantity += 1
        #         order_item.save()
        #         messages.info(request, "This item quantity was updated.")
        #         return redirect("core:order-summary")
        #     else:
        #         order.items.add(order_item)
        #         messages.info(request, "This item was added to your cart.")
        #         return redirect("core:order-summary")
        # else:
        #     ordered_date = timezone.now()
        #     order = Order.objects.create(
        #         user=request.user, ordered_date=ordered_date)
        #     order.items.add(order_item)
        #     messages.info(request, "This item was added to your cart.")
        #     return redirect("core:order-summary")


        # Serialize the updated shopping cart
        serializer = CartItemSerializer(shopping_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        # http://127.0.0.1:8000/api/product/78b3b6f6-68e1-4b3b-a552-d24fcbf45630/add-to-cart/?start_date=2023-10-15&end_date=2023-10-16



class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'  # You can use 'id' or any other field as needed



class ReservationView(APIView):
    
    def post(self, request, id):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the start_date and end_date from request parameters or data
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Check if start_date and end_date are present in the request
        if start_date is None or end_date is None:
            return Response({"error": "start_date or end_date is missing in the request."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if start_date and end_date are present in the request
        if start_date >= end_date:
            return Response({"error": "End date should be less than start date."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=id)
        
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Filter ProductPrice objects based on the date
        productprice = ProductPrice.objects.filter(
            product=product,
            start_date__lte=start_date,
            end_date__gte=end_date
        ).first()

        if productprice is None:
            return Response({"error": "Product price not available for the current date"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the user's shopping cart
        booking, created = Reservation.objects.get_or_create(
            user=request.user,
            product=product,
            currency=productprice.currency.code,
            price=productprice.price,
            price_discounted=productprice.price,
            start_date=start_date,
            end_date=end_date
        )

        # if the booking is duplicate, what you would like to do
        if not created:
            return Response({"message": "You already have reservation for same dates"}, status=status.HTTP_404_NOT_FOUND)


        # # Add the selected productprice to the shopping cart
        # # shopping_cart.add_to_cart(productprice)

        # order_queryset = Order.objects.filter(user=request.user, ordered=False)

        # if not order_queryset.exists():
        #     order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        #     order.items.add(shopping_cart)
        #     print("New order is created and item was added to your cart.")

        # else:
        #     order = order_queryset[0]
        #     if order.items.filter(item_id=shopping_cart.id).exists():
        #          shopping_cart.quantity += 1
        #          shopping_cart.save()
        #     else:
        #          order.items.add(shopping_cart)
        #          print("This item quantity was updated.")

        # Serialize the updated shopping cart
        serializer = ReservationSerializer(booking)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


