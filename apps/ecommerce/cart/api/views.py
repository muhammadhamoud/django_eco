from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.generics import CreateAPIView
from django.contrib.sessions.backends.db import SessionStore

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.models import Session

# from .models import Cart, CartItems
from store.models import Product, ProductPrice

# from notifications.utils import push_notifications
# from .serializers import CartItemsSerializer, CartItemUpdateSerializer
from django.db.models import Q

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

# from cart.models import Cart, Cartitems
# from cart.serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CartItemSerializer


from cart.services import Cart
from rest_framework.views import APIView

class CartAPI(APIView):
    """
    Single API to handle cart operations
    """
    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()), 
            "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
            )

    def post(self, request, **kwargs):
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                    product=product["product"],
                    quantity=product["quantity"],
                    overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
                )

        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)


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

















# class CartViewSet(CreateModelMixin,RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer


# class CartItemViewSet(ModelViewSet):
    
#     http_method_names = ["get", "post", "patch", "delete"]
    
#     def get_queryset(self):
#         return Cartitems.objects.filter(cart_id=self.kwargs["cart_pk"])
        
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return AddCartItemSerializer
        
#         elif self.request.method == 'PATCH':
#             return UpdateCartItemSerializer
        
#         return CartItemSerializer
    
#     def get_serializer_context(self):
#         return {"cart_id": self.kwargs["cart_pk"]}


# class CartItemAPIView(ListCreateAPIView):
#     serializer_class = CartItemSerializer

#     def get_queryset(self):
#         user = self.request.user
#         session_key = self.request.session.session_key
#         queryset = CartItem.objects.filter(Q(cart__user=user) | Q(cart__session_key=session_key))
#         return queryset

#     def create(self, request, *args, **kwargs):
#         # Check if the user is authenticated
#         if request.user.is_authenticated:
#             user = request.user
#             # Ensure the user has an associated session key
#             session_key = request.session.session_key
#             if session_key is None:
#                 request.session.create()
#                 session_key = request.session.session_key
        
#         elif request.user.AnonymousUser:
#             # If the user is anonymous, create a session and get the session key
#             session = SessionStore()
#             session.create()
#             session_key = session.session_key
#             user = None

#         # cart = get_object_or_404(Cart, user=user)

#         # Create a cart for the user or session key
#         cart, created = Cart.objects.get_or_create(user=user, session_key=session_key)
#         product = get_object_or_404(Product, pk=request.data["product"])
#         current_item = CartItem.objects.filter(cart=cart, product=product)

#         if user == product.user:
#             raise PermissionDenied("This Is Your Product")

#         if current_item.count() > 0:
#             raise NotAcceptable("You already have this item in your shopping cart")

#         try:
#             quantity = int(request.data["quantity"])
#         except Exception as e:
#             raise ValidationError("Please Enter Your Quantity")

#         if quantity > product.quantity:
#             raise NotAcceptable("You order quantity more than the seller have")

#         cart_item = CartItem(cart=cart, product=product, quantity=quantity)
#         cart_item.save()
#         serializer = CartItemSerializer(cart_item)
#         total = float(product.price) * float(quantity)
#         cart.total = total
#         cart.save()
#         # push_notifications(
#         #     cart.user,
#         #     "New cart product",
#         #     "you added a product to your cart " + product.title,
#         # )

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CartItemView(RetrieveUpdateDestroyAPIView):
#     serializer_class = CartItemSerializer
#     # method_serializer_classes = {
#     #     ('PUT',): CartItemUpdateSerializer
#     # }
#     queryset = CartItem.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         if cart_item.cart.user != request.user:
#             raise PermissionDenied("Sorry this cart not belong to you")
#         serializer = self.get_serializer(cart_item)
#         return Response(serializer.data)

#     def update(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         print(request.data)
#         product = get_object_or_404(Product, pk=request.data["product"])

#         if cart_item.cart.user != request.user:
#             raise PermissionDenied("Sorry this cart not belong to you")

#         try:
#             quantity = int(request.data["quantity"])
        
#         except Exception as e:
#             raise ValidationError("Please, input vaild quantity")

#         if quantity > product.quantity:
#             raise NotAcceptable("Your order quantity more than the seller have")

#         serializer = CartItemUpdateSerializer(cart_item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         if cart_item.cart.user != request.user:
#             raise PermissionDenied("Sorry this cart not belong to you")
#         cart_item.delete()
#         # push_notifications(
#         #     cart_item.cart.user,
#         #     "deleted cart product",
#         #     "you have been deleted this product: "
#         #     + cart_item.product.title
#         #     + " from your cart",
#         # )

#         return Response(
#             {"detail": _("your item has been deleted.")},
#             status=status.HTTP_204_NO_CONTENT,
#         )
